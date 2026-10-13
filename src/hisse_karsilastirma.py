
import pandas as pd

from src.veri_cekme import hisse_verisi_cek
from src.veri_kontrol import (
    veri_kontrol_et,
    son_eksik_gunu_temizle
)
from src.getiri_analizi import gecmis_getirileri_hesapla
from src.risk_analizi import (
    donemsel_maksimum_dusus_hesapla,
    donemsel_volatilite_hesapla
)


def hisseleri_karsilastir(hisse_kodlari):
    """
    Birden fazla BIST hissesinin
    6, 12 ve 24 aylik getiri/risk
    degerlerini karsilastirir.
    """

    sonuclar = []

    for hisse_kodu in hisse_kodlari:

        hisse_kodu = hisse_kodu.strip().upper()

        if not hisse_kodu:
            continue

        print(f"\n{hisse_kodu} analiz ediliyor...")

        veriler = hisse_verisi_cek(hisse_kodu)

        if veriler is None or veriler.empty:
            print(f"{hisse_kodu}: Veri alinamadi.")
            continue

        veriler = son_eksik_gunu_temizle(veriler)

        uygun_mu, mesaj = veri_kontrol_et(veriler)

        if not uygun_mu:
            print(f"{hisse_kodu}: {mesaj}")
            continue

        analiz = gecmis_getirileri_hesapla(veriler)
        analiz = donemsel_maksimum_dusus_hesapla(analiz)
        analiz = donemsel_volatilite_hesapla(analiz)

        son = analiz.iloc[-1]

        satir = {
            "Hisse": hisse_kodu,
            "Veri_Gunu": len(analiz)
        }

        for donem in ["6A", "12A", "24A"]:

            satir[f"Getiri_{donem}"] = son[
                f"Getiri_{donem}"
            ]

            satir[f"Volatilite_{donem}"] = son[
                f"Volatilite_{donem}"
            ]

            satir[f"MDD_{donem}"] = son[
                f"MDD_{donem}"
            ]

        sonuclar.append(satir)

    return pd.DataFrame(sonuclar)
