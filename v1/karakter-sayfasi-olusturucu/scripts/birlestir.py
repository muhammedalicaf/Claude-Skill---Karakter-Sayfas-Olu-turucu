#!/usr/bin/env python3
"""
birlestir.py - altı kareyi tek karakter sayfası hâline getirir.

Düzen references/sayfa-duzeni.md ile birebir aynıdır: dört eşit sütun, sol iki sütun tam
yükseklik (tam boy kareler), sağ iki sütun ortadan bölünmüş (dört portre karesi).

TEMEL KURAL: bu script karelerin içeriğine müdahale etmez. Yaptığı iş yalnızca ölçeklemek,
kırpmak ve yerleştirmektir. Arka plan düzeltilmez, gölge silinmez, ton değiştirilmez, boşluk
doldurulmaz. Kare bozuksa çözüm fotomontaj değil yeniden üretimdir; script yalnızca uyarır.

Hizalama:
  - Portre kareleri (3-6): duvar renginden karakter ayrıştırılıp kafa genişliği ölçülür, dört
    portre aynı kafa ölçüsüne getirilir. Ölçüm güvenilir değilse kare ortalanır ve uyarı basılır.
  - Tam boy kareler (1-2): ölçüm yapılmaz. Kadraj promptla kurulur, script yalnızca hücre
    oranına kırpar. Zemin ile duvar ayrı tonlarda olduğu için otomatik ölçüm güvenilir değil.

Kullanım:
  python3 birlestir.py k1.png k2.png k3.png k4.png k5.png k6.png --ad "Mert"
"""

import argparse
import os
import sys
from datetime import date

import numpy as np
from PIL import Image
from scipy import ndimage

# --- sayfa-duzeni.md sabitleri ---
AYRAC_RENK = (20, 20, 20)      # #141414
AYRAC_ORAN = 0.0023            # tuval genişliğine göre ayraç kalınlığı

PORTRE_UST = 0.08              # portre: baş üstü boşluk (hücre yüksekliğinin oranı)
PORTRE_KAFA = 0.40             # portre: hedef kafa genişliği / hücre genişliği
KAFA_ESIK = 26.0               # duvardan sapma eşiği (öklid uzaklık)
EN_KUCUK_LEKE = 0.01           # maskede tutulacak en küçük bileşen (piksel oranı)
OLCEK_SINIR = (0.5, 2.0)       # bu aralık dışına çıkan ölçüm güvenilmez sayılır

KARE_ADLARI = ["Ön Profil", "Arka Profil", "Ön Portre",
               "Sol 3/4 Portre", "Sağ 3/4 Portre", "Arka Portre"]


def duvar_rengi(a):
    """Üst köşelerden duvar rengi. Portre kadrajında üst köşelerde yalnızca duvar vardır."""
    k = max(8, min(a.shape[0], a.shape[1]) // 20)
    kose = np.concatenate([a[:k, :k].reshape(-1, 3), a[:k, -k:].reshape(-1, 3)])
    return np.median(kose, axis=0).astype(np.float32)


def kafa_olcusu(a):
    """(kafa genişliği, tepe y) döndürür; ölçülemezse None."""
    duvar = duvar_rengi(a)
    fark = np.linalg.norm(a.astype(np.float32) - duvar, axis=2)
    m = ndimage.binary_opening(fark > KAFA_ESIK, np.ones((5, 5)))
    etiket, adet = ndimage.label(m)
    if adet == 0:
        return None
    boyutlar = ndimage.sum(m, etiket, range(1, adet + 1))
    en_buyuk = int(np.argmax(boyutlar)) + 1
    if boyutlar[en_buyuk - 1] < m.size * EN_KUCUK_LEKE:
        return None
    m = ndimage.binary_fill_holes(etiket == en_buyuk)

    ys = np.nonzero(m.any(axis=1))[0]
    if ys.size < 10:
        return None
    tepe, dip = int(ys[0]), int(ys[-1])
    boy = dip - tepe
    genislikler = []
    for y in range(tepe + int(boy * 0.10), tepe + max(1, int(boy * 0.28))):
        x = np.nonzero(m[y])[0]
        if x.size:
            genislikler.append(x[-1] - x[0] + 1)
    if not genislikler:
        return None
    return float(np.median(genislikler)), tepe


def kirp(a, hucre_w, hucre_h, olcek=None, tepe=None, ust_bosluk=None):
    """Kareyi hücreye kırpar. Ölçek verilmezse hücreyi kaplayan en küçük ölçek kullanılır."""
    h, w = a.shape[:2]
    kapla = max(hucre_w / w, hucre_h / h)
    if olcek is None or olcek < kapla:
        olcek = kapla
        tepe = None
    yeni = (max(1, int(round(w * olcek))), max(1, int(round(h * olcek))))
    b = np.array(Image.fromarray(a).resize(yeni, Image.LANCZOS))

    x0 = int(round((b.shape[1] - hucre_w) / 2))
    if tepe is None or ust_bosluk is None:
        y0 = int(round((b.shape[0] - hucre_h) / 2))
    else:
        y0 = int(round(tepe * olcek - ust_bosluk))
    x0 = max(0, min(x0, b.shape[1] - hucre_w))
    y0 = max(0, min(y0, b.shape[0] - hucre_h))
    return b[y0:y0 + hucre_h, x0:x0 + hucre_w], olcek


def kareyi_hazirla(yol, hucre_w, hucre_h, portre):
    a = np.array(Image.open(yol).convert("RGB"))
    uyarilar = []

    if a.shape[1] < hucre_w or a.shape[0] < hucre_h:
        uyarilar.append("kare hücreden küçük - daha yüksek çözünürlükte yeniden üret")

    istenen, tepe = None, None
    if portre:
        olcum = kafa_olcusu(a)
        if olcum is None:
            uyarilar.append("kafa ölçülemedi - hizalama yapılmadı, kare ortalandı")
        else:
            kafa, tepe = olcum
            istenen = (hucre_w * PORTRE_KAFA) / max(1.0, kafa)
            if not (OLCEK_SINIR[0] <= istenen <= OLCEK_SINIR[1]):
                uyarilar.append(f"ölçüm sınır dışı ({istenen:.2f}) - kadraj bozuk olabilir")
                istenen, tepe = None, None

    hucre, olcek = kirp(a, hucre_w, hucre_h, istenen, tepe,
                        hucre_h * PORTRE_UST if portre else None)
    bilgi = f"{a.shape[1]}x{a.shape[0]} -> olcek {olcek:.3f}"
    return Image.fromarray(hucre), bilgi, uyarilar


def dagit(toplam, parca):
    """Kalanı soldan sağa birer piksel dağıtarak tam sayı genişlikler üretir."""
    temel, kalan = divmod(toplam, parca)
    return [temel + (1 if i < kalan else 0) for i in range(parca)]


def sayfayi_kur(yollar, genislik, yukseklik):
    g = max(2, round(genislik * AYRAC_ORAN))
    sayfa = Image.new("RGB", (genislik, yukseklik), AYRAC_RENK)

    sutunlar = dagit(genislik - 5 * g, 4)
    tam_h = yukseklik - 2 * g
    portre_h = dagit(yukseklik - 3 * g, 2)

    x, xler = g, []
    for w in sutunlar:
        xler.append(x)
        x += w + g

    yerlesim = [
        (0, xler[0], g, sutunlar[0], tam_h, False),
        (1, xler[1], g, sutunlar[1], tam_h, False),
        (2, xler[2], g, sutunlar[2], portre_h[0], True),
        (3, xler[3], g, sutunlar[3], portre_h[0], True),
        (4, xler[2], g * 2 + portre_h[0], sutunlar[2], portre_h[1], True),
        (5, xler[3], g * 2 + portre_h[0], sutunlar[3], portre_h[1], True),
    ]

    sorunlu = []
    for i, hx, hy, hw, hh, portre in yerlesim:
        hucre, bilgi, uyarilar = kareyi_hazirla(yollar[i], hw, hh, portre)
        sayfa.paste(hucre, (hx, hy))
        print(f"  {i + 1} {KARE_ADLARI[i]:<16} {hw}x{hh}  {bilgi}")
        for u in uyarilar:
            print(f"      ! {u}")
            sorunlu.append(KARE_ADLARI[i])

    return sayfa, sorted(set(sorunlu))


def main():
    p = argparse.ArgumentParser(description="Altı kareyi karakter sayfasına birleştirir.")
    p.add_argument("kareler", nargs=6, help="1..6 sırasıyla kare dosyaları")
    p.add_argument("-o", "--cikti", default=None)
    p.add_argument("--ad", default="karakter")
    p.add_argument("--genislik", type=int, default=2560)
    p.add_argument("--yukseklik", type=int, default=1440)
    a = p.parse_args()

    for y in a.kareler:
        if not os.path.exists(y):
            sys.exit(f"bulunamadi: {y}")

    print(f"Sayfa kuruluyor: {a.genislik}x{a.yukseklik}")
    sayfa, sorunlu = sayfayi_kur(a.kareler, a.genislik, a.yukseklik)

    cikti = a.cikti or f"karakter-sayfasi_{a.ad}_{date.today():%Y%m%d}.png"
    sayfa.save(cikti)
    print(f"Yazildi: {cikti}")
    if sorunlu:
        print("Uyari alan kareler: " + ", ".join(sorunlu))


if __name__ == "__main__":
    main()
