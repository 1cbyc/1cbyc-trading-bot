from data.market_data import fetch_market_data
from strategies.moving_average import moving_average_strategy
from trading.order_execution import create_api_connection, place_order
from dotenv import load_dotenv
import os
import time

def main():
    load_dotenv()

    # these are the list of tickers to trade
    # the tickers is for stocks
    tickers = ['AAPL', 'GOOGL', 'MSFT']
    # tickers = ['BTCUSD', 'ETHUSD', 'XRPUSD']

    # definitely common parameters
    start_date = "2024-01-01"
    end_date = "2024-07-31"
    short_window = 20
    long_window = 50

    # retrieve the api details from environment variables
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    BASE_URL = os.getenv('BASE_URL')

    api = create_api_connection(API_KEY, API_SECRET, BASE_URL)

    # looping through each ticker
    for ticker in tickers:
        # collect data from the market again
        data = fetch_market_data(ticker, start_date, end_date)

        # apply the trading strategy this time
        data = moving_average_strategy(data, short_window, long_window)

        # properly execute trading logic
        # for i in range(len(data)):
        #     if data['Position'][i] == 1:  # buy trade signal
        #         place_order(api, ticker, 1, 'buy')
        #     elif data['Position'][i] == -1:  # sell trade signal
        #         place_order(api, ticker, 1, 'sell')
        #
        # decided to use iloc instead
        for i in range(len(data)):
            if data['Position'].iloc[i] == 1:  # buy trade signal
                place_order(api, ticker, 1, 'buy')
            elif data['Position'].iloc[i] == -1:  # sell trade signal
                place_order(api, ticker, 1, 'sell')

    print("Trading bot has completed running.")

if __name__ == "__main__":
    main()
