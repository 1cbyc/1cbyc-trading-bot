# # config.py
#
# API_KEY = 'my_api_key'
# SECRET_KEY = 'my_secret_key'
#
# EXCHANGE = 'binance'  # or any other exchange supported by ccxt
# SYMBOL = 'BTC/USDT'
# TIMEFRAME = '1h'
# SHORT_WINDOW = 40
# LONG_WINDOW = 100
# TRADE_AMOUNT = 0.001  # depends on my requirements

import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
EXCHANGE = os.getenv('EXCHANGE')
SYMBOL = os.getenv('SYMBOL')
TIMEFRAME = os.getenv('TIMEFRAME')
SHORT_WINDOW = int(os.getenv('SHORT_WINDOW'))
LONG_WINDOW = int(os.getenv('LONG_WINDOW'))
TRADE_AMOUNT = float(os.getenv('TRADE_AMOUNT'))
