import yfinance as yf
import plotly.express as px

def fetch_stock_data(ticker):
    # Fetch data from Yahoo Finance
    data = yf.download(ticker)
    return data

def create_candlestick_chart(data, title):
    fig = px.candlestick(data, x=data.index,
                        y=["Open", "High", "Low", "Close"])
    fig.update_layout(title=title)
    return fig