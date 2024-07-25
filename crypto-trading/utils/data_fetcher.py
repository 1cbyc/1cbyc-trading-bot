import ccxt
import pandas as pd
from config import API_KEY, SECRET_KEY, EXCHANGE

exchange = ccxt.binance({
    'apiKey': API_KEY,
    'secret': SECRET_KEY,
})

def fetch_ohlcv(symbol, timeframe, limit=100):
    data = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df

def fetch_latest_price(symbol):
    ticker = exchange.fetch_ticker(symbol)
    return ticker['last']
