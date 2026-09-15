# -*- coding: utf-8 -*-
"""Buyuk acik veri setlerinden AI/insan havuzu toplar.

AMAC "daha cok veri" degil, ZOR ORNEK MADENCILIGI. Bu havuz once mevcut
siniflandiriciyla skorlanir; sonra:

  AI etiketli ama dusuk p(AI)  -> gizlenmis AI ornegi (bizim aradigimiz)
  insan etiketli ama yuksek p(AI) -> zor insan ornegi (yanlis pozitif riski)

Bu iki kume, gizlenmis-AI kafasinin egitim setini elle yazilan 58 ornekten
yuzlerceye cikarir ve — kritik olarak — ornekler artik tek bir modelden
(benden) gelmez. Kaynak cesitliligi, modelin "yapay zeka" yerine
"belirli bir modelin uslubu" ogrenmesini engeller.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from engine import normalize   # noqa: E402

MIN_W, MAX_W = 140, 400
OUT = os.path.join(ROOT, "data", "pool_en.jsonl")


def clean(t):
    if not t:
        return None
    t = re.sub(r"\s+", " ", str(t)).strip()
    t, _ = normalize.normalize(t)
    w = t.split()
    if len(w) < MIN_W:
        return None
    return " ".join(w[:MAX_W])


def collect(want_ai=1800, want_hum=1800):
    from datasets import load_dataset
    ai, hum, seen = [], [], set()

    def add(bucket, text, src, cap):
        t = clean(text)
        if not t or t[:70] in seen or len(bucket) >= cap:
            return
        seen.add(t[:70])
        bucket.append({"text": t, "source": src})

    # 1) eslestirilmis essay verisi — ayni talimat, iki yazar
    try:
        d = load_dataset("dmitva/human_ai_generated_text", split="train", streaming=True)
        for i, r in enumerate(d):
            add(ai, r.get("ai_text"), "dmitva", want_ai // 3)
            add(hum, r.get("human_text"), "dmitva", want_hum // 3)
            if i > 20000 or (len(ai) >= want_ai // 3 and len(hum) >= want_hum // 3):
                break
        print("  dmitva      -> AI %d | insan %d" % (len(ai), len(hum)))
    except Exception as e:
        print("  dmitva HATA:", str(e)[:70])

    # 2) gayriresmi/gizlenmis uslup iceren set
    n0a, n0h = len(ai), len(hum)
    try:
        d = load_dataset("andythetechnerd03/AI-human-text", split="train", streaming=True)
        for i, r in enumerate(d):
            g = r.get("generated")
            is_ai = str(g) in ("1", "1.0", "True", "true")
            add(ai if is_ai else hum, r.get("text"), "andy",
                (want_ai * 2 // 3) if is_ai else (want_hum * 2 // 3))
            if i > 40000 or (len(ai) >= want_ai * 2 // 3 and len(hum) >= want_hum * 2 // 3):
                break
        print("  andy        -> AI +%d | insan +%d" % (len(ai) - n0a, len(hum) - n0h))
    except Exception as e:
        print("  andy HATA:", str(e)[:70])

    # 3) NabeelShar — ek cesitlilik
    n1a, n1h = len(ai), len(hum)
    try:
        d = load_dataset("NabeelShar/ai_and_human_text", split="train", streaming=True)
        for i, r in enumerate(d):
            g = r.get("generated")
            is_ai = str(g) in ("1", "1.0", "True", "true")
            add(ai if is_ai else hum, r.get("text"), "nabeel", want_ai)
            if i > 40000 or (len(ai) >= want_ai and len(hum) >= want_hum):
                break
        print("  nabeel      -> AI +%d | insan +%d" % (len(ai) - n1a, len(hum) - n1h))
    except Exception as e:
        print("  nabeel HATA:", str(e)[:70])

    return ai, hum


def main():
    ai, hum = collect()
    with open(OUT, "w", encoding="utf-8") as f:
        for r in ai:
            f.write(json.dumps({"text": r["text"], "label": 1, "lang": "en",
                                "source": "pool/" + r["source"]}, ensure_ascii=False) + "\n")
        for r in hum:
            f.write(json.dumps({"text": r["text"], "label": 0, "lang": "en",
                                "source": "pool/" + r["source"]}, ensure_ascii=False) + "\n")
    print("\n-> %s : %d AI + %d insan = %d kayit" % (OUT, len(ai), len(hum), len(ai) + len(hum)))


if __name__ == "__main__":
    main()
