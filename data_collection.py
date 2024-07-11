import yfinance as yf
import pandas as pd
from newsapi import NewsApiClient
from datetime import datetime, timedelta
import os

DATA_DIR = "stock_data"

def get_stock_data(ticker, start_date, end_date):
    """
    Fetch historical stock data using yfinance API or load from CSV if available.
    
    :param ticker: Stock symbol (e.g., "AAPL" for Apple Inc.)
    :param start_date: Start date for historical data (format: "YYYY-MM-DD")
    :param end_date: End date for historical data (format: "YYYY-MM-DD")
    :return: DataFrame containing historical stock data
    """
    # Create data directory if it doesn't exist
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    # Construct file path
    file_path = os.path.join(DATA_DIR, f"{ticker}.csv")
    
    # Check if we have recent data stored
    if os.path.exists(file_path):
        stored_data = pd.read_csv(file_path, parse_dates=['Date'])
        last_stored_date = stored_data['Date'].max()
        
        # If stored data is up to date, return it
        if last_stored_date.strftime('%Y-%m-%d') == end_date:
            print(f"Loading data for {ticker} from CSV file.")
            return stored_data[(pd.to_datetime(stored_data['Date'],utc=True) >= start_date) & (pd.to_datetime(stored_data['Date'],utc=True) <= end_date)]
        
        # If stored data is outdated, update it
        print(f"Updating data for {ticker}.")
        new_start_date = (last_stored_date + timedelta(days=1)).strftime('%Y-%m-%d')
        new_data = fetch_stock_data(ticker, new_start_date, end_date)
        
        if new_data is not None and not new_data.empty:
            updated_data = pd.concat([stored_data, new_data]).drop_duplicates().reset_index(drop=True)
            updated_data.to_csv(file_path, index=False)
            return updated_data[(pd.to_datetime(updated_data['Date'],utc=True) >= start_date) & (pd.to_datetime(updated_data['Date'],utc=True) <= end_date)]
        else:
            print(f"No new data available for {ticker}. Using stored data.")
            return stored_data[(pd.to_datetime(stored_data['Date'],utc=True) >= start_date) & (pd.to_datetime(stored_data['Date'],utc=True) <= end_date)]
    
    # If no stored data, fetch all data
    print(f"Fetching all data for {ticker}.")
    data = fetch_stock_data(ticker, start_date, end_date)
    
    if data is not None and not data.empty:
        data.to_csv(file_path, index=False)
    
    return data

def fetch_stock_data(ticker, start_date, end_date):
    """
    Fetch stock data from yfinance API.
    """
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(start=start_date, end=end_date)
        
        if data.empty:
            print(f"No data available for {ticker} between {start_date} and {end_date}")
            return None
        
        # Reset index to make Date a column
        data.reset_index(inplace=True)
        
        # Ensure all expected columns are present
        expected_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        for col in expected_columns:
            if col not in data.columns:
                print(f"Warning: {col} column is missing from the data")
                data[col] = None
        
        return data
    
    except Exception as e:
        print(f"Error fetching data for {ticker}: {str(e)}")
        return None

def preprocess_stock_data(data):
    """
    Preprocess the stock data.
    
    :param data: DataFrame containing stock data
    :return: Preprocessed DataFrame
    """
    if data is None:
        return None
    
    # Convert Date column to datetime
    data['Date'] = pd.to_datetime(data['Date'],utc=True)
    
    # Sort data by date
    data.sort_values('Date', inplace=True)
    
    # Handle missing values
    data.fillna(method='ffill', inplace=True)  # Forward fill
    data.fillna(method='bfill', inplace=True)  # Backward fill
    
    # Calculate daily returns
    data['Returns'] = data['Close'].pct_change()
    
    # Calculate volatility (20-day rolling standard deviation of returns)
    data['Volatility'] = data['Returns'].rolling(window=20).std()
    
    data.to_csv("stock_data/preprocessed.csv", index=False)
    return data

# if __name__ == "__main__":
#     # Example usage
#     ticker = "AAPL"
#     start_date = "2022-01-01"
#     end_date =  datetime.now().strftime('%Y-%m-%d')
#     newsapi_key = "3c9f7f7ea9504ff084b5aad55895839d"
    
#     # Fetch stock data
#     stock_data = get_stock_data(ticker, start_date, end_date)
#     if stock_data is not None:
#         processed_data = preprocess_stock_data(stock_data)
#         print(processed_data.head())
#         print(f"Shape of processed data: {processed_data.shape}")
    
#     # Fetch news data
#     news_data = get_news_data(newsapi_key, ticker)
#     if news_data is not None:
#         print(f"Number of news articles fetched: {len(news_data)}")
#         print("First article title:", news_data[0]['title'])