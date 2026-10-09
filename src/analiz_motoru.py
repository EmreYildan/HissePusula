
import pandas as pd

# THYAO verilerini oku
veriler = pd.read_csv("data/raw/THYAO.csv")

# Tarih sütununu tarih tipine dönüştür
veriler["Date"] = pd.to_datetime(veriler["Date"])

# Tarihe göre sırala
veriler = veriler.sort_values("Date")

# 20 ve 50 günlük hareketli ortalamalar
veriler["MA20"] = veriler["Close"].rolling(window=20).mean()
veriler["MA50"] = veriler["Close"].rolling(window=50).mean()

print("=== HISSE PUSULA - TEKNIK ANALIZ ===")

# Son 5 işlem gününü göster
print("\nSon 5 gunun teknik analiz verileri:")
print(veriler[["Date", "Close", "MA20", "MA50"]].tail())

# Son işlem gününün değerleri
son = veriler.iloc[-1]

print("\nSon kapanis fiyati:", round(son["Close"], 2))
print("20 gunluk ortalama:", round(son["MA20"], 2))
print("50 gunluk ortalama:", round(son["MA50"], 2))


#RSI ANALİZ 14 günlük


fiyat_degisim = veriler["Close"].diff()

kazanc = fiyat_degisim.clip(lower=0)
kayip = -fiyat_degisim.clip(upper=0)

# Wilder yöntemiyle RSI hesaplama
ortalama_kazanc = kazanc.ewm(
    alpha=1/14,
    adjust=False,
    min_periods=14
).mean()

ortalama_kayip = kayip.ewm(
    alpha=1/14,
    adjust=False,
    min_periods=14
).mean()

rs = ortalama_kazanc / ortalama_kayip

veriler["RSI14"] = 100 - (100 / (1 + rs))

print("\n=== RSI ANALIZI ===")
print(veriler[["Date", "Close", "RSI14"]].tail())

son_rsi = veriler["RSI14"].iloc[-1]

print("\nSon RSI14:", round(son_rsi, 2))

if son_rsi < 30:
    print("Yorum: Asiri satim bolgesi")
elif son_rsi > 70:
    print("Yorum: Asiri alim bolgesi")
else:
    print("Yorum: Normal RSI araligi")
