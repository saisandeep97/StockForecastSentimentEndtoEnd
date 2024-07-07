import pandas as pd
import numpy as np
from data_collection import get_stock_data, preprocess_stock_data
from feature_engineering import add_technical_indicators, create_lagged_features
from model_implementation import SARIMAXModel, LinearRegressionModel, LightGBMModel
from model_evaluation import compare_models
import pandas_market_calendars as mcal

def prepare_data_for_forecast(ticker, start_date, end_date):
    """
    Prepare data for forecasting.
    
    :param ticker: Stock symbol
    :param start_date: Start date for historical data
    :param end_date: End date for historical data
    :return: Prepared DataFrame
    """
    stock_data = get_stock_data(ticker, start_date, end_date)
    processed_data = preprocess_stock_data(stock_data)
    data_with_indicators = add_technical_indicators(processed_data)
    final_data = create_lagged_features(data_with_indicators)
    return final_data

def select_best_model(X, y):
    """
    Select the best model based on RMSE.
    
    :param X: Feature data
    :param y: Target data
    :return: Best model
    """
    models = {
        'SARIMAX': SARIMAXModel(),
        'Linear Regression': LinearRegressionModel(),
        'LightGBM': LightGBMModel()
    }
    results = compare_models(models, X, y)
    print("\nModel Comparison Results:")
    print(results)
    best_model_name = results['rmse'].idxmin()
    return models[best_model_name], results

def forecast_next_day(model, data, feature_columns):
    """
    Forecast the next day's opening price.
    
    :param model: Trained model
    :param data: Historical data
    :param feature_columns: List of feature column names
    :return: Forecasted opening price
    """
    last_data_point = data[feature_columns].iloc[-1:]
    forecast = model.predict(last_data_point)
 #   print(last_data_point.index)
    return forecast[0] if isinstance(forecast, np.ndarray) else forecast

def run_forecast_pipeline(ticker, start_date, end_date):
    """
    Run the complete forecasting pipeline.
    
    :param ticker: Stock symbol
    :param start_date: Start date for historical data
    :param end_date: End date for historical data
    :return: Forecasted opening price for the next day
    """
    

    # Prepare data
    data = prepare_data_for_forecast(ticker, start_date, end_date)
    
    # Define feature columns
    feature_columns = ['Open','Close' ,'High', 'Low', 'Volume', 'Returns', 'Volatility', 
                       'SMA_20', 'RSI', 'MACD', 'ATR', 'OBV', 
                       'Close_Lag_1', 'Volume_Lag_1', 'Returns_Lag_1']
    
    data = data.dropna()
    # Prepare features and target
    X = data[feature_columns]
    y = data['Close'].shift(-1) # Shift target column by 1 day to prevent lookahead bias
    
    
    # Select and train the best model
    best_model,results = select_best_model( X.iloc[:-1], y.iloc[:-1])
    best_model.fit(X.iloc[:-1], y.iloc[:-1])
    y_train_pred=best_model.predict(X.iloc[:-1])
    y_train = pd.DataFrame(y.iloc[:-1].values,index=pd.to_datetime(data['Date']).iloc[:-1].dt.date)

    # Make forecast
    forecast = forecast_next_day(best_model, data, feature_columns)
    last_date=pd.Timestamp(data['Date'].iloc[-1])
    nyse = mcal.get_calendar('NYSE')
    next_trading_day = nyse.valid_days(start_date=pd.to_datetime(last_date+pd.Timedelta(days=1)).strftime('%Y-%m-%d'), end_date=pd.to_datetime(last_date+pd.Timedelta(days=10)).strftime('%Y-%m-%d'))[0].strftime('%Y-%m-%d')
    return forecast,next_trading_day,best_model.__class__.__name__, results, y_train,y_train_pred

# if __name__ == "__main__":
#     from datetime import datetime
#     ticker = "AAPL"
#     start_date = "2018-01-01"
#     end_date = datetime.now().strftime("%Y-%m-%d")
    
#     forecast = run_forecast_pipeline(ticker, start_date, end_date)
#     print(f"Forecasted closing  price for {ticker} for the next trading day: ${forecast:.2f}")