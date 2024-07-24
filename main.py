from data.market_data import fetch_market_data
from strategies.moving_average import moving_average_strategy
from trading.order_execution import create_api_connection, place_order
from dotenv import load_dotenv
import os
import time

def main():
    load_dotenv()

    # tickers = ['AAPL', 'GOOGL', 'MSFT']
    # let me trade chips like NVIDIA only for now:
    # tickers = ['NVDA', 'AMD', 'INTC', 'QCOM', 'AVGO', 'TXN', 'MU', 'AMAT', 'LRCX', 'ASML']
    # trade for AI
    tickers = ['GOOGL', 'MSFT', 'NVDA', 'IBM', 'AMZN', 'META', 'BIDU', 'CRM', 'ADBE', 'TSLA']
    # trade for real estate:
    # tickers = ['AMT', 'PLD', 'CCI', 'SPG', 'EQIX', 'PSA', 'DLR', 'AVB', 'EQR', 'O']

    start_date = "2024-01-01"
    end_date = "2024-12-31"
    short_window = 20
    long_window = 50

    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    BASE_URL = os.getenv('BASE_URL')

    api = create_api_connection(API_KEY, API_SECRET, BASE_URL)

    # loop through each ticker
    for ticker in tickers:
        # collect data from the market
        data = fetch_market_data(ticker, start_date, end_date)

        # applying the trading strategy
        data = moving_average_strategy(data, short_window, long_window)

        last_action = None
        for i in range(len(data)):
            if data['Position'].iloc[i] == 1 and last_action != 'buy':  # buy trade signal
                place_order(api, ticker, 1, 'buy')
                last_action = 'buy'
                time.sleep(1)  # ah no wan wash trades
            # elif data['Position'].iloc[i] == -1 and last_action != 'sell':  # sell trade signal
            #     place_order(api, ticker, 1, 'sell')
            #     last_action = 'sell'
            #     time.sleep(1)  # i set this delay to prevent wash trades

    print("Trading bot has completed running.")
    # i want to loop it to trade every 1 minute
    # print("opened first batch of trades. will open another next 1 minute...")
    # time.sleep(60)

if __name__ == "__main__":
    main()