# Teslimat

Altı kare onaylandıktan sonrası: künye, isimlendirme, arşiv ve aksiyon özeti. Akışın sonunda
bir kez okunur.

## Künye

Sayfa bittikten sonra karaktere kısa bir künye yazılır. Künye bir **teslimat belgesidir**:
kullanıcının karakteri sonraki işlerde (sahne üretimi, casting notu, senaryo) hatırlaması için
vardır.

**Künye prompta girmez.** Ne B bloğuna eklenir ne de ayrı bir blok olarak gönderilir; altı kare
zaten üretilmiş olur. Kimlik bloğu görselin tek kaynağıdır, künye onun yanında duran bir nottur.
Bu ayrım korunmazsa kimlik bloğu edebi tarifle kirlenir ve kareler birbirinden uzaklaşır.

Biçim: **2-3 cümle, Türkçe, düz metin.** Başlık, madde işareti, süsleme yok.

İçerir:
- Ad, yaş aralığı, tek cümlelik fiziksel özet (kimlik bloğunun Türkçe karşılığı, kısaltılmış)
- Uğraş ya da meslek — kullanıcı söylediyse
- Yaşadığı yerin havası ve genel mizaç — kullanıcı söylediyse

İçermez:
- Gerçek bir kişinin adı, markası, kurumu ya da tanınabilir bir yaşam öyküsü
- Yaşla çelişen ayrıntı (on yaşındaki karaktere meslek yazılmaz)
- Müstehcen, cinsel ya da şiddet içeren bağlam
- Çocuk karakterde yetişkin bağlamı — çocuk künyesi okul, oyun ve aile çevresiyle sınırlıdır
- Uydurma kesinlik: kullanıcı söylemediyse doğum yeri, aile durumu, geçmiş olay yazılmaz.
  Bilinmeyen alan **boş geçilir**, doldurulmaz.

Örnek:

```
Altay, otuzlu yaşların başında, zeytin tenli, kare çeneli ve atletik yapılı. Marangoz;
atölyesini babasından devralmış, işini sessiz ve ölçülü yapan biri. İzmir'de yaşıyor.
```

Kullanıcı hiçbir ek bilgi vermediyse künye tek cümleye iner ve yalnızca fiziksel özeti taşır.
Boşluğu kurguyla doldurmak yerine kısa künye yazılır.

## İsimlendirme

Sabittir; kullanıcı aksini istemedikçe değişmez. `<İsim>` görüşmede alınan karakter adıdır.

| Ne | Ad |
|---|---|
| Kareler | `<İsim> <Çekim Türü>.png` |
| Referans sayfası | `<İsim> - Karakter Referans Sayfası.png` |
| Künye | `<İsim> - Künye.md` |
| Arşiv | `<İsim>.zip` |

Çekim türleri `kalite-kontrol.md`'deki adlarla birebir aynıdır — tek fark, `3/4` dosya adında
`3-4` yazılır (`/` dosya sistemi ayracıdır):

```
<İsim> Ön Profil.png          <İsim> Sol 3-4 Portre.png
<İsim> Arka Profil.png        <İsim> Sağ 3-4 Portre.png
<İsim> Ön Portre.png          <İsim> Arka Portre.png
```

Kullanıcı karakter adı vermediyse görüşmenin sonunda bir kez sorulur; yine vermezse `Karakter`
kullanılır. Tarih, model adı, sürüm numarası ya da kare numarası dosya adına yazılmaz.

## Arşiv

Kullanıcıya sohbette **yalnızca `.zip` verilir.** Kareler tek tek dosya olarak sunulmaz — sekiz
ayrı ek, sohbeti okunmaz hâle getirir ve kullanıcının dosyaları toplamasını zorlaştırır.

```bash
python3 scripts/paketle.py --ad "<İsim>" \
  --kareler k1.png k2.png k3.png k4.png k5.png k6.png \
  --sayfa "<İsim> - Karakter Referans Sayfası.png" \
  --kunye "<İsim> - Künye.md"
```

`--kareler` **hücre sırasıyla** verilir (1 Ön Profil, 2 Arka Profil, 3 Ön Portre, 4 Sol 3/4,
5 Sağ 3/4, 6 Arka Portre) — üretim sırasıyla değil. Bu ikisi v2'de farklıdır; karıştırılırsa
dosya adları yanlış kareye yapışır.

Arşiv açıldığında `<İsim>/` klasörü çıkar. Eksik dosya varsa script arşivi kurmaz; yarım
teslimat yapılmaz.

## Aksiyon özeti

Arşiv verildikten sonra kısa bir döküm yazılır. Amacı kullanıcının ne aldığını ve süreçte ne
olduğunu tek bakışta görmesidir. Türkçe, kısa, yorumsuz.

```
Teslim edildi: <İsim>.zip

Karakter   <künyenin ilk cümlesi>
Kareler    6 kare üretildi, <n> yeniden üretim (<hata etiketleri>)
İşlemler   Birleştirme (3840x2160) -> fotografik geçiş -> paketleme
İçerik     6 kare + referans sayfası + künye
Maliyet    <toplam kare sayısı> üretim
```

Kurallar:
- Yeniden üretim olmadıysa satır `6 kare üretildi, yeniden üretim yok` olur — satır silinmez.
- Hata etiketleri gizlenmez; düzeltilip geçilmiş olsa bile yazılır.
- Script'ten uyarı alınmış ve kare yeniden üretilmemişse bu ayrı bir satırda söylenir.
- Övgü, kapanış cümlesi ve öneri eklenmez. Kullanıcı devamında ne isteyeceğini kendisi bilir.
