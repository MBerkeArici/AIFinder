# Uzunluk Bandı Ölçümü

Aynı metinler farklı uzunluklara kırpılıp her bantta ayrı ölçüldü.
Böylece uzunluğun tek başına etkisi görünür.

| Kelime | AI örnek | İnsan örnek | ROC-AUC | TPR @ FPR %1 |
|---:|---:|---:|---:|---:|
| 85 | 90 | 90 | 0.993 | 88.9% |
| 110 | 69 | 90 | 0.992 | 91.3% |
| 140 | 43 | 84 | 0.999 | 93.0% |
| 200 | 18 | 64 | 0.995 | 72.2% |

**Okuma notu.** Bu tablo üretimdeki kalibre motorun çıktısıyla
hesaplandı (engine/calibration.json), yani kullanıcının gördüğü
karar mekanizmasının ta kendisi. Kalibrasyon 140 kelime bandında
yapıldığı için diğer bantlarda eşik ideal olmayabilir; AUC sütunu
eşikten bağımsız olduğu için ayırt etme gücünü daha iyi gösterir.

AUC en düşük 0.992, en yüksek 0.999.
