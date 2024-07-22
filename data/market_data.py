import yfinance as yf
import pandas as pd

def fetch_market_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data
