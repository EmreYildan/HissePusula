
import pandas as pd
from pathlib import Path


HISSELER = ["THYAO", "ASELS", "TUPRS"]

VERI_KLASORU = Path("data/raw")


def veri_denetimi_yap():

    for hisse in HISSELER:

        dosya = VERI_KLASORU / f"{hisse}.csv"

        print(f"\n{'=' * 45}")
        print(f"HISSE: {hisse}")
        print(f"{'=' * 45}")

        if not dosya.exists():
            print("HATA: Veri dosyasi bulunamadi.")
            continue

        veri = pd.read_csv(
            dosya,
            index_col=0,
            parse_dates=True
        )

        print("Satir sayisi:", len(veri))
        print("Ilk tarih:", veri.index.min())
        print("Son tarih:", veri.index.max())

        print(
            "Tekrarlanan tarih:",
            veri.index.duplicated().sum()
        )

        print(
            "Tarihler sirali mi:",
            veri.index.is_monotonic_increasing
        )

        print(
            "Eksik degerler:"
        )
        print(veri.isna().sum())

        if "Close" in veri.columns:

            print(
                "Sifir veya negatif kapanis:",
                (veri["Close"] <= 0).sum()
            )

            print(
                "Son 5 kapanis:"
            )
            print(veri["Close"].tail(5))

        print(
            "Veri dosyasi boyutu:",
            dosya.stat().st_size,
            "byte"
        )


if __name__ == "__main__":
    veri_denetimi_yap()
