# -*- coding: utf-8 -*-
"""Ingilizce AI metinlerini RAID'den ceker.

Iki ayri kume uretilir:
  ai_en.jsonl        saldirisiz (attack == none) — temel dogruluk olcumu
  ai_en_attack.jsonl parafraz / esanlamli / homoglif saldirilari — dayaniklilik olcumu

Eski uretecler (gpt2, gpt3) kasitli olarak sinirlanir: tespiti cok kolaydir,
test setini doldurursa dogruluk yapay olarak sisen bir rakam cikar.
"""
import json
import os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")

MODERN = {"chatgpt", "gpt4", "llama-chat", "mistral-chat", "cohere-chat", "mpt-chat"}
LEGACY = {"gpt2", "gpt3", "mistral", "cohere", "mpt"}
MIN_W, MAX_W = 120, 600
WANT_CLEAN, WANT_ATTACK = 200, 120
LEGACY_CAP = 40
ATTACKS = {"paraphrase", "synonym", "article_deletion", "homoglyph", "whitespace"}


def clip(t):
    w = t.split()
    return " ".join(w[:MAX_W]) if len(w) >= MIN_W else None


def main():
    from datasets import load_dataset
    ds = load_dataset("liamdugan/raid", "raid", split="train", streaming=True)
    clean, attacked = [], []
    legacy_n = 0
    per_model, per_attack = Counter(), Counter()

    for i, r in enumerate(ds):
        model = r.get("model")
        if model in (None, "human"):
            continue
        atk = r.get("attack") or "none"
        t = clip((r.get("generation") or "").strip())
        if not t:
            continue

        if atk == "none" and len(clean) < WANT_CLEAN:
            if model in LEGACY:
                if legacy_n >= LEGACY_CAP:
                    continue
                legacy_n += 1
            elif model not in MODERN:
                continue
            if per_model[model] >= 45:
                continue
            per_model[model] += 1
            clean.append({"text": t, "label": 1, "lang": "en",
                          "source": "raid/" + model, "attack": "none"})

        elif atk in ATTACKS and len(attacked) < WANT_ATTACK:
            if model not in MODERN or per_attack[atk] >= 30:
                continue
            per_attack[atk] += 1
            attacked.append({"text": t, "label": 1, "lang": "en",
                             "source": "raid/" + model, "attack": atk})

        if len(clean) >= WANT_CLEAN and len(attacked) >= WANT_ATTACK:
            break
        if i > 900000:
            break

    for name, rows in (("ai_en.jsonl", clean), ("ai_en_attack.jsonl", attacked)):
        with open(os.path.join(DATA, name), "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print("  -> %s (%d kayit)" % (name, len(rows)))
    print("  uretec dagilimi:", dict(per_model))
    print("  saldiri dagilimi:", dict(per_attack))


if __name__ == "__main__":
    main()
