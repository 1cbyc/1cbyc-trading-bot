# MT5 Trading Bot

A Python-based trading bot that connects to MetaTrader 5 (MT5) demo account to trade forex, indices, and other instruments.

## Features

- **Direct MT5 Integration**: Connects directly to your MT5 demo account
- **Multiple Strategies**: Moving Average, RSI, Bollinger Bands, MACD
- **Multi-Instrument Trading**: Forex pairs, indices, commodities
- **Risk Management**: Position sizing and stop-loss management
- **Real-time Monitoring**: Live trade tracking and performance statistics

## Prerequisites

1. **MetaTrader 5 Terminal**: Download and install MT5 from your broker
2. **MT5 Demo Account**: Create a demo account with your broker
3. **Python 3.8+**: Ensure Python is installed on your system

## Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up Environment**:
   ```bash
   # Copy the example environment file
   cp .env-example .env
   
   # Edit .env with your MT5 credentials
   nano .env
   ```

3. **Configure MT5 Credentials**:
   - Open your MT5 terminal
   - Go to Tools → Options → Expert Advisors
   - Enable "Allow automated trading"
   - Note your account number, password, and server

## Configuration

Edit the `.env` file with your MT5 demo account details:

```env
# MT5 Demo Account Credentials
MT5_LOGIN=12345678
MT5_PASSWORD=your_password_here
MT5_SERVER=MetaQuotes-Demo

# Optional: Custom symbols to trade
MT5_SYMBOLS=EURUSD,GBPUSD,USDJPY,US30,US500

# Optional: Strategy type
MT5_STRATEGY=multi
```

### Available Symbols

**Forex Pairs**:
- `EURUSD` - Euro/US Dollar
- `GBPUSD` - British Pound/US Dollar
- `USDJPY` - US Dollar/Japanese Yen
- `USDCHF` - US Dollar/Swiss Franc
- `AUDUSD` - Australian Dollar/US Dollar
- `USDCAD` - US Dollar/Canadian Dollar

**Indices**:
- `US30` - Dow Jones Industrial Average
- `US500` - S&P 500
- `NAS100` - NASDAQ 100
- `GER30` - DAX 30
- `UK100` - FTSE 100

## Usage

### Basic Usage

```bash
python main.py
```

### Custom Symbols

```python
# Trade only specific symbols
symbols = ['EURUSD', 'GBPUSD', 'USDJPY']
bot = MT5TradingBot(symbols=symbols)
bot.start()
```

### Custom Strategy

```python
# Use different strategy
bot = MT5TradingBot(strategy_type='ma')  # Moving Average only
bot.start()
```

## Trading Strategies

The bot uses multiple strategies for signal generation:

1. **Moving Average Crossover**: 10-period vs 20-period MA
2. **RSI (Relative Strength Index)**: Oversold/Overbought levels
3. **Bollinger Bands**: Price channel analysis
4. **MACD**: Momentum and trend analysis

### Signal Generation

- **BUY Signal**: When multiple strategies agree on upward movement
- **SELL Signal**: When multiple strategies agree on downward movement
- **HOLD**: When signals are mixed or confidence is low

### Risk Management

- **Position Size**: 0.01 lots (minimum) per trade
- **Stop Loss**: Configurable per trade
- **Take Profit**: Configurable per trade
- **Maximum Positions**: Limited by account balance

## Monitoring

The bot provides real-time monitoring:

```
📊 Processing EURUSD...
🔍 Signal detected: EURUSD BUY (confidence: 0.75)
🎯 Executing trade: EURUSD BUY (confidence: 0.75)
✅ Order placed: EURUSD BUY 0.01 lots at 1.0850
```

## Performance Tracking

The bot tracks performance per symbol:

```
📊 FINAL TRADING STATISTICS:
==================================================
EURUSD:
  Trades: 5
  Win Rate: 60.0%
  P&L: $12.50

GBPUSD:
  Trades: 3
  Win Rate: 66.7%
  P&L: $8.75

OVERALL:
  Total Trades: 8
  Win Rate: 62.5%
  Total P&L: $21.25
```

## Safety Features

- **Demo Account Only**: Designed for demo trading
- **Position Limits**: Maximum position size controls
- **Error Handling**: Graceful error recovery
- **Graceful Shutdown**: Proper cleanup on exit

## Troubleshooting

### Common Issues

1. **Connection Failed**:
   - Check MT5 terminal is running
   - Verify login credentials
   - Ensure "Allow automated trading" is enabled

2. **No Data Received**:
   - Check symbol names are correct
   - Verify market hours
   - Check internet connection

3. **Order Failed**:
   - Insufficient margin
   - Market closed
   - Invalid symbol

### Debug Mode

Enable debug output by modifying the bot:

```python
# Add debug prints
print(f"Debug: {variable}")
```

## Disclaimer

⚠️ **This is for educational purposes only.**
- Use only on demo accounts
- Never risk real money
- Past performance doesn't guarantee future results
- Always test thoroughly before live trading

## Support

For issues and questions:
1. Check the troubleshooting section
2. Verify your MT5 setup
3. Review the error messages
4. Test with a single symbol first

## License

This project is for educational purposes. Use at your own risk. 