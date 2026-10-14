
import pandas as pd
import numpy as np


def veri_kontrol_et(veriler):
    """
    Hisse fiyat verilerinin temel kalite kontrollerini yapar.

    Donus:
        (True, mesaj)  -> Veri uygun
        (False, mesaj) -> Veri uygun degil
    """

    if veriler is None or veriler.empty:
        return False, "Veri seti bos."

    gerekli_sutunlar = [
        "Open", "High", "Low", "Close", "Volume"
    ]

    # Gerekli sutunlar var mi?
    eksik_sutunlar = [
        sutun for sutun in gerekli_sutunlar
        if sutun not in veriler.columns
    ]

    if eksik_sutunlar:
        return False, (
            f"Eksik sutunlar: {eksik_sutunlar}"
        )

    # Teknik analiz icin yeterli gun var mi?
    if len(veriler) < 50:
        return False, (
            f"Yetersiz veri: {len(veriler)} islem gunu. "
            "En az 50 gun gerekli."
        )

    # Eksik deger var mi?
    
    # Eksik degerleri kontrol et
    eksik_veriler = veriler[
        veriler[gerekli_sutunlar].isna().any(axis=1)
    ]

    if not eksik_veriler.empty:

        print("\n=== EKSIK VERI RAPORU ===")

        print(
            eksik_veriler[gerekli_sutunlar].to_string()
        )

        print("\nSutunlara gore eksik deger sayisi:")

        print(
            veriler[gerekli_sutunlar].isna().sum()
        )

        return False, (
            f"{len(eksik_veriler)} islem gununde "
            "eksik fiyat veya hacim verisi bulundu."
        )


    # Tekrarlanan tarihler var mi?
    if veriler.index.has_duplicates:
        return False, "Tekrarlanan tarihler bulundu."

    # Fiyatlar pozitif mi?
    fiyat_sutunlari = ["Open", "High", "Low", "Close"]

    if (veriler[fiyat_sutunlari] <= 0).any().any():
        return False, "Sifir veya negatif fiyat bulundu."

    # Hacim negatif olabilir mi?
    if (veriler["Volume"] < 0).any():
        return False, "Negatif islem hacmi bulundu."

    # Gun ici fiyat tutarliligi
   
    # Gun ici fiyat tutarliligi
    en_yuksek = veriler[
        ["Open", "Close", "Low"]
    ].max(axis=1)

    en_dusuk = veriler[
        ["Open", "Close", "High"]
    ].min(axis=1)

    # Cok kucuk sayisal hassasiyet farklarini tolere et
    tolerans = 1e-8

    high_hatali = (
        (veriler["High"] < en_yuksek)
        & ~np.isclose(
            veriler["High"],
            en_yuksek,
            rtol=0,
            atol=tolerans
        )
    )

    low_hatali = (
        (veriler["Low"] > en_dusuk)
        & ~np.isclose(
            veriler["Low"],
            en_dusuk,
            rtol=0,
            atol=tolerans
        )
    )

    if high_hatali.any():
        print("\n=== HATALI HIGH SATIRLARI ===")
        print(
            veriler.loc[
                high_hatali,
                ["Open", "High", "Low", "Close"]
            ].head(10).to_string()
        )
        return False, "High fiyatinda tutarsizlik var."

    if low_hatali.any():
        print("\n=== HATALI LOW SATIRLARI ===")
        print(
            veriler.loc[
                low_hatali,
                ["Open", "High", "Low", "Close"]
            ].head(10).to_string()
        )
        return False, "Low fiyatinda tutarsizlik var."
   
   
    return True, (
        f"Veri kontrolu basarili. "
        f"{len(veriler)} islem gunu incelendi."
    )

def son_eksik_gunu_temizle(veriler):

    veriler = veriler.copy().sort_index()

    fiyat_sutunlari = ["Open", "High", "Low", "Close"]

    if veriler.iloc[-1][fiyat_sutunlari].isna().any():

        son_tarih = veriler.index[-1]

        print(
            f"\nUYARI: {son_tarih.strftime('%d.%m.%Y')} "
            "tarihindeki fiyatlar eksik."
        )

        print(
            "Son gun analiz disinda birakildi. "
            "Onceki gecerli islem gunu kullanilacak."
        )

        veriler = veriler.iloc[:-1].copy()

    return veriler

def eksik_hafta_ici_gunlerini_bul(veriler):
    """
    Veri setindeki eksik hafta ici tarihlerini bulur.

    Not:
    Resmi BIST tatilleri henuz haric tutulmaz.
    Bu nedenle bulunan her tarih veri hatasi degildir.
    """

    if veriler.empty:
        return pd.DatetimeIndex([])

    tarihler = pd.DatetimeIndex(
        pd.to_datetime(veriler.index)
    ).normalize()

    tarihler = tarihler.sort_values().unique()

    beklenen_tarihler = pd.bdate_range(
        start=tarihler.min(),
        end=tarihler.max()
    )

    eksik_tarihler = beklenen_tarihler.difference(
        tarihler
    )

    return eksik_tarihler



def veri_kalitesi_raporu(veriler):
    """
    Fiyat verisinin temel butunlugunu kontrol eder.

    Eksik islem gunlerini de raporlar.
    Ancak bu fonksiyon eksik fiyat uretmez.
    """

    import pandas as pd

    if veriler is None or veriler.empty:
        return {
            "durum": "HATALI",
            "mesaj": "Veri seti bos.",
            "satir_sayisi": 0,
            "tekrar_tarih": 0,
            "eksik_deger": 0,
            "gecersiz_kapanis": 0,
            "eksik_hafta_ici": []
        }

    tarihler = pd.DatetimeIndex(
        pd.to_datetime(veriler.index)
    )

    tekrar_tarih = int(
        tarihler.duplicated().sum()
    )

    eksik_deger = int(
        veriler.isna().sum().sum()
    )

    gecersiz_kapanis = 0

    if "Close" in veriler.columns:
        gecersiz_kapanis = int(
            (veriler["Close"] <= 0).sum()
        )

    eksik_hafta_ici = eksik_hafta_ici_gunlerini_bul(
        veriler
    )

    from src.bist_takvimi import (
    bist_tatillerini_filtrele,
    takvimi_tanimli_yillar
    )
    

    aciklanamayan_gunler = bist_tatillerini_filtrele(
        eksik_hafta_ici
    )
    tanimli_yillar = set(takvimi_tanimli_yillar())

    dogrulanamayan_gunler = [
        tarih
        for tarih in aciklanamayan_gunler
        if tarih.year not in tanimli_yillar
    ]

    takvimi_tanimli_bosluklar = [
        tarih
        for tarih in aciklanamayan_gunler
        if tarih.year in tanimli_yillar
    ]

    kritik_hata = (
        tekrar_tarih > 0
        or eksik_deger > 0
        or gecersiz_kapanis > 0
        or not tarihler.is_monotonic_increasing
        or "Close" not in veriler.columns
    )

    if kritik_hata:
        durum = "HATALI"
        mesaj = "Veri butunlugu hatasi bulundu."

    elif len(aciklanamayan_gunler) > 0:
        durum = "UYARI"
        mesaj = "Aciklanamayan hafta ici veri bosluklari var."

    else:
        durum = "TEMIZ"
        mesaj = "Temel veri kontrolleri basarili."

    
    return {
        "durum": durum,
        "mesaj": mesaj,
        "satir_sayisi": len(veriler),
        "tekrar_tarih": tekrar_tarih,
        "eksik_deger": eksik_deger,
        "gecersiz_kapanis": gecersiz_kapanis,
        "eksik_gun_detaylari": [],

        "eksik_hafta_ici": [
            tarih.strftime("%Y-%m-%d")
            for tarih in aciklanamayan_gunler
        ],

        "takvimi_eksik_yillar": sorted({
            tarih.year
            for tarih in dogrulanamayan_gunler
        }),

        "eksik_gun_detaylari": [
            kayit
            for kayit in eksik_gunleri_siniflandir(veriler)
            if kayit["kategori"] != "Tam gun tatil"
        ],

        "takvimi_tanimli_bosluklar": [
            tarih.strftime("%Y-%m-%d")
            for tarih in takvimi_tanimli_bosluklar
        ]

        
    }


def eksik_gunleri_siniflandir(veriler):
    """
    Eksik hafta ici tarihlerini BIST takvimine gore
    siniflandirir.

    Tam gun tatiller raporlanir ancak veri hatasi
    olarak degerlendirilmez.
    """
    from src.bist_takvimi import bist_takvimini_oku

    eksik_tarihler = eksik_hafta_ici_gunlerini_bul(veriler)
    takvim = bist_takvimini_oku()

    takvim_durumu = {
        tarih.strftime("%Y-%m-%d"): durum
        for tarih, durum in zip(
            takvim["Tarih"], takvim["Durum"]
        )
    }

    sonuc = []

    for tarih in eksik_tarihler:
        tarih_str = tarih.strftime("%Y-%m-%d")
        durum = takvim_durumu.get(tarih_str)

        if durum == "Kapali":
            kategori = "Tam gun tatil"
        elif durum == "Yarim Gun":
            kategori = "Yarim islem gunu - veri eksik"
        else:
            kategori = "Aciklanamayan eksik gun"

        sonuc.append({
            "tarih": tarih_str,
            "kategori": kategori
        })

    return sonuc




