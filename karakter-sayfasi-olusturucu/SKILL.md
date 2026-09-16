---
name: karakter-sayfasi-olusturucu
description: Fotogerçekçi teknik karakter referans sayfası üretir. Kullanıcıyla konuşup karakteri netleştirir, altı görünümü (iki tam boy, dört baş-omuz portre) Replicate üzerinde nano-banana-pro ile tek tek üretir, her kareyi denetler, hatalıyı yeniden üretir ve hepsini 2560x1440 tek sayfada birleştirip Lightroom karşılığı bir fotografik geçiş uygular. Kullanıcı karakter sayfası, model sheet, turnaround, karakter referansı, çoklu açıdan karakter görseli, oyuncu referansı ya da ürün çekimi için karakter istediğinde kullanılır.
---

# Karakter Sayfası Oluşturucu

Tek bir karakterin altı açıdan fotoğraflanmış teknik referans sayfasını üretir. Çıktı, gerçek bir
stüdyo çekiminden ayırt edilemeyecek kalitede olmayı hedefler.

## Akış

```
1  Görüşme            -> references/gorusme.md
2  Profil onayı        (kullanıcı)
3  Kare 3 üretimi     -> references/prompt-mimarisi.md
4  Kare 3 onayı        (kullanıcı — zincirdeki tek onay noktası)
5  Kalan beş kare     -> kare 3 referans alınarak
6  Denetim            -> references/kalite-kontrol.md
7  Birleştirme        -> scripts/birlestir.py
8  Fotografik geçiş   -> scripts/foto_ayar.py
9  Teslim
```

Adımlar sırayla işler. Kare 3 onaylanmadan 5. adıma geçilmez; altı kare onaylanmadan sayfa
kurulmaz.

## 1-2. Görüşme ve profil

`references/gorusme.md` okunur ve uygulanır. Ton analitik ve profesyoneldir; sorular şıklı
sorulur, kullanıcının zaten söylediği tekrar sorulmaz. Sonunda Türkçe profil özeti gösterilip
onay alınır ve üretim maliyeti (kare sayısı) tek satırda söylenir.

Kullanıcı karakter sayfası dışına çıkarsa (sahne, kostüm, video, gerçek kişi benzerliği) kibarca
sınır hatırlatılır: ne yapılamadığı, neden, yerine ne yapılabileceği — tek cümlede.

Onaylanan profilden İngilizce kimlik bloğu (B) yazılır ve **saklanır**. Bu blok altı promptta
birebir kopyalanır; yeniden üretimlerde asla yeniden yazılmaz.

## 3-5. Üretim

`references/prompt-mimarisi.md` okunur. Özet: Replicate, `google/nano-banana-pro`,
`resolution: "2K"`, tam boy kareler `9:16`, portreler `1:1`. Promptlar A-G blok sırasıyla
kurulur, İngilizce yazılır.

Sıra: önce kare 3 (ön portre) üretilir ve kullanıcıya sunulur. Onaydan sonra kalan beş kare,
`image_input` alanında kare 3'ün bağlantısı ile üretilir — kimliği taşıyan mekanizma budur.

Her adımda durum mesajı yazılır (biçimi `kalite-kontrol.md`'de):

```
Sağ 3/4 Portre Üretiliyor..
Sağ 3/4 Portre Üretildi..
Sağ 3/4 Portre [Kadraja Sığmama] Nedeni ile Hatalı..
Sağ 3/4 Portre Tekrar Üretiliyor..
Sağ 3/4 Portre Onay Aldı..
```

Üretilen bağlantılar geçicidir; kareler ilk fırsatta indirilir.

## 6. Denetim

`references/kalite-kontrol.md` okunur. Kare 3'ü kullanıcı, kalan beşini Claude onaylar.

Claude kareye **bakmadan** onay vermez. Bakamıyorsa bunu söyler ve kullanıcıdan kareleri sohbete
yüklemesini ister. Kare başına en fazla iki yeniden üretim; üçüncüde durulur ve kullanıcıya
seçenek sunulur.

## 7-8. Birleştirme ve geçiş

```bash
python3 scripts/birlestir.py k1.png k2.png k3.png k4.png k5.png k6.png --ad "<karakter>"
python3 scripts/foto_ayar.py karakter-sayfasi_<karakter>_<tarih>.png -o <ayni>_son.png
```

`birlestir.py` düzeni `references/sayfa-duzeni.md`'den uygular: dört sütun, sol ikisi tam boy,
sağ ikisi ortadan bölünmüş, 2560x1440, ince koyu ayraçlar, etiketsiz.

`foto_ayar.py` sayfanın tamamına tek bir fotografik geçiş uygular; ayarlar Lightroom'da yapılan
pozlama -0,40 / kontrast -4 / sıcaklık -4 / renk tonu -4 / canlılık -4 / doygunluk -4 / gren
5-25-50 takımının ölçümle kalibre edilmiş karşılığıdır.

Script'lerin bastığı uyarılar okunur ve kullanıcıya iletilir. Uyarı alan kare varsa sayfa
teslim edilmeden önce o kare yeniden üretilir.

## Değişmez kurallar

- **Script içeriğe müdahale etmez.** Arka plan düzeltilmez, gölge silinmez, ton bölgesel olarak
  oynanmaz, boşluk doldurulmaz. Bozuk kareyi fotomontajla kurtarmak yerine yeniden üretmek şarttır.
- **Fon sonsuz gri değildir.** Gerçek stüdyo: duvar ile zemin ayırt edilir, ışığın duvara düşüşü
  korunur. Yerde gölge zorunlu değildir.
- **Kıyafet sabittir:** beyaz bisiklet yaka tişört, siyah pantolon, gri spor ayakkabı, aksesuar
  yok. Kullanıcı ne isterse istesin bu sayfada değişmez.
- **Kimlik bloğu bir kez yazılır**, altı promptta kopyalanır.
- **4 ve 5 birbirinin aynası olamaz;** 4'te sol yanak, 5'te sağ yanak kameraya dönüktür.
- **Hazır karakter sayfası iş akışları kullanılmaz** — altı kare tek tek üretilir; hatalı kare
  tek başına yenilenebilsin diye.
- Kullanıcıya model adı, parametre adı, araç adı ya da prompt iç yapısı gösterilmez.

## Dosyalar

| Dosya | Ne zaman okunur |
|---|---|
| `references/gorusme.md` | Görüşme başlarken |
| `references/prompt-mimarisi.md` | İlk kare üretilmeden önce |
| `references/kalite-kontrol.md` | İlk kare döndüğünde |
| `references/sayfa-duzeni.md` | Birleştirmeden önce (script'in ne yaptığını bilmek gerekirse) |
| `scripts/birlestir.py` | 7. adım |
| `scripts/foto_ayar.py` | 8. adım |
