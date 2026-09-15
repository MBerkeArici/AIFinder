# -*- coding: utf-8 -*-
"""Ana cozumleme akisi: metin -> pencereler -> uc sinyal -> yuzde.

Akis:
  1) dil tespiti
  2) ~300 kelimelik %50 ortusen pencerelere bolme
  3) her pencere icin Binoculars + siniflandirici + stilometri
  4) kalibre olasilik (engine/calibration.json)
  5) esigi asan pencerelerin kelime orani = % AI
"""
import threading
import time

import detector
from engine import aggregate, ensemble, hidden, normalize, segment

MIN_WORDS = 85       # bunun altinda karar vermiyoruz
STRONG_WORDS = 300   # bunun uzerinde guven belirgin artar

# Modeller ~7 GB tutuyor. Arac acik birakildiginda makineyi surekli mesgul
# etmemesi icin, bu sure boyunca kullanilmazsa bellek geri verilir.
# Sonraki istek modelleri yeniden yukler (~15 sn).
IDLE_UNLOAD_SEC = 600

_last_use = [0.0]
_lock = threading.Lock()


def _touch():
    _last_use[0] = time.time()


def _idle_watch():
    from engine import classifier
    from engine.binoculars import Binoculars
    while True:
        time.sleep(30)
        with _lock:
            if _last_use[0] and time.time() - _last_use[0] > IDLE_UNLOAD_SEC:
                Binoculars.unload()
                classifier.unload()
                _last_use[0] = 0.0
                print("[bellek] %d dk boşta kalındı, modeller bellekten düşürüldü"
                      % (IDLE_UNLOAD_SEC // 60))


threading.Thread(target=_idle_watch, daemon=True).start()


def _features(texts, lang):
    """Pencere metinleri icin uc ham sinyal."""
    from engine.binoculars import Binoculars
    from engine import classifier

    bino = Binoculars.shared().score(texts)
    clf = classifier.get(lang)
    if clf and hidden.available(lang):
        # gomu ayni ileri gecisten gelir — ek model yuklenmez
        probs, embs = clf.predict(texts, with_embeddings=True)
        hid = hidden.score(embs)
    elif clf:
        probs, hid = clf.predict(texts), [0.5] * len(texts)
    else:
        probs, hid = [0.5] * len(texts), [0.5] * len(texts)
    out = []
    for t, b, p, h in zip(texts, bino, probs, hid):
        r = detector.analyze(t)
        out.append({"bino": float(b), "clf": float(p), "hidden": float(h),
                    "style": float(r["score"]) if r.get("ok") else 50.0})
    return out


def warmup():
    """Modelleri onden yukle; ilk istegin 15 saniye beklemesini onler."""
    try:
        from engine.binoculars import Binoculars
        from engine import classifier
        Binoculars.shared()
        for lang in ("tr", "en"):
            if ensemble.available(lang):
                classifier.get(lang)
        _touch()
        return True
    except Exception as e:
        print("[warmup] %s: %s" % (type(e).__name__, e))
        return False


def analyze(text, forensics=None):
    text = (text or "").replace("\r\n", "\n").strip()
    # Saldiri normalizasyonu analizden ONCE: homoglif ve gorunmez karakterler
    # tespiti cokertiyor (RAID olcumu: homoglif altinda %3.3 yakalama).
    text, norm_stats = normalize.normalize(text)
    words = text.split()
    n = len(words)

    if n < MIN_WORDS:
        return {"ok": False, "undecided": True,
                "error": "Karar verebilmek için en az %d kelime gerekiyor (şu an %d). "
                         "Daha kısa metinlerde hiçbir yöntem güvenilir sonuç üretemez — "
                         "tahmin yürütmek yerine karar vermiyoruz." % (MIN_WORDS, n)}

    lang = detector.detect_lang(text)

    # Kalibrasyon yoksa SAYI URETME. Kalibre edilmemis bir yuzde, hak
    # etmedigi bir kesinlik izlenimi verir: esik olculmemistir, olasilik
    # gercek olasilik degildir. Bos bir cevap, yanlis bir sayidan iyidir.
    if not ensemble.available(lang):
        return {"ok": False, "undecided": True, "uncalibrated": True,
                "error": "%s için kalibrasyon henüz yapılmadı. Motor ölçülmüş bir eşiğe "
                         "sahip olmadan yüzde üretmez — kalibre edilmemiş bir sayı "
                         "yanıltıcı olur. Ölçüm tamamlandığında bu ekran kendiliğinden "
                         "çalışır duruma gelecek." % ("Türkçe" if lang == "tr" else "İngilizce")}

    # Pencere boyutu, kalibrasyonun yapildigi uzunlukla ESLESMELI.
    # Kalibrasyon 140 kelimelik metinlerle yapildi; 300 kelimelik pencere
    # beslemek esigi gecersiz kilar. Ayrica kucuk pencere karma belgelerde
    # cozunurlugu artirir: 440 kelimelik yari-yariya bir belge, 300'luk
    # pencerelerde iki karisik pencereye dusup %0 veriyordu.
    win_size = (ensemble.load().get(lang) or {}).get("clip_words", 140)
    wins = segment.windows(text, size=win_size, stride=max(60, win_size // 2),
                           min_tail=max(50, win_size // 2))
    with _lock:
        _touch()
        feats = _features([w["text"] for w in wins], lang)
        _touch()

    probs, calib = [], None
    for f in feats:
        p, c = ensemble.probability(f, lang)
        probs.append(p)
        calib = calib or c

    thr = ensemble.threshold(lang)
    agg = aggregate.combine(wins, probs, n, thr)
    percent = agg["percent"]
    confidence = aggregate.document_confidence(probs, n, thr)

    # aciklanabilirlik: stilometri katmaninin tam dokumu (belge geneli)
    style = detector.analyze(text, forensics)

    # ONEMLI: dusuk sonuc "insan yazimi" DEMEK DEGILDIR.
    #
    # Olcum (eval/report.md): yapay zekaya "insan gibi yaz" denildiginde
    # uretilen metinlerin 0/10'u yakalaniyor; bu kumede Binoculars ve
    # stilometrinin ayirt etme gucu sansin altinda. Boyle bir metnin
    # kalibre olasiligi (0.13) insan metinlerinin medyaninin (0.07)
    # hemen yaninda kaliyor ve esik nereye cekilirse cekilsin ayrilmiyor.
    #
    # Bu yuzden araç "insan yazımı" gibi olumlu bir hukum vermez.
    # Yapay zeka izi BULAMAMAK, yapay zeka olmadigi anlamina gelmez.
    if percent >= 80:
        verdict, tone = "Büyük olasılıkla yapay zekâ üretimi", "ai"
    elif percent >= 45:
        verdict, tone = "Belgenin önemli bir bölümü yapay zekâ üretimi görünüyor", "likely-ai"
    elif percent >= 15:
        verdict, tone = "Karma — bazı bölümler yapay zekâ üretimi olabilir", "mixed"
    elif percent > 0:
        verdict, tone = "Sınırlı yapay zekâ izi", "likely-human"
    else:
        verdict, tone = "Yapay zekâ izi bulunamadı", "human"

    layers = []
    if calib:
        lbl = {"binoculars": "Binoculars (dil modeli şaşkınlığı)",
               "siniflandirici": "Eğitilmiş sınıflandırıcı",
               "gizlenmis": "Gizlenmiş AI tespiti",
               "stilometri": "Stilometri (yazım biçemi)"}
        raw = {"binoculars": sum(f["bino"] for f in feats) / len(feats),
               "siniflandirici": sum(f["clf"] for f in feats) / len(feats),
               "gizlenmis": sum(f.get("hidden", 0.5) for f in feats) / len(feats),
               "stilometri": sum(f["style"] for f in feats) / len(feats)}
        fmt = {"binoculars": "%.3f (düşük = AI)",
               "siniflandirici": "p(AI) = %.3f",
               "gizlenmis": "p(AI) = %.3f",
               "stilometri": "%.0f / 100"}
        for name in calib["names"]:
            layers.append({"label": lbl[name], "value": fmt[name] % raw[name]})

    return {
        "ok": True,
        "percent": percent,
        "verdict": verdict,
        "tone": tone,
        "confidence": confidence,
        "threshold": round(thr, 3),
        "lang": "Türkçe" if lang == "tr" else "İngilizce",
        "lang_code": lang,
        "quality": ensemble.quality(lang),
        "layers": layers,
        "windows": agg["windows"],
        "word_probs": [round(p, 3) for p in agg["word_probs"]],
        "calibrated": calib is not None,
        "stylometry": style.get("metrics", []) if style.get("ok") else [],
        "sentences": style.get("sentences", []) if style.get("ok") else [],
        "not_proof": percent < 15,
        "not_proof_note": ("Yapay zekâ izi bulunamadı — bu, metnin insan tarafından "
                           "yazıldığını göstermez. Ölçümümüzde, yapay zekâya \u201cinsan gibi "
                           "yaz\u201d denilerek üretilen metinlerin hiçbiri yakalanamadı "
                           "(0/10). Bu tür metinler bu araçla ayırt edilemiyor."),
        "forensics": normalize.report(norm_stats) + (forensics or {}).get("notes", []),
        "words": words[:8000],       # arayuzdeki kelime bazli vurgulama icin
        "stats": {"words": n, "windows": len(wins),
                  "sentences": style.get("stats", {}).get("sentences", 0),
                  "short": n < STRONG_WORDS},
    }
