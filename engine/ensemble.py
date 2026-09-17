# -*- coding: utf-8 -*-
"""Uc sinyali tek bir kalibre olasiliga cevirir.

Agirliklar elle atanmaz: eval/calibrate.py bunlari olcum setinden ogrenir ve
engine/calibration.json dosyasina yazar. Burasi yalnizca o dosyayi uygular.
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CALIB_PATH = os.path.join(HERE, "calibration.json")

_calib = None


def load():
    global _calib
    if _calib is None:
        if os.path.exists(CALIB_PATH):
            with open(CALIB_PATH, encoding="utf-8") as f:
                _calib = json.load(f)
        else:
            _calib = {}
    return _calib


def available(lang):
    return lang in load()


def raw_vector(feat, names):
    """Ham sinyalleri "buyuk = AI" yonune cevirip sirala."""
    m = {
        "binoculars": -feat["bino"],
        "siniflandirici": feat["clf"],
        "gizlenmis": feat.get("hidden", 0.5),
        "stilometri": feat["style"] / 100.0,
    }
    return [m[n] for n in names]


def _isotonic(p, points):
    """Kaydedilmis isotonic egrisini dogrusal ara-degerle uygula."""
    xs, ys = points["x"], points["y"]
    if p <= xs[0]:
        return ys[0]
    if p >= xs[-1]:
        return ys[-1]
    lo, hi = 0, len(xs) - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if xs[mid] <= p:
            lo = mid
        else:
            hi = mid
    span = xs[hi] - xs[lo]
    t = 0.0 if span == 0 else (p - xs[lo]) / span
    return ys[lo] + t * (ys[hi] - ys[lo])


def probability(feat, lang):
    """feat -> (kalibre p(AI), kullanilan kalibrasyon kaydi)"""
    c = load().get(lang)
    if not c:
        # kalibrasyon yoksa yalnizca stilometriye dus (zayif ama calisir)
        return max(0.0, min(1.0, feat["style"] / 100.0)), None

    names = c["names"]
    x = raw_vector(feat, names)
    z = c["intercept"]
    for xi, mu, sd, w in zip(x, c["mean"], c["scale"], c["coef"]):
        z += w * ((xi - mu) / (sd if sd else 1.0))
    p = 1.0 / (1.0 + math.exp(-max(-30.0, min(30.0, z))))
    if c.get("isotonic"):
        p = _isotonic(p, c["isotonic"])
    return max(0.0, min(1.0, p)), c


def threshold(lang, n_windows=1):
    """Pencere sayisina gore ayarlanmis esik.

    Belge birden cok pencereye bolundugunde her pencere ayri bir yanlis
    pozitif sansi verir. Sabit esikle belge duzeyi hata orani pencere
    sayisiyla birlikte buyur: pencere basina %5 risk, 10 pencerede
    1-(0.95)^10 = %40 eder. Olcum 140 kelimelik tek parcalarla yapildigi
    icin bu etki olcumde gorunmuyordu; gercek belgelerde goruldu
    (20 insan metninin 2'si isaretlendi).

    Duzeltme: her pencerenin asmasi gereken yuzdelik, belge duzeyi hedefi
    sabit kalacak sekilde yukseltilir  ->  q = (1 - hedef)^(1/n)
    """
    c = load().get(lang) or {}
    base = c.get("threshold", 0.5)
    hq = c.get("human_q")
    if not hq or n_windows <= 1:
        return base

    target = c.get("target_fpr", 0.05)
    q_needed = (1.0 - target) ** (1.0 / float(n_windows))

    qs, vs = hq["q"], hq["v"]
    if q_needed <= qs[0]:
        adj = vs[0]
    elif q_needed >= qs[-1]:
        adj = vs[-1]
    else:
        adj = vs[-1]
        for i in range(len(qs) - 1):
            if qs[i] <= q_needed <= qs[i + 1]:
                span = qs[i + 1] - qs[i]
                t = 0.0 if span == 0 else (q_needed - qs[i]) / span
                adj = vs[i] + t * (vs[i + 1] - vs[i])
                break
    return max(base, float(adj))


def quality(lang):
    """Arayuzde gosterilecek olculmus dogruluk bilgisi."""
    c = load().get(lang) or {}
    return {
        "auc": c.get("auc"),
        "tpr_at_fpr1": c.get("tpr_at_fpr1"),
        "attack_tpr": c.get("attack_tpr"),
        "n": c.get("n"),
        "signals": c.get("names"),
    }
