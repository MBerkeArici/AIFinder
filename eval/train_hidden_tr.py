# -*- coding: utf-8 -*-
"""Turkce "gizlenmis AI" kafasini egitir -> engine/hidden_head_tr.npz

NEDEN: eval/report.md'ye gore Turkce ensemble TPR@FPR1% yalnizca ~%48.
Ingilizce'yi %100'e tasiyan sey 'gizlenmis' katmani (AUC 0.994); Turkce'de
bu katman hic yoktu. Bu betik onu ekler.

YONTEM: Ingilizce'deki kesif Turkce'ye de uygulanir — siniflandiricinin
KAFASI zayif olabilir ama GOVDE GOMULERI ayrimi tasir. BERTurk govdesinin
768 boyutlu ortalama gomuleri uzerine kucuk bir lojistik kafa egitilir.
Ek model yuklenmez: govde zaten Turkce siniflandirici icin bellekte.

USLUP DENGESI (en kritik nokta): AI ornekleri gunluk/samimi uslupta yazildi.
Insan tarafi yalnizca haber ve Vikipedi olsaydi model "samimi yazi = AI"
gibi ters ve zararli bir kural ogrenirdi. Bu yuzden insan tarafinin agirligi
gayriresmi metinden (human_tr_informal.jsonl) gelir, resmi metin azinlikta
tutulur.

DURUSTLUK UYARISI: elde yalnizca ~52 Turkce AI ornegi var (Ingilizce'de
madencilikle binlerce vardi). Bu boyutta tek bir egitim/test ayrimi
rastlantiya cok acik, bu yuzden tekrarli capraz dogrulama kullanilir ve
raporlanan AUC, egitimde hic gorulmemis katlardan (out-of-fold) gelir.
Yine de bu rakam genis bir guven araligi tasir; kucuk veri gercegi
raporda belirtilmelidir.
"""
import json
import os
import sys

import numpy as np
import torch

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)

from engine import memory, normalize                    # noqa: E402
from engine.classifier import TR_MODEL, pick_device     # noqa: E402

MAX_W = 140                       # run_eval.py ve train_hidden2.py ile ayni bant
OUT = os.path.join(ROOT, "engine", "hidden_head_tr.npz")
MIN_AUC = 0.75                    # bunun altinda kafa yazilmaz


def load_jsonl(path, limit=None, kind=None, label=None):
    rows, p = [], os.path.join(ROOT, "data", path)
    if not os.path.exists(p):
        return rows
    with open(p, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            t, _ = normalize.normalize(r["text"])
            w = t.split()
            if len(w) < MAX_W:
                continue
            r["text"] = " ".join(w[:MAX_W])
            if kind:
                r["kind"] = kind
            if label is not None:
                r["label"] = label
            rows.append(r)
            if limit and len(rows) >= limit:
                break
    return rows


@torch.inference_mode()
def embed(texts, bs=8, tag=""):
    """BERTurk govdesinin ortalama gomuleri (n, 768)."""
    from transformers import AutoModel, AutoTokenizer

    dev = pick_device()
    tok = AutoTokenizer.from_pretrained(TR_MODEL)
    mdl = AutoModel.from_pretrained(TR_MODEL).to(dev).eval()

    out = []
    for i in range(0, len(texts), bs):
        enc = tok(texts[i:i + bs], return_tensors="pt", padding=True,
                  truncation=True, max_length=512).to(dev)
        hid = mdl(enc["input_ids"], attention_mask=enc["attention_mask"])[0]
        m = enc["attention_mask"].unsqueeze(-1).expand(hid.size()).float()
        out.append(((hid * m).sum(1) / m.sum(1).clamp(min=1e-9)).float().cpu().numpy())
        if (i // bs) % 10 == 0:
            print("  %s gomu %d/%d" % (tag, min(i + bs, len(texts)), len(texts)), flush=True)
    del mdl
    memory.release()
    return np.vstack(out)


def main():
    memory.acquire("train_hidden_tr", need_gb=1.5)   # BERTurk base (~0.45 GB) + gomuler
    try:
        # EGITIM/OLCUM AYRIMI — bu ayrim bozulursa rapor yalan soyler.
        #
        # run_eval.py Turkce olcumu su iki dosyadan yapar:
        #     ai_tr.jsonl  +  human_tr.jsonl
        # Bu yuzden ikisi de egitimde KULLANILMAZ. Aksi halde 'gizlenmis'
        # sinyali kendi egitim verisi uzerinde olculur, AUC yapay olarak
        # 1.000'e firlar ve arayuzde gosterilen dogruluk gercek disi olur.
        # (train_hidden2.py'de Ingilizce icin ayni hata bir kez yapilmis ve
        # dosyanin basinda not edilmis.)
        ai = load_jsonl("ai_tr_hidden.jsonl", kind="gizlenmis_ai", label=1)

        # Insan tarafi IKI usluptan da beslenmeli.
        #
        # Ilk surumde yalnizca birlestirilmis urun yorumlari kullanilmisti ve
        # sonuc olcumde gorundu: insan metinlerinin ortalama skoru 0.524, ust
        # ceyregi 0.97. Model "insan"i degil "birlestirilmis kisa yorum"u
        # ogrenmis, akici yazilmis haber/ansiklopedi metnini yapay zeka
        # saniyordu. Resmi metin eklenmeden bu duzelmiyor.
        #
        # human_tr_formal_train.jsonl, olcum setiyle (human_tr.jsonl)
        # kesismeyecek sekilde toplanir — bkz. build_human.formal_tr_train.
        informal = load_jsonl("human_tr_informal.jsonl", limit=max(len(ai) * 2, 60),
                              kind="gayriresmi_insan", label=0)
        formal = load_jsonl("human_tr_formal_train.jsonl", limit=max(len(ai) * 2, 60),
                            kind="resmi_insan", label=0)
        if not formal:
            print("UYARI: human_tr_formal_train.jsonl yok — resmi insan metni olmadan")
            print("       egitilen kafa duzgun yazilmis metni AI sanma egiliminde olur.")
            print("       Once: .venv/bin/python eval/build_human.py formal-train")
        human = informal + formal

        if len(ai) < 20 or len(human) < 25:
            print("HATA: veri yetersiz (AI %d, insan %d). Once:" % (len(ai), len(human)))
            print("  .venv/bin/python eval/ai_tr_hidden.py")
            print("  .venv/bin/python eval/build_human.py informal")
            return

        rows = ai + human
        from collections import Counter
        print("VERI: %d ornek  %s" % (len(rows), dict(Counter(r["kind"] for r in rows))))
        print("      insan tarafi: %%%.0f gayriresmi / %%%.0f resmi"
              % (100.0 * len(informal) / max(1, len(human)),
                 100.0 * len(formal) / max(1, len(human))))
        print("      (tek uslup baskin olursa model uslubu ogrenir, yapay zekayi degil)")

        X = embed([r["text"] for r in rows], tag="gomu")
        y = np.array([r["label"] for r in rows])

        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import roc_auc_score
        from sklearn.model_selection import RepeatedStratifiedKFold
        from sklearn.pipeline import make_pipeline
        from sklearn.preprocessing import StandardScaler

        def build():
            return make_pipeline(
                StandardScaler(),
                LogisticRegression(max_iter=4000, C=0.05, class_weight="balanced"))

        # --- durust olcum: out-of-fold, tekrarli
        cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=4, random_state=42)
        aucs, oof_all = [], []
        for tr, te in cv.split(X, y):
            m = build()
            m.fit(X[tr], y[tr])
            p = m.predict_proba(X[te])[:, 1]
            if len(set(y[te])) > 1:
                aucs.append(roc_auc_score(y[te], p))
            oof_all.append((te, p))
        auc_mean, auc_sd = float(np.mean(aucs)), float(np.std(aucs))

        # kat ortalamasiyla birlestirilmis oof -> esik/kalibrasyon icin
        oof = np.zeros(len(y)); cnt = np.zeros(len(y))
        for te, p in oof_all:
            oof[te] += p; cnt[te] += 1
        oof /= np.maximum(cnt, 1)

        human_scores = np.sort(oof[y == 0])[::-1]
        k = max(1, int(len(human_scores) * 0.01))
        thr = human_scores[k - 1]
        tpr1 = float((oof[y == 1] >= thr).mean())

        print("\n=== CAPRAZ DOGRULAMA (egitimde gorulmemis katlar) ===")
        print("  AUC        : %.4f  (± %.4f, %d kat)" % (auc_mean, auc_sd, len(aucs)))
        print("  TPR@FPR1%%  : %.1f%%" % (tpr1 * 100))
        print("  ornek      : %d AI / %d insan" % (int(y.sum()), int((1 - y).sum())))
        print("  UYARI: kucuk veri — bu rakamlarin guven araligi genistir.")

        if auc_mean < MIN_AUC:
            print("\nAUC %.3f < %.2f — kafa YAZILMADI." % (auc_mean, MIN_AUC))
            print("Once daha fazla Turkce AI ornegi toplanmali.")
            return

        final = build()
        final.fit(X, y)
        sc, lr = final[0], final[-1]
        np.savez(OUT, mean=sc.mean_, scale=sc.scale_,
                 coef=lr.coef_[0], intercept=lr.intercept_[0],
                 auc=auc_mean, auc_sd=auc_sd, tpr_at_fpr1=tpr1,
                 n=len(rows), n_ai=int(y.sum()), dim=X.shape[1])
        print("\n-> %s yazildi (boyut %d)" % (OUT, X.shape[1]))
        print("   Sonraki adim: .venv/bin/python eval/calibrate_lang.py tr")
    finally:
        memory.release_lock()


if __name__ == "__main__":
    main()
