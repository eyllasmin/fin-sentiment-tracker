import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

DB_NAME = "finance_sentiment.db"

st.set_page_config(page_title="Finans Duygu Takip Paneli", layout="wide")
st.title("📈 Hisse Senedi Duygu & Trend Analiz Paneli")

def load_data():
    conn = sqlite3.connect(DB_NAME)
    query = """
    SELECT 
        r.ticker, 
        r.title, 
        r.published_at, 
        s.compound_score, 
        s.sentiment_label,
        s.analyzed_at
    FROM raw_posts r
    INNER JOIN sentiment_scores s ON r.id = s.post_id
    ORDER BY s.analyzed_at DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

df = load_data()

if df.empty:
    st.warning("Veritabanında henüz analiz edilmiş veri bulunmuyor.")
else:
    # Kenar Çubuğu - Filtreler
    st.sidebar.header("Filtreleme Seçenekleri")
    tickers = df["ticker"].unique().tolist()
    selected_ticker = st.sidebar.selectbox("Hisse Seçin:", tickers)

    ticker_df = df[df["ticker"] == selected_ticker]

    # Üst Metrik Kartları
    avg_score = ticker_df["compound_score"].mean()
    total_news = len(ticker_df)
    pos_count = len(ticker_df[ticker_df["sentiment_label"] == "positive"])
    pos_ratio = (pos_count / total_news * 100) if total_news > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Ortalama Duygu Skoru", f"{avg_score:.2f}")
    col2.metric("Toplam Haber Sayısı", total_news)
    col3.metric("Pozitif Haber Oranı", f"%{pos_ratio:.1f}")

    # Görselleştirmeler
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("Duygu Dağılımı")
        label_counts = ticker_df["sentiment_label"].value_counts().reset_index()
        label_counts.columns = ["Duygu", "Adet"]
        fig_pie = px.pie(label_counts, names="Duygu", values="Adet", hole=0.4,
                         color="Duygu",
                         color_discrete_map={"positive": "#2ecc71", "negative": "#e74c3c", "neutral": "#95a5a6"})
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_chart2:
        st.subheader("Skor Dağılımı (Histogram)")
        fig_hist = px.histogram(ticker_df, x="compound_score", nbins=15, 
                                labels={"compound_score": "Duygu Skoru (-1 ile +1)"},
                                color_discrete_sequence=["#3498db"])
        st.plotly_chart(fig_hist, use_container_width=True)

    # Haber Listesi Tablosu
    st.subheader(f"Son {selected_ticker} Haberleri ve Skorları")
    st.dataframe(ticker_df[["published_at", "title", "sentiment_label", "compound_score"]], use_container_width=True)