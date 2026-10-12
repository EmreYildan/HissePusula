
import unittest

import numpy as np
import pandas as pd

from src.getiri_analizi import gecmis_getirileri_hesapla


class TestGetiriAnalizi(unittest.TestCase):

    def test_6_12_24_aylik_getiriler(self):
        # 600 islem gunluk yapay fiyat serisi
        kapanislar = np.full(600, 100.0)

        # Son gunku kapanis fiyati 200 TL
        kapanislar[-1] = 200.0

        # Gecmis referans fiyatlari
        kapanislar[-127] = 125.0
        kapanislar[-253] = 80.0
        kapanislar[-505] = 50.0

        tarihler = pd.bdate_range(
            start="2023-01-02",
            periods=600
        )

        veriler = pd.DataFrame(
            {"Close": kapanislar},
            index=tarihler
        )

        analiz = gecmis_getirileri_hesapla(veriler)

        # 6 ay: (200 / 125 - 1) * 100 = %60
        self.assertAlmostEqual(
            analiz["Getiri_6A"].iloc[-1],
            60.0
        )

        # 12 ay: (200 / 80 - 1) * 100 = %150
        self.assertAlmostEqual(
            analiz["Getiri_12A"].iloc[-1],
            150.0
        )

        # 24 ay: (200 / 50 - 1) * 100 = %300
        self.assertAlmostEqual(
            analiz["Getiri_24A"].iloc[-1],
            300.0
        )

    def test_yetersiz_gecmis_veri(self):
        # 200 islem gunu: 12 ve 24 ay icin yetersiz
        kapanislar = np.full(200, 100.0)

        tarihler = pd.bdate_range(
            start="2025-01-01",
            periods=200
        )

        veriler = pd.DataFrame(
            {"Close": kapanislar},
            index=tarihler
        )

        analiz = gecmis_getirileri_hesapla(veriler)

        # 6 ay hesaplanabilir
        self.assertAlmostEqual(
            analiz["Getiri_6A"].iloc[-1],
            0.0
        )

        # 12 ve 24 ay hesaplanamaz
        self.assertTrue(
            pd.isna(analiz["Getiri_12A"].iloc[-1])
        )

        self.assertTrue(
            pd.isna(analiz["Getiri_24A"].iloc[-1])
        )

    def test_girdi_verisi_degismemeli(self):
        # Fonksiyon orijinal DataFrame'i degistirmemeli
        veriler = pd.DataFrame(
            {
                "Close": np.linspace(100, 200, 600)
            },
            index=pd.bdate_range(
                start="2023-01-02",
                periods=600
            )
        )

        orijinal = veriler.copy(deep=True)

        gecmis_getirileri_hesapla(veriler)

        pd.testing.assert_frame_equal(
            veriler,
            orijinal
        )


if __name__ == "__main__":
    unittest.main()
