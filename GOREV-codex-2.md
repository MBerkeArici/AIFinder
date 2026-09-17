# Codex görevi #2 — arayüz: açıklama, uyarı ve uyum

Kapsam **yalnızca `static/index.html`**. Sunucu tarafına (`analyze.py`,
`engine/`, `eval/`, `app.py`) dokunulmayacak; o dosyalarda paralel çalışma
sürüyor.

Referanslar: `API.md` (veri sözleşmesi) ve `UI-METINLERI.md` (hazır metinler).

---

## 1. Bölümler kendini açıklasın  ← en öncelikli

Kullanıcı "burası ne anlama geliyor, hiç anlamadım" geri bildirimini verdi.
`UI-METINLERI.md` dosyasında her bölüm için hazır Türkçe açıklama var.
Bunları arayüze yerleştir — açılır bilgi (tooltip), başlık altı alt metin ya
da katlanır "nedir bu?" bölümü olarak; yöntem sana kalmış, ama açıklama
görünür olmalı.

Özellikle şu ikisi karıştırılıyor, aradaki farkın ekranda anlaşılması gerekiyor:

| Bölüm | Ne olduğu |
|---|---|
| **İnceleme pencereleri** | Gerçek karar. Yüzdeler kalibre edilmiş olasılık. |
| **Cümle görünümü** | Karar değil, **gerekçe**. Olasılık değil, biçem işareti. |

## 2. `sentences` alanı değişti — yüzde gösterme

Artık `{text, level, label, raw}` geliyor:

- `label` gösterilecek: `işaret yok` · `hafif iz` · `bir miktar kalıp` · `belirgin kalıp`
- `raw` **yüzde olarak gösterilmeyecek** — yalnızca renk yoğunluğu/sıralama için

Gerekçe: o değerin tabanı 40'tır, yani hiçbir iz taşımayan cümle bile 40
alır. Yüzde olarak gösterilince kullanıcı onu olasılık sanıyor ve pencere
kararlarıyla çelişir görünüyordu (pencere %0 derken cümleler %70).

## 3. `not_proof` uyarısı zorunlu

`percent < 15` olduğunda yanıt `not_proof: true` ve `not_proof_note` taşır.
Bu not **gösterilmek zorunda**.

Araç hiçbir koşulda "insan yazımı" demez; en düşük sonuçta bile ifade
"Yapay zekâ izi bulunamadı"dır. Arayüz bunu olumlu bir onaya (yeşil tik,
"temiz", "insan yazımı") dönüştürmemeli — ölçümde, gizlenmiş yapay zekâ
metinlerinin hiçbiri yakalanamadı.

## 4. Mobil ve dar ekran uyumu

Sonuç ekranı telefonda kullanılabilir olmalı: tablolar yatay kaydırılabilir,
yüzde göstergesi taşmamalı, metin işaretleme okunabilir kalmalı.

## 5. Erişilebilirlik

- Renk tek başına bilgi taşımasın (kırmızı/yeşil ayrımı metinle de verilsin)
- Sekmeler ve butonlar klavyeyle kullanılabilsin, odak halkası görünür olsun
- Yükleme durumunda `aria-live` ile ekran okuyucuya bilgi verilsin
- Kontrast oranları WCAG AA seviyesini karşılasın

---

## Test

```bash
AIFINDER_NO_WARMUP=1 .venv/bin/python app.py
```

Bu modda modeller yüklenmez, arayüz belleği meşgul etmeden denenebilir.
Gerçek sonuç ekranını görmek için `AIFINDER_NO_WARMUP` olmadan başlat.

## Yapılmayacaklar

- Sunucu sözleşmesini değiştirmek (yeni alan istemek, alan adı değiştirmek)
- Dış kaynak eklemek (CDN, web fontu, analitik) — sayfa tek dosya ve çevrimdışı
- Uyarı metinlerini yumuşatmak veya kaldırmak
