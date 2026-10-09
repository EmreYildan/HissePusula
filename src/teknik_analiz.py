
import pandas as pd
import numpy as np



# ==========================================
# 1. TEKNIK GOSTERGELERI HESAPLA
# ==========================================

def teknik_gostergeleri_hesapla(veriler):

    # Orijinal veriyi koru
    veriler = veriler.copy()

    # Tarih indeksine gore sirala
    veriler = veriler.sort_index()

    # Yeterli veri kontrolu
    if len(veriler) < 50:
        raise ValueError(
            "MA50 hesaplamak icin en az 50 islem gunu gerekli."
        )

    # Hareketli ortalamalar
    veriler["MA20"] = veriler["Close"].rolling(
        window=20
    ).mean()

    veriler["MA50"] = veriler["Close"].rolling(
        window=50
    ).mean()

    # ======================================
    # RSI14 - Wilder Yontemi
    # ======================================

    donem = 14

    fiyat_degisim = veriler["Close"].diff()

    kazanc = fiyat_degisim.clip(lower=0)
    kayip = -fiyat_degisim.clip(upper=0)

    # Ilk 14 degisimin basit ortalamasi
    ilk_kazanc = kazanc.iloc[1:donem + 1].mean()
    ilk_kayip = kayip.iloc[1:donem + 1].mean()

    # Wilder'in tekrarli ortalama hesabi
    ortalama_kazanc = pd.Series(
        np.nan, index=veriler.index, dtype=float
    )
    ortalama_kayip = pd.Series(
        np.nan, index=veriler.index, dtype=float
    )

    ortalama_kazanc.iloc[donem] = ilk_kazanc
    ortalama_kayip.iloc[donem] = ilk_kayip

    for i in range(donem + 1, len(veriler)):

        ortalama_kazanc.iloc[i] = (
            ortalama_kazanc.iloc[i - 1] * (donem - 1)
            + kazanc.iloc[i]
        ) / donem

        ortalama_kayip.iloc[i] = (
            ortalama_kayip.iloc[i - 1] * (donem - 1)
            + kayip.iloc[i]
        ) / donem

    # Sifira bolme durumlarini ele al
    rs = ortalama_kazanc / ortalama_kayip.replace(0, np.nan)

    veriler["RSI14"] = 100 - (100 / (1 + rs))

    # Hic kayip yoksa RSI = 100
    veriler.loc[
        (ortalama_kayip == 0) & (ortalama_kazanc > 0),
        "RSI14"
    ] = 100

    # Hic kazanc yoksa RSI = 0
    veriler.loc[
        (ortalama_kazanc == 0) & (ortalama_kayip > 0),
        "RSI14"
    ] = 0

    # Hic fiyat degisimi yoksa RSI = 50
    veriler.loc[
        (ortalama_kazanc == 0) & (ortalama_kayip == 0),
        "RSI14"
    ] = 50

    # ======================================
    # MACD (12, 26, 9)
    # ======================================

    # 12 gunluk ustel hareketli ortalama
    ema12 = veriler["Close"].ewm(
        span=12,
        adjust=False
    ).mean()

    # 26 gunluk ustel hareketli ortalama
    ema26 = veriler["Close"].ewm(
        span=26,
        adjust=False
    ).mean()

    # MACD cizgisi
    veriler["MACD"] = ema12 - ema26

    # MACD sinyal cizgisi (9 gunluk EMA)
    veriler["MACD_Sinyal"] = veriler["MACD"].ewm(
        span=9,
        adjust=False
    ).mean()

    # MACD histogrami
    veriler["MACD_Histogram"] = (
        veriler["MACD"] - veriler["MACD_Sinyal"]
    )

    # ======================================
    # MACD KESISIM TESPITI
    # ======================================

    # MACD ve sinyal cizgisi arasindaki fark
    fark = veriler["MACD"] - veriler["MACD_Sinyal"]

    # Bir onceki gunun farki
    onceki_fark = fark.shift(1)

    # Yukari yonlu kesisim
    veriler["MACD_Yukari_Kesisim"] = (
        (onceki_fark <= 0) & (fark > 0)
    )

    # Asagi yonlu kesisim
    veriler["MACD_Asagi_Kesisim"] = (
        (onceki_fark >= 0) & (fark < 0)
    )

    return veriler

    



# ==========================================
# 2. TEKNIK ANALIZI YORUMLA
# ==========================================

def teknik_analizi_yorumla(analiz):

    son = analiz.iloc[-1]

    kapanis = son["Close"]
    ma20 = son["MA20"]
    ma50 = son["MA50"]
    rsi = son["RSI14"]   
    macd = son["MACD"]
    macd_sinyal = son["MACD_Sinyal"]
    macd_histogram = son["MACD_Histogram"]
    
    

    print("\n=== HISSE PUSULA - ANALIZ YORUMU ===")

    print("\nSon kapanis:", round(kapanis, 2))
    print("MA20:", round(ma20, 2))
    print("MA50:", round(ma50, 2))
    print("RSI14:", round(rsi, 2))

    # Trend analizi
    if kapanis > ma20 and kapanis > ma50:
        print("\nTrend: Pozitif gorunum")

    elif kapanis < ma20 and kapanis < ma50:
        print("\nTrend: Negatif gorunum")

    else:
        print("\nTrend: Karisik gorunum")

    # Ortalama iliskisi
    if ma20 > ma50:
        print("Ortalamalar: Kisa vadeli ortalama ustte")

    elif ma20 < ma50:
        print("Ortalamalar: Kisa vadeli ortalama altta")

    else:
        print("Ortalamalar: Esit")

    # RSI analizi
    if rsi < 30:
        print("RSI: Asiri satim bolgesi")

    elif rsi > 70:
        print("RSI: Asiri alim bolgesi")

    elif rsi < 50:
        print("RSI: Momentum zayif")

    else:
        print("RSI: Momentum guclu")


        
    
    # ======================================
    # MACD - ANLASILIR YORUMLAMA
    # ======================================

    print("\n=== MACD - YUKSELIS / DUSUS GUCU ===")

    print(f"MACD degeri: {macd:.4f}")
    print(f"Sinyal degeri: {macd_sinyal:.4f}")
    print(f"Histogram: {macd_histogram:.4f}")

    # 1. MACD ile sinyal cizgisinin iliskisi
    if macd > macd_sinyal:
        print(
            "\nOlumlu isaret: Son fiyat hareketlerinde "
            "yukselis yonundeki ivme gucleniyor olabilir."
        )

    elif macd < macd_sinyal:
        print(
            "\nOlumsuz isaret: Son fiyat hareketlerinde "
            "dus us yonundeki baski artiyor olabilir."
        )

    else:
        print(
            "\nNotr gorunum: Yukselis veya dusus "
            "yonunde belirgin bir ivme farki yok."
        )

    # 2. MACD'nin sifir cizgisine gore konumu
    if macd > 0:
        print(
            "Genel egilim: Son 12 gunun fiyat ortalamasi, "
            "26 gunluk ortalamanin uzerinde. "
            "Bu, yukselis yonunu destekleyen bir isarettir."
        )

    elif macd < 0:
        print(
            "Genel egilim: Son 12 gunun fiyat ortalamasi, "
            "26 gunluk ortalamanin altinda. "
            "Yani onceki dusus etkisi henuz tamamen "
            "ortadan kalkmamis olabilir."
        )

    else:
        print(
            "Genel egilim: Kisa ve uzun vadeli "
            "fiyat ortalamalari birbirine esit."
        )

    # 3. Iki sonucu birlestir
    print("\nMACD GENEL DEGERLENDIRME:")

    if macd > macd_sinyal and macd < 0:
        print(
            "Hissede toparlanma belirtileri var. "
            "Ancak uzun vadeli dusus etkisi devam ediyor olabilir."
        )

    elif macd > macd_sinyal and macd >= 0:
        print(
            "Hem fiyat hareketlerinin ivmesi hem de "
            "MACD'nin genel yonu olumlu gorunuyor."
        )

    elif macd < macd_sinyal and macd > 0:
        print(
            "Genel yukselis gorunumu surse de "
            "son donemde yukselis ivmesi zayifliyor olabilir."
        )

    elif macd < macd_sinyal and macd <= 0:
        print(
            "Hem genel egilim hem de son donem "
            "momentum gorunumu zayif."
        )

    else:
        print("MACD cizgileri birbirine esit.")

        
    # ======================================
    # MACD KESISIM YORUMU
    # ======================================

    print("\n=== MACD KESISIM KONTROLU ===")

    if son["MACD_Yukari_Kesisim"]:
        print(
            "Yeni olumlu sinyal: MACD bugun sinyal "
            "cizgisini yukari kesti. Yukselis yonundeki "
            "momentum gucleniyor olabilir."
        )

    elif son["MACD_Asagi_Kesisim"]:
        print(
            "Yeni olumsuz sinyal: MACD bugun sinyal "
            "cizgisini asagi kesti. Dusus yonundeki "
            "momentum gucleniyor olabilir."
        )

    else:
        print(
            "Bugun yeni bir MACD kesisimi olusmadi."
        )

        if son["MACD"] > son["MACD_Sinyal"]:
            print(
                "MACD sinyal cizgisinin uzerinde. "
                "Olumlu momentum gorunumu devam ediyor."
            )

        elif son["MACD"] < son["MACD_Sinyal"]:
            print(
                "MACD sinyal cizgisinin altinda. "
                "Zayif momentum gorunumu devam ediyor."
            )


    # ======================================
    # SON MACD KESISIM TARIHI
    # ======================================

    kesisimler = analiz[
        analiz["MACD_Yukari_Kesisim"] |
        analiz["MACD_Asagi_Kesisim"]
    ]

    print("\n=== SON MACD KESISIMI ===")

    if not kesisimler.empty:
        son_kesisim = kesisimler.iloc[-1]
        son_tarih = kesisimler.index[-1]

        print(
            "Kesisim tarihi:",
            son_tarih.strftime("%d.%m.%Y")
        )

        if son_kesisim["MACD_Yukari_Kesisim"]:
            print("Kesisim yonu: YUKARI")
            print(
                "Bu tarihte MACD sinyal cizgisinin "
                "uzerine cikti."
            )
        else:
            print("Kesisim yonu: ASAGI")
            print(
                "Bu tarihte MACD sinyal cizgisinin "
                "altina indi."
            )

    else:
        print("Veri araliginda MACD kesisimi bulunamadi.")




