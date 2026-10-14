# Hisse Pusula 📈

**Borsa İstanbul (BIST) hisseleri için Python tabanlı teknik analiz, geçmiş getiri, risk analizi ve hisse karşılaştırma projesi.**

Hisse Pusula, Borsa İstanbul'da işlem gören hisse senetlerinin tarihsel fiyat ve işlem hacmi verilerini analiz ederek yatırım araştırmalarını desteklemeyi amaçlayan bireysel bir bitirme projesidir.

Uygulama; teknik göstergeler, geçmiş getiriler, risk ölçümleri ve çoklu hisse karşılaştırmaları sunar. Verilerin güvenilirliğini değerlendirmek amacıyla BIST işlem takvimi ve veri kalitesi kontrolleri de içerir.

> **Uyarı:** Bu proje eğitim ve araştırma amaçlıdır. Yatırım tavsiyesi sunmaz. Geçmiş performans gelecekteki getirileri garanti etmez. Mevcut sürüm gelecekteki hisse fiyatlarını tahmin etmez.

## 1. Projenin mevcut durumu

| Bileşen | Durum |
|---|---|
| Hisse adı veya koduyla arama | Tamamlandı |
| Yahoo Finance üzerinden geçmiş veri çekme | Tamamlandı |
| OHLCV verilerini CSV olarak kaydetme | Tamamlandı |
| Veri bütünlüğü ve kalite kontrolleri | Tamamlandı |
| CSV tabanlı BIST tatil takvimi (2016–2026) | İlk sürüm hazır |
| Teknik göstergeler | Tamamlandı |
| Plotly ile etkileşimli grafikler | Tamamlandı |
| 6, 12 ve 24 aylık geçmiş getiri analizi | Tamamlandı |
| Dönemsel volatilite ve maksimum düşüş | Tamamlandı |
| Çoklu hisse karşılaştırma modülü | Tamamlandı |
| Ortak analiz tarihi kontrolü | Tamamlandı |
| Veri yeterliliği ve kalite bilgileri | Tamamlandı |
| Otomatik testler | 44 test başarılı |
| Temel analiz ve açıklanabilir puanlama | Planlanıyor |
| Backtest, makine öğrenmesi ve web arayüzü | Gelecek aşamalar |

**Not:** BIST takviminde 2016–2026 yılları için kayıtlar bulunmaktadır. Takvim verilerinin resmî kaynaklarla son doğrulaması ayrıca yapılmalıdır.

## 2. Kullanılan teknolojiler

- **Python 3.11:** Uygulama geliştirme
- **pandas:** Finansal zaman serilerinin işlenmesi
- **NumPy:** Sayısal hesaplamalar
- **yfinance:** Yahoo Finance üzerinden piyasa verileri
- **Plotly:** Etkileşimli finansal grafikler
- **unittest:** Otomatik birim testleri
- **Git ve GitHub:** Sürüm kontrolü
- **VS Code:** Geliştirme ortamı

## 3. Proje yapısı

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
│   └── hisse_karsilastirma.py
├── tests/
│   ├── test_bist_takvimi.py
│   ├── test_getiri_analizi.py
│   ├── test_hisse_karsilastirma.py
│   ├── test_risk_analizi.py
│   └── test_teknik_analiz.py
├── data/
│   ├── raw/
│   └── processed/
│       └── bist_tatilleri.csv
└── models/
```

`data/raw/` klasörü indirilen hisse verilerini, `data/processed/` klasörü ise işlenmiş verileri ve karşılaştırma sonuçlarını içerir.

## 4. Kurulum

Python 3.11 yüklü bir Windows bilgisayarda proje klasörünü açın.

### Sanal ortam oluşturma

```powershell
py -3.11 -m venv .venv
```

### Sanal ortamı etkinleştirme

```powershell
.\.venv\Scripts\Activate.ps1
```

### Gerekli kütüphaneleri yükleme

```powershell
python -m pip install pandas numpy yfinance plotly
```

### Uygulamayı çalıştırma

```powershell
python main.py
```

Program üzerinden hisse adı veya kodu ile arama yapılabilir.

Örnek hisse kodları:

- `THYAO`
- `ASELS`
- `TUPRS`

Veri sağlayıcısına yapılan sorgularda BIST hisseleri için uygun borsa uzantısı kullanılabilir.

## 5. Teknik analiz göstergeleri

Uygulamada aşağıdaki teknik göstergeler hesaplanmaktadır.

| Gösterge | Kullanım amacı |
|---|---|
| MA20 | Kısa vadeli fiyat eğilimi |
| MA50 | Orta vadeli fiyat eğilimi |
| MA200 | Uzun vadeli fiyat eğilimi |
| RSI(14) | Fiyat hareketlerinin göreli gücü |
| MACD(12,26,9) | Momentum ve trend değişimlerinin incelenmesi |
| Bollinger Bantları(20) | Fiyat oynaklığının değerlendirilmesi |
| ATR(14) | Ortalama gerçek fiyat aralığı |
| Hacim oranı | Güncel hacmin geçmiş ortalamayla karşılaştırılması |
| Destek/direnç | Önceki 20 işlem gününe dayalı fiyat seviyeleri |

Teknik göstergeler tek başına alım veya satım sinyali olarak değerlendirilmemelidir.

## 6. Geçmiş getiri analizi

Hisselerin geçmiş performansı yaklaşık işlem günü esasına göre üç dönemde hesaplanmaktadır.

| Dönem | İşlem günü |
|---|---:|
| 6 ay | 126 |
| 12 ay | 252 |
| 24 ay | 504 |

Getiri formülü:

```text
Getiri (%) = (Son Kapanış / Önceki Kapanış - 1) × 100
```

Örneğin 12 aylık geçmiş getiri hesaplanırken güncel kapanış fiyatı, 252 gözlem önceki kapanış fiyatıyla karşılaştırılır.

Bu değerler geçmiş gerçekleşmiş getirileri ifade eder. Gelecekteki performansı tahmin etmez.

## 7. Risk analizi

### Yıllıklandırılmış volatilite

Günlük fiyat getirilerinin standart sapması kullanılarak hesaplanır.

```text
Yıllık Volatilite = Günlük Getiri Standart Sapması × √252
```

Sonuç yüzde cinsinden ifade edilir.

### Maksimum düşüş (Maximum Drawdown)

Bir yatırımın belirli bir dönem içinde önceki zirvesinden sonraki en büyük değer kaybını ölçer.

```text
Düşüş (%) = (Fiyat / Önceki Zirve - 1) × 100
```

Dönemsel maksimum düşüş hesaplamasında başlangıç fiyatı da dikkate alınır.

| Dönem | Gerekli kapanış gözlemi |
|---|---:|
| 6 ay | 127 |
| 12 ay | 253 |
| 24 ay | 505 |

Yeterli geçmiş verinin bulunmadığı dönemlerde sonuçlar eksik değer olarak bırakılabilir.

## 8. Çoklu hisse karşılaştırması

`src/hisse_karsilastirma.py` modülü birden fazla hissenin aynı analiz tarihi itibarıyla karşılaştırılmasını sağlar.

Karşılaştırmada kullanılan ölçütler:

- 6, 12 ve 24 aylık geçmiş getiriler
- 6, 12 ve 24 aylık volatilite
- 6, 12 ve 24 aylık maksimum düşüş
- Kullanılabilir veri günü sayısı
- Veri kalitesi durumu
- Eksik hafta içi günü sayısı
- Dönemlere göre veri yeterliliği

### Ortak analiz tarihi

Hisselerin karşılaştırılabilir olması için tüm hisselerde bulunan en son ortak işlem tarihi belirlenir.

Her hissenin geçmiş getiri ve risk hesaplaması kendi tarihsel verileri üzerinden gerçekleştirilir. Böylece bir hissedeki eksik tarih, diğer hisselerin geçmiş verilerinin gereksiz yere silinmesine neden olmaz.

Ortak tarihten sonraki veriler karşılaştırmaya dahil edilmez.

### Sıralama

Hisseler aşağıdaki ölçütlere göre sıralanabilir:

- Getiri: yüksekten düşüğe
- Volatilite: düşükten yükseğe
- Maksimum düşüş: sıfıra en yakın değerden en büyük kayba

Karşılaştırma sonuçları CSV biçiminde kaydedilebilir.

## 9. Veri kalitesi ve BIST işlem takvimi

Finansal analizlerde kullanılan verilerin doğruluğu sonuçları doğrudan etkileyebilir.

Bu nedenle projede aşağıdaki kontroller uygulanmaktadır:

- Tekrarlanan tarihler
- Eksik değerler
- Geçersiz kapanış fiyatları
- Tarih sıralaması
- Eksik hafta içi günleri
- BIST tam gün tatilleri
- BIST yarım gün seansları
- Takvim kapsamı dışında kalan yıllar

### BIST tatil takvimi

`data/processed/bist_tatilleri.csv` dosyasında 2016–2026 yıllarına ilişkin tam gün kapanış ve yarım gün seans kayıtları bulunmaktadır.

Tam gün kapanışlar beklenen işlem günleri arasından çıkarılır.

Yarım gün seanslar ise işlem günü olarak kabul edilir ve eksik kayıtların kontrolünde korunur.

### Bilinen veri boşlukları

İncelenen THYAO, ASELS ve TUPRS veri kümelerinde aşağıdaki tarihler eksik olarak gözlemlenmiştir:

- **9 Nisan 2024:** BIST yarım gün seansı; eksik kayıt kontrolünde korunmaktadır.
- **12 Ekim 2026:** Veri kaynağında gözlemlenen ve nedeni henüz doğrulanmamış boşluk.

Eksik fiyatlar tahmin edilerek doldurulmaz.

Veri kalitesi raporları temiz, uyarı veya hatalı durumlarını gösterebilir.

## 10. Otomatik testler

Projenin hesaplama ve veri kontrol bileşenleri Python `unittest` altyapısıyla test edilmektedir.

Testleri çalıştırmak için:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

Son başarılı çalıştırmada:

```text
Ran 44 tests

OK
```

Test kapsamındaki başlıca alanlar:

- Teknik gösterge hesaplamaları
- Geçmiş getiri hesaplamaları
- Volatilite ve maksimum düşüş
- BIST tatil takvimi
- Veri yeterliliği
- Çoklu hisse karşılaştırması
- Ortak analiz tarihi
- Veri kalitesi eşleştirmesi
- CSV kaydetme ve sıralama

Testler, tanımlanan senaryolarda beklenen davranışları doğrular; tüm piyasa verilerinin doğruluğunu garanti etmez.

## 11. Bilinen sınırlamalar

1. Veri kaynağı Yahoo Finance'tır. Kayıtlar eksik, gecikmeli veya sonradan değiştirilmiş olabilir.
2. İşlem günü esaslı 6, 12 ve 24 aylık dönemler takvim aylarıyla birebir aynı değildir.
3. Eksik işlem günleri dönemlerin gerçek takvim uzunluğunu etkileyebilir.
4. BIST takvimindeki kayıtların resmî kaynaklarla son doğrulaması devam etmektedir.
5. Hesaplanan getiriler enflasyona göre düzeltilmiş reel getiriler değildir.
6. Fiyat düzeltmelerinin temettü ve bölünmeler açısından etkisi veri sağlayıcısının yöntemine bağlıdır.
7. Teknik göstergeler ve geçmiş performans ölçümleri yatırım tavsiyesi veya gelecek fiyat tahmini değildir.

## 12. Geliştirme yol haritası

### Tamamlanan aşamalar

- Hisse arama ve tarihsel veri toplama
- Teknik analiz göstergeleri
- Etkileşimli grafikler
- Geçmiş getiri ve risk analizi
- BIST takvimi ve veri kalitesi kontrolleri
- Çoklu hisse karşılaştırması
- Otomatik test altyapısı

### Planlanan aşamalar

1. Resmî kaynaklarla veri takviminin son doğrulaması
2. Temel analiz ve finansal oranların entegrasyonu
3. Açıklanabilir hisse değerlendirme sistemi
4. Geriye dönük performans değerlendirmesi (backtest)
5. İsteğe bağlı makine öğrenmesi modelleri
6. Streamlit tabanlı web arayüzü

## 13. Akademik amaç

Hisse Pusula, yazılım geliştirme ve finansal veri analizi yöntemlerini bir araya getiren bireysel bir bitirme projesidir.

Çalışmanın temel amacı, geçmiş piyasa verilerinden hesaplanan teknik ve istatistiksel ölçümleri kullanıcıya anlaşılır, karşılaştırılabilir ve test edilebilir biçimde sunmaktır.

## 14. Lisans

Proje için henüz bir açık kaynak lisansı belirlenmemiştir.