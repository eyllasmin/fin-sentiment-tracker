import sqlite3

DB_NAME = "finance_sentiment.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 1. Ham metinlerin tutulacağı tablo
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS raw_posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker TEXT NOT NULL,
        source TEXT NOT NULL,
        title TEXT NOT NULL,
        published_at TEXT,
        url TEXT UNIQUE
    )
    """)

    # 2. Duygu analizi skorlarının tutulacağı tablo
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sentiment_scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER,
        compound_score REAL,
        sentiment_label TEXT,
        analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (post_id) REFERENCES raw_posts (id)
    )
    """)

    conn.commit()
    conn.close()
    print("Veritabanı ve tablolar başarıyla hazırlandı!")

if __name__ == "__main__":
    init_db()