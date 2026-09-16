#!/usr/bin/env python3
"""
paketle.py - teslimatı tek bir .zip hâline getirir.

Kullanıcıya altı kare, sayfa ve künye ayrı dosyalar olarak verilmez; hepsi tek arşivde
toplanır. İsimlendirme references/teslimat.md'de sabitlenmiştir:

    Kareler  ->  <İsim> <Çekim Türü>.png
    Sayfa    ->  <İsim> - Karakter Referans Sayfası.png
    Künye    ->  <İsim> - Künye.md
    Arşiv    ->  <İsim>.zip        (açıldığında <İsim>/ klasörü çıkar)

TEMEL KURAL: bu script de içeriğe dokunmaz. Yeniden kodlamaz, ölçeklemez, sıkıştırma ile
görüntü kalitesini düşürmez - dosyaları olduğu gibi kopyalar. Eksik dosya varsa arşiv
kurulmaz; yarım teslimat yapılmaz.

Kullanım:
  python3 paketle.py --ad "Altay" \
      --kareler k1.png k2.png k3.png k4.png k5.png k6.png \
      --sayfa "Altay - Karakter Referans Sayfası.png" \
      --kunye kunye.md
"""

import argparse
import os
import sys
import zipfile

# birlestir.py ile birebir aynı sıra ve adlar (hücre no 1..6).
KARE_ADLARI = ["Ön Profil", "Arka Profil", "Ön Portre",
               "Sol 3/4 Portre", "Sağ 3/4 Portre", "Arka Portre"]


def dosya_adi(ad):
    """Çekim türünü dosya adına çevirir; '/' dosya sistemi ayracı olduğu için '-' olur."""
    return ad.replace("/", "-")


def uzanti(yol, varsayilan):
    u = os.path.splitext(yol)[1]
    return u if u else varsayilan


def girdileri_kur(ad, kareler, sayfa, kunye):
    """(kaynak yol, arşiv içi yol) çiftlerini sırayla üretir."""
    girdiler = []
    for i, kare in enumerate(kareler):
        girdiler.append((kare, f"{ad} {dosya_adi(KARE_ADLARI[i])}{uzanti(kare, '.png')}"))
    girdiler.append((sayfa, f"{ad} - Karakter Referans Sayfası{uzanti(sayfa, '.png')}"))
    if kunye:
        girdiler.append((kunye, f"{ad} - Künye{uzanti(kunye, '.md')}"))
    return girdiler


def main():
    p = argparse.ArgumentParser(description="Teslimatı tek .zip hâline getirir.")
    p.add_argument("--ad", required=True, help="karakter adı; bütün dosya adlarının önekidir")
    p.add_argument("--kareler", nargs=6, required=True, help="1..6 sırasıyla kare dosyaları")
    p.add_argument("--sayfa", required=True, help="birlestir.py + foto_ayar.py çıktısı")
    p.add_argument("--kunye", default=None, help="künye metni (.md)")
    p.add_argument("-o", "--cikti", default=None, help="arşiv yolu; varsayılan <İsim>.zip")
    a = p.parse_args()

    girdiler = girdileri_kur(a.ad, a.kareler, a.sayfa, a.kunye)

    eksik = [k for k, _ in girdiler if not os.path.exists(k)]
    if eksik:
        sys.exit("bulunamadi: " + ", ".join(eksik))

    cikti = a.cikti or f"{a.ad}.zip"
    # Dosya adları Türkçe karakter taşıdığı için zipfile UTF-8 bayrağını kendisi kurar.
    with zipfile.ZipFile(cikti, "w", zipfile.ZIP_DEFLATED) as z:
        for kaynak, hedef in girdiler:
            z.write(kaynak, f"{a.ad}/{hedef}")
            print(f"  + {hedef}")

    boyut = os.path.getsize(cikti) / 1024 / 1024
    print(f"Yazildi: {cikti}  ({len(girdiler)} dosya, {boyut:.1f} MB)")


if __name__ == "__main__":
    main()
