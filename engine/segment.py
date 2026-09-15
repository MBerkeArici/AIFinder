# -*- coding: utf-8 -*-
"""Metni ortusen pencerelere boler (Turnitin'in segment yaklasimi).

Belge yuzdesi, tek bir global skordan degil, pencere pencere karardan
uretilir. Bu sayede karma belgelerde (yarisi insan, yarisi AI) hangi
bolumun AI oldugu da soylenebilir.
"""
import re

WORD_RE = re.compile(r"\S+")


def word_spans(text):
    """Metindeki her kelimenin (baslangic, bitis) karakter araligi."""
    return [(m.start(), m.end()) for m in WORD_RE.finditer(text)]


def windows(text, size=300, stride=150, min_tail=120):
    """Ortusen pencereler uretir.

    size   : pencere basina kelime
    stride : pencereler arasi kayma (size/2 -> %50 ortusme)
    min_tail: son pencere bundan kisaysa bir oncekine eritilir

    Doner: [{'text', 'w_start', 'w_end', 'c_start', 'c_end'}, ...]
    """
    spans = word_spans(text)
    n = len(spans)
    if n == 0:
        return []
    if n <= size:
        return [{"text": text[spans[0][0]:spans[-1][1]], "w_start": 0, "w_end": n,
                 "c_start": spans[0][0], "c_end": spans[-1][1]}]

    out = []
    start = 0
    while start < n:
        end = min(start + size, n)
        # kuyruk cok kisaysa bu pencereyi sonuna kadar uzat ve bitir
        if n - end < min_tail:
            end = n
        out.append({
            "text": text[spans[start][0]:spans[end - 1][1]],
            "w_start": start, "w_end": end,
            "c_start": spans[start][0], "c_end": spans[end - 1][1],
        })
        if end >= n:
            break
        start += stride
    return out
