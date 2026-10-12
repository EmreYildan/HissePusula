import pandas as pd
from src.hisse_arama import hisse_kodu_bul
from src.veri_cekme import hisse_verisi_cek
from src.teknik_analiz import (
    teknik_gostergeleri_hesapla,
    teknik_analizi_yorumla
)
from src.veri_kontrol import veri_kontrol_et, son_eksik_gunu_temizle


from src.grafik import (
    fiyat_grafigi_olustur,
    rsi_grafigi_olustur,
    macd_grafigi_olustur,
    birlesik_grafik_olustur
)

from src.getiri_analizi import gecmis_getirileri_hesapla

from src.risk_analizi import risk_analizi_hesapla



def main():

    print("\n=== HISSE PUSULA ===")

    # 1. Kullanici girisi
    arama = input(
        "\nAnaliz etmek istediginiz hisse adi veya kodu: "
    )

    # 2. Hisse adini borsa koduna donustur
    hisse_kodu = hisse_kodu_bul(arama)

    if hisse_kodu is None:
        print("\nHisse bulunamadi.")
        return

    print(f"\nSecilen hisse: {hisse_kodu}")

    # 3. Hisse verilerini cek
    veriler = hisse_verisi_cek(hisse_kodu)

    if veriler is None:
        print("\nHisse verileri alinamadi.")
        return

       
       
 
    # 4. Son islem gunundeki eksik fiyatlari kontrol et
    veriler = son_eksik_gunu_temizle(veriler)

    # 5. Veri kalite kontrolu
    uygun_mu, mesaj = veri_kontrol_et(veriler)

    print(f"\nVERI KONTROLU: {mesaj}")

    if not uygun_mu:
        print("Analiz durduruldu.")
        return

    # 6. Teknik gostergeleri hesapla
    analiz = teknik_gostergeleri_hesapla(veriler)       
    # Uzun vadeli gecmis getirileri hesapla
    analiz = gecmis_getirileri_hesapla(analiz)
    analiz = risk_analizi_hesapla(analiz)   
    son = analiz.iloc[-1]

    print("\n========== UZUN VADELI GETIRI ANALIZI ==========")

    donemler = {
        "6 Aylik": "Getiri_6A",
        "12 Aylik": "Getiri_12A",
        "24 Aylik": "Getiri_24A"
    }

    for donem, sutun in donemler.items():
        deger = son[sutun]

        if pd.isna(deger):
            print(f"{donem} Getiri: Yetersiz gecmis veri")
        else:
            print(f"{donem} Getiri: %{deger:.2f}")


    # ==========================================
    # RISK ANALIZI SONUCLARI
    # ==========================================

    son = analiz.iloc[-1]

    print("\n========== RISK ANALIZI ==========")

    volatilite = son["Volatilite_252"]
    maksimum_dusus = son["Max_Drawdown"]
    guncel_dusus = son["Drawdown"]

    if pd.isna(volatilite):
        print("Yillik Volatilite: Yetersiz veri")
    else:
        print(f"Yillik Volatilite: %{volatilite:.2f}")

    print(f"Maksimum Dusus: %{maksimum_dusus:.2f}")
    print(f"Guncel Zirveden Dusus: %{guncel_dusus:.2f}")

    print("=================================")

    
    print("================================================")

    print("\n=== SON 5 GUN ATR ANALIZI ===")
    print(
        analiz[
            ["Close", "High", "Low", "ATR14", "ATR_Yuzde"]
        ]
        .tail()
        .round(2)
    )


    
    print("\n=== SON 5 GUNLUK HACIM ANALIZI ===")
    print(
        analiz[
            ["Volume", "Hacim_MA20", "Hacim_Orani"]
        ].tail().round(2)
    )


    # 7. Son 5 islem gununu goster
    print("\n=== SON 5 ISLEM GUNU ===")

    print(
        analiz[
            [
                "Close",
                "MA20",
                "MA50",
                "RSI14",
                "MACD",
                "MACD_Sinyal",
                "MACD_Histogram",
                "BB_Orta",
                "BB_Ust",
                "BB_Alt"
            ]
            ].tail().round(2)
        )
    print("\n=== SON 5 GUN DESTEK VE DIRENC ===")
    print(
        analiz[
            ["Close", "Destek20", "Direnc20"]
        ]
        .tail()
        .round(2)
    )
    # 8. Teknik analiz yorumlarini goster
    teknik_analizi_yorumla(analiz)
    #fiyat_grafigi_olustur(analiz, hisse_kodu)
    #rsi_grafigi_olustur(analiz, hisse_kodu)
    #macd_grafigi_olustur(analiz, hisse_kodu)
    
    birlesik_grafik_olustur(analiz, hisse_kodu)

if __name__ == "__main__":
    main()
