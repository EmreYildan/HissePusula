
import yfinance as yf
import pandas as pd

print("=== HISSE PUSULA ===")
print("THYAO hisse verileri kontrol ediliyor...")

# Türk Hava Yolları hisse kodu
hisse = "THYAO.IS"

# Son 1 yıllık günlük verileri çek
veriler = yf.download(
    hisse,
    period="1y",
    interval="1d",
    auto_adjust=True,
    progress=False,
    multi_level_index=False
)

if veriler.empty:
    print("HATA: Hisse verileri alınamadı!")
else:
    print("\nVeri çekme başarılı!")

    print("\nİlk 5 satır:")
    print(veriler.head())

    print("\nSon 5 satır:")
    print(veriler.tail())

    print("\nToplam veri sayısı:", len(veriler))

    # Verileri CSV dosyasına kaydet
    veriler.to_csv("data/raw/THYAO.csv")

    print("\nVeriler data/raw/THYAO.csv dosyasına kaydedildi.")