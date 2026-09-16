import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import datetime

DB_NAME = "finance_sentiment.db"

def fetch_finviz_news(ticker):
    url = f"https://finviz.com/quote.ashx?t={ticker}&p=d"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"[{ticker}] Veri çekilemedi, durum kodu: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    news_table = soup.find(id="news-table")
    
    if not news_table:
        print(f"[{ticker}] Haber tablosu bulunamadı.")
        return []

    articles = []
    current_date = ""

    for row in news_table.findAll("tr"):
        title_tag = row.find("a")
        date_tag = row.find("td")

        if title_tag and date_tag:
            title = title_tag.text.strip()
            link = title_tag["href"]
            date_info = date_tag.text.strip().split()

            # Finviz tarih formatını düzenleme (örn: 'Dec-15-23 09:30AM' veya sadece '09:30AM')
            if len(date_info) == 2:
                current_date = date_info[0]
                time_str = date_info[1]
            else:
                time_str = date_info[0]

            published_at = f"{current_date} {time_str}".strip()

            articles.append({
                "ticker": ticker,
                "source": "Finviz",
                "title": title,
                "published_at": published_at,
                "url": link
            })

    return articles

def save_to_db(articles):
    if not articles:
        return 0

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    saved_count = 0

    for item in articles:
        try:
            # INSERT OR IGNORE sayesinde daha önce kaydedilmiş aynı URL tekrar eklenmez
            cursor.execute("""
            INSERT OR IGNORE INTO raw_posts (ticker, source, title, published_at, url)
            VALUES (?, ?, ?, ?, ?)
            """, (item["ticker"], item["source"], item["title"], item["published_at"], item["url"]))
            
            if cursor.rowcount > 0:
                saved_count += 1
        except Exception as e:
            print(f"Kayıt hatası: {e}")

    conn.commit()
    conn.close()
    return saved_count

if __name__ == "__main__":
    # Test için 3 popüler hisse belirleyelim
    tickers = ["AAPL", "NVDA", "TSLA"]
    
    for ticker in tickers:
        print(f"{ticker} için haberler çekiliyor...")
        news = fetch_finviz_news(ticker)
        added = save_to_db(news)
        print(f"-> {ticker}: {len(news)} haber bulundu, {added} yeni haber veritabanına eklendi.")