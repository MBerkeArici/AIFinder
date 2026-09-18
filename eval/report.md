# Ölçüm Raporu

Bu dosya otomatik üretilir (`eval/run_eval.py`). Arayüzde gösterilen
doğruluk rakamlarının tek kaynağı budur.

## Bu rakamları okurken

**Türkçe sonuçlar iyimser okunmalıdır.** Türkçe AI örneklerinin tamamı
tek bir model ailesinden üretildi. ChatGPT ve Gemini'nin Türkçe üslubu
ölçüm setinde hiç temsil edilmiyor; gerçek kullanımda en sık karşılaşılan
iki kaynak bunlar.

**Parafraz saldırısı sonucu özellikle yanıltıcıdır.** Parafraz örnekleri
(`eval/ai_tr_paraphrase.py`) kaynak metinlerle aynı model ailesinden
yeniden yazıldı. Gerçek "humanizer" araçları başka modeller kullanır ve
başka bir istatistiksel imza bırakır — bu ölçüm o durumu kapsamıyor.
Türkçe saldırı rakamı, İngilizce tarafın bağımsız kaynaklı (RAID)
rakamıyla doğrudan karşılaştırılamaz.

**Eşik seçimi doğruluk için değil düşük yanlış pozitif için yapılır.**
İnsan metinlerinin en fazla %1'inin aşabildiği nokta seçilir; bir AI
metnini kaçırmak ile bir insanı haksız yere işaretlemek eşit maliyetli
hatalar değildir.


## Türkçe

Örnek: **239 insan**, **43 AI** (her metin ilk 140 kelimeye kırpıldı).


### Tek tek sinyaller

| Sinyal | ROC-AUC | TPR @ FPR %1 |
|---|---:|---:|
| binoculars | 0.812 | 0.0% |
| siniflandirici | 0.823 | 18.6% |
| stilometri | 0.861 | 4.7% |
| gizlenmis | 0.999 | 95.3% |
| **birleşik (ensemble)** | **0.999** | **97.7%** |

Öğrenilen ağırlıklar: `{'binoculars': 0.773, 'siniflandirici': 0.363, 'stilometri': 1.148, 'gizlenmis': 2.92}`  ·  eşik: `0.6967`


### Saldırı altında (parafraz / eşanlamlı / homoglif)

Aynı eşikte yakalama oranı: **97.4%** (196 örnek)


| Saldırı türü | Yakalama |
|---|---:|
| bosluk | 97.7% (43) |
| esanlamli | 97.4% (39) |
| homoglif | 97.7% (43) |
| karma | 97.7% (43) |
| noktalama | 95.2% (21) |
| parafraz | 100.0% (7) |

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
| gizlenmis | 0.998 | 95.0% |
| **birleşik (ensemble)** | **1.000** | **98.6%** |

Öğrenilen ağırlıklar: `{'binoculars': -0.708, 'siniflandirici': 1.698, 'stilometri': 0.342, 'gizlenmis': 3.992}`  ·  eşik: `0.6436`


### Saldırı altında (parafraz / eşanlamlı / homoglif)

Aynı eşikte yakalama oranı: **80.8%** (78 örnek)


| Saldırı türü | Yakalama |
|---|---:|
| homoglyph | 100.0% (19) |
| paraphrase | 60.0% (20) |
| synonym | 65.0% (20) |
| whitespace | 100.0% (19) |

### İnsan metinlerinde yanlış pozitif (kaynak bazında)

| Kaynak | Yanlış pozitif | n |
|---|---:|---:|
| raid | 0.8% | 129 |
| reddit-informal | 0.0% | 120 |
