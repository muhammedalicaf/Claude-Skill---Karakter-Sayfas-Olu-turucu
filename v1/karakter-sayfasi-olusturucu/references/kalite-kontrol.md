# Kalite Kontrol

Hangi karenin geçtiği, hangisinin yeniden üretileceği ve kullanıcının ne göreceği.

## Onay yetkisi

| Kare | Onaylayan |
|---|---|
| 3 — Ön portre | **Kullanıcı.** Sunulur, onay gelmeden hiçbir kare üretilmez |
| 1, 2, 4, 5, 6 | **Claude.** Aşağıdaki ölçütlerle denetler, hatalıyı yeniden üretir |

Kare 3 kimliğin kaynağıdır; oradaki bir kusur beş kareye birden taşınır. Bu yüzden tek kullanıcı
onayı orada, en başta alınır. Kullanıcı "beğenmedim" derse kare 3 yeniden üretilir, zincir
başlamaz.

## Denetim kanalı

Claude kareyi **görmeden** onaylayamaz. Replicate çıktısı bir bağlantı olarak döner; piksele
ulaşmanın yolu sırayla denenir:

1. **İndir ve bak.** `replicate.delivery` hesabın ağ izin listesindeyse kare sandbox'a indirilir;
   Claude hem bakar hem script'ler aynı dosyayı kullanır. İstenen yol budur.
2. **Köprü.** İndirme engelliyse kare Higgsfield deposuna aktarılıp oradan okunabilir. Denetim
   çalışır ama dosya yerelde olmadığı için birleştirme yapılamaz.
3. **Yükleme.** İkisi de yoksa kullanıcıdan altı kareyi sohbete yüklemesi istenir; hem denetim
   hem birleştirme bundan beslenir.

Claude kareyi görmediği hâlde "Onay Aldı" demez. Görememişse bunu açıkça söyler ve yükleme ister.
Sessizce varsayım yapmak bu akışın en pahalı hatasıdır: kusur altı kareye birden yayılır.

## Ortak ölçütler (her karede)

| Etiket | Ne aranır |
|---|---|
| `[Kadraja Sığmama]` | Baş, ayak, omuz veya kulak kadrajdan taşmış |
| `[Kadraj Ölçeği]` | Karakter diğer karelere göre belirgin yakın/uzak; göz hizası ya da boy tutmuyor |
| `[Yanlış Açı]` | İstenen dönüş açısı tutmuyor (3/4 yerine neredeyse cepheden ya da tam yandan) |
| `[Kimlik Kayması]` | Yüz hatları, yaş, saç kesimi, ten tonu ya da vücut tipi kare 3'ten farklı |
| `[Fon Uyumsuzluğu]` | Stüdyo diğer karelerle aynı değil: duvar tonu, ışık düşüşü ya da zemin-duvar ilişkisi farklı |
| `[Işık Uyumsuzluğu]` | Işığın yönü ya da sertliği diğer karelerden farklı |
| `[Sahne Kayması]` | Kadraja mobilya, eşya, ikinci bir mekân ya da dış ortam girmiş |
| `[Kıyafet Farkı]` | Sabit nötr kıyafet değişmiş; baskı, logo, takı, saat, gözlük eklenmiş |
| `[Fazla Nesne]` | İkinci kişi, manken, aksesuar, mobilya, prop |
| `[Anatomi Hatası]` | Fazla/eksik parmak, bozuk el, bozuk kulak, imkânsız eklem |
| `[Yazı/Filigran]` | Yazı, altyazı, logo, çerçeve, kolaj/panel bölmesi |
| `[Plastik Cilt]` | Mikro detay yok: gözeneksiz, pürüzsüzleştirilmiş, parlak/mumsu cilt, tek tonlu saç |
| `[Bakış Hatası]` | Bakış yönü şablondakinden farklı; şaşı ya da boş bakış |

## Kareye özel ölçütler

- **1 — Ön profil:** Tam boy; iki ayak da tam görünür, ayaklar yerde, kollar yanda, gövde dönük
  değil. Baş üstü ve ayak altı boşluğu var (kırpma payı için gerekli). Duvar ile zemin ayırt
  edilebiliyor.
- **2 — Arka profil:** Yüzün hiçbir parçası görünmez. Omuz hattı simetrik, gövde kameraya dönük
  değil. Boy ve duruş kare 1 ile aynı okunmalı.
- **4 ve 5:** Gerçek 3/4 (yaklaşık 35-45°). İkisi birbirinin aynası olamaz — `[Aynalama]` etiketi
  bu ikisine özeldir. Yakın taraftaki kulak tam görünür.
- **6 — Arka portre:** Yüz görünmez, iki kulak simetrik, saç kesimi ve ense hattı okunur.

## Yeniden üretim kuralı

1. Hata etiketi belirlenir, kullanıcıya durum mesajıyla bildirilir.
2. Aynı prompt, aynı kimlik bloğu, aynı eleman ile yeniden gönderilir; tek değişiklik hataya
   yönelik **düzeltici cümle**dir (ör. `[Kadraja Sığmama]` için: *"the entire head and both feet
   fully inside the frame with a clear empty margin on every side, nothing cropped"*).
3. Kimlik bloğu yeniden yazılmaz, kopyalanır.
4. Bir kare için en fazla **2 yeniden üretim**. Üçüncüde durulur, kullanıcıya ne olduğu ve iki
   seçenek söylenir: elde olan en iyi kareyle devam etmek ya da kare 3'e dönüp kimliği yenilemek.
5. Aynı hata iki kez üst üste çıkıyorsa gerekçe promptun kendisindedir; düzeltici cümleyi
   tekrarlamak yerine ilgili blok güçlendirilir.

Her üretim ücretlidir. Altı kare artı yeniden üretimler toplam maliyettir; üretime başlamadan
önce kullanıcıya kaç kare üretileceği söylenir.

## Durum mesajları

Notion'daki biçim birebir korunur. Kare adları: **Ön Profil, Arka Profil, Ön Portre,
Sol 3/4 Portre, Sağ 3/4 Portre, Arka Portre.**

```
<Kare Adı> Üretiliyor..
<Kare Adı> Üretildi..
<Kare Adı> [Hata Etiketi] Nedeni ile Hatalı..
<Kare Adı> Tekrar Üretiliyor..
<Kare Adı> Onay Aldı..
```

Örnek:

```
Sağ 3/4 Portre Üretiliyor..
Sağ 3/4 Portre Üretildi..
Sağ 3/4 Portre [Kadraja Sığmama] Nedeni ile Hatalı..
Sağ 3/4 Portre Tekrar Üretiliyor..
Sağ 3/4 Portre Üretildi..
Sağ 3/4 Portre Onay Aldı..
```

Kurallar: her adım anında bildirilir, toplu özet geçilmez. Hata gizlenmez — düzeltilip geçilse
bile satırı yazılır. Mesajlar kısa tutulur, araya yorum eklenmez.

## Sayfa öncesi son kontrol

Altı kare onaylandıktan sonra, birleştirme script'i çalışmadan önce:

- Altı karenin tamamı var mı? Eksikle sayfa üretilmez.
- Altısında kıyafet, saç ve stüdyo aynı mı?
- Dört portrede göz hizası ve kafa boyutu birbirini tutuyor mu?
- İki tam boyda karakterin boyu aynı piksel yüksekliğinde mi?
- 4 ile 5 birbirinin aynası değil, değil mi?

Bu listede takılan bir madde varsa ilgili kare yeniden üretilir; sayfa "nasılsa küçük görünür"
diye kusurlu kareyle kurulmaz. Hiçbir kusur script ile düzeltilmez — birleştirme ve fotoğraf
ayarı script'leri içeriğe müdahale etmez, yalnızca uyarır.
