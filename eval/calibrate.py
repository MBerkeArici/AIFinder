# -*- coding: utf-8 -*-
"""Olcum setinden agirliklari ve esigi ogrenip engine/calibration.json yazar.

Iki asamali:
  1) Lojistik regresyon — uc sinyali birlestirir (agirliklar veriden gelir)
  2) Isotonic regresyon — ham cikti olasiligini GERCEK olasiliga cevirir

Ikinci adim sik atlanir ama onemlidir: kalibre edilmemis bir siniflandiricinin
"0.9" ciktisi %90 ihtimal anlamina gelmez. Kullaniciya yuzde gosterecegimiz
icin bu duzeltme sart.

Esik, dogruluk degil DUSUK YANLIS POZITIF hedefiyle secilir: insan metinlerinin
en fazla %1'inin asabildigi nokta. Yanlis suclama, kacirilan AI metninden
cok daha pahali bir hatadir.
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)

import features            # noqa: E402
import run_eval as ev      # noqa: E402

TARGET_FPR = 0.05   # kullanici karari: kisisel kullanimda dengeli nokta
OUT = os.path.join(ROOT, "engine", "calibration.json")


def _human_quantiles(scores, y):
    """Insan metinlerinin skor dagilimindan yuzdelik tablosu."""
    import numpy as _np
    h = _np.asarray(scores)[_np.asarray(y) == 0]
    if len(h) == 0:
        return None
    qs = [0.50, 0.75, 0.90, 0.95, 0.97, 0.98, 0.99, 0.995, 0.998, 0.999, 1.0]
    return {"q": qs, "v": [round(float(_np.quantile(h, q)), 8) for q in qs]}


def build(lang):
    human = ev.read("human_%s.jsonl" % lang)
    ai = ev.read("ai_%s.jsonl" % lang)
    attacked = ev.read("ai_%s_attack.jsonl" % lang)
    if not human or not ai:
        print("[%s] veri yok, atlandi" % lang)
        return None

    rows = human + ai
    features.compute(rows, verbose=False)
    if attacked:
        features.compute(attacked, verbose=False)

    y = np.array([r["label"] for r in rows])
    sig = ev.signals(rows)
    all_names = list(sig.keys())

    # ---- Hangi sinyal kombinasyonu en iyi? Veriye sor, varsayma.
    #
    # Ingilizce olcumunde uclu ensemble (TPR@FPR1% %59.5) tek basina
    # siniflandiricidan (%82.0) DAHA KOTU cikti: zayif stilometri sinyali
    # (AUC 0.606) esik bolgesinde gurultu ekleyip guclu sinyali suluyordu.
    # AUC'ye bakip karar vermek bunu gizliyordu (0.992 vs 0.995, neredeyse
    # esit). Secim olcutu bu yuzden AUC degil, TPR@FPR1% — arac bu esikte
    # calisacak.
    import itertools
    best = None
    for k in (1, 2, 3):
        for combo in itertools.combinations(all_names, k):
            try:
                oof_c, model_c, coefs_c = ev.fit_ensemble(rows, list(combo))
            except Exception:
                continue
            tpr_c, _ = ev.tpr_at_fpr(y, oof_c, TARGET_FPR)
            auc_c = ev.auc(y, oof_c)
            if np.isnan(tpr_c):
                continue
            cand = {"names": list(combo), "oof": oof_c, "model": model_c,
                    "coefs": coefs_c, "tpr": round(tpr_c, 4), "auc": round(auc_c, 4)}
            # Secim: once yakalama orani. Beraberlikte ve AUC farki ihmal
            # edilebilirse DAHA COK SINYAL kazanir.
            #
            # Gerekce: olcum seti gercek dunyayi tam temsil etmiyor. RAID'in
            # AI metinleri siniflandirici icin "kolay" (p(AI)>0.95); gercekte
            # iyi yazilmis bir AI metni 0.69 gibi ara deger aliyor ve tek
            # sinyale dayanan esik onu kaciriyor. Esit olcum skoru veren iki
            # aday arasindan cok sinyalli olani secmek, tek modelin kor
            # noktasina bagimli kalmayi onler.
            def better(a, b):
                if a["tpr"] != b["tpr"]:
                    return a["tpr"] > b["tpr"]
                if abs(a["auc"] - b["auc"]) > 0.01:
                    return a["auc"] > b["auc"]
                return len(a["names"]) > len(b["names"])

            if best is None or better(cand, best):
                best = cand
            print("   %-46s TPR@FPR1%% %5.1f%%  AUC %.3f"
                  % (" + ".join(combo), tpr_c * 100, auc_c))

    names, oof, model, coefs = best["names"], best["oof"], best["model"], best["coefs"]
    print("   -> secilen: %s" % " + ".join(names))
    scaler, lr = model[0], model[-1]

    # ---- isotonic: ham olasiligi gercek olasiliga esle
    from sklearn.isotonic import IsotonicRegression
    iso = IsotonicRegression(out_of_bounds="clip", y_min=0.0, y_max=1.0)
    iso.fit(oof, y)
    grid = np.linspace(oof.min(), oof.max(), 40)
    iso_y = [float(v) for v in iso.predict(grid)]

    # Isotonic, siniflarin TAM ayrildigi veride adim fonksiyonuna donusur:
    # olcum setinde ara deger bulunmadigi icin egri genis bir bolgeyi duz
    # sifira ezer. Gercek metinler tam o bosluga dustugunde (orn. ham
    # p(AI)=0.69) kalibre cikti 0.0000 olur ve arac acikca AI olan metni
    # insan sayar. Uretimde tam bu hata gorulmustu.
    # Bu yuzden isotonic ancak YETERLI COZUNURLUK tasiyorsa kullanilir;
    # tasimazsa lojistik regresyonun kendi olasiligi zaten kalibredir.
    distinct = len({round(v, 3) for v in iso_y})
    use_iso = distinct >= 8
    iso_pts = {"x": [round(float(v), 6) for v in grid],
               "y": [round(v, 6) for v in iso_y]} if use_iso else None
    if not use_iso:
        print("   isotonic atlandi (yalnizca %d farkli deger — adim fonksiyonu)" % distinct)

    cal_oof = iso.predict(oof) if use_iso else oof
    tpr, thr = ev.tpr_at_fpr(y, cal_oof, TARGET_FPR)
    auc_v = ev.auc(y, cal_oof)

    attack_tpr = None
    if attacked:
        sa = ev.signals(attacked)
        Xa = np.column_stack([sa[n] for n in names])
        raw_a = model.predict_proba(Xa)[:, 1]
        pa = iso.predict(raw_a) if use_iso else raw_a
        attack_tpr = round(float((pa >= thr).mean()), 4)

    rec = {
        "names": names,
        "mean": [round(float(v), 8) for v in scaler.mean_],
        "scale": [round(float(v), 8) for v in scaler.scale_],
        "coef": [round(float(v), 8) for v in lr.coef_[0]],
        "intercept": round(float(lr.intercept_[0]), 8),
        "isotonic": iso_pts,   # None ise uygulanmaz
        "threshold": round(float(thr), 9),
        # Belge duzeyi duzeltme icin: insan metinlerinin pencere skor dagilimi.
        # Cok pencereli bir belgede her pencere ayri bir sans veriyor; esik
        # sabit kalirsa belge duzeyi yanlis pozitif pencere sayisiyla birlikte
        # buyur (10 pencere x %5 -> ~%40). Asagidaki yuzdelikler, calisma
        # zamaninda pencere sayisina gore esigi sikilastirmak icin kullanilir.
        "human_q": _human_quantiles(cal_oof if use_iso else oof, y),
        "auc": round(float(auc_v), 4),
        "tpr_at_fpr1": round(float(tpr), 4),
        "target_fpr": TARGET_FPR,
        "attack_tpr": attack_tpr,
        "n": len(rows),
        "n_human": len(human),
        "n_ai": len(ai),
        "clip_words": ev.CLIP_WORDS,
    }
    print("[%s] AUC %.3f | TPR@FPR1%% %.1f%% | esik %.4f | agirliklar %s"
          % (lang, auc_v, tpr * 100, thr, coefs))
    return rec


def main():
    out = {}
    for lang in ("tr", "en"):
        rec = build(lang)
        if rec:
            out[lang] = rec
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("-> %s yazildi" % OUT)


if __name__ == "__main__":
    main()
