#!/usr/bin/env python3
"""
foto_ayar.py - sayfanın tamamına tek bir fotografik geçiş uygular.

Adobe Lightroom'da yapılan şu ayarların karşılığıdır:

    Işık:  Pozlama -0,40   Kontrast -4
    Renk:  Sıcaklık -4   Renk Tonu -4   Canlılık -4   Doygunluk -4
    Gren:  Miktar +5   Boyut +25   Pürüzlülük +50

KURAL: bu script bölgesel rötuş yapmaz. Maske yok, fon düzeltme yok, gölge silme yok, yüz
rötuşu yok. Görüntünün tamamına aynı geçiş uygulanır; amacı altı karenin tek bir çekimden
çıkmış gibi durmasıdır. Bir kare bozuksa çözüm burada değil, yeniden üretimdedir.

KALİBRASYON: sabitler teoriden değil ölçümden gelir. Aynı görselin Lightroom öncesi ve sonrası
hâli (2048x2048) karşılaştırılıp boru hattı bu çifte uydurulmuştur. Lightroom'un slider'ları
kendi ton eğrisiyle birlikte çalıştığı için -0,40 EV saf bir doğrusal çarpan değildir; ölçülen
toplam etki buradaki sabitlere gömülüdür. Varsayılan değerlerle çalıştırıldığında çıktı referansı
yeniden üretir; değerler değiştirildiğinde davranış makul ama yaklaşıktır.

Doğrulama:
  python3 foto_ayar.py once.png -o cikti.png --dogrula sonra.jpg

Kullanım:
  python3 foto_ayar.py sayfa.png -o sayfa_ayarli.png
"""

import argparse
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

# --- ölçümden gelen sabitler ---
# Referans çiftine uydurulan doğrusal ışık kazançları; pozlama -0,40 ile sıcaklık/renk tonu
# -4/-4'ün birlikte ölçülen toplam etkisidir. Lightroom slider'ları kendi ton eğrisiyle
# çalıştığı için bu değerler saf 2^-0.40'tan farklıdır; ölçüm neyse o yazılmıştır.
TABAN_KAZANC = (0.7604, 0.8064, 0.8427)
VARSAYILAN_POZLAMA = -0.40
VARSAYILAN_SICAKLIK = -4
VARSAYILAN_TON = -4

SICAKLIK_BIRIM = 0.01284  # varsayılandan sapma: birim başına log kazanç (R artı, B eksi)
TON_BIRIM = 0.01550       # varsayılandan sapma: birim başına log kazanç (G eksi, R ve B yarısı)
KONTRAST_BIRIM = -0.0454  # birim başına S eğrisi katsayısı (negatif slider = yumuşama)
DOYGUNLUK_BIRIM = 0.0121  # birim başına doygunluk kaybı
CANLILIK_BIRIM = 0.0121   # birim başına canlılık kaybı (düşük doygunluklu piksellere ağırlıklı)
GREN_BIRIM = 0.00165      # miktar birimi başına gren standart sapması (0-1 ölçeğinde)

W = np.array([0.2126, 0.7152, 0.0722])


def s2l(x):
    """sRGB -> doğrusal ışık."""
    return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)


def l2s(x):
    """Doğrusal ışık -> sRGB."""
    x = np.clip(x, 0, 1)
    return np.where(x <= 0.0031308, x * 12.92, 1.055 * x ** (1 / 2.4) - 0.055)


def kanal_kazanclari(pozlama, sicaklik, ton):
    """Pozlama + beyaz ayarını doğrusal ışıkta kanal kazançlarına çevirir.

    Varsayılan slider takımında (-0,40 / -4 / -4) doğrudan ölçülen kazançları verir. Slider'lar
    varsayılandan saptığında fark, birim başına katsayılarla bu tabanın üstüne bindirilir."""
    ln = np.log(np.array(TABAN_KAZANC))
    ln = ln + np.log(2) * (pozlama - VARSAYILAN_POZLAMA)     # fazladan EV

    ds = sicaklik - VARSAYILAN_SICAKLIK                      # + sıcak: R artar, B azalır
    dt = ton - VARSAYILAN_TON                                # + ton: G azalır, R ve B artar
    ln = ln + np.array([SICAKLIK_BIRIM * ds, 0.0, -SICAKLIK_BIRIM * ds])
    ln = ln + np.array([TON_BIRIM * dt / 2, -TON_BIRIM * dt, TON_BIRIM * dt / 2])
    return np.exp(ln)


def s_egrisi(y, kontrast):
    """Orta tonlarda etkili, uçlarda sönen yumuşak S eğrisi. Negatif slider düzleştirir."""
    k = KONTRAST_BIRIM * kontrast
    return y + k * (y - 0.5) * (1 - np.abs(y - 0.5) * 2)


def doygunluk_uygula(y, canlilik, doygunluk):
    """Doygunluk bütün piksellere, canlılık düşük doygunluklu piksellere ağırlıklı uygulanır."""
    L = (y * W).sum(axis=2, keepdims=True)
    fark = y - L
    d = 1 + DOYGUNLUK_BIRIM * doygunluk
    if canlilik:
        mevcut = np.abs(fark).max(axis=2, keepdims=True) / np.maximum(L, 1e-6)
        agirlik = np.clip(1 - mevcut, 0, 1)             # gri pikselde 1, doygunda 0'a iner
        d = d + CANLILIK_BIRIM * canlilik * agirlik
    return L + fark * d


def gren_uygula(y, miktar, boyut, puruzluluk, tohum=0):
    """Tek kanallı (parlaklık) gren. Boyut tane inceliğini, pürüzlülük ince/kaba karışımını verir."""
    if miktar <= 0:
        return y
    rng = np.random.default_rng(tohum)
    h, w = y.shape[:2]
    sigma = 0.25 + (boyut / 100) * 1.4                  # boyut 25 -> ~0.6 px
    ince = ndimage.gaussian_filter(rng.standard_normal((h, w)), sigma)
    kaba = ndimage.gaussian_filter(rng.standard_normal((h, w)), sigma * 3)
    p = np.clip(puruzluluk / 100, 0, 1)
    n = ince * (1 - p * 0.4) + kaba * (p * 0.4)
    n /= max(n.std(), 1e-9)

    L = (y * W).sum(axis=2, keepdims=True)
    agirlik = 1 - (2 * L - 1) ** 2 * 0.45               # orta tonlarda güçlü, uçlarda zayıf
    return y + (n[..., None] * agirlik) * (GREN_BIRIM * miktar)


def uygula(a, pozlama=-0.40, kontrast=-4, sicaklik=-4, ton=-4,
           canlilik=-4, doygunluk=-4, gren_miktar=5, gren_boyut=25,
           gren_puruzluluk=50, tohum=0):
    x = a.astype(np.float64) / 255
    y = l2s(s2l(x) * kanal_kazanclari(pozlama, sicaklik, ton))
    y = s_egrisi(y, kontrast)
    y = doygunluk_uygula(y, canlilik, doygunluk)
    y = gren_uygula(y, gren_miktar, gren_boyut, gren_puruzluluk, tohum)
    return (np.clip(y, 0, 1) * 255).round().astype(np.uint8)


def main():
    p = argparse.ArgumentParser(description="Sayfaya Lightroom karşılığı geçişi uygular.")
    p.add_argument("girdi")
    p.add_argument("-o", "--cikti", default=None)
    p.add_argument("--pozlama", type=float, default=-0.40)
    p.add_argument("--kontrast", type=float, default=-4)
    p.add_argument("--sicaklik", type=float, default=-4)
    p.add_argument("--ton", type=float, default=-4)
    p.add_argument("--canlilik", type=float, default=-4)
    p.add_argument("--doygunluk", type=float, default=-4)
    p.add_argument("--gren-miktar", type=float, default=5)
    p.add_argument("--gren-boyut", type=float, default=25)
    p.add_argument("--gren-puruzluluk", type=float, default=50)
    p.add_argument("--tohum", type=int, default=0)
    p.add_argument("--dogrula", default=None, help="referans çıktı ile karşılaştır")
    a = p.parse_args()

    if not os.path.exists(a.girdi):
        sys.exit(f"bulunamadi: {a.girdi}")

    kaynak = np.asarray(Image.open(a.girdi).convert("RGB"))
    sonuc = uygula(kaynak, a.pozlama, a.kontrast, a.sicaklik, a.ton,
                   a.canlilik, a.doygunluk, a.gren_miktar, a.gren_boyut,
                   a.gren_puruzluluk, a.tohum)

    cikti = a.cikti or os.path.splitext(a.girdi)[0] + "_ayarli.png"
    Image.fromarray(sonuc).save(cikti)
    print(f"Yazildi: {cikti}")

    if a.dogrula:
        ref = Image.open(a.dogrula).convert("RGB")
        if ref.size != (sonuc.shape[1], sonuc.shape[0]):
            ref = ref.resize((sonuc.shape[1], sonuc.shape[0]), Image.LANCZOS)
        R = np.asarray(ref).astype(np.float64)
        S = sonuc.astype(np.float64)
        print(f"  ortalama mutlak hata : {np.abs(S - R).mean():.2f}/255")
        print(f"  kanal ortalamalari   : script {S.mean(axis=(0,1)).round(2)}"
              f"  referans {R.mean(axis=(0,1)).round(2)}")
        print(f"  kanal std            : script {S.std(axis=(0,1)).round(2)}"
              f"  referans {R.std(axis=(0,1)).round(2)}")


if __name__ == "__main__":
    main()
