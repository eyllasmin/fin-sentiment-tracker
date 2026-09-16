import sqlite3
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

DB_NAME = "finance_sentiment.db"
MODEL_NAME = "ProsusAI/finbert"

print("FinBERT modeli ve tokenizer yükleniyor, lütfen bekleyin...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

LABELS = ["positive", "negative", "neutral"]

def get_unprocessed_posts():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Henüz duygu analizi yapılmamış haberleri getir
    query = """
    SELECT r.id, r.title 
    FROM raw_posts r
    LEFT JOIN sentiment_scores s ON r.id = s.post_id
    WHERE s.id IS NULL
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows

def analyze_sentiment(texts):
    if not texts:
        return []

    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
        # Olasılıklara dönüştür (Softmax)
        probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)

    results = []
    for probs in probabilities:
        pos_prob = probs[0].item()
        neg_prob = probs[1].item()
        neu_prob = probs[2].item()

        # -1.0 ile +1.0 arası bileşik skor: (Pozitiflik - Negatiflik)
        compound_score = round(pos_prob - neg_prob, 4)

        # En yüksek olasılıklı sınıfı belirleme
        max_idx = torch.argmax(probs).item()
        sentiment_label = LABELS[max_idx]

        results.append((compound_score, sentiment_label))
        
    return results

def process_and_save():
    posts = get_unprocessed_posts()
    if not posts:
        print("Analiz edilecek yeni haber bulunamadı.")
        return

    print(f"Toplam {len(posts)} adet yeni haber analiz ediliyor...")

    post_ids = [p[0] for p in posts]
    titles = [p[1] for p in posts]

    # Modelden duygu skorlarını al
    scores = analyze_sentiment(titles)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    for post_id, (score, label) in zip(post_ids, scores):
        cursor.execute("""
        INSERT INTO sentiment_scores (post_id, compound_score, sentiment_label)
        VALUES (?, ?, ?)
        """, (post_id, score, label))

    conn.commit()
    conn.close()
    print(f"{len(posts)} haber başarıyla puanlandı ve veritabanına kaydedildi!")

if __name__ == "__main__":
    process_and_save()