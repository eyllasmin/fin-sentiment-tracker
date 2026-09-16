#  Finansal Duygu Durum & Trend Takip Motoru

Piyasa haberlerini otomatik toplayan, **ProsusAI/FinBERT** derin öğrenme modeli ile finansal jargona özel duygu analizi gerçekleştiren ve sonuçları **Streamlit** ile **Plotly** üzerinden görselleştiren uçtan uca veri analitiği hattı.

![Dashboard Görünümü](fin-sentiment-tracker/docs/dashboard_preview.png)

---

##  Temel Özellikler

* **Otomatik Haber Kazıma:** Popüler hisse senetleri (AAPL, NVDA, TSLA) için güncel finans haberlerini BeautifulSoup ile çeker.
* **Finansal NLP Modellemesi:** FinBERT kullanarak haber başlıklarını analiz eder; -1.0 ile +1.0 arasında duygu puanı (compound score) ve duygu etiketi (Pozitif, Negatif, Nötr) üretir.
* **İlişkisel Veri Depolama:** Ham metinleri ve analiz sonuçlarını ilişkisel SQLite veritabanında mükerrer kayıt kontrolü yaparak saklar.
* **Etkileşimli Karar Paneli:** Seçilen hisseye göre anlık dağılım grafikleri, duygu yüzdeleri ve filtrelenebilir haber listesi sunar.

---

##  Teknolojiler

* **Programlama Dili:** Python
* **NLP & Makine Öğrenmesi:** Hugging Face Transformers, PyTorch, FinBERT
* **Veri Kazıma & İşleme:** Requests, BeautifulSoup4, Pandas
* **Veritabanı:** SQLite
* **Arayüz & Görselleştirme:** Streamlit, Plotly

---

## Proje Yapısı

```text
fin-sentiment-tracker/
│
├── database.py             # SQLite veritabanı ve tablo oluşturma script'i
├── scraper.py              # Finviz haber kazıma modülü
├── sentiment_analyzer.py   # FinBERT modeli ile puanlama modülü
├── main_pipeline.py        # Tüm hattı tek seferde çalıştıran orkestrasyon
├── app.py                  # Streamlit etkileşimli kontrol paneli
├── requirements.txt        # Proje kütüphane bağımlılıkları
└── README.md
