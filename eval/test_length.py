# -*- coding: utf-8 -*-
"""Uzunluk bandi olcumu — kisa metinde arac ne kadar guvenilir?

NEDEN VAR: analyze.py 85 kelimeden itibaren sonuc uretiyor (MIN_WORDS=85),
ama butun olcumler 140 kelimede yapildi. Yani 85-140 arasindaki davranis
hic bilinmiyordu. Kullanici 90 kelimelik bir metin yapistirdiginda arayuz
yuzde gosteriyor ve o yuzdenin ne kadar guvenilir oldugunu soyleyemiyorduk.

data/ai_tr_short.jsonl (47 ornek, 87-131 kelime) bu amacla toplanmisti ama
hicbir olcumde kullanilmiyordu.

YONTEM: ayni metinler farkli uzunluklara kirpilir ve her bantta ayri ayri
olculur. Boylece uzunlugun tek basina etkisi gorulur — farkli metinler
karsilastirilsaydi, aradaki fark uzunluktan mi metinden mi geldigi
bilinemezdi.
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)

import features          # noqa: E402
import run_eval as ev    # noqa: E402

BANDS = [85, 110, 140, 200, 300]
MAX_HUMAN = 90           # olcum suresini makul tutmak icin


def pool(path, limit=None):
    p = os.path.join(DATA, path)
    if not os.path.exists(p):
        return []
    out = []
    with open(p, encoding="utf-8") as f:
        for line in f:
            out.append(json.loads(line))
            if limit and len(out) >= limit:
                break
    return out


def band_rows(rows, n):
    """Metinleri tam n kelimeye kirp; kisa olanlari ele."""
    out = []
    for r in rows:
        w = r["text"].split()
        if len(w) < n:
            continue
        c = dict(r)
        c["text"] = " ".join(w[:n])
        out.append(c)
    return out


def main():
    ai_all = pool("ai_tr_short.jsonl") + pool("ai_tr.jsonl")
    human_all = pool("human_tr.jsonl", MAX_HUMAN)

    out = ["# Uzunluk Bandı Ölçümü", "",
           "Aynı metinler farklı uzunluklara kırpılıp her bantta ayrı ölçüldü.",
           "Böylece uzunluğun tek başına etkisi görünür.", "",
           "| Kelime | AI örnek | İnsan örnek | ROC-AUC | TPR @ FPR %1 |",
           "|---:|---:|---:|---:|---:|"]
    results = []

    for n in BANDS:
        ai = band_rows(ai_all, n)
        hu = band_rows(human_all, n)
        if len(ai) < 10 or len(hu) < 20:
            print("%d kelime: yetersiz ornek (AI %d, insan %d)" % (n, len(ai), len(hu)))
            continue
        rows = ai + hu
        print("%d kelime bandi: %d AI + %d insan" % (n, len(ai), len(hu)), flush=True)
        features.compute(rows, verbose=False)

        y = [r["label"] for r in rows]
        sig = ev.signals(rows)
        names = [k for k in sig if k != "siniflandirici"] + ["siniflandirici"]
        _, model, _ = ev.fit_ensemble(rows, list(sig.keys()))
        X = np.column_stack([sig[k] for k in sig])
        # capraz dogrulama disi tahmin yerine, kalibre motorun kendi ciktisi
        from engine import ensemble as eng
        probs = []
        for r in rows:
            p, _ = eng.probability(r["feat"], "tr")
            probs.append(p)
        auc = ev.auc(y, probs)
        tpr, thr = ev.tpr_at_fpr(y, probs)
        results.append((n, len(ai), len(hu), auc, tpr))
        out.append("| %d | %d | %d | %.3f | %.1f%% |" % (n, len(ai), len(hu), auc, tpr * 100))
        print("   AUC %.3f | TPR@FPR1%% %.1f%%" % (auc, tpr * 100), flush=True)

    if results:
        best = max(r[3] for r in results)
        worst = min(r[3] for r in results)
        out.append("")
        out.append("**Okuma notu.** Bu tablo üretimdeki kalibre motorun çıktısıyla")
        out.append("hesaplandı (engine/calibration.json), yani kullanıcının gördüğü")
        out.append("karar mekanizmasının ta kendisi. Kalibrasyon 140 kelime bandında")
        out.append("yapıldığı için diğer bantlarda eşik ideal olmayabilir; AUC sütunu")
        out.append("eşikten bağımsız olduğu için ayırt etme gücünü daha iyi gösterir.")
        out.append("")
        out.append("AUC en düşük %.3f, en yüksek %.3f." % (worst, best))

    path = os.path.join(HERE, "report_length.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print("\n-> eval/report_length.md yazildi")
    print("\n".join(out))


if __name__ == "__main__":
    main()
