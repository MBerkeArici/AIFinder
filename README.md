# AIFinder

Bir metnin yapay zekâ tarafından yazılıp yazılmadığını tahmin etmeye çalışan
bir araç. Türkçe ve İngilizce çalışıyor, PDF ve Word dosyalarını da okuyabiliyor.
Her şey kendi bilgisayarında çalışıyor, metin hiçbir yere gönderilmiyor.

Başta basit bir şey olacağını düşünmüştüm. Öyle olmadı.

## Önce şunu söyleyeyim

Bu araç kesin sonuç vermiyor, veremez de. Hiçbir araç veremiyor zaten.

Stanford'un 2023'te yaptığı bir çalışmada, yedi farklı ticari detektör test
edilmiş ve ana dili İngilizce olmayan öğrencilerin denemelerinin **%61'ini**
yanlışlıkla "yapay zekâ" olarak işaretlemişler. Yani düzgün İngilizce yazmaya
çalışan bir öğrenci, sırf düzgün yazdığı için suçlanabiliyor.

Bu yüzden aracı, hata yapacaksa "kaçırma" yönünde hata yapacak şekilde ayarladım.
Bir yapay zekâ metnini kaçırmak, bir insanı haksız yere suçlamaktan daha az kötü.

Not vermek, disiplin işlemi yapmak gibi şeyler için tek başına kullanmayın.

## Nasıl çalışıyor

Temel fikir şu: dil modelleri metni kelime kelime üretirken hep en olası
kelimeyi seçme eğiliminde. İnsan öyle yazmıyor — tuhaf kelime seçiyor, cümleyi
yarıda bırakıyor, alakasız detay veriyor.

```
"Sonuç olarak bu konu büyük önem ..."  → "taşımaktadır"   çok beklenen
"Kedim dün gece yine ..."              → "kustu"          hiç beklenmeyen
```

Bu farkı ölçmeye çalışıyoruz.

Belge tek parça değerlendirilmiyor. Yaklaşık 140 kelimelik, birbiriyle örtüşen
parçalara bölünüyor ve her parça ayrı puanlanıyor. Böylece yarısını kendin
yazıp yarısını yapay zekâya yazdırdığın bir metinde hangi kısmın ne olduğu
görülebiliyor. (Turnitin de benzer bir şey yapıyor.)

Her parça dört ayrı yerden geçiyor:

**1. Binoculars.** İki dil modeli kullanıyor ve aralarındaki "şaşkınlık farkına"
bakıyor. 2024'te ICML'de yayımlanan bir yöntem. Güzel tarafı hiç eğitim
gerektirmemesi — yani yarın yeni bir GPT çıksa bu yöntem yine çalışır.

**2. Eğitilmiş sınıflandırıcı.** `desklib/ai-text-detector-v1.01` modeli.
Milyonlarca metinle eğitilmiş, bilinen modellerde çok iyi.

**3. Gizlenmiş AI tespiti.** Bunu kendim eğittim, hikâyesi aşağıda.

**4. Stilometri.** Cümle uzunlukları, kalıp ifadeler, noktalama alışkanlıkları.
Tek başına zayıf ama kararın *neden* böyle olduğunu açıklayabilen tek katman bu.

Dördünün sonucu, ölçüm verisinden öğrenilen ağırlıklarla birleştiriliyor.
Ağırlıkları elle yazmadım; bütün kombinasyonları deneyip en iyisini seçen bir
kod var.

## Doğruluk

Bu rakamlar kendi ölçümümden geliyor, `eval/report.md` içinde detayı var.

Eşiği, insan metinlerinin en fazla %5'inin yanlış işaretleneceği noktaya
ayarladım.

| Dil | AUC | Yakalama |
|---|---|---|
| Türkçe | 0,911 | %48 |
| İngilizce | 0,987 | %95 |

İngilizce için ilk başta %100 çıkmıştı ama o rakam sahteydi — kullandığım model
RAID veri setiyle eğitilmiş, ben de test setimi RAID'den almışım. Model kendi
sınavını kendi hazırlamış gibi olmuş. Başka bir veri setiyle test edince %95
çıktı, gerçek olan bu.

Türkçe'deki %48 düşük görünüyor, gerçekten de düşük. Sebebi elimde sadece 74
Türkçe yapay zekâ örneği olması. Daha fazla örnek toplamak gerekiyor.

Metin bozularak tespitin atlatılmaya çalışıldığı durumlar:

| Yöntem | Yakalama |
|---|---|
| Homoglif (harflerin benzerleriyle değiştirilmesi) | %100 |
| Boşluk karakteri ekleme | %100 |
| Parafraz | %65 |
| Eşanlamlı değiştirme | %60 |

Homoglif ilk denemede %3 yakalıyordu. Latin harflerini görüntüsü aynı olan
Kiril harfleriyle değiştirince (`a` yerine Kiril `а` gibi) model metni tamamen
başka bir şey sanıyor. Analiz öncesi bir temizleme adımı ekleyince %100'e çıktı.

## Kurulum

```bash
git clone https://github.com/MBerkeArici/AIFinder.git
cd AIFinder
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

İlk çalıştırmada modeller iniyor, yaklaşık 5 GB. Bir kere iniyor.

```bash
.venv/bin/python app.py
```

Sonra http://127.0.0.1:9317 adresini aç. Mac'te `AIFinder Başlat.command`
dosyasına çift tıklamak da olur.

16 GB RAM öneriyorum. Bende 16 GB var ve sınırda gidiyor — modeller yaklaşık
7 GB yer kaplıyor. Bir analiz, modeller yüklüyken 7-15 saniye sürüyor.

## Gizlenmiş AI meselesi

Projenin en öğretici kısmı burası.

Araç bir süre iyi çalışıyordu. Sonra bir metin denedim, araç "insan yazımı"
dedi, halbuki yapay zekâ yazmıştı. Klasik AI metni değildi — kısa cümleler,
samimi ton, gündelik detaylar. Yani birinin "insan gibi yaz" diyerek yazdırdığı
türden.

Önce eşiği düşürmeyi denedim. Olmadı. Eşiği 0,78'den 0,30'a kadar indirdim,
metin hâlâ yakalanmıyordu, sadece masum metinler işaretlenmeye başladı. Sonra
fark ettim ki sorun eşikte değil — o metinde ayırt edilecek bir sinyal yoktu.
Üstelik iki katman (Binoculars ve stilometri) bu tür metinlerde şansın *altında*
performans gösteriyordu. Yani bu metinleri insan metninden daha "insan" sayıyorlardı.

Çözüm modelde değil veride çıktı. İki şey yaptım:

Birincisi, buna benzer 58 metin yazdım. Ama insan tarafında da eşleşen veri
lazımdı — çünkü benim örneklerim samimi/kişisel üsluptayken insan verim sadece
haber ve ansiklopedi metniydi. Öyle eğitsem model "yapay zekâ"yı değil "kişisel
üslup"u öğrenirdi. Reddit'ten 160 tane birinci şahıs anlatı topladım.

İkincisi, 58 örnek az olduğu için üç açık veri setinden 3.600 metin çekip
mevcut modelle taradım ve **modelin yanıldığı** örnekleri ayıkladım. 64 tane
kaçırılan yapay zekâ metni, 124 tane yanlışlıkla işaretlenen insan metni çıktı.
Bunlar tam olarak öğrenilmesi gereken örneklerdi.

Sonra tam fine-tune yerine daha güvenli bir yol seçtim: mevcut modelin
gömülerini (embedding) çıkarıp üstüne küçük bir sınıflandırıcı eğittim. 58-200
örnekle 430 milyon parametreli bir modeli fine-tune etsem büyük ihtimalle
ezberlerdi.

Sonuç: eğitimde hiç kullanılmamış 296 metinlik test setinde AUC 0,997. Ve asıl
önemlisi, başta kaçan o metin artık yakalanıyor.

Bu katman şu an sadece İngilizce çalışıyor. Türkçesi için aynı veriyi toplamak
gerekiyor.

## Yaptığım hatalar

Bunları yazıyorum çünkü hepsi "kod çalışıyor ama sonuç yanlış" türündendi ve
fark etmesi zor oldu.

**Eşik sıfıra yuvarlanıyordu.** Kalibrasyon mükemmel ayrım bulduğunda eşik
`0.0` olarak kaydediliyordu. `p >= 0` her zaman doğru olduğu için araç her
metni yapay zekâ işaretliyordu. Kaydetme hassasiyeti meselesiymiş.

**Isotonic kalibrasyon kararı eziyordu.** Ölçüm setinde insan metinleri 0,004,
yapay zekâ metinleri 0,95 alıyordu — arada hiç örnek yoktu. Isotonic bu veriye
uydurulunca bir merdiven fonksiyonuna dönüşüp 0,93'ün altındaki her şeyi sıfıra
eziyordu. Gerçek metinler tam o boşluğa düşüyor. Test metnim 0,69 almıştı, yani
sınıflandırıcı doğru çalışıyordu, sonucu kalibrasyon bozuyordu.

**Pencere boyutu kalibrasyonla uyumsuzdu.** 140 kelimelik metinlerle kalibre
edip 300 kelimelik pencereler besliyordum. Yarısı yapay zekâ olan bir belge bu
yüzden %0 veriyordu.

**Çoklu karşılaştırma sorunu.** Bunu en son fark ettim. Ölçümde yanlış pozitif
%0,8 görünüyordu ama gerçek belgelerde %10 çıkıyordu. Sebep: ölçümü tek parça
metinlerle yapıyordum, gerçek belgeler ise 10-15 parçaya bölünüyor. Her parça
ayrı bir yanlış pozitif şansı demek. Parça başına %5 risk, 10 parçada
1-(0,95)^10 = %40 ediyor. Eşiği parça sayısına göre sıkılaştırarak düzelttim.

**Güven hesabı yanlıştı.** Kullanıcı sordu, bakınca gördüm. Olasılığı 0,00 olan
bir metin — yani mümkün olan en net insan kararı — %16 güven gösteriyordu.
Formül her iki yönü de aynı paydaya bölüyordu, oysa insan tarafında
ulaşılabilecek en büyük mesafe eşiğin kendisi. Asimetrik hale getirince aynı
metin %81 oldu.

**Üç model aynı anda bellekteydi.** 16 GB'lık makinede sistem takasa düşüp
kullanılamaz hale geliyordu. Modelleri sırayla yükleyip boşaltacak şekilde
değiştirdim, tepe kullanım 9 GB'dan 6,5 GB'a indi.

## Bilmesi gerekenler

- Gizlenmiş metin hâlâ zor. İngilizce için bir çözüm var ama Türkçe için yok.
- Türkçe rakamları 74 örneğe dayanıyor, bu az. Güvenilir olması için 200+ lazım.
- Parafraz araçlarından geçmiş metinlerde yakalama %65'e düşüyor.
- 85 kelimeden kısa metinlerde karar vermiyor. Hiçbir yöntem o uzunlukta çalışmıyor.
- Resmî, akademik üslupla yazan insanlar yanlış işaretlenme riski taşıyor.
- Araç hiçbir zaman "insan yazımı" demiyor, "yapay zekâ izi bulunamadı" diyor.
  İz bulamamak iz olmadığı anlamına gelmiyor.

## Dosyalar

```
app.py              sunucu
analyze.py          ana akış
extract.py          PDF/Word okuma
detector.py         stilometri
engine/
  binoculars.py     1. katman
  classifier.py     2. katman
  hidden.py         3. katman
  normalize.py      homoglif temizliği
  segment.py        parçalara bölme
  ensemble.py       birleştirme
  aggregate.py      yüzde hesabı
eval/               ölçüm ve eğitim betikleri
static/index.html   arayüz
```

Ölçüm verisi depoda yok — üçüncü taraf kaynaklardan geliyor ve dağıtmak doğru
olmaz. `eval/build_*.py` betikleriyle yeniden indirilebiliyor.

## Kaynaklar

- Binoculars — [arXiv:2401.12070](https://arxiv.org/abs/2401.12070), ICML 2024
- RAID veri seti — [arXiv:2405.07940](https://arxiv.org/abs/2405.07940), ACL 2024
- Liang ve ark., "GPT detectors are biased against non-native English writers",
  Patterns, 2023
- [desklib/ai-text-detector-v1.01](https://huggingface.co/desklib/ai-text-detector-v1.01)
- [Qwen2.5-1.5B](https://huggingface.co/Qwen/Qwen2.5-1.5B)

MIT lisansı.
