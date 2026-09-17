# -*- coding: utf-8 -*-
"""Turkce AI setini birlestirip data/ai_tr.jsonl yazar."""
import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import ai_tr_long_1, ai_tr_long_2, ai_tr_long_3, ai_tr_long_4   # noqa: E402
import ai_tr_samples                                      # noqa: E402

rows = (ai_tr_long_1.rows() + ai_tr_long_2.rows() + ai_tr_long_3.rows()
        + ai_tr_long_4.rows())
short = ai_tr_samples.all_samples()          # ilk kisa set: ayri dosyada saklanir

out = os.path.join(os.path.dirname(HERE), "data")
with open(os.path.join(out, "ai_tr.jsonl"), "w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
with open(os.path.join(out, "ai_tr_short.jsonl"), "w", encoding="utf-8") as f:
    for r in short:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

ws = sorted(len(r["text"].split()) for r in rows)
print("ai_tr.jsonl        %d ornek | kelime: min %d, medyan %d, max %d"
      % (len(rows), ws[0], ws[len(ws) // 2], ws[-1]))
for k, v in sorted(collections.Counter(r["source"] for r in rows).items()):
    print("   %-26s %d" % (k, v))
print("ai_tr_short.jsonl  %d ornek (kisa metin testi icin ayri tutuldu)" % len(short))
