#!/usr/bin/env python3
"""
Test script to check if strategies are generating signals
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from deriv_trading.strategies import MultiStrategy, MovingAverageCrossover, RSIStrategy
import random

def test_strategies():
    """Test if strategies generate signals with sample data"""
    
    # Create sample candle data
    base_price = 100.0
    candles = []
    
    for i in range(100):
        # Create some trending data
        trend = 0.1 * (i - 50)  # Upward trend
        noise = random.uniform(-2, 2)
        price = base_price + trend + noise
        
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
    
    # Test different strategies
    strategies = {
        'MA': MovingAverageCrossover('R_100'),
        'RSI': RSIStrategy('R_100'),
        'Multi': MultiStrategy('R_100')
    }
    
    for name, strategy in strategies.items():
        print(f"\n🧪 Testing {name} strategy:")
        
        # Add candles to strategy
        for candle in candles:
            strategy.add_candle(candle)
        
        # Get signal
        signal, confidence = strategy.get_signal()
        print(f"   Signal: {signal} (confidence: {confidence:.2f})")
        
        # Test with more data
        print(f"   Data points: {len(strategy.data)}")
        
        if hasattr(strategy, 'strategies'):
            print(f"   Sub-strategies: {len(strategy.strategies)}")
            for sub_name, sub_strategy in strategy.strategies.items():
                try:
                    sub_signal, sub_conf = sub_strategy.get_signal()
                    print(f"     {sub_name}: {sub_signal} ({sub_conf:.2f})")
                except Exception as e:
                    print(f"     {sub_name}: Error - {e}")

if __name__ == "__main__":
    test_strategies() 