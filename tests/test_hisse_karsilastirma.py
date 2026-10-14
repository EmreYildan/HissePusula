
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

    def test_veri_kalitesi_sutunlari(self):
        import pandas as pd

        from src.hisse_karsilastirma import hisseleri_karsilastir

        with patch(
            "src.hisse_karsilastirma.hisse_verisi_cek"
        ) as mock_veri:

            tarihler = pd.bdate_range(
                "2024-01-01",
                periods=550
            )

            veri = pd.DataFrame({
                "Open": [100.0] * 550,
                "High": [101.0] * 550,
                "Low": [99.0] * 550,
                "Close": [100.0] * 550,
                "Volume": [1000] * 550
            }, index=tarihler)

            mock_veri.return_value = veri

            sonuc = hisseleri_karsilastir(["THYAO", "ASELS"])

            self.assertIn("Veri_Kalitesi", sonuc.columns)
            self.assertIn("Eksik_Gun_Sayisi", sonuc.columns)

            self.assertEqual(len(sonuc), 2)    

    def test_veri_kalitesi_dogru_hisseye_aktarilmali(self):
        import pandas as pd
        from unittest.mock import patch
        from src.hisse_karsilastirma import hisseleri_karsilastir

        tarihler = pd.bdate_range("2024-01-01", periods=550)

        veri = pd.DataFrame({
            "Open": [100.0] * 550,
            "High": [101.0] * 550,
            "Low": [99.0] * 550,
            "Close": [100.0] * 550,
            "Volume": [1000] * 550
        }, index=tarihler)

        raporlar = [
            {
                "durum": "TEMIZ",
                "eksik_hafta_ici": []
            },
            {
                "durum": "UYARI",
                "eksik_hafta_ici": [
                    "2024-04-09",
                    "2026-10-12"
                ]
            }
        ]

        with patch(
            "src.hisse_karsilastirma.hisse_verisi_cek",
            return_value=veri
        ), patch(
            "src.hisse_karsilastirma.veri_kalitesi_raporu",
            side_effect=raporlar
        ):
            sonuc = hisseleri_karsilastir(["THYAO", "ASELS"])

        sonuc = sonuc.set_index("Hisse")

        self.assertEqual(
            sonuc.loc["THYAO", "Veri_Kalitesi"],
            "TEMIZ"
        )
        self.assertEqual(
            sonuc.loc["THYAO", "Eksik_Gun_Sayisi"],
            0
        )
        self.assertEqual(
            sonuc.loc["ASELS", "Veri_Kalitesi"],
            "UYARI"
        )
        self.assertEqual(
            sonuc.loc["ASELS", "Eksik_Gun_Sayisi"],
            2
        )            


    
    def test_eksik_gun_diger_hissenin_gecmisini_silmemeli(self):
        import pandas as pd
        from unittest.mock import patch
        from src.hisse_karsilastirma import hisseleri_karsilastir

        tarihler = pd.bdate_range("2024-01-01", periods=550)

        def veri_olustur(index):
            return pd.DataFrame({
                "Open": [100.0] * len(index),
                "High": [101.0] * len(index),
                "Low": [99.0] * len(index),
                "Close": [100.0] * len(index),
                "Volume": [1000] * len(index)
            }, index=index)

        thy_verisi = veri_olustur(tarihler)

        # ASELS'in gecmisinden bir gun eksiltiyoruz.
        asels_verisi = veri_olustur(tarihler.delete(100))

        def sahte_veri_cek(hisse):
            if hisse == "THYAO":
                return thy_verisi.copy()
            return asels_verisi.copy()

        with patch(
            "src.hisse_karsilastirma.hisse_verisi_cek",
            side_effect=sahte_veri_cek
        ):
            sonuc = hisseleri_karsilastir(["THYAO", "ASELS"])

        sonuc = sonuc.set_index("Hisse")

        self.assertEqual(sonuc.loc["THYAO", "Veri_Gunu"], 550)
        self.assertEqual(sonuc.loc["ASELS", "Veri_Gunu"], 549)

        self.assertEqual(
            sonuc.loc["THYAO", "Analiz_Tarihi"],
            sonuc.loc["ASELS", "Analiz_Tarihi"]
        )

        
    def test_ortak_tarihten_sonraki_veri_kullanilmamali(self):
        import pandas as pd
        from unittest.mock import patch
        from src.hisse_karsilastirma import hisseleri_karsilastir

        tarihler = pd.bdate_range("2024-01-01", periods=550)

        def veri_olustur(index):
            return pd.DataFrame({
                "Open": [100.0] * len(index),
                "High": [101.0] * len(index),
                "Low": [99.0] * len(index),
                "Close": [100.0] * len(index),
                "Volume": [1000] * len(index)
            }, index=index)

        thy_verisi = veri_olustur(tarihler)
        asels_verisi = veri_olustur(tarihler[:-5])

        def sahte_veri_cek(hisse):
            if hisse == "THYAO":
                return thy_verisi.copy()
            return asels_verisi.copy()

        with patch(
            "src.hisse_karsilastirma.hisse_verisi_cek",
            side_effect=sahte_veri_cek
        ):
            sonuc = hisseleri_karsilastir(["THYAO", "ASELS"])

        sonuc = sonuc.set_index("Hisse")

        self.assertEqual(sonuc.loc["THYAO", "Veri_Gunu"], 545)
        self.assertEqual(sonuc.loc["ASELS", "Veri_Gunu"], 545)

        self.assertEqual(
            sonuc.loc["THYAO", "Analiz_Tarihi"],
            tarihler[-6].date()
        )





if __name__ == "__main__":
    unittest.main()
