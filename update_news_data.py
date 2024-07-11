import os
from news_sentiment import get_news

NEWS_API_KEY = '3c9f7f7ea9504ff084b5aad55895839d'
tickers = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]
days = 7  # Number of days of news to fetch

for ticker in tickers:
    get_news(NEWS_API_KEY, ticker, days)

print("News data update completed.")