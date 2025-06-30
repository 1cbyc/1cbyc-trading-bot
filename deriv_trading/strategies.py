import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from .config import DerivConfig

class SyntheticTradingStrategy:
    """Base class for synthetic indices trading strategies"""
    
    def __init__(self, symbol: str, timeframe: str = '5m'):
        self.symbol = symbol
        self.timeframe = timeframe
        self.granularity = DerivConfig.TIMEFRAMES.get(timeframe, 300)
        self.data = pd.DataFrame()
        
    def add_candle(self, candle: Dict):
        """Add a new candle to the data"""
        new_row = pd.DataFrame([{
            'timestamp': candle.get('epoch', 0),
            'open': float(candle.get('open', 0)),
            'high': float(candle.get('high', 0)),
            'low': float(candle.get('low', 0)),
            'close': float(candle.get('close', 0)),
            'volume': float(candle.get('volume', 0))
        }])
        
        self.data = pd.concat([self.data, new_row], ignore_index=True)
        
        # Keep only last 1000 candles to prevent memory issues
        if len(self.data) > 1000:
            self.data = self.data.tail(1000)
    
    def get_signal(self) -> Tuple[str, float]:
        """Get trading signal - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement get_signal()")
    
    def reset(self):
        """Reset strategy data"""
        self.data = pd.DataFrame()

class MovingAverageCrossover(SyntheticTradingStrategy):
    """Moving Average Crossover Strategy for Synthetic Indices"""
    
    def __init__(self, symbol: str, timeframe: str = '5m', short_window: int = 10, long_window: int = 20):
        super().__init__(symbol, timeframe)
        self.short_window = short_window
        self.long_window = long_window
        
    def get_signal(self) -> Tuple[str, float]:
        """Get trading signal based on MA crossover"""
        if len(self.data) < self.long_window:
            return "HOLD", 0.0
        
        # Calculate moving averages
        short_ma = self.data['close'].rolling(window=self.short_window).mean()
        long_ma = self.data['close'].rolling(window=self.long_window).mean()
        
        current_short = short_ma.iloc[-1]
        current_long = long_ma.iloc[-1]
        prev_short = short_ma.iloc[-2] if len(short_ma) > 1 else current_short
        prev_long = long_ma.iloc[-2] if len(long_ma) > 1 else current_long
        
        # Check for crossover
        if current_short > current_long and prev_short <= prev_long:
            return "UP", 0.8  # Strong buy signal
        elif current_short < current_long and prev_short >= prev_long:
            return "DOWN", 0.8  # Strong sell signal
        elif current_short > current_long:
            return "UP", 0.6  # Weak buy signal
        else:
            return "DOWN", 0.6  # Weak sell signal

class RSIStrategy(SyntheticTradingStrategy):
    """RSI Strategy for Synthetic Indices"""
    
    def __init__(self, symbol: str, timeframe: str = '5m', period: int = 14, 
                 oversold: int = 30, overbought: int = 70):
        super().__init__(symbol, timeframe)
        self.period = period
        self.oversold = oversold
        self.overbought = overbought
        
    def calculate_rsi(self) -> float:
        """Calculate RSI value"""
        if len(self.data) < self.period + 1:
            return 50.0
        
        delta = self.data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi.iloc[-1]
    
    def get_signal(self) -> Tuple[str, float]:
        """Get trading signal based on RSI"""
        if len(self.data) < self.period + 1:
            return "HOLD", 0.0
        
        rsi = self.calculate_rsi()
        
        if rsi < self.oversold:
            return "UP", 0.9  # Strong buy signal (oversold)
        elif rsi > self.overbought:
            return "DOWN", 0.9  # Strong sell signal (overbought)
        elif rsi < 50:
            return "UP", 0.6  # Weak buy signal
        else:
            return "DOWN", 0.6  # Weak sell signal

class BollingerBandsStrategy(SyntheticTradingStrategy):
    """Bollinger Bands Strategy for Synthetic Indices"""
    
    def __init__(self, symbol: str, timeframe: str = '5m', period: int = 20, std_dev: float = 2.0):
        super().__init__(symbol, timeframe)
        self.period = period
        self.std_dev = std_dev
        
    def get_signal(self) -> Tuple[str, float]:
        """Get trading signal based on Bollinger Bands"""
        if len(self.data) < self.period:
            return "HOLD", 0.0
        
        # Calculate Bollinger Bands
        sma = self.data['close'].rolling(window=self.period).mean()
        std = self.data['close'].rolling(window=self.period).std()
        
        upper_band = sma + (std * self.std_dev)
        lower_band = sma - (std * self.std_dev)
        
        current_price = self.data['close'].iloc[-1]
        current_upper = upper_band.iloc[-1]
        current_lower = lower_band.iloc[-1]
        
        # Check for signals
        if current_price <= current_lower:
            return "UP", 0.8  # Price at lower band - buy signal
        elif current_price >= current_upper:
            return "DOWN", 0.8  # Price at upper band - sell signal
        else:
            return "HOLD", 0.0

class VolatilityBreakoutStrategy(SyntheticTradingStrategy):
    """Volatility Breakout Strategy for Synthetic Indices"""
    
    def __init__(self, symbol: str, timeframe: str = '5m', period: int = 20, multiplier: float = 1.5):
        super().__init__(symbol, timeframe)
        self.period = period
        self.multiplier = multiplier
        
    def get_signal(self) -> Tuple[str, float]:
        """Get trading signal based on volatility breakout"""
        if len(self.data) < self.period:
            return "HOLD", 0.0
        
        # Calculate average true range (ATR)
        high_low = self.data['high'] - self.data['low']
        high_close = np.abs(self.data['high'] - self.data['close'].shift())
        low_close = np.abs(self.data['low'] - self.data['close'].shift())
        
        true_range = np.maximum(high_low, np.maximum(high_close, low_close))
        atr = true_range.rolling(window=self.period).mean()
        
        current_atr = atr.iloc[-1]
        avg_atr = atr.mean()
        
        # Check for volatility breakout
        if current_atr > (avg_atr * self.multiplier):
            # High volatility - look for momentum
            price_change = self.data['close'].iloc[-1] - self.data['close'].iloc[-2]
            if price_change > 0:
                return "UP", 0.7  # Upward momentum
            else:
                return "DOWN", 0.7  # Downward momentum
        else:
            return "HOLD", 0.0

class MultiStrategy(SyntheticTradingStrategy):
    """Combines multiple strategies for better signals"""
    
    def __init__(self, symbol: str, timeframe: str = '5m'):
        super().__init__(symbol, timeframe)
        self.strategies = {
            'ma': MovingAverageCrossover(symbol, timeframe),
            'rsi': RSIStrategy(symbol, timeframe),
            'bb': BollingerBandsStrategy(symbol, timeframe),
            'vb': VolatilityBreakoutStrategy(symbol, timeframe)
        }
        
    def add_candle(self, candle: Dict):
        """Add candle to all strategies"""
        super().add_candle(candle)
        for strategy in self.strategies.values():
            strategy.add_candle(candle)
    
    def get_signal(self) -> Tuple[str, float]:
        """Get combined signal from all strategies"""
        signals = {}
        for name, strategy in self.strategies.items():
            signal, confidence = strategy.get_signal()
            signals[name] = (signal, confidence)
        
        # Count signals
        up_count = sum(1 for signal, _ in signals.values() if signal == "UP")
        down_count = sum(1 for signal, _ in signals.values() if signal == "DOWN")
        hold_count = sum(1 for signal, _ in signals.values() if signal == "HOLD")
        
        # Calculate average confidence
        total_confidence = sum(confidence for _, confidence in signals.values())
        avg_confidence = total_confidence / len(signals) if signals else 0
        
        # Determine final signal
        if up_count > down_count and up_count > hold_count:
            return "UP", min(avg_confidence * (up_count / len(signals)), 0.95)
        elif down_count > up_count and down_count > hold_count:
            return "DOWN", min(avg_confidence * (down_count / len(signals)), 0.95)
        else:
            return "HOLD", 0.0 