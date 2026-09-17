# -*- coding: utf-8 -*-
"""Her metin icin uc katmanin ham sinyallerini cikarir ve onbellege alir.

FAZ FAZ CALISIR. Onceki surum uc modeli ayni anda bellekte tutuyordu
(~9 GB) ve 16 GB'lik makinede tum sistemi takasa dusuruyordu. Simdi:

  Faz 1: Binoculars (2 model, ~6 GB)  -> bosalt
  Faz 2: siniflandiricilar (~1 GB)    -> bosalt
  Faz 3: stilometri (model yok, CPU)

Tepe bellek ~6.5 GB'a iner ve DOGRULUK AYNI KALIR — hicbir model kucultulmedi,
yalnizca ayni anda kacinin bellekte durdugu degisti.

Her faz kendi ara dosyasina yazar; islem yarida kesilse bile o ana kadarki
hesap korunur.
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

DATA = os.path.join(ROOT, "data")
CACHE = os.path.join(DATA, "features_cache.jsonl")


def key(text, lang):
    return hashlib.sha1(("%s|%s" % (lang, text)).encode("utf-8")).hexdigest()


def _read_jsonl(path):
    if not os.path.exists(path):
        return {}
    out = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            try:
                r = json.loads(line)
                out[r["k"]] = r["f"]
            except Exception:
                pass
    return out


def _append_jsonl(path, rows):
    with open(path, "a", encoding="utf-8") as f:
        for k, v in rows:
            f.write(json.dumps({"k": k, "f": v}) + "\n")


load_cache = lambda: _read_jsonl(CACHE)


def _stage_path(name):
    return os.path.join(DATA, "_stage_%s.jsonl" % name)


def _progress(done, total, label):
    sys.stdout.write("\r  %-12s %d/%d" % (label, done, total))
    sys.stdout.flush()


def _stage_binoculars(todo, batch, verbose):
    from engine.binoculars import Binoculars
    path = _stage_path("bino")
    have = _read_jsonl(path)
    pending = [r for r in todo if r["_k"] not in have]
    if pending:
        bino = Binoculars.shared()
        for i in range(0, len(pending), batch):
            chunk = pending[i:i + batch]
            scores = bino.score([r["text"] for r in chunk])
            rows = [(r["_k"], float(s)) for r, s in zip(chunk, scores)]
            _append_jsonl(path, rows)
            have.update(dict(rows))
            if verbose:
                _progress(min(i + batch, len(pending)), len(pending), "binoculars")
        if verbose:
            print()
        Binoculars.unload()          # ~6 GB geri verilir
    return have


def _stage_classifier(todo, batch, verbose):
    from engine import classifier, hidden
    path = _stage_path("clf")
    have = _read_jsonl(path)
    pending = [r for r in todo if r["_k"] not in have]
    if pending:
        for lang in sorted(set(r["lang"] for r in pending)):
            sub = [r for r in pending if r["lang"] == lang]
            clf = classifier.get(lang)
            for i in range(0, len(sub), batch):
                chunk = sub[i:i + batch]
                if clf and hidden.available(lang):
                    probs, embs = clf.predict([r["text"] for r in chunk], with_embeddings=True)
                    hids = hidden.score(embs, lang)   # dil sart: TR kafa 768, EN kafa 1024 boyutlu
                elif clf:
                    probs, hids = clf.predict([r["text"] for r in chunk]), [0.5] * len(chunk)
                else:
                    probs, hids = [0.5] * len(chunk), [0.5] * len(chunk)
                rows = [(r["_k"], {"clf": float(p), "hidden": float(h)})
                        for r, p, h in zip(chunk, probs, hids)]
                _append_jsonl(path, rows)
                have.update(dict(rows))
                if verbose:
                    _progress(min(i + batch, len(sub)), len(sub), "clf-" + lang)
            if verbose:
                print()
        classifier.unload()          # ~1 GB geri verilir
    return have


def _stage_style(todo, verbose):
    import detector
    path = _stage_path("style")
    have = _read_jsonl(path)
    pending = [r for r in todo if r["_k"] not in have]
    if pending:
        rows = []
        for n, r in enumerate(pending, 1):
            res = detector.analyze(r["text"])
            rows.append((r["_k"], float(res["score"]) if res.get("ok") else 50.0))
            if len(rows) >= 50:
                _append_jsonl(path, rows); have.update(dict(rows)); rows = []
            if verbose and n % 25 == 0:
                _progress(n, len(pending), "stilometri")
        if rows:
            _append_jsonl(path, rows); have.update(dict(rows))
        if verbose:
            print()
    return have


def compute(rows, batch=4, verbose=True):
    """rows: [{'text','lang',...}] -> her satira 'feat' ekler."""
    cache = load_cache()
    for r in rows:
        r["_k"] = key(r["text"], r["lang"])
    todo = [r for r in rows if r["_k"] not in cache]
    if verbose:
        print("  onbellekte %d, hesaplanacak %d" % (len(rows) - len(todo), len(todo)))

    if todo:
        bino = _stage_binoculars(todo, batch, verbose)
        clf = _stage_classifier(todo, batch, verbose)
        style = _stage_style(todo, verbose)

        fresh = []
        for r in todo:
            k = r["_k"]
            if k in bino and k in clf and k in style:
                c = clf[k]
                if isinstance(c, dict):
                    fresh.append((k, {"bino": bino[k], "clf": c["clf"],
                                      "hidden": c.get("hidden", 0.5), "style": style[k]}))
                else:
                    fresh.append((k, {"bino": bino[k], "clf": c, "style": style[k]}))
        _append_jsonl(CACHE, fresh)
        cache.update(dict(fresh))

    for r in rows:
        r["feat"] = cache[r["_k"]]
    return rows
