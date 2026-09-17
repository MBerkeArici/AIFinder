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
HEAD_PATH = os.path.join(HERE, "hidden_head.npz")          # Ingilizce (desklib govdesi)
HEAD_PATH_TR = os.path.join(HERE, "hidden_head_tr.npz")    # Turkce (BERTurk govdesi)

_heads = {}


def _head_path(lang):
    return HEAD_PATH_TR if lang == "tr" else HEAD_PATH


# Her dilin kafasi kendi govdesinin gomuleri uzerinde egitilir ve boyutlari
# farklidir: desklib 1024, BERTurk 768. Kafa dosyasi yoksa ya da boyut
# uymuyorsa katman sessizce devre disi kalir (score() notr 0.5 doner) —
# yanlis boyutla yanlis sonuc uretmektense hic uretmemek dogru.
#
# Turkce kafa icin egitim verisi: eval/ai_tr_hidden.py (gizlenmis AI) ve
# data/human_tr_informal.jsonl (uslupca eslesen insan metni).
# Egitim: eval/train_hidden_tr.py
SUPPORTED_LANGS = ("en", "tr")


def available(lang="en"):
    return lang in SUPPORTED_LANGS and os.path.exists(_head_path(lang))


def _load(lang="en"):
    if lang not in _heads:
        path = _head_path(lang)
        if not (lang in SUPPORTED_LANGS and os.path.exists(path)):
            _heads[lang] = None
        else:
            z = np.load(path)
            _heads[lang] = {k: z[k] for k in z.files}
    return _heads[lang]


def quality(lang="en"):
    h = _load(lang)
    return float(h["auc"]) if h is not None and "auc" in h else None


def score(embeddings, lang="en"):
    """Gomu matrisi (n, hidden) -> p(gizlenmis AI) listesi.

    Boyut uyusmazsa (baska bir govdenin gomusu) notr 0.5 doner; sessizce
    yanlis sonuc uretmektense katman devre disi kalir.
    """
    h = _load(lang)
    emb = np.asarray(embeddings, dtype=np.float64)
    if h is None or emb.ndim != 2 or emb.shape[1] != h["mean"].shape[0]:
        return [0.5] * len(emb)
    x = (emb - h["mean"]) / h["scale"]
    z = x @ h["coef"] + h["intercept"]
    return (1.0 / (1.0 + np.exp(-np.clip(z, -30, 30)))).tolist()
