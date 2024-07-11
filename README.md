
# MarketPulse: Stock Forecasting & Sentiment Analysis

## Live Demonstration
https://stockforecastsentimentendtoend.streamlit.app/

## Project Overview

This project is an end-to-end solution for stock price forecasting and news sentiment analysis. It includes data collection, preprocessing, feature engineering, model implementation, forecasting, news sentiment analysis, and a web-based dashboard. The system is designed to update daily and is deployed using Streamlit.

## Features

- Historical stock data collection and storage
- Technical indicator calculation
- Multiple forecasting models (Moving Average, SARIMAX, Linear Regression, LightGBM)
- News data collection and sentiment analysis
- Interactive web dashboard
- Automated daily updates and deployment

## Project Structure

```
stock-forecast-dashboard/
│
├── data_collection.py
├── feature_engineering.py
├── model_implementation.py
├── model_evaluation.py
├── forecasting.py
├── news_sentiment.py
├── dashboard.py
├── requirements.txt
├── .github/
│   └── workflows/
│       └── update_data.yml
├── stock_data/
├── news_data/
├── update_news_data.py
├── update_stock_data.py
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/saisandeep97/StockForecastSentimentEndtoEnd.git
   cd stock-forecast-dashboard
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - `NEWS_API_KEY`: Your NewsAPI key

## Usage

1. Data Collection:
   ```
   python data_collection.py
   ```

2. Feature Engineering:
   ```
   python feature_engineering.py
   ```

3. Model Implementation and Evaluation:
   ```
   python model_implementation.py
   python model_evaluation.py
   ```

4. Forecasting:
   ```
   python forecasting.py
   ```

5. News Sentiment Analysis:
   ```
   python news_sentiment.py
   ```

6. Run the Dashboard:
   ```
   streamlit run dashboard.py
   ```

## Hosting with Streamlit

This project is hosted using Streamlit Cloud for easy sharing and collaboration:

1. Push your project to a GitHub repository.
2. Sign up for a [Streamlit Cloud](https://streamlit.io/cloud) account.
3. Connect your GitHub account to Streamlit Cloud.
4. Deploy your app by selecting the repository and the `dashboard.py` file.
5. Set the required secrets in the Streamlit Cloud dashboard:
   - `NEWS_API_KEY`

Streamlit Cloud will automatically deploy your app and provide a public URL. The app will update whenever you push changes to your GitHub repository.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgements

- [yfinance](https://github.com/ranaroussi/yfinance) for stock data
- [NewsAPI](https://newsapi.org/) for news data
- [Streamlit](https://streamlit.io/) for the web dashboard
- [scikit-learn](https://scikit-learn.org/) for machine learning models
- [pandas](https://pandas.pydata.org/) for data manipulation
- [TextBlob](https://textblob.readthedocs.io/) for sentiment analysis

## Optional
You can set up github actions to fetch and update the stock and news data on daily basis so that the workload on streamlit server could be reduced. 