
import unittest

import numpy as np
import pandas as pd

from src.risk_analizi import risk_analizi_hesapla


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


if __name__ == "__main__":
    unittest.main()
