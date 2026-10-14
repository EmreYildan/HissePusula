
import numpy as np
import pandas as pd


def risk_analizi_hesapla(veriler):
    """
    Hissenin gecmis fiyat verilerinden
    risk gostergelerini hesaplar.

    Hesaplanan degerler:
    - Gunluk getiri (%)
    - Yilliklandirilmis volatilite (%)
    - Zirveden dusus / Drawdown (%)
    - Maksimum dusus / Max Drawdown (%)
    """

    sonuc = veriler.copy()
    sonuc = sonuc.sort_index()

    kapanis = sonuc["Close"]

    # 1. Gunluk yuzdesel getiri
    sonuc["Gunluk_Getiri"] = (
        kapanis.pct_change(fill_method=None) * 100
    )

    # 2. Son 252 islem gununun
    # yilliklandirilmis volatilitesi
    sonuc["Volatilite_252"] = (
        sonuc["Gunluk_Getiri"]
        .rolling(window=252, min_periods=252)
        .std(ddof=1)
        * np.sqrt(252)
    )

    # 3. O ana kadarki en yuksek kapanis
    zirve = kapanis.cummax()

    # 4. Zirveden yuzdesel dusus
    sonuc["Drawdown"] = (
        (kapanis / zirve) - 1
    ) * 100

    # 5. O ana kadarki en buyuk dusus
    sonuc["Max_Drawdown"] = (
        sonuc["Drawdown"].cummin()
    )

    return sonuc



def donemsel_maksimum_dusus_hesapla(veriler):
    """
    Son 6, 12 ve 24 aylik donemlerdeki
    maksimum zirveden dususu hesaplar.

    Donemler:
    6 ay  = 126 islem gunu
    12 ay = 252 islem gunu
    24 ay = 504 islem gunu

    Her donem icin baslangic fiyati da
    hesaba katilir.
    """

    sonuc = veriler.copy()
    sonuc = sonuc.sort_index()

    kapanis = sonuc["Close"]

    donemler = {
        "MDD_6A": 126,
        "MDD_12A": 252,
        "MDD_24A": 504
    }

    for sutun, gun_sayisi in donemler.items():

        # Baslangic dahil N+1 fiyat gozlemi
        pencere = gun_sayisi + 1

        def maksimum_dusus(fiyatlar):
            zirve = np.maximum.accumulate(fiyatlar)

            dusus = (
                fiyatlar / zirve - 1
            ) * 100

            return np.min(dusus)

        sonuc[sutun] = kapanis.rolling(
            window=pencere,
            min_periods=pencere
        ).apply(
            maksimum_dusus,
            raw=True
        )

    return sonuc

# ==========================================
# DONEMSEL VOLATILITE HESAPLAMA
# ==========================================

def donemsel_volatilite_hesapla(veriler):
    """
    Son 6, 12 ve 24 aylik donemler icin
    yilliklandirilmis volatilite hesaplar.

    6 ay  = 126 gunluk getiri
    12 ay = 252 gunluk getiri
    24 ay = 504 gunluk getiri

    Sonuclar yuzde cinsindendir.
    """

    sonuc = veriler.copy()
    sonuc = sonuc.sort_index()

    kapanis = sonuc["Close"]

    # Gunluk yuzdesel getiriler
    gunluk_getiri = (
        kapanis.pct_change(fill_method=None) * 100
    )

    donemler = {
        "Volatilite_6A": 126,
        "Volatilite_12A": 252,
        "Volatilite_24A": 504
    }

    for sutun, gun_sayisi in donemler.items():

        sonuc[sutun] = (
            gunluk_getiri
            .rolling(
                window=gun_sayisi,
                min_periods=gun_sayisi
            )
            .std(ddof=1)
            * np.sqrt(252)
        )

    return sonuc
