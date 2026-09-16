import time
from scraper import fetch_finviz_news, save_to_db
from sentiment_analyzer import process_and_save

TICKERS = ["AAPL", "NVDA", "TSLA"]

def run_pipeline():
    print("=" * 50)
    print("--- [1/2] Veri Toplama Başlatılıyor ---")
    total_added = 0
    for ticker in TICKERS:
        articles = fetch_finviz_news(ticker)
        added = save_to_db(articles)
        total_added += added
        print(f"{ticker}: {added} yeni haber eklendi.")
    
    print(f"Toplam yeni kayıt: {total_added}")
    print("=" * 50)
    
    print("--- [2/2] FinBERT Duygu Analizi Başlatılıyor ---")
    process_and_save()
    print("Pipeline turu başarıyla tamamlandı!")
    print("=" * 50)

if __name__ == "__main__":
    run_pipeline()