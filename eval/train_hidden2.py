# -*- coding: utf-8 -*-
"""Gizlenmis AI kafasini MADENDEN gelen veriyle yeniden egitir.

ONCEKI SURUMUN SORUNU: 58 ornegin tamami elle yazilmisti ve hepsi tek bir
model ailesinden geliyordu. Model "yapay zeka"yi degil "o modelin uslubunu"
ogrenmis olabilirdi. Ayrica olcum, egitim verisinin uzerinde yapildigi icin
AUC 1.000 cikiyordu — o rakam gecersizdi.

BU SURUM:
  - Egitim verisi mine_hard.py'nin uc acik veri setinden ayikladigi zor
    orneklerden gelir (cok kaynakli).
  - Elle yazilan ornekler de eklenir ama artik azinliktadir.
  - TEST BOLUMU EGITIMDE ASLA KULLANILMAZ. Raporlanan rakam bu bolumden
    gelir ve durusttur.
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

from engine import normalize                                   # noqa: E402
from engine.classifier import EN_MODEL, _DesklibModel, pick_device  # noqa: E402

MAX_W = 140
OUT = os.path.join(ROOT, "engine", "hidden_head.npz")


def load_jsonl(path, limit=None):
    rows = []
    p = os.path.join(ROOT, "data", path)
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
            rows.append(r)
            if limit and len(rows) >= limit:
                break
    return rows


@torch.inference_mode()
def embed(texts, bs=8, tag=""):
    from transformers import AutoTokenizer
    from huggingface_hub import hf_hub_download
    from safetensors.torch import load_file

    dev = pick_device()
    tok = AutoTokenizer.from_pretrained(EN_MODEL)
    mdl = _DesklibModel(EN_MODEL)
    mdl.load_state_dict(load_file(hf_hub_download(EN_MODEL, "model.safetensors")), strict=False)
    mdl.to(dev).eval()

    out = []
    for i in range(0, len(texts), bs):
        enc = tok(texts[i:i + bs], return_tensors="pt", padding=True,
                  truncation=True, max_length=512).to(dev)
        hid = mdl.model(enc["input_ids"], attention_mask=enc["attention_mask"])[0]
        m = enc["attention_mask"].unsqueeze(-1).expand(hid.size()).float()
        out.append(((hid * m).sum(1) / m.sum(1).clamp(min=1e-9)).float().cpu().numpy())
        if (i // bs) % 10 == 0:
            print("  %s gomu %d/%d" % (tag, min(i + bs, len(texts)), len(texts)), flush=True)
    del mdl
    import gc; gc.collect()
    if dev == "mps":
        torch.mps.empty_cache()
    return np.vstack(out)


def main():
    train = load_jsonl("mined_train.jsonl")
    test = load_jsonl("mined_test.jsonl")
    handwritten = load_jsonl("ai_en_hidden.jsonl")
    informal = load_jsonl("human_en_informal.jsonl", limit=140)

    # Akademik insan metni — Turkce tarafta ogrenilen dersin Ingilizce'ye
    # uygulanmasi. Insan tarafi yalnizca Reddit + madencilik havuzu oldugunda
    # model resmi/yogun akademik yazimi yapay zeka sanma egiliminde oluyor:
    # canli taramada Reddit'te 0/25, bilimsel makale ozetlerinde 2/25 yanlis
    # pozitif cikti. human_en_formal_train.jsonl olcum setiyle (human_en.jsonl)
    # kesismeyecek sekilde toplanir — bkz. build_human.formal_en_train.
    formal = load_jsonl("human_en_formal_train.jsonl", limit=130)
    if not formal:
        print("UYARI: human_en_formal_train.jsonl yok — akademik insan metni")
        print("       olmadan egitilen kafa ozet/makale metnini AI sanabilir.")
        print("       Once: .venv/bin/python eval/build_human.py formal-en")

    if not train:
        print("HATA: mined_train.jsonl yok — once eval/mine_hard.py calistirin")
        return

    # elle yazilan ornekler ve gayriresmi insan metni egitime katilir
    for r in handwritten:
        r["kind"] = "elle_zor_ai"; r["label"] = 1
    for r in informal:
        r["kind"] = "gayriresmi_insan"; r["label"] = 0
    for r in formal:
        r["kind"] = "akademik_insan"; r["label"] = 0

    tr_rows = train + handwritten + informal + formal
    te_rows = test

    from collections import Counter
    print("EGITIM: %d  %s" % (len(tr_rows), dict(Counter(r.get("kind", "?") for r in tr_rows))))
    print("TEST  : %d  %s" % (len(te_rows), dict(Counter(r.get("kind", "?") for r in te_rows))))

    Xtr = embed([r["text"] for r in tr_rows], tag="egitim")
    ytr = np.array([r["label"] for r in tr_rows])
    Xte = embed([r["text"] for r in te_rows], tag="test")
    yte = np.array([r["label"] for r in te_rows])

    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import roc_auc_score

    model = make_pipeline(StandardScaler(),
                          LogisticRegression(max_iter=4000, C=0.05, class_weight="balanced"))
    model.fit(Xtr, ytr)
    pte = model.predict_proba(Xte)[:, 1]

    print("\n=== BAGIMSIZ TEST (egitimde hic kullanilmadi) ===")
    auc = roc_auc_score(yte, pte) if len(set(yte)) > 1 else float("nan")
    print("  genel AUC: %.3f  (n=%d)" % (auc, len(yte)))

    kinds = np.array([r.get("kind", "?") for r in te_rows])
    for k in sorted(set(kinds)):
        m = kinds == k
        print("    %-14s ortalama skor %.3f  (n=%d)" % (k, pte[m].mean(), m.sum()))

    zor_ai = kinds == "zor_ai"
    ins = np.isin(kinds, ["zor_insan", "kolay_insan"])
    if zor_ai.sum() and ins.sum():
        yy = np.concatenate([np.zeros(ins.sum()), np.ones(zor_ai.sum())])
        ss = np.concatenate([pte[ins], pte[zor_ai]])
        auc_hard = roc_auc_score(yy, ss)
        thr = np.percentile(pte[ins], 95)
        print("\n  ZOR AI vs INSAN AUC: %.3f   <- ASIL OLCU" % auc_hard)
        print("  yanlis pozitif %%5 esiginde yakalama: %.1f%%" % (100 * (pte[zor_ai] >= thr).mean()))
    else:
        auc_hard = auc

    sc, lr = model[0], model[-1]
    np.savez(OUT, mean=sc.mean_, scale=sc.scale_, coef=lr.coef_[0],
             intercept=lr.intercept_, auc=float(auc_hard))
    print("\n-> %s guncellendi (auc=%.3f)" % (OUT, auc_hard))


if __name__ == "__main__":
    main()
