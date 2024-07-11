import numpy as np
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.linear_model import LinearRegression, SGDRegressor
from sklearn.preprocessing import StandardScaler
import lightgbm as lgb
from sklearn import svm

class SARIMAXModel:
    def __init__(self, order=(1,1,1), seasonal_order=(1,1,1,12)):
        self.order = order
        self.seasonal_order = seasonal_order
        self.model = None

    def fit(self, X, y=None):
        self.model = SARIMAX(X['Close'], 
                             order=self.order, 
                             seasonal_order=self.seasonal_order)
        self.results = self.model.fit(disp=False)

    def predict(self,X_test):
        steps = len(X_test)
        return self.results.forecast(steps=steps).values

class LinearRegressionModel:
    def __init__(self):
        self.model = LinearRegression()
        self.scaler = StandardScaler()

    def fit(self, X, y):
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)

    def predict(self, X):
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)

class SVMModel:
    def __init__(self):
        self.model = svm.SVR()
        self.scaler = StandardScaler()

    def fit(self, X, y):
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)

    def predict(self, X):
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)
    

class SGDModel:
    def __init__(self):
        self.model = SGDRegressor()
        self.scaler = StandardScaler()

    def fit(self, X, y):
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)

    def predict(self, X):
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)

# class LightGBMModel:
#     def __init__(self, params=None):
#         self.params = params or {
#             'objective': 'regression',
#             'metric': 'mse',
#             # 'num_leaves': 31,
#             # 'learning_rate': 0.05,
#             # 'feature_fraction': 0.9,
#             'vebose': -1
#         }
#         self.model = None

#     def fit(self, X, y):
#         train_data = lgb.Dataset(X, label=y)
#         self.model = lgb.train(self.params, train_data, num_boost_round=100)

#     def predict(self, X):
#         return self.model.predict(X)

def prepare_data_for_models(data, feature_columns, target_column='Close', test_size=0.2):
    """
    Prepare data for model training and testing.
    
    :param data: DataFrame containing stock data and features
    :param feature_columns: List of column names to use as features
    :param target_column: Name of the target column
    :param test_size: Proportion of data to use for testing
    :return: X_train, X_test, y_train, y_test
    """
    # Remove any rows with NaN values
    data = data.dropna()


    # Prepare features and target
    X = data[feature_columns]
    y = data[target_column].shift(-1) # Shift target column by 1 day to prevent lookahead bias

    # Split data into training and testing sets
    split_index = int(len(data) * (1 - test_size))
    X_train, X_test = X[:split_index], X[split_index:]
    y_train, y_test = y[:split_index], y[split_index:]

    return X_train, X_test, y_train, y_test

# if __name__ == "__main__":
#     from data_collection import get_stock_data, preprocess_stock_data
#     from feature_engineering import add_technical_indicators, create_lagged_features
#     from datetime import datetime


#     # Fetch and prepare data
#     ticker = "AAPL"
#     start_date = "2020-01-01"
#     end_date = datetime.now().strftime('%Y-%m-%d')

#     stock_data = get_stock_data(ticker, start_date, end_date)
#     processed_data = preprocess_stock_data(stock_data)
#     data_with_indicators = add_technical_indicators(processed_data)
#     final_data = create_lagged_features(data_with_indicators)

#     # Prepare data for models
#     feature_columns = ['Open','Close', 'High', 'Low', 'Volume', 'Returns', 'Volatility', 
#                        'SMA_20', 'RSI', 'MACD', 'ATR', 'OBV', 
#                        'Close_Lag_1', 'Volume_Lag_1', 'Returns_Lag_1']
#     X_train, X_test, y_train, y_test = prepare_data_for_models(final_data, feature_columns)

#     # Example usage of models

#     sarimax_model = SARIMAXModel()
#     sarimax_model.fit(final_data)
#     sarimax_prediction = sarimax_model.predict()
#     print(f"SARIMAX Prediction: {sarimax_prediction}")

#     lr_model = LinearRegressionModel()
#     lr_model.fit(X_train, y_train)
#     lr_prediction = lr_model.predict(X_test[:1])
#     print(f"Linear Regression Prediction: {lr_prediction}")

#     lgb_model = LightGBMModel()
#     lgb_model.fit(X_train, y_train)
#     lgb_prediction = lgb_model.predict(X_test[:1])
#     print(f"LightGBM Prediction: {lgb_prediction}")