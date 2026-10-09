
# Kullanici girislerini hisse kodlarina eslestiriyoruz

HISSELER = {
    "ASELS": ["ASELSAN", "ASELSAN ELEKTRONIK"],
    "THYAO": ["TURK HAVA YOLLARI", "THY", "TURKISH AIRLINES"],
    "TUPRS": ["TUPRAS"],
    "BIMAS": ["BIM", "BIM MAGAZALARI"],
    "AKBNK": ["AKBANK"]
}


def metni_duzenle(metin):
    metin = metin.strip().upper()

    # Turkce karakterleri standartlastir
    ceviriler = str.maketrans(
        "ÇĞİÖŞÜ",
        "CGIOSU"
    )

    return metin.translate(ceviriler)


def hisse_kodu_bul(arama):
    arama = metni_duzenle(arama)

    if not arama:
        return None

    # .IS uzantisini kaldir
    if arama.endswith(".IS"):
        arama = arama[:-3]

    # Once bilinen sirket adlarini kontrol et
    for kod, isimler in HISSELER.items():
        if arama == kod or arama in isimler:
            return kod

    # Bilinmeyen ama kod formatina uygun girisleri
    # veri kaynaginda kontrol edilmek uzere kabul et
    if arama.isalpha() and 3 <= len(arama) <= 6:
        return arama

    return None

if __name__ == "__main__":
    arama = input("Hisse adi veya kodu girin: ")

    sonuc = hisse_kodu_bul(arama)

    if sonuc:
        print(f"Bulunan hisse: {sonuc}.IS")
    else:
        print("Hisse bulunamadi.")
