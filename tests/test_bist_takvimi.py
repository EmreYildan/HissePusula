
import unittest
import pandas as pd

from src.bist_takvimi import (
    bist_tatillerini_getir,
    bist_tatillerini_filtrele,
    takvimi_eksik_yillari_bul
)
from unittest.mock import patch


class TestBistTakvimi(unittest.TestCase):

    def test_2026_tatilleri(self):
        """2026 tatilleri dogru getirilmeli."""

        tatiller = bist_tatillerini_getir(2026)

        self.assertEqual(len(tatiller), 10)

        self.assertIn(
            pd.Timestamp("2026-01-01"),
            tatiller
        )

        self.assertIn(
            pd.Timestamp("2026-10-29"),
            tatiller
        )

    def test_tatil_filtreleme(self):
        """Tatiller cikarilmali, diger tarihler korunmali."""

        eksik_tarihler = pd.to_datetime([
            "2026-01-01",
            "2026-04-23",
            "2026-10-12",
            "2026-10-29"
        ])

        sonuc = bist_tatillerini_filtrele(
            eksik_tarihler
        )

        beklenen = pd.DatetimeIndex([
            "2026-10-12"
        ])

        pd.testing.assert_index_equal(
            sonuc,
            beklenen
        )

    def test_tanimsiz_yil(self):
        with self.assertRaises(ValueError):
            bist_tatillerini_getir(2015)

    def test_tanimsiz_yil_filtreleme(self):
        eksik_tarihler = pd.DatetimeIndex([
            "2023-01-02",
            "2026-10-12"
        ])

        sonuc = bist_tatillerini_filtrele(eksik_tarihler)

        pd.testing.assert_index_equal(
            sonuc,
            eksik_tarihler
        )
        
    def test_takvimi_eksik_yillar(self):
        """Tanimlanmamis takvim yillari bulunmali."""

        veriler = pd.DataFrame(
            {"Close": [100, 110, 120, 130]},
            index=pd.to_datetime([
                "2024-06-10",
                "2025-06-10",
                "2026-06-10",
                "2026-06-11"
            ])
        )

        sonuc = takvimi_eksik_yillari_bul(veriler)

        self.assertEqual(sonuc, [])

    def test_bos_veri_takvim_kontrolu(self):
        """Bos veri setinde eksik yil olmamali."""

        veriler = pd.DataFrame(columns=["Close"])

        sonuc = takvimi_eksik_yillari_bul(veriler)

        self.assertEqual(sonuc, [])
        
    def test_yarim_gunler_filtrelenmemeli(self):
        """Yarim gunler eksik tarih listesinden silinmemeli."""

        eksik_tarihler = pd.to_datetime([
            "2026-03-19",
            "2026-03-20",
            "2026-10-28",
            "2026-10-29"
        ])

        sonuc = bist_tatillerini_filtrele(eksik_tarihler)

        beklenen = pd.DatetimeIndex([
            "2026-03-19",
            "2026-10-28"
        ])

        pd.testing.assert_index_equal(
            sonuc,
            beklenen
        )

        
    def test_2024_yarim_gun_korunmali(self):
        tarihler = pd.DatetimeIndex([
            "2024-04-09",
            "2024-04-10"
        ])

        sonuc = bist_tatillerini_filtrele(tarihler)

        beklenen = pd.DatetimeIndex([
            "2024-04-09"
        ])

        pd.testing.assert_index_equal(sonuc, beklenen)


    def test_2026_aciklanamayan_gun_korunmali(self):
        tarihler = pd.DatetimeIndex([
            "2026-10-12"
        ])

        sonuc = bist_tatillerini_filtrele(tarihler)

        pd.testing.assert_index_equal(sonuc, tarihler)



if __name__ == "__main__":
    unittest.main()
