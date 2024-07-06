import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from forecasting import run_forecast_pipeline
from news_sentiment import get_news, summarize_sentiment

# Replace with your actual NewsAPI key
NEWS_API_KEY = "3c9f7f7ea9504ff084b5aad55895839d"

def plot_stock_data(data):
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=data['Date'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='Stock Data'))
    fig.update_layout(title='Stock Price', xaxis_title='Date', yaxis_title='Price')
    return fig

def run_dashboard():
    st.title("Stock Forecast and News Sentiment Dashboard")

    # Sidebar for user input
    st.sidebar.header("User Input")
    #ticker = st.sidebar.text_input("Enter Stock Ticker", value="AAPL")
    ticker = st.sidebar.selectbox("Select Stock Ticker", ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"])
    days = st.sidebar.slider("Select number of days for historical data", 30, 365, 180)

    # Calculate date range
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

    # Run forecast pipeline
    with st.spinner('Fetching data and generating forecast...'):
        forecast,next_trading_day,model_name = run_forecast_pipeline(ticker, start_date, end_date)

    forecast = forecast.values[0] if type(forecast) == pd.Series else forecast
    # Display forecast
    st.header(f"Stock Forecast for {ticker} by best model {model_name}")
    st.write(f"Forecasted closing price for the next trading day {next_trading_day}: ${forecast:.2f}")

    # Fetch historical data
    from data_collection import get_stock_data, preprocess_stock_data
    stock_data = get_stock_data(ticker, start_date, end_date)
    processed_data = preprocess_stock_data(stock_data)

    # Plot historical data
    st.subheader("Historical Stock Data")
    st.plotly_chart(plot_stock_data(processed_data))

    # Fetch and display news sentiment
    st.header("News Sentiment Analysis")
    with st.spinner('Fetching and analyzing news...'):
        articles = get_news(NEWS_API_KEY, ticker)
        if articles:
            df, summary = summarize_sentiment(articles)
            
            st.subheader("Sentiment Summary")
            col1, col2, col3 = st.columns(3)
            col1.metric("Average Sentiment", f"{summary['average_sentiment']:.2f}")
            col2.metric("Positive Articles", summary['positive_articles'])
            col3.metric("Negative Articles", summary['negative_articles'])
            
            st.subheader("Recent Articles")
            for _, row in df.head().iterrows():
                st.write(f"**{row['title']}**")
                st.write(f"Date: {row['date']}, Sentiment: {row['sentiment_category']}")
                st.write("---")
        else:
            st.write("No news articles found.")

if __name__ == "__main__":
    run_dashboard()