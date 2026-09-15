# Ölçüm Raporu

Bu dosya otomatik üretilir (`eval/run_eval.py`). Arayüzde gösterilen
doğruluk rakamlarının tek kaynağı budur.


## Türkçe

Örnek: **239 insan**, **27 AI** (her metin ilk 140 kelimeye kırpıldı).


### Tek tek sinyaller

| Sinyal | ROC-AUC | TPR @ FPR %1 |
|---|---:|---:|
| binoculars | 0.824 | 0.0% |
| siniflandirici | 0.810 | 18.5% |
| stilometri | 0.861 | 7.4% |
| gizlenmis | 0.500 | 0.0% |
| **birleşik (ensemble)** | **0.888** | **11.1%** |

Öğrenilen ağırlıklar: `{'binoculars': 1.178, 'siniflandirici': 0.139, 'stilometri': 1.411, 'gizlenmis': 0.0}`  ·  eşik: `0.9739`


### İnsan metinlerinde yanlış pozitif (kaynak bazında)

| Kaynak | Yanlış pozitif | n |
|---|---:|---:|
| ttc4900 | 0.0% | 113 |
| urun-yorumlari | 0.0% | 39 |
| wikipedia-tr-2023 | 0.0% | 87 |

## İngilizce

Örnek: **249 insan**, **139 AI** (her metin ilk 140 kelimeye kırpıldı).


### Tek tek sinyaller

| Sinyal | ROC-AUC | TPR @ FPR %1 |
|---|---:|---:|
| binoculars | 0.566 | 0.0% |
| siniflandirici | 0.799 | 58.3% |
| stilometri | 0.618 | 7.2% |
| gizlenmis | 1.000 | 100.0% |
| **birleşik (ensemble)** | **0.998** | **100.0%** |

Öğrenilen ağırlıklar: `{'binoculars': -0.06, 'siniflandirici': 0.343, 'stilometri': 0.114, 'gizlenmis': 4.139}`  ·  eşik: `0.5555`


### Saldırı altında (parafraz / eşanlamlı / homoglif)

Aynı eşikte yakalama oranı: **75.6%** (78 örnek)


| Saldırı türü | Yakalama |
|---|---:|
| homoglyph | 100.0% (19) |
| paraphrase | 65.0% (20) |
| synonym | 40.0% (20) |
| whitespace | 100.0% (19) |

### İnsan metinlerinde yanlış pozitif (kaynak bazında)

| Kaynak | Yanlış pozitif | n |
|---|---:|---:|
| raid | 0.8% | 129 |
| reddit-informal | 0.0% | 120 |
