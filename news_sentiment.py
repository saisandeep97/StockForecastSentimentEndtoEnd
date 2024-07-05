import requests
from datetime import datetime, timedelta
from textblob import TextBlob
import pandas as pd
import os
import json

NEWS_DATA_DIR = "news_data"

def get_news(api_key, ticker, days=7):
    """
    Fetch news articles related to a stock using NewsAPI or load from CSV if available.
    
    :param api_key: Your NewsAPI key
    :param ticker: Stock symbol
    :param days: Number of days to look back for news articles
    :return: List of dictionaries containing news data
    """
    # Create news data directory if it doesn't exist
    if not os.path.exists(NEWS_DATA_DIR):
        os.makedirs(NEWS_DATA_DIR)
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Construct file path
    file_path = os.path.join(NEWS_DATA_DIR, f"{ticker}_news_{start_date.strftime('%Y-%m-%d')}_{end_date.strftime('%Y-%m-%d')}.csv")
    
    # Check if we have recent news data stored
    if os.path.exists(file_path):
        stored_data = pd.read_csv(file_path, parse_dates=['publishedAt'])
        last_stored_date = stored_data['publishedAt'].max()
        
        # If stored data is up to date, return it
        if last_stored_date.date() == end_date.date():
            print(f"Loading news data for {ticker} from CSV file.")
            return stored_data.to_dict('records')
        
        # If stored data is outdated, update it
        print(f"Updating news data for {ticker}.")
        new_start_date = last_stored_date + timedelta(seconds=1)
        new_articles = fetch_news(api_key, ticker, new_start_date, end_date)
        
        if new_articles:
            new_data = pd.DataFrame(new_articles)
            updated_data = pd.concat([stored_data, new_data]).drop_duplicates(subset=['title']).reset_index(drop=True)
            updated_data.to_csv(file_path, index=False)
            return updated_data.to_dict('records')
        else:
            print(f"No new news data available for {ticker}. Using stored data.")
            return stored_data.to_dict('records')
    
    # If no stored data, fetch all data
    print(f"Fetching all news data for {ticker}.")
    articles = fetch_news(api_key, ticker, start_date, end_date)
    
    if articles:
        pd.DataFrame(articles).to_csv(file_path, index=False)
    
    return articles

def fetch_news(api_key, ticker, start_date, end_date):
    """
    Fetch news articles from NewsAPI.
    """
    base_url = "https://newsapi.org/v2/everything"
    
    params = {
        'q': ticker,
        'from': start_date.strftime('%Y-%m-%d'),
        'to': end_date.strftime('%Y-%m-%d'),
        'language': 'en',
        'sortBy': 'publishedAt',
        'apiKey': api_key
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        news_data = response.json()
        return news_data['articles']
    except requests.RequestException as e:
        print(f"Error fetching news: {e}")
        return None

def analyze_sentiment(text):
    """
    Perform sentiment analysis on the given text.
    
    :param text: Text to analyze
    :return: Sentiment polarity (-1 to 1)
    """
    blob = TextBlob(text)
    return blob.sentiment.polarity

def summarize_sentiment(articles):
    """
    Summarize sentiment for a list of news articles.
    
    :param articles: List of news articles
    :return: DataFrame with sentiment summary
    """
    data = []
    for article in articles:
        if article['title'] is None or article['description'] is None:
            continue
        else:
            sentiment = analyze_sentiment(str(article['title']) + " " + str(article['description']))
            data.append({
                'date': article['publishedAt'],
                'title': article['title'],
                'sentiment': sentiment,
                'sentiment_category': 'Positive' if sentiment > 0 else 'Negative' if sentiment < 0 else 'Neutral'
            })
    
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date', ascending=False)
    
    summary = {
        'average_sentiment': df['sentiment'].mean(),
        'positive_articles': (df['sentiment'] > 0).sum(),
        'negative_articles': (df['sentiment'] < 0).sum(),
        'neutral_articles': (df['sentiment'] == 0).sum(),
        'total_articles': len(df)
    }
    
    return df, summary

# if __name__ == "__main__":
#     # Replace with your actual NewsAPI key
#     NEWS_API_KEY = "YOUR_NEWS_API_KEY_HERE"
#     ticker = "AAPL"
    
#     articles = get_news(NEWS_API_KEY, ticker)
    
#     if articles:
#         df, summary = summarize_sentiment(articles)
        
#         print(f"News Sentiment Summary for {ticker}:")
#         print(f"Average Sentiment: {summary['average_sentiment']:.2f}")
#         print(f"Positive Articles: {summary['positive_articles']}")
#         print(f"Negative Articles: {summary['negative_articles']}")
#         print(f"Neutral Articles: {summary['neutral_articles']}")
#         print(f"Total Articles: {summary['total_articles']}")
        
#         print("\nRecent Articles and Sentiment:")
#         print(df[['date', 'title', 'sentiment_category']].head())
#     else:
#         print("No news articles found.")