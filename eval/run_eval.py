# -*- coding: utf-8 -*-
"""Olcum kosucusu — dogruluk iddialarinin tek kaynagi.

Onemli tasarim karari: tum metinler ayni kelime bandina KIRPILIR.
AI ve insan ornekleri farkli uzunluk dagilimlarina sahip oldugunda,
model "kisa = AI" gibi sahte bir kural ogrenir ve raporlanan dogruluk
gercekte var olmayan bir basariyi olcer.
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
sys.path.insert(0, ROOT)

import features  # noqa: E402
from engine import normalize as _norm  # noqa: E402

# Ortak bant: her iki sinifin da karsilayabildigi uzunluk. Uzun Turkce AI
# setinin en kisasi 140 kelime. Bant ne kadar yuksekse olcum gercek kullanima
# (300+ kelimelik odev/rapor) o kadar yakin olur; kisa bantta her yontem zayiflar.
CLIP_WORDS = 140


def read(name):
    path = os.path.join(DATA, name)
    if not os.path.exists(path):
        return []
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            # uretimdeki ayni on isleme: olcum gercek akisi yansitmali
            r["text"], _ = _norm.normalize(r["text"])
            w = r["text"].split()
            if len(w) < CLIP_WORDS:
                continue
            r["text"] = " ".join(w[:CLIP_WORDS])
            r.setdefault("attack", "none")
            rows.append(r)
    return rows


def auc(y, s):
    y = np.asarray(y); s = np.asarray(s, dtype=float)
    if len(set(y)) < 2:
        return float("nan")
    from sklearn.metrics import roc_auc_score
    return roc_auc_score(y, s)


def tpr_at_fpr(y, s, target=0.01):
    """Insan metninde yanlis pozitif oranini <=target tutan esikte, AI yakalama orani.

    Esik, insan skorlarinin ustunde OLMAK ZORUNDA. Mukemmel ayrimda (isotonic
    ciktisi tam 0 ve 1) ham hesap 0'a cok yakin bir sayi uretir; bu deger
    yuvarlanip 0.0 olarak kaydedilirse "p >= 0" her metin icin dogru olur ve
    arac her seyi AI isaretler. Bu hata uretimde gorulmustu; asagidaki taban
    onu engelliyor.
    """
    y = np.asarray(y); s = np.asarray(s, dtype=float)
    human = np.sort(s[y == 0])[::-1]
    ai = s[y == 1]
    if len(human) == 0:
        return float("nan"), float("nan")
    k = max(1, int(np.floor(len(human) * target)))
    cut = float(human[k - 1])

    # esik bu kesimin hemen ustunde; asagidaki AI skorlarindan da ayirt edilebilir olmali
    above = ai[ai > cut]
    if len(above):
        thr = (cut + float(above.min())) / 2.0     # iki sinif arasinda orta nokta
    else:
        thr = cut + 1e-6
    if thr <= cut:
        thr = cut + 1e-6
    thr = max(thr, 1e-6)                           # asla 0 olmasin

    tpr = float((ai >= thr).mean())
    return tpr, float(thr)


def signals(rows):
    """Ham sinyalleri "buyuk = AI" yonune cevirir."""
    out = {
        "binoculars": [-r["feat"]["bino"] for r in rows],   # dusuk bino = AI
        "siniflandirici": [r["feat"]["clf"] for r in rows],
        "stilometri": [r["feat"]["style"] / 100.0 for r in rows],
    }
    if any("hidden" in r["feat"] for r in rows):
        out["gizlenmis"] = [r["feat"].get("hidden", 0.5) for r in rows]
    return out


def fit_ensemble(rows, names):
    """Agirliklari veriden ogrenir (elle atanmaz), CV ile disaridan degerlendirir."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import StratifiedKFold
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import make_pipeline

    sig = signals(rows)
    X = np.column_stack([sig[n] for n in names])
    y = np.array([r["label"] for r in rows])

    oof = np.zeros(len(y))
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    for tr, te in skf.split(X, y):
        m = make_pipeline(StandardScaler(),
                          LogisticRegression(max_iter=2000, C=1.0, class_weight="balanced"))
        m.fit(X[tr], y[tr])
        oof[te] = m.predict_proba(X[te])[:, 1]

    full = make_pipeline(StandardScaler(),
                         LogisticRegression(max_iter=2000, C=1.0, class_weight="balanced"))
    full.fit(X, y)
    coefs = dict(zip(names, full[-1].coef_[0].round(3).tolist()))
    return oof, full, coefs


def report_lang(lang, out):
    human = read("human_%s.jsonl" % lang)
    ai = read("ai_%s.jsonl" % lang)
    attacked = read("ai_%s_attack.jsonl" % lang)
    if not human or not ai:
        out.append("\n## %s — veri yok, atlandi\n" % lang.upper())
        return None

    rows = human + ai
    print("\n[%s] %d insan + %d AI (+%d saldirili) — ozellikler cikariliyor"
          % (lang, len(human), len(ai), len(attacked)))
    features.compute(rows)
    if attacked:
        features.compute(attacked)

    y = [r["label"] for r in rows]
    sig = signals(rows)

    out.append("\n## %s\n" % ("Türkçe" if lang == "tr" else "İngilizce"))
    out.append("Örnek: **%d insan**, **%d AI** (her metin ilk %d kelimeye kırpıldı).\n"
               % (len(human), len(ai), CLIP_WORDS))
    out.append("\n### Tek tek sinyaller\n")
    out.append("| Sinyal | ROC-AUC | TPR @ FPR %1 |")
    out.append("|---|---:|---:|")
    for name, s in sig.items():
        t, _ = tpr_at_fpr(y, s)
        out.append("| %s | %.3f | %.1f%% |" % (name, auc(y, s), t * 100))

    names = list(sig.keys())
    oof, model, coefs = fit_ensemble(rows, names)
    e_auc = auc(y, oof)
    e_tpr, e_thr = tpr_at_fpr(y, oof)
    out.append("| **birleşik (ensemble)** | **%.3f** | **%.1f%%** |" % (e_auc, e_tpr * 100))
    out.append("\nÖğrenilen ağırlıklar: `%s`  ·  eşik: `%.4f`\n" % (coefs, e_thr))

    # saldiri dayanikliligi
    if attacked:
        sa = signals(attacked)
        Xa = np.column_stack([sa[n] for n in names])
        pa = model.predict_proba(Xa)[:, 1]
        out.append("\n### Saldırı altında (parafraz / eşanlamlı / homoglif)\n")
        out.append("Aynı eşikte yakalama oranı: **%.1f%%** (%d örnek)\n"
                   % (float((pa >= e_thr).mean()) * 100, len(attacked)))
        by = {}
        for r, p in zip(attacked, pa):
            by.setdefault(r.get("attack", "?"), []).append(p >= e_thr)
        out.append("\n| Saldırı türü | Yakalama |")
        out.append("|---|---:|")
        for k, v in sorted(by.items()):
            out.append("| %s | %.1f%% (%d) |" % (k, 100 * np.mean(v), len(v)))

    # kaynak bazinda yanlis pozitif
    out.append("\n### İnsan metinlerinde yanlış pozitif (kaynak bazında)\n")
    out.append("| Kaynak | Yanlış pozitif | n |")
    out.append("|---|---:|---:|")
    hs = {}
    for r, p in zip(rows, oof):
        if r["label"] == 0:
            hs.setdefault(r["source"].split("/")[0], []).append(p >= e_thr)
    for k, v in sorted(hs.items()):
        out.append("| %s | %.1f%% | %d |" % (k, 100 * np.mean(v), len(v)))

    return {"lang": lang, "auc": e_auc, "tpr": e_tpr, "thr": e_thr,
            "coefs": coefs, "names": names, "model": model, "n": len(rows)}


def main():
    out = ["# Ölçüm Raporu", "",
           "Bu dosya otomatik üretilir (`eval/run_eval.py`). Arayüzde gösterilen",
           "doğruluk rakamlarının tek kaynağı budur.", ""]
    results = {}
    for lang in ("tr", "en"):
        r = report_lang(lang, out)
        if r:
            results[lang] = r

    path = os.path.join(HERE, "report.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print("\n-> eval/report.md yazildi")
    print("\n".join(l for l in out if l.startswith(("|", "#", "Öğrenilen"))))
    return results


if __name__ == "__main__":
    main()
