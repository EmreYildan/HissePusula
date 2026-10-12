
import unittest

import numpy as np
import pandas as pd

from src.teknik_analiz import teknik_gostergeleri_hesapla


# ==========================================
# TEST VERISI OLUSTURMA
# ==========================================

def test_verisi_olustur(kapanislar):
    """
    Verilen kapanis fiyatlarindan yapay OHLCV
    verisi olusturur.
    """
    kapanislar = np.asarray(kapanislar, dtype=float)

    tarihler = pd.bdate_range(
        start="2025-01-01",
        periods=len(kapanislar)
    )

    return pd.DataFrame(
        {
            "Open": kapanislar,
            "High": kapanislar + 1,
            "Low": kapanislar - 0.5,
            "Close": kapanislar,
            "Volume": np.full(len(kapanislar), 1000)
        },
        index=tarihler
    )


# ==========================================
# 1. HAREKETLI ORTALAMA TESTLERI
# ==========================================

class TestHareketliOrtalamalar(unittest.TestCase):

    def test_ma20_ma50_ma200(self):

        kapanislar = np.arange(1, 251, dtype=float)

        veriler = test_verisi_olustur(kapanislar)

        analiz = teknik_gostergeleri_hesapla(veriler)

        # Son 20 gunun ortalamasi
        self.assertAlmostEqual(
            analiz["MA20"].iloc[-1],
            240.5
        )

        # Son 50 gunun ortalamasi
        self.assertAlmostEqual(
            analiz["MA50"].iloc[-1],
            225.5
        )

        # Son 200 gunun ortalamasi
        self.assertAlmostEqual(
            analiz["MA200"].iloc[-1],
            150.5
        )

        # Ilk 199 gunde MA200 hesaplanmamali
        self.assertTrue(
            analiz["MA200"].iloc[:199].isna().all()
        )

        # 200. gundeki ilk MA200
        self.assertAlmostEqual(
            analiz["MA200"].iloc[199],
            100.5
        )


# ==========================================
# 2. BOLLINGER BANTLARI TESTI
# ==========================================

class TestBollingerBantlari(unittest.TestCase):

    def test_bollinger_bantlari(self):

        kapanislar = np.arange(1, 251, dtype=float)

        veriler = test_verisi_olustur(kapanislar)

        analiz = teknik_gostergeleri_hesapla(veriler)

        son_20 = kapanislar[-20:]

        # Bagimsiz beklenen degerler
        beklenen_orta = np.mean(son_20)

        beklenen_std = np.std(
            son_20,
            ddof=0
        )

        beklenen_ust = (
            beklenen_orta + 2 * beklenen_std
        )

        beklenen_alt = (
            beklenen_orta - 2 * beklenen_std
        )

        beklenen_genislik = (
            (beklenen_ust - beklenen_alt)
            / beklenen_orta
        ) * 100

        self.assertAlmostEqual(
            analiz["BB_Orta"].iloc[-1],
            beklenen_orta
        )

        self.assertAlmostEqual(
            analiz["BB_Ust"].iloc[-1],
            beklenen_ust
        )

        self.assertAlmostEqual(
            analiz["BB_Alt"].iloc[-1],
            beklenen_alt
        )

        self.assertAlmostEqual(
            analiz["BB_Genislik"].iloc[-1],
            beklenen_genislik
        )


# ==========================================
# 3. RSI14 TESTLERI
# ==========================================

class TestRSI(unittest.TestCase):

    def test_rsi14_sabit_yukselis(self):
        """
        Her gun yukselen fiyatlarda RSI 100 olmali.
        """

        kapanislar = np.arange(
            1, 251,
            dtype=float
        )

        veriler = test_verisi_olustur(kapanislar)

        analiz = teknik_gostergeleri_hesapla(veriler)

        self.assertAlmostEqual(
            analiz["RSI14"].iloc[-1],
            100.0
        )

        # Ilk 14 fiyat degisimi tamamlanmadan
        # RSI hesaplanmamali
        self.assertTrue(
            analiz["RSI14"].iloc[:14].isna().all()
        )

    def test_rsi14_sabit_fiyat(self):
        """
        Fiyat hic degismiyorsa uygulamamizda
        RSI notr deger olan 50 olmali.
        """

        kapanislar = np.full(
            250,
            100.0
        )

        veriler = test_verisi_olustur(kapanislar)

        analiz = teknik_gostergeleri_hesapla(veriler)

        self.assertAlmostEqual(
            analiz["RSI14"].iloc[-1],
            50.0
        )

    def test_rsi14_wilder_karma_fiyatlar(self):
        """
        Yukselis ve dusus iceren fiyatlarda
        Wilder yontemini bagimsiz hesapla.
        """

        kapanislar = np.array(
            [
                100 + i * 0.15 + 3 * np.sin(i * 0.7)
                for i in range(250)
            ],
            dtype=float
        )

        veriler = test_verisi_olustur(kapanislar)

        analiz = teknik_gostergeleri_hesapla(veriler)

        # Bagimsiz RSI hesabi
        degisimler = np.diff(kapanislar)

        kazanc = np.maximum(
            degisimler,
            0
        )

        kayip = np.maximum(
            -degisimler,
            0
        )

        # Ilk 14 degisimin ortalamasi
        ort_kazanc = np.mean(kazanc[:14])
        ort_kayip = np.mean(kayip[:14])

        # Wilder'in tekrarli ortalama formulu
        for i in range(14, len(degisimler)):

            ort_kazanc = (
                ort_kazanc * 13 + kazanc[i]
            ) / 14

            ort_kayip = (
                ort_kayip * 13 + kayip[i]
            ) / 14

        rs = ort_kazanc / ort_kayip

        beklenen_rsi = 100 - (
            100 / (1 + rs)
        )

        program_rsi = analiz["RSI14"].iloc[-1]

        # Iki hesaplama eslesmeli
        self.assertAlmostEqual(
            program_rsi,
            beklenen_rsi,
            places=6
        )

        # RSI 0-100 araliginda olmali
        self.assertTrue(
            analiz["RSI14"]
            .dropna()
            .between(0, 100)
            .all()
        )


# ==========================================
# 4. MACD TESTLERI
# ==========================================

class TestMACD(unittest.TestCase):

    def test_macd_hesaplama(self):
        # Yukselis ve dusus iceren 250 gunluk veri
        kapanislar = np.array(
            [
                100 + i * 0.1 + 5 * np.sin(i * 0.2)
                for i in range(250)
            ],
            dtype=float
        )

        veriler = test_verisi_olustur(kapanislar)
        analiz = teknik_gostergeleri_hesapla(veriler)

        # MACD'yi ayri olarak hesapla
        fiyatlar = pd.Series(kapanislar)

        ema12 = fiyatlar.ewm(
            span=12, adjust=False
        ).mean()

        ema26 = fiyatlar.ewm(
            span=26, adjust=False
        ).mean()

        beklenen_macd = ema12 - ema26

        beklenen_sinyal = beklenen_macd.ewm(
            span=9, adjust=False
        ).mean()

        beklenen_histogram = (
            beklenen_macd - beklenen_sinyal
        )

        np.testing.assert_allclose(
            analiz["MACD"].to_numpy(),
            beklenen_macd.to_numpy(),
            rtol=1e-10,
            atol=1e-10
        )

        np.testing.assert_allclose(
            analiz["MACD_Sinyal"].to_numpy(),
            beklenen_sinyal.to_numpy(),
            rtol=1e-10,
            atol=1e-10
        )

        np.testing.assert_allclose(
            analiz["MACD_Histogram"].to_numpy(),
            beklenen_histogram.to_numpy(),
            rtol=1e-10,
            atol=1e-10
        )

    def test_macd_kesisimleri(self):
        kapanislar = np.array(
            [
                100 + 5 * np.sin(i * 0.2)
                for i in range(250)
            ],
            dtype=float
        )

        veriler = test_verisi_olustur(kapanislar)
        analiz = teknik_gostergeleri_hesapla(veriler)

        fark = (
            analiz["MACD"] -
            analiz["MACD_Sinyal"]
        )

        onceki_fark = fark.shift(1)

        beklenen_yukari = (
            (onceki_fark <= 0) & (fark > 0)
        )

        beklenen_asagi = (
            (onceki_fark >= 0) & (fark < 0)
        )

        pd.testing.assert_series_equal(
            analiz["MACD_Yukari_Kesisim"],
            beklenen_yukari.rename(
                "MACD_Yukari_Kesisim"
            )
        )

        pd.testing.assert_series_equal(
            analiz["MACD_Asagi_Kesisim"],
            beklenen_asagi.rename(
                "MACD_Asagi_Kesisim"
            )
        )

        # Her iki kesisim turu de olusmali
        self.assertTrue(
            analiz["MACD_Yukari_Kesisim"].any()
        )

        self.assertTrue(
            analiz["MACD_Asagi_Kesisim"].any()
        )

        # Ayni gun iki yonlu kesisim olamaz
        self.assertFalse(
            (
                analiz["MACD_Yukari_Kesisim"]
                & analiz["MACD_Asagi_Kesisim"]
            ).any()
        )

# ==========================================
# 5. ATR14 TESTLERI
# ==========================================

class TestATR(unittest.TestCase):

    def test_atr14_sabit_aralik(self):
        # Her gun High-Low farki 4 TL
        kapanislar = np.full(250, 100.0)

        veriler = test_verisi_olustur(kapanislar)

        veriler["High"] = 102.0
        veriler["Low"] = 98.0

        analiz = teknik_gostergeleri_hesapla(veriler)

        # True Range her gun 4 TL
        # Dolayisiyla ATR14 de 4 TL olmali
        self.assertAlmostEqual(
            analiz["ATR14"].iloc[-1],
            4.0
        )

        # ATR yuzdesi = ATR / Close * 100
        self.assertAlmostEqual(
            analiz["ATR_Yuzde"].iloc[-1],
            4.0
        )

    def test_atr14_wilder_hesaplama(self):
        # Degisken fiyatlar ve gunluk araliklar
        kapanislar = np.array(
            [
                100 + i * 0.1 + 3 * np.sin(i * 0.3)
                for i in range(250)
            ],
            dtype=float
        )

        veriler = test_verisi_olustur(kapanislar)

        veriler["High"] = kapanislar + 2
        veriler["Low"] = kapanislar - 1.5

        analiz = teknik_gostergeleri_hesapla(veriler)

        # True Range degerlerini ayri hesapla
        high = veriler["High"].to_numpy()
        low = veriler["Low"].to_numpy()
        close = veriler["Close"].to_numpy()

        tr = np.empty(len(close))

        tr[0] = high[0] - low[0]

        for i in range(1, len(close)):
            tr[i] = max(
                high[i] - low[i],
                abs(high[i] - close[i - 1]),
                abs(low[i] - close[i - 1])
            )

        # Ilk ATR = ilk 14 TR degerinin ortalamasi
        beklenen_atr = np.mean(tr[:14])

        # Sonraki gunlerde Wilder yumusatmasi
        for i in range(14, len(tr)):
            beklenen_atr = (
                beklenen_atr * 13 + tr[i]
            ) / 14

        self.assertAlmostEqual(
            analiz["ATR14"].iloc[-1],
            beklenen_atr,
            places=6
        )

        beklenen_yuzde = (
            beklenen_atr / close[-1]
        ) * 100

        self.assertAlmostEqual(
            analiz["ATR_Yuzde"].iloc[-1],
            beklenen_yuzde,
            places=6
        )



# ==========================================
# 6. HACIM TESTLERI
# ==========================================

class TestHacim(unittest.TestCase):

    def test_hacim_ortalama_ve_oran(self):

        kapanislar = np.full(250, 100.0)
        veriler = test_verisi_olustur(kapanislar)

        # Tum gunlerde hacim 1000
        veriler["Volume"] = 1000.0

        # Son gun hacmi 3000
        veriler.iloc[-1, veriler.columns.get_loc("Volume")] = 3000.0

        analiz = teknik_gostergeleri_hesapla(veriler)

        # Son 20 gun: 19 * 1000 + 3000
        beklenen_ortalama = 1100.0

        beklenen_oran = 3000.0 / 1100.0

        self.assertAlmostEqual(
            analiz["Hacim_MA20"].iloc[-1],
            beklenen_ortalama
        )

        self.assertAlmostEqual(
            analiz["Hacim_Orani"].iloc[-1],
            beklenen_oran
        )

        # Ilk 19 gun ortalama hesaplanmamali
        self.assertTrue(
            analiz["Hacim_MA20"].iloc[:19].isna().all()
        )


# ==========================================
# 7. DESTEK VE DIRENC TESTLERI
# ==========================================

class TestDestekDirenc(unittest.TestCase):

    def test_destek_direnc_onceki_20_gun(self):

        kapanislar = np.full(250, 100.0)
        veriler = test_verisi_olustur(kapanislar)

        veriler["High"] = 105.0
        veriler["Low"] = 95.0

        # Son gunden onceki 20 gunun
        # icinde belirgin seviyeler olustur
        veriler.iloc[-10, veriler.columns.get_loc("High")] = 120.0
        veriler.iloc[-15, veriler.columns.get_loc("Low")] = 80.0

        # Bugunun fiyatlari daha ekstrem olsun.
        # Ancak destek ve dirence DAHIL EDILMEMELI.
        veriler.iloc[-1, veriler.columns.get_loc("High")] = 150.0
        veriler.iloc[-1, veriler.columns.get_loc("Low")] = 50.0

        analiz = teknik_gostergeleri_hesapla(veriler)

        self.assertAlmostEqual(
            analiz["Destek20"].iloc[-1],
            80.0
        )

        self.assertAlmostEqual(
            analiz["Direnc20"].iloc[-1],
            120.0
        )

        # Ilk 20 gunde yeterli gecmis veri yok
        self.assertTrue(
            analiz["Destek20"].iloc[:20].isna().all()
        )

        self.assertTrue(
            analiz["Direnc20"].iloc[:20].isna().all()
        )

if __name__ == "__main__":
    unittest.main()
