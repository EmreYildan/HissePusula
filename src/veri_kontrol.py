
import pandas as pd


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
    en_yuksek = veriler[
        ["Open", "Close", "Low"]
    ].max(axis=1)

    en_dusuk = veriler[
        ["Open", "Close", "High"]
    ].min(axis=1)

    if (veriler["High"] < en_yuksek).any():
        return False, "High fiyatinda tutarsizlik var."

    if (veriler["Low"] > en_dusuk).any():
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
