#!/usr/bin/env python3
"""
Test script to demonstrate all advanced trading strategies
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from deriv_trading.strategies import (
    MultiStrategy, MovingAverageCrossover, RSIStrategy, BollingerBandsStrategy,
    VolatilityBreakoutStrategy, MACDStrategy, StochasticStrategy, WilliamsRStrategy,
    ParabolicSARStrategy, IchimokuStrategy, MomentumStrategy, MeanReversionStrategy,
    TrendFollowingStrategy, AdvancedVolatilityStrategy, SupportResistanceStrategy,
    DivergenceStrategy, VolumePriceStrategy, FibonacciRetracementStrategy, AdaptiveStrategy,
    ElliottWaveStrategy, HarmonicPatternStrategy, OrderFlowStrategy, MarketMicrostructureStrategy,
    SentimentAnalysisStrategy, MomentumDivergenceStrategy, VolatilityRegimeStrategy,
    PriceActionStrategy, CorrelationStrategy, MachineLearningInspiredStrategy
)
import random

def test_all_strategies():
    """Test all available strategies with sample data"""
    
    # Create sample candle data with different market conditions
    base_price = 100.0
    candles = []
    
    for i in range(100):
        # Create trending data with some volatility
        trend = 0.05 * (i - 50)  # Upward trend
        volatility = 2.0 * random.uniform(-1, 1)
        noise = random.uniform(-1, 1)
        price = base_price + trend + volatility + noise
        
        candle = {
            'epoch': 1609459200 + i * 300,  # 5-minute intervals
            'open': price - random.uniform(0, 1),
            'high': price + random.uniform(0, 2),
            'low': price - random.uniform(0, 2),
            'close': price,
            'volume': random.uniform(100, 1000)
        }
        candles.append(candle)
    
    print(f"📊 Generated {len(candles)} sample candles")
    
    # Test individual strategies
    strategies = {
        # Basic strategies (10)
        'MA Crossover': MovingAverageCrossover('R_100'),
        'RSI': RSIStrategy('R_100'),
        'Bollinger Bands': BollingerBandsStrategy('R_100'),
        'Volatility Breakout': VolatilityBreakoutStrategy('R_100'),
        'MACD': MACDStrategy('R_100'),
        'Stochastic': StochasticStrategy('R_100'),
        'Williams %R': WilliamsRStrategy('R_100'),
        'Parabolic SAR': ParabolicSARStrategy('R_100'),
        'Ichimoku': IchimokuStrategy('R_100'),
        'Momentum': MomentumStrategy('R_100'),
        
        # Advanced strategies (8)
        'Mean Reversion': MeanReversionStrategy('R_100'),
        'Trend Following': TrendFollowingStrategy('R_100'),
        'Advanced Volatility': AdvancedVolatilityStrategy('R_100'),
        'Support/Resistance': SupportResistanceStrategy('R_100'),
        'Divergence': DivergenceStrategy('R_100'),
        'Volume/Price': VolumePriceStrategy('R_100'),
        'Fibonacci': FibonacciRetracementStrategy('R_100'),
        'Adaptive': AdaptiveStrategy('R_100'),
        
        # Ultra-advanced strategies (10) - NEW ADDITIONS
        'Elliott Wave': ElliottWaveStrategy('R_100'),
        'Harmonic Pattern': HarmonicPatternStrategy('R_100'),
        'Order Flow': OrderFlowStrategy('R_100'),
        'Market Microstructure': MarketMicrostructureStrategy('R_100'),
        'Sentiment Analysis': SentimentAnalysisStrategy('R_100'),
        'Momentum Divergence': MomentumDivergenceStrategy('R_100'),
        'Volatility Regime': VolatilityRegimeStrategy('R_100'),
        'Price Action': PriceActionStrategy('R_100'),
        'Correlation': CorrelationStrategy('R_100'),
        'ML Inspired': MachineLearningInspiredStrategy('R_100')
    }
    
    print(f"\n🧪 Testing {len(strategies)} individual strategies:")
    print("=" * 70)
    
    for name, strategy in strategies.items():
        # Add candles to strategy
        for candle in candles:
            strategy.add_candle(candle)
        
        # Get signal
        signal, confidence = strategy.get_signal()
        print(f"{name:<25}: {signal:<4} (confidence: {confidence:.2f})")
    
    # Test the enhanced MultiStrategy
    print(f"\n🎯 Testing Enhanced MultiStrategy:")
    print("=" * 70)
    
    multi_strategy = MultiStrategy('R_100')
    
    # Add candles to multi-strategy
    for candle in candles:
        multi_strategy.add_candle(candle)
    
    # Get combined signal
    signal, confidence = multi_strategy.get_signal()
    print(f"Combined Signal: {signal} (confidence: {confidence:.2f})")
    
    # Show individual strategy breakdown
    print(f"\n📋 Individual Strategy Breakdown:")
    print("-" * 50)
    
    for name, strategy in multi_strategy.strategies.items():
        try:
            sub_signal, sub_conf = strategy.get_signal()
            print(f"{name:<25}: {sub_signal:<4} ({sub_conf:.2f})")
        except Exception as e:
            print(f"{name:<25}: Error - {e}")
    
    print(f"\n🚀 Strategy Summary:")
    print(f"• Total Strategies: {len(multi_strategy.strategies)}")
    print(f"• Basic Strategies: 10")
    print(f"• Advanced Strategies: 8")
    print(f"• Ultra-Advanced Strategies: 10")
    print(f"• Combined Signal: {signal} ({confidence:.2f})")
    
    if signal != "HOLD":
        print(f"✅ Signal detected! Ready to trade.")
    else:
        print(f"⏸️  No strong signal detected.")
    
    print(f"\n🎯 Multi-Confirmation System:")
    print(f"• 28 different analysis perspectives")
    print(f"• Cross-confirmation across all boards")
    print(f"• Professional-grade trading system")
    print(f"• Institutional-level sophistication")

if __name__ == "__main__":
    test_all_strategies() 