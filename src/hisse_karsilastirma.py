
import pandas as pd
from pathlib import Path

from src.veri_cekme import hisse_verisi_cek
from src.veri_kontrol import (
    veri_kontrol_et,
    son_eksik_gunu_temizle
)
from src.getiri_analizi import gecmis_getirileri_hesapla
from src.risk_analizi import (
    donemsel_maksimum_dusus_hesapla,
    donemsel_volatilite_hesapla
)

from src.veri_kontrol import veri_kalitesi_raporu


DONEMLER = ["6A", "12A", "24A"]


def ortak_tarihleri_bul(veri_sozlugu):
    """
    Tum hisselerde bulunan ortak islem
    tarihlerini bulur.
    """

    if not veri_sozlugu:
        return pd.DatetimeIndex([])

    ortak = None

    for veriler in veri_sozlugu.values():
        tarihler = pd.DatetimeIndex(veriler.index)

        if ortak is None:
            ortak = tarihler
        else:
            ortak = ortak.intersection(tarihler)

    return ortak.sort_values()



def hisseleri_karsilastir(hisse_kodlari):
    """
    Hisseleri ortak son analiz tarihinde karsilastirir.

    Her hissenin getiri ve risk hesaplamasi kendi
    tarihsel verileri uzerinde yapilir.
    """

    veri_sozlugu = {}

    # 1. HISSE VERILERINI TOPLA
    for hisse_kodu in hisse_kodlari:

        hisse_kodu = hisse_kodu.strip().upper()

        if not hisse_kodu:
            continue

        print(f"\n{hisse_kodu} analiz ediliyor...")

        veriler = hisse_verisi_cek(hisse_kodu)

        if veriler is None or veriler.empty:
            print(f"{hisse_kodu}: Veri alinamadi.")
            continue

        veriler = son_eksik_gunu_temizle(veriler)

        uygun_mu, mesaj = veri_kontrol_et(veriler)

        if not uygun_mu:
            print(f"{hisse_kodu}: {mesaj}")
            continue

        veri_sozlugu[hisse_kodu] = veriler

    if not veri_sozlugu:
        return pd.DataFrame()

    # 2. KAYNAK VERI KALITESINI KONTROL ET
    kalite_raporlari = {
        hisse: veri_kalitesi_raporu(veri)
        for hisse, veri in veri_sozlugu.items()
    }

    # 3. ORTAK SON ANALIZ TARIHINI BUL
    ortak_tarihler = ortak_tarihleri_bul(veri_sozlugu)

    if ortak_tarihler.empty:
        print("Hisseler arasinda ortak islem tarihi bulunamadi.")
        return pd.DataFrame()

    analiz_tarihi = ortak_tarihler.max()

    print(
        f"\nOrtak analiz tarihi: "
        f"{analiz_tarihi.date()}"
    )

    # 4. GETIRI VE RISK ANALIZLERI
    sonuclar = []

    for hisse_kodu, veriler in veri_sozlugu.items():

        # Yalnizca analiz tarihinden sonrasini cikar.
        # Gecmisteki hisselere ozel tarihler korunur.
        analiz_verileri = veriler.loc[
            veriler.index <= analiz_tarihi
        ].copy()

        if analiz_verileri.empty:
            continue

        analiz = gecmis_getirileri_hesapla(analiz_verileri)
        analiz = donemsel_maksimum_dusus_hesapla(analiz)
        analiz = donemsel_volatilite_hesapla(analiz)

        # Analiz tarihi tum hisselerde ortak oldugu
        # icin son satir ayni tarihe aittir.
        son = analiz.loc[analiz_tarihi]

        satir = {
            "Hisse": hisse_kodu,
            "Analiz_Tarihi": analiz_tarihi.date(),
            "Veri_Gunu": len(analiz)
        }

        for donem in DONEMLER:
            satir[f"Getiri_{donem}"] = son[
                f"Getiri_{donem}"
            ]

            satir[f"Volatilite_{donem}"] = son[
                f"Volatilite_{donem}"
            ]

            satir[f"MDD_{donem}"] = son[
                f"MDD_{donem}"
            ]

        sonuclar.append(satir)

    if not sonuclar:
        return pd.DataFrame()

    # 5. SONUCLARI TABLOYA DONUSTUR
    sonuclar = pd.DataFrame(sonuclar)

    # 6. VERI KALITESI BILGILERINI EKLE
    sonuclar["Veri_Kalitesi"] = sonuclar["Hisse"].map(
        lambda hisse: kalite_raporlari[hisse]["durum"]
    )

    sonuclar["Eksik_Gun_Sayisi"] = sonuclar["Hisse"].map(
        lambda hisse: len(
            kalite_raporlari[hisse]["eksik_hafta_ici"]
        )
    )

    # 7. VERI YETERLILIGINI KONTROL ET
    sonuclar = veri_yeterliligini_kontrol_et(sonuclar)

    return sonuclar



def hisseleri_sirala(sonuclar, donem="12A", kriter="Getiri"):
    """
    Hisseleri secilen donem ve kritere gore siralar.

    Getiri: yuksekten dusuge
    Volatilite: dusukten yuksege
    MDD: sifira en yakin dususten en buyuk dususe
    """

    if donem not in DONEMLER:
        raise ValueError(
            "Donem 6A, 12A veya 24A olmali."
        )

    if kriter not in ["Getiri", "Volatilite", "MDD"]:
        raise ValueError(
            "Kriter Getiri, Volatilite veya MDD olmali."
        )

    sutun = f"{kriter}_{donem}"

    if sutun not in sonuclar.columns:
        raise ValueError(
            f"Sonuc tablosunda {sutun} sutunu bulunamadi."
        )

    # Getiri ve MDD: buyukten kucuge
    # Volatilite: kucukten buyuge
    artan = kriter == "Volatilite"

    return sonuclar.sort_values(
        by=sutun,
        ascending=artan,
        na_position="last"
    ).reset_index(drop=True)


def karsilastirmayi_kaydet(sonuclar, dosya_adi="hisse_karsilastirma.csv"):
    """
    Hisse karsilastirma sonuclarini CSV dosyasina kaydeder.
    """

    if sonuclar.empty:
        raise ValueError("Kaydedilecek karsilastirma sonucu yok.")

    # Dosya adinin klasor disina cikmasini engelle
    if Path(dosya_adi).name != dosya_adi:
        raise ValueError("Yalnizca dosya adi girilmeli.")

    if not dosya_adi.lower().endswith(".csv"):
        raise ValueError("Dosya uzantisi .csv olmali.")

    proje_koku = Path(__file__).resolve().parent.parent
    kayit_klasoru = proje_koku / "data" / "processed"

    kayit_klasoru.mkdir(parents=True, exist_ok=True)

    dosya_yolu = kayit_klasoru / dosya_adi

    sonuclar.to_csv(
        dosya_yolu,
        index=False,
        encoding="utf-8-sig"
    )

    return dosya_yolu



def veri_yeterliligini_kontrol_et(sonuclar):
    """
    Her hissenin 6, 12 ve 24 aylik
    analiz icin yeterli verisi olup
    olmadigini kontrol eder.
    """

    if sonuclar.empty:
        return sonuclar.copy()

    gerekli_sutunlar = {
        "Veri_Gunu",
        "Getiri_6A",
        "Getiri_12A",
        "Getiri_24A"
    }

    eksik = gerekli_sutunlar - set(sonuclar.columns)

    if eksik:
        raise ValueError(
            f"Eksik sutunlar: {sorted(eksik)}"
        )

    sonuc = sonuclar.copy()

    donemler = {
        "6A": 127,
        "12A": 253,
        "24A": 505
    }

    for donem, minimum_gun in donemler.items():
        sonuc[f"Yeterli_{donem}"] = (
            (sonuc["Veri_Gunu"] >= minimum_gun)
            & sonuc[f"Getiri_{donem}"].notna()
        )

    return sonuc
