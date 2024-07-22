import alpaca_trade_api as tradeapi

def create_api_connection(api_key, api_secret, base_url):
    api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')
    return api

def place_order(api, ticker, qty, side, order_type='market', time_in_force='gtc'):
    api.submit_order(
        symbol=ticker,
        qty=qty,
        side=side,
        type=order_type,
        time_in_force=time_in_force
    )
