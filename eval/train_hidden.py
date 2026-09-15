# -*- coding: utf-8 -*-
"""Gizlenmis AI metnini yakalamak icin gomu-tabanli siniflandirici.

NEDEN TAM FINE-TUNE DEGIL: elde 58 gizlenmis ornek var. Bu sayida veriyle
430M parametreli bir modeli fine-tune etmek neredeyse kesin ezberleme
uretir; capraz dogrulama iyi gorunur, gercek metinde coker.

Bunun yerine: desklib govdesinin GOMULERI (son katman ortalamasi) sabit
ozellik olarak cikarilir ve ustune kucuk bir lojistik regresyon egitilir.
Az veriyle saglam calisir, ezberlemesi zordur ve capraz dogrulamasi
durustur.

Insan tarafi Reddit'in gayriresmi birinci sahis anlatilaridir; gizlenmis AI
ornekleriyle uslup olarak eslesir. Bu esleme olmadan model "yapay zeka"yi
degil "kisisel uslup"u ogrenir.
"""
import json
import os
import sys

import numpy as np
import torch

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from engine import normalize          # noqa: E402
from engine.classifier import EN_MODEL, _DesklibModel, pick_device  # noqa: E402

MAX_W = 140
OUT = os.path.join(ROOT, "engine", "hidden_head.npz")


def load(path, limit=None):
    rows = []
    with open(os.path.join(ROOT, "data", path), encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            t, _ = normalize.normalize(r["text"])
            w = t.split()
            if len(w) < MAX_W:
                continue
            rows.append(" ".join(w[:MAX_W]))
            if limit and len(rows) >= limit:
                break
    return rows


@torch.inference_mode()
def embed(texts, bs=8):
    """desklib govdesinin mean-pooled son katman gomuleri."""
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
        mask = enc["attention_mask"].unsqueeze(-1).expand(hid.size()).float()
        pooled = (hid * mask).sum(1) / mask.sum(1).clamp(min=1e-9)
        out.append(pooled.float().cpu().numpy())
        print("  gomu %d/%d" % (min(i + bs, len(texts)), len(texts)), flush=True)
    del mdl
    import gc; gc.collect()
    if dev == "mps":
        torch.mps.empty_cache()
    return np.vstack(out)


def main():
    hidden = load("ai_en_hidden.jsonl")
    human = load("human_en_informal.jsonl", limit=len(hidden) * 2)
    easy = load("ai_en.jsonl", limit=40)
    formal = load("human_en.jsonl", limit=40)

    print("veri: %d gizlenmis AI | %d gayriresmi insan | %d kolay AI | %d resmi insan"
          % (len(hidden), len(human), len(easy), len(formal)))

    texts = hidden + easy + human + formal
    y = np.array([1] * (len(hidden) + len(easy)) + [0] * (len(human) + len(formal)))
    grp = np.array(["gizli"] * len(hidden) + ["kolay"] * len(easy)
                   + ["gayriresmi"] * len(human) + ["resmi"] * len(formal))

    X = embed(texts)
    print("gomu boyutu:", X.shape)

    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import StratifiedKFold
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import roc_auc_score

    oof = np.zeros(len(y))
    for tr, te in StratifiedKFold(5, shuffle=True, random_state=0).split(X, y):
        m = make_pipeline(StandardScaler(),
                          LogisticRegression(max_iter=3000, C=0.05, class_weight="balanced"))
        m.fit(X[tr], y[tr])
        oof[te] = m.predict_proba(X[te])[:, 1]

    print("\nCAPRAZ DOGRULAMA (gormedigi veride):")
    print("  genel AUC: %.3f" % roc_auc_score(y, oof))
    hid_mask = grp == "gizli"
    hum_mask = (grp == "gayriresmi")
    yy = np.concatenate([np.zeros(hum_mask.sum()), np.ones(hid_mask.sum())])
    ss = np.concatenate([oof[hum_mask], oof[hid_mask]])
    print("  gizlenmis AI vs gayriresmi insan AUC: %.3f   <- ASIL OLCU" % roc_auc_score(yy, ss))
    for g in ("gizli", "kolay", "gayriresmi", "resmi"):
        m = grp == g
        print("    %-12s ortalama skor %.3f (n=%d)" % (g, oof[m].mean(), m.sum()))

    final = make_pipeline(StandardScaler(),
                          LogisticRegression(max_iter=3000, C=0.05, class_weight="balanced"))
    final.fit(X, y)
    sc, lr = final[0], final[-1]
    np.savez(OUT, mean=sc.mean_, scale=sc.scale_, coef=lr.coef_[0],
             intercept=lr.intercept_, auc=roc_auc_score(yy, ss))
    print("\n-> %s yazildi" % OUT)


if __name__ == "__main__":
    main()
