from data_collection import get_stock_data
from datetime import datetime, timedelta

tickers = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]

end_date = datetime.now().strftime('%Y-%m-%d')
start_date = (datetime.now() - timedelta(days=500)).strftime('%Y-%m-%d')

for ticker in tickers:
    get_stock_data(ticker, start_date, end_date)

print("Stock data update completed.")