import os
from news_sentiment import get_news
from datetime import datetime, timedelta

NEWS_API_KEY = os.getenv('NEWS_API_KEY')
tickers = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]
days = 7  # Number of days of news to fetch

for ticker in tickers:
    get_news(NEWS_API_KEY, ticker, days)

print("News data update completed.")