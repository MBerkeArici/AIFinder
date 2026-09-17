# Ölçüm Raporu

Bu dosya otomatik üretilir (`eval/run_eval.py`). Arayüzde gösterilen
doğruluk rakamlarının tek kaynağı budur.


## Türkçe

Örnek: **239 insan**, **43 AI** (her metin ilk 140 kelimeye kırpıldı).


### Tek tek sinyaller

| Sinyal | ROC-AUC | TPR @ FPR %1 |
|---|---:|---:|
| binoculars | 0.812 | 0.0% |
| siniflandirici | 0.823 | 18.6% |
| stilometri | 0.861 | 4.7% |
| gizlenmis | 0.904 | 48.8% |
| **birleşik (ensemble)** | **0.971** | **25.6%** |

Öğrenilen ağırlıklar: `{'binoculars': 0.83, 'siniflandirici': 0.277, 'stilometri': 1.801, 'gizlenmis': 1.982}`  ·  eşik: `0.9791`


### İnsan metinlerinde yanlış pozitif (kaynak bazında)

| Kaynak | Yanlış pozitif | n |
|---|---:|---:|
| ttc4900 | 0.0% | 113 |
| urun-yorumlari | 0.0% | 39 |
| wikipedia-tr-2023 | 1.1% | 87 |

## İngilizce

Örnek: **249 insan**, **139 AI** (her metin ilk 140 kelimeye kırpıldı).


### Tek tek sinyaller

| Sinyal | ROC-AUC | TPR @ FPR %1 |
|---|---:|---:|
| binoculars | 0.566 | 0.0% |
| siniflandirici | 0.799 | 58.3% |
| stilometri | 0.618 | 7.2% |
| gizlenmis | 0.994 | 93.5% |
| **birleşik (ensemble)** | **0.995** | **80.6%** |

Öğrenilen ağırlıklar: `{'binoculars': -0.823, 'siniflandirici': 1.376, 'stilometri': -0.287, 'gizlenmis': 4.015}`  ·  eşik: `0.9564`


### Saldırı altında (parafraz / eşanlamlı / homoglif)

Aynı eşikte yakalama oranı: **83.3%** (78 örnek)


| Saldırı türü | Yakalama |
|---|---:|
| homoglyph | 100.0% (19) |
| paraphrase | 75.0% (20) |
| synonym | 60.0% (20) |
| whitespace | 100.0% (19) |

### İnsan metinlerinde yanlış pozitif (kaynak bazında)

| Kaynak | Yanlış pozitif | n |
|---|---:|---:|
| raid | 0.8% | 129 |
| reddit-informal | 0.0% | 120 |
