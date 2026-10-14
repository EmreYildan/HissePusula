
import pandas as pd

from src.hisse_arama import hisse_kodu_bul
from src.veri_cekme import hisse_verisi_cek

from src.veri_kontrol import (
    veri_kontrol_et,
    son_eksik_gunu_temizle,
    eksik_hafta_ici_gunlerini_bul
)

from src.bist_takvimi import (
    bist_tatillerini_filtrele,
    takvimi_eksik_yillari_bul
)

from src.teknik_analiz import (
    teknik_gostergeleri_hesapla,
    teknik_analizi_yorumla
)

from src.getiri_analizi import (
    gecmis_getirileri_hesapla
)

from src.risk_analizi import (
    risk_analizi_hesapla,
    donemsel_maksimum_dusus_hesapla,
    donemsel_volatilite_hesapla
)

from src.grafik import birlesik_grafik_olustur


# ==========================================
# YUZDE FORMATLAMA
# ==========================================

def yuzde_formatla(deger):
    """
    Yuzde degerlerini okunabilir bicimde gosterir.

    Pozitif: +25.50%
    Negatif: -15.20%
    Sifir:    0.00%
    Eksik:   Veri yok
    """

    if pd.isna(deger):
        return "Veri yok"

    isaret = "+" if deger > 0 else ""

    return f"{isaret}{deger:.2f}%"


# ==========================================
# ANA PROGRAM
# ==========================================

def main():

    print("\n=== HISSE PUSULA ===")

    # 1. Kullanici girisi
    arama = input(
        "\nAnaliz etmek istediginiz hisse adi veya kodu: "
    )

    # 2. Hisse kodunu bul
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

    # 4. Son eksik islem gununu temizle
    print("\nTEMIZLEME ONCESI SON 5 GUN:")
    print(veriler.tail())
    veriler = son_eksik_gunu_temizle(veriler)
    
    # Eksik hafta ici tarihlerini kontrol et
    eksik_gunler = eksik_hafta_ici_gunlerini_bul(veriler)
    print("\n===== TATIL FILTRESI SONRASI EKSIK TARIHLER =====")
    eksik_gunler = bist_tatillerini_filtrele(eksik_gunler)

    eksik_takvim_yillari = takvimi_eksik_yillari_bul(veriler)

    if eksik_takvim_yillari:
        print(
            "UYARI: BIST tatil takvimi eksik yillar:",
            eksik_takvim_yillari
        )

    

    print("\n========== EKSIK TARIH KONTROLU ==========")

    print(f"Eksik hafta ici tarihi: {len(eksik_gunler)}")

    print("\nSon 10 eksik tarih:")

    for tarih in eksik_gunler[-10:]:
        print(tarih.strftime("%Y-%m-%d"))

    print("=========================================")

    print("\nTEMIZLEME SONRASI SON 5 GUN:")
    print(veriler.tail())
    # 5. Veri kalite kontrolu
    uygun_mu, mesaj = veri_kontrol_et(veriler)

    print(f"\nVERI KONTROLU: {mesaj}")

    if not uygun_mu:
        print("Analiz durduruldu.")
        return

    # ==========================================
    # 6. TUM ANALIZLERI HESAPLA
    # ==========================================

    analiz = teknik_gostergeleri_hesapla(veriler)

    analiz = gecmis_getirileri_hesapla(analiz)

    analiz = risk_analizi_hesapla(analiz)

    analiz = donemsel_maksimum_dusus_hesapla(analiz)

    analiz = donemsel_volatilite_hesapla(analiz)

    son = analiz.iloc[-1]

    print("\n========== VERI SETI KONTROLU ==========")
    print(f"Toplam islem gunu: {len(analiz)}")
    print(f"Ilk tarih: {analiz.index.min()}")
    print(f"Son tarih: {analiz.index.max()}")
    print(f"Eksik kapanis sayisi: {analiz['Close'].isna().sum()}")
    print("========================================")

    # ==========================================
    # 7. UZUN VADELI GETIRI ANALIZI
    # ==========================================

    print("\n========== UZUN VADELI GETIRI ANALIZI ==========")

    getiri_donemleri = {
        "6 Aylik": "Getiri_6A",
        "12 Aylik": "Getiri_12A",
        "24 Aylik": "Getiri_24A"
    }

    for donem, sutun in getiri_donemleri.items():

        deger = son[sutun]

        print(
            f"{donem} Getiri: {yuzde_formatla(deger)}"
        )

    print("================================================")

    # ==========================================
    # 8. GENEL RISK ANALIZI
    # ==========================================

    print("\n========== RISK ANALIZI ==========")

    volatilite = son["Volatilite_252"]

    maksimum_dusus = son["Max_Drawdown"]

    guncel_dusus = son["Drawdown"]

    print(
        "Yillik Volatilite: "
        f"{yuzde_formatla(volatilite)}"
    )

    print(
        "Maksimum Dusus (Tum Gecmis): "
        f"{yuzde_formatla(maksimum_dusus)}"
    )

    print(
        "Guncel Zirveden Dusus: "
        f"{yuzde_formatla(guncel_dusus)}"
    )

    print("=================================")

    # ==========================================
    # 9. DONEMSEL GETIRI / RISK KARSILASTIRMASI
    # ==========================================

    print(
        "\n========== DONEMSEL GETIRI / RISK =========="
    )

    print(
        f"{'Donem':<12}"
        f"{'Getiri':>14}"
        f"{'Volatilite':>16}"
        f"{'Maks. Dusus':>16}"
    )

    print("-" * 58)

    donemler = [
        (
            "6 Ay",
            "Getiri_6A",
            "Volatilite_6A",
            "MDD_6A"
        ),
        (
            "12 Ay",
            "Getiri_12A",
            "Volatilite_12A",
            "MDD_12A"
        ),
        (
            "24 Ay",
            "Getiri_24A",
            "Volatilite_24A",
            "MDD_24A"
        )
    ]

    for ad, getiri, volatilite, mdd in donemler:

        print(
            f"{ad:<12}"
            f"{yuzde_formatla(son[getiri]):>14}"
            f"{yuzde_formatla(son[volatilite]):>16}"
            f"{yuzde_formatla(son[mdd]):>16}"
        )

    print("=" * 58)

    # ==========================================
    # 10. SON 5 GUN ATR ANALIZI
    # ==========================================

    print("\n=== SON 5 GUN ATR ANALIZI ===")

    print(
        analiz[
            [
                "Close",
                "High",
                "Low",
                "ATR14",
                "ATR_Yuzde"
            ]
        ]
        .tail()
        .round(2)
    )

    # ==========================================
    # 11. SON 5 GUN HACIM ANALIZI
    # ==========================================

    print("\n=== SON 5 GUNLUK HACIM ANALIZI ===")

    print(
        analiz[
            [
                "Volume",
                "Hacim_MA20",
                "Hacim_Orani"
            ]
        ]
        .tail()
        .round(2)
    )

    # ==========================================
    # 12. SON 5 ISLEM GUNU TEKNIK ANALIZ
    # ==========================================

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
        ]
        .tail()
        .round(2)
    )

    # ==========================================
    # 13. DESTEK VE DIRENC
    # ==========================================

    print("\n=== SON 5 GUN DESTEK VE DIRENC ===")

    print(
        analiz[
            [
                "Close",
                "Destek20",
                "Direnc20"
            ]
        ]
        .tail()
        .round(2)
    )

    # ==========================================
    # 14. TEKNIK ANALIZ YORUMLARI
    # ==========================================

    teknik_analizi_yorumla(analiz)

    # ==========================================
    # 15. BIRLESIK GRAFIK
    # ==========================================

    birlesik_grafik_olustur(
        analiz,
        hisse_kodu
    )


# ==========================================
# PROGRAM BASLANGICI
# ==========================================

if __name__ == "__main__":
    main()
