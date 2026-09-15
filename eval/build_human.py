# -*- coding: utf-8 -*-
"""Insan yazimi metinleri toplar.

Kaynak secimi kritik: metinler LLM caginden ONCE yazilmis olmali, yoksa
"insan" etiketli veriye AI metni sizar ve tum olcum bozulur.

  EN : RAID (liamdugan/raid) — model=="human" satirlari; kaynaklar 2023 oncesi
  TR : ttc4900 haber derlemi (2015 oncesi)
       + Turkce Vikipedi'nin 2014 tarihli revizyonlari (resmi/ansiklopedik uslup)
"""
import json
import os
import random
import re
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")
os.makedirs(DATA, exist_ok=True)
random.seed(20260914)

MIN_WORDS, MAX_WORDS = 120, 600


def wc(t):
    return len(t.split())


def clip(t, lo=MIN_WORDS, hi=MAX_WORDS):
    w = t.split()
    if len(w) < lo:
        return None
    return " ".join(w[:hi])


def write(path, rows):
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("  -> %s (%d kayit)" % (os.path.basename(path), len(rows)))


# --------------------------------------------------------------- EN: RAID ---

def raid_human(n=200):
    from datasets import load_dataset
    print("RAID insan metinleri cekiliyor...")
    ds = load_dataset("liamdugan/raid", "raid", split="train", streaming=True)
    rows, seen = [], set()
    for i, r in enumerate(ds):
        if r.get("model") != "human" or r.get("attack") not in (None, "none"):
            continue
        t = clip((r.get("generation") or "").strip())
        if not t or t[:80] in seen:
            continue
        seen.add(t[:80])
        rows.append({"text": t, "label": 0, "lang": "en",
                     "source": "raid/human/" + str(r.get("domain", "?"))})
        if len(rows) >= n:
            break
        if i > 400000:
            break
    return rows


# ------------------------------------------------------------ TR: ttc4900 ---

def ttc4900(n=140):
    from datasets import load_dataset
    print("ttc4900 (Turkce haber) cekiliyor...")
    ds = load_dataset("savasy/ttc4900", split="train")
    idx = list(range(len(ds)))
    random.shuffle(idx)
    rows = []
    for i in idx:
        t = clip((ds[i]["text"] or "").strip())
        if not t:
            continue
        rows.append({"text": t, "label": 0, "lang": "tr",
                     "source": "ttc4900/" + str(ds[i].get("category", "?"))})
        if len(rows) >= n:
            break
    return rows


# --------------------------------------------------- TR: Vikipedi 2014 rev ---

WIKI_API = "https://tr.wikipedia.org/w/api.php"
UA = {"User-Agent": "ai-detector-eval/1.0 (local research)"}


def _api(params):
    url = WIKI_API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def strip_wikitext(s):
    s = re.sub(r"\{\{[^{}]*\}\}", " ", s)
    s = re.sub(r"\{\{[^{}]*\}\}", " ", s)          # ic ice sablonlar
    s = re.sub(r"\{\|.*?\|\}", " ", s, flags=re.S)  # tablolar
    s = re.sub(r"<ref[^>]*>.*?</ref>", " ", s, flags=re.S)
    s = re.sub(r"<ref[^>]*/>", " ", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\[\[(?:Dosya|Resim|File|Image|Kategori|Category):[^\]]*\]\]", " ", s)
    s = re.sub(r"\[\[([^\]|]*)\|([^\]]*)\]\]", r"\2", s)
    s = re.sub(r"\[\[([^\]]*)\]\]", r"\1", s)
    s = re.sub(r"'{2,}", "", s)
    s = re.sub(r"^[*#:;=].*$", " ", s, flags=re.M)
    s = re.sub(r"https?://\S+", " ", s)
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{2,}", "\n\n", s)
    return s.strip()


def wikipedia_2014(n=90):
    print("Turkce Vikipedi 2014 revizyonlari cekiliyor...")
    rows, tries = [], 0
    while len(rows) < n and tries < 40:
        tries += 1
        try:
            rnd = _api({"action": "query", "list": "random", "rnnamespace": 0,
                        "rnlimit": 20, "format": "json", "formatversion": 2})
            titles = [p["title"] for p in rnd["query"]["random"]]
            for title in titles:
                if len(rows) >= n:
                    break
                try:
                    res = _api({"action": "query", "prop": "revisions", "titles": title,
                                "rvprop": "content|timestamp", "rvslots": "main",
                                "rvstart": "2014-12-31T23:59:59Z", "rvdir": "older",
                                "rvlimit": 1, "format": "json", "formatversion": 2})
                    pages = res.get("query", {}).get("pages", [])
                    if not pages or "revisions" not in pages[0]:
                        continue
                    rev = pages[0]["revisions"][0]
                    body = rev["slots"]["main"]["content"]
                    t = clip(strip_wikitext(body))
                    if not t:
                        continue
                    rows.append({"text": t, "label": 0, "lang": "tr",
                                 "source": "wikipedia-tr/" + rev.get("timestamp", "2014")[:7]})
                except Exception:
                    continue
                time.sleep(0.12)
        except Exception as e:
            print("   uyari:", type(e).__name__, str(e)[:60])
            time.sleep(1)
    return rows


def wikipedia_tr_hf(n=90):
    """Turkce Vikipedi (2023-11 dump) — ansiklopedik/resmi uslup.

    Yanlis pozitif riski en yuksek insan metni turu bu: kurallara uygun,
    duz, tekduze. Test setinde bulunmasi sart, yoksa esik fazla gevsek kalir.
    """
    from datasets import load_dataset
    print("Turkce Vikipedi (HF dump) cekiliyor...")
    ds = load_dataset("wikimedia/wikipedia", "20231101.tr", split="train", streaming=True)
    rows = []
    for i, r in enumerate(ds):
        if i % 7:            # dump basi alfabetik/populer makalelerle dolu, seyrelt
            continue
        body = re.sub(r"\n{2,}", "\n\n", (r.get("text") or "").strip())
        t = clip(body)
        if not t:
            continue
        rows.append({"text": t, "label": 0, "lang": "tr", "source": "wikipedia-tr-2023"})
        if len(rows) >= n:
            break
    return rows


def reviews_tr(n=40, per_doc=14):
    """Kisa urun yorumlarini birlestirerek gayriresmi insan metni uretir."""
    from datasets import load_dataset
    print("Turkce urun yorumlari cekiliyor...")
    ds = load_dataset("fthbrmnby/turkish_product_reviews", split="train", streaming=True)
    buf, rows = [], []
    for r in ds:
        s = (r.get("sentence") or "").strip()
        if len(s.split()) < 6:
            continue
        buf.append(s if s.endswith((".", "!", "?")) else s + ".")
        if len(buf) >= per_doc:
            t = clip(" ".join(buf), lo=90)
            buf = []
            if t:
                rows.append({"text": t, "label": 0, "lang": "tr", "source": "urun-yorumlari"})
            if len(rows) >= n:
                break
    return rows


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("all", "en"):
        write(os.path.join(DATA, "human_en.jsonl"), raid_human(200))
    if what in ("all", "tr"):
        tr = ttc4900(120) + wikipedia_tr_hf(90) + reviews_tr(40)
        random.shuffle(tr)
        write(os.path.join(DATA, "human_tr.jsonl"), tr)
