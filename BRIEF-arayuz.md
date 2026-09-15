# Arayüz görevi — AIFinder

Bu dosya, arayüzü yeniden tasarlayacak herkese (insan ya da başka bir kodlama
aracı) verilecek eksiksiz brieftir. Motora dokunulmayacak; **yalnızca**
`static/index.html` değişecek.

## Ürün nedir

Yerel çalışan bir yapay zekâ metin tespit aracı. Kullanıcı metin yapıştırır ya
da PDF/DOCX yükler; araç belgeyi ~300 kelimelik örtüşen pencerelere böler, her
pencereyi üç bağımsız katmandan geçirir ve **belgenin yüzde kaçının yapay zekâ
üretimi olduğunu** söyler.

- **Kullanıcı:** tek kişi (projenin sahibi), kendi metinlerini kontrol ediyor.
  Kimse hakkında karar alınmıyor, kurumsal kullanım yok.
- **Dil:** arayüz tamamen Türkçe.
- **Çalışma yeri:** `http://127.0.0.1:9317`, internet yok, dış istek yasak.
- **Ziyaretçi modu:** Operate — kullanıcı bir işi tamamlıyor, gösteri değil.

## Değiştirilemeyecek olanlar

1. **Yanlış pozitif uyarısı kalır.** Küçültülebilir, yeniden yazılabilir, ama
   sonucun yanında görünür olmalı. Gerekçe: Stanford 2023 (Liang ve ark.,
   *Patterns*) çalışmasında yedi ticari detektör, ana dili İngilizce olmayan
   kişilerin denemelerinin %61'ini yanlışlıkla "AI" olarak işaretledi.
2. **Ölçülmüş doğruluk (`quality`) gösterilir.** Gizlenirse yüzde, hak
   etmediği bir kesinlik izlenimi verir.
3. **Kalibrasyon yoksa yüzde gösterilmez.** Sunucu `undecided: true` +
   `uncalibrated: true` döndürür; bu ayrı ve sakin bir ekrandır, hata değildir.
4. **Dış kaynak yok.** CDN, web fontu, analytics, uzak görsel — hiçbiri.
   Tek dosya, gömülü CSS/JS.
5. **Koyu/açık tema** `prefers-color-scheme` ile çalışmaya devam etmeli.

## Veri sözleşmesi

Tam alan listesi `API.md` dosyasındadır. Özet:

| Alan | Kullanım |
|---|---|
| `percent` | Ana çıktı: 0–100 |
| `verdict` / `tone` | Sözel karar + renk sınıfı |
| `confidence` | Kararın ne kadar sağlam olduğu |
| `threshold` | Bir pencerenin "AI" sayılma eşiği |
| `words` + `word_probs` | Aynı sırada: kelime ve o kelimenin AI olasılığı |
| `windows` | Pencere sınırları ve olasılıkları |
| `layers` | Üç katmanın ayrı ayrı çıktısı |
| `stylometry` | Biçem sinyalleri — kararın gerekçesi |
| `forensics` | Belge üstverisi + saldırı izleri (`flag: "warn"` vurgulanır) |
| `quality` | Ölçülmüş AUC / yakalama oranı |
| `stats.short` | Metin 300 kelimeden kısaysa uyarı gerekir |

## Test

```bash
.venv/bin/python app.py          # http://127.0.0.1:9317
```

`AIFINDER_NO_WARMUP=1` ile başlatılırsa modeller yüklenmez; arayüzü bellek
harcamadan denemek için kullanılır (analiz isteği yine de modelleri yükler).

## Kapsam dışı

`analyze.py`, `engine/`, `eval/`, `extract.py`, `detector.py`, `app.py` —
hiçbirine dokunulmayacak. Sunucu sözleşmesi sabittir.
