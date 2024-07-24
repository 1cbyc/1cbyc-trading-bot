import numpy as np
import pandas as pd

def moving_average_strategy(data, short_window, long_window):
    data['SMA_Short'] = data['Close'].rolling(window=short_window).mean()
    data['SMA_Long'] = data['Close'].rolling(window=long_window).mean()

    # generated signals
    data['Signal'] = 0
    data['Signal'][short_window:] = np.where(data['SMA_Short'][short_window:] > data['SMA_Long'][short_window:], 1, 0)

    # generate trading orders
    data['Position'] = data['Signal'].diff()

    return data
