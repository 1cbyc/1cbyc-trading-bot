import time
import pandas as pd
from utils.data_fetcher import fetch_ohlcv, fetch_latest_price
from utils.order_executor import place_market_order
from strategies.moving_average import generate_signals
from config import SYMBOL, TIMEFRAME, SHORT_WINDOW, LONG_WINDOW, TRADE_AMOUNT

def run_bot():
    while True:
        try:
            df = fetch_ohlcv(SYMBOL, TIMEFRAME)
            signals = generate_signals(df, SHORT_WINDOW, LONG_WINDOW)
            latest_signal = signals['positions'].iloc[-1]
            latest_price = fetch_latest_price(SYMBOL)

            if latest_signal == 1.0:
                print(f"Buying {SYMBOL} at {latest_price}")
                place_market_order(SYMBOL, 'buy', TRADE_AMOUNT)
            elif latest_signal == -1.0:
                print(f"Selling {SYMBOL} at {latest_price}")
                place_market_order(SYMBOL, 'sell', TRADE_AMOUNT)

            time.sleep(3600)  # to allow trade run every hour
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)  # this would allow it wait before retrying

if __name__ == "__main__":
    run_bot()
