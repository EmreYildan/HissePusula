
from pathlib import Path

import pandas as pd


# ==========================================
# DOSYA YOLU
# ==========================================

PROJE_KOKU = Path(__file__).resolve().parent.parent

TAKVIM_DOSYASI = (
    PROJE_KOKU / "data" / "processed" / "bist_tatilleri.csv"
)


# ==========================================
# BIST TATIL TAKVIMINI OKU
# ==========================================

def bist_takvimini_oku():
    """
    BIST tam gun tatillerini CSV dosyasindan okur.
    """

    if not TAKVIM_DOSYASI.exists():
        raise FileNotFoundError(
            f"BIST tatil dosyasi bulunamadi: {TAKVIM_DOSYASI}"
        )

    takvim = pd.read_csv(TAKVIM_DOSYASI)

    gerekli_sutunlar = {"Tarih", "Aciklama"}

    if not gerekli_sutunlar.issubset(takvim.columns):
        raise ValueError(
            "BIST tatil dosyasinda Tarih ve Aciklama "
            "sutunlari bulunmali."
        )

    takvim["Tarih"] = pd.to_datetime(
        takvim["Tarih"],
        format="%Y-%m-%d",
        errors="raise"
    )

    if takvim["Tarih"].duplicated().any():
        raise ValueError(
            "BIST tatil dosyasinda tekrar eden tarihler var."
        )

    return takvim.sort_values("Tarih").reset_index(drop=True)


# ==========================================
# TAKVIMI TANIMLI YILLAR
# ==========================================

def takvimi_tanimli_yillar():
    """
    CSV'deki tarihlerin ait oldugu yillari dondurur.

    Not: Bir yilin CSV'de bulunmasi, o yilin
    tum tatillerinin eksiksiz oldugunu tek
    basina kanitlamaz.
    """

    takvim = bist_takvimini_oku()

    return sorted(
        takvim["Tarih"].dt.year.unique().tolist()
    )


# ==========================================
# BELIRLI YILIN TATILLERI
# ==========================================


def bist_tatillerini_getir(yil):
    """
    Belirtilen yilin yalnizca tam gun
    BIST kapanis tarihlerini dondurur.
    """

    takvim = bist_takvimini_oku()

    secilen = takvim[
        (takvim["Tarih"].dt.year == yil)
        & (takvim["Durum"] == "Kapali")
    ]

    if secilen.empty:
        raise ValueError(
            f"{yil} yili icin tam gun tatil kaydi bulunamadi."
        )

    return pd.DatetimeIndex(secilen["Tarih"])



# ==========================================
# TATILLERI FILTRELE
# ==========================================


def bist_tatillerini_filtrele(eksik_tarihler):
    """
    Yalnizca BIST'in tamamen kapali
    oldugu tarihleri filtreler.

    Yarim gunler korunur.
    """

    eksik_tarihler = pd.DatetimeIndex(
        pd.to_datetime(eksik_tarihler)
    )

    takvim = bist_takvimini_oku()

    # Yalnizca tam gun kapanislar
    kapali_gunler = takvim[
        takvim["Durum"] == "Kapali"
    ]

    tatiller = pd.DatetimeIndex(
        kapali_gunler["Tarih"]
    )

    return eksik_tarihler.difference(tatiller)



# ==========================================
# TAKVIMI EKSIK YILLARI BUL
# ==========================================

def takvimi_eksik_yillari_bul(veriler):
    """
    Veri setindeki, tatil takvimi henuz
    tanimlanmamis yillari bulur.
    """

    if veriler.empty:
        return []

    veri_yillari = pd.DatetimeIndex(
        pd.to_datetime(veriler.index)
    ).year.unique()

    tanimli_yillar = takvimi_tanimli_yillar()

    return sorted([
        int(yil)
        for yil in veri_yillari
        if yil not in tanimli_yillar
    ])
