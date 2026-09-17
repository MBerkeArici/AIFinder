# -*- coding: utf-8 -*-
"""Zor / "gizlenmis" Turkce AI ornekleri (bir buyuk dil modeli tarafindan uretildi).

NEDEN VAR: engine/hidden.py Ingilizce'de AUC 0.994 veriyor ama Turkce'de
katman hic yok — SUPPORTED_LANGS = ("en",). Gerekcesi hidden.py'de yazili:
Turkce icin ayri bir kafa egitilmeli, bunun icin de once Turkce gizlenmis
AI ornekleri toplanmali. Bu dosya o eksigi kapatir.

Olcum (eval/report.md, Turkce): ensemble TPR@FPR1% yalnizca %48 — yani
yanlis pozitifi %1'de tutan esikte AI metinlerinin yarisi kaciyor. Kacanlar
tam olarak bu dosyadaki turden metinler: kalip ifade kullanmayan, cumle
uzunlugu degisken, somut ayrinti tasiyan, "yapay zeka gibi gorunmemeye"
calisan yazilar.

USLUP DENGESI UYARISI: hidden.py'nin notu Ingilizce icin de gecerli —
egitimde insan tarafi uslup olarak eslesmezse model yapay zekayi degil
"resmi dil"i ogrenir. Bu set gayriresmi agirlikli oldugu icin, egitimde
karsisina gayriresmi Turkce insan metni (urun yorumlari, forum) konmali;
yalnizca Vikipedi/haber ile egitilirse olculen basari sahte cikar.
"""

SAMPLES = [
("deneme", """Masamdaki kaktüs üç proje yöneticisinden uzun yaşadı. Şirket kat değiştirdiğinde taşınma hediyesi olarak gelmişti ve bugüne kadar kimse sahiplenmedi. Cuma günleri suluyorum, çoğunlukla alışkanlıktan. O da karşılık olarak pencereye doğru yan yatarak büyüdü, hafif sitemkâr bir açıyla.

Burada öğretici bir şey var. Kaktüs neredeyse hiçbir şey istemiyor ve neredeyse hiçbir şey almıyor, buna rağmen ayakta. Oysa işin etrafına kurduğumuz özenli sistemler — panolar, sprint tahtaları, ismi düşünülerek konmuş kanallar — sürekli ilgi istiyor ve biri bakmayı bıraktığı anda çöküyor.

İhmalin bazen bir tasarım biçimi olduğunu fark eden ilk kişi ben değilim. Heyecana dayanan sistemler, heyecan bitince ölüyor. Hiçbir şeye dayanmayanlar ise yaşamayı sürdürüyor. Her şirketteki en çirkin tablo dosyasının neden herkesin gerçekten kullandığı dosya olduğu da bundan.

Kaktüsün paydaşı yok. Hiçbir zaman göç ettirilmedi. Şirket gelecek yıl araçlarını yine değiştirdiğinde — ki değiştirecek — kaktüs geçiş planına aldırmadan yan büyümeye devam edecek.

Bunu hedeflenmeye değer bir ölçüt saymaya başladım. Kimse bakmazken çalışmayı sürdüren şeyi yap. Gerisi seyirci isteyen bir gösteri.

Geçen hafta yeni bir yönetici geldi. Masaları dolaşırken kaktüsün önünde durdu, "bu ne kadar zamandır burada" diye sordu. Kimse tam bilmiyordu. Dört yıl dedim, tahminen. Başını salladı, yürüdü gitti. Kaktüs hakkında bir karar alınmadı, ki en iyisi de bu."""),

("analiz", """Uzaktan çalışmanın ekonomisi genelde ofis kirasından tasarruf üzerinden konuşuluyor, ki hikâyenin en az ilginç kısmı bu. Ofisler pahalı, ama maaşların yanında yuvarlama hatası kalıyorlar. Asıl değişken, şirketin kimi işe alabildiği.

Konum istihdamı kısıtlamayı bıraktığında aday havuzu genişliyor ve ücret tabanı kayıyor. Bu iki yönlü kesiyor. Pahalı bir şehirdeki firma, asla taşınmayacak adaylara erişiyor. Aynı adaylar da kendi yerel piyasalarının kaldıramayacağı maaşlara. Bir süre iki taraf da kazandığını düşünüyor.

Düzeltme sonra geliyor. Coğrafyadan koparılan ücret bantları yukarı değil aşağı yakınsıyor — bir komplo yüzünden değil, basitçe küresel işe alan bir şirketin pozisyondan fazla adayı olduğu için. Çalışanların ilk kıtlık döneminde kısa süre tattığı pazarlık gücü, havuz genişleyince yaşamıyor.

İlginç olan, bunun hangi tarafta daha hızlı gerçekleştiği. Üst düzey rollerde yakınsama yavaş, çünkü değerlendirme zor ve ikame maliyeti yüksek. Kolayca tarif edilebilen işlerde ise neredeyse anında oluyor. Yani uzaktan çalışma eşitleyici değil; ayrıştırıcı.

Bir de ölçüm sorunu var. Uzaktan çalışmanın verimliliğe etkisini araştıran çalışmaların çoğu, gönüllü olarak uzaktan çalışmayı seçmiş kişileri inceliyor. Kendi seçimiyle uzaktan çalışan biriyle, zorunlu olarak evde kalan biri aynı örneklem değil. Pandemi dönemi verisi bu yüzden sanıldığı kadar kullanışlı çıkmadı."""),

("ani", """Babam arabayı hep aynı yere park ederdi. Sitenin girişine beş adım, gölgeye değil, gölgenin iki metre ötesine. Sorduğumda "öğleden sonra gölge oraya kayıyor" derdi. Doğruydu da.

Öldükten sonra arabayı sattık. Alıcı genç bir adamdı, muhtemelen ilk arabasıydı. Anahtarı verirken bir şey söylemek istedim, söyleyemedim. "Gölge saat üçte oraya geliyor" demek saçma olurdu.

Şimdi düşünüyorum da, insanların geride bıraktığı şeylerin çoğu bu türden. Miras dediğimiz şey tapular ve hesaplar değil, kimsenin devralamayacağı bir park yeri bilgisi. Bir ekmeğin hangi fırından alınacağı. Hangi musluğun sıkı kapatılması gerektiği.

Annem hâlâ o siteye park ediyor, aynı noktaya. Kendi arabası, kendi alışkanlığı değil. Bir kez sordum, omuz silkti. "Alışmışım" dedi.

Alışkanlık miras kalmaz aslında, taklit edilir. Ama yeterince uzun taklit edilirse aradaki fark kalmıyor galiba.

Geçen yaz o siteye uğradım. Park yeri boştu, saat de üçe yakındı. Gölge tam oradaydı, babamın dediği gibi. Bir süre arabanın içinde oturdum. Sonra çalıştırıp gittim, park etmeden. Neyi kanıtlamaya çalıştığımı bilmiyorum."""),

("forum", """Ben de aynı sorunu yaşadım, çözümü biraz saçma ama işe yaradı yazayım.

Modem yeni, hat yeni, hız testi gayet iyi çıkıyor ama akşam yedi civarı video izlerken donmalar başlıyordu. Önce servis sağlayıcıyı aradım tabii. Hat testi yaptılar, "sorun görünmüyor" dediler. Bir hafta böyle gitti.

Sonra fark ettim: donmalar sadece oturma odasında oluyordu. Yatak odasında sorun yok. Halbuki modeme daha uzak. Mantıksız geldi önce.

Meğer komşunun yeni aldığı kablosuz kamerası aynı kanalda yayın yapıyormuş. Modem otomatik kanal seçiyor ama bir kere seçince değiştirmiyor. Kanalı elle 11'e aldım, sorun bitti.

Yani hız testi iyi diye rahat olmayın. Testin ölçtüğü şeyle akşam yaşadığınız şey aynı değil. Kanal çakışması hız testinde görünmüyor çünkü test kısa sürüyor ve genelde çakışmanın olmadığı anda denk geliyor.

Modemin arayüzünde "kanal tarama" diye bir şey varsa ona bakın. Yoksa telefona bir wifi analiz uygulaması kurup hangi kanalların dolu olduğuna bakabilirsiniz. Beş dakikalık iş.

Bir de ek not: kanalı elle sabitledikten sonra modemi yeniden başlatırsanız bazı markalarda ayar sıfırlanıyor, otomatiğe dönüyor. Benimkinde öyle oldu. Ayarı yaptıktan sonra bir kez yeniden başlatıp kontrol edin, kalıcı olmuş mu diye. Kalmıyorsa modemin yazılımını güncellemek gerekebilir."""),

("teknik", """Veritabanı yavaşlamasının en sık sebebi eksik indeks değil, gereksiz indeks. Bunu anlaması biraz zaman aldı.

Bizim tabloda on bir indeks vardı. Çoğu, bir zamanlar birisinin yavaş bulduğu bir sorgu için eklenmişti. O sorgular çoktan değişmiş, indeksler kalmıştı. Okuma tarafında kimse fark etmiyordu. Yazma tarafında her satır eklendiğinde on bir ayrı yapı güncelleniyordu.

Ölçtüğümüzde ekleme işleminin süresinin yüzde altmışı indeks bakımına gidiyordu. Kullanılmayan yedi indeksi sildik. Ekleme süresi üçte birine indi, hiçbir sorgu yavaşlamadı.

Buradaki asıl ders şu: indeksler ücretsiz görünüyor çünkü maliyetleri ölçtüğümüz yerde görünmüyor. Sorgu planına bakarsın, indeks kullanılıyor, iyi. Ama ekleme maliyetine kimse bakmıyor.

Postgres'te `pg_stat_user_indexes` tablosu hangi indeksin kaç kez kullanıldığını tutuyor. Üretimde bir ay çalışmış bir sistemde `idx_scan` değeri sıfır olan indeks, neredeyse kesinlikle silinebilir. Neredeyse diyorum çünkü ayda bir çalışan bir rapor olabilir. Silmeden önce sorun.

Silmeden önce bir şey daha: indeksi hemen silmek yerine önce `pg_index` üzerinden devre dışı bırakmayı deneyebilirsiniz. Böylece bir hafta gözlemleyip sorun çıkmazsa kalıcı silersiniz. Silinen indeksi geri oluşturmak büyük tabloda saatler sürebiliyor, o yüzden bu ara adım ucuz bir sigorta."""),

("elestiri", """Filmin ilk kırk dakikası çok iyi, sonrası dağılıyor ve bunun nedeni senaryo değil, kurgu.

Açılış sahnesinde kadın mutfakta tek başına. Kamera hareket etmiyor, kesme yok, yaklaşık iki dakika. Sadece çay demliyor. Hiçbir şey olmuyor ama sahne gergin, çünkü arkada bir kapı açık ve biz o kapıyı görüyoruz, o görmüyor. Yönetmen bize bilgi verip karaktere vermiyor. Klasik ama iyi kurulmuş.

Sonra ikinci perdede bu sabır tamamen kayboluyor. Sahneler ortalama on iki saniye. Karakterin bir karar aldığını görmüyoruz, kararın sonucunu görüyoruz. Aradaki boşluk, izleyicinin karakterle kurduğu bağı kesiyor.

Bunun bir yapım kararı olduğunu düşünüyorum. Film festival versiyonunda iki saat on dakikaymış, gösterime giren hali bir saat kırk beş. Kesilen yirmi beş dakikanın nereden kesildiği belli.

Açılışı böyle kuran biri ortasını böyle kesmez. Sonuç olarak elimizde iyi bir filmin içinden çıkarılmış, tutarsız bir film var. İlk kırk dakika için yine de izlenir.

Oyunculuk tarafına hiç girmedim çünkü orada söylenecek fazla şey yok. İki başrol de işini yapıyor. Yan rollerden biri fazla tanıdık bir kalıba oturuyor ama bu da yönetmenin tercihi olabilir. Kurgu meselesi yanında bunlar ayrıntı kalıyor zaten."""),

("gezi", """Kasabaya varmak için otobüsten inip kırk dakika yürümek gerekiyor, çünkü yol asfaltsız ve kimse o yolu kullanmıyor. Bunu önceden bilmiyordum.

Yürürken iki kişiyle karşılaştım. İkisi de nereye gittiğimi sordu, ikisi de cevabı duyunca aynı ifadeyi yaptı — hafif kaşları kalktı, bir şey söylemedi. Vardığımda anladım nedenini. Kasabada otuz kadar ev var ve on beşi boş.

Kahvede oturdum. Kahve deyince yanlış anlaşılıyor, dört masalı bir oda. Adam çay getirdi, para almadı. "Misafirsin" dedi. Sonra kırk dakika konuştuk, daha doğrusu o konuştu ben dinledim.

Buradaki mesele turistik güzellik değil. Fotoğraf çekecek bir şey yok açıkçası, manzara sıradan. Ama bir yerin nüfusunun neden azaldığını okumakla, o azalmanın içinde oturup çay içmek aynı şey değil.

Dönüş otobüsünü kaçırdım, o gece orada kaldım. Ertesi sabah aynı adam beni yola kadar geçirdi. Adresini aldım, mektup yazacağımı söyledim. Yazmadım. Bunu düşününce hâlâ rahatsız oluyorum.

Dönüşte otobüste yanımda oturan kadın da aynı kasabadanmış. Otuz yıl önce çıkmış, yılda bir kez geliyormuş. "Değişmiyor" dedi, sonra düzeltti: "azalıyor ama değişmiyor." Aradaki farkı düşünüp durdum yol boyunca."""),

("is-notu", """Toplantıyı iptal etmemiz gerektiğini düşünüyorum, sebebini yazayım.

Haftalık senkron toplantımız yedi kişi, kırk beş dakika. Yani haftada beş buçuk saatlik kurum zamanı. Son altı toplantının notlarına baktım. Alınan karar sayısı: iki. Geri kalan her şey durum aktarımıydı, ki zaten panoda yazıyor.

Toplantının asıl işlevi karar almak değil, insanların birbirini görmesi diye düşünülebilir. Makul bir gerekçe ama o zaman kırk beş dakika yanlış format. On beş dakikalık bir sohbet aynı işi görür.

Önerim: haftalık toplantıyı kaldıralım, yerine iki şey koyalım. Birincisi, karar gerektiren konular için talep üzerine toplanan kısa görüşme — konusu ve katılımcısı belli. İkincisi, ayda bir kez daha uzun, gerçekten tartışmalı konular için.

Bunu iki ay deneyip geri dönebiliriz. Kötü giderse eski düzene dönmek beş dakikalık iş.

Karşı argüman duymak isterim, özellikle yeni başlayan arkadaşlardan — onlar için bağlam edinme açısından toplantının değeri benim gördüğümden fazla olabilir.

Uygulama tarafında bir ayrıntı: toplantıyı kaldırırsak panonun güncel tutulması daha da önemli hale geliyor. Şu an panoya kimse bakmıyor çünkü bilgi zaten toplantıda söyleniyor. Bu sırayı tersine çevirmemiz gerekecek, yoksa toplantıyı kaldırmak bilgiyi kaldırmaya dönüşür."""),

("mektup", """Uzun zamandır yazmadım, kusura bakma. Aslında birkaç kez başladım, yarıda bıraktım. Sebebini tam bilmiyorum.

Taşındık sonunda. Yeni ev daha küçük ama balkon var, sen bilirsin balkon meselemi. Sabahları orada kahve içiyorum. Karşıda bir okul var, sekiz buçukta zil çalıyor, çocuklar bağırıyor. İlk hafta rahatsız oldum, şimdi zil çalmasa eksik hissediyorum.

İşler aynı. Aynı derken gerçekten aynı, iki yıl önce sana anlattığım sorunlar hâlâ duruyor. Bazen düşünüyorum, ben mi değişmiyorum yoksa yer mi değişmiyor.

Annem iyi. Geçen ay hastaneye gitti ama ciddi bir şey çıkmadı. Doktoru "yaşına göre gayet iyi" dedi, o da "yaşım ne ki" diye kızdı. Seni sordu.

Bu yaz gelebilir misin bilmiyorum ama gelirsen yer var artık. Küçük ev dedim ama iki oda.

Yazarsan sevinirim. Yazmazsan da anlarım, ben de yazmadım iki yıl.

Bir şey daha. Geçen gün eski fotoğrafları karıştırırken o yaz çekilen resmi buldum, hani sen şapkayla duruyorsun ya. Arkasına bir tarih yazmışız ama kimin yazısı belli değil. Sana göndereyim mi, yoksa sende de var mı bilmiyorum."""),

("blog", """Ekmek yapmaya başladıktan sonra markette ekmek almayı bıraktığımı söyleyemem. Hâlâ alıyorum, çünkü haftanın her günü hamur yoğuracak vaktim yok. Ama tadı hakkında düşünme biçimim değişti.

İlk denemem taş gibi çıktı. Maya ölmüştü, suyun sıcaklığından. Kimse söylemiyor bunu, tariflerde "ılık su" yazıyor, ılık herkes için farklı. Otuz sekiz derece civarı deniyor, elle anlamak zor.

İkincisi kabardı ama içi çiğ kaldı. Fırın termostatı yalan söylüyormuş — ayrı bir termometre aldım, ayar iki yüzü gösterirken içerisi yüz yetmiş beşmiş. Bunu öğrenmek yalnızca ekmeği değil, o fırında yaptığım her şeyi düzeltti.

Üçüncüsünde oldu. Kabuk çıtırdadı, iç dokusu düzgün geldi.

Buradan çıkan ders ekmekle ilgili değil aslında. Tarifler, ölçülebilir olduğunu varsaydığımız değişkenler üzerine kurulu. Gerçekte o değişkenlerin çoğu senin mutfağında farklı. Tarifin işe yaramaması genelde tarifin hatası değil, ölçüm hatası.

Son bir not: un meselesine hiç girmedim çünkü orası ayrı bir konu. Aynı tarif farklı unlarla farklı çıkıyor ve paketin üstündeki bilgi genelde yetersiz. Protein oranı yazmıyorsa deneyerek bulmak gerekiyor, ki bu da birkaç başarısız ekmek demek."""),

("gozlem", """Metroda kimse kimseye bakmıyor ama herkes birbirinin nerede duracağını biliyor. Bu tuhaf bir koordinasyon.

Kapı açıldığında inenler için açılan boşluk hep aynı genişlikte. Kimse ölçmüyor, kimse yönetmiyor. Yeni gelen biri yanlış yere dursa, üç saniye içinde kendiliğinden düzeliyor — itilerek değil, sadece etrafındakilerin küçük kaymalarıyla.

Bunu birkaç haftadır izliyorum, iş sıkıcı olduğu için. Fark ettiğim şu: koordinasyonun bozulduğu tek an, birinin telefona bakarken yürümesi. O kişi sisteme dahil olmuyor ve etrafındaki herkes onun etrafından dolaşmak zorunda kalıyor. Yani maliyet dağılıyor, sadece ona değil.

Trafikte de aynısı var galiba. Kurallara uymayan bir araç kendine zaman kazanıyor ama arkasındaki kırk araca küçük gecikmeler bindiriyor. Toplamı kazandığından büyük.

Bunun ahlaki bir hikâyeye dönüşmesi kolay ama ilgimi çeken kısmı o değil. İlgimi çeken, kimsenin öğretmediği bu düzenin nasıl bu kadar sağlam olduğu. Ve tek bir dikkatsizlikle nasıl bozulduğu.

Bir ayrıntı daha fark ettim: koordinasyon vagon tipine göre değişiyor. Kapıları geniş olan vagonlarda boşluk daha dar kalıyor, çünkü insanlar kapının genişliğine değil kendi görüş açılarına göre yer açıyor. Yani tasarımın hesapladığı şeyle insanların yaptığı şey örtüşmüyor."""),

("tarif-disi", """Kedim on bir yaşında ve son altı aydır sabahları kusuyor. Veteriner tüy yumağı dedi, macun verdi. Macun işe yaramadı.

İkinci veterinere gittim. Kan tahlili istedi. Böbrek değerleri hafif yüksek çıkmış ama "yaşına göre normal" dedi. Mama değiştirmemi önerdi.

Mamayı değiştirdim, iki hafta iyiydi, sonra tekrar başladı. Bu sefer daha dikkatli izledim. Her sabah değil, sadece gece boyunca mama kabı boş kaldığında oluyormuş. Yani aç kalınca mide asidi.

Çözüm otomatik mama kabı almak oldu. Gece üçte küçük bir porsiyon veriyor. Kusma tamamen bitti.

Bunu yazıyorum çünkü iki veteriner de doğru şeyleri söyledi ama ikisi de sorunun ne zaman olduğunu sormadı. Ben de söylemedim, çünkü önemli olduğunu bilmiyordum.

Hayvanla ilgili bir sorun yaşayan varsa: gitmeden önce bir hafta not tutun. Saat kaçta, ne yedikten sonra, ne kadar sonra. Veteriner bu bilgiyi sizden alamıyorsa tahmin yürütmek zorunda kalıyor.

Otomatik kabı alırken dikkat edilecek şey porsiyon hassasiyeti. Ucuz olanlar gramajı tutturamıyor, bazen iki katını veriyor. Kedi yaşlıysa ve kilo takibi yapıyorsanız bu önemli. Benimki on gram sapmayla çalışıyor, yeterli."""),

("ogretici", """Fotoğrafta ışığı anlamanın en hızlı yolu makineyi bırakıp gölgelere bakmak.

Öğleyin dışarı çık ve kendi gölgene bak. Kenarı keskin. Bu, ışık kaynağının küçük ve uzak olduğu anlamına geliyor. Aynı şeyi bulutlu bir günde yap, gölge neredeyse yok, olan da yumuşak. Bulut ışığı yaymış, kaynak büyümüş.

Stüdyoda binlerce liralık ekipmanın yaptığı şey tam olarak bu: kaynağı büyütmek ya da küçültmek. Şemsiye, yumuşatıcı kutu, yansıtıcı — hepsi bulut taklidi.

Bunu anladıktan sonra pencerenin yanında çekim yapmak bedava bir stüdyo oluyor. Perde varsa yumuşatıcın var. Karşı duvar beyazsa yansıtıcın var.

Bir şey daha: mesafe. Işık kaynağını konuya yaklaştırdıkça yumuşuyor, uzaklaştırdıkça sertleşiyor. Pencereden bir metre uzakta çekilen yüz ile üç metre uzakta çekilen yüz farklı görünür, aynı pencere olmasına rağmen.

Makine ayarları bunlardan sonra gelir. Diyafram ve enstantane ışığın miktarını belirliyor, karakterini değil. Karakteri belirleyen yukarıdaki iki şey.

Bunları öğrendikten sonra yapılacak en iyi alıştırma şu: bir hafta boyunca sadece pencere ışığında, tek bir nesneyi günün farklı saatlerinde çek. Aynı nesne, aynı yer, değişen tek şey ışık. Karşılaştırınca gölgenin karakterinin ne kadar değiştiğini görmek, okuyarak öğrenilecek bir şey değil."""),

("tartisma", """Yapay zekânın işleri elinden alacağı tartışması yanlış soruyla başlıyor bence.

Soru "hangi meslekler yok olacak" değil, "hangi görevler ucuzlayacak" olmalı. Meslekler görev demetleri. Bir muhasebecinin işi tek bir şey değil; veri girişi, mevzuat yorumu, müşteriyle konuşma, sorumluluk üstlenme. Bunlardan birincisi ucuzluyor, diğerleri ucuzlamıyor.

Tarihsel örnek olarak ATM'ler sık veriliyor. ATM geldiğinde banka veznedarı sayısı azalmadı, arttı. Çünkü şube açmak ucuzladı, şube sayısı arttı, veznedarın işi para saymaktan ürün satmaya kaydı.

Ama bu örneği fazla rahatlatıcı bulanlardanım. ATM tek bir görevi otomatikleştirdi. Şu anki durumda birden fazla görev aynı anda ucuzluyor ve bunların bazıları demetteki "pahalı" görevler.

Asıl belirleyici olan, ucuzlayan görevin demet içindeki payı. Payı yüzde yirmiyse verimlilik artışı olur. Yüzde seksense o meslek yeniden tanımlanır.

Bunu sektör sektör konuşmak gerekiyor. Genel cevap yok, genel cevap arayan tartışmalar da bir yere varmıyor.

Bir de zamanlama meselesi var. Görevler aynı anda ucuzlamıyor, sırayla ucuzluyor. Bu da mesleklerin yok olmasından çok, sürekli yeniden tanımlanması anlamına geliyor. Sürekli yeniden tanımlanan bir meslekte kariyer planlamak, yok olan bir meslekte plan yapmaktan daha zor olabilir."""),

("gunluk", """Bugün hiçbir şey yapmadım denemez ama yapılanların toplamı da bir şey etmiyor.

Sabah üç saat bir hatayı aradım. Bulduğumda bir satırdı, hem de benim geçen hafta yazdığım satır. Değişkeni yanlış yerde tanımlamışım. Düzeltmek on saniye sürdü.

Öğleden sonra toplantı. Konu geçen ayki toplantının konusuydu, muhtemelen gelecek ayınki de olacak. Kimse karar alamıyor çünkü karar alması gereken kişi toplantıda değil.

Akşam yürüyüşe çıktım. Hava serinlemiş, yaz bitiyor galiba. Parkta bir adam köpeğine sürekli "otur" diyordu, köpek oturmuyordu. Yarım saat sonra döndüğümde hâlâ aynı yerdeydiler, adam hâlâ aynı şeyi söylüyordu.

Eve gelince bir şey yazmak istedim, bu çıktı.

Bazı günler böyle. Kötü değil aslında, sadece şekilsiz. Şekilsiz günler anlatılamadığı için yokmuş gibi oluyor, oysa hayatın çoğu bunlardan.

Yatmadan önce yarınki işlere baktım. Üç madde var, üçü de bugünden devredilmiş. Yarın da devredilirse bir şey demek istiyor olmalı ama ne dediğini çözemedim. Uyku bastırdı."""),

("inceleme", """Uygulamayı üç haftadır kullanıyorum, kısa değerlendirme yazayım.

İyi tarafı: senkronizasyon gerçekten hızlı. Telefonda yazdığım not bilgisayarda iki saniye içinde görünüyor. Rakiplerinde bu bazen dakikaları buluyordu.

Kötü tarafı: arama işe yaramıyor. Tam kelime eşleşmesi arıyor, ekleri görmezden gelmiyor. "Toplantı" yazınca "toplantıda" geçen notu bulmuyor. Türkçe için bu ciddi bir eksik, çünkü dilin yapısı gereği kelimelerin çoğu ek almış halde bulunuyor.

Geliştiriciye yazdım, "listede var" cevabı geldi. Ne zaman olacağı belli değil.

Ücretlendirme tarafında da bir gariplik var. Ücretsiz sürümde not sayısı sınırsız ama klasör sayısı beşle sınırlı. Bu, kullanıcıyı düzenli olmaktan caydıran tuhaf bir tercih. Sınır koyacaklarsa not sayısına koymaları daha mantıklı olurdu.

Şu anki halinde tavsiye eder miyim: hızlı senkron sizin için belirleyiciyse evet. Çok not biriktirip sonra arayan biriyseniz hayır, arama düzelene kadar bekleyin.

Veri taşıma tarafını da denedim, oradan söz edeyim. Dışa aktarma çalışıyor ama biçimlendirme kayboluyor — kalın yazılar düz metne dönüyor. Notlarınızda biçimlendirme önemliyse bu ciddi bir kayıp. İçe aktarma tarafı ise sorunsuz, rakip uygulamadan gelen dosyayı düzgün okudu."""),

("hatira", """Lisede matematik öğretmenimiz tahtaya soruyu yazar, sonra sınıfa arkasını dönüp pencereden bakardı. Bir dakika kadar. Kimse konuşmazdı.

Yıllar sonra öğrendim ki o bir dakikada düşünmemizi beklemiyormuş. Kendini toparlıyormuş. Eşi hastaymış o dönem, kimse bilmiyordu.

Bunu bana yıllar sonra sınıf arkadaşım anlattı, o da başka bir öğretmenden duymuş.

Şimdi düşünüyorum, o sessiz dakikalar sınıfın en verimli anlarıydı. Çünkü kimse bize "düşünün" demiyordu, sadece düşünecek zaman vardı. Şimdiki eğitimde en eksik şey bu galiba — boşluk. Her dakika bir şeyle doldurulmuş durumda.

Öğretmenin niyeti pedagojik değildi. Yine de işe yaradı.

Bazen en iyi yöntemler böyle ortaya çıkıyor sanırım. Biri kendi derdiyle uğraşırken tesadüfen doğru şeyi yapıyor, sonra başkaları onu kopyalıyor ve neden işe yaradığını açıklamaya çalışıyor.

Geçen sene mezunlar buluşmasında öğretmeni andık. Birkaç kişi o sessizliği hatırlıyordu, ama hepsi farklı açıklamıştı kendine. Biri "bize güveniyordu" demişti, bir diğeri "sinirleniyordu, kendini tutuyordu". Gerçek sebebi bilen tek kişi bendim ve söylemedim."""),

("acikla", """Enflasyonun neden herkesi aynı oranda etkilemediğini anlatmaya çalışayım, çünkü bu kısım genelde atlanıyor.

Açıklanan oran bir sepetin ortalaması. Sepette gıda var, kira var, ulaşım var, elektronik var. Herkesin harcaması aynı dağılımda olsa ortalama herkes için doğru olurdu. Değil.

Geliri düşük bir hanenin harcamasının yüzde altmışı gıda ve kira. Geliri yüksek bir hanenin ise belki yüzde yirmisi. Gıda fiyatları ortalamanın üzerinde arttığında, düşük gelirli hanenin yaşadığı enflasyon açıklanan rakamdan yüksek oluyor. Aynı ülkede, aynı ay.

Buna literatürde "enflasyon eşitsizliği" deniyor ve ölçülebiliyor. Bazı ülkelerde aradaki fark yıllık beş puana kadar çıkıyor.

Pratik sonucu şu: "enflasyon düştü" haberi, size düştüğü anlamına gelmiyor. Kendi sepetinizi biliyorsanız kendi oranınızı kabaca hesaplayabilirsiniz — harcama kalemlerinizin payını, o kalemlerin artış oranıyla çarpıp toplamak yeterli.

Bu hesabı yapan çok az kişi var, oysa aradaki fark ciddi.

Bir de bileşim etkisi var, atlanmaması gereken. Fiyatlar arttıkça insanlar sepetini değiştiriyor — pahalılaşan üründen vazgeçip ucuzuna geçiyor. Resmî ölçüm bu değişimi gecikmeyle yansıtıyor. Yani hissedilen enflasyon ile açıklanan arasındaki farkın bir kısmı ölçüm gecikmesinden geliyor, kötü niyetten değil."""),

("tepki", """Yorumlara katılmıyorum, sorun fiyat değil.

Ürün pahalı evet, ama pahalı olduğu için değil, verdiği sözü tutmadığı için kötü. Aynı parayı isteyip işini yapan bir sürü şey var.

Kutudan çıkan ilk izlenim iyi. Malzeme sağlam, ağırlığı hissettiriyor. İlk hafta hiçbir şikâyetim yoktu. Sorun ikinci haftada başladı: pil ömrü yarıya düştü. Üçüncü haftada üçte birine.

Destek hattına yazdım. "Normal kalibrasyon süreci" dediler. Dördüncü hafta aynı. Tekrar yazdım, bu sefer değişim önerdiler. Değişen ürün de aynı davrandı.

Yani bu tekil bir arıza değil, tasarım sorunu. Ürünün tanıtımında yazan pil süresi muhtemelen laboratuvar koşullarında, ilk şarj döngüsünde ölçülmüş.

Puanım iki. Bir vermiyorum çünkü iade süreci sorunsuzdu, paramı geri aldım.

Almayı düşünenlere önerim: iade süresi boyunca günlük kullanın ve pil davranışını not edin. Sorun varsa ikinci haftada görünüyor, iade süresi genelde on dört gün — yani sınırda kalıyorsunuz.

Ekleme: iade ederken kutuyu ve tüm aksesuarları saklamış olmam işe yaradı. Kutuyu atmışsanız iade kabul edilmiyor, bu satın alma sayfasında küçük yazıyla yazıyor. Deneme süresi boyunca kutuyu bir kenarda tutun derim."""),

("dusunce", """Bir şeyi öğrendiğini nasıl anlarsın sorusu üzerine düşünüyorum.

Sınav geçmek yeterli değil. Ezberleyerek geçilebiliyor. Anlatabilmek daha iyi bir ölçüt ama o da tam değil — iyi ezberlenmiş bir açıklama akıcı çıkabilir.

Bana kalırsa ölçüt şu: konuyla ilgili yeni bir soruyu, daha önce duymadığın bir soruyu, cevaplayabiliyor musun. Cevap doğru olmasa bile, soruya nereden yaklaşacağını biliyor musun.

Bunu test etmek zor çünkü kendi kendine yeni soru üretmek zor. İnsan bildiği sorulara benzer sorular üretiyor.

En işe yarayan yöntem bir başkasına öğretmek. Öğrenen kişi tahmin edilemez sorular soruyor, çünkü senin kafandaki haritaya sahip değil. O sorular haritandaki boşlukları gösteriyor.

İkinci yöntem biraz beklemek. Bir ay sonra hâlâ anlatabiliyorsan öğrenmişsindir. Anlatamıyorsan o bilgi hiç yerleşmemiş, sadece kısa süre elinde durmuş.

İkisini de yapmak en iyisi ama ikisi de zaman istiyor ve bu yüzden kimse yapmıyor.

Üçüncü bir ölçüt daha var aslında: hatayı fark edebiliyor musun. Konuyu bilmeyen biri yanlış bir açıklama yaptığında rahatsız oluyorsan, o alanda bir şey oturmuş demektir. Rahatsızlık, açıklayamadığın bilginin bile var olduğunu gösteriyor."""),

("saha", """Sahada üç gün kaldık, beklediğimizden farklı çıktı.

Plan basitti: on iki köyde anket, köy başına yirmi hane. Kâğıt üstünde üç gün yeterliydi. Gerçekte ilk gün iki köy bitirebildik.

Sebebi ulaşım değildi, güven meselesiydi. İnsanlar kapıyı açıyor ama anketin ne işe yarayacağını sorup cevabı beğenmeyince kapatıyordu. Haklılar da. Daha önce gelen ekipler söz verip dönmemiş.

İkinci gün yöntemi değiştirdik. Önce muhtara gidip bir saat oturduk, çay içtik, ne yaptığımızı anlattık. O bizi iki haneye kendisi götürdü. Sonrası kendiliğinden açıldı. O gün beş köy bitti.

Buradan çıkan not, metodoloji bölümüne yazılmayacak ama yazılması gereken bir şey: veri toplamanın maliyeti anketin uzunluğuyla değil, girişin kalitesiyle belirleniyor.

Üçüncü gün kalan beş köyü tamamladık. Toplam 217 hane, hedef 240'tı. Eksik kalan 23 hane büyük ölçüde tek bir köyden — orada muhtar yoktu, kimse aracı olmadı.

Rapora yazılacak bir uyarı daha: eksik kalan köyün verisi diğerlerinden sistematik olarak farklı olabilir. Muhtarsız köy, muhtemelen nüfusu en çok azalan köy. Yani örneklem eksikliği rastgele değil, ve bu analizde belirtilmeli."""),

("itiraf", """Kitabı bitirmeden hakkında yazdım ve bunun yanlış olduğunu biliyordum.

Teslim tarihi vardı, kitap dört yüz sayfaydı, ben iki yüzde kalmıştım. Kalan kısmı hakkında yeterince fikir sahibi olduğumu düşündüm. Yazıyı yazdım, yayımlandı, kimse bir şey demedi.

Sonra bitirdim. Son yüz sayfada kitap tamamen başka bir şeye dönüşüyordu. Benim "tekrara düşüyor" dediğim yapı, aslında kasıtlı bir hazırlıkmış.

Yazıyı geri çekmedim. Düzeltme de yayımlamadım. Gerekçem şuydu: kimse fark etmedi, düzeltme dikkat çeker.

Bu gerekçenin kötü olduğunu o zaman da biliyordum.

Bir yıl sonra yazarla bir etkinlikte karşılaştım. Yazıyı okumuş. Bir şey demedi, sadece "sonunu beğenmediniz galiba" dedi ve konuyu değiştirdi.

Şimdi bunu yazıyorum çünkü aynı durumda olan biri varsa: düzeltme yayımla. Kimsenin fark etmemesi, yapılan şeyi doğru yapmıyor. Ben yapmadım ve bir yıl sonra bir etkinlikte o cümleyi duydum.

Bu arada kitabı ikinci kez okudum geçen yıl. İlk okumada kaçırdığım şey sadece son yüz sayfa değilmiş. Baştaki tekrarlar da kasıtlıymış, sonraki kırılmayı hazırlıyormuş. Yani yazı iki kere yanlıştı, bir kere değil."""),

("plan", """Bütçe önerisini sadeleştirdim, gerekçeleriyle birlikte aşağıda.

Üç kalem çıkardım. Birincisi, konferans katılımı. Geçen yıl dört kişi gitti, dönüşte hiçbiri sunum yapmadı, edinilen bilgi paylaşılmadı. Faydasız demiyorum, ölçülemiyor demiyorum — ölçmeye çalışmadık bile. Bu yıl bir kişi gitsin, dönüşte anlatsın, ertesi yıl buna göre karar verelim.

İkincisi, yazılım lisansları. Sekiz araca ödeme yapıyoruz, üçünün son üç ayda hiç oturum açılmamış. Yönetici hesabından bakılabiliyor, baktım.

Üçüncüsü, yedek donanım. Elimizde iki yedek dizüstü var ve ikisi de bir yıldır kutuda. Bir tanesi yeterli.

Eklediğim tek kalem: veri depolama. Şu anki paketin sınırına iki ay içinde varacağız, sonrasında yazma işlemleri duruyor. Bu, fark edilmeden gelirse acil ve pahalı bir sorun olur.

Net etki: yaklaşık yüzde on bir düşüş. Rakamlar ekte, itiraz edilecek kalem varsa konuşalım.

Bir de zamanlama önerisi: kesintileri yılbaşında değil, bu çeyrek içinde uygulayalım. Yılbaşına bırakırsak lisanslar otomatik yenileniyor ve bir yıl daha ödemiş oluyoruz. İptal için son tarih önümüzdeki ayın sonu, takvime aldım."""),

("sorun", """Aynı hatayı üçüncü kez yaşadık ve bu sefer sebebini yazıyorum ki dördüncüsü olmasın.

Gece yarısı yedekleme çalışıyor. Yedekleme sırasında bellek kullanımı tavan yapıyor. İşletim sistemi en çok bellek kullanan süreci kapatıyor. En çok bellek kullanan süreç bizim uygulama. Sabah geliyoruz, servis kapalı.

Üç kez de logda hiçbir şey yok, çünkü süreç kapanmadı — öldürüldü. Kapanma prosedürü çalışmadığı için kapanış kaydı da yazılmadı.

Bunu anlamak üç saat sürdü. `dmesg` çıktısında görünüyor aslında, ama oraya bakmak akla gelmiyor çünkü uygulama logu temiz.

Aldığımız önlemler: yedeklemeye bellek sınırı koyduk, uygulamayı öldürülme önceliğinde geriye çektik, ve sistem seviyesinde bir uyarı kurduk.

Genel ders: uygulamanızın logu sessizse sorun uygulamada olmayabilir. Bir katman aşağıya bakın. Biz üç kez yukarıya baktık.

Bir not daha: sistem seviyesindeki uyarıyı kurarken eşiği dikkatli seçin. İlk denemede eşiği düşük tuttuk, gecede altı bildirim geldi ve iki gün sonra herkes bildirimleri susturdu. Susturulan uyarı, olmayan uyarıdan kötü çünkü var sanıyorsunuz."""),

("yanit", """Sorunuza kısa cevap: hayır, o yöntem sizin durumunuzda işe yaramaz. Uzun cevabı yazayım.

Anlattığınız kadarıyla veri setiniz yaklaşık sekiz yüz satır. Önerilen yöntem derin öğrenme tabanlı ve bu boyutta veriyle ezberlemeye çok müsait. Doğrulama setinde iyi sonuç alsanız bile, o sonuç büyük ihtimalle yanıltıcı olur.

Bu boyutta veride klasik yöntemler genelde daha iyi. Gradyan artırma ya da düzenlileştirilmiş doğrusal model deneyin. İkisi de birkaç saniyede eğitiliyor, yani beş dakikada ikisini de görebilirsiniz.

Bir de şunu sorayım: sekiz yüz satır neyin sınırı? Toplanabilecek maksimum bu mu, yoksa şimdilik elinizde olan mı? İkinciyse, model seçmeye harcadığınız zamanı veri toplamaya harcamak daha yüksek getirili olabilir. İki bin satırda seçenekleriniz gerçekten değişir.

Değerlendirme tarafında da uyarayım: bu boyutta tek bir ayrım yeterli değil, çapraz doğrulama kullanın. Tek ayrımda alınan sonuç rastlantıya çok açık.

Son bir şey: hangi yöntemi seçerseniz seçin, temel çizgi kurmadan başlamayın. En sık görülen sınıfı her seferinde tahmin eden aptal bir model kurun ve onun skorunu not edin. Geliştirdiğiniz modelin o çizgiyi anlamlı biçimde geçip geçmediği, tek başına doğruluk oranından çok daha bilgilendirici."""),

("soru-cevap", """Sorduğunuz konuda kendi deneyimimi anlatayım, genel geçer bir cevap veremeyeceğim.

Ben de iki yıl önce aynı kararsızlığı yaşadım. Bölüm değiştirmek mi, devam edip mezun olmak mı. Danıştığım herkes farklı şey söyledi, bu da işi kolaylaştırmadı.

Sonunda şunu sordum kendime: bu bölümden mezun olsam, diploma elimde, ne yapacağım? Cevabım "bilmiyorum" oldu. Sonra ikinci soruyu sordum: değiştirsem ne yapacağım? Ona da net cevap veremedim ama en azından bir yön vardı.

Değiştirdim. İki yıl kaybettim, evet. Ama o iki yılı zaten kaybediyordum, sadece daha yavaş.

Sizin durumunuz farklı olabilir. Yaş, maddi durum, aile beklentisi — bunların hepsi denklemde. Benim lehime olan şey, ailemin baskı yapmamasıydı. Bu herkeste olmuyor.

Bir şey daha: "geç kaldım" hissi çok yanıltıcı. Sınıfta benden beş yaş büyük biri vardı, kimse umursamadı. Birkaç ay sonra ben de umursamamaya başladım.

Karar sizin tabii. Sadece şunu söyleyeyim: iki yıl sonra aynı yerde olmak da bir seçim ve o seçimin de bedeli var. İkisini yan yana koyup bakmak gerekiyor."""),

("dukkan", """Mahalledeki kırtasiye kapandı. Otuz yıllık dükkândı.

Amcanın adı Necati'ydi. Kalem alırdım çocukken, sonra üniversitede fotokopi çektirirdim. Son yıllarda pek uğramıyordum açıkçası, her şeyi internetten alıyorum.

Geçen hafta önünden geçerken kepenk kapalıydı, camda bir kâğıt: "Kapanmıştır, teşekkür ederiz." O kadar.

Bir anda suçluluk hissettim. Ben de sebeplerden biriyim sonuçta. Yıllarca oradan alışveriş yapmadım, sonra kapanınca üzülüyorum. Bu biraz sahtekârca.

Ama şunu da düşünüyorum: fiyatlar gerçekten farklıydı. İnternetten aldığım defter yarı fiyatına geliyordu. Öğrenciyken bu fark önemliydi. Şimdi de önemli aslında.

Yani suçluluk hissetmek ile yanlış yapmış olmak aynı şey değil galiba. Herkes kendi bütçesine göre davranıyor ve toplamı bir dükkânı kapatıyor. Kimse kötü niyetli değil.

Yerine ne açılacak bilmiyorum. Muhtemelen kafe. Bu sokakta dört kafe var zaten.

Necati amcayı görürsem ne derim bilmiyorum. Belki hiçbir şey demem, selam veririm sadece.

Bu arada sokağın karşısındaki manav da satılık levhası asmış. Onu geçen hafta fark ettim."""),

("rapor", """Pilot uygulamanın ilk ayına dair gözlemlerimi paylaşıyorum. Sayısal sonuçlar ekte, burada daha çok izlenimlerim var.

Beklediğimizden iyi giden şey: kullanıcılar sistemi hızlı benimsedi. Eğitim için ayırdığımız iki günün çoğu gereksiz kaldı, insanlar kendi başlarına keşfetti. Bu, arayüzün iyi tasarlandığını gösteriyor olabilir ama başka bir açıklaması da var: eski sistem o kadar kötüydü ki her alternatif kolay görünüyor.

Beklemediğimiz sorun: veri girişindeki tutarsızlık. Aynı bilgi farklı kişiler tarafından farklı biçimlerde giriliyor. Tarih formatı, isim yazımı, birim seçimi. Bunu sistem kısıtlamadığı için ortaya karışık bir veri kümesi çıkıyor. İlk ay bu fark edilmedi çünkü veri az. İkinci ayda raporlama yapmaya kalkarsak sorun görünür hale gelecek.

Önerim, kısıtlamaları şimdi eklemek. Sonra eklersek geçmiş veriyi temizlemek gerekir, o daha pahalı.

Bir de şu: kullanıcılar bize soru sormuyor. Bu iyi görünüyor ama emin değilim. Belki sorun yaşamıyorlar, belki sorun yaşayıp kendi çözümlerini üretiyorlar. İkincisi olursa sonradan anlarız, geç olur.

Önümüzdeki ay birkaç kullanıcıyla oturup izlemeyi öneriyorum. Anket değil, doğrudan gözlem."""),

("tarif", """Mercimek çorbasının sırrı malzemede değil, sabırda. Bunu annem söylerdi, doğru olduğunu geç anladım.

Herkesin tarifi aynı aslında: kırmızı mercimek, soğan, havuç, patates, tereyağı, un. Ölçüler biraz oynuyor ama temelde aynı. Peki neden bazıları daha güzel oluyor?

Soğanı iyi kavurmak gerekiyor. Şeffaflaşana kadar değil, hafif renk alana kadar. Bu on dakika sürüyor ve çoğu kişi üç dakikada geçiyor. Aradaki fark çorbanın tadında doğrudan hissediliyor.

İkinci nokta, unu yakmamak. Tereyağında unu kavururken kokusu değişiyor, o anı yakalamak lazım. Fazla kavrulursa acımsı oluyor, az kavrulursa hamur tadı kalıyor.

Blenderdan geçirme konusunda ikiye ayrılıyor insanlar. Ben geçiriyorum ama tamamen pürüzsüz yapmıyorum, hafif doku kalsın istiyorum.

Üzerine ne konacağı ayrı tartışma. Kırmızı biberli tereyağı klasik. Nane de olur. Limon şart bence ama karşı çıkanlar var.

Bir de kıvam. Soğuyunca koyulaşıyor, sıcakken ideal görünen kıvam tabakta sertleşiyor. Biraz sulu bırakmak gerekiyor.

Yazınca uzun göründü ama toplamda kırk dakikalık iş."""),

("izlenim", """Sergiyi gezdim, karışık duygularla çıktım.

İlk salon çok iyiydi. Erken dönem işleri kronolojik sırayla dizilmiş, yanlarında kısa notlar var. Sanatçının nasıl değiştiğini adım adım görüyorsunuz. İki resim arasında beş yıl var ve o beş yılda ne olduğunu tahmin edebiliyorsunuz.

İkinci salon sorunlu. Geç dönem işleri var ama bu sefer tematik gruplanmış, kronoloji bozulmuş. Neden böyle yapıldığını anlamadım. Küratör bir şey anlatmak istemiş herhalde ama bana ulaşmadı.

Aydınlatma da ikinci salonda kötü. Büyük tuvallerin üst kısmı gölgede kalıyor. Birkaç kişi geri çekilip bakmaya çalışıyordu, mesafe yetmiyor çünkü salon dar.

En sevdiğim iş girişteki küçük eskizdi aslında. Muhtemelen en önemsiz parça, bir kenarda duruyor. Ama içinde bir şey var, diğerlerinde olmayan bir tereddüt gibi.

Bilet fiyatı yüksek bence. Öğrenci indirimi var, o makul.

Giderseniz ikinci salonu önce gezin derim. Yorulmadan bakmak gerekiyor oraya, çünkü zaten zor bakılıyor.

Kataloğu almadım bu arada, pahalıydı. Sonra internetten birkaç görsel buldum, aynı şey değil tabii."""),

("tavsiye", """Ev taşıyacaklara birkaç şey söyleyeyim, üç kez taşındım son beş yılda, bazı dersler aldım.

Kutu sayısını her zaman az tahmin ediyorsunuz. Aldığınız kutu sayısını bir buçukla çarpın. Eksik kalırsa taşınma gününde market poşetiyle uğraşıyorsunuz, o da berbat oluyor.

Kutuların üstüne değil yanına yazın. Üst üste dizince üstteki yazı görünmüyor. Bunu üçüncü taşınmada öğrendim, utanç verici.

Bir kutuyu "ilk gece" diye ayırın. İçinde çarşaf, havlu, diş fırçası, telefon şarjı, bir tencere olsun. Taşınma günü akşamı hiçbir şey bulamıyorsunuz ve çok yoruluyorsunuz. O kutu hayat kurtarıyor.

Nakliyeciyle anlaşırken asansör durumunu mutlaka söyleyin. Söylemezseniz gün içinde fiyat değişiyor ve tartışma çıkıyor. Kat sayısı, asansöre sığmayan eşya varsa o da.

Elektrik ve su aboneliklerini önceden aktarın. Yeni eve gidip elektrik olmadığını anlamak kötü bir sürpriz.

Son olarak: atmaya çalışın. Taşınma, biriktirdiğiniz şeylerle yüzleşmek için iyi bir fırsat. Ben her seferinde bir şeyler attım ve hiçbirini özlemedim."""),

("yorum", """Yazınızı okudum, katıldığım ve katılmadığım yerler var.

Temel tespitiniz doğru: uzaktan çalışma ekip içi bağı zayıflatıyor. Bunu ben de gözlemliyorum. Yeni gelen biri ekibe karışmakta zorlanıyor, çünkü kahve molasında kurulan o gündelik ilişki yok.

Ama çözüm olarak ofise dönüşü önermeniz bana eksik geldi. Ofiste olmak da bağ kurmayı garanti etmiyor. Eski işimde herkes ofisteydi ve kimse kimseyle konuşmuyordu, hepimiz kulaklık takıp oturuyorduk.

Yani sorun mekân değil, tasarım. Bağ kurmak için ayrılmış zaman olmadığında, insanlar bunu kendiliğinden yapmıyor. Ne ofiste ne evde.

Bizde işe yarayan bir şey var: haftada bir kez otuz dakikalık, gündemi olmayan görüşme. İlk başta tuhaftı, şimdi ekibin en sevdiği toplantı. İş konuşulmuyor, kural bu.

Bunu ofiste de yapabilirsiniz tabii. Mesele formatı kurmakta.

Bir de yazınızdaki verimlilik verilerine temkinli yaklaşırdım. Kaynak gösterdiğiniz çalışma pandemi dönemine ait ve o dönem herkes olağanüstü koşullardaydı. Çocuklar evde, okullar kapalı. Bugüne genellemek zor."""),

("hikaye", """Otobüste yanıma oturan adam kitabımın adını sordu. Söyledim. "İyi mi?" dedi. "Daha yeni başladım" dedim.

Sonra o anlatmaya başladı. Kendisi de okurmuş eskiden, şimdi gözleri iyi görmüyormuş. Sesli kitap denemiş, olmamış. "Başkasının sesi araya giriyor" dedi.

Bunu daha önce hiç düşünmemiştim. Okurken kafamızdaki ses kimin sesi? Kendi sesimiz herhalde. Sesli kitapta o kayboluyor.

Kırk dakika konuştuk. Daha doğrusu o konuştu. Hangi kitapları sevdiğini, hangilerini bitiremediğini anlattı. Bir kitabı üç kez başlayıp üç kez bırakmış, dördüncüde bitirmiş ve çok sevmiş.

İneceği durakta kalktı, "iyi okumalar" dedi.

Ben kitabı açtım ama okuyamadım. Onun anlattıklarını düşündüm yol boyunca.

Sonra fark ettim: adını sormadım. Kırk dakika konuştuk, ben hiçbir şey sormadım. Sadece dinledim ve bu kolayıma geldi.

Bunu düşününce biraz kötü hissettim. Ama belki de o istediği buydu, bilmiyorum. Bazı insanlar sorulmasını değil dinlenmesini istiyor.

Kitabı o akşam bitirdim. Fena değildi ama o konuşma kadar aklımda kalmadı."""),

("aciklama", """Faiz ve enflasyon arasındaki ilişkiyi soranlar oluyor, basitçe anlatmaya çalışayım.

Elinizde yüz lira olduğunu düşünün. Bankaya koydunuz, yıllık yüzde kırk faiz veriyor. Yıl sonunda yüz kırk liranız oluyor. Kazandınız gibi görünüyor.

Ama aynı yıl fiyatlar yüzde elli arttıysa? Yıl başında yüz liraya aldığınız şey artık yüz elli lira. Yüz kırk liranızla o şeyi alamıyorsunuz. Yani nominal olarak kazandınız, gerçekte kaybettiniz.

İşte bu farka reel faiz deniyor. Kabaca faiz eksi enflasyon. Örnekte kırk eksi elli, yani eksi on. Negatif reel faiz.

Negatif reel faiz ortamında para tutmak zarar ettiriyor. İnsanlar bu yüzden parayı başka yerlere kaydırıyor: döviz, altın, gayrimenkul. Bu kaymanın kendisi de fiyatları etkiliyor.

Merkez bankalarının faizi artırmasının mantığı burada. Faiz yükselince para tutmak cazipleşiyor, harcama azalıyor, talep düşüyor, fiyat baskısı hafifliyor. Teorik olarak.

Pratikte gecikmeler var. Faiz kararının etkisi altı ay ile bir buçuk yıl arasında görülüyor. Bu yüzden bugünkü karar bugünkü enflasyona göre değil, gelecek tahminine göre alınıyor.

Tahmin tutmazsa karar da yanlış oluyor. Sık oluyor bu."""),

("dert", """Arabayı satmaya karar verdim ama karar vermek ile yapmak arasında bir ay geçti.

Sebep mantıklı: şehir içinde kullanmıyorum, park sorunu var, sigorta ve bakım masrafı duruyor. Hesapladım, taksi ve toplu taşımayla yılda daha az harcayacağım. Rakamlar net.

Ama bir ay boyunca ilan vermedim.

Sonra anladım, mesele araba değil. Araba bir seçenek demek. Canım isterse kalkıp gidebilirim demek. O seçeneği yılda iki kez kullanıyorum ama kullanabilme ihtimali önemliymiş benim için.

Bunu fark edince biraz rahatladım. Çünkü artık gerçek soruyu sorabiliyordum: yılda iki kullanım için bu parayı vermeye değer mi?

Cevabım hâlâ net değil. Kiralamak mümkün, hesap olarak ucuz. Ama kiralamak planlamayı gerektiriyor, "canım isterse" kısmı kayboluyor.

Şu an ilanı verdim. Arayan olmadı henüz. İçten içe aranmamasını istiyor muyum bilmiyorum.

Belki de bazı kararlar mantıkla alınmıyor. Alınıyor gibi yapıp erteliyoruz, sonra bir şey oluyor ve karar kendiliğinden gerçekleşiyor.

Bu arada sigortanın yenilenmesine iki ay var. O tarihe kadar satamazsam bir yıl daha ödemiş olacağım."""),

("ders", """Ders anlatırken en zor kısım ne biliyor musunuz? Bildiğiniz şeyi unutmak.

Bir konuyu iyi bildiğinizde, onu öğrenirken takıldığınız yerleri hatırlamıyorsunuz. Şimdi bakınca her şey bariz görünüyor. Öğrenci "anlamadım" dediğinde neyi anlamadığını çıkaramıyorsunuz, çünkü sizin için orada anlaşılmayacak bir şey yok.

Buna uzmanlık laneti deniyormuş, sonradan öğrendim.

Benim bulduğum çözüm not tutmak. Yeni bir şey öğrenirken takıldığım yerleri yazıyorum. Sonra o konuyu anlatırken o notlara bakıyorum. "Ha evet, ben de burada takılmıştım" diyorum.

İkinci yöntem: öğrenciye anlatmak yerine sordurtmak. Ben anlatınca kendi mantığımla gidiyorum. Onlar sorunca kendi mantıklarıyla geliyorlar ve boşluk nerede görüyorum.

Bir de şu: "anladınız mı" diye sormak işe yaramıyor. Herkes evet diyor. Bunun yerine küçük bir soru soruyorum, cevap veremiyorlarsa anlamamışlar demektir.

Yıllar sürdü bunları bulmam. Kimse öğretmedi. Belki öğretiliyor bir yerde, ben denk gelmedim.

Şimdi düşünüyorum, öğretmen yetiştirme programlarında bu anlatılıyor mudur acaba.

Bir de sınıf mevcudu meselesi var. On kişilik grupta bunların hepsi işliyor, kırk kişide hiçbiri işlemiyor."""),

("kayip", """Eski telefonun yedeği bozuktu ve iki yıllık fotoğraf gitti.

Fark etmem bir hafta sürdü. Yeni telefonu kurdum, her şey yerine geldi sandım. Sonra bir şey aradım, bulamadım. Tarihe göre baktım, belli bir aralık tamamen yok.

Önce panik, sonra kabullenme. Kurtarma servisine sordum, eski telefon çalışmıyorsa şansın düşük dediler.

İlginç olan şu: neyi kaybettiğimi tam bilmiyorum. Fotoğraf listesine bakamıyorum ki. Sadece o iki yılda çektiğim şeyleri hatırlamaya çalışıyorum ve hatırlayamıyorum. Zaten hatırlasam fotoğrafa ihtiyacım olmazdı.

Bir arkadaşım "belki iyi oldu" dedi. Sinirlendim önce. Sonra biraz düşündüm.

Fotoğrafların çoğuna zaten bakmıyordum. Çekiyorum, yükleniyor, bir daha açmıyorum. Yani saklıyordum ama kullanmıyordum. Kaybedince de bir şey değişmedi pratikte.

Yine de canım sıkkın. Birkaç tanesi vardı gerçekten önemli.

Şimdi iki ayrı yere yedekliyorum. Bir de ara sıra eski fotoğraflara bakıyorum. En azından bakayım, madem saklıyorum.

Bir arkadaşım bulut yedeklemesini önerdi ama aylık ücret var. Şimdilik harici diske kopyalıyorum, o da unutuluyor bazen."""),

("gozlem2", """Markette kasa sırası seçme konusunda insanların tuhaf bir davranışı var.

Herkes en kısa sıraya giriyor. Mantıklı görünüyor ama yanlış. Önemli olan sıradaki kişi sayısı değil, sepetlerin doluluğu. Üç kişilik sıra, sepetleri doluysa altı kişilikten uzun sürebiliyor.

Ben sepetlere bakıyorum, sayıya değil. Genelde işe yarıyor.

Ama bir istisna var: kasiyer hızı. Bunu dışarıdan göremiyorsunuz. Yavaş bir kasiyer tüm hesabı bozuyor. Birkaç kez sepetlere göre doğru seçim yapıp yine de geç kaldım.

Bir de kart sorunu, fiyat kontrolü gibi rastgele olaylar var. Öngörülemiyor.

Sonuç olarak optimize etmeye çalışmak çoğu zaman boşa emek. İki dakika kazanıyorsunuz belki.

Yine de yapıyorum. Neden yaptığımı düşündüm. Sanırım kontrol hissi veriyor. Sırada beklemek edilgen bir şey, seçim yapmak onu biraz etken kılıyor.

Yani mesele iki dakika değil. Mesele kendini çaresiz hissetmemek. Bunu anlayınca kendime biraz güldüm.

Self servis kasalar ayrı bir konu. Onlarda sıra kısa oluyor ama bir şey ters giderse görevli beklemek gerekiyor."""),

("proje", """Projeyi iptal ettik ve bunu doğru karar olarak görüyorum, gerekçelerimi yazayım.

Sekiz ay çalıştık. Ürün ortaya çıktı, çalışıyor, fena da değil. Ama kullanıcı sayısı hedefimizin onda biri.

İlk tepkimiz pazarlamayı suçlamak oldu. Belki yeterince duyurmadık. Bir ay daha deneyelim dedik. Denedik, değişmedi.

Sonra kullanıcılarla konuştuk. Asıl mesele orada çıktı. Çözdüğümüz sorun gerçekti ama insanlar için öncelikli değildi. "Güzel olmuş" diyorlardı, "ama ben bunu zaten Excel'de yapıyorum."

Excel'i rakip olarak hiç düşünmemiştik. Yetersiz bir araç bizim gözümüzde. Ama kullanıcı için yeterli, üstelik zaten açık.

Devam etme seçeneği vardı. Özellik ekler, farklılaşmaya çalışırdık. Altı ay daha, belki bir yıl.

Vazgeçtik. Sekiz ayı batırmış olduk ama on dört ayı kurtardık. Batık maliyet tuzağına düşmemek kolay değil, hele emek verilmişse.

Ekipten bazıları kırgın. Anlıyorum. Ben de kırgınım biraz.

Öğrendiğimiz şey şu: sorunun gerçek olması yetmiyor, acil de olması gerekiyor. Bunu sekiz ay önce sorabilirdik. Sormadık çünkü cevabı duymak istemiyorduk."""),

("mutfak", """Bulaşık makinesi almamakta direniyordum, aldım, haksız çıktım.

Argümanım şuydu: iki kişiyiz, bulaşık az, elde on dakikada bitiyor. Makine yer kaplıyor, su ve elektrik harcıyor, bir de kendisi temizlenmek istiyor.

Eşim ısrar etti, aldık.

Bir ay sonra itiraf ediyorum: haklıymış. Ama beklediğim sebepten değil.

Zaman tasarrufu gerçekten az. On dakikaydı, şimdi beş dakika yükleme. Büyük fark yok.

Fark başka yerde: bulaşık artık görünmüyor. Eskiden lavaboda birikirdi, ben "sonra yaparım" derdim, eşim rahatsız olurdu, tartışırdık. Şimdi makineye giriyor, tezgâh boş.

Yani makine bulaşığı değil, tartışmayı çözdü.

Bunu satın alırken kimse söylemiyor tabii. Broşürde su tasarrufu yazıyor, litre hesabı var. Asıl faydası ölçülemeyen şey.

Su konusunda da yanılmışım bu arada. Elde yıkarken musluğu açık bırakıyormuşum, makine daha az harcıyor. Ölçtüm.

Yer meselesi hâlâ geçerli ama. Mutfak küçüldü, bu doğru.

Deterjan meselesine de girmedim. Tablet mi toz mu tartışması var, ikisini de denedim, belirgin fark göremedim."""),

("vazgectim", """Blog yazmayı bıraktım. Dört yıl yazdım, son altı aydır yazmıyorum ve artık resmen bitti diyebilirim.

Sebep okunmaması değil. Okunuyordu, az ama istikrarlı. Yorum gelirdi, birkaç kişi düzenli takip ederdi.

Sebep şu: yazacak bir şeyim kalmadı. Bunu kabul etmek uzun sürdü. Bir süre zorlayarak yazdım, ortaya vasat yazılar çıktı. Kendim de beğenmiyordum.

Aslında ilk iki yılda söyleyeceklerimi söylemişim. Sonraki iki yıl aynı şeyleri farklı kelimelerle tekrarlamışım. Geriye dönüp okuyunca görüyorum.

Bu utanç verici değil sanırım. Herkesin söyleyeceği belli sayıda şey var belki.

Şimdi ne yapıyorum? Okuyorum. Yazmadığım altı ayda dört yılın toplamından fazla okudum. Belki yazmak okumaya engel oluyordu, sürekli "bunu nasıl yazarım" diye düşünüyordum.

Bir gün tekrar başlar mıyım bilmiyorum. Yeni bir şey öğrenirsem belki.

Siteyi kapatmadım. Orada dursun, kimseye zararı yok.

Alan adının süresi gelecek yıl doluyor. Uzatır mıyım bilmiyorum, muhtemelen uzatırım, ucuz bir şey sonuçta."""),

("haber-ai", """Kentteki toplu taşıma ağının genişletilmesine yönelik çalışmaların bu yıl içinde başlayacağı bildirildi. Yetkililer, projenin özellikle yeni yerleşim bölgelerine hizmet vereceğini belirtti.

Yapılan açıklamada, mevcut hatların kapasitesinin nüfus artışını karşılamakta yetersiz kaldığı ifade edildi. Yoğun saatlerde yaşanan sıkışıklığın azaltılması için sefer sıklığının da artırılacağı kaydedildi.

Projenin çevresel etki değerlendirme sürecinin tamamlandığı, olumsuz bir bulguya rastlanmadığı açıklandı. Güzergâh belirlenirken yeşil alanların korunmasına özen gösterildiği vurgulandı.

Finansman modeline ilişkin çalışmaların sürdüğü belirtildi. Uluslararası kaynaklardan destek sağlanması seçeneğinin değerlendirildiği aktarıldı.

Bölge sakinleri, çalışmaların bir an önce tamamlanmasını beklediklerini dile getirdi. Yetkililer ise takvime uyulacağı konusunda güvence verdi. Tamamlandığında günlük yüz binlerce yolcuya hizmet verilmesi bekleniyor.

Ulaşım uzmanları, hat genişletmesinin tek başına yeterli olmayacağını değerlendirmektedir. Aktarma noktalarının yeniden düzenlenmesi ve bilet sisteminin bütünleştirilmesi de gündemdedir. Yetkililer bu konudaki çalışmaların ayrı bir program kapsamında yürütüldüğünü bildirdi. Güzergâh üzerindeki esnaf için geçiş dönemine yönelik önlemlerin değerlendirildiği kaydedildi."""),

("haber-ai", """Tarım sektöründe dijital teknolojilerin kullanımına yönelik destek programının başvuru süreci başladı. Program kapsamında üreticilere hem eğitim hem finansal destek sağlanacağı bildirildi.

Yetkililer, akıllı sulama sistemleri ve toprak analizi teknolojilerinin verimliliği artırdığını belirtti. Pilot uygulamalarda su tüketiminde kayda değer azalma gözlendiği ifade edildi.

Başvuru kriterleri arasında işletme büyüklüğü ve üretim çeşidinin yer aldığı kaydedildi. Küçük ölçekli üreticilere öncelik tanınacağı açıklandı.

Programın ilk aşamasında belirli bölgelerde uygulanacağı, sonuçlara göre kapsamın genişletileceği bildirildi. Değerlendirme sürecinin şeffaf biçimde yürütüleceği vurgulandı.

Sektör temsilcileri düzenlemeyi olumlu karşıladıklarını belirtti. Ancak teknik destek hizmetlerinin süreklilik göstermesi gerektiğine dikkat çekildi. Başvuruların önümüzdeki ay sonuna kadar kabul edileceği duyuruldu.

Uygulamanın izlenmesi için ayrı bir birim oluşturulduğu açıklandı. Destek alan işletmelerin verimlilik göstergeleri düzenli olarak kayıt altına alınacak, elde edilen veriler program tasarımının güncellenmesinde kullanılacaktır. Yetkililer, sonuçların kamuoyuyla paylaşılacağını belirtti. Başvuru koşullarına ilişkin ayrıntılı bilgiye resmî internet sitesinden ulaşılabileceği duyuruldu.

Sektör temsilcileri, uygulamanın yaygınlaştırılması hâlinde üretim maliyetlerinde kalıcı düşüş sağlanabileceğini değerlendirmektedir."""),

("haber-ai", """Sağlık alanında yürütülen aşılama kampanyasının hedeflenen orana ulaştığı açıklandı. Yetkililer, çalışmaların planlanan takvime uygun şekilde tamamlandığını bildirdi.

Kampanya kapsamında özellikle risk grubundaki bireylere öncelik verildiği belirtildi. Mobil sağlık ekipleri aracılığıyla kırsal bölgelere erişim sağlandığı kaydedildi.

Bilgilendirme faaliyetlerinin katılım oranını artırmada etkili olduğu değerlendirildi. Yerel yöneticiler ve muhtarların sürece desteğinin belirleyici olduğu ifade edildi.

Soğuk zincir koşullarının her aşamada korunduğu, denetimlerin düzenli olarak yapıldığı açıklandı. Herhangi bir aksaklık yaşanmadığı bildirildi.

Önümüzdeki dönemde izleme çalışmalarının sürdürüleceği duyuruldu. Vatandaşlara düzenli sağlık kontrollerini ihmal etmemeleri çağrısında bulunuldu.

Kampanya süresince yürütülen iletişim çalışmalarının ayrıca değerlendirileceği bildirildi. Yanlış bilgilendirmeyle mücadele kapsamında sağlık çalışanlarına yönelik rehber materyal hazırlandığı ifade edildi. Yetkililer, toplumsal bağışıklık düzeyinin korunması için düzenli tekrar dozlarının önemine dikkat çekti. İzleme verilerinin önümüzdeki dönemde raporlanacağı açıklandı.

Yetkililer ayrıca, bölgesel farklılıkların giderilmesine yönelik ek planlamaların gündemde olduğunu, saha ekiplerinin görevlendirmesinin bu doğrultuda yeniden düzenleneceğini bildirdi."""),

("kurumsal-ai", """Enerji verimliliği politikamız kapsamında yürüttüğümüz çalışmaların sonuçlarını paydaşlarımızla paylaşmaktan memnuniyet duyarız. Bu alandaki taahhütlerimiz kararlılıkla sürdürülmektedir.

Tesislerimizde gerçekleştirilen iyileştirmeler sonucunda birim üretim başına enerji tüketiminde azalma sağlanmıştır. Aydınlatma sistemlerinin yenilenmesi ve ısı geri kazanım uygulamaları bu sonuçta belirleyici olmuştur.

Yenilenebilir enerji kaynaklarının toplam tüketimimizdeki payı kademeli olarak artırılmaktadır. Çatı üstü güneş enerjisi kurulumları devreye alınmış, ek yatırımlar planlanmaktadır.

İzleme altyapımız güçlendirilmiştir. Enerji tüketimi noktasal olarak ölçülmekte, sapmalar erken aşamada tespit edilebilmektedir.

Çalışanlarımıza yönelik farkındalık programları düzenlenmiştir. Katılım oranları hedeflenen düzeyde gerçekleşmiştir.

Önümüzdeki dönemde belirlenen hedeflere ulaşılması öngörülmektedir. Paydaşlarımızın görüş ve önerilerini her zaman değerli bulduğumuzu belirtmek isteriz.

Tedarikçilerimizle yürütülen ortak çalışmalar da bu kapsamda değerlendirilmektedir. Lojistik süreçlerinde rota optimizasyonu uygulamaları hayata geçirilmiş, taşıma kaynaklı salımlarda azalma sağlanmıştır. Ölçüm yöntemlerimiz bağımsız kuruluşlar tarafından doğrulanmaktadır. Elde edilen sonuçlar yıllık sürdürülebilirlik raporumuzda ayrıntılı biçimde yer almaktadır.

Hedeflerimizin gözden geçirilmesi yıllık olarak yapılmakta, sapmalar tespit edildiğinde düzeltici eylem planları devreye alınmaktadır."""),

("kurumsal-ai", """Müşteri deneyimi stratejimizin gözden geçirilmesi tamamlanmış bulunmaktadır. Elde edilen bulgular ve atılacak adımlar aşağıda özetlenmiştir.

Hizmet kanallarımız arasındaki bütünlüğün güçlendirilmesi öncelikli alan olarak belirlenmiştir. Farklı kanallardan gelen taleplerin tek bir yapıda izlenmesi, çözüm sürelerini kısaltacaktır.

Geri bildirim toplama yöntemlerimiz çeşitlendirilmiştir. Anket temelli ölçümlere ek olarak, işlem sonrası değerlendirmeler devreye alınmıştır. Bu sayede daha güncel veriye ulaşılmaktadır.

Çalışan yetkinliklerinin geliştirilmesi kapsamında eğitim programları güncellenmiştir. Sahada karşılaşılan örnek durumlar üzerinden yürütülen uygulamalı çalışmalar olumlu geri dönüş almıştır.

Süreç iyileştirme çalışmalarında veri odaklı bir yaklaşım benimsenmiştir. Darboğaz oluşturan adımlar tespit edilmiş, sadeleştirme çalışmaları başlatılmıştır.

Şeffaf iletişim ilkemiz doğrultusunda gelişmeleri düzenli olarak paylaşmayı sürdüreceğiz.

Dijital kanallarımızda erişilebilirlik standartlarına uyum çalışmaları sürdürülmektedir. Ekran okuyucu uyumluluğu ve renk karşıtlığı gereksinimleri gözden geçirilmiş, tespit edilen eksiklikler giderilmiştir. Bu düzenlemelerin tüm kullanıcılar için deneyimi iyileştirdiği değerlendirilmektedir. Geri bildirimleriniz doğrultusunda gelişmeye devam edeceğimizi belirtmek isteriz.

Uygulama takvimimiz çeyrek dönemler hâlinde planlanmış olup, ilerleme durumu düzenli aralıklarla paydaşlarımızla paylaşılacaktır."""),

("kurumsal-ai", """Risk yönetimi çerçevemizin yıllık değerlendirmesi tamamlanmıştır. Süreç, bağımsız denetim bulguları dikkate alınarak yürütülmüştür.

Operasyonel riskler kategorize edilerek önceliklendirilmiştir. Yüksek etkili risk alanları için azaltıcı kontroller tanımlanmış, sorumluluklar netleştirilmiştir.

İş sürekliliği planlarımız güncellenmiştir. Kritik süreçler için alternatif çalışma senaryoları hazırlanmış, tatbikatlar gerçekleştirilmiştir. Tespit edilen iyileştirme alanları planlara yansıtılmıştır.

Tedarik zinciri kaynaklı riskler ayrı bir başlık altında değerlendirilmiştir. Tek kaynağa bağımlılığın azaltılması yönündeki çalışmalar sürdürülmektedir.

Bilgi güvenliği alanındaki kontroller düzenli testlerden geçirilmektedir. Çalışan farkındalığının güvenlik zincirindeki belirleyici rolü göz önünde bulundurularak eğitimler zorunlu tutulmuştur.

Raporlama mekanizmalarımız güçlendirilmiştir. Risk göstergeleri yönetim kuruluna düzenli olarak sunulmaktadır.

Mevzuat uyumu ayrı bir izleme başlığı olarak ele alınmaktadır. İlgili düzenlemelerdeki değişiklikler takip edilmekte, etki analizleri ilgili birimlerle paylaşılmaktadır. Uyum riskine ilişkin bulgular denetim komitesine düzenli olarak raporlanmaktadır. Çerçevenin bir sonraki gözden geçirmesinin önümüzdeki yıl gerçekleştirilmesi planlanmaktadır.

Ayrıca iklim kaynaklı fiziksel ve geçiş risklerinin çerçeveye dâhil edilmesine yönelik hazırlık çalışmaları başlatılmış, ilk değerlendirme raporu hazırlanmıştır."""),

("akademik-ai", """Şehir içi ulaşım planlamasında talep yönetimi yaklaşımı, altyapı yatırımlarına alternatif bir çerçeve sunmaktadır. Bu yaklaşım, kapasite artırımı yerine mevcut kapasitenin daha verimli kullanılmasını hedeflemektedir.

Yol kapasitesinin artırılmasının uzun vadede trafiği azaltmadığı, aksine ek talep yarattığı çeşitli çalışmalarda ortaya konmuştur. Bu olgu literatürde uyarılmış talep olarak adlandırılmaktadır.

Talep yönetimi araçları arasında fiyatlandırma mekanizmaları öne çıkmaktadır. Yoğunluk ücretlendirmesi uygulayan kentlerde merkez trafiğinde azalma gözlenmiştir. Ancak bu uygulamaların gelir dağılımı üzerindeki etkileri tartışma konusudur.

Toplu taşımanın çekiciliğinin artırılması tamamlayıcı bir stratejidir. Sefer sıklığı ve güvenilirlik, kullanıcı tercihlerini fiyattan daha fazla etkileyebilmektedir.

Esnek çalışma düzenlerinin yaygınlaşması, zirve saat yoğunluğunu azaltma potansiyeli taşımaktadır. Bu etkinin kalıcılığı henüz yeterince incelenmemiştir.

Sonuç olarak, tek bir araca dayanan politikalar sınırlı sonuç vermektedir. Araçların birbirini destekleyecek biçimde tasarlanması gerekmektedir.

Ölçme yöntemlerine ilişkin sınırlılıklar da belirtilmelidir. Trafik akışı verileri genellikle belirli noktalardan toplanmakta, bu da kentin bütününe genelleme yapmayı güçleştirmektedir. Mobil konum verilerinin kullanımı daha kapsamlı bir resim sunmakla birlikte mahremiyet açısından soru işaretleri doğurmaktadır. Yöntem seçiminin bulguları etkilediği göz önünde bulundurulmalıdır."""),

("akademik-ai", """Dil edinim sürecinde girdi niteliğinin rolü, uygulamalı dilbilim alanının temel tartışma konularından biridir. Öğrenicinin maruz kaldığı dilsel verinin miktarı kadar niteliği de belirleyici görülmektedir.

Anlaşılabilir girdi kavramı, öğrenicinin mevcut düzeyinin bir miktar üzerinde bulunan materyali ifade etmektedir. Bu düzeyin altındaki girdi gelişim sağlamamakta, çok üzerindeki girdi ise işlenememektedir.

Etkileşimin rolü ayrıca vurgulanmaktadır. Anlam müzakeresi içeren karşılıklı iletişim, tek yönlü maruz kalmaya kıyasla daha güçlü sonuçlar üretmektedir. Öğrenici anlaşılmadığında yaptığı düzeltmeler, dilsel yapıların pekişmesine katkı sağlamaktadır.

Çıktı üretiminin işlevi de göz ardı edilmemelidir. Üretim sırasında karşılaşılan güçlükler, öğrenicinin bilgi boşluklarını fark etmesini sağlamaktadır.

Bireysel farklılıklar süreci etkileyen bir diğer boyuttur. Güdülenme düzeyi, kaygı ve öğrenme stratejileri edinim hızında farklılaşmaya yol açmaktadır.

Özetle, dil edinimi tek bir değişkenle açıklanamayacak kadar çok boyutlu bir süreçtir. Öğretim tasarımlarının bu karmaşıklığı gözetmesi beklenmektedir.

Yaş faktörü de sıklıkla tartışılan bir değişkendir. Erken yaşta başlayan edinimde sesletim açısından avantaj gözlenmekle birlikte, sözdizimsel gelişimde yetişkin öğrenicilerin hızlı ilerleyebildiği bildirilmektedir. Bu bulgular kritik dönem varsayımının mutlak biçimde yorumlanmaması gerektiğine işaret etmektedir. Alanda uzlaşı henüz sağlanmamıştır."""),

("akademik-ai", """Kooperatif örgütlenme modeli, küçük ölçekli üreticilerin piyasa karşısındaki pazarlık gücünü artırmaya yönelik bir mekanizma olarak değerlendirilmektedir. Model, ortak alım ve satım yoluyla ölçek ekonomisi sağlamayı amaçlamaktadır.

Tarım sektöründeki uygulamalar bu potansiyeli kısmen doğrulamaktadır. Ortak girdi temini maliyetleri düşürmekte, ortak pazarlama ise aracı sayısını azaltmaktadır. Üretici geliri üzerindeki etki olumlu yönde gözlenmektedir.

Ancak modelin başarısı yönetişim kalitesine bağlıdır. Karar süreçlerinde şeffaflığın sağlanamadığı yapılarda üye bağlılığı zayıflamaktadır. Denetim mekanizmalarının işlerliği bu açıdan belirleyicidir.

Finansmana erişim yaygın bir kısıt oluşturmaktadır. Kooperatiflerin teminat yapısı geleneksel kredi değerlendirme ölçütleriyle uyuşmamakta, bu da sermaye ihtiyacının karşılanmasını güçleştirmektedir.

Ölçek büyüdükçe ortaya çıkan koordinasyon maliyetleri de dikkate alınmalıdır. Üye sayısı arttıkça karar alma süreçleri yavaşlayabilmektedir.

Sonuç olarak, kooperatif modeli tek başına yeterli bir çözüm değildir. Destekleyici politika çerçevesi olmadan sürdürülebilirliği sınırlı kalmaktadır.

Karşılaştırmalı çalışmalar, hukuki çerçevenin belirleyici olduğunu göstermektedir. Ortaklık yapısının ve kâr dağıtım kurallarının açık biçimde tanımlandığı ülkelerde kooperatiflerin ömrü daha uzun olmaktadır. Vergi düzenlemelerinin de model tercihini etkilediği gözlenmektedir. Bu nedenle politika tasarımında ülkeye özgü koşulların dikkate alınması gerekmektedir."""),
]


def rows():
    return [{"text": " ".join(t.split()), "label": 1, "lang": "tr",
             "source": "claude-hard/" + k, "attack": "none"} for k, t in SAMPLES]


if __name__ == "__main__":
    import json, os, collections
    rs = rows()
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "data", "ai_tr_hidden.jsonl")
    with open(path, "w", encoding="utf-8") as f:
        for r in rs:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    ws = [len(r["text"].split()) for r in rs]
    print("  -> ai_tr_hidden.jsonl (%d kayit)" % len(rs))
    print("     kelime: min %d / ort %d / max %d" % (min(ws), sum(ws)//len(ws), max(ws)))
    print("     >=140 kelime olan: %d" % sum(1 for w in ws if w >= 140))
