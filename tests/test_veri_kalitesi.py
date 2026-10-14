import unittest
from unittest.mock import patch

import pandas as pd

from src.veri_kontrol import eksik_gunleri_siniflandir


class TestEksikGunSiniflandirma(unittest.TestCase):

    def test_yarim_gun_eksik_veri(self):
        veriler = pd.DataFrame(
            {"Close": [100, 102]},
            index=pd.to_datetime([
                "2024-04-08",
                "2024-04-11",
            ])
        )

        takvim = pd.DataFrame({
            "Tarih": pd.to_datetime([
                "2024-04-09",
                "2024-04-10",
            ]),
            "Durum": ["Yarim Gun", "Kapali"],
        })

        with patch(
            "src.bist_takvimi.bist_takvimini_oku",
            return_value=takvim
        ):
            sonuc = eksik_gunleri_siniflandir(veriler)

        self.assertEqual(sonuc, [
            {
                "tarih": "2024-04-09",
                "kategori": "Yarim islem gunu - veri eksik",
            },
            {
                "tarih": "2024-04-10",
                "kategori": "Tam gun tatil",
            },
        ])

    def test_aciklanamayan_eksik_gun(self):
        veriler = pd.DataFrame(
            {"Close": [100, 102]},
            index=pd.to_datetime([
                "2026-10-09",
                "2026-10-13",
            ])
        )

        takvim = pd.DataFrame({
            "Tarih": pd.to_datetime([]),
            "Durum": pd.Series(dtype="object"),
        })

        with patch(
            "src.bist_takvimi.bist_takvimini_oku",
            return_value=takvim
        ):
            sonuc = eksik_gunleri_siniflandir(veriler)

        self.assertEqual(sonuc, [
            {
                "tarih": "2026-10-12",
                "kategori": "Aciklanamayan eksik gun",
            },
        ])

    
from src.veri_kontrol import veri_kalitesi_raporu


class TestVeriKalitesiRaporu(unittest.TestCase):

    def test_yarim_gun_detayi_raporda_gorunmeli(self):
        veriler = pd.DataFrame(
            {"Close": [100.0, 102.0]},
            index=pd.to_datetime([
                "2024-04-08",
                "2024-04-11",
            ])
        )

        takvim = pd.DataFrame({
            "Tarih": pd.to_datetime([
                "2024-04-09",
                "2024-04-10",
            ]),
            "Durum": ["Yarim Gun", "Kapali"],
        })

        with patch(
            "src.bist_takvimi.bist_takvimini_oku",
            return_value=takvim
        ), patch(
            "src.bist_takvimi.takvimi_tanimli_yillar",
            return_value=[2024]
        ):
            rapor = veri_kalitesi_raporu(veriler)

        self.assertEqual(rapor["durum"], "UYARI")
        self.assertEqual(rapor["eksik_hafta_ici"], ["2024-04-09"])
        self.assertEqual(
            rapor["eksik_gun_detaylari"],
            [{
                "tarih": "2024-04-09",
                "kategori": "Yarim islem gunu - veri eksik",
            }]
        )
if __name__ == "__main__":
    unittest.main()