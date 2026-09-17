# -*- coding: utf-8 -*-
"""Turkce AI metin ornekleri — UZUN set, parti 4.

NEDEN: Turkce olcum setinde yalnizca 27 ornek vardi. eval/calibrate.py bu
darliktan oturu "isotonic atlandi — yalnizca 7 farkli deger" uyarisi
veriyordu: 27 ornek, kalibrasyon egrisini cizmeye yetmiyor ve esik kaba bir
adim fonksiyonuna donusuyor. Bu parti olcum setini genisletir.

AYRIM UYARISI: bu dosya OLCUM setine gider (data/ai_tr.jsonl). Gizlenmis
katmanin egitim verisi ayridir (eval/ai_tr_hidden.py -> ai_tr_hidden.jsonl).
Ikisi karistirilirsa katman kendi egitim verisi uzerinde olculur ve
raporlanan dogruluk gercek disi cikar.

Ornekler 150-200 kelime araliginda; olcum bandi (140) rahatca asiliyor.
Onceki partiler 250+ tutulmustu, bu parti ornek SAYISINI artirmaya odaklandi:
kalibrasyon egrisi icin belirleyici olan uzunluk degil, farkli skor sayisi.
"""

SAMPLES = [
("akademik", """Mikroplastik kirliliği, son yıllarda çevre bilimlerinin öncelikli araştırma konularından biri haline gelmiştir. Beş milimetreden küçük plastik parçacıkları ifade eden bu kavram, hem birincil hem ikincil kaynaklardan beslenmektedir. Birincil mikroplastikler doğrudan küçük boyutlarda üretilirken, ikincil olanlar büyük plastik atıkların parçalanmasıyla oluşmaktadır.

Deniz ekosistemleri bu kirlilikten en fazla etkilenen alanlar arasındadır. Yapılan araştırmalar, okyanus yüzeyinden derin deniz tabanına kadar geniş bir alanda mikroplastik varlığını ortaya koymuştur. Deniz canlıları bu parçacıkları besin zannederek tüketmekte ve bu durum sindirim sistemlerinde tıkanıklıklara yol açabilmektedir.

Besin zinciri yoluyla taşınma, sorunun en endişe verici boyutunu oluşturmaktadır. Küçük organizmalar tarafından alınan parçacıklar, zincirin üst basamaklarına doğru birikmektedir. İnsan tüketimine sunulan deniz ürünlerinde mikroplastik tespit edilmesi, halk sağlığı açısından soru işaretleri doğurmaktadır.

Kara ekosistemlerindeki durum da göz ardı edilmemelidir. Tarım alanlarında kullanılan arıtma çamurları ve plastik örtüler, toprağa mikroplastik girişine neden olmaktadır. Bu parçacıkların toprak mikroorganizmaları üzerindeki etkileri henüz yeterince aydınlatılmamıştır.

Mücadele stratejileri açısından kaynakta önleme yaklaşımı öne çıkmaktadır. Tek kullanımlık plastiklerin sınırlandırılması, atık yönetim sistemlerinin güçlendirilmesi ve arıtma tesislerinde filtrasyon teknolojilerinin geliştirilmesi bu kapsamda değerlendirilmektedir.

Sonuç olarak, mikroplastik kirliliği disiplinler arası bir yaklaşım gerektiren karmaşık bir sorundur. Etkilerinin tam olarak anlaşılabilmesi için uzun vadeli izleme çalışmalarına ihtiyaç duyulmaktadır. Politika yapıcıların bu alandaki bilimsel bulguları düzenlemelere yansıtması büyük önem taşımaktadır."""),

("akademik", """Uzaktan eğitim modeli, teknolojik altyapının gelişmesiyle birlikte yükseköğretimde giderek yaygınlaşan bir uygulama alanı bulmuştur. Geleneksel yüz yüze eğitimin mekân ve zaman kısıtlarını ortadan kaldıran bu model, erişilebilirlik açısından önemli avantajlar sunmaktadır.

Modelin en belirgin katkısı, coğrafi engellerin aşılmasıdır. Kırsal bölgelerde yaşayan veya çalışma hayatı nedeniyle kampüse gelemeyen bireyler, eğitim olanaklarından yararlanabilmektedir. Bu durum, yaşam boyu öğrenme anlayışının yaygınlaşmasına katkı sağlamaktadır.

Ancak modelin sınırlılıkları da dikkate alınmalıdır. Öğrenci-öğretim elemanı etkileşiminin azalması, öğrenme sürecinin niteliğini etkileyebilmektedir. Yüz yüze ortamda kendiliğinden gerçekleşen soru-cevap alışverişi, çevrim içi ortamda planlanmayı gerektirmektedir.

Değerlendirme süreçleri ayrı bir zorluk alanı oluşturmaktadır. Sınav güvenliğinin sağlanması, uzaktan eğitimin en çok tartışılan boyutlarından biridir. Bu kapsamda geliştirilen gözetim yazılımları, mahremiyet açısından eleştiri konusu olmaktadır.

Dijital eşitsizlik meselesi de göz ardı edilmemelidir. İnternet erişimi ve uygun cihaza sahip olmayan öğrenciler, modelden eşit ölçüde yararlanamamaktadır. Bu durum, eğitimde fırsat eşitliği hedefiyle çelişen sonuçlar doğurabilmektedir.

Karma modeller, iki yaklaşımın güçlü yönlerini birleştirme potansiyeli taşımaktadır. Teorik içeriğin çevrim içi sunulması, uygulama derslerinin yüz yüze yürütülmesi dengeli bir çözüm olarak değerlendirilmektedir.

Özetle, uzaktan eğitim geleneksel modelin yerine geçen değil, onu tamamlayan bir yapı olarak konumlandırıldığında en verimli sonuçları vermektedir. Kurumların bu doğrultuda strateji geliştirmesi beklenmektedir."""),

("akademik", """Kültürel miras alanlarının korunması, turizm gelirleri ile koruma ilkeleri arasında hassas bir denge gerektirmektedir. Bu iki hedef zaman zaman çatışabilmekte, kısa vadeli ekonomik kazanç uzun vadeli koruma amacının önüne geçebilmektedir.

Ziyaretçi yoğunluğu, fiziksel yıpranmanın başlıca nedenlerinden biridir. Tarihî yapılarda artan insan trafiği, zemin aşınmasından nem dengesinin bozulmasına kadar çeşitli sorunlara yol açmaktadır. Bazı alanlarda günlük ziyaretçi sayısına sınır getirilmesi bu nedenle gündeme gelmiştir.

Çevresel faktörler de koruma çalışmalarını güçleştirmektedir. Hava kirliliği, taş yüzeylerde kimyasal bozunmaya neden olmaktadır. İklim değişikliğine bağlı aşırı hava olayları, özellikle açık alandaki kalıntılar için risk oluşturmaktadır.

Restorasyon uygulamalarında özgünlük ilkesi belirleyici olmalıdır. Kullanılan malzemelerin özgün yapıyla uyumlu olması, müdahalelerin geri döndürülebilir nitelikte tasarlanması uluslararası koruma belgelerinde vurgulanmaktadır. Aceleci ve belgelenmemiş müdahaleler, korunmak istenen değerin kaybına yol açabilmektedir.

Yerel halkın sürece katılımı, sürdürülebilir koruma açısından kritik öneme sahiptir. Miras alanını kendi kimliğinin parçası olarak gören topluluklar, koruma çabalarının doğal savunucusu haline gelmektedir. Buna karşılık dışlanmış topluluklar, alanı bir kısıtlama kaynağı olarak algılayabilmektedir.

Dijital belgeleme teknolojileri, bu alanda umut verici olanaklar sunmaktadır. Üç boyutlu tarama yöntemleriyle oluşturulan kayıtlar, olası bir kayıp durumunda referans niteliği taşımaktadır.

Sonuç olarak, koruma ve kullanım arasındaki dengenin her alan için ayrı ayrı kurgulanması gerekmektedir. Genel geçer reçeteler yerine alana özgü yönetim planları daha etkili sonuçlar üretmektedir."""),

("akademik", """Bağımsız merkez bankacılığı kavramı, para politikasının siyasi döngülerden yalıtılması amacıyla geliştirilmiş kurumsal bir düzenlemedir. Bu yaklaşımın temelinde, kısa vadeli siyasi kaygıların uzun vadeli fiyat istikrarı hedefini zayıflatabileceği varsayımı bulunmaktadır.

Teorik çerçeve, zaman tutarsızlığı sorunuyla açıklanmaktadır. Seçim dönemlerinde genişletici politika uygulama eğilimi, kısa vadede büyümeyi desteklerken orta vadede enflasyonist baskı yaratmaktadır. Bağımsız bir otoritenin bu baskıya direnebileceği öngörülmektedir.

Ampirik çalışmalar, bağımsızlık düzeyi ile enflasyon oranları arasında negatif bir ilişki bulunduğunu göstermektedir. Ancak bu ilişkinin nedenselliği tartışmalıdır. Güçlü kurumsal yapıya sahip ülkelerde hem merkez bankası bağımsızlığının hem düşük enflasyonun ortak bir nedenden kaynaklanıyor olması mümkündür.

Bağımsızlığın sınırları da tartışma konusudur. Seçilmemiş bir kurumun ekonomik sonuçları belirgin biçimde etkileyen kararlar alması, demokratik hesap verebilirlik açısından soru işaretleri doğurmaktadır. Bu nedenle şeffaflık mekanizmaları, bağımsızlığın tamamlayıcısı olarak görülmektedir.

Kriz dönemleri, çerçevenin sınandığı zamanlardır. Olağanüstü koşullarda uygulanan geleneksel olmayan politika araçları, merkez bankalarının görev alanını genişletmiştir. Bu genişleme, maliye politikasıyla sınırların bulanıklaşması eleştirisini beraberinde getirmiştir.

Gelişmekte olan ülkelerde tablo daha karmaşıktır. Döviz kuru istikrarı, finansal derinliğin sınırlılığı ve dışsal şoklara açıklık, para politikasının hareket alanını daraltmaktadır.

Sonuç olarak, bağımsızlık tek başına yeterli bir koşul değildir. Kurumsal kapasite, iletişim politikası ve mali disiplinle desteklenmediğinde beklenen sonuçları vermemektedir."""),

("akademik", """Antibiyotik direnci, modern tıbbın karşı karşıya olduğu en ciddi tehditlerden biri olarak değerlendirilmektedir. Mikroorganizmaların kendilerini hedef alan ilaçlara karşı dayanıklılık geliştirmesi, tedavi edilebilir enfeksiyonların yeniden ölümcül hale gelmesi riskini taşımaktadır.

Direncin gelişim mekanizması evrimsel bir süreçtir. Antibiyotik uygulaması, duyarlı bakterileri elimine ederken dirençli olanların çoğalmasına olanak tanımaktadır. Bu seçilim baskısı, dirençli suşların popülasyon içindeki payını artırmaktadır.

Gereksiz kullanım, süreci hızlandıran başlıca etkendir. Viral enfeksiyonlarda antibiyotik reçetelenmesi, tıbbi açıdan yararsız olmakla birlikte direnç gelişimine katkıda bulunmaktadır. Hastaların tedaviyi yarıda bırakması da benzer şekilde riskli bir davranıştır.

Tarım ve hayvancılık sektöründeki kullanım ayrı bir boyut oluşturmaktadır. Büyümeyi hızlandırma amacıyla yapılan uygulamalar, dirençli suşların gıda zinciri yoluyla insanlara geçmesine zemin hazırlamaktadır. Birçok ülke bu kullanımı kısıtlayan düzenlemeler getirmiştir.

Yeni antibiyotik geliştirme süreci ise yavaş ilerlemektedir. Araştırma maliyetlerinin yüksekliği ve beklenen ticari getirinin sınırlılığı, ilaç şirketlerinin bu alana yatırımını azaltmıştır. Kamu destekli araştırma programları bu boşluğu doldurmaya çalışmaktadır.

Enfeksiyon kontrolü, direnç yayılımını sınırlamada etkili bir araçtır. Hastane ortamında el hijyeni uygulamaları ve izolasyon protokolleri, dirençli suşların bulaşını önemli ölçüde azaltmaktadır.

Sonuç olarak, antibiyotik direnci tek bir sektörün çözebileceği bir sorun değildir. Tıp, veterinerlik, tarım ve çevre alanlarını kapsayan bütüncül bir yaklaşım gerekmektedir."""),

("zor-negatif", """Annemin dikiş makinesi hâlâ çalışıyor. Kırk yıllık falan, o zamanlar çeyiz olarak almışlar. Geçen ay perdeleri kısaltmak gerekti, indirdim dolaptan.

Çalıştırmayı bilmiyordum açıkçası. Çocukken izlerdim ama hiç denememiştim. Annemi aradım, telefonda anlattı. İpliği nereden geçireceğim, masuranın nasıl takıldığı falan. Yarım saat sürdü.

İlk dikişim eğri çıktı. İkincisi de. Üçüncüde biraz düzeldi. Perde zaten aşağı sarkıyor, eğrilik görünmüyor çok. Kendimi kandırıyor olabilirim ama idare eder.

İlginç olan şu: makine bozulmamış. Kırk yıl önce yapılmış bir şey, hiç servise gitmemiş, hâlâ iş görüyor. Geçen yıl aldığım tost makinesi on ay dayandı.

Bunu anneme söyledim, güldü. "Eskiden sağlam yapıyorlardı" dedi. Klasik cümle ama bu durumda doğru galiba.

Öte yandan makine ağır. Çok ağır. Dolaptan indirirken belim tutuldu neredeyse. Yeni olanlar hafif ve taşınabiliyor. Yani sağlamlığın bir bedeli var, o da ağırlık.

Şimdi düşünüyorum da, belki bazı şeyleri elimizde tutmak gerekiyor. Atmadan önce bir daha bakmak. Bu makine yirmi yıl dolapta durdu, sonra bir gün lazım oldu.

Ama her şeyi de saklayamayız tabii. Ev o kadar büyük değil. Nerede duracağını bilmek lazım sanırım. Ben bilmiyorum.

Perde işi bitti neyse. Makineyi dolaba geri koydum. Belki yirmi yıl daha orada durur."""),

("zor-negatif", """Kahve içmeyi bıraktım. Üç hafta oldu. Yazayım bakalım ne oldu.

Sebep basit: uyuyamıyordum. Gece yatağa giriyorum, kafam çalışıyor. Sabaha kadar dönüp duruyorum. Doktor sordu günde kaç kahve içtiğimi, saydım, beş oluyormuş. Beşinciyi de saat dörtte falan içiyorum.

İlk üç gün berbat geçti. Baş ağrısı sürekli. İş yapamadım neredeyse. Ekrana bakıyorum, kelimeler anlam ifade etmiyor. Bir kere pes edip içecektim, arkadaşım "üç gün dayan" dedi, dayandım.

Dördüncü gün düzeldi. Aniden. Sabah kalktım, baş ağrısı yok. Garip bir his, sanki bir şey eksik ama kötü değil.

Şu an durum şöyle: uyku düzeldi. Gerçekten düzeldi, abartmıyorum. On buçukta yatıyorum, on dakikada uyuyorum. Yıllardır olmayan bir şeydi bu.

Ama enerji konusunda kayıp var. Eskiden sabah kahveyle hızlı başlıyordum, şimdi ısınmam bir saat sürüyor. Öğleden sonra da bir düşüş oluyor. Yürüyüş yapıyorum o saatte, biraz işe yarıyor.

Tadını özlüyorum en çok. Kokusunu. Ofiste biri demlediğinde dönüp bakıyorum hâlâ.

Tamamen bırakacak mıyım bilmiyorum. Belki sabah bir tane içerim ileride. Şimdilik devam edeyim, biraz daha göreyim.

Tavsiye eder miyim? Uykunuz bozuksa evet. Yoksa gerek yok bence, ben abartmışım zaten."""),

("zor-negatif", """Komşumuz taşındı geçen hafta. Altı yıldır yan dairedeydi. Pek konuşmazdık, merhaba selam.

Taşınma günü koridorda karşılaştık. Kutular vardı etrafta. Bir şey söylemek gerekti, "hayırlı olsun" dedim. Teşekkür etti. Sonra bir sessizlik oldu.

Sonra o konuştu. Nereye gittiğini anlattı, işi değişmiş, başka şehir. Ben de bir şeyler söyledim. Yaklaşık on dakika konuştuk. Altı yılda toplam konuştuğumuzdan fazla.

Giderken "iyi komşuydunuz" dedi. Ben de aynısını söyledim. İkimiz de doğruyu söylüyorduk aslında ama garip bir doğruydu. Birbirimizi tanımıyorduk. İyi komşu olmak tanımayı gerektirmiyor galiba, sadece rahatsız etmemeyi.

Şimdi daire boş. Duvarın arkasından ses gelmiyor. Fark etmemişim ama meğer ses geliyormuş sürekli, televizyon falan. Şimdi sessizlik var ve bu sessizlik dikkat çekiyor.

Yeni biri gelecek tabii. Belki gürültücü olur, belki olmaz. Şansa kalmış.

Bir de şunu düşündüm: benim hakkımda da aynı şeyi söyleyecekler bir gün. "İyi komşuydu." Adımı hatırlarlar mı bilmiyorum. Ben komşunun adını hatırlıyorum ama soyadını bilmiyordum mesela. Zarflara bakıp öğrenirdim posta kutusunda.

Neyse. Altı yıl böyle geçti işte."""),

("zor-negatif", """Telefonumu iki gün evde unuttum. Kasten değil, tatilde çantaya koymayı unutmuşum.

İlk saat panik. Sürekli cebime atıyorum elimi. Yok tabii. Sonra kabullendim.

İlginç olan şu: rahatsızlık geçti ama yerine tuhaf bir şey geldi. Sıkılmak. Uzun zamandır sıkılmamışım meğer. Sırada beklerken, otobüste, yemekten sonra — bu boşluklar hep telefonla doluyormuş.

İkinci gün alıştım. Kitap okudum biraz. Dışarı baktım. Bir öğleden sonra hiçbir şey yapmadan oturdum, bu garipti ama kötü değildi.

Eve dönünce telefonda kırk yedi bildirim vardı. Hepsine baktım. Hiçbiri önemli değildi. Bir tanesi belki, o da beklerdi zaten.

Şimdi "telefonu bırakın" tarzı bir sonuç çıkarmam bekleniyor herhalde. Çıkarmıyorum. İki gün sonra yine aynı şekilde kullanıyorum. Fark ettiğim tek şey, kullanımın çoğunun bir şey için değil, boşluğu doldurmak için olduğu.

Belki bunu bilmek biraz işe yarar. Belki yaramaz. En azından artık farkındayım, o kadar.

Bir de şu: kimse beni aramadı iki gün boyunca. Merak eden olmadı. Bu biraz dokundu açıkçası. Ama ben de kimseyi aramıyorum zaten, adil sayılır."""),

("blog", """Ev bitkilerinin kış bakımı, çoğu kişinin fark etmediği kadar farklı kurallar gerektiriyor. Yaz aylarında işe yarayan rutin, kış geldiğinde bitkiye zarar verebiliyor. Bu yazıda mevsim geçişinde dikkat edilmesi gerekenleri toparladım.

En yaygın hata sulama sıklığını değiştirmemek. Kışın bitkilerin büyümesi yavaşlıyor, dolayısıyla su ihtiyacı azalıyor. Yaz rutinini sürdürmek kök çürümesine yol açıyor. Toprağın üst kısmı kuruduktan sonra birkaç gün daha beklemek genellikle doğru yaklaşım.

Işık konusunda tam tersi geçerli. Günler kısaldığı için bitkiler daha az ışık alıyor. Pencereye yakın konumlandırmak, hatta yer değiştirmek gerekebiliyor. Camın hemen dibinde soğuk hava akımı varsa bu da ayrı bir risk, dengelemek gerekiyor.

Kalorifer kaynaklı kuru hava, kışın en büyük sorunlardan biri. Nem oranı düşünce yaprak kenarları kahverengileşiyor. Bitkinin yanına bir kap su koymak veya çakıl taşlı tabak kullanmak basit çözümler sunuyor. Yaprakları su püskürterek nemlendirmek de işe yarıyor ancak her tür için uygun değil.

Gübreleme konusunda kış aylarında ara vermek öneriliyor. Bitki aktif büyüme döneminde olmadığı için besin talebi düşük. Fazla gübre toprakta birikiyor ve kökleri yakabiliyor.

Saksı değiştirme işlemi de bahara bırakılmalı. Kış döneminde yapılan repotlama, bitkinin toparlanmasını zorlaştırıyor.

Son olarak sabırlı olmakta fayda var. Kışın bitkiler durgunlaşıyor, yeni yaprak vermiyor. Bu normal bir durum, müdahale gerektirmiyor. Bahar geldiğinde hareketlenme kendiliğinden başlıyor."""),

("blog", """İkinci el ürün alırken nelere dikkat edilmeli sorusu, özellikle elektronik ürünlerde kritik önem taşıyor. Doğru değerlendirme yapıldığında ciddi tasarruf sağlanabiliyor; aceleci karar ise pahalıya patlayabiliyor. İşte pratik bir kontrol listesi.

Satıcının geçmişi ilk bakılacak nokta. Platform üzerinden alışveriş yapıyorsanız değerlendirme puanı ve yorum sayısı fikir veriyor. Yeni açılmış ve hiç geçmişi olmayan hesaplardan yüksek değerli ürün almak risk barındırıyor.

Fiyat, piyasa değerinin belirgin biçimde altındaysa temkinli olmakta fayda var. Çok cazip teklifler genellikle bir sorunu gizliyor. Ürünün ikinci el piyasasındaki ortalama fiyatını birkaç ilandan kontrol etmek yeterli.

Fotoğraflar konusunda stok görseli kullanan ilanlardan uzak durmalı. Ürünün kendi fotoğrafı, farklı açılardan ve gerçek ortamda çekilmiş olmalı. Satıcıdan ek fotoğraf istemek de makul bir talep.

Buluşarak alışverişte ürünü çalışır halde görmek şart. Telefon alıyorsanız kamera, hoparlör, şarj girişi ve ekranın tüm bölgeleri test edilmeli. Bilgisayarda ise ısınma davranışını görmek için birkaç dakika çalıştırmak gerekiyor.

Garanti durumu sıkça atlanıyor. Bazı ürünlerde garanti devredilebiliyor, faturanın saklanmış olması önemli. Seri numarasından garanti sorgusu yapmak mümkün.

Ödeme aşamasında platform dışına çıkmamak en temel güvenlik kuralı. Kapora talep eden, acele ettiren satıcılara karşı dikkatli olunmalı.

Bu adımlar uzun görünse de toplamda on dakikanızı alıyor. Karşılığında alacağınız güvence ise bu süreye fazlasıyla değiyor."""),

("blog", """Toplantıların verimliliğini artırmak, çoğu ekibin gündeminde olan ancak nadiren çözülen bir konu. Sorun genellikle toplantı sayısında değil, toplantı tasarımında yatıyor. Aşağıda uygulanabilir birkaç ilke var.

Her toplantının yazılı bir amacı olmalı. "Durum güncellemesi" bir amaç değil; bilgi aktarımı yazılı olarak da yapılabilir. Amaç, toplantı bitiminde neyin değişmiş olacağını tarif etmeli. Karar alınacaksa hangi karar, tartışılacaksa hangi seçenekler belli olmalı.

Katılımcı listesi dikkatle belirlenmeli. Herkesin haberdar olması gerekiyorsa not paylaşmak yeterli. Toplantıya yalnızca konuşacak veya karar verecek kişiler çağrılmalı. Sekiz kişilik bir toplantıda genellikle üç kişi konuşuyor, kalanların zamanı harcanıyor.

Ön okuma materyali göndermek, tartışma süresini belirgin biçimde kısaltıyor. Bağlamı toplantı içinde aktarmak yerine önceden paylaşmak, ilk on beş dakikayı kurtarıyor. Bazı ekipler ilk beş dakikayı sessiz okumaya ayırıyor; kulağa tuhaf gelse de işe yarıyor.

Süre kısaltmak basit ama etkili bir müdahale. Altmış dakikalık toplantılar genellikle otuz dakikada bitebiliyor. Takvim uygulamaları varsayılan olarak bir saat öneriyor ve kimse bunu sorgulamıyor.

Toplantı sonunda kararların ve sorumluların yazılması, en çok atlanan adım. Karar yazılmazsa alınmamış sayılıyor; iki hafta sonra aynı tartışma tekrar ediliyor.

Bu ilkeler yeni değil ancak uygulanması disiplin gerektiriyor. Bir ekip bunları iki ay tutarlı biçimde uygularsa fark belirgin şekilde görülüyor."""),

("kurumsal", """Kalite yönetim sistemimize ilişkin yıllık gözden geçirme çalışmalarımız tamamlanmıştır. Bu kapsamda elde edilen bulguları ve önümüzdeki döneme yönelik planlarımızı paydaşlarımızla paylaşmak isteriz.

Denetim süreçleri bağımsız kuruluşlar tarafından yürütülmüştür. Gerçekleştirilen incelemelerde sistemin genel işleyişinin standartlara uygun olduğu tespit edilmiştir. Belirlenen iyileştirme alanları için düzeltici faaliyet planları oluşturulmuş ve uygulamaya alınmıştır.

Üretim süreçlerinde izlenebilirlik kapasitemiz güçlendirilmiştir. Hammadde girişinden nihai ürün sevkiyatına kadar tüm aşamalar dijital ortamda kayıt altına alınmaktadır. Bu sayede olası bir uygunsuzluk durumunda kaynak tespiti hızla yapılabilmektedir.

Müşteri geri bildirimlerinin sisteme entegrasyonu konusunda ilerleme kaydedilmiştir. Gelen bildirimler kategorize edilerek ilgili birimlere yönlendirilmekte, çözüm süreleri düzenli olarak izlenmektedir. Ortalama çözüm süresinde geçen yıla kıyasla iyileşme gözlenmiştir.

Tedarikçi denetimleri planlanan takvime uygun şekilde yürütülmüştür. Kalite kriterlerini karşılamayan tedarikçilerle iyileştirme planları üzerinde çalışılmış, gerekli görülen durumlarda çalışma ilişkisi gözden geçirilmiştir.

Personel eğitimleri kapsamında kalite bilinci programları düzenlenmiştir. Katılım oranları hedeflenen düzeyde gerçekleşmiştir. Eğitim etkinliğinin ölçülmesine yönelik değerlendirme yöntemleri geliştirilmektedir.

Önümüzdeki dönemde süreç otomasyonu alanındaki yatırımlarımızın sürdürülmesi planlanmaktadır. Veri toplama noktalarının artırılması, analiz kabiliyetimizi güçlendirecektir. Paydaşlarımızın katkı ve önerilerini her zaman değerli bulduğumuzu belirtmek isteriz."""),

("kurumsal", """Dijital dönüşüm yol haritamızın ilk aşaması tamamlanmış bulunmaktadır. Sürecin mevcut durumu ve sonraki adımlara ilişkin değerlendirmelerimiz aşağıda özetlenmiştir.

Altyapı modernizasyonu kapsamında sistemlerimizin bulut ortamına taşınması büyük ölçüde gerçekleştirilmiştir. Bu geçiş, işlem kapasitemizin talebe göre esnek biçimde ayarlanabilmesine olanak tanımaktadır. Kesinti sürelerinde belirgin azalma kaydedilmiştir.

Veri yönetimi alanında merkezi bir yapıya geçilmiştir. Daha önce farklı birimlerde ayrı ayrı tutulan bilgiler tek bir platformda toplanmıştır. Bu düzenleme, raporlama süreçlerini hızlandırmış ve tutarsızlıkları azaltmıştır.

Süreç otomasyonu çalışmalarında öncelik, tekrar eden manuel işlemlere verilmiştir. Belirlenen süreçlerde insan müdahalesi gerektiren adım sayısı azaltılmıştır. Böylece çalışanlarımız katma değeri yüksek işlere yönelebilmektedir.

Değişim yönetimi boyutu özenle ele alınmıştır. Teknolojik geçişin başarısı, kullanıcı benimsemesine bağlıdır. Bu nedenle kapsamlı eğitim programları düzenlenmiş, geçiş dönemi boyunca destek ekipleri görevlendirilmiştir.

Güvenlik gereksinimleri her aşamada gözetilmiştir. Erişim yetkilendirme yapısı yeniden tasarlanmış, düzenli denetim mekanizmaları kurulmuştur.

İkinci aşamada veri analitiği yeteneklerimizin geliştirilmesi hedeflenmektedir. Toplanan verinin karar süreçlerinde daha etkin kullanılması amaçlanmaktadır.

Sürecin her adımında paydaşlarımızla şeffaf iletişim kurma ilkemizi sürdüreceğimizi belirtmek isteriz."""),

("haber", """Bölgede yürütülen ağaçlandırma çalışmaları kapsamında bu yıl belirlenen hedefe ulaşıldığı açıklandı. Yetkililer, dikim çalışmalarının planlanan takvime uygun şekilde tamamlandığını bildirdi.

Yapılan açıklamada, çalışmaların özellikle erozyon riski taşıyan alanlarda yoğunlaştığı belirtildi. Bölgenin iklim koşullarına uyumlu türlerin tercih edildiği, bu seçimin fidan yaşama oranını artırdığı ifade edildi.

Dikim sonrası bakım sürecinin kritik önem taşıdığı vurgulandı. İlk iki yıl boyunca düzenli sulama ve koruma faaliyetlerinin sürdürüleceği kaydedildi. Geçmiş yıllarda yapılan dikimlerde yaşama oranının beklentilerin üzerinde gerçekleştiği aktarıldı.

Çalışmalara gönüllü katılımın yüksek olduğu bildirildi. Okul grupları ve yerel derneklerin organizasyonlara destek verdiği, bu katılımın çevre bilinci açısından da değerli olduğu değerlendirildi.

Bölgedeki yaban hayatının korunmasına yönelik ek önlemlerin de gündemde olduğu açıklandı. Ağaçlandırılan alanların doğal yaşam koridorlarıyla bağlantısının gözetildiği ifade edildi.

Yetkililer, orman yangınlarıyla mücadelede erken müdahale kapasitesinin güçlendirildiğini belirtti. Gözetleme noktalarının sayısının artırıldığı, teknolojik izleme sistemlerinin devreye alındığı kaydedildi.

Önümüzdeki yıl için belirlenen hedefin bu yılın üzerinde olduğu duyuruldu. Vatandaşların gönüllü katılım için ilgili kurumlara başvurabileceği hatırlatıldı."""),

("kisisel", """Bu yıl ilk kez bir maratona hazırlandım ve süreç beklediğimden çok daha öğretici geçti. Koşuyu bitirdim ancak asıl kazanımın derece olmadığını söyleyebilirim.

Hazırlık dönemi altı ay sürdü. Başlangıçta haftada üç gün, toplam yirmi kilometre koşuyordum. Program kademeli olarak artıyordu. En zorlandığım kısım, mesafenin uzaması değil, düzeni korumaktı. Yağmurlu bir salı akşamı dışarı çıkmak, uzun mesafeden daha fazla irade gerektiriyordu.

Sakatlık riski konusunda uyarılmıştım ancak ciddiye almamıştım. Üçüncü ayda diz ağrısı başladı. İki hafta ara vermek zorunda kaldım. Fizyoterapist, koşu tekniğimdeki bir sorunu gösterdi. Adım uzunluğumu kısaltmak, ağrıyı tamamen ortadan kaldırdı.

Beslenme tarafı da öğrenme gerektirdi. Uzun koşulardan önce ne yeneceği, koşu sırasında sıvı alımının nasıl planlanacağı denemeyle bulundu. Bir antrenmanda yanlış tercih yüzünden yarısında durmak zorunda kaldım.

Yarış günü hava serindi, benim için avantajdı. İlk yirmi kilometre planladığım tempoda geçti. Otuzuncu kilometreden sonra zorlanmaya başladım. Son beş kilometreyi neredeyse tamamen zihinsel dirençle tamamladım.

Bitiş çizgisini geçtiğimde beklediğim coşkuyu hissetmedim açıkçası. Daha çok bir rahatlama vardı. Coşku ertesi gün geldi.

Tekrar yapar mıyım? Muhtemelen evet. Ama bu sefer hazırlığın tadını çıkarmaya çalışarak."""),
]


def rows():
    return [{"text": " ".join(t.split()), "label": 1, "lang": "tr",
             "source": "uretilmis-uzun/" + kind, "attack": "none"} for kind, t in SAMPLES]


if __name__ == "__main__":
    rs = rows()
    ws = [len(r["text"].split()) for r in rs]
    print("parti 4: %d ornek | kelime min %d / ort %d / max %d | >=140: %d"
          % (len(rs), min(ws), sum(ws) // len(ws), max(ws), sum(1 for w in ws if w >= 140)))
