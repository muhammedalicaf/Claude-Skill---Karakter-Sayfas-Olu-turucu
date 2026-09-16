# Prompt Mimarisi

Altı karenin nasıl üretileceği. Promptlar **İngilizce** yazılır (görsel modelleri İngilizce
betimlemeyi belirgin biçimde daha iyi karşılıyor); kullanıcıyla konuşma dili Türkçedir.

## Platform ve parametreler

Üretim **Replicate** üzerinden yapılır.

| | Değer |
|---|---|
| Model | `google/nano-banana-pro` |
| Çözünürlük | `resolution: "2K"` — büyük harf, `"1K"`/`"2K"`/`"4K"` dışında değer reddedilir |
| Çıktı | `output_format: "png"` |
| Oran: kare 1 ve 2 | `aspect_ratio: "9:16"` |
| Oran: kare 3-6 | `aspect_ratio: "1:1"` |
| Kimlik referansı | `image_input: [<kare 3'ün URL'i>]` |

Her kare ayrı bir istektir. `Prefer: wait` ile çağrıldığında sonuç aynı yanıtta döner.

Çıktı bağlantıları **geçicidir**; birleştirme yapılacaksa kareler ilk fırsatta indirilmelidir.

## Tutarlılık zinciri

Tek prompt tutarlılık getirmez; kimlik ilk kareye bağlanır.

1. **Kare 3 (ön portre)** önce üretilir. Kullanıcı referans fotoğraf verdiyse o fotoğrafın URL'i
   `image_input` içinde geçer; vermediyse yalnızca metinden üretilir.
2. Kare 3 **kullanıcıya sunulur ve onaylanır.** Onaylanmadan hiçbir kare üretilmez.
3. Kalan beş kare, `image_input` alanında kare 3'ün URL'i ile üretilir.
4. Referans görsel **kimlik metnini geçersiz kılmaz**: B bloğu (kimlik) altı promptta da aynen
   tekrarlanır. Referans + metin birlikte, tek başına her birinden daha kararlı sonuç verir.

Kullanıcıya model adı, parametre adı ya da araç adı gösterilmez.

## Blok sırası

Her prompt tek paragraf, virgülle ayrılmış, şu sırada. Modeller baştaki token'lara daha çok
ağırlık verir: önce kadraj, sonra kimlik, en sonda kalite ve negatif kuyruk.

```
A. VIEW      — kamera açısı, poz, kadraj (kareye özel, aşağıdaki altı şablon)
B. IDENTITY  — karakterin tarifi (bir kez yazılır, altı promptta birebir kopyalanır)
C. WARDROBE  — sabit nötr kıyafet (değişmez)
D. SET       — stüdyo, fon, ışık, ifade (değişmez)
E. MICRO     — mikro detay yığını (değişmez) + karenin gerektirdiği vurgu
F. REALISM   — anti-AI doku motoru (değişmez)
G. NEGATIVE  — negatif kuyruk (değişmez)
```

B bloğu `gorusme.md`'deki profilden üretilir ve **bir kez** yazılıp saklanır. Bir kareyi yeniden
üretirken B bloğu asla yeniden yazılmaz, kopyalanır — yeniden yazmak kimliği kaydırır.

## C — Sabit nötr kıyafet (değişmez)

Kıyafet karakteri değil vücudu okutur; kullanıcı ne tarif ederse etsin bu blok değişmez.

```
wearing a plain white crew-neck cotton t-shirt with no print and no logo, plain black slim-fit
trousers, plain grey low-top sneakers, no jacket, no hat, no jewelry, no watch, no bag,
no accessories
```

Gözlük, karakterin ayrılmaz parçası olsa bile bu sayfada takılmaz — yüz geometrisini gizler.

## D — Set (değişmez)

Fon **sonsuz gri değildir**: gerçek bir stüdyodur, duvar ile zemin ayırt edilir ve ışığın duvara
düşüşü korunur. Fonu boyanmış düz bir yüzeye çevirmek fotoğrafın gerçekçiliğini bozar.

Tam boy kareler (1, 2) — duvar ve zemin birlikte görünür:

```
photographed in a real photography studio, plain mid-grey painted wall behind and a matching
grey studio floor, the wall and the floor distinguishable from each other, natural falloff of
light across the wall, large softbox key light with soft even fill, neutral relaxed expression,
mouth closed, no smile, head level, shoulders square, photographed with an 85mm lens at f/5.6
```

Portre kareleri (3-6) — kadrajda yalnızca duvar kalır:

```
photographed in a real photography studio against a plain mid-grey painted wall with natural
falloff of light across the wall, large softbox key light with soft even fill, neutral relaxed
expression, mouth closed, no smile, head level, shoulders square, photographed with an 85mm lens
at f/5.6
```

Yerde gölge zorunlu değildir; olursa da sorun değil, yoksa da. Zorlanmaz, sonradan silinmez.

85mm ve aynı ışık kurulumu altı karede sabittir: odak uzaklığı ya da ışık yönü değişirse yüz
geometrisi değişir ve kareler aynı kişi olmaktan çıkar.

## E — Mikro detaylar (değişmez)

Sayfayı "üretilmiş" olmaktan çıkarıp fotoğrafa yaklaştıran asıl katman bu.

| Bölge | İstenen |
|---|---|
| Cilt | Gözenekler, ince çizgiler, tüyler, doğal renk geçişleri, hafif kızarıklıklar, düzensiz alanlar, asimetriler |
| Gözler | Mikro kılcal damarlar, doğal renk geçişli gradyan iris, doğal kıvrımlı ve tek tek seçilebilen kirpikler |
| Kaşlar | Doğal şekilli, ayrı ayrı seçilebilen kıllar |
| Burun | Çok hafif tüy ve gözenekler, doğal şekil |
| Ağız | Dudak asimetrisi, mikro kırışıklıklar, yumuşak pembe tonlar, hafif çatlaklar, dudak kenarında doğal renk geçişi |
| Kulaklar | Ciltle uyumlu doğal yapı, kıkırdakta ışık geçirgenliği (SSS), mikro ayva tüyleri, kıvrımlarda derinlik gölgeleri, hafif asimetri |
| Saçlar | Tek renk değil çok tonlu, tek tek seçilebilen tel dokusu, ayrımda görünen saç derisi, mat/doğal ışık kırma |

Prompt karşılığı (değişmez blok):

```
extreme micro detail, skin with visible pores, fine lines, fine vellus hair, natural tonal
transitions, faint natural redness, slightly uneven patches and natural asymmetry, eyes with
micro capillaries in the sclera and a detailed gradient iris with natural color variation and
individually separated naturally curved lashes, eyebrows with naturally shaped individually
distinguishable hairs and slightly irregular edges, nose with very fine vellus hair and visible
pores across the bridge and nostrils, lips with natural asymmetry, fine micro wrinkles, soft pink
tonal range, very faint cracks and a natural color transition at the vermilion border, ears with
natural structure matching the skin texture, subsurface scattering translucency through the
cartilage, micro vellus hair, depth shadows inside the folds and slight natural asymmetry,
multi-tonal hair that is never a single flat color, individually distinguishable strands, faintly
visible scalp texture at the parting, matte natural light refraction with no plastic sheen
```

## F — Gerçekçilik (değişmez)

```
photorealistic unretouched photography, matte-to-natural complexion, naturally muted catchlights,
no digital smoothing, no beauty filter, no airbrushing, no plastic skin, no glossy highlight
blooms, natural anatomy, sharp focus on skin and hair texture detail
```

## G — Negatif kuyruk (değişmez)

```
no text, no watermark, no logo, no caption, no frame, no border, no collage, no split screen,
no multiple panels, no second person, no duplicate figure, no mirrored copy, no mannequin,
no props, no furniture, no background objects, no colored background, no cropped head,
no cropped feet, no extra fingers, no distorted anatomy
```

## A — Altı görünüm şablonu

Her şablonun ikinci bölümü o kareye özel mikro detay vurgusudur; E bloğunun yerine değil,
üstüne eklenir.

**1 — Ön profil (tam boy, önden)**
```
full-body standing photograph of the same person, facing the camera straight on, head-to-toe
framing with the entire body and both feet fully visible and not cropped, feet flat on the
ground, arms relaxed at the sides, palms facing the thighs, weight evenly on both legs, standing
upright, camera at chest height, a small empty margin above the head and below the feet,
micro detail carried through to the forearms and hands: visible skin pores and fine vellus hair
on the forearms, natural knuckle creases, individually readable fingernails, the fabric weave of
the cotton t-shirt visible
```

**2 — Arka profil (tam boy, arkadan)**
```
full-body standing photograph of the same person seen from directly behind, back of the head and
the entire back of the body to the camera, the person does not turn and the face is not visible,
head-to-toe framing with both feet fully visible and not cropped, arms relaxed at the sides,
standing upright, camera at chest height, the same standing height and framing as the front
full-body frame,
micro detail concentrated on the back of the head and the nape: individually distinguishable
multi-tonal hair strands, the natural hairline and taper at the nape, faint scalp texture at the
crown, fine vellus hair on the neck, subsurface scattering through the rims of both ears
```

**3 — Ön portre (baş-omuz, önden)**
```
head-and-shoulders portrait photograph, facing the camera straight on, eyes looking directly into
the lens, head upright and level, shoulders square to the camera, tight framing from the top of
the head to the upper chest,
the full micro detail stack fully resolved and sharp across the face: pores and fine lines on the
forehead, nose and cheeks, micro capillaries in the sclera, gradient iris, separated lashes,
individually distinguishable eyebrow hairs, lip micro wrinkles and vermilion border transition
```

**4 — Sol 3/4 portre (sol yanak kamerada)**
```
head-and-shoulders three-quarter portrait photograph, the head turned about 40 degrees to the
subject's own right so that the subject's LEFT cheek faces the camera and the face is angled
toward the left side of the frame, the far eye and the far cheekbone partially visible, the nose
line clear of the cheek contour, gaze following the direction of the head, shoulders nearly
square to the camera, tight framing from the top of the head to the upper chest,
micro detail concentrated along the near side: pores and vellus hair across the left cheek and
jaw, the left ear fully visible with subsurface scattering through the cartilage, depth shadows
inside the ear folds, nose pores in raking light, lash separation on the near eye
```

**5 — Sağ 3/4 portre (sağ yanak kamerada)**
```
head-and-shoulders three-quarter portrait photograph, the head turned about 40 degrees to the
subject's own left so that the subject's RIGHT cheek faces the camera and the face is angled
toward the right side of the frame, the far eye and the far cheekbone partially visible, the nose
line clear of the cheek contour, gaze following the direction of the head, shoulders nearly
square to the camera, tight framing from the top of the head to the upper chest,
micro detail concentrated along the near side: pores and vellus hair across the right cheek and
jaw, the right ear fully visible with subsurface scattering through the cartilage, depth shadows
inside the ear folds, nose pores in raking light, lash separation on the near eye, the natural
asymmetry between this side and the left side preserved rather than mirrored
```

**6 — Arka portre (baş-omuz, arkadan)**
```
head-and-shoulders photograph of the same person seen from directly behind, the back of the head,
the nape of the neck and the tops of the shoulders to the camera, no part of the face visible,
both ears symmetrically at the edges of the head, hairline and haircut clearly readable, tight
framing from the top of the head to the upper back,
micro detail at maximum on the hair: individually distinguishable multi-tonal strands, growth
direction and crown whorl readable, faint scalp texture between the strands, matte natural
refraction with no plastic sheen, fine vellus hair on the nape, subsurface scattering through
both ear rims
```

## Birleştirilmiş örnek prompt

Kare 4 için, bütün bloklar sırasıyla, gerçekte gönderilen hâliyle. Kimlik bloğu örnektir;
üretimde `gorusme.md` çıktısıyla değişir, geri kalan her şey aynen kalır.

```
head-and-shoulders three-quarter portrait photograph, the head turned about 40 degrees to the
subject's own right so that the subject's LEFT cheek faces the camera and the face is angled
toward the left side of the frame, the far eye and the far cheekbone partially visible, the nose
line clear of the cheek contour, gaze following the direction of the head, shoulders nearly
square to the camera, tight framing from the top of the head to the upper chest, micro detail
concentrated along the near side: pores and vellus hair across the left cheek and jaw, the left
ear fully visible with subsurface scattering through the cartilage, depth shadows inside the ear
folds, nose pores in raking light, lash separation on the near eye,
the identical original character, a man in his early thirties, olive skin, oval face with a
defined jawline and mature adult bone structure, straight nose with a slightly broad tip,
medium-full lips, deep-set hazel eyes with a slight downward outer tilt, thick straight dark
brown eyebrows, short dark brown textured crop with a natural side parting and a clean taper,
light stubble of three days, lean athletic build with square shoulders,
wearing a plain white crew-neck cotton t-shirt with no print and no logo, plain black slim-fit
trousers, plain grey low-top sneakers, no jacket, no hat, no jewelry, no watch, no bag,
no accessories,
photographed in a real photography studio against a plain mid-grey painted wall with natural
falloff of light across the wall, large softbox key light with soft even fill, neutral relaxed
expression, mouth closed, no smile, head level, shoulders square, photographed with an 85mm lens
at f/5.6,
extreme micro detail, skin with visible pores, fine lines, fine vellus hair, natural tonal
transitions, faint natural redness, slightly uneven patches and natural asymmetry, eyes with
micro capillaries in the sclera and a detailed gradient iris with natural color variation and
individually separated naturally curved lashes, eyebrows with naturally shaped individually
distinguishable hairs and slightly irregular edges, nose with very fine vellus hair and visible
pores across the bridge and nostrils, lips with natural asymmetry, fine micro wrinkles, soft pink
tonal range, very faint cracks and a natural color transition at the vermilion border, ears with
natural structure matching the skin texture, subsurface scattering translucency through the
cartilage, micro vellus hair, depth shadows inside the folds and slight natural asymmetry,
multi-tonal hair that is never a single flat color, individually distinguishable strands, faintly
visible scalp texture at the parting, matte natural light refraction with no plastic sheen,
photorealistic unretouched photography, matte-to-natural complexion, naturally muted catchlights,
no digital smoothing, no beauty filter, no airbrushing, no plastic skin, no glossy highlight
blooms, natural anatomy, sharp focus on skin and hair texture detail,
no text, no watermark, no logo, no caption, no frame, no border, no collage, no split screen,
no multiple panels, no second person, no duplicate figure, no mirrored copy, no mannequin,
no props, no furniture, no background objects, no colored background, no cropped head,
no cropped feet, no extra fingers, no distorted anatomy
```

Kare 3 aynı yapıyı kullanır; tek farkı `image_input`'un boş olması ya da kullanıcının referans
fotoğrafını taşımasıdır — henüz bağlanacak bir kimlik karesi yoktur.

## IP güvenliği

Karakter daima özgündür. Kullanıcı gerçek bir kişinin adını verirse o kişinin benzerliği
üretilmez; isim yalnızca genel bir hava olarak alınır ve özgün bir yüz kurulur. Kullanıcı kendi
fotoğrafını yüklediyse bu kural geçerli değildir. Çocuk karakterde referans fotoğraf yolu
kapalıdır (bkz. `gorusme.md`).
