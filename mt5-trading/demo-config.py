import os
from typing import List, Dict, Any
from dotenv import load_dotenv

class MT5Config:
    """Configuration class for MT5 Trading Bot"""
    
    # Load environment variables
    load_dotenv()
    
    # MT5 Connection Settings (from environment variables)
    MT5_LOGIN = int(os.getenv('MT5_LOGIN', '0'))
    MT5_PASSWORD = os.getenv('MT5_PASSWORD', '')
    MT5_SERVER = os.getenv('MT5_SERVER', 'Deriv-Demo')
    
    # Trading Symbols (Deriv Synthetic Indices) - FOCUS ON ONE INSTRUMENT FOR DEBUGGING
    # DEFAULT_SYMBOLS = [
    #     'Volatility 100 Index', 'Volatility 75 Index', 'Volatility 50 Index',
    #     'Boom 1000 Index', 'Crash 1000 Index', 'Step Index',
    #     'Range Break 100 Index', 'Jump 100 Index'
    # ]
    DEFAULT_SYMBOLS = ['Volatility 100 Index']  # <--- Only trade this for now
    
    # Strategy Configuration
    AVAILABLE_STRATEGIES = {
        'ma': 'MovingAverageCrossover',
        'rsi': 'RSIStrategy', 
        'bollinger': 'BollingerBandsStrategy',
        'volatility': 'VolatilityBreakoutStrategy',
        'macd': 'MACDStrategy',
        'stochastic': 'StochasticStrategy',
        'williams_r': 'WilliamsRStrategy',
        'parabolic_sar': 'ParabolicSARStrategy',
        'ichimoku': 'IchimokuStrategy',
        'momentum': 'MomentumStrategy',
        'mean_reversion': 'MeanReversionStrategy',
        'trend_following': 'TrendFollowingStrategy',
        'advanced_volatility': 'AdvancedVolatilityStrategy',
        'support_resistance': 'SupportResistanceStrategy',
        'divergence': 'DivergenceStrategy',
        'volume_price': 'VolumePriceStrategy',
        'fibonacci': 'FibonacciRetracementStrategy',
        'adaptive': 'AdaptiveStrategy',
        'elliott_wave': 'ElliottWaveStrategy',
        'harmonic_pattern': 'HarmonicPatternStrategy',
        'order_flow': 'OrderFlowStrategy',
        'market_microstructure': 'MarketMicrostructureStrategy',
        'sentiment': 'SentimentAnalysisStrategy',
        'momentum_divergence': 'MomentumDivergenceStrategy',
        'volatility_regime': 'VolatilityRegimeStrategy',
        'price_action': 'PriceActionStrategy',
        'correlation': 'CorrelationStrategy',
        'ml_inspired': 'MachineLearningInspiredStrategy',
        'multi': 'MultiStrategy'
    }
    
    # Default Strategy Selection
    DEFAULT_STRATEGY = 'multi'
    
    # Strategy Weights for Multi-Strategy (confidence multipliers)
    STRATEGY_WEIGHTS = {
        'MovingAverageCrossover': 1.0,
        'RSIStrategy': 1.2,
        'BollingerBandsStrategy': 1.0,
        'VolatilityBreakoutStrategy': 1.1,
        'MACDStrategy': 1.0,
        'StochasticStrategy': 0.9,
        'WilliamsRStrategy': 0.9,
        'ParabolicSARStrategy': 0.8,
        'IchimokuStrategy': 1.0,
        'MomentumStrategy': 0.8,
        'MeanReversionStrategy': 1.1,
        'TrendFollowingStrategy': 1.0,
        'AdvancedVolatilityStrategy': 1.1,
        'SupportResistanceStrategy': 1.0,
        'DivergenceStrategy': 1.2,
        'VolumePriceStrategy': 0.9,
        'FibonacciRetracementStrategy': 0.8,
        'AdaptiveStrategy': 1.0,
        'ElliottWaveStrategy': 0.7,
        'HarmonicPatternStrategy': 0.7,
        'OrderFlowStrategy': 1.0,
        'MarketMicrostructureStrategy': 0.8,
        'SentimentAnalysisStrategy': 0.8,
        'MomentumDivergenceStrategy': 1.1,
        'VolatilityRegimeStrategy': 1.0,
        'PriceActionStrategy': 1.0,
        'CorrelationStrategy': 0.5,
        'MachineLearningInspiredStrategy': 0.9,
        'MultiStrategy': 1.0
    }
    
    # Trading Parameters (from environment variables with defaults)
    TIMEFRAME = os.getenv('MT5_TIMEFRAME', 'M5')
    VOLUME = float(os.getenv('MT5_VOLUME', '0.01'))
    CONFIDENCE_THRESHOLD = float(os.getenv('MT5_CONFIDENCE_THRESHOLD', '0.4'))
    MAX_POSITIONS_PER_SYMBOL = 1
    MAX_TOTAL_POSITIONS = 5
    
    # Risk Management
    STOP_LOSS_PERCENT = 2.0  # 2% stop loss
    TAKE_PROFIT_PERCENT = 4.0  # 4% take profit
    MAX_DAILY_LOSS = 10.0  # 10% max daily loss
    MAX_DAILY_PROFIT = 20.0  # 20% max daily profit
    
    # Time Settings (from environment variables with defaults)
    TRADING_INTERVAL = int(os.getenv('MT5_TRADING_INTERVAL', '10'))  # seconds between trading cycles
    DATA_LOOKBACK = 100  # number of candles to analyze
    
    # Minimum volume per instrument
    MIN_VOLUME_MAP = {
        "Volatility 10 Index": 0.5,
        "Volatility 10 (1s) Index": 0.5,
        "Volatility 25 Index": 0.5,
        "Volatility 25 (1s) Index": 0.005,
        "Volatility 50 Index": 4.0,
        "Volatility 50 (1s) Index": 0.005,
        "Volatility 75 Index": 0.001,
        "Volatility 75 (1s) Index": 0.05,
        "Volatility 100 Index": 0.5,
        "Volatility 100 (1s) Index": 0.2,
        "Volatility 150 (1s) Index": 0.01,
        "Volatility 200 (1s) Index": 0.02,
        "Volatility 300 (1s) Index": 1.0,
        "Boom 1000 Index": 0.2,
        "Crash 1000 Index": 0.2,
        "Boom 500 Index": 0.2,
        "Crash 500 Index": 0.2,
        "Boom 300 Index": 1.0,
        "Crash 300 Index": 0.5,
        "Jump 10 Index": 0.01,
        "Jump 25 Index": 0.01,
        "Jump 50 Index": 0.01,
        "Jump 75 Index": 0.01,
        "Jump 100 Index": 0.01,
        "Step Index": 0.1,
        "Range Break 100 Index": 0.01,
        "Range Break 200 Index": 0.01,
        # Add more as needed
    }

    @classmethod
    def get_min_volume(cls, symbol: str) -> float:
        """Get the minimum volume for a symbol, or fallback to config/env value"""
        return cls.MIN_VOLUME_MAP.get(symbol, cls.VOLUME)
    
    @classmethod
    def get_strategy_class(cls, strategy_name: str) -> str:
        """Get the class name for a strategy"""
        return cls.AVAILABLE_STRATEGIES.get(strategy_name, cls.AVAILABLE_STRATEGIES['multi'])
    
    @classmethod
    def get_strategy_weight(cls, strategy_class: str) -> float:
        """Get the weight/confidence multiplier for a strategy"""
        return cls.STRATEGY_WEIGHTS.get(strategy_class, 1.0)
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate the configuration"""
        if not cls.MT5_LOGIN or not cls.MT5_PASSWORD:
            raise ValueError("MT5 credentials not configured in environment variables")
        if not cls.DEFAULT_SYMBOLS:
            raise ValueError("No trading symbols configured")
        return True
    
    @classmethod
    def get_symbols_from_env(cls) -> List[str]:
        """Get symbols from environment variable or use defaults"""
        symbols_str = os.getenv('MT5_SYMBOLS', '')
        if symbols_str:
            return [s.strip() for s in symbols_str.split(',') if s.strip()]
        return cls.DEFAULT_SYMBOLS
    
    @classmethod
    def get_strategy_from_env(cls) -> str:
        """Get strategy from environment variable or use default"""
        return os.getenv('MT5_STRATEGY', cls.DEFAULT_STRATEGY) 