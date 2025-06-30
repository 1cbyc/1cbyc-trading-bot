import pandas as pd
import numpy as np
from typing import Dict, Tuple

class SyntheticTradingStrategy:
    """Base class for synthetic indices trading strategies (MT5 version)"""
    def __init__(self, symbol: str, timeframe: str = 'M5'):
        self.symbol = symbol
        self.timeframe = timeframe
        self.data = pd.DataFrame()

    def update_data(self, df: pd.DataFrame):
        self.data = df.copy()
        if len(self.data) > 1000:
            self.data = self.data.tail(1000)

    def get_signal(self) -> Tuple[str, float]:
        raise NotImplementedError("Subclasses must implement get_signal()")

class MovingAverageCrossover(SyntheticTradingStrategy):
    def __init__(self, symbol: str, timeframe: str = 'M5', short_window: int = 10, long_window: int = 20):
        super().__init__(symbol, timeframe)
        self.short_window = short_window
        self.long_window = long_window

    def get_signal(self) -> Tuple[str, float]:
        if len(self.data) < self.long_window:
            return "HOLD", 0.0
        short_ma = self.data['close'].rolling(window=self.short_window).mean()
        long_ma = self.data['close'].rolling(window=self.long_window).mean()
        current_short = short_ma.iloc[-1]
        current_long = long_ma.iloc[-1]
        prev_short = short_ma.iloc[-2] if len(short_ma) > 1 else current_short
        prev_long = long_ma.iloc[-2] if len(long_ma) > 1 else current_long
        if current_short > current_long and prev_short <= prev_long:
            return "BUY", 0.8
        elif current_short < current_long and prev_short >= prev_long:
            return "SELL", 0.8
        elif current_short > current_long:
            return "BUY", 0.6
        else:
            return "SELL", 0.6

class RSIStrategy(SyntheticTradingStrategy):
    def __init__(self, symbol: str, timeframe: str = 'M5', period: int = 14, oversold: int = 30, overbought: int = 70):
        super().__init__(symbol, timeframe)
        self.period = period
        self.oversold = oversold
        self.overbought = overbought

    def calculate_rsi(self) -> float:
        if len(self.data) < self.period + 1:
            return 50.0
        delta = self.data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.iloc[-1]

    def get_signal(self) -> Tuple[str, float]:
        if len(self.data) < self.period + 1:
            return "HOLD", 0.0
        rsi = self.calculate_rsi()
        if rsi < self.oversold:
            return "BUY", 0.9
        elif rsi > self.overbought:
            return "SELL", 0.9
        elif rsi < 50:
            return "BUY", 0.6
        else:
            return "SELL", 0.6

class BollingerBandsStrategy(SyntheticTradingStrategy):
    def __init__(self, symbol: str, timeframe: str = 'M5', period: int = 20, std_dev: float = 2.0):
        super().__init__(symbol, timeframe)
        self.period = period
        self.std_dev = std_dev

    def get_signal(self) -> Tuple[str, float]:
        if len(self.data) < self.period:
            return "HOLD", 0.0
        sma = self.data['close'].rolling(window=self.period).mean()
        std = self.data['close'].rolling(window=self.period).std()
        upper_band = sma + (std * self.std_dev)
        lower_band = sma - (std * self.std_dev)
        current_price = self.data['close'].iloc[-1]
        current_upper = upper_band.iloc[-1]
        current_lower = lower_band.iloc[-1]
        if current_price <= current_lower:
            return "BUY", 0.8
        elif current_price >= current_upper:
            return "SELL", 0.8
        else:
            return "HOLD", 0.0

class VolatilityBreakoutStrategy(SyntheticTradingStrategy):
    def __init__(self, symbol: str, timeframe: str = 'M5', period: int = 20, multiplier: float = 1.5):
        super().__init__(symbol, timeframe)
        self.period = period
        self.multiplier = multiplier

    def get_signal(self) -> Tuple[str, float]:
        if len(self.data) < self.period:
            return "HOLD", 0.0
        high_low = self.data['high'] - self.data['low']
        high_close = np.abs(self.data['high'] - self.data['close'].shift())
        low_close = np.abs(self.data['low'] - self.data['close'].shift())
        true_range = np.maximum(high_low, np.maximum(high_close, low_close))
        atr = true_range.rolling(window=self.period).mean()
        current_atr = atr.iloc[-1]
        avg_atr = atr.mean()
        if current_atr > (avg_atr * self.multiplier):
            price_change = self.data['close'].iloc[-1] - self.data['close'].iloc[-2]
            if price_change > 0:
                return "BUY", 0.7
            else:
                return "SELL", 0.7
        else:
            return "HOLD", 0.0

class MACDStrategy(SyntheticTradingStrategy):
    def __init__(self, symbol: str, timeframe: str = 'M5', fast_period: int = 12, slow_period: int = 26, signal_period: int = 9):
        super().__init__(symbol, timeframe)
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period

    def calculate_macd(self):
        if len(self.data) < self.slow_period:
            return 0.0, 0.0, 0.0
        ema_fast = self.data['close'].ewm(span=self.fast_period).mean()
        ema_slow = self.data['close'].ewm(span=self.slow_period).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=self.signal_period).mean()
        hist = macd_line - signal_line
        return macd_line.iloc[-1], signal_line.iloc[-1], hist.iloc[-1]

    def get_signal(self) -> Tuple[str, float]:
        if len(self.data) < self.slow_period:
            return "HOLD", 0.0
        macd, signal, hist = self.calculate_macd()
        prev_macd, prev_signal, _ = self.calculate_macd() if len(self.data) > self.slow_period else (macd, signal, hist)
        if macd > signal and prev_macd <= prev_signal:
            return "BUY", 0.7
        elif macd < signal and prev_macd >= prev_signal:
            return "SELL", 0.7
        else:
            return "HOLD", 0.0 