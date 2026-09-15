# -*- coding: utf-8 -*-
"""Saldiri normalizasyonu — analiz oncesi metin temizligi.

RAID olcumunde iki saldiri turu tespit oranini cokertiyordu:

  homoglif  : %3.3 yakalama — Latin harfleri gorsel olarak ayni Kiril/Yunan
              harfleriyle degistirilince tokenizer metni tamamen farkli
              gorup sasiriyor ve perplexity yapay olarak yukseliyor.
  bosluk    : %93 yakalama — gorunmez karakterler kelime sinirlarini bozuyor.

Ikisi de modelin sucu degil, girdinin bozulmasi. Cozum de modelde degil,
burada: metni analizden once kanonik hale getir.

Turkce harfler (ı ğ ş ç ö ü) KORUNUR — bunlar mesru karakterlerdir,
confusable degildir.
"""
import re
import unicodedata

# Gorsel olarak Latin harflerle ayni olan Kiril ve Yunan harfleri
CONFUSABLES = {
    # Kiril -> Latin
    "А": "A", "В": "B", "Е": "E", "К": "K", "М": "M", "Н": "H", "О": "O",
    "Р": "P", "С": "C", "Т": "T", "У": "Y", "Х": "X", "Ѕ": "S", "І": "I",
    "Ј": "J", "Ԛ": "Q", "Ԝ": "W", "Ғ": "F",
    "а": "a", "е": "e", "о": "o", "р": "p", "с": "c", "х": "x", "у": "y",
    "ѕ": "s", "і": "i", "ј": "j", "ԛ": "q", "ԝ": "w", "ь": "b", "ѵ": "v",
    # Yunan -> Latin
    "Α": "A", "Β": "B", "Ε": "E", "Ζ": "Z", "Η": "H", "Ι": "I", "Κ": "K",
    "Μ": "M", "Ν": "N", "Ο": "O", "Ρ": "P", "Τ": "T", "Υ": "Y", "Χ": "X",
    "ο": "o", "ν": "v", "α": "a", "ρ": "p", "τ": "t", "υ": "u", "χ": "x",
    "ϲ": "c", "ϳ": "j", "ı": None,          # None = dokunma (Turkce)
    # Diger
    "ℓ": "l", "Ⅰ": "I", "Ⅴ": "V", "Ⅹ": "X", "𝐚": "a", "ﬁ": "fi", "ﬂ": "fl",
}
CONFUSABLES = {k: v for k, v in CONFUSABLES.items() if v is not None}

# Gorunmez / sifir genislikli karakterler
INVISIBLE = re.compile(
    "[​‌‍⁠﻿᠎­͏"
    "⁡⁢⁣⁤⁪-⁯]")

# Alisilmadik bosluklar -> normal bosluk
ODD_SPACE = re.compile("[  -   　 ]")

_TR_KEEP = set("çğıİöşüÇĞÖŞÜâîûÂÎÛ")


def normalize(text):
    """Metni analiz icin kanonik hale getirir. Ne degistigini de bildirir.

    Doner: (temizlenmis_metin, {'homoglif': n, 'gorunmez': n, 'bosluk': n})
    """
    if not text:
        return text, {}

    stats = {}

    n = len(INVISIBLE.findall(text))
    if n:
        text = INVISIBLE.sub("", text)
        stats["gorunmez"] = n

    n = len(ODD_SPACE.findall(text))
    if n:
        text = ODD_SPACE.sub(" ", text)
        stats["bosluk"] = n

    hits = 0
    out = []
    for ch in text:
        if ch in _TR_KEEP:
            out.append(ch)
            continue
        rep = CONFUSABLES.get(ch)
        if rep is not None:
            out.append(rep)
            hits += 1
        else:
            out.append(ch)
    if hits:
        text = "".join(out)
        stats["homoglif"] = hits

    # Uyumluluk normalizasyonu (tam genislikli, bitisik harf vb.)
    nfkc = unicodedata.normalize("NFKC", text)
    if nfkc != text:
        stats["unicode"] = 1
        text = nfkc

    # Kelime araligi tekrarlarini sadelestir (bosluk enjeksiyonu)
    collapsed = re.sub(r"[ \t]{2,}", " ", text)
    if collapsed != text:
        stats["fazla_bosluk"] = 1
        text = collapsed

    return text, stats


def report(stats):
    """Kullaniciya gosterilecek uyari satirlari."""
    notes = []
    if stats.get("homoglif"):
        notes.append({"label": "Homoglif karakter", "flag": "warn",
                      "value": "%d karakter Latin harfleriyle görsel olarak aynı olan "
                               "Kiril/Yunan harfleriyle değiştirilmiş. Bu, tespit araçlarını "
                               "atlatmak için kullanılan bilinen bir yöntemdir; "
                               "analiz öncesi düzeltildi." % stats["homoglif"]})
    if stats.get("gorunmez"):
        notes.append({"label": "Görünmez karakter", "flag": "warn",
                      "value": "%d adet sıfır genişlikli karakter bulundu ve temizlendi. "
                               "Normal yazıda bulunmaz." % stats["gorunmez"]})
    if stats.get("bosluk") or stats.get("fazla_bosluk"):
        notes.append({"label": "Boşluk düzensizliği", "flag": "info",
                      "value": "Alışılmadık boşluk karakterleri normale çevrildi."})
    return notes
