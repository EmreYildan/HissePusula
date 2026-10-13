# Hisse Pusula 📈

**Borsa İstanbul (BIST) hisseleri için Python tabanlı teknik analiz, geçmiş getiri ve risk araştırma projesi.**

Hisse Pusula, bir hisse senedinin tarihsel fiyat ve hacim verilerini inceleyerek teknik göstergeleri, farklı yatırım ufuklarındaki geçmiş getirileri ve risk ölçülerini anlaşılır biçimde sunmayı amaçlayan bireysel bir bitirme projesidir. İlerleyen aşamalarda hisseler arası karşılaştırma, temel analiz, açıklanabilir puanlama ve geriye dönük değerlendirme eklenecektir.

> **Uyarı:** Bu proje eğitim ve araştırma amaçlıdır. Yatırım tavsiyesi vermez; geçmiş performans gelecekteki getiriyi garanti etmez. Mevcut sürüm gelecek fiyatları tahmin etmez.

## Mevcut durum

| Bileşen | Durum |
| --- | --- |
| Hisse adı/kodu arama | Çalışıyor |
| Yahoo Finance üzerinden OHLCV verisi çekme ve CSV'ye kaydetme | Çalışıyor |
| Veri kalite kontrolü ve son eksik günü temizleme | Çalışıyor |
| Teknik göstergeler ve birleşik Plotly grafiği | Çalışıyor |
| 6, 12 ve 24 aylık geçmiş getiri analizi | Çalışıyor |
| 6, 12 ve 24 aylık volatilite ve maksimum düşüş | Çalışıyor |
| Eksik hafta içi tarihlerini bulma | Çalışıyor; resmî tatil ayrımı henüz tüm yılları kapsamıyor |
| CSV tabanlı BIST tatil takvimi (2026 tam/yarım gün ayrımı) | İlk sürüm tamamlandı |
| Otomatik testler | Son bildirilen çalıştırmada **31 test başarılı** |
| Çoklu hisse karşılaştırma | İlk modül taslağı hazır; entegrasyon ve testler tamamlanmadı |
| Temel analiz, puanlama, backtest, makine öğrenmesi, web arayüzü | Planlanıyor |

## Kullanılan teknolojiler

- **Python 3.11** — uygulama dili
- **pandas, NumPy** — veri işleme ve sayısal hesaplamalar
- **yfinance** — Yahoo Finance üzerinden geçmiş piyasa verileri
- **Plotly** — etkileşimli grafikler
- **unittest** — otomatik testler
- **Git / GitHub** — sürüm kontrolü
- **VS Code / Windows PowerShell** — geliştirme ortamı

## Proje yapısı

```text
HissePusula/
├── main.py
├── README.md
├── src/
│   ├── hisse_arama.py
│   ├── veri_cekme.py
│   ├── veri_kontrol.py
│   ├── bist_takvimi.py
│   ├── teknik_analiz.py
│   ├── grafik.py
│   ├── getiri_analizi.py
│   ├── risk_analizi.py
│   └── hisse_karsilastirma.py  # Taslak / geliştirme aşaması
├── tests/
│   ├── test_teknik_analiz.py
│   ├── test_getiri_analizi.py
│   ├── test_risk_analizi.py
│   └── test_bist_takvimi.py
├── data/
│   ├── raw/                  # İndirilen hisse CSV'leri
│   └── processed/
│       └── bist_tatilleri.csv
└── models/                   # İlerideki model çalışmaları için
```

> Dosya ağacı geliştirme planını da gösterir; `hisse_karsilastirma.py` henüz oluşturulmadıysa bu aşamada zorunlu değildir.

## Kurulum ve çalıştırma

Windows PowerShell'de proje klasöründe:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install pandas numpy yfinance plotly
python main.py
```

Program hisse adı veya kodu ister. Örneğin `THYAO`, `ASELS` veya `TUPRS` girilebilir. Veri kaynağının desteklediği hisse ve tarih aralıkları değişebilir.

### Testler

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

Son doğrulanan geliştirme aşamasında **31 test** geçmiştir. Bu sayı yeni özelliklerle artacaktır.

## Hesaplanan göstergeler

### Teknik analiz

- Hareketli ortalamalar: **MA20, MA50, MA200**
- **RSI(14)**, **MACD(12, 26, 9)**
- **Bollinger Bantları (20)**
- **ATR(14)** ve fiyatın yüzdesi olarak ATR
- **20 günlük ortalama hacim** ve hacim oranı
- Önceki 20 güne dayalı **destek/direnç** seviyeleri

### Geçmiş getiri

| Dönem | Yaklaşık işlem günü | Hesaplama |
| --- | ---: | --- |
| 6 ay | 126 | `(Close[t] / Close[t-126] - 1) * 100` |
| 12 ay | 252 | `(Close[t] / Close[t-252] - 1) * 100` |
| 24 ay | 504 | `(Close[t] / Close[t-504] - 1) * 100` |

Bunlar **geçmiş gerçekleşmiş getiriler** olup ileriye yönelik tahmin değildir. İşlem günü sayıları yaklaşık takvim karşılıklarıdır; eksik kayıtlar zaman pencerelerini kaydırabilir.

### Risk analizi

- Günlük yüzdesel getiri
- **Yıllıklandırılmış volatilite:** ilgili dönemdeki günlük getirilerin örnek standart sapması × `sqrt(252)`
- **Maksimum düşüş (Maximum Drawdown):** seçilen aralıkta önceki zirveden sonraki en büyük yüzde gerileme
- Tüm mevcut geçmiş için maksimum düşüş ve güncel zirveden düşüş

Dönemsel maksimum düşüş, 126/252/504 günlük aralıklar için başlangıç günü dahil **127/253/505 kapanış fiyatı** üzerinden hesaplanır. Yeterli veri yoksa sonuç gösterilmez.

## Veri kalitesi ve bilinen sınırlamalar

- Kaynak Yahoo Finance'tır; tarihsel kayıtlar eksik, gecikmeli veya sonradan revize edilmiş olabilir.
- `son_eksik_gunu_temizle()` son kaydı kontrol eder; geçmişteki tüm eksik günleri kendiliğinden onarmaz.
- Eksik hafta içi tarihleri taranır. **BIST tatil takvimi şu anda yalnızca 2026 kayıtlarıyla başlamıştır**; 2016–2025 henüz tamamlanmadığından tüm eksik hafta içi tarihleri veri hatası değildir.
- 2026 takviminde **tam gün kapanışlar** filtrelenir; **yarım gün seanslar** işlem günü kabul edilir.
- 12 Ekim 2026 tarihinin sorgulanan veri kaynağında bulunmadığı gözlemlenmiştir; bu tarihin fiyat kaydı alternatif kaynakla henüz doğrulanmamıştır. Eksik fiyatlar tahmin edilerek doldurulmaz.
- Hisseler arası kıyaslamada ortak bitiş tarihi henüz zorunlu tutulmuyor.
- Fiyat getirileri enflasyona göre düzeltilmiş reel getiri değildir. Veri sağlayıcısının fiyat düzeltme yaklaşımı ayrıca doğrulanmalıdır.

## Yol haritası

1. **Veri bütünlüğü:** 2016–2025 resmî BIST takvimini kaynaklarıyla tamamlamak; takvim kapsamı ve eksik işlem günlerini test etmek.
2. **Çoklu hisse karşılaştırması:** aynı tarih itibarıyla 6/12/24 aylık getiri, volatilite ve maksimum düşüşü kıyaslamak; eksik verileri işaretlemek, CSV raporu üretmek.
3. **Temel analiz:** şirket finansalları ve sektör bazlı karşılaştırmalar.
4. **Açıklanabilir puanlama:** geçmiş getiri, risk, teknik ve temel göstergeleri ayrı ayrı değerlendirmek.
5. **Geriye dönük test:** ileriye bilgi sızdırmadan, zaman sıralı doğrulama ve uygun kıyas ölçütleriyle performans incelemek.
6. **İsteğe bağlı ileri aşamalar:** makine öğrenmesi ve Streamlit arayüzü.

## Geliştirme notları

- İşlem günü sayısı ile takvim günü aynı şey değildir.
- `NaN` her zaman hesaplama hatası değildir; yeterli geçmiş veri bulunmamasını gösterebilir.
- Volatilite yıllıklandırılmış bir ölçüdür; 6 aylık toplam getiriyle aynı zaman ölçeğinde değildir.
- Maksimum düşüş hesabında **zirve-dip sırası** korunmalıdır.
- Her yeni modül otomatik testlerle doğrulanmalı, anlamlı geliştirme paketleri Git'e commit edilmelidir.

## Lisans

Henüz bir lisans seçilmemiştir.
