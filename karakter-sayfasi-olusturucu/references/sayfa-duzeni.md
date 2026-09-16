# Sayfa Düzeni

Nihai karakter sayfasının geometrisi. `scripts/birlestir.py` bu dosyadaki kuralları uygular.
Ölçüler orana bağlıdır; piksel değerleri 3840x2160 karşılıklarıdır.

## Tuval

| Değer | Oran | 3840x2160 |
|---|---|---|
| Genişlik x yükseklik | 16:9 | 3840 x 2160 |
| Ayraç / dış çerçeve kalınlığı | W x 0.0023 | 9 px |
| Ayraç rengi | — | `#141414` |
| Çıktı | — | PNG, sRGB, etiketsiz |

**Arka plan sayfanın değil karelerin işidir.** Script hiçbir karenin fonuna dokunmaz: ton
düzeltmez, gradyan silmez, boşluk doldurmaz. Altı karenin fonu birbirini tutmuyorsa bu bir
birleştirme sorunu değil, üretim sorunudur — ilgili kare yeniden üretilir.

## Izgara

Dört eşit sütun. Sol iki sütun tam yükseklik, sağ iki sütun ortadan ikiye bölünür.

```
┌──────────┬──────────┬─────────┬─────────┐
│          │          │    3    │    4    │
│    1     │    2     ├─────────┼─────────┤
│          │          │    5    │    6    │
└──────────┴──────────┴─────────┴─────────┘
```

| No | Görünüm | Kadraj | Hücre (3840x2160) | Hücre oranı |
|---|---|---|---|---|
| 1 | Ön profil | Tam boy, önden | 949 x 2142 | ~9:20 |
| 2 | Arka profil | Tam boy, arkadan | 949 x 2142 | ~9:20 |
| 3 | Ön portre | Baş-omuz, önden | 949 x 1067 | ~9:10 |
| 4 | Sol 3/4 portre | Baş-omuz, 3/4 — sol yanak | 948 x 1067 | ~9:10 |
| 5 | Sağ 3/4 portre | Baş-omuz, 3/4 — sağ yanak | 949 x 1066 | ~9:10 |
| 6 | Arka portre | Baş-omuz, arkadan | 948 x 1066 | ~9:10 |

Hesap: sütun genişliği `(W - 5g) / 4`, tam boy yükseklik `H - 2g`, portre yükseklik `(H - 3g) / 2`.
Bölme artığı soldan sağa sütunlara birer piksel dağıtılır; hiçbir ayraç kalınlaşmaz. 3840x2160'ta
artık 949/949/949/948 ve 1067/1066 olarak dağılır — tablodaki tek piksellik farklar bundandır.

**Numaralar hücre numaralarıdır, üretim sırası değil.** Üretim 3 → 4 → 5 → 6 → 1 → 2 sırasıyla
yapılır (`prompt-mimarisi.md`); birleştirme ve dosya adları ise bu tablodaki sırayı kullanır.

3/4 karelerin yönü **karakterin yanağına göre** tanımlanır:

- **4 — sol 3/4:** karakterin sol yanağı kameraya dönüktür. Gövde ve baş birlikte karakterin
  kendi sağına döner, kadrajda yüz sola bakar.
- **5 — sağ 3/4:** karakterin sağ yanağı kameraya dönüktür. Gövde ve baş birlikte karakterin
  kendi soluna döner, kadrajda yüz sağa bakar.

Bu iki karede **yalnızca baş dönmez, gövde de döner:** omuz hattı kameraya paralel değildir,
uzak omuz geride, yakın omuz öndedir.

İkisi de gerçek 3/4 profil olmalı (baş ~35-45 derece dönük). Bu iki kare **birbirinin aynası
olamaz**: yüzün iki yanı doğal olarak asimetriktir, aynalanmış görüntü kalite kontrol hatasıdır.

## Kaynak kareleri hücreye oturtma

Üretim oranları hücre oranlarıyla birebir aynı değildir; script kareyi hücreyi kaplayacak kadar
ölçekler ve taşanı kırpar. Gerdirme yok, boşluk yok, dolgu yok.

| Hücre tipi | Üretim oranı | Hizalama |
|---|---|---|
| Tam boy (1, 2) | 9:16, 4K | Ölçüm yok. Kadrajı prompt kurar; script yalnızca hücre oranına kırpar |
| Baş-omuz (3-6) | 1:1, 4K | Kafa genişliği ölçülür, dört portre aynı kafa ölçüsüne getirilir |

Portrelerde ölçüm şöyle çalışır: üst köşelerden duvar rengi alınır, karakter duvardan
ayrıştırılır, tepe noktasının biraz altındaki satırlarda maske genişliği (kafa genişliği)
ölçülür. Hedef, kafa genişliğinin hücre genişliğinin %40'ı olması ve baş üstü boşluğun hücre
yüksekliğinin %8'i olması.

Tam boy karelerde bu ölçüm yapılmaz: zemin ile duvar ayrı tonlarda olduğu için otomatik
ayrıştırma güvenilmez. Oradaki tutarlılığı prompt sağlar (baş üstü ve ayak altı boşlukları
promptta istenir), script yalnızca kırpar.

### Kadraj esneme payı

Hedef değerler (%40 kafa genişliği, %8 baş üstü boşluk) **±%10 payla** geçerlidir. Görsel modeli
bu oranları birebir tutturmaz ve tutturmak zorunda da değildir:

- **Pay içinde** (sapma ≤ %10): kareye dokunulmaz, yeniden ölçeklenmez; yalnızca baş üstü
  boşluğuna göre hizalanır. %10'luk farkla boğuşmak kaliteyi artırmaz, kareyi yeniden üretme
  maliyeti getirir.
- **Pay dışı ama makul** (sapma %10 ile 1,6 kat arası): kare sessizce hedef kafa ölçüsüne
  getirilir. Bu script'in olağan işidir, hata değildir.
- **Bozuk kadraj** (1,6 kattan fazla sapma): hizalama yapılmaz, kare ortalanır ve uyarı basılır.
  Çözüm kareyi yeniden üretmektir.

Ölçütün kaynak karenin piksel boyutuna bağlı olmaması önemlidir; bu yüzden karşılaştırma mutlak
ölçek üzerinden değil, hizalama ölçeğinin hücreyi kaplayan ölçeğe oranı üzerinden yapılır.
`kalite-kontrol.md`'deki `[Kadraj Ölçeği]` ölçütü aynı payı kullanır.

Ölçüm hiç yapılamazsa (karakter duvardan ayrıştırılamadıysa) script kareyi ortalar ve uyarı
basar. Tahmin yürütmez.

## Değişmezler

- Etiket, yazı, filigran, logo, çerçeve süsü yok.
- Altı hücre sabittir; eksik kare varsa sayfa üretilmez.
- Kıyafet, saç ve ışık altı karede aynı olmalıdır; farklılık kalite kontrol hatasıdır ve
  düzeltmesi yeniden üretimdir.
- Kareler hücreden küçükse script uyarır; çözüm daha yüksek çözünürlükte yeniden üretmektir.
- Dosya adı: `<İsim> - Karakter Referans Sayfası.png` (bkz. `teslimat.md`)

Sayfa kurulduktan sonra `scripts/foto_ayar.py` ile tek bir fotografik geçiş uygulanır; o script
de bölgesel rötuş yapmaz, sayfanın tamamına aynı işlemi uygular.
