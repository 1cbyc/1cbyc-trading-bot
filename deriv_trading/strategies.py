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

class MACDStrategy(SyntheticTradingStrategy):
    """MACD (Moving Average Convergence Divergence) Strategy"""
    
    def __init__(self, symbol: str, timeframe: str = '5m', fast_period: int = 12, 
                 slow_period: int = 26, signal_period: int = 9):
        super().__init__(symbol, timeframe)
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period
        
    def calculate_macd(self) -> Tuple[float, float, float]:
        """Calculate MACD line, signal line, and histogram"""
        if len(self.data) < self.slow_period:
            return 0.0, 0.0, 0.0
        
        # Calculate EMAs
        ema_fast = self.data['close'].ewm(span=self.fast_period).mean()
        ema_slow = self.data['close'].ewm(span=self.slow_period).mean()
        
        # MACD line
        macd_line = ema_fast - ema_slow
        
        # Signal line
        signal_line = macd_line.ewm(span=self.signal_period).mean()
        
        # Histogram
        histogram = macd_line - signal_line
        
        return macd_line.iloc[-1], signal_line.iloc[-1], histogram.iloc[-1]
    
    def get_signal(self) -> Tuple[str, float]:
        """Get trading signal based on MACD"""
        if len(self.data) < self.slow_period:
            return "HOLD", 0.0
        
        macd_line, signal_line, histogram = self.calculate_macd()
        
        # Check for MACD crossover
        if macd_line > signal_line and histogram > 0:
            return "UP", 0.8  # Bullish signal
        elif macd_line < signal_line and histogram < 0:
            return "DOWN", 0.8  # Bearish signal
        else:
            return "HOLD", 0.0

class StochasticStrategy(SyntheticTradingStrategy):
    """Stochastic Oscillator Strategy"""
    
    def __init__(self, symbol: str, timeframe: str = '5m', k_period: int = 14, 
                 d_period: int = 3, oversold: int = 20, overbought: int = 80):
        super().__init__(symbol, timeframe)
        self.k_period = k_period
        self.d_period = d_period
        self.oversold = oversold
        self.overbought = overbought
        
    def calculate_stochastic(self) -> Tuple[float, float]:
        """Calculate %K and %D lines"""
        if len(self.data) < self.k_period:
            return 50.0, 50.0
        
        # Calculate %K
        lowest_low = self.data['low'].rolling(window=self.k_period).min()
        highest_high = self.data['high'].rolling(window=self.k_period).max()
        
        k_percent = 100 * ((self.data['close'] - lowest_low) / (highest_high - lowest_low))
        
        # Calculate %D (SMA of %K)
        d_percent = k_percent.rolling(window=self.d_period).mean()
        
        return k_percent.iloc[-1], d_percent.iloc[-1]
    
    def get_signal(self) -> Tuple[str, float]:
        """Get trading signal based on Stochastic"""
        if len(self.data) < self.k_period:
            return "HOLD", 0.0
        
        k_percent, d_percent = self.calculate_stochastic()
        
        # Check for oversold/overbought conditions
        if k_percent < self.oversold and d_percent < self.oversold:
            return "UP", 0.9  # Strong buy signal
        elif k_percent > self.overbought and d_percent > self.overbought:
            return "DOWN", 0.9  # Strong sell signal
        elif k_percent < 50 and d_percent < 50:
            return "UP", 0.6  # Weak buy signal
        elif k_percent > 50 and d_percent > 50:
            return "DOWN", 0.6  # Weak sell signal
        else:
            return "HOLD", 0.0

class WilliamsRStrategy(SyntheticTradingStrategy):
    """Williams %R Strategy"""
    
    def __init__(self, symbol: str, timeframe: str = '5m', period: int = 14, 
                 oversold: int = -80, overbought: int = -20):
        super().__init__(symbol, timeframe)
        self.period = period
        self.oversold = oversold
        self.overbought = overbought
        
    def calculate_williams_r(self) -> float:
        """Calculate Williams %R"""
        if len(self.data) < self.period:
            return -50.0
        
        highest_high = self.data['high'].rolling(window=self.period).max()
        lowest_low = self.data['low'].rolling(window=self.period).min()
        
        williams_r = -100 * ((highest_high - self.data['close']) / (highest_high - lowest_low))
        
        return williams_r.iloc[-1]
    
    def get_signal(self) -> Tuple[str, float]:
        """Get trading signal based on Williams %R"""
        if len(self.data) < self.period:
            return "HOLD", 0.0
        
        williams_r = self.calculate_williams_r()
        
        if williams_r < self.oversold:
            return "UP", 0.9  # Oversold - buy signal
        elif williams_r > self.overbought:
            return "DOWN", 0.9  # Overbought - sell signal
        else:
            return "HOLD", 0.0

class ParabolicSARStrategy(SyntheticTradingStrategy):
    """Parabolic SAR Strategy"""
    
    def __init__(self, symbol: str, timeframe: str = '5m', acceleration: float = 0.02, 
                 maximum: float = 0.2):
        super().__init__(symbol, timeframe)
        self.acceleration = acceleration
        self.maximum = maximum
        
    def calculate_sar(self) -> float:
        """Calculate Parabolic SAR"""
        if len(self.data) < 2:
            return self.data['close'].iloc[-1] if len(self.data) > 0 else 0.0
        
        # Simplified SAR calculation
        high = self.data['high'].iloc[-1]
        low = self.data['low'].iloc[-1]
        close = self.data['close'].iloc[-1]
        
        # Basic SAR logic
        if close > high * 0.99:  # Price near high
            return low * 0.99  # SAR below low
        elif close < low * 1.01:  # Price near low
            return high * 1.01  # SAR above high
        else:
            return close  # Neutral
        
    def get_signal(self) -> Tuple[str, float]:
        """Get trading signal based on Parabolic SAR"""
        if len(self.data) < 2:
            return "HOLD", 0.0
        
        sar = self.calculate_sar()
        current_price = self.data['close'].iloc[-1]
        
        if current_price > sar:
            return "UP", 0.7  # Bullish
        elif current_price < sar:
            return "DOWN", 0.7  # Bearish
        else:
            return "HOLD", 0.0

class IchimokuStrategy(SyntheticTradingStrategy):
    """Ichimoku Cloud Strategy"""
    
    def __init__(self, symbol: str, timeframe: str = '5m'):
        super().__init__(symbol, timeframe)
        
    def calculate_ichimoku(self) -> Dict[str, float]:
        """Calculate Ichimoku components"""
        if len(self.data) < 52:
            return {}
        
        # Tenkan-sen (Conversion Line): (9-period high + 9-period low)/2
        period9_high = self.data['high'].rolling(window=9).max()
        period9_low = self.data['low'].rolling(window=9).min()
        tenkan_sen = (period9_high + period9_low) / 2
        
        # Kijun-sen (Base Line): (26-period high + 26-period low)/2
        period26_high = self.data['high'].rolling(window=26).max()
        period26_low = self.data['low'].rolling(window=26).min()
        kijun_sen = (period26_high + period26_low) / 2
        
        # Senkou Span A (Leading Span A): (Conversion Line + Base Line)/2
        senkou_span_a = (tenkan_sen + kijun_sen) / 2
        
        # Senkou Span B (Leading Span B): (52-period high + 52-period low)/2
        period52_high = self.data['high'].rolling(window=52).max()
        period52_low = self.data['low'].rolling(window=52).min()
        senkou_span_b = (period52_high + period52_low) / 2
        
        return {
            'tenkan_sen': tenkan_sen.iloc[-1],
            'kijun_sen': kijun_sen.iloc[-1],
            'senkou_span_a': senkou_span_a.iloc[-1],
            'senkou_span_b': senkou_span_b.iloc[-1]
        }
    
    def get_signal(self) -> Tuple[str, float]:
        """Get trading signal based on Ichimoku Cloud"""
        if len(self.data) < 52:
            return "HOLD", 0.0
        
        ichimoku = self.calculate_ichimoku()
        current_price = self.data['close'].iloc[-1]
        
        # Check if price is above cloud (bullish)
        if current_price > max(ichimoku['senkou_span_a'], ichimoku['senkou_span_b']):
            return "UP", 0.8
        # Check if price is below cloud (bearish)
        elif current_price < min(ichimoku['senkou_span_a'], ichimoku['senkou_span_b']):
            return "DOWN", 0.8
        else:
            return "HOLD", 0.0

class MomentumStrategy(SyntheticTradingStrategy):
    """Momentum-based Strategy using Rate of Change"""
    
    def __init__(self, symbol: str, timeframe: str = '5m', period: int = 10, 
                 threshold: float = 0.5):
        super().__init__(symbol, timeframe)
        self.period = period
        self.threshold = threshold
        
    def calculate_momentum(self) -> float:
        """Calculate momentum using Rate of Change"""
        if len(self.data) < self.period:
            return 0.0
        
        current_price = self.data['close'].iloc[-1]
        past_price = self.data['close'].iloc[-self.period]
        
        momentum = ((current_price - past_price) / past_price) * 100
        return momentum
    
    def get_signal(self) -> Tuple[str, float]:
        """Get trading signal based on momentum"""
        if len(self.data) < self.period:
            return "HOLD", 0.0
        
        momentum = self.calculate_momentum()
        
        if momentum > self.threshold:
            return "UP", min(abs(momentum) / 10, 0.9)  # Strong positive momentum
        elif momentum < -self.threshold:
            return "DOWN", min(abs(momentum) / 10, 0.9)  # Strong negative momentum
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
            'vb': VolatilityBreakoutStrategy(symbol, timeframe),
            'macd': MACDStrategy(symbol, timeframe),
            'stoch': StochasticStrategy(symbol, timeframe),
            'williams': WilliamsRStrategy(symbol, timeframe),
            'sar': ParabolicSARStrategy(symbol, timeframe),
            'ichimoku': IchimokuStrategy(symbol, timeframe),
            'momentum': MomentumStrategy(symbol, timeframe)
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
            try:
                signal, confidence = strategy.get_signal()
                signals[name] = (signal, confidence)
            except Exception as e:
                print(f"Error in strategy {name}: {e}")
                signals[name] = ("HOLD", 0.0)
        
        # Count signals
        up_count = sum(1 for signal, _ in signals.values() if signal == "UP")
        down_count = sum(1 for signal, _ in signals.values() if signal == "DOWN")
        hold_count = sum(1 for signal, _ in signals.values() if signal == "HOLD")
        
        # Calculate average confidence
        total_confidence = sum(confidence for _, confidence in signals.values())
        avg_confidence = total_confidence / len(signals) if signals else 0
        
        # More aggressive logic: if we have any clear signal, use it
        if up_count > down_count and up_count > 0:
            return "UP", min(avg_confidence * (up_count / len(signals)), 0.95)
        elif down_count > up_count and down_count > 0:
            return "DOWN", min(avg_confidence * (down_count / len(signals)), 0.95)
        else:
            return "HOLD", 0.0 