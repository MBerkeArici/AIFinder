# -*- coding: utf-8 -*-
"""Ingilizce saldiri ureteci — EGITIM verisi icin.

NEDEN: Olcum, esanlamli degistirme saldirisinda yakalamanin %60'a dustugunu
gosteriyor (RAID'in gercek saldiri verisi, yani guvenilir bir rakam). Gizli
kafa bu tur bozulmalari hic gormeden egitildigi icin, kelimeler degistiginde
gomudeki imzayi takip edemiyor.

Cozum saldiriya karsi egitim: egitim metinlerinin bozulmus varyantlari da
egitime katilir, boylece model yuzeysel degisimlere degil altta yatan imzaya
bakmayi ogrenir.

KRITIK DENGE: saldiri YALNIZCA AI metinlerine uygulanirsa model yanlis sey
ogrenir — "bozuk karakter varsa AI" gibi. Gercek hayatta bir insan metni de
kopyalanirken tuhaf karakter tasiyabilir. Bu yuzden ayni donusumler INSAN
metinlerine de uygulanir ve etiketleri degismez.

CAKISMA YASAGI: kaynak yalnizca EGITIM kumeleridir. Olcum setine
(ai_en.jsonl, ai_en_attack.jsonl, human_en.jsonl) dokunulmaz — aksi halde
model kendi sinavinin sorularini ezberlemis olur.
"""
import json
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
random.seed(90210)

SYN = {
    "important": "significant", "significant": "considerable", "however": "nevertheless",
    "therefore": "thus", "additionally": "moreover", "furthermore": "in addition",
    "approach": "method", "method": "technique", "result": "outcome",
    "increase": "rise", "decrease": "decline", "show": "demonstrate",
    "use": "employ", "make": "create", "help": "assist", "need": "require",
    "problem": "issue", "change": "shift", "large": "substantial",
    "small": "modest", "many": "numerous", "various": "diverse",
    "because": "since", "although": "though", "often": "frequently",
    "provide": "offer", "consider": "regard", "suggest": "indicate",
    "study": "research", "find": "discover", "improve": "enhance",
    "reduce": "lower", "develop": "build", "understand": "grasp",
    "quality": "standard", "process": "procedure", "system": "framework",
}
HOMOGLYPH = {"a": "а", "e": "е", "o": "о", "c": "с", "p": "р", "x": "х", "y": "у"}
ZWSP = "​"


def synonym(text, rate=0.6):
    def swap(m):
        w = m.group(0)
        k = w.lower()
        if k in SYN and random.random() < rate:
            rep = SYN[k]
            return rep.capitalize() if w[0].isupper() else rep
        return w
    return re.sub(r"[A-Za-z]+", swap, text)


def homoglyph(text, rate=0.05):
    return "".join(HOMOGLYPH[c] if c in HOMOGLYPH and random.random() < rate else c
                   for c in text)


def whitespace(text, rate=0.05):
    return " ".join(w + (ZWSP if random.random() < rate else "")
                    for w in text.split(" "))


def punctuation(text):
    text = text.replace("—", "-").replace("–", "-")
    text = text.replace("“", '"').replace("”", '"').replace("’", "'")
    return re.sub(r",\s+(?=(but|and|however)\b)", " ", text)


def mixed(text):
    return whitespace(homoglyph(punctuation(synonym(text, 0.4)), 0.03), 0.03)


ATTACKS = {"synonym": synonym, "homoglyph": homoglyph,
           "whitespace": whitespace, "punctuation": punctuation, "mixed": mixed}

# Yalnizca EGITIM kumeleri. Olcum kumeleri kasitla disarida.
SOURCES = ["ai_en_hidden.jsonl", "mined_train.jsonl", "human_en_informal.jsonl",
           "human_en_formal_train.jsonl"]


def main():
    rows = []
    for name in SOURCES:
        p = os.path.join(DATA, name)
        if not os.path.exists(p):
            print("  atlandi (yok): %s" % name)
            continue
        with open(p, encoding="utf-8") as f:
            for line in f:
                r = json.loads(line)
                if len(r["text"].split()) >= 140:
                    rows.append(r)

    if not rows:
        print("HATA: egitim kumesi bulunamadi")
        return

    out = []
    for r in rows:
        # her metne rastgele tek bir saldiri: kume sismesin, cesitlilik kalsin
        name = random.choice(list(ATTACKS))
        t = ATTACKS[name](r["text"])
        if t == r["text"]:
            continue
        c = dict(r)
        c["text"] = t
        c["attack"] = name
        c["source"] = str(r.get("source", "?")) + "+" + name
        out.append(c)

    path = os.path.join(DATA, "attacked_train_en.jsonl")
    with open(path, "w", encoding="utf-8") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    import collections
    lab = collections.Counter(r["label"] for r in out)
    atk = collections.Counter(r["attack"] for r in out)
    print("  -> attacked_train_en.jsonl (%d kayit)" % len(out))
    print("     etiket dagilimi: AI %d, insan %d" % (lab.get(1, 0), lab.get(0, 0)))
    print("     (ikisi de bozulur; yalnizca AI bozulsaydi model 'bozulma = AI' ogrenirdi)")
    print("     saldiri dagilimi: %s" % dict(atk))


if __name__ == "__main__":
    main()
