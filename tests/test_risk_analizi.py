
import unittest

import numpy as np
import pandas as pd

from src.risk_analizi import (
    risk_analizi_hesapla,
    donemsel_maksimum_dusus_hesapla,
    donemsel_volatilite_hesapla
)


class TestRiskAnalizi(unittest.TestCase):

    def test_sabit_fiyat_volatilite(self):
        # 300 gun boyunca fiyat 100 TL
        kapanislar = np.full(300, 100.0)

        veriler = pd.DataFrame({
            "Close": kapanislar
        })

        analiz = risk_analizi_hesapla(veriler)

        # Sabit fiyatlarda volatilite sifir olmali
        self.assertAlmostEqual(
            analiz["Volatilite_252"].iloc[-1],
            0.0
        )

        # Fiyat hic dusmedigi icin MDD sifir
        self.assertAlmostEqual(
            analiz["Max_Drawdown"].iloc[-1],
            0.0
        )

    def test_max_drawdown_hesaplama(self):
        # 100 -> 150 -> 90 -> 120 -> 135
        # Zirveden en buyuk dusus: 150 -> 90
        kapanislar = [100, 150, 90, 120, 135]

        veriler = pd.DataFrame({
            "Close": kapanislar
        })

        analiz = risk_analizi_hesapla(veriler)

        self.assertAlmostEqual(
            analiz["Max_Drawdown"].iloc[-1],
            -40.0
        )

        # Son gundeki drawdown:
        # 135 / 150 - 1 = -%10
        self.assertAlmostEqual(
            analiz["Drawdown"].iloc[-1],
            -10.0
        )

        # Maksimum dusus ile guncel dusus farkli
        self.assertLess(
            analiz["Max_Drawdown"].iloc[-1],
            analiz["Drawdown"].iloc[-1]
        )

    def test_yetersiz_veri_volatilite(self):
        # 200 fiyat gozlemi, 199 gunluk getiri
        kapanislar = np.linspace(100, 150, 200)

        veriler = pd.DataFrame({
            "Close": kapanislar
        })

        analiz = risk_analizi_hesapla(veriler)

        # 252 getiri gozlemi yok
        self.assertTrue(
            pd.isna(
                analiz["Volatilite_252"].iloc[-1]
            )
        )

        # Drawdown yine hesaplanabilmeli
        self.assertFalse(
            pd.isna(
                analiz["Max_Drawdown"].iloc[-1]
            )
        )

    def test_orijinal_veri_korunmali(self):
        kapanislar = np.linspace(100, 200, 300)

        veriler = pd.DataFrame({
            "Close": kapanislar
        })

        orijinal = veriler.copy(deep=True)

        risk_analizi_hesapla(veriler)

        # Fonksiyon girdi verisini degistirmemeli
        pd.testing.assert_frame_equal(
            veriler,
            orijinal
        )

# ==========================================
# DONEMSEL MAKSIMUM DUSUS TESTLERI
# ==========================================

class TestDonemselMaksimumDusus(unittest.TestCase):

    def test_donemsel_mdd(self):
        # 600 gunluk sabit fiyat serisi
        kapanislar = np.full(600, 100.0)

        # Son 126 gun icinde:
        # 150 TL zirve, ardindan 90 TL dip
        kapanislar[-100] = 150.0
        kapanislar[-50] = 90.0

        # Daha eski donemde daha buyuk dusus
        kapanislar[200] = 200.0
        kapanislar[250] = 80.0

        veriler = pd.DataFrame({
            "Close": kapanislar
        })

        analiz = donemsel_maksimum_dusus_hesapla(veriler)

        # Son 6 ayda 150 -> 90 = -%40
        self.assertAlmostEqual(
            analiz["MDD_6A"].iloc[-1],
            -40.0
        )

        # Son 12 ayda da en buyuk dusus -%40
        self.assertAlmostEqual(
            analiz["MDD_12A"].iloc[-1],
            -40.0
        )

        # Son 24 ayda 200 -> 80 = -%60
        self.assertAlmostEqual(
            analiz["MDD_24A"].iloc[-1],
            -60.0
        )

    def test_yetersiz_veri(self):
        kapanislar = np.full(200, 100.0)

        veriler = pd.DataFrame({
            "Close": kapanislar
        })

        analiz = donemsel_maksimum_dusus_hesapla(veriler)

        # 127 fiyat gozlemi yeterli
        self.assertAlmostEqual(
            analiz["MDD_6A"].iloc[-1],
            0.0
        )

        # 253 ve 505 gozlem yok
        self.assertTrue(
            pd.isna(analiz["MDD_12A"].iloc[-1])
        )

        self.assertTrue(
            pd.isna(analiz["MDD_24A"].iloc[-1])
        )


# ==========================================
# DONEMSEL VOLATILITE TESTLERI
# ==========================================

class TestDonemselVolatilite(unittest.TestCase):

    def test_sabit_fiyat_volatilite(self):
        kapanislar = np.full(600, 100.0)

        veriler = pd.DataFrame({
            "Close": kapanislar
        })

        analiz = donemsel_volatilite_hesapla(veriler)

        for sutun in [
            "Volatilite_6A",
            "Volatilite_12A",
            "Volatilite_24A"
        ]:
            self.assertAlmostEqual(
                analiz[sutun].iloc[-1],
                0.0
            )

    def test_bilinen_getirilerle_volatilite(self):
        # 600 fiyat icin degisken gunluk getiriler
        gunluk_oranlar = np.array(
            [0.01, -0.02, 0.03, -0.01] * 150
        )

        kapanislar = np.empty(601)
        kapanislar[0] = 100.0

        for i, oran in enumerate(gunluk_oranlar):
            kapanislar[i + 1] = (
                kapanislar[i] * (1 + oran)
            )

        veriler = pd.DataFrame({
            "Close": kapanislar
        })

        analiz = donemsel_volatilite_hesapla(veriler)

        for sutun, gun_sayisi in [
            ("Volatilite_6A", 126),
            ("Volatilite_12A", 252),
            ("Volatilite_24A", 504)
        ]:
            beklenen = (
                np.std(
                    gunluk_oranlar[-gun_sayisi:] * 100,
                    ddof=1
                )
                * np.sqrt(252)
            )

            self.assertAlmostEqual(
                analiz[sutun].iloc[-1],
                beklenen,
                places=6
            )

    def test_yetersiz_veri(self):
        kapanislar = np.full(200, 100.0)

        veriler = pd.DataFrame({
            "Close": kapanislar
        })

        analiz = donemsel_volatilite_hesapla(veriler)

        self.assertAlmostEqual(
            analiz["Volatilite_6A"].iloc[-1],
            0.0
        )

        self.assertTrue(
            pd.isna(analiz["Volatilite_12A"].iloc[-1])
        )

        self.assertTrue(
            pd.isna(analiz["Volatilite_24A"].iloc[-1])
        )

    def test_orijinal_veri_korunmali(self):
        veriler = pd.DataFrame({
            "Close": np.linspace(100, 200, 600)
        })

        orijinal = veriler.copy(deep=True)

        donemsel_volatilite_hesapla(veriler)

        pd.testing.assert_frame_equal(
            veriler,
            orijinal
        )

if __name__ == "__main__":
    unittest.main()
