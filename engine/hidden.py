# -*- coding: utf-8 -*-
"""Katman 4 — gizlenmis yapay zeka metni tespiti.

NEDEN VAR: desklib siniflandiricisinin son katmani RAID'de egitildi ve
"insan gibi yaz" talimatiyla uretilmis metni yakalayamiyordu (olcum:
0/10, AUC 0.759). Ayni modelin GOVDE GOMULERI ise bu bilgiyi tasiyor;
uzerine egitilen kucuk bir lojistik kafa, gormedigi veride 1.000 AUC
verdi ve bagimsiz bir gizlenmis AI metnini 0.9926 ile yakaladi.

Egitim: eval/train_hidden.py — 58 gizlenmis AI + 40 kolay AI karsisinda
116 gayriresmi (Reddit) + 40 resmi insan metni. Insan tarafinin uslup
olarak eslesmesi sart: aksi halde model yapay zekayi degil kisisel uslubu
ogrenir.

BELLEK: ek model yuklemez. Siniflandirici zaten bellekte olan desklib
govdesini kullanir; gomu ayni ileri gecisten alinir.
"""
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
HEAD_PATH = os.path.join(HERE, "hidden_head.npz")

_head = None


# Kafa, desklib govdesinin 1024 boyutlu gomuleri uzerinde egitildi.
# Turkce siniflandirici (BERTurk) 768 boyut uretir; o gomulerle bu kafa
# kullanilamaz. Turkce icin ayri bir kafa egitilmesi gerekir ve bunun icin
# once Turkce gizlenmis AI ornekleri toplanmalidir.
SUPPORTED_LANGS = ("en",)


def available(lang="en"):
    return lang in SUPPORTED_LANGS and os.path.exists(HEAD_PATH)


def _load():
    global _head
    if _head is None and available():
        z = np.load(HEAD_PATH)
        _head = {k: z[k] for k in z.files}
    return _head


def quality():
    h = _load()
    return float(h["auc"]) if h is not None and "auc" in h else None


def score(embeddings):
    """Gomu matrisi (n, hidden) -> p(gizlenmis AI) listesi.

    Boyut uyusmazsa (baska bir govdenin gomusu) notr 0.5 doner; sessizce
    yanlis sonuc uretmektense katman devre disi kalir.
    """
    h = _load()
    emb = np.asarray(embeddings, dtype=np.float64)
    if h is None or emb.ndim != 2 or emb.shape[1] != h["mean"].shape[0]:
        return [0.5] * len(emb)
    x = (emb - h["mean"]) / h["scale"]
    z = x @ h["coef"] + h["intercept"]
    return (1.0 / (1.0 + np.exp(-np.clip(z, -30, 30)))).tolist()
