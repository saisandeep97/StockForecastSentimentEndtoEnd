import pandas as pd
import numpy as np

def add_technical_indicators(df):
    """
    Add technical indicators to the dataframe.
    
    :param df: DataFrame containing stock data
    :return: DataFrame with additional technical indicators
    """
    # Ensure the dataframe is sorted by date
    df = df.sort_values('Date')
    
    # Simple Moving Average (SMA)
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    
    # Exponential Moving Average (EMA)
    df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
    
    # Relative Strength Index (RSI)
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # Moving Average Convergence Divergence (MACD)
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
    # Bollinger Bands
    df['BB_Middle'] = df['Close'].rolling(window=20).mean()
    df['BB_Upper'] = df['BB_Middle'] + 2 * df['Close'].rolling(window=20).std()
    df['BB_Lower'] = df['BB_Middle'] - 2 * df['Close'].rolling(window=20).std()
    
    # Average True Range (ATR)
    high_low = df['High'] - df['Low']
    high_close = np.abs(df['High'] - df['Close'].shift())
    low_close = np.abs(df['Low'] - df['Close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    df['ATR'] = true_range.rolling(14).mean()
    
    # On-Balance Volume (OBV)
    df['OBV'] = (np.sign(df['Close'].diff()) * df['Volume']).fillna(0).cumsum()
    
    return df

def create_lagged_features(df, lag_days=[1, 2, 3, 5]):
    """
    Create lagged features for the specified columns.
    
    :param df: DataFrame containing stock data
    :param lag_days: List of days to lag
    :return: DataFrame with additional lagged features
    """
    features_to_lag = ['Close', 'Volume', 'Returns']
    
    for feature in features_to_lag:
        for lag in lag_days:
            df[f'{feature}_Lag_{lag}'] = df[feature].shift(lag)
    
    return df

# if __name__ == "__main__":
#     # Example usage
#     from data_collection import get_stock_data, preprocess_stock_data
    
#     ticker = "AAPL"
#     start_date = "2022-01-01"
#     end_date = datetime.now().strftime('%Y-%m-%d')
    
#     # Fetch and preprocess stock data
#     stock_data = get_stock_data(ticker, start_date, end_date)
#     if stock_data is not None:
#         processed_data = preprocess_stock_data(stock_data)
        
#         # Add technical indicators
#         data_with_indicators = add_technical_indicators(processed_data)
        
#         # Create lagged features
#         final_data = create_lagged_features(data_with_indicators)
        
#         print(final_data.head())
#         print(f"Shape of final data: {final_data.shape}")
#         print(f"Columns in final data: {final_data.columns.tolist()}")