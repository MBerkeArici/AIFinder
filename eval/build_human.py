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


def formal_en_train(n=130):
    """Gizlenmis kafanin EGITIMI icin akademik Ingilizce insan metni.

    NEDEN GEREKLI: Turkce tarafta ogrenilen ders Ingilizce'de uygulanmamisti.
    train_hidden2.py'nin insan tarafi Reddit (gayriresmi) + madencilik havuzu;
    akademik metin yok. Canli tarama sonucu: Reddit metinlerinde yanlis pozitif
    0/25, bilimsel makale ozetlerinde 2/25. Model resmi ve yogun akademik
    yazimi yapay zeka sanma egiliminde, cunku egitimde o usluptaki insan
    metnini yeterince gormemis.

    CAKISMA YASAGI: olcum seti data/human_en.jsonl'dir; buradan donen metinler
    onunla kesismemelidir.
    """
    from datasets import load_dataset

    used = set()
    ep = os.path.join(DATA, "human_en.jsonl")
    if os.path.exists(ep):
        with open(ep, encoding="utf-8") as f:
            for line in f:
                try:
                    used.add(json.loads(line)["text"][:80])
                except Exception:
                    pass
    print("Egitim icin akademik Ingilizce metin cekiliyor (olcumdeki %d haric)..."
          % len(used))

    ds = load_dataset("liamdugan/raid", "raid", split="train", streaming=True)
    rows = []
    for i, r in enumerate(ds):
        if r.get("model") != "human" or (r.get("attack") or "none") != "none":
            continue
        t = clip((r.get("generation") or "").strip())
        if not t or t[:80] in used:
            continue
        used.add(t[:80])
        rows.append({"text": t, "label": 0, "lang": "en",
                     "source": "raid-egitim/" + str(r.get("domain", "?")),
                     "kind": "resmi_insan"})
        if len(rows) >= n:
            break
        if i > 600000:
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


def formal_tr_train(n=110):
    """Gizlenmis kafanin EGITIMI icin resmi Turkce insan metni.

    NEDEN GEREKLI: kafa ilk surumde yalnizca birlestirilmis urun yorumlariyla
    egitilmisti. Sonuc olcumde goruldu — insan metinlerinin ortalama skoru
    0.524, ust ceyregi 0.97. Model "insan"i ogrenmemis, "birlestirilmis kisa
    yorum"u ogrenmisti; akici ve duzgun yazilmis haber/ansiklopedi metnini
    yapay zeka saniyordu. Yanlis pozitifin en pahali oldugu tur tam olarak bu.

    CAKISMA YASAGI: olcum seti data/human_tr.jsonl'dir. Buradan donen
    metinler onunla kesismemelidir, yoksa kafa kendi olcum verisi uzerinde
    egitilmis olur ve rapor gercek disi cikar. Kesisim metin onekiyle
    engellenir.
    """
    from datasets import load_dataset

    used = set()
    ep = os.path.join(DATA, "human_tr.jsonl")
    if os.path.exists(ep):
        with open(ep, encoding="utf-8") as f:
            for line in f:
                try:
                    used.add(json.loads(line)["text"][:80])
                except Exception:
                    pass
    print("Egitim icin resmi Turkce metin cekiliyor (olcumdeki %d metin haric)..."
          % len(used))

    rows = []
    ds = load_dataset("savasy/ttc4900", split="train")
    idx = list(range(len(ds)))
    random.Random(777).shuffle(idx)          # olcumden FARKLI siralama
    for i in idx:
        t = clip((ds[i]["text"] or "").strip())
        if not t or t[:80] in used:
            continue
        used.add(t[:80])
        rows.append({"text": t, "label": 0, "lang": "tr",
                     "source": "ttc4900-egitim", "kind": "resmi_insan"})
        if len(rows) >= n - 25:      # agirlik yerel derlemde: akis cok yavas
            break

    wd = load_dataset("wikimedia/wikipedia", "20231101.tr", split="train", streaming=True)
    for i, r in enumerate(wd):
        if i % 5 != 3:                       # olcumdeki "i %% 7 == 0" ile ortusmez
            continue
        body = re.sub(r"\n{2,}", "\n\n", (r.get("text") or "").strip())
        t = clip(body)
        if not t or t[:80] in used:
            continue
        used.add(t[:80])
        rows.append({"text": t, "label": 0, "lang": "tr",
                     "source": "wikipedia-tr-egitim", "kind": "resmi_insan"})
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


def informal_tr(n=170, per_doc=26):
    """Gayriresmi Turkce insan metni — USLUP DENGESI icin zorunlu.

    engine/hidden.py'nin notu: egitimde insan tarafi uslup olarak esitlenmezse
    model yapay zekayi degil "resmi dil"i ogrenir. Turkce gizlenmis AI
    ornekleri (eval/ai_tr_hidden.py) gunluk uslupta yazildi; karsilarina
    ayni uslupta insan metni konmazsa model "samimi yazi = AI" gibi ters ve
    zararli bir kural ogrenir. Haber ve Vikipedi bu dengeyi saglamiyor.

    Yorumlar tek tek cok kisa; 140 kelimelik olcum bandini karsilamak icin
    birlestiriliyor. Birlestirme yapaylik katiyor ama alternatif, gayriresmi
    insan metnini tumuyle disarida birakmak.
    """
    from datasets import load_dataset
    print("Gayriresmi Turkce metin (urun yorumlari) cekiliyor...")
    ds = load_dataset("fthbrmnby/turkish_product_reviews", split="train", streaming=True)
    buf, rows, seen = [], [], set()
    for r in ds:
        t = (r.get("sentence") or "").strip()
        if len(t.split()) < 8 or t[:40] in seen:
            continue
        seen.add(t[:40])
        buf.append(t if t.endswith((".", "!", "?")) else t + ".")
        if len(buf) >= per_doc:
            doc = clip(" ".join(buf), lo=145)
            buf = []
            if doc:
                rows.append({"text": doc, "label": 0, "lang": "tr",
                             "source": "urun-yorumlari", "kind": "gayriresmi_insan"})
            if len(rows) >= n:
                break
    return rows


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("all", "en"):
        write(os.path.join(DATA, "human_en.jsonl"), raid_human(200))
    if what in ("all", "en", "formal-en"):
        write(os.path.join(DATA, "human_en_formal_train.jsonl"), formal_en_train(130))
    if what in ("all", "tr"):
        tr = ttc4900(120) + wikipedia_tr_hf(90) + reviews_tr(40)
        random.shuffle(tr)
        write(os.path.join(DATA, "human_tr.jsonl"), tr)
    if what in ("all", "tr", "informal"):
        write(os.path.join(DATA, "human_tr_informal.jsonl"), informal_tr(170))
    if what in ("all", "tr", "formal-train"):
        write(os.path.join(DATA, "human_tr_formal_train.jsonl"), formal_tr_train(110))
