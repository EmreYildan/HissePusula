
import pandas as pd


def gecmis_getirileri_hesapla(veriler):
    """
    Hissenin son 6, 12 ve 24 aylik
    yaklasik fiyat getirilerini hesaplar.

    6 ay  = 126 islem gunu
    12 ay = 252 islem gunu
    24 ay = 504 islem gunu
    """

    sonuc = veriler.copy()
    sonuc = sonuc.sort_index()

    donemler = {
        "Getiri_6A": 126,
        "Getiri_12A": 252,
        "Getiri_24A": 504
    }

    for sutun, gun_sayisi in donemler.items():
        sonuc[sutun] = (
            sonuc["Close"]
            / sonuc["Close"].shift(gun_sayisi)
            - 1
        ) * 100

    return sonuc
