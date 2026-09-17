# -*- coding: utf-8 -*-
"""Karma belge testi — aracin asil iddiasinin sinanmasi.

AIFinder tek bir "AI mi degil mi" karari vermiyor; belgenin YUZDE KACININ
yapay zeka uretimi oldugunu soyluyor. Bu iddia bugune kadar hic olculmedi:
olcum seti yalnizca tamamen insan ya da tamamen AI metinlerden olusuyor.

Bu betik bilinen oranlarda (%0, %25, %50, %75, %100) karma belgeler kurar ve
aracin tahminiyle gercek orani karsilastirir. Gercekci senaryo blok halinde
karisim: ogrenci odevin bir bolumunu kendi yazip bir bolumunu uretiyor.
Cumle cumle serpistirme daha zor bir durum ama daha az gercekci.

OLCUT: ortalama mutlak hata (MAE). Ayrica sistematik sapma (bias) raporlanir —
arac surekli fazla mi tahmin ediyor, az mi? Yanlis suclama riski acisindan
%0 belgelerdeki sonuc ayrica onemlidir.
"""
import json
import os
import random
import sys
import urllib.request
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
sys.path.insert(0, ROOT)

URL = "http://127.0.0.1:9317/api/analyze"
RATIOS = [0.0, 0.25, 0.50, 0.75, 1.0]
PER_RATIO = 3
TARGET_WORDS = 900          # gercekci odev boyutu
random.seed(4242)


def load(path, limit=None):
    p = os.path.join(DATA, path)
    if not os.path.exists(p):
        return []
    out = []
    with open(p, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            if len(r["text"].split()) >= 120:
                out.append(r["text"])
            if limit and len(out) >= limit:
                break
    return out


def build(human_pool, ai_pool, ratio, target=TARGET_WORDS):
    """Verilen oranda AI kelimesi iceren tek bir belge kurar.

    Blok duzeni: once insan bolumu, sonra AI bolumu. Boylece pencerelerin
    cogu tek kaynakli olur; sinirdaki pencereler karisik kalir ve bu da
    gercek kullanimdaki durumu yansitir.
    """
    need_ai = int(target * ratio)
    need_hu = target - need_ai

    def take(pool, n):
        if n <= 0:
            return [], 0
        parts, total = [], 0
        for t in random.sample(pool, min(len(pool), 12)):
            w = t.split()
            if total + len(w) > n:
                w = w[: max(0, n - total)]
            if not w:
                break
            parts.append(" ".join(w))
            total += len(w)
            if total >= n:
                break
        return parts, total

    hu_parts, hu_n = take(human_pool, need_hu)
    ai_parts, ai_n = take(ai_pool, need_ai)
    body = "\n\n".join(hu_parts + ai_parts)
    total = hu_n + ai_n
    return body, (100.0 * ai_n / total if total else 0.0)


def analyze(text):
    b = str(uuid.uuid4())
    payload = ('--%s\r\nContent-Disposition: form-data; name="text"\r\n\r\n%s\r\n--%s--\r\n'
               % (b, text, b)).encode("utf-8")
    req = urllib.request.Request(URL, data=payload,
                                 headers={"Content-Type":
                                          "multipart/form-data; boundary=%s" % b})
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.loads(r.read().decode("utf-8"))


def run(lang, human_pool, ai_pool, out):
    if not human_pool or not ai_pool:
        print("[%s] havuz bos, atlandi" % lang)
        return []
    print("\n[%s] karma belge testi" % lang)
    rows = []
    for ratio in RATIOS:
        for k in range(PER_RATIO):
            text, actual = build(human_pool, ai_pool, ratio)
            d = analyze(text)
            if not d.get("ok"):
                print("   %.0f%% -> HATA: %s" % (ratio * 100, str(d.get("error"))[:60]))
                continue
            pred = d["percent"]
            rows.append({"lang": lang, "actual": actual, "pred": pred,
                         "words": d["stats"]["words"], "windows": d["stats"]["windows"]})
            print("   gercek %5.1f%%  ->  tahmin %3d%%   (fark %+d, %d kelime, %d pencere)"
                  % (actual, pred, pred - actual, d["stats"]["words"], d["stats"]["windows"]))
    return rows


def summarize(rows, out):
    if not rows:
        return
    import collections
    by = collections.defaultdict(list)
    for r in rows:
        by[(r["lang"], round(r["actual"] / 25) * 25)].append(r)

    out.append("\n## Karma belge testi\n")
    out.append("Belgenin yüzde kaçının yapay zekâ üretimi olduğu iddiası, bilinen")
    out.append("oranlarda kurulmuş karma belgelerle sınandı. Düzen blok hâlinde:")
    out.append("belgenin bir bölümü insan, bir bölümü yapay zekâ metni.\n")
    out.append("| Dil | Gerçek oran | Ortalama tahmin | Ortalama sapma |")
    out.append("|---|---:|---:|---:|")
    for (lang, bucket) in sorted(by):
        rs = by[(lang, bucket)]
        pred = sum(r["pred"] for r in rs) / len(rs)
        act = sum(r["actual"] for r in rs) / len(rs)
        out.append("| %s | %%%.0f | %%%.0f | %+.0f |"
                   % ("Türkçe" if lang == "tr" else "İngilizce", act, pred, pred - act))

    for lang in sorted(set(r["lang"] for r in rows)):
        rs = [r for r in rows if r["lang"] == lang]
        mae = sum(abs(r["pred"] - r["actual"]) for r in rs) / len(rs)
        bias = sum(r["pred"] - r["actual"] for r in rs) / len(rs)
        zero = [r for r in rs if r["actual"] == 0]
        full = [r for r in rs if r["actual"] >= 99]
        out.append("\n**%s** — ortalama mutlak hata **%.1f puan**, sistematik sapma %+.1f puan."
                   % ("Türkçe" if lang == "tr" else "İngilizce", mae, bias))
        if zero:
            out.append("Tamamı insan yazımı belgelerde tahmin: %s."
                       % ", ".join("%%%d" % r["pred"] for r in zero))
        if full:
            out.append("Tamamı yapay zekâ belgelerde tahmin: %s."
                       % ", ".join("%%%d" % r["pred"] for r in full))


def main():
    tr_h = load("human_tr.jsonl", 60)
    tr_a = load("ai_tr.jsonl")
    en_h = load("human_en.jsonl", 60)
    en_a = load("ai_en.jsonl", 60)

    rows = run("tr", tr_h, tr_a, None) + run("en", en_h, en_a, None)

    out = []
    summarize(rows, out)
    path = os.path.join(HERE, "report_mixed.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("# Karma Belge Ölçümü\n" + "\n".join(out) + "\n")
    print("\n-> eval/report_mixed.md yazildi")
    print("\n".join(out))


if __name__ == "__main__":
    main()
