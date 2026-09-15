# -*- coding: utf-8 -*-
import os
import threading
import traceback

from flask import Flask, jsonify, request, send_from_directory

import analyze as engine
import extract as extractor
from engine import ensemble

HERE = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=os.path.join(HERE, "static"))
app.config["MAX_CONTENT_LENGTH"] = 12 * 1024 * 1024

_ready = {"models": False, "error": None}


def _warm():
    try:
        _ready["models"] = engine.warmup()
    except Exception as e:
        _ready["error"] = str(e)


# AIFINDER_NO_WARMUP=1 ile modeller onden yuklenmez: arayuzu bellek
# harcamadan acmak icin. Ilk analiz isteginde yine de yuklenirler.
if os.environ.get("AIFINDER_NO_WARMUP") != "1":
    threading.Thread(target=_warm, daemon=True).start()


@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.get("/api/status")
def status():
    return jsonify(ready=_ready["models"], error=_ready["error"],
                   calibrated={l: ensemble.available(l) for l in ("tr", "en")},
                   quality={l: ensemble.quality(l) for l in ("tr", "en")})


@app.post("/api/analyze")
def api_analyze():
    try:
        forensics = {"notes": [], "score_delta": 0}
        source = "yapıştırılan metin"

        if "file" in request.files and request.files["file"].filename:
            f = request.files["file"]
            data = f.read()
            if not data:
                return jsonify(ok=False, error="Dosya boş görünüyor."), 400
            text, forensics = extractor.extract(f.filename, data)
            source = f.filename
        else:
            text = (request.form.get("text") or
                    (request.get_json(silent=True) or {}).get("text") or "")

        result = engine.analyze(text, forensics)
        result["source"] = source
        return jsonify(result), (200 if result.get("ok") else 400)

    except ValueError as e:
        return jsonify(ok=False, error=str(e)), 400
    except Exception:
        traceback.print_exc()
        return jsonify(ok=False, error="Beklenmeyen bir hata oluştu."), 500


@app.errorhandler(413)
def too_large(_):
    return jsonify(ok=False, error="Dosya çok büyük (en fazla 12 MB)."), 413


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 9317))
    print("\n  AIFinder  ➜  http://127.0.0.1:%d   (modeller arka planda yükleniyor)\n" % port)
    app.run(host="127.0.0.1", port=port, debug=False, threaded=True)
