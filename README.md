# Claude Skill - Karakter Sayfası Oluşturucu
Claude'a ''Karakter Referans Sayfası (Character Sheets)'' oluşturma yeteneği kazandıran Claude SKILL. Bu yetenek sayesinde Claude; görüşmeyi yönetir,
kareleri tek tek üretir, kalite denetimi yapar, panelleri birleştirir, son bir fotografik geçiş
uygular ve çıktıyı tek bir arşiv olarak teslim eder.

**NOT:** Bu yetenek (v1.0) Claude uygulaması içerisinde ''skill-generator'' yeteneği kullanılarak Opus 5 (High) ile birlikte geliştirilmiştir.

**NOT:** Yetenek Claude Code üzerinden Opus 5 (High) ile birlikte geliştirilmeye devam etmektedir.

**Güncel sürüm: v2.0**

## Özellikler
- **Gelişmiş Mikro Detaylar:** Claude, gözlerde gradyan geçişli iris ve kulaklarda hafif ayva tüylerin bulunması gibi önceden tanımlanmış mikro detayları hazırladığı prompta enjekte eder.
- **4K Çözünürlük:** Her görsel 4K çözünürlükte ayrı ayrı üretilir. Karakter sayfası da benzer şekilde 3840x2160 çözünürlüğe sahiptir.
- **Kalite Kontrol ve Revizyon Mekanizması:** Claude, otonom şekilde her ürettiği görsele tek tek kalite kontrol uygular. Onay almayan görselleri, promptu revize ederek yeniden üretir. Onay konusunda kararsız kaldığı ve kabiliyetlerini aşan durumlarda görseli kullanıcının onayına sunar.
- **Yüksek Tutarlılık:** İlk üretilen portre her görselin temel referansıdır; tam boy kareler ayrıca birbirini besler.
- **Karakter Künyesi:** Üretim bittikten sonra karaktere kısa bir Türkçe künye yazılır ve arşive konur.
- **Tek Dosya Teslimat:** Altı kare, referans sayfası ve künye tek bir `.zip` olarak verilir.
- **Aksiyon Özeti:** Her üretimin sonunda ne üretildiğinin ve süreçte ne olduğunun kısa bir dökümü sunulur.
- **Replicate MCP:** Görsel üretimi MCP aracılığıyla Replicate platformu üzerinden Nano Banana Pro modeli ile gerçekleştirilir.

## İş Akışı
1. **Kullanıcı ile Diyalog:** Karakterin görünümü ve kimliği üzerine soru-cevap formatında, Türkçe diyalog gerçekleştirilir.
2. **Profil Taslağı:** Claude, aldığı cevaplar doğrultusunda hazırladığı profil taslağını kullanıcının onayına sunar.
3. **Referans Görselin Üretimi:** Karakterin ön portresi üretilerek kimlik referansı hazırlanır ve kullanıcıya sunulur. Onay alırsa asıl üretim başlar.
4. **Diğer Görünümlerin Üretimi:** Önce kalan üç portre, ardından iki tam boy kare üretilir. Kimlik yüzde okunduğu için portreler öne alınmıştır; olası bir kimlik kayması zincir bozulmadan görülür.
5. **Panelleri Birleştirme:** Önceden hazırlanmış ve yetenek içerisinde tanımlanmış şablon üzerinden ''python script'' ile görseller mozaik düzeninde birleştirilir.
6. **Fotoğrafik Geçiş:** Adobe Lightroom uygulaması üzerinden kalibre edilmiş ölçüm değerleri ''python script'' formatında uygulanır. Bu işlemdeki amaç yapay zeka görsel modellerinin kronik problemi olan ''aşırı doygun ve PVC görünümü'' azaltmaktır.
7. **Künye ve Paketleme:** Karakterin künyesi yazılır; kareler, sayfa ve künye sabit isimlendirmeyle tek `.zip` hâline getirilir.
8. **Teslim ve Aksiyon Özeti:** Arşiv verilir ve yapılan işlemlerin kısa dökümü sunulur.

## Örnek Workflow
_Aşağıdaki ekran görüntüleri v1 akışına aittir; v2'nin görselleri ilk üretimden sonra güncellenecektir._

_Oluşturma İşlemini Başlatıyoruz_
![Oluşturma İşlemini Başlatıyoruz.](./assets/gorsel_1.jpg)

_Profil Taslağı ve Onay_
![Profil Taslağı ve Onay](./assets/gorsel_2.jpg)

_Kimlik Referansının Üretilmesi ve Onaylanması_
![Kimlik Referansının Üretilmesi ve Onaylanması](./assets/gorsel_3.jpg)

_Üretilen Görsellerin Sunulması_
![Üretilen Görsellerin Sunulması](./assets/gorsel_4.jpg)

_Sohbetin Sonu_
![Sohbetin Sonu](./assets/gorsel_5.jpg)

_Nihai Çıktı_
![Nihai Çıktı](./assets/karakter-sayfasi_altay_20260916_son.png)

## Proje Yapısı
```
karakter-sayfasi-olusturucu/   # v2.0 - güncel sürüm
├── SKILL.md   # Yetenek sayfası
├── references/
│   ├── gorusme.md   # Kullanıcı ile kurulacak diyaloğun genel çerçevesi
│   ├── prompt-mimarisi.md   # Promptların nasıl üretileceği konusunda yarı esnek yarı sabit açıklamalar
│   ├── kalite-kontrol.md   # Üretilen görsellere kalite kontrol uygulama rehberi
│   ├── sayfa-duzeni.md   # Mozaik düzeninin nasıl sağlanacağı ve ızgara yapısı
│   └── teslimat.md   # Künye, isimlendirme, arşivleme ve aksiyon özeti
└── scripts/
    ├── birlestir.py   # Üretilen görselleri panel mantığı ile birleştiren script
    ├── foto_ayar.py   # Fotografik geçiş script'i
    └── paketle.py   # Teslimatı tek .zip hâline getiren script

v1/                            # v1.0 - arşiv, değiştirilmez
└── karakter-sayfasi-olusturucu/
```

## Yol Haritası
### v2.0
- **Gelişmiş Kimlik Atama:** Karakter sayfası oluşturmanın yanı sıra kısa bir kimlik tanımlaması fonksiyonu eklendi.
- **İletişim Dili Optimizasyonu:** Model kullanıcı ile iletişimde bazen İngilizce bazen Türkçe konuşuyordu. Bu sorun düzeltildi.
- **Bildirim Stili Değişikliği:** Loq kayıtları ‘’Summary’’ paneli üzerinden verilirken artık sohbet içerisine yazılıyor.
- **Üretim Sırası Optimizasyonu:** Görsel üretiminde sıralama değiştirilerek karakter tutarlılığında artış sağlandı.
- **Dosya Organizasyonu:** Üretilen görseller tek tek sohbet üzerinden verilirken ‘’.zip’’ formatında sıkıştırılarak organize halde verilmeye başlandı.
- **İsimlendirme Formatı Güncellemesi:** İsimlendirme formatı daha açıklayıcı ve organize olacak şekilde optimize edildi.
- **Kadraj Oranı Esnetildi:** Karakterin kadrajdaki oranı hatası %10 esneklik payı verilerek çözüldü.
- **Poz Optimizasyonu:** Artık karakter çapraz profil görsellerinde sadece kafasını sağa sola çevirmiyor. Tüm vücudunu dönüyor.
- **Çözünürlük Artışı:** Çıktı çözünürlüğü 2K’dan 4K’ya yükseltildi.
- **Aksiyon Özeti:** İşlem tamamlandıktan sonra kullanıcıya kısa bir faliyet raporu veriliyor.
- **Gren Optimizasyonu:** Gren tane boyutu 4K çözünürlüğe uyarlandı.

### v1.0
[`v1/`](./v1/) klasöründe arşivlendi.


## Lisans
Bu proje [MIT Lisansı](LICENSE) ile lisanslanmıştır.
