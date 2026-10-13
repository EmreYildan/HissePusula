
import unittest

import pandas as pd

from src.hisse_karsilastirma import (
    ortak_tarihleri_bul,
    hisseleri_sirala,
    karsilastirmayi_kaydet,
    veri_yeterliligini_kontrol_et
)

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch


class TestHisseKarsilastirma(unittest.TestCase):

    def test_ortak_tarihler(self):

        veri_a = pd.DataFrame(
            {"Close": [10, 11, 12]},
            index=pd.to_datetime([
                "2026-10-08",
                "2026-10-09",
                "2026-10-13"
            ])
        )

        veri_b = pd.DataFrame(
            {"Close": [20, 21, 22]},
            index=pd.to_datetime([
                "2026-10-09",
                "2026-10-12",
                "2026-10-13"
            ])
        )

        sonuc = ortak_tarihleri_bul({
            "AAA": veri_a,
            "BBB": veri_b
        })

        beklenen = pd.DatetimeIndex([
            "2026-10-09",
            "2026-10-13"
        ])

        pd.testing.assert_index_equal(
            sonuc,
            beklenen
        )

    def test_bos_sozluk(self):

        sonuc = ortak_tarihleri_bul({})

        self.assertTrue(sonuc.empty)

        
    def test_getiriye_gore_siralama(self):
        veriler = pd.DataFrame({
            "Hisse": ["AAA", "BBB", "CCC"],
            "Getiri_12A": [15.0, 40.0, -5.0]
        })

        sonuc = hisseleri_sirala(
            veriler,
            donem="12A",
            kriter="Getiri"
        )

        self.assertEqual(
            sonuc["Hisse"].tolist(),
            ["BBB", "AAA", "CCC"]
        )

    def test_volatiliteye_gore_siralama(self):
        veriler = pd.DataFrame({
            "Hisse": ["AAA", "BBB", "CCC"],
            "Volatilite_12A": [35.0, 20.0, 50.0]
        })

        sonuc = hisseleri_sirala(
            veriler,
            donem="12A",
            kriter="Volatilite"
        )

        self.assertEqual(
            sonuc["Hisse"].tolist(),
            ["BBB", "AAA", "CCC"]
        )

        
    def test_karsilastirma_csv_kaydetme(self):
        veriler = pd.DataFrame({
            "Hisse": ["THYAO", "ASELS"],
            "Getiri_12A": [10.5, 25.3]
        })

        with TemporaryDirectory() as klasor:
            with patch(
                "src.hisse_karsilastirma.__file__",
                str(Path(klasor) / "src" / "hisse_karsilastirma.py")
            ):
                dosya = karsilastirmayi_kaydet(veriler)

            self.assertTrue(dosya.exists())

            okunan = pd.read_csv(dosya)

            pd.testing.assert_frame_equal(
                okunan,
                veriler
            )

    def test_bos_karsilastirma_kaydedilmemeli(self):
        with self.assertRaises(ValueError):
            karsilastirmayi_kaydet(pd.DataFrame())


    
    def test_veri_yeterliligi(self):
        veriler = pd.DataFrame({
            "Hisse": ["AAA", "BBB", "CCC"],
            "Veri_Gunu": [100, 300, 600],
            "Getiri_6A": [float("nan"), 10.0, 15.0],
            "Getiri_12A": [float("nan"), 20.0, 25.0],
            "Getiri_24A": [float("nan"), float("nan"), 30.0]
        })

        sonuc = veri_yeterliligini_kontrol_et(veriler)

        self.assertEqual(
            sonuc["Yeterli_6A"].tolist(),
            [False, True, True]
        )

        self.assertEqual(
            sonuc["Yeterli_12A"].tolist(),
            [False, True, True]
        )

        self.assertEqual(
            sonuc["Yeterli_24A"].tolist(),
            [False, False, True]
        )




if __name__ == "__main__":
    unittest.main()
