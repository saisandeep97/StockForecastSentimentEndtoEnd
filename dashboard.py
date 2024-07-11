import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from forecasting import run_forecast_pipeline
from news_sentiment import get_news, summarize_sentiment

# Replace with your actual NewsAPI key
NEWS_API_KEY = st.secrets["NEWS_API_KEY"]

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

def plot_actual_vs_predicted(y_train, y_train_pred):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=y_train.index, y=y_train[0].to_list(), mode='lines', name='Actual', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=y_train.index, y=y_train_pred, mode='lines', name='Predicted', line=dict(color='red')))
    fig.update_layout(xaxis_title='Date', yaxis_title='Closing Price')
    return fig

def run_dashboard():
    st.title("MarketPulse: Stock Forecasting & Sentiment Analysis")

    # Sidebar for user input
    st.sidebar.header("User Input")
    #ticker = st.sidebar.text_input("Enter Stock Ticker", value="AAPL")
    ticker = st.sidebar.selectbox("Select Stock Ticker", ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"])
    days = st.sidebar.slider("Select number of days for historical data training", 60, 500, 500)

    # Calculate date range
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

    # Run forecast pipeline
    with st.spinner('Fetching data and generating forecast...'):
        forecast,next_trading_day,model_name,results,y_train,y_train_pred = run_forecast_pipeline(ticker, start_date, end_date)

    st.header(f"Model Evaluation Results for {ticker}")
    st.write(f"Evaluation results on test dataset after performing 3 fold time series cross validation")

    st.dataframe(results)
    forecast = forecast.values[0] if type(forecast) == pd.Series else forecast
    y_train_pred = y_train_pred.values if type(y_train_pred) == pd.Series else y_train_pred
    # Display forecast
    st.header(f"Forecasted closing price for {next_trading_day}: ${forecast:.2f}")
    st.header(f"For {ticker} by {model_name}")

    # Load preprocessed data
    processed_data = pd.read_csv("stock_data/preprocessed.csv")

    # Plot historical data
    st.subheader("Historical Stock Data")
    st.plotly_chart(plot_stock_data(processed_data))

    # Plot historical predictions
    st.subheader("Historical Actual vs. Predicted Closing Price for best model")
    st.plotly_chart(plot_actual_vs_predicted(y_train, y_train_pred))

    # Fetch and display news sentiment
    st.header("News Sentiment Analysis")
    with st.spinner('Fetching and analyzing news...'):
        articles = get_news(NEWS_API_KEY, ticker)
        if articles:
            df, summary = summarize_sentiment(articles)
            
            st.subheader("Sentiment Summary for past week")
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