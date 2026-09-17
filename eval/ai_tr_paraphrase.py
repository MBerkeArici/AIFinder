# -*- coding: utf-8 -*-
"""Parafraz saldirisi — elle yazilmis "humanize edilmis" AI metinleri.

NEDEN ELLE: eval/attack_tr.py'nin mekanik saldirilari (esanlamli, homoglif,
bosluk, noktalama) metnin KODLAMASINI degistiriyor, YAZIMINI degil. Olcumde
%97 yakalama cikti ama bu rakam aracin gucunu degil saldirinin zayifligini
gosteriyor: Ingilizce tarafta ayni aile %60'a kadar dusuruyordu.

Gercek "humanizer" araclari metni bastan yeniden yaziyor: kalip ifadeleri
atiyor, cumleleri boluyor ve birlestiriyor, konusma diline yaklastiriyor,
kucuk kusurlar birakiyor. Bu mekanik olarak taklit edilemez.

Bu dosyadaki metinler kaynak kumedeki (data/ai_tr.jsonl) metinlerle AYNI
ICERIGI tasiyor ama tamamen yeniden yazildi — yani gercek bir parafraz
saldirisinin yapacagi sey. OLCUM tarafina gider; egitimde kullanilmaz.
"""

SAMPLES = [
("akademik", """Kadın erkek eşitliği meselesi kalkınma hedeflerinin tam ortasında duruyor. Basitçe söylemek gerekirse: cinsiyetin, kimin neye erişebileceğini belirlememesi gerekiyor. Haklar, fırsatlar, kaynaklar. Bunun yalnızca bireyler için değil toplumun tümü için önemli olduğunu gösteren epey veri var.

Eğitim tarafında somut ilerleme görünüyor. Kız çocuklarının okula gitme oranı son yıllarda ciddi biçimde yükseldi. Ama ilkokulda kapanan makas, yükseköğretimde yeniden açılıyor. Özellikle mühendislik gibi alanlarda kadın oranı hâlâ düşük. Nedeni yetenek değil; mesleklerin zihinlerde nasıl kodlandığı.

İş hayatında durum daha karışık. Aynı işi yapan kadın ve erkek arasında ücret farkı çoğu ülkede duruyor. Bir kısmı sektör tercihiyle açıklanabiliyor, bir kısmı açıklanamıyor. Üst düzey yönetimde kadın sayısı ise hâlâ istisna sayılacak kadar az.

Ev içi iş yükü konusuna girmeden bu tabloyu anlamak zor. Bakım emeği ücretsiz ve büyük ölçüde kadınların üzerinde. Bu yük, kariyer ilerlemesini doğrudan kesiyor.

Politika tarafında kota gibi araçlar tartışılıyor. İşe yarıyorlar ama tek başına yetmiyorlar. Zihniyet değişmeden sayılar değişse ne olur, orası ayrı bir soru.

Ölçme tarafında da sorun var. Eşitlik endeksleri ülkeleri sıralıyor ama neyi ölçtükleri birbirinden farklı. Aynı ülke bir listede yükselirken diğerinde düşebiliyor. Bu yüzden tek bir sıralamaya bakıp sonuç çıkarmak yanıltıcı oluyor."""),

("kisisel", """Uzun süredir aklımda olan bir şeyi sonunda yaptım: düzenli yürüyüşe başladım. Büyük bir motivasyonum yoktu açıkçası. Sadece bütün gün masada oturmanın beni ne kadar yorduğunu fark etmiştim. Üç ay oldu, ne gördüğümü yazayım.

İlk günler sandığımdan zordu. Kırk dakika kulağa az geliyor ama alışkanlık olmayınca her gün bir savaş. Hava soğuksa kapıdan çıkmak ayrı bir iş.

İkinci haftada bir şey değişti. Ayakkabı meselesi. Eski koşu ayakkabımla yürüyordum, tabanı ölmüş. Yenisini alınca ayak ağrım geçti. Bu kadar basit bir şeyin bu kadar fark yaratması tuhaf.

Rotayı değiştirmek de işe yaradı. İlk rotam ana cadde boyuncaydı, egzoz kokusu ve gürültü. Parktan geçen bir yol buldum, on dakika uzun ama tamamen başka bir deneyim.

Ölçülebilir sonuç şu: uykum düzeldi. Bunu beklemiyordum. Kilo vermedim, onu da söyleyeyim.

Devam eder miyim kışın? Bilmiyorum. Karanlıkta yürümek başka bir iş. Belki saat değiştiririm.

Bir de şunu fark ettim: telefonu evde bırakınca yürüyüş başka bir şeye dönüşüyor. İlk denediğimde huzursuz oldum, şimdi kasten bırakıyorum. Kırk dakika hiçbir şey kontrol etmemek tuhaf biçimde iyi geliyor."""),

("akademik", """Uzaktan eğitim üniversitelerde hızla yayıldı, teknoloji izin verdikçe. Mekân ve zaman kısıtını kaldırması en büyük avantajı. Kırsalda yaşayan ya da çalıştığı için kampüse gelemeyen biri artık derse girebiliyor. Yaşam boyu öğrenme dediğimiz şeye de kapı açıyor.

Ama sınırları var ve bunları konuşmadan olmaz. Öğrenciyle öğretim üyesi arasındaki bağ zayıflıyor. Sınıfta kendiliğinden olan soru-cevap, ekranda planlanması gereken bir şeye dönüşüyor.

Sınav tarafı ayrı bir baş ağrısı. Uzaktan sınavın güvenliği en çok tartışılan konu. Gözetim yazılımları geliştirildi ama bu sefer mahremiyet tartışması çıktı. Öğrencinin odasını kameraya açması makul mü, orası belirsiz.

Dijital eşitsizlik de var. İnternet bağlantısı zayıf olan ya da düzgün cihazı olmayan öğrenci bu modelden eşit yararlanamıyor. Fırsat eşitliği sağlayacak diye başlanan şey tersine işleyebiliyor.

Karma model bana en makul çözüm gibi görünüyor. Teori çevrim içi, uygulama yüz yüze. Ne birini ne diğerini tümüyle bırakmak gerekiyor.

Maliyet tarafı da konuşulmuyor yeterince. Kurum açısından ucuz görünüyor ama içerik üretimi ve teknik destek ciddi kaynak istiyor. Ucuza yapılan uzaktan eğitim, kaydedilmiş video izletmekten öteye geçmiyor ve kimse ondan memnun kalmıyor."""),

("blog", """Kışın bitki bakımı yazınkinden farklı, çoğu insan bunu bilmiyor. Yazın işe yarayan rutini kışın sürdürürsen bitkiye zarar veriyorsun. Neleri değiştirmek gerektiğini yazayım.

En sık yapılan hata sulama. Kışın bitki yavaşlıyor, o kadar suya ihtiyacı kalmıyor. Yaz düzenini sürdürürsen kökler çürüyor. Toprağın üstü kuruduktan sonra birkaç gün daha bekle, genelde doğru olan bu.

Işıkta durum tersine dönüyor. Günler kısalınca bitki daha az ışık alıyor, pencereye yaklaştırmak gerekebiliyor. Ama camın dibinde soğuk hava akımı varsa o da ayrı bir sorun. Dengeyi bulmak lazım.

Kalorifer havayı kurutuyor, bu da yaprak kenarlarını kahverengileştiriyor. Yanına bir kap su koymak ya da çakıllı tabak kullanmak işe yarıyor.

Gübreye kışın ara ver. Bitki büyümediği için besin istemiyor, fazlası toprakta birikip kökü yakıyor.

Saksı değiştirmeyi de bahara bırak. Kışın yapılan repotlama bitkinin toparlanmasını zorlaştırıyor.

Bir de sabır. Kışın yeni yaprak çıkmaz, bu normal. Müdahale etme.

Son olarak yaprakları silmeyi unutma. Kışın toz birikiyor ve zaten az olan ışığı daha da engelliyor. Nemli bir bezle ayda bir silmek yetiyor, beş dakikalık iş ama gözle görülür fark yaratıyor."""),

("akademik", """Mikroplastik kirliliği çevre araştırmalarının en çok konuşulan başlıklarından biri oldu. Beş milimetreden küçük plastik parçacıklardan söz ediyoruz. Bir kısmı zaten o boyutta üretiliyor, bir kısmı büyük atıkların parçalanmasıyla oluşuyor.

Denizler en çok etkilenen yer. Okyanus yüzeyinden dip çamuruna kadar her yerde bu parçacıklara rastlanıyor. Deniz canlıları onları yiyecek sanıp yutuyor, sindirim sistemleri tıkanıyor.

Asıl endişe verici kısım besin zinciri. Küçük organizmaların aldığı parçacıklar yukarı doğru birikiyor. İnsanın tükettiği deniz ürünlerinde mikroplastik bulunması bu yüzden soru işareti yaratıyor.

Karada da benzer bir durum var, daha az konuşuluyor. Tarımda kullanılan arıtma çamurları ve plastik örtüler toprağa parçacık taşıyor. Toprak canlıları üzerindeki etkisi henüz net değil.

Çözüm tarafında en çok kaynakta önleme konuşuluyor. Tek kullanımlık plastiği kısmak, atık toplama sistemini düzeltmek, arıtmada filtre kullanmak.

Sonuç olarak bu tek bir disiplinin çözebileceği bir mesele değil. Uzun vadeli izleme gerekiyor ve o izleme daha yeni başlıyor.

Bir de ölçüm standardı sorunu var. Farklı çalışmalar farklı yöntemlerle örnekliyor, sonuçlar doğrudan karşılaştırılamıyor. Bu da politika yapıcının hangi rakama dayanacağını bilmemesine yol açıyor. Ortak protokol çalışmaları yeni yeni ilerliyor."""),

("haber", """Şehirdeki toplu taşıma ağı genişletilecek, çalışmalar bu yıl başlıyor. Proje özellikle yeni yerleşim bölgelerini hedefliyor.

Yetkililer mevcut hatların nüfus artışına yetişemediğini söylüyor. Yoğun saatlerdeki sıkışıklığı azaltmak için sefer sayısı da artırılacak.

Çevresel etki değerlendirmesi tamamlanmış, olumsuz bir sonuç çıkmamış. Güzergâh belirlenirken yeşil alanların korunmasına dikkat edildiği belirtiliyor.

Paranın nereden geleceği henüz netleşmemiş. Dış kaynaklı finansman seçeneği masada.

Bölgede yaşayanlar işin bir an önce bitmesini istiyor. Yetkililer takvime uyulacağını söylüyor ama bu tür projelerde gecikme alışıldık bir şey.

Tamamlandığında günde yüz binlerce kişiye hizmet vermesi bekleniyor. Aktarma noktalarının düzenlenmesi ve bilet sisteminin birleştirilmesi de ayrı bir çalışma olarak yürüyor.

Esnaf tarafında tedirginlik var. İnşaat süresince kaldırımların kapanması işleri etkileyecek. Yetkililer geçiş dönemi için bazı önlemler değerlendirildiğini söylüyor ama ayrıntı verilmedi. Benzer projelerde bu konu genelde sonradan gündeme geliyor."""),

("kurumsal", """Enerji verimliliği konusunda yaptıklarımızı paylaşmak istiyoruz.

Tesislerde yaptığımız iyileştirmeler sonucunda birim üretim başına harcadığımız enerji düştü. En çok fark yaratan iki şey aydınlatmanın yenilenmesi ve ısı geri kazanımı oldu.

Yenilenebilir kaynakların payını yavaş yavaş artırıyoruz. Çatılara güneş paneli kurduk, ek yatırım planlıyoruz.

Ölçüm tarafını da güçlendirdik. Artık tüketimi tek tek noktalardan izliyoruz, sapma olduğunda erken görüyoruz. Eskiden aylık faturaya bakıp tahmin yürütüyorduk.

Çalışanlara yönelik farkındalık çalışmaları yaptık. Katılım beklediğimiz düzeydeydi.

Tedarikçilerle de ortak çalışıyoruz. Lojistikte rota optimizasyonuna geçtik, taşımadan kaynaklanan salım azaldı.

Hedeflerimizi yılda bir gözden geçiriyoruz. Tutmadığımız yerlerde düzeltici plan devreye giriyor. Sonuçları sürdürülebilirlik raporumuzda ayrıntılı paylaşıyoruz.

Bir de şeffaflık meselesi var. Bu tür raporlarda rakamlar seçilerek sunulabiliyor, biz mümkün olduğunca ham veriyi paylaşmaya çalışıyoruz. Doğrulamayı bağımsız kuruluşlar yapıyor, yöntem notlarını da rapora ekliyoruz."""),

("blog", """Bütçe tutmak sıkıcı geliyor olabilir ama parayla ilgili huzurun temeli bu. Ne kazandığın değil, nereye gittiğini bilip bilmediğin önemli. Karmaşık sistemlere gerek yok, basit bir yöntem anlatayım.

İlk adım: bir ay boyunca hiçbir şeyi değiştirme, sadece kaydet. Kendini kısmaya çalışma, amaç veri toplamak. Telefonda basit bir not uygulaması yeter. Harcamayı o anda yaz, akşam hatırlamaya çalışmak işe yaramıyor.

Ay sonunda kategorilere ayır. Kira, market, ulaşım, dışarıda yemek, eğlence, abonelikler. Çoğu kişi burada şaşırıyor. Küçük ve sık harcamaların toplamı beklenenden yüksek çıkıyor.

Abonelikler ayrı bir başlık. Otomatik yenilenen ödemeler gözden kaçıyor, kullanmadığın servise para veriyor olabilirsin. Listeyi çıkarıp tek tek bak, genelde anında tasarruf çıkıyor.

İkinci ay hedef koy. Ama gerçekçi olsun. Yüzde on azaltma yüzde elliden daha kalıcı.

Acil durum fonu en önemli parça. Üç aylık gider kadar birikim, beklenmedik durumda borçlanmanı önlüyor. Bu olmadan yatırım düşünme.

Ayda bir kez on beş dakika gözden geçirmek yeterli. Sistem oturunca kendiliğinden yürüyor.

Son bir not: nakit ile kart arasındaki fark sandığından büyük. Nakit harcarken insan daha çok düşünüyor, bu psikolojik olarak ölçülmüş bir şey. Belli kategorileri nakde çevirmek denemeye değer."""),

("akademik", """Antibiyotik direnci modern tıbbın en ciddi tehditlerinden biri sayılıyor. Basitçe: bakteriler kendilerini öldüren ilaçlara dayanıklı hale geliyor ve tedavi edilebilir enfeksiyonlar yeniden ölümcül olabiliyor.

Mekanizma evrimsel. Antibiyotik duyarlı bakterileri temizlerken dirençli olanlara alan açıyor. Onlar çoğalıyor ve popülasyondaki payları büyüyor.

Gereksiz kullanım süreci hızlandırıyor. Viral enfeksiyonda antibiyotik yazmak tıbben yararsız ama direnç gelişimine katkıda bulunuyor. Tedaviyi yarıda bırakmak da aynı kapıya çıkıyor.

Hayvancılıktaki kullanım ayrı bir boyut. Büyümeyi hızlandırmak için verilen antibiyotikler, dirençli suşların gıda yoluyla insana geçmesine zemin hazırlıyor. Birçok ülke bunu kısıtladı.

Yeni antibiyotik geliştirme ise yavaş ilerliyor. Araştırma pahalı, beklenen kazanç düşük, ilaç şirketleri bu alandan çekildi. Kamu destekli programlar boşluğu doldurmaya çalışıyor.

Hastane içi enfeksiyon kontrolü en etkili araçlardan biri. El hijyeni ve izolasyon protokolleri bulaşı ciddi biçimde azaltıyor.

Yani bu tek bir sektörün çözebileceği bir sorun değil. Tıp, veterinerlik, tarım ve çevre birlikte hareket etmek zorunda.

Hasta tarafında da bir beklenti sorunu var. Doktora giden kişi elinde reçeteyle çıkmak istiyor, çıkmazsa tedavi edilmemiş hissediyor. Bu beklentiyi değiştirmek, düzenleme yapmaktan daha zor ve daha yavaş ilerliyor."""),

("kurumsal", """Kalite sistemimizin yıllık gözden geçirmesi bitti, bulguları paylaşıyoruz.

Denetimleri bağımsız kuruluşlar yaptı. Genel işleyişin standartlara uygun olduğu görüldü. İyileştirme gereken yerler için düzeltici plan hazırlandı ve uygulamaya alındı.

Üretimde izlenebilirliği güçlendirdik. Hammadde girişinden sevkiyata kadar her aşama dijital kayıt altında. Bir uygunsuzluk çıkarsa kaynağını hızla bulabiliyoruz. Eskiden bu iş günler alıyordu.

Müşteri geri bildirimlerini sisteme bağladık. Gelen bildirimler kategorilere ayrılıp ilgili birime gidiyor, çözüm süresi izleniyor. Ortalama süre geçen yıla göre kısaldı.

Tedarikçi denetimleri planlanan takvimde yürüdü. Kriterleri karşılamayanlarla iyileştirme planı üzerinde çalıştık, bazılarında çalışma ilişkisini yeniden değerlendirdik.

Personel eğitimlerinde katılım hedeflediğimiz düzeydeydi. Eğitimin gerçekten işe yarayıp yaramadığını ölçmek için yöntem geliştiriyoruz, orası henüz eksik.

Önümüzdeki dönem otomasyon yatırımlarına devam edeceğiz.

Bir eksiğimizi de yazalım: müşteri şikâyetlerinin kök neden analizi hâlâ istediğimiz derinlikte değil. Belirti düzeyinde çözüyoruz, altta yatan süreç sorununa her zaman inemiyoruz. Önümüzdeki dönemin önceliklerinden biri bu."""),
]


def rows():
    return [{"text": " ".join(t.split()), "label": 1, "lang": "tr",
             "source": "parafraz/" + kind, "attack": "parafraz"} for kind, t in SAMPLES]


if __name__ == "__main__":
    rs = rows()
    ws = [len(r["text"].split()) for r in rs]
    print("parafraz kumesi: %d metin | kelime min %d / ort %d / max %d | >=140: %d"
          % (len(rs), min(ws), sum(ws) // len(ws), max(ws), sum(1 for w in ws if w >= 140)))
