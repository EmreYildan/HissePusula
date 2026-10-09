# Hisse Pusula — Proje Geliştirme Günlüğü

> Bu belge, bitirme projesi boyunca gerçekleştirilen işlemleri, kullanılan araçları, teknik kararları, karşılaşılan sorunları ve sonraki adımları kaydetmek için hazırlanmıştır.

**Proje adı:** Hisse Pusula  
**Akademik başlık:** BIST Hisse Senetlerinin Teknik Analizi ve Makine Öğrenmesi ile Fiyat Yönü Tahmini  
**Çalışma biçimi:** Bireysel bitirme projesi  
**Başlangıç tarihi:** 8 Ekim 2026  
**Geliştirme ortamı:** Windows, Visual Studio Code, Python 3.11.0

## 1. Projenin amacı

Borsa İstanbul'da işlem gören seçili hisselerin tarihsel fiyat ve işlem hacmi verilerini analiz etmek; teknik göstergeleri hesaplamak; makine öğrenmesiyle gelecek beş işlem günündeki fiyat yönü için olasılıksal tahminler üretmek; risk göstergelerini ve model performansını web arayüzünde sunmak.

**Not:** Sistem kesin fiyat tahmini veya yatırım tavsiyesi vermek için değil, analiz ve akademik karar desteği için geliştirilecektir.

## 2. Planlanan kapsam

- Başlangıçta THYAO için veri çekme ve kalite kontrolü
- Sonrasında ASELS, TUPRS, BIMAS ve AKBNK verilerinin denenmesi
- RSI, MACD, hareketli ortalamalar ve volatilite hesaplamaları
- Logistic Regression, Random Forest ve XGBoost modellerinin karşılaştırılması
- Zaman sıralı eğitim/doğrulama/test değerlendirmesi
- Streamlit ile grafik ve sonuçların gösterimi
- İsteğe bağlı: açıklanabilirlik (SHAP), strateji simülasyonu

## 3. Kullanılan ve planlanan teknolojiler

| Teknoloji | Kullanım amacı | Durum |
|---|---|---|
| Windows | Geliştirme işletim sistemi | Kullanılıyor |
| Visual Studio Code | Kod editörü ve terminal | Kullanılıyor |
| Python 3.11.0 | Ana programlama dili | Kurulu, sürüm kullanıcı tarafından bildirildi |
| Python `venv` | Projeye özel sanal ortam | Oluşturuldu ve etkinleştirildi |
| pip | Python paket yöneticisi | Kullanılıyor |
| yfinance | Tarihsel hisse verisi alma | Kurulum denendi, henüz doğrulanmadı |
| pandas | Veri işleme ve CSV çıktısı | Kurulum denendi, henüz doğrulanmadı |
| NumPy / Scikit-learn / XGBoost | Analiz ve makine öğrenmesi | Planlandı |
| Streamlit / Plotly | Web arayüzü ve grafikler | Planlandı |
| SQLite | Yerel veri saklama | Planlandı |

## 4. Geliştirme kayıtları

### 8 Ekim 2026 — İlk kurulum

**Yapılanlar**
1. Proje adı **Hisse Pusula** olarak belirlendi.
2. Windows üzerinde Visual Studio Code ile geliştirme kararı alındı.
3. `HissePusula` proje klasörü oluşturuldu.
4. Python 3.11.0 sürümü bildirildi.
5. `py -3.11 -m venv .venv` komutuyla sanal ortam oluşturuldu.
6. PowerShell'de sanal ortam etkinleştirildi; terminalde `(.venv)` görüldü.
7. `python -m pip install yfinance pandas` komutuyla kütüphane kurulumu başlatıldı.

**Karşılaşılan sorun**

Paket indirme sırasında aşağıdaki mesaj alındı:

```text
ERROR: Operation cancelled by user
```

İşlem tamamlanmadığı için `yfinance` ve `pandas` kurulumları **henüz başarılı kabul edilmiyor**. Hatanın kesin nedeni doğrulanmadı; işlem kullanıcı tarafından iptal edilmiş olabilir.

**Planlanan çözüm ve doğrulama**

```powershell
python -m pip install --upgrade pip
python -m pip install yfinance pandas
python -c "import yfinance; import pandas; print('Hisse Pusula kutuphaneleri hazir!')"
```

Son komut başarıyla çalışırsa paketler kurulu olarak işaretlenecek.

## 5. Sıradaki işler

- [ ] pip güncellemesini tamamla.
- [ ] `yfinance` ve `pandas` kurulumunu doğrula.
- [ ] `veri_test.py` dosyasını oluştur.
- [ ] THYAO.IS için bir yıllık günlük fiyat verisi çek.
- [ ] Verinin tarih, satır sayısı, boş değer, tekrar eden tarih ve hacim kontrollerini yap.
- [ ] CSV dosyasına kaydet.
- [ ] Diğer dört BIST hissesini dene.
- [ ] Veri kaynağının erişim ve kullanım koşullarını değerlendir.

## 6. Teknik kararlar ve gerekçeleri

**Neden Python?** Finansal veri işleme, görselleştirme ve makine öğrenmesi için zengin bir kütüphane ekosistemine sahiptir.

**Neden `venv`?** Projeye ait kütüphaneleri diğer Python kurulumlarından ayırır ve sürüm yönetimini kolaylaştırır.

**Neden önce veri testi?** Hisse verilerine güvenilir biçimde erişilememesi, daha sonraki analiz ve model geliştirme aşamalarını doğrudan etkiler. Bu riski en başta görmek istiyoruz.

**Neden ilk olarak tek hisse?** THYAO ile uçtan uca veri çekme ve kaydetme sürecini doğruladıktan sonra diğer hisselere genişlemek daha kontrollüdür.

## 7. Sunum ve rapor için biriktirilecek kanıtlar

- Kurulum ve kütüphane sürümlerinin terminal çıktıları
- Veri çekme kodu ve CSV örneği
- Veri kalite kontrol sonuçları
- Teknik gösterge grafikleri
- Modellerin karşılaştırma tabloları
- Web uygulamasının ekran görüntüleri
- Karşılaşılan hatalar ve çözümleri

## 8. Günlük kayıt şablonu

Yeni çalışma günlerinde aşağıdaki şablonu çoğalt:

```markdown
### YYYY-AA-GG — Çalışma başlığı
**Hedef:**

**Yapılan işlemler:**
1.

**Kullanılan araçlar / komutlar:**

**Sonuç ve kanıt:**

**Karşılaşılan sorunlar ve çözümler:**

**Sonraki adım:**
```

---

*Bu belge yaşayan bir proje günlüğüdür. Her önemli aşamadan sonra gerçek sonuçlara göre güncellenmelidir.*

## 9. CHECKPOINT 1 — 8 Ekim 2026: Dinamik analiz pipeline'ı çalışıyor

**Durum:** Kullanıcı, `python main.py` ile veri kontrolü dahil pipeline'ın başarıyla çalıştığını bildirdi. Bu kayıt, yukarıdaki ilk kurulum dönemine ait ve artık güncelliğini yitirmiş kontrol listesi/statülerin yerine geçer.

### Tamamlanan işler
- Python 3.11 ve `.venv` ile geliştirme ortamı kuruldu; `yfinance` ve `pandas` kullanılarak veri indirme çalıştırıldı.
- Windows'ta pandas DLL içe aktarma sorunu `pandas==2.2.3` yeniden kurulumu ile çözüldü.
- THYAO için yaklaşık bir yıllık günlük OHLCV verisi çekilip CSV'ye kaydedildi; temel kalite kontrolleri yapıldı.
- `src/hisse_arama.py`: bilinen şirket adları kodlara çevriliyor; sözlükte olmayan, biçimi uygun hisse kodları da veri kaynağında deneniyor. Şirket adı eşleştirme listesi henüz sınırlı.
- `src/veri_cekme.py`: kullanıcı koduna `.IS` ekleyerek Yahoo Finance verisini çekiyor.
- `src/veri_kontrol.py`: gerekli sütunlar, minimum 50 satır, eksik değerler, yinelenen tarihler, fiyat/hacim ve OHLC tutarlılığı denetleniyor.
- `src/teknik_analiz.py`: MA20, MA50, RSI14 hesaplıyor; trend, hareketli ortalama ilişkisi ve RSI yorumu üretiyor.
- `main.py`: hisse girişi → kod çözümleme → veri çekme → kalite kontrolü → teknik göstergeler → yorumlama akışını tek komutla yönetiyor.

### Kullanılan komut
```powershell
python main.py
```

### Mimari kararlar
- Hesaplama fonksiyonları kullanıcı arayüzünden ayrılacak; ileride Streamlit tarafından yeniden kullanılabilecek.
- THYAO sadece test örneği, kullanıcı farklı BIST hisselerini seçebiliyor.
- Bilinmeyen kodun biçimsel kabulü, BIST'te listelendiğinin doğrulanması anlamına gelmiyor.
- Mevcut kalite kontrolü yapısal tutarlılığı denetler; resmi piyasa verisiyle doğrulama değildir.
- Teknik analiz yorumları kesin fiyat tahmini veya yatırım tavsiyesi değildir.

### Sonraki aşamalar
1. Teknik gösterge kapsamını genişlet: MACD, Bollinger Bantları, SMA200, ATR, hacim göstergeleri. **SMA200 için veri çekme süresini en az 200 işlem gününü kapsayacak şekilde kontrol et.**
2. Gösterge hesaplamalarını bilinen örnekler ve sınır durumlarıyla test et; veri kontrolü için hatalı veri senaryoları ekle.
3. Şirket adından arama için güncellenebilir ve kapsamlı BIST sembol listesi oluştur.
4. Streamlit arayüzü ve grafikler geliştir.
5. Makine öğrenmesi için 5 işlem günü ileri yön etiketleri, kronolojik eğitim/test ayrımı ve veri sızıntısı önlemleri oluştur.
6. Basit temel model ile Logistic Regression, Random Forest ve uygun görülürse XGBoost'u karşılaştır; accuracy, precision, recall, F1 ve backtest raporla.
7. Bitirme raporu, yöntem, test çıktıları ve sunum materyallerini hazırla.

### Bilinen sınırlar / teknik borç
- `teknik_analizi_yorumla()` şimdilik `print()` kullanıyor; web arayüzünde kullanılmak üzere yapılandırılmış sonuç döndürmesi planlanıyor.
- RSI hesaplama yöntemi önceki EWM sürümünden Wilder'ın SMA ile başlatılan sürümüne değiştirilmiş olabilir; sayısal sonuçlar test edilmeli.
- Yalnızca 50 işlem günü şartı, ileride SMA200 eklendiğinde yeterli olmayacak.
- Veriler Yahoo Finance kaynaklıdır; kapsama, güncellik ve düzeltilmiş fiyat politikası belgelenmeli.

**Checkpoint sonucu:** Veri indirme, kalite kontrolü ve temel teknik analiz tek giriş noktasında birleştirildi. Henüz makine öğrenmesi modeli veya doğrulanmış tahmin performansı yok.
