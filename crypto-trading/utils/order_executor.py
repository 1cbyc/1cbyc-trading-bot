import ccxt
from config import API_KEY, SECRET_KEY, EXCHANGE

exchange = ccxt.binance({
    'apiKey': API_KEY,
    'secret': SECRET_KEY,
})

def place_market_order(symbol, side, amount):
    order = exchange.create_order(symbol, 'market', side, amount)
    return order
