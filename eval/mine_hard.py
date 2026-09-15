# -*- coding: utf-8 -*-
"""Zor ornek madenciligi.

Havuzdaki 3600 metni mevcut siniflandiriciyla skorlar ve MODELIN YANILDIGI
ornekleri ayiklar:

  AI etiketli, dusuk p(AI)     -> gizlenmis AI  (yakalayamadigimiz kume)
  insan etiketli, yuksek p(AI) -> zor insan     (yanlis pozitif riski)

Bu, elle yazilan 58 ornegi yuzlerce gercek ornekle degistirir ve kaynak
cesitliligi saglar: ornekler artik tek bir modelden gelmiyor.

Ayrica veriyi EGITIM ve TEST olarak boler. Onceki turda gizlenmis kafa
kendi egitim verisiyle olculdugu icin AUC 1.000 cikmisti; o rakam
gecersizdi. Test bolumu egitimde asla kullanilmaz.
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

POOL = os.path.join(ROOT, "data", "pool_en.jsonl")
OUT_TRAIN = os.path.join(ROOT, "data", "mined_train.jsonl")
OUT_TEST = os.path.join(ROOT, "data", "mined_test.jsonl")
SCORES = os.path.join(ROOT, "data", "pool_scores.npy")


def main():
    from engine import classifier

    rows = [json.loads(l) for l in open(POOL, encoding="utf-8")]
    print("havuz: %d metin" % len(rows))

    if os.path.exists(SCORES):
        probs = np.load(SCORES)
        print("skorlar onbellekten alindi")
    else:
        clf = classifier.get("en")
        probs = []
        bs = 8
        for i in range(0, len(rows), bs):
            chunk = [r["text"] for r in rows[i:i + bs]]
            probs += list(clf.predict(chunk))
            if (i // bs) % 25 == 0:
                print("  %d/%d" % (min(i + bs, len(rows)), len(rows)), flush=True)
        probs = np.array(probs)
        np.save(SCORES, probs)

    y = np.array([r["label"] for r in rows])
    ai_p, hum_p = probs[y == 1], probs[y == 0]
    print("\nmevcut siniflandirici havuzda:")
    print("  AI   metinleri p(AI): medyan %.3f | 0.5 altinda %d/%d" %
          (np.median(ai_p), (ai_p < 0.5).sum(), len(ai_p)))
    print("  insan metinleri p(AI): medyan %.3f | 0.5 ustunde %d/%d" %
          (np.median(hum_p), (hum_p > 0.5).sum(), len(hum_p)))

    hard_ai = [r for r, p in zip(rows, probs) if r["label"] == 1 and p < 0.5]
    hard_hum = [r for r, p in zip(rows, probs) if r["label"] == 0 and p > 0.5]
    easy_ai = [r for r, p in zip(rows, probs) if r["label"] == 1 and p >= 0.9]
    easy_hum = [r for r, p in zip(rows, probs) if r["label"] == 0 and p <= 0.1]

    print("\nmadencilik sonucu:")
    print("  zor AI  (kacirilan)      : %d" % len(hard_ai))
    print("  zor insan (yanlis poz.)  : %d" % len(hard_hum))
    print("  kolay AI                 : %d" % len(easy_ai))
    print("  kolay insan              : %d" % len(easy_hum))

    rng = np.random.default_rng(3)

    def split(items, frac=0.3):
        items = list(items)
        rng.shuffle(items)
        k = max(1, int(len(items) * frac)) if items else 0
        return items[k:], items[:k]

    tr_ha, te_ha = split(hard_ai)
    tr_hh, te_hh = split(hard_hum)
    tr_ea, te_ea = split(easy_ai[:400])
    tr_eh, te_eh = split(easy_hum[:400])

    def tag(items, kind):
        return [{**r, "kind": kind} for r in items]

    train = (tag(tr_ha, "zor_ai") + tag(tr_hh, "zor_insan")
             + tag(tr_ea, "kolay_ai") + tag(tr_eh, "kolay_insan"))
    test = (tag(te_ha, "zor_ai") + tag(te_hh, "zor_insan")
            + tag(te_ea, "kolay_ai") + tag(te_eh, "kolay_insan"))

    for path, data in ((OUT_TRAIN, train), (OUT_TEST, test)):
        with open(path, "w", encoding="utf-8") as f:
            for r in data:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print("  -> %s : %d" % (os.path.basename(path), len(data)))


if __name__ == "__main__":
    main()
