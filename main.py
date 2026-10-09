
from src.hisse_arama import hisse_kodu_bul
from src.veri_cekme import hisse_verisi_cek
from src.teknik_analiz import (
    teknik_gostergeleri_hesapla,
    teknik_analizi_yorumla
)
from src.veri_kontrol import veri_kontrol_et, son_eksik_gunu_temizle


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
                "MACD_Histogram"
            ]
        ].tail()
    )

    # 8. Teknik analiz yorumlarini goster
    teknik_analizi_yorumla(analiz)


if __name__ == "__main__":
    main()
