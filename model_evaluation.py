import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from model_implementation import SARIMAXModel, LinearRegressionModel, LightGBMModel
from data_collection import get_stock_data, preprocess_stock_data
from feature_engineering import add_technical_indicators, create_lagged_features


def evaluate_model(model, X, y, cv=5):
    """
    Evaluate a model using time series cross-validation.
    
    :param model: The model to evaluate
    :param X: Feature data
    :param y: Target data
    :param cv: Number of splits for cross-validation
    :return: Dictionary of evaluation metrics
    """
    tscv = TimeSeriesSplit(n_splits=cv)
    mse_scores = []
    mae_scores = []
    r2_scores = []

    for train_index, test_index in tscv.split(X):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]

        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        mse_scores.append(mean_squared_error(y_test, predictions))
        mae_scores.append(mean_absolute_error(y_test, predictions))
        r2_scores.append(r2_score(y_test, predictions))

    return {
        'mse': np.mean(mse_scores),
        'mae': np.mean(mae_scores),
        'r2': np.mean(r2_scores),
        'rmse': np.sqrt(np.mean(mse_scores))
    }

def compare_models(models, X, y):
    """
    Compare multiple models using the same evaluation process.
    
    :param models: Dictionary of models to compare
    :param X: Feature data
    :param y: Target data
    :return: DataFrame with evaluation results for each model
    """
    results = []
    for name, model in models.items():
        print(f"Evaluating {name}...")
        metrics = evaluate_model(model, X, y)
        metrics['model'] = name
        results.append(metrics)
    
    return pd.DataFrame(results).set_index('model')


# if __name__ == "__main__":
#     from datetime import datetime
#     # Fetch and prepare data
#     ticker = "AAPL"
#     start_date = "2018-01-01"
#     end_date = datetime.now().strftime("%Y-%m-%d")

#     stock_data = get_stock_data(ticker, start_date, end_date)
#     processed_data = preprocess_stock_data(stock_data)
#     data_with_indicators = add_technical_indicators(processed_data)
#     final_data = create_lagged_features(data_with_indicators)

#     # Prepare data for models
#     feature_columns = ['Open','Close', 'High', 'Low', 'Volume', 'Returns', 'Volatility', 
#                     'SMA_20', 'RSI', 'MACD', 'ATR', 'OBV', 
#                     'Close_Lag_1', 'Volume_Lag_1', 'Returns_Lag_1']
   
    
#     # Remove any rows with NaN values
#     data = final_data.dropna()


#     # Prepare features and target
#     X = data[feature_columns]
#     y = data['Close'].shift(-1) # Shift target column by 1 day to prevent lookahead bias
 
#     # Consider all rows except the last one for X and y as last value for y is NaN
#     X = X.iloc[:-1]
#     y = y.iloc[:-1]

#     # Define models to compare
#     models = {
#         'SARIMAX': SARIMAXModel(),
#         'Linear Regression': LinearRegressionModel(),
#         'LightGBM': LightGBMModel()
#     }

#     # Compare models
#     results = compare_models(models, X, y)
#     print("\nModel Comparison Results:")
#     print(results)

#     # Find the best model based on RMSE
#     best_model = results['rmse'].idxmin()
#     print(f"\nBest model based on RMSE: {best_model}")