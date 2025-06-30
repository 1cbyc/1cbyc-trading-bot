#!/usr/bin/env python3
"""
Deriv Synthetic Indices Trading Bot Launcher
============================================

This script launches the Deriv trading bot with easy configuration.
"""

import sys
import os
from deriv_trading.main import DerivTradingBot

def main():
    print("🎯 Deriv Synthetic Indices Trading Bot")
    print("=" * 50)
    
    # Configuration - you can modify these
    symbols = ['R_100', 'R_75']  # Volatility indices to trade
    strategy = 'multi'  # Strategy type: 'multi', 'ma', 'rsi'
    
    print(f"📈 Trading symbols: {', '.join(symbols)}")
    print(f"🎯 Strategy: {strategy}")
    print()
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️  No .env file found!")
        print("Please create a .env file with your Deriv API credentials:")
        print()
        print("DERIV_ACCOUNT_TOKEN=your_token_here")
        print("DERIV_IS_DEMO=true")
        print("DERIV_DEFAULT_AMOUNT=1.00")
        print("DERIV_MAX_DAILY_LOSS=50.00")
        print("DERIV_MAX_DAILY_TRADES=20")
        print()
        print("Get your token from: https://app.deriv.com/account/api-token")
        return
    
    # Create and start the bot
    try:
        bot = DerivTradingBot(symbols=symbols, strategy_type=strategy)
        bot.start()
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 