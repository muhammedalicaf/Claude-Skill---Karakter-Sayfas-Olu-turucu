# Sayfa Düzeni

Nihai karakter sayfasının geometrisi. `scripts/birlestir.py` bu dosyadaki kuralları uygular.
Ölçüler orana bağlıdır; piksel değerleri 2560x1440 karşılıklarıdır.

## Tuval

| Değer | Oran | 2560x1440 |
|---|---|---|
| Genişlik x yükseklik | 16:9 | 2560 x 1440 |
| Ayraç / dış çerçeve kalınlığı | W x 0.0023 | 6 px |
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

| No | Görünüm | Kadraj | Hücre (2560x1440) | Hücre oranı |
|---|---|---|---|---|
| 1 | Ön profil | Tam boy, önden | 632 x 1428 | ~9:20 |
| 2 | Arka profil | Tam boy, arkadan | 632 x 1428 | ~9:20 |
| 3 | Ön portre | Baş-omuz, önden | 632 x 711 | ~9:10 |
| 4 | Sol 3/4 portre | Baş-omuz, 3/4 — sol yanak | 632 x 711 | ~9:10 |
| 5 | Sağ 3/4 portre | Baş-omuz, 3/4 — sağ yanak | 632 x 711 | ~9:10 |
| 6 | Arka portre | Baş-omuz, arkadan | 632 x 711 | ~9:10 |

Hesap: sütun genişliği `(W - 5g) / 4`, tam boy yükseklik `H - 2g`, portre yükseklik `(H - 3g) / 2`.
Bölme artığı soldan sağa sütunlara birer piksel dağıtılır; hiçbir ayraç kalınlaşmaz.

3/4 karelerin yönü **karakterin yanağına göre** tanımlanır:

- **4 — sol 3/4:** karakterin sol yanağı kameraya dönüktür. Baş karakterin kendi sağına döner,
  kadrajda yüz sola bakar.
- **5 — sağ 3/4:** karakterin sağ yanağı kameraya dönüktür. Baş karakterin kendi soluna döner,
  kadrajda yüz sağa bakar.

İkisi de gerçek 3/4 profil olmalı (baş ~35-45 derece dönük). Bu iki kare **birbirinin aynası
olamaz**: yüzün iki yanı doğal olarak asimetriktir, aynalanmış görüntü kalite kontrol hatasıdır.

## Kaynak kareleri hücreye oturtma

Üretim oranları hücre oranlarıyla birebir aynı değildir; script kareyi hücreyi kaplayacak kadar
ölçekler ve taşanı kırpar. Gerdirme yok, boşluk yok, dolgu yok.

| Hücre tipi | Üretim oranı | Hizalama |
|---|---|---|
| Tam boy (1, 2) | 9:16, 2K | Ölçüm yok. Kadrajı prompt kurar; script yalnızca hücre oranına kırpar |
| Baş-omuz (3-6) | 1:1, 2K | Kafa genişliği ölçülür, dört portre aynı kafa ölçüsüne getirilir |

Portrelerde ölçüm şöyle çalışır: üst köşelerden duvar rengi alınır, karakter duvardan
ayrıştırılır, tepe noktasının biraz altındaki satırlarda maske genişliği (kafa genişliği)
ölçülür. Hedef, kafa genişliğinin hücre genişliğinin %40'ı olması ve baş üstü boşluğun hücre
yüksekliğinin %8'i olması.

Tam boy karelerde bu ölçüm yapılmaz: zemin ile duvar ayrı tonlarda olduğu için otomatik
ayrıştırma güvenilmez. Oradaki tutarlılığı prompt sağlar (baş üstü ve ayak altı boşlukları
promptta istenir), script yalnızca kırpar.

Ölçüm başarısız olur ya da makul aralığın dışına çıkarsa script kareyi ortalar ve uyarı basar.
Tahmin yürütmez.

## Değişmezler

- Etiket, yazı, filigran, logo, çerçeve süsü yok.
- Altı hücre sabittir; eksik kare varsa sayfa üretilmez.
- Kıyafet, saç ve ışık altı karede aynı olmalıdır; farklılık kalite kontrol hatasıdır ve
  düzeltmesi yeniden üretimdir.
- Kareler hücreden küçükse script uyarır; çözüm daha yüksek çözünürlükte yeniden üretmektir.
- Dosya adı: `karakter-sayfasi_<karakter-adi>_<YYYYAAGG>.png`

Sayfa kurulduktan sonra `scripts/foto_ayar.py` ile tek bir fotografik geçiş uygulanır; o script
de bölgesel rötuş yapmaz, sayfanın tamamına aynı işlemi uygular.
