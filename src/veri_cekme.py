
import yfinance as yf
from pathlib import Path


def hisse_verisi_cek(hisse_kodu, donem="1y"):
    # Hisse kodunu düzenle
    hisse_kodu = hisse_kodu.strip().upper()

    # BIST hisseleri için .IS uzantısını ekle
    if not hisse_kodu.endswith(".IS"):
        hisse_kodu += ".IS"

    print(f"\n{hisse_kodu} verileri cekiliyor...")

    # Yahoo Finance üzerinden verileri çek
    veriler = yf.download(
        hisse_kodu,
        period=donem,
        interval="1d",
        auto_adjust=True,
        progress=False,
        multi_level_index=False
    )

    # Veri gelmediyse uyarı ver
    if veriler.empty:
        print("HATA: Hisse verisi bulunamadi.")
        return None

    # Kayıt klasörünü oluştur
    veri_klasoru = Path("data/raw")
    veri_klasoru.mkdir(parents=True, exist_ok=True)

    # Hisse kodunu dosya adı olarak kullan
    dosya_adi = hisse_kodu.replace(".IS", "") + ".csv"
    dosya_yolu = veri_klasoru / dosya_adi

    # Verileri CSV dosyasına kaydet
    veriler.to_csv(dosya_yolu)

    print(f"BASARILI: {len(veriler)} satir veri alindi.")
    print(f"Kaydedilen dosya: {dosya_yolu}")

    return veriler


