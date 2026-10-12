
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
