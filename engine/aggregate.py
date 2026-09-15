# -*- coding: utf-8 -*-
"""Pencere olasiliklarindan belge yuzdesi.

Turnitin'in yaklasimi: belge tek bir skorla degil, segment segment
degerlendirilir. Esigi asan pencerelerin kelimeleri "AI" olarak isaretlenir,
ortusen pencerelerde kelime bazinda en yuksek olasilik gecerlidir. Boylece
karma belgelerde (yarisi insan, yarisi AI) hangi bolumun AI oldugu da
soylenebilir — tek bir ortalama bunu gizlerdi.
"""


def combine(windows, probs, total_words, thr):
    """windows: segment.windows() ciktisi, probs: her pencere icin p(AI)."""
    if not windows:
        return {"percent": 0, "word_probs": [], "windows": []}

    word_p = [0.0] * total_words
    for w, p in zip(windows, probs):
        for i in range(w["w_start"], min(w["w_end"], total_words)):
            if p > word_p[i]:
                word_p[i] = p

    ai_words = sum(1 for p in word_p if p >= thr)
    percent = 100.0 * ai_words / total_words if total_words else 0.0

    return {
        "percent": round(percent),
        "ai_words": ai_words,
        "word_probs": word_p,
        "windows": [
            {"p": round(p, 4), "is_ai": p >= thr,
             "w_start": w["w_start"], "w_end": w["w_end"],
             "c_start": w["c_start"], "c_end": w["c_end"],
             "preview": w["text"][:160]}
            for w, p in zip(windows, probs)
        ],
    }


def document_confidence(probs, n_words, thr):
    """Belge geneli guven: kararin esikten ne kadar uzak oldugu + metin uzunlugu."""
    if not probs:
        return 0
    margin = sum(abs(p - thr) for p in probs) / len(probs)
    margin_score = min(1.0, margin / max(thr, 1 - thr))
    length_score = min(1.0, max(0.0, (n_words - 85) / 500.0))
    return round(100 * (0.6 * margin_score + 0.4 * length_score))
