from data.market_data.py import fetch_market_data
from strategies.moving_average import moving_average_strategy
from trading.order_execution import create_api_connection, place_order

def main():
    #  collecting data from the market
    ticker = 'AAPL'
    start_date = "2022-01-01"
    end_date = "2022-12-31"
    data = fetch_market_data(ticker, start_date, end_date)

    # how i apply the trading strategy i want to use
    short_window = 20
    long_window = 50
    data = moving_average_strategy(data, short_window, long_window)

    # my alpaca api details (though i want to use an env"
    API_KEY = 'my_api_key'
    API_SECRET = 'my_api_secret'
    BASE_URL = 'https://paper-api.alpaca.markets'

    api = create_api_connection(API_KEY, API_SECRET, BASE_URL)

    # will execute trading logic here
    for i in range(len(data)):
        if data['Position'][i] == 1:  # buy trade signal
            place_order(api, ticker, 1, 'buy')
        elif data['Position'][i] == -1:  # sell trade signal
            place_order(api, ticker, 1, 'sell')

    print("trading bot has completed running.")

if __name__ == "__main__":
    main()
