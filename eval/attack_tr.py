# -*- coding: utf-8 -*-
"""Turkce saldiri simulatoru — aracin kendi dayanikliligini olcer.

NEDEN VAR: Ingilizce tarafta RAID'in saldirili ornekleri sayesinde dayaniklilik
olculebiliyor (parafrazda %75, esanlamli degistirmede %60'a dusuyor). Turkce
icin boyle bir kume yoktu; raporda "Saldiri altinda" bolumu yalnizca Ingilizce
icin vardi. Yani Turkce'de bir metin "humanizer"dan gecirildiginde ne oldugunu
bilmiyorduk. Bu dosya o boslugu kapatir.

KAPSAM SINIRI: burasi bir OLCUM aracidir, arayuze bagli degildir. Amaci
tespiti atlatmayi kolaylastirmak degil, atlatmanin ne kadar kolay oldugunu
sayiyla gostermek ve gerekirse egitim verisini bu ornekleri de icerecek
sekilde guclendirmek.

Uygulanan saldirilar (RAID'in tasnifiyle ayni aileler):
  esanlamli      yaygin kelimelerin esanlamlilariyla degistirilmesi
  homoglif       goruntusu ayni, kodu farkli harfler (Latin -> Kiril)
  bosluk         kelime aralarina sifir genislikli karakter enjeksiyonu
  noktalama      virgul ekleme/cikarma, uzun tirelerin sadelestirilmesi
  karma          yukaridakilerin hafif dozda birlestirilmesi

Parafraz saldirisi burada YOK: gercek parafraz anlam koruyarak yeniden yazmayi
gerektirir, mekanik olarak taklit edilemez. Elle yazilmis parafraz ornekleri
ayri dosyada tutulur (eval/ai_tr_paraphrase.py).
"""
import json
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
sys.path.insert(0, ROOT)
random.seed(31337)

# Turkce yaygin kelime -> esanlamli. Ek almis biciminde de eslesmesi icin
# kok eslestirme yapilmaz; yalnizca tam kelime degisimi uygulanir.
SYN = {
    "önemli": "mühim", "büyük": "geniş", "küçük": "ufak", "gerekli": "lüzumlu",
    "sorun": "problem", "çözüm": "hal", "durum": "vaziyet", "amaç": "hedef",
    "sonuç": "netice", "etki": "tesir", "değişim": "dönüşüm", "gelişme": "ilerleme",
    "kullanım": "kullanma", "yöntem": "metot", "olanak": "imkân", "koşul": "şart",
    "süreç": "işleyiş", "artış": "yükseliş", "azalma": "düşüş", "katkı": "fayda",
    "yaklaşım": "bakış", "ihtiyaç": "gereksinim", "bölge": "yöre", "alan": "saha",
    "çalışma": "faaliyet", "uygulama": "tatbik", "değerlendirme": "inceleme",
    "belirli": "muayyen", "çeşitli": "farklı", "genel": "umumi", "özel": "hususi",
    "hızlı": "süratli", "kolay": "basit", "zor": "güç", "yeni": "taze",
    "ancak": "fakat", "bununla birlikte": "yine de", "ayrıca": "bunun yanında",
    "dolayısıyla": "bu yüzden", "örneğin": "mesela", "genellikle": "çoğunlukla",
}

# Goruntusu ayni, Unicode kod noktasi farkli harfler
HOMOGLYPH = {"a": "а", "e": "е", "o": "о", "c": "с", "p": "р", "x": "х",
             "y": "у", "i": "і", "s": "ѕ", "A": "А", "B": "В", "E": "Е",
             "K": "К", "M": "М", "O": "О", "T": "Т"}
ZWSP = "​"


def synonym(text, rate=0.55):
    def swap(m):
        w = m.group(0)
        key = w.lower()
        if key in SYN and random.random() < rate:
            rep = SYN[key]
            return rep.capitalize() if w[0].isupper() else rep
        return w
    return re.sub(r"[A-Za-zÇĞİÖŞÜçğıöşü]+", swap, text)


def homoglyph(text, rate=0.06):
    out = []
    for ch in text:
        if ch in HOMOGLYPH and random.random() < rate:
            out.append(HOMOGLYPH[ch])
        else:
            out.append(ch)
    return "".join(out)


def whitespace(text, rate=0.05):
    words = text.split(" ")
    return " ".join(w + (ZWSP if random.random() < rate else "") for w in words)


def punctuation(text):
    text = text.replace("—", "-").replace("–", "-")
    text = text.replace("“", '"').replace("”", '"').replace("’", "'")
    # bazi virgulleri dusur, bazi "ve" once virgul ekle
    text = re.sub(r",\s+(?=(ancak|fakat|ama)\b)", " ", text)
    text = re.sub(r"\s+ve\s+", lambda m: ", ve " if random.random() < 0.3 else m.group(0), text)
    return text


def mixed(text):
    return whitespace(homoglyph(punctuation(synonym(text, rate=0.35)), rate=0.03), rate=0.03)


ATTACKS = {"esanlamli": synonym, "homoglif": homoglyph,
           "bosluk": whitespace, "noktalama": punctuation, "karma": mixed}


def main():
    src = os.path.join(DATA, "ai_tr.jsonl")
    if not os.path.exists(src):
        print("HATA: data/ai_tr.jsonl yok — once eval/build_ai_tr.py")
        return
    rows = [json.loads(l) for l in open(src, encoding="utf-8")]
    rows = [r for r in rows if len(r["text"].split()) >= 140]

    out = []
    for name, fn in ATTACKS.items():
        for r in rows:
            t = fn(r["text"])
            if t == r["text"]:
                continue
            out.append({"text": t, "label": 1, "lang": "tr",
                        "source": r["source"], "attack": name})

    # parafraz ornekleri (elle yazilmis) varsa eklenir
    try:
        sys.path.insert(0, HERE)
        import ai_tr_paraphrase
        para = ai_tr_paraphrase.rows()
        out.extend(para)
        print("  parafraz ornekleri eklendi: %d" % len(para))
    except ImportError:
        print("  not: elle yazilmis parafraz kumesi yok (ai_tr_paraphrase.py)")

    path = os.path.join(DATA, "ai_tr_attack.jsonl")
    with open(path, "w", encoding="utf-8") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    import collections
    c = collections.Counter(r["attack"] for r in out)
    print("  -> ai_tr_attack.jsonl (%d kayit)" % len(out))
    for k, v in sorted(c.items()):
        print("     %-12s %d" % (k, v))


if __name__ == "__main__":
    main()
