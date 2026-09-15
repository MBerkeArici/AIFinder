# AIFinder — Arayüz ↔ Sunucu Sözleşmesi

Arayüzü (`static/index.html`) yeniden tasarlayacak herkesin — insan ya da başka
bir kodlama aracı — uyması gereken veri sözleşmesi. Sunucu tarafını değiştirmeden
arayüz tamamen baştan yazılabilir; yeter ki aşağıdaki alanlar tüketilsin.

## `GET /api/status`

Modeller arka planda yüklenir. Arayüz hazır olana kadar yoklamalıdır.

```json
{
  "ready": true,
  "error": null,
  "calibrated": { "tr": true, "en": true },
  "quality": {
    "tr": { "auc": 0.97, "tpr_at_fpr1": 0.91, "attack_tpr": null, "n": 297,
            "signals": ["binoculars", "siniflandirici", "stilometri"] }
  }
}
```

## `POST /api/analyze`

`multipart/form-data` ile ya `text` alanı ya da `file` alanı (PDF/DOCX/TXT/MD).

### Başarılı yanıt

| Alan | Tip | Anlamı |
|---|---|---|
| `percent` | 0–100 | **Ana çıktı.** Eşiği aşan pencerelerin kelime oranı |
| `verdict` / `tone` | metin | Sözel karar ve renk sınıfı (`ai`, `likely-ai`, `mixed`, `likely-human`, `human`) |
| `confidence` | 0–100 | Kararın eşikten uzaklığı + metin uzunluğundan türetilir |
| `threshold` | 0–1 | Bir pencerenin "AI" sayılması için gereken olasılık |
| `words` | dizi | Metnin kelimeleri (en fazla 8000) |
| `word_probs` | dizi | `words` ile **aynı sırada**, kelime başına AI olasılığı |
| `windows` | dizi | `{p, is_ai, w_start, w_end, c_start, c_end, preview}` |
| `layers` | dizi | `{label, value}` — üç katmanın ayrı ayrı çıktısı |
| `stylometry` | dizi | `{label, score, detail, weight, why}` — biçem sinyalleri |
| `sentences` | dizi | `{text, level, label, raw}` — cümle bazlı **biçem işareti** |
| `forensics` | dizi | `{label, value, flag}` — belge üstveri bulguları (`flag: "warn"` vurgulanmalı) |
| `quality` | nesne | Ölçülmüş doğruluk; **arayüzde gösterilmeli** |
| `stats` | nesne | `{words, windows, sentences, short}` |

### Karar verilemeyen durum (HTTP 400)

```json
{ "ok": false, "undecided": true, "error": "Karar verebilmek için en az 85 kelime…" }
```

Bu bir hata değildir; ayrı ve sakin bir ekranla gösterilmelidir.

### Hata (HTTP 400/413/500)

```json
{ "ok": false, "error": "…" }
```

## Tasarımda uyulması gereken kurallar

1. **Yanlış pozitif uyarısı kaldırılamaz.** Araç bir kişi hakkında karar almak
   için kullanılabilir; uyarı sonucun yanında, göz ardı edilemeyecek yerde durmalı.
2. **`quality` gösterilmeli.** Ölçülmüş doğruluk rakamları gizlenirse yüzde,
   hak etmediği bir kesinlik izlenimi verir.
3. **`percent` tek başına büyük gösterilmemeli** — `confidence` ve
   `stats.short` (kısa metin uyarısı) ona eşlik etmeli.
4. **`word_probs` eşiğin altında da bilgi taşır**; eşiğe yakın bölümler ayrı
   bir tonla gösterilmeli, sadece ikili (AI/değil) boyama yapılmamalı.
5. Metin dışarı gönderilmez — arayüz hiçbir dış servise istek atmamalı.

### Düşük sonuçlarda zorunlu uyarı (`not_proof`)

`percent < 15` olduğunda yanıt `not_proof: true` ve `not_proof_note` taşır.
Bu not **gösterilmek zorundadır**. Gerekçe ölçümdedir: yapay zekâya "insan
gibi yaz" denilerek üretilen metinlerin 0/10'u yakalanıyor ve bu metinlerin
kalibre olasılığı insan metinlerinin medyanının yanında kalıyor — eşik
hiçbir noktada ikisini ayırmıyor.

Araç bu nedenle **"insan yazımı" hükmü vermez**; en düşük sonuçta bile
"Yapay zekâ izi bulunamadı" der. Arayüz bu ayrımı korumalı, sonucu
"temiz/insan" gibi olumlu bir onaya dönüştürmemelidir.

### `sentences` yüzde olarak gösterilmemeli

Cümle değerleri **olasılık değildir** ve kalibre edilmemiştir. Ham puanın
tabanı 40'tır: hiçbir yapay zekâ işareti taşımayan bir cümle bile 40 alır;
kalıp ifade +18, geçiş kelimesi +11 ekler.

Bu değer yüzde olarak gösterilirse kullanıcı onu olasılık sanar ve pencere
kararlarıyla çelişir görünür — pencere "%0, eşik altında" derken cümleler
"%70" görünür. İkisi farklı ölçeklerdir.

Bu yüzden alan `level` (0-3) ve `label` ("işaret yok", "hafif iz",
"bir miktar kalıp", "belirgin kalıp") taşır. **Arayüz `label`'ı
göstermeli, `raw`'u yüzde olarak göstermemelidir.** `raw` yalnızca
sıralama ve renk yoğunluğu içindir.

Karar `windows` alanındadır; `sentences` yalnızca "neden böyle düşünüyor"
sorusunu açıklar.
