# -*- coding: utf-8 -*-
"""Tek bir dil icin kalibrasyon — SADECE onbellekten, model yuklemeden.

Turkce fazi bitip Ingilizce surerken araci kullanilabilir hale getirmek icin.
Onbellekte olmayan metin varsa sessizce atlanir: burada model yuklemek,
suren olcumle bellek icin yarisir ve ikisini de yavaslatir.
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)

import features          # noqa: E402
import run_eval as ev    # noqa: E402
import calibrate as cal  # noqa: E402


def cached_only(rows, cache):
    for r in rows:
        r["_k"] = features.key(r["text"], r["lang"])
    out = [r for r in rows if r["_k"] in cache]
    for r in out:
        r["feat"] = cache[r["_k"]]
    return out


def main(lang):
    cache = features.load_cache()
    human = cached_only(ev.read("human_%s.jsonl" % lang), cache)
    ai = cached_only(ev.read("ai_%s.jsonl" % lang), cache)
    attacked = cached_only(ev.read("ai_%s_attack.jsonl" % lang), cache)

    print("[%s] onbellekte: %d insan, %d AI, %d saldirili" % (lang, len(human), len(ai), len(attacked)))
    if len(human) < 30 or len(ai) < 15:
        print("   yetersiz — kalibrasyon atlandi")
        return None

    rows = human + ai
    y = np.array([r["label"] for r in rows])
    sig = ev.signals(rows)
    all_names = list(sig.keys())

    import itertools
    best = None
    for k in (1, 2, 3):
        for combo in itertools.combinations(all_names, k):
            try:
                oof_c, model_c, coefs_c = ev.fit_ensemble(rows, list(combo))
            except Exception:
                continue
            tpr_c, _ = ev.tpr_at_fpr(y, oof_c, cal.TARGET_FPR)
            auc_c = ev.auc(y, oof_c)
            if np.isnan(tpr_c):
                continue
            print("   %-46s TPR@FPR%d%% %5.1f%%  AUC %.3f" % (" + ".join(combo), cal.TARGET_FPR*100, tpr_c * 100, auc_c))
            cand = {"names": list(combo), "oof": oof_c, "model": model_c,
                    "coefs": coefs_c, "tpr": round(tpr_c, 4), "auc": round(auc_c, 4)}
            def better(a, b):
                if a["tpr"] != b["tpr"]:
                    return a["tpr"] > b["tpr"]
                if abs(a["auc"] - b["auc"]) > 0.01:
                    return a["auc"] > b["auc"]
                return len(a["names"]) > len(b["names"])
            if best is None or better(cand, best):
                best = cand

    names, oof, model, coefs = best["names"], best["oof"], best["model"], best["coefs"]
    print("   -> secilen: %s" % " + ".join(names))

    from sklearn.isotonic import IsotonicRegression
    iso = IsotonicRegression(out_of_bounds="clip", y_min=0.0, y_max=1.0)
    iso.fit(oof, y)
    grid = np.linspace(oof.min(), oof.max(), 40)
    cal_oof = iso.predict(oof)
    tpr, thr = ev.tpr_at_fpr(y, cal_oof, cal.TARGET_FPR)

    attack_tpr = None
    if attacked:
        sa = ev.signals(attacked)
        Xa = np.column_stack([sa[n] for n in names])
        raw_a = model.predict_proba(Xa)[:, 1]
        pa = iso.predict(raw_a) if use_iso else raw_a
        attack_tpr = round(float((pa >= thr).mean()), 4)

    scaler, lr = model[0], model[-1]
    rec = {
        "names": names,
        "mean": [round(float(v), 8) for v in scaler.mean_],
        "scale": [round(float(v), 8) for v in scaler.scale_],
        "coef": [round(float(v), 8) for v in lr.coef_[0]],
        "intercept": round(float(lr.intercept_[0]), 8),
        "isotonic": iso_pts,
        "threshold": round(float(thr), 9),
        "auc": round(float(ev.auc(y, cal_oof)), 4),
        "tpr_at_fpr1": round(float(tpr), 4),
        "target_fpr": cal.TARGET_FPR,
        "attack_tpr": attack_tpr,
        "n": len(rows), "n_human": len(human), "n_ai": len(ai),
        "clip_words": ev.CLIP_WORDS, "partial": True,
    }

    out = {}
    if os.path.exists(cal.OUT):
        try:
            out = json.load(open(cal.OUT, encoding="utf-8"))
        except Exception:
            out = {}
    out[lang] = rec
    with open(cal.OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("[%s] AUC %.3f | TPR@FPR%d%%: %.1f%% | esik %.4f -> calibration.json"
          % (lang, rec["auc"], cal.TARGET_FPR*100, tpr * 100, thr))
    return rec


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "tr")
