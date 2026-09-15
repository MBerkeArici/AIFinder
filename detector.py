# -*- coding: utf-8 -*-
"""
Sezgisel (heuristic) AI-metin analiz motoru.
Turkce + Ingilizce destekler. Istatistiksel ve stilometrik sinyalleri
birlestirerek 0-100 arasi bir "AI benzerligi" skoru uretir.

ONEMLI: Bu bir kanit uretici degildir. Olasiliksal bir gostergedir.
"""
import math
import re
import statistics
from collections import Counter

# ----------------------------------------------------------------------------
# Sozluklar
# ----------------------------------------------------------------------------

TR_TRANSITIONS = [
    "ayrica", "bununla birlikte", "bunun yani sira", "ote yandan", "dolayisiyla",
    "bu nedenle", "bu sayede", "sonuc olarak", "ozetle", "ilk olarak", "ikinci olarak",
    "son olarak", "ornegin", "bir diger deyisle", "baska bir deyisle", "kisacasi",
    "bu baglamda", "bu dogrultuda", "bu cercevede", "genel olarak", "ozellikle",
    "ancak", "fakat", "ne var ki", "bunun sonucunda", "bu acidan", "buna ek olarak",
    "unutulmamalidir ki", "belirtmek gerekir ki", "goze carpmaktadir",
]

EN_TRANSITIONS = [
    "furthermore", "moreover", "in addition", "additionally", "however",
    "nevertheless", "nonetheless", "therefore", "thus", "consequently",
    "as a result", "in conclusion", "to conclude", "overall", "in summary",
    "first of all", "firstly", "secondly", "lastly", "for instance",
    "for example", "on the other hand", "in other words", "that said",
    "it is worth noting", "it should be noted",
]

TR_CLICHES = [
    "gunumuzde", "gunumuz dunyasinda", "dijital cagda", "teknolojinin hizla gelistigi",
    "hizla gelisen", "onemli bir rol oynamaktadir", "onemli bir yer tutmaktadir",
    "buyuk onem tasimaktadir", "dikkat cekmektedir", "on plana cikmaktadir",
    "kritik bir oneme sahiptir", "vazgecilmez bir parcasi", "ayrilmaz bir parcasi",
    "gelismis teknolojiler sayesinde", "bir dizi", "genis bir yelpaze",
    "cok yonlu bir", "etkili bir sekilde", "verimli bir sekilde",
    "surdurulebilir bir", "yenilikci cozumler", "hayatimizin her alaninda",
    "soz konusu oldugunda", "degerlendirildiginde", "bu makalede ele alinacaktir",
    "detayli bir sekilde incelenecektir", "unutulmamalidir ki", "sonuc olarak",
    "kisacasi", "bu yazida", "adim adim", "bir bakalim",
]

EN_CLICHES = [
    "in today's world", "in the digital age", "in the modern era",
    "rapidly evolving", "ever-evolving", "plays a crucial role",
    "plays a vital role", "plays a significant role", "it is important to note",
    "it's important to note", "delve into", "delving into", "a testament to",
    "tapestry", "landscape of", "navigate the", "unlock the potential",
    "harness the power", "at the forefront", "cornerstone of",
    "when it comes to", "a wide range of", "a myriad of", "seamless",
    "robust", "leverage", "underscores", "pivotal", "paradigm shift",
    "not only ... but also", "in conclusion", "let's dive in",
    "game-changer", "cutting-edge", "holistic approach", "comprehensive overview",
]

# Insan isareti: konusma dili, argo, kisaltma, duygusal ifadeler
TR_INFORMAL = [
    "yani", "iste", "ya", "hani", "bence", "valla", "abi", "ee", "hadi",
    "falan", "filan", "bi ", "napiyor", "napti", "cok iyi ya", "of ", "ya ni",
    "sey", "gercekten ya", "bilmiyorum", "sanirim", "galiba", "herhalde",
    "aslinda", "keske", "ulan", "be ", "aman", "vay", "eh ", "tamam da",
]

EN_INFORMAL = [
    "i mean", "kinda", "sorta", "gonna", "wanna", "yeah", "yep", "nope",
    "honestly", "tbh", "btw", "lol", "idk", "imo", "dunno", "stuff like that",
    "y'know", "you know", "i guess", "whatever", "pretty much", "a bit",
    "anyway", "oh ", "ugh", "hmm", "damn",
]

TR_CHARS = set("çğıöşüÇĞİÖŞÜ")
TR_HINT_WORDS = {"ve", "bir", "bu", "ile", "için", "olarak", "daha", "gibi", "de", "da"}

ABBREV = [
    "vb.", "vs.", "örn.", "bkz.", "Dr.", "Prof.", "Doç.", "Av.", "Sn.", "yy.",
    "Mr.", "Mrs.", "Ms.", "Dr.", "Prof.", "e.g.", "i.e.", "etc.", "vol.", "No.",
]


# ----------------------------------------------------------------------------
# Yardimcilar
# ----------------------------------------------------------------------------

def _fold(text):
    """Turkce karakterleri sadelestirerek kucuk harfe cevir (eslesme icin)."""
    tr = str.maketrans("çğıöşüÇĞİÖŞÜÂâÎîÛû", "cgiosucgiosuAaIiUu")
    return text.translate(tr).lower()


def ramp(value, at_zero, at_hundred):
    """at_zero -> 0 puan, at_hundred -> 100 puan; arada dogrusal, disinda kirpilir."""
    if at_hundred == at_zero:
        return 50.0
    ratio = (value - at_zero) / (at_hundred - at_zero)
    return max(0.0, min(100.0, ratio * 100.0))


def split_sentences(text):
    masked = text
    for i, ab in enumerate(ABBREV):
        masked = masked.replace(ab, "\x00%d\x00" % i)
    parts = re.split(r"(?<=[.!?…])[\s\n]+|\n{2,}", masked)
    out = []
    for p in parts:
        for i, ab in enumerate(ABBREV):
            p = p.replace("\x00%d\x00" % i, ab)
        p = p.strip()
        if len(p.split()) >= 3:
            out.append(p)
    return out


def tokenize(text):
    return re.findall(r"[0-9A-Za-zÇĞİÖŞÜçğıöşüÂÎÛâîû']+", text)


def mtld_one_way(tokens, threshold=0.72):
    factors, types, count = 0, set(), 0
    for t in tokens:
        types.add(t)
        count += 1
        if len(types) / count <= threshold:
            factors += 1
            types, count = set(), 0
    if count > 0:
        ttr = len(types) / count
        factors += (1 - ttr) / (1 - threshold)
    return len(tokens) / factors if factors > 0 else float(len(tokens))


def mtld(tokens):
    if len(tokens) < 30:
        return 0.0
    return (mtld_one_way(tokens) + mtld_one_way(list(reversed(tokens)))) / 2.0


def count_phrases(folded_text, phrases):
    hits = Counter()
    for ph in phrases:
        if "..." in ph:
            a, b = ph.split(" ... ")
            if a in folded_text and b in folded_text:
                hits[ph] += 1
            continue
        n = folded_text.count(ph)
        if n:
            hits[ph] += n
    return hits


def detect_lang(text):
    folded_tokens = set(_fold(text).split())
    tr_score = len(folded_tokens & {_fold(w) for w in TR_HINT_WORDS})
    has_tr_chars = any(c in TR_CHARS for c in text[:4000])
    return "tr" if (tr_score >= 3 or has_tr_chars) else "en"


# ----------------------------------------------------------------------------
# Metrikler
# ----------------------------------------------------------------------------

def m_burstiness(sentences):
    """Insan yazisi dalgalidir: kisa-uzun cumleler karisir. AI duzenli yazar."""
    lengths = [len(tokenize(s)) for s in sentences]
    if len(lengths) < 4:
        return None
    mean = statistics.mean(lengths)
    sd = statistics.pstdev(lengths)
    cv = sd / mean if mean else 0
    score = ramp(cv, 0.62, 0.20)  # dusuk CV -> yuksek AI puani
    return {
        "score": score,
        "detail": "Cümle uzunluğu değişkenliği (CV): %.2f — ortalama %.1f kelime" % (cv, mean),
        "raw": round(cv, 3),
    }


def m_sentence_starters(sentences):
    """AI cumle baslangiclarini tekrarlar; insan daha cesitlidir."""
    if len(sentences) < 5:
        return None
    starters = [_fold(tokenize(s)[0]) for s in sentences if tokenize(s)]
    uniq = len(set(starters)) / len(starters)
    score = ramp(uniq, 0.95, 0.50)
    dupes = [w for w, c in Counter(starters).most_common(3) if c > 1]
    return {
        "score": score,
        "detail": "Farklı cümle başlangıcı oranı: %%%.0f%s" % (
            uniq * 100, (" — tekrar edenler: " + ", ".join(dupes)) if dupes else ""),
        "raw": round(uniq, 3),
    }


def m_paragraph_uniformity(text):
    """AI paragraflari birbirine cok yakin uzunlukta olur."""
    paras = [p for p in re.split(r"\n\s*\n", text) if len(tokenize(p)) >= 15]
    if len(paras) < 3:
        return None
    lengths = [len(tokenize(p)) for p in paras]
    mean = statistics.mean(lengths)
    cv = statistics.pstdev(lengths) / mean if mean else 0
    score = ramp(cv, 0.55, 0.10)
    return {
        "score": score,
        "detail": "%d paragraf, uzunluk değişkenliği (CV): %.2f" % (len(paras), cv),
        "raw": round(cv, 3),
    }


def m_ngram_repeat(tokens):
    """Tekrarlayan 4'lu kelime obekleri sablonlu uretimi gosterir."""
    if len(tokens) < 80:
        return None
    low = [_fold(t) for t in tokens]
    grams = [" ".join(low[i:i + 4]) for i in range(len(low) - 3)]
    c = Counter(grams)
    repeated = sum(v for v in c.values() if v > 1)
    ratio = repeated / len(grams)
    score = ramp(ratio, 0.01, 0.14)
    top = [g for g, n in c.most_common(2) if n > 1]
    return {
        "score": score,
        "detail": "Tekrar eden 4'lü öbek oranı: %%%.1f%s" % (
            ratio * 100, (" — örn. \"%s\"" % top[0]) if top else ""),
        "raw": round(ratio, 4),
    }


def m_lexical(tokens):
    """Kelime cesitliligi. Cok dusuk cesitlilik + cok az 'tek kullanimlik'
    kelime, sablonlu metnin isaretidir."""
    if len(tokens) < 60:
        return None
    low = [_fold(t) for t in tokens]
    c = Counter(low)
    hapax = sum(1 for v in c.values() if v == 1) / len(c)
    md = mtld(low)
    s_hapax = ramp(hapax, 0.70, 0.35)
    s_mtld = ramp(md, 110, 45)
    score = 0.5 * s_hapax + 0.5 * s_mtld
    return {
        "score": score,
        "detail": "MTLD: %.0f | tek kullanımlık kelime oranı: %%%.0f" % (md, hapax * 100),
        "raw": round(md, 1),
    }


def m_transitions(text, sentences, lang):
    """AI her cumleyi bir baglayiciyla acar."""
    if len(sentences) < 4:
        return None
    folded = _fold(text)
    phrases = TR_TRANSITIONS if lang == "tr" else EN_TRANSITIONS
    hits = count_phrases(folded, phrases)
    total = sum(hits.values())
    per_sentence = total / len(sentences)
    score = ramp(per_sentence, 0.06, 0.45)
    top = ", ".join("%s (%d)" % (k, v) for k, v in hits.most_common(3))
    return {
        "score": score,
        "detail": "Cümle başına geçiş ifadesi: %.2f%s" % (
            per_sentence, (" — " + top) if top else ""),
        "raw": round(per_sentence, 3),
    }


def m_cliches(text, tokens, lang):
    """Modellerin asiri kullandigi kalip ifadeler."""
    if len(tokens) < 40:
        return None
    folded = _fold(text)
    phrases = (TR_CLICHES if lang == "tr" else EN_CLICHES)
    hits = count_phrases(folded, phrases)
    total = sum(hits.values())
    per100 = total / len(tokens) * 100
    score = ramp(per100, 0.15, 2.2)
    top = ", ".join("“%s” (%d)" % (k, v) for k, v in hits.most_common(4))
    return {
        "score": score,
        "detail": ("Bulunan kalıp: " + top) if top else "Bilinen AI kalıbı bulunamadı",
        "raw": round(per100, 2),
        "matches": [k for k, _ in hits.most_common(12)],
    }


def m_punctuation(text, tokens):
    """AI: uzun tire ve tipografik tirnak sever; unlem/uc nokta/parantezden kacinir."""
    if len(tokens) < 60:
        return None
    n = len(tokens) / 1000.0
    dash = (text.count("—") + text.count("–")) / n
    curly = (text.count("“") + text.count("”") + text.count("’")) / n
    excl = text.count("!") / n
    ellip = (text.count("...") + text.count("…")) / n
    paren = text.count("(") / n
    s_dash = ramp(dash, 0.3, 9.0)
    s_curly = ramp(curly, 0.5, 14.0)
    s_human = ramp(excl + ellip + paren, 9.0, 0.0)  # hic yoksa AI puani yukselir
    score = 0.35 * s_dash + 0.20 * s_curly + 0.45 * s_human
    return {
        "score": score,
        "detail": "1000 kelimede — uzun tire: %.1f, ünlem: %.1f, üç nokta: %.1f, parantez: %.1f"
                  % (dash, excl, ellip, paren),
        "raw": round(dash, 2),
    }


def m_informality(text, tokens, lang):
    """Konusma dili, tereddut, argo = guclu insan sinyali."""
    if len(tokens) < 50:
        return None
    folded = _fold(text)
    phrases = TR_INFORMAL if lang == "tr" else EN_INFORMAL
    hits = count_phrases(folded, phrases)
    total = sum(hits.values())
    # yazim/duzen kusurlari da insan isareti
    typos = len(re.findall(r"\s{2,}", text)) + len(re.findall(r"[,.!?]{2,}", text))
    typos += len(re.findall(r"[a-zçğıöşü]\s+[a-zçğıöşü]{2,}\s*[.!?]\s+[a-zçğıöşü]", text))
    emoji = len(re.findall(r"[\U0001F300-\U0001FAFF☀-➿]", text))
    signal = (total + typos * 0.6 + emoji * 1.5) / len(tokens) * 100
    score = ramp(signal, 1.6, 0.0)  # hic gayriresmi iz yoksa AI puani 100
    top = ", ".join("“%s”" % k for k, _ in hits.most_common(3))
    return {
        "score": score,
        "detail": ("Günlük dil izleri: " + top) if top
                  else "Günlük dil / doğal kusur izi yok (çok düzgün metin)",
        "raw": round(signal, 2),
    }


METRIC_META = {
    "burstiness":   ("Cümle ritmi (burstiness)", 0.20,
                     "İnsanlar kısa ve uzun cümleleri karıştırır; modeller tekdüze yazar."),
    "transitions":  ("Geçiş ifadesi yoğunluğu", 0.13,
                     "“Ayrıca”, “sonuç olarak” gibi bağlayıcıların aşırı kullanımı."),
    "cliches":      ("AI kalıp ifadeleri", 0.14,
                     "Dil modellerinin istatistiksel olarak fazla ürettiği klişeler."),
    "lexical":      ("Kelime çeşitliliği", 0.10,
                     "MTLD ve tek kullanımlık kelime oranı."),
    "punctuation":  ("Noktalama profili", 0.10,
                     "Uzun tire/tipografik tırnak fazlalığı, ünlem-parantez yokluğu."),
    "informality":  ("Doğallık / günlük dil", 0.10,
                     "Konuşma dili, tereddüt, küçük kusurlar güçlü insan işaretidir."),
    "sentence_starters": ("Cümle başlangıç çeşitliliği", 0.08,
                     "Aynı kelimeyle başlayan cümlelerin tekrarı."),
    "ngram_repeat": ("Öbek tekrarı", 0.08,
                     "Aynı 4 kelimelik dizilerin metin boyunca tekrarlanması."),
    "para_uniformity": ("Paragraf tekdüzeliği", 0.07,
                     "Paragrafların birbirine çok yakın uzunlukta olması."),
}


# ----------------------------------------------------------------------------
# Cumle bazli isi haritasi
# ----------------------------------------------------------------------------

def sentence_heat(sentences, lang, global_mean):
    """Cumle bazli BICEM ISARETI — olasilik DEGILDIR.

    Bu deger kalibre edilmemistir ve taban puani 40'tir: hicbir yapay zeka
    isareti tasimayan bir cumle bile 40 alir. Kalip ifade +18, gecis
    kelimesi +11 ekler. Yani "70", "bu cumlede iki kalip var" demektir,
    "bu cumle %70 ihtimalle yapay zeka" demek degil.

    Yuzde olarak gosterilirse kullanici bunu olasilik sanar ve pencere
    kararlariyla celisir gorunur (pencere %0 derken cumleler %70 gorunur).
    Bu yuzden disariya nitel seviye olarak verilir; ham puan yalnizca
    siralama icindir.
    """
    folded_cliches = TR_CLICHES if lang == "tr" else EN_CLICHES
    folded_trans = TR_TRANSITIONS if lang == "tr" else EN_TRANSITIONS
    out = []
    for s in sentences:
        f = _fold(s)
        n = len(tokenize(s))
        sc = 40.0
        if global_mean:
            dev = abs(n - global_mean) / global_mean
            sc += ramp(dev, 0.55, 0.0) * 0.30   # ortalamaya cok yakinsa AI'ye yaklas
        c_hits = sum(1 for p in folded_cliches if p in f)
        t_hits = sum(1 for p in folded_trans if p in f)
        sc += min(30, c_hits * 18) + min(18, t_hits * 11)
        if "—" in s or "–" in s:
            sc += 6
        if any(x in s for x in ("!", "...", "…")):
            sc -= 14
        raw = max(0, min(100, round(sc)))
        # taban 40 oldugu icin esikler ona gore: 40 = isaret yok
        if raw >= 75:
            level, label = 3, "belirgin kalıp"
        elif raw >= 58:
            level, label = 2, "bir miktar kalıp"
        elif raw >= 45:
            level, label = 1, "hafif iz"
        else:
            level, label = 0, "işaret yok"
        out.append({"text": s, "level": level, "label": label, "raw": raw})
    return out


# ----------------------------------------------------------------------------
# Ana giris
# ----------------------------------------------------------------------------

def analyze(text, forensics=None):
    text = (text or "").replace("\r\n", "\n").strip()
    tokens = tokenize(text)
    sentences = split_sentences(text)

    if len(tokens) < 40:
        return {
            "ok": False,
            "error": "Analiz için en az ~40 kelime gerekiyor (şu an %d). "
                     "Kısa metinlerde hiçbir yöntem güvenilir sonuç veremez." % len(tokens),
        }

    lang = detect_lang(text)
    metrics = {
        "burstiness": m_burstiness(sentences),
        "sentence_starters": m_sentence_starters(sentences),
        "para_uniformity": m_paragraph_uniformity(text),
        "ngram_repeat": m_ngram_repeat(tokens),
        "lexical": m_lexical(tokens),
        "transitions": m_transitions(text, sentences, lang),
        "cliches": m_cliches(text, tokens, lang),
        "punctuation": m_punctuation(text, tokens),
        "informality": m_informality(text, tokens, lang),
    }

    rows, total_w, acc = [], 0.0, 0.0
    for key, (label, weight, why) in METRIC_META.items():
        m = metrics.get(key)
        if not m:
            rows.append({"key": key, "label": label, "why": why,
                         "score": None, "weight": weight, "detail": "Yetersiz veri — atlandı"})
            continue
        acc += m["score"] * weight
        total_w += weight
        rows.append({"key": key, "label": label, "why": why,
                     "score": round(m["score"]), "weight": weight,
                     "detail": m["detail"], "matches": m.get("matches", [])})

    score = acc / total_w if total_w else 50.0

    # Belge adli sinyalleri skoru hafifce kaydirir
    forensic_notes = []
    if forensics:
        forensic_notes = forensics.get("notes", [])
        score = max(0.0, min(100.0, score + forensics.get("score_delta", 0)))

    # Guven: metin uzunlugu + calisabilen metrik sayisi
    length_conf = ramp(len(tokens), 40, 700)
    metric_conf = total_w / sum(w for _, w, _ in METRIC_META.values()) * 100
    confidence = round(0.65 * length_conf + 0.35 * metric_conf)

    if score >= 78:
        verdict, tone = "Büyük olasılıkla AI üretimi", "ai"
    elif score >= 60:
        verdict, tone = "AI izleri belirgin", "likely-ai"
    elif score >= 42:
        verdict, tone = "Belirsiz — karma ya da düzenlenmiş olabilir", "mixed"
    elif score >= 25:
        verdict, tone = "Büyük olasılıkla insan yazımı", "likely-human"
    else:
        verdict, tone = "Neredeyse kesin insan yazımı", "human"

    lengths = [len(tokenize(s)) for s in sentences] or [0]
    return {
        "ok": True,
        "score": round(score),
        "verdict": verdict,
        "tone": tone,
        "confidence": confidence,
        "lang": "Türkçe" if lang == "tr" else "İngilizce",
        "metrics": rows,
        "sentences": sentence_heat(sentences, lang, statistics.mean(lengths)),
        "forensics": forensic_notes,
        "stats": {
            "words": len(tokens),
            "sentences": len(sentences),
            "chars": len(text),
            "avg_sentence": round(statistics.mean(lengths), 1),
            "reading_min": max(1, round(len(tokens) / 200)),
        },
    }
