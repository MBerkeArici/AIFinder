# Arayüz açıklama metinleri

Kullanıcı arayüzdeki bölümlerin ne anlama geldiğini anlamadığını bildirdi.
Bu dosya her bölüm için hazır Türkçe açıklamaları içerir. Arayüz bunları
doğrudan kullanabilir; teknik terimler kullanıcıya açıklanmadan
gösterilmemelidir.

---

## Ana sonuç: "%N yapay zekâ"

**Başlık altı açıklama:**
> Belge yaklaşık 140 kelimelik, birbiriyle örtüşen bölümlere ayrıldı. Her
> bölüm ayrı ayrı değerlendirildi. Bu yüzde, yapay zekâ üretimi olduğu
> değerlendirilen bölümlerin metindeki kelime oranıdır.

**Neden bölüm bölüm:** Bir belgenin tamamı aynı kaynaktan olmak zorunda
değil. Yarısı insan yazıp yarısını yapay zekâya tamamlatan bir metinde tek
bir ortalama gerçeği gizler; bölüm bölüm bakınca hangi kısmın nereden
geldiği görünür.

---

## "Güven: %N"

> Kararın ne kadar sağlam olduğunu gösterir. İki şeye bakar: bölüm
> puanlarının karar eşiğinden ne kadar uzak olduğu ve metnin uzunluğu.
> Kısa metinlerde ve eşiğe yakın puanlarda güven düşer.

Güven, **doğruluk değildir**. Yüksek güven "kesinlikle doğru" demek değil,
"bu metin için karar sınırda değil" demektir.

---

## "İnceleme pencereleri"

> Belgenin ayrı ayrı değerlendirilen bölümleri. Her satır bir bölümü ve o
> bölüm için hesaplanan olasılığı gösterir. "Eşik altında" etiketi, o
> bölümün yapay zekâ sayılmadığı anlamına gelir.

**Buradaki yüzdeler gerçek olasılıktır** — ölçülmüş verilerle kalibre
edilmiştir ve karar bu sayılara göre verilir.

---

## "Cümle görünümü"

> Bu bölüm bir olasılık göstermez. Yalnızca hangi cümlelerin yapay zekâ
> metinlerinde sık görülen kalıpları taşıdığını işaretler — "sonuç olarak",
> "önemli bir rol oynamaktadır" gibi ifadeler, tekdüze cümle uzunluğu,
> alışılmadık noktalama.

**Önemli:** Bir cümlenin "belirgin kalıp" işareti alması o cümlenin yapay
zekâ olduğu anlamına gelmez. Kalıp ifadeler insan yazısında da bulunur.
Bu bölüm kararı değil, kararın **gerekçesini** gösterir.

Alan artık yüzde değil, dört seviyeden biridir:
`işaret yok` · `hafif iz` · `bir miktar kalıp` · `belirgin kalıp`

---

## "Üç katman ne dedi" / sinyal dökümü

| Katman | Kullanıcıya açıklama |
|---|---|
| **Binoculars** | İki farklı dil modeline metni okutup "bu kelimeyi ne kadar beklerdiniz" diye sorar. Yapay zekâ genellikle tahmin edilebilir kelimeler seçer; insan daha şaşırtıcı yazar. Eğitim gerektirmediği için daha önce görülmemiş modellere de uyum sağlar. |
| **Eğitilmiş sınıflandırıcı** | Milyonlarca yapay zekâ ve insan metniyle eğitilmiş bir model. Bilinen üreticilerde en güçlü katman. |
| **Gizlenmiş AI tespiti** | Yapay zekâya "insan gibi yaz" denildiğinde üretilen metinleri yakalamak için ayrıca eğitildi. Şu an yalnızca İngilizce çalışır. |
| **Stilometri** | Cümle ritmi, kelime çeşitliliği, kalıp ifadeler, noktalama alışkanlıkları. Tek başına zayıftır ama kararı **açıklayan** tek katmandır. |

---

## "Belge adli sinyalleri"

> Dosyanın içindeki üstveriden okunur, metnin kendisinden bağımsızdır.
> Örneğin bir Word belgesinin toplam düzenleme süresi çok kısaysa, metin
> başka bir yerden yapıştırılmış olabilir.

Ayrıca **tespit atlatma izleri** burada görünür: görünmez karakterler veya
Latin harflerinin yerine konmuş benzer görünümlü Kiril/Yunan harfleri.
Bunlar normal yazıda bulunmaz.

---

## Düşük sonuç uyarısı (`not_proof`)

> Yapay zekâ izi bulunamadı — bu, metnin insan tarafından yazıldığını
> **göstermez**. Ölçümümüzde, yapay zekâya "insan gibi yaz" denilerek
> üretilen metinlerin hiçbiri yakalanamadı. Bu tür metinler bu araçla
> ayırt edilemiyor.

Araç hiçbir koşulda "insan yazımı" hükmü vermez. En düşük sonuçta bile
ifade "yapay zekâ izi bulunamadı"dır. Arayüz bu ayrımı olumlu bir onaya
(“temiz”, “insan”, yeşil tik) dönüştürmemelidir.

---

## "Bu rakam ne kadar güvenilir"

> Bu değerler pazarlama iddiası değil, kendi ölçümümüzden gelir
> (`eval/report.md`). Eşik, insan metinlerinin en fazla %5'inin
> aşabileceği noktaya ayarlanmıştır — yani araç, kaçırma pahasına yanlış
> suçlamadan kaçınacak şekilde ayarlıdır.

| Terim | Kullanıcıya açıklama |
|---|---|
| ROC-AUC | Aracın iki metni doğru sıralama yeteneği. 0,5 = yazı tura, 1,0 = kusursuz. |
| Yakalama oranı | Yapay zekâ metinlerinin yüzde kaçının yakalandığı. |
| Yanlış pozitif | İnsan yazısının yanlışlıkla yapay zekâ sayılma oranı. |
| Saldırı dayanıklılığı | Metin kasıtlı olarak değiştirildiğinde (kelime değiştirme, parafraz) tespitin ne kadar dayandığı. |
