# Deriv Trading Bot

A Python-based automated trading bot for Deriv synthetic indices and boom/crash indices using WebSocket API.

## Features

- **Multi-Instrument Trading**: Trades all synthetic indices and boom/crash indices simultaneously
- **Real-time Trading**: Uses WebSocket API for live price data
- **Multiple Strategies**: 
  - Moving Average Crossover
  - RSI (Relative Strength Index)
  - Bollinger Bands
  - Volatility Breakout
- **Risk Management**: 
  - Daily loss limits
  - Position sizing
  - Consecutive loss protection
- **Performance Tracking**: Individual statistics for each instrument
- **Demo Account Support**: Safe testing with demo funds

## Supported Instruments

### Volatility Indices
- `R_10` - Volatility 10 Index
- `R_25` - Volatility 25 Index
- `R_50` - Volatility 50 Index
- `R_75` - Volatility 75 Index
- `R_100` - Volatility 100 Index
- `R_150` - Volatility 150 Index
- `R_200` - Volatility 200 Index

### Boom & Crash Indices
- `BOOM1000` - Boom 1000 Index
- `CRASH1000` - Crash 1000 Index
- `BOOM500` - Boom 500 Index
- `CRASH500` - Crash 500 Index

## Quick Start

### 1. Install Dependencies

```bash
pip install -r deriv_requirements.txt
```

### 2. Setup Environment

```bash
python create_env.py
```

This will prompt you for:
- **Deriv API Token**: Get from https://app.deriv.com/account/api-token
- **App ID**: Usually `1089` for demo accounts

### 3. Run the Bot

```bash
python -m deriv_trading.main
```

The bot will automatically trade all 11 instruments (7 volatility + 4 boom/crash indices).

## Configuration

The bot uses a `.env` file for configuration:

```env
# API Credentials
DERIV_API_TOKEN=your_token_here
DERIV_APP_ID=your_app_id_here

# Trading Configuration
SYMBOL=R_100
CONFIDENCE_THRESHOLD=0.4
TRADE_DURATION=5
MIN_DATA_POINTS=50

# Risk Management
MAX_DAILY_LOSS=50.0
MAX_POSITION_SIZE=10.0
MAX_CONSECUTIVE_LOSSES=5
RISK_PER_TRADE=0.02
```

## Multi-Instrument Features

### Automatic Instrument Selection
- By default, trades all 11 synthetic and boom/crash indices
- Each instrument is analyzed independently
- Position sizes are reduced by 50% to manage risk across multiple instruments

### Performance Tracking
- Individual statistics for each instrument
- Win rates, P&L, and trade counts per symbol
- Overall portfolio performance metrics

### Custom Instrument Selection
You can customize which instruments to trade:

```python
# Trade only specific instruments
symbols = ['R_100', 'BOOM1000', 'CRASH1000']
bot = DerivTradingBot(symbols=symbols)

# Trade all instruments (default)
bot = DerivTradingBot()
```

## Trading Strategies

### Moving Average Crossover
- Compares short-term (10 periods) vs long-term (20 periods) moving averages
- Generates CALL signals when short MA > long MA
- Generates PUT signals when short MA < long MA

### RSI Strategy
- Uses 14-period RSI with 30/70 oversold/overbought levels
- CALL signals when RSI < 30 (oversold)
- PUT signals when RSI > 70 (overbought)

### Bollinger Bands
- Uses 20-period SMA with 2 standard deviations
- CALL signals when price touches lower band
- PUT signals when price touches upper band

### Volatility Breakout
- Detects price movements beyond normal volatility
- CALL signals on positive breakouts
- PUT signals on negative breakouts

## Risk Management

- **Daily Loss Limit**: Stops trading if daily loss exceeds $50
- **Position Sizing**: Adjusts trade size based on signal strength
- **Multi-Instrument Risk**: Reduces position sizes by 50% for multi-instrument trading
- **Consecutive Losses**: Stops after 5 consecutive losses
- **Balance Protection**: Maintains minimum balance buffer

## Output Guide

### Connection Messages
- `Connected to Deriv WebSocket API` - Successfully connected
- `Successfully authorized with Deriv API` - API authentication successful
- `Trading symbols: R_10, R_25, R_50, R_75, R_100, R_150, R_200, BOOM1000, CRASH1000, BOOM500, CRASH500` - All instruments loaded

### Trading Signals
- `Strong signal: R_100 CALL (confidence: 0.75)` - High-confidence buy signal
- `Strong signal: BOOM1000 PUT (confidence: 0.68)` - High-confidence sell signal
- `Risk check failed: Daily loss limit reached` - Risk management blocked trade

### Trade Execution
- `Executing trade: R_100 CALL` - Placing a buy trade
- `Position size: $2.50` - Trade amount (reduced for multi-instrument)
- `Trade placed: R_100 CALL - 12345678` - Order confirmed

### Performance Statistics
- Individual instrument performance displayed
- Overall portfolio statistics
- Risk management summary

## Safety Features

- **Demo Account**: Uses demo funds by default
- **Environment Variables**: Secure credential storage
- **Git Ignore**: `.env` file is excluded from version control
- **Error Handling**: Graceful handling of API errors
- **Logging**: Detailed logs for debugging
- **Multi-Instrument Safety**: Reduced position sizes and rotation delays

## Getting API Credentials

1. Go to https://app.deriv.com/account/api-token
2. Create a new token with appropriate permissions
3. Note your App ID (usually `1089` for demo)
4. Use these in the setup script

## Disclaimer

⚠️ **Trading involves risk. This bot is for educational purposes only.**

- Past performance doesn't guarantee future results
- Start with demo accounts only
- Never risk more than you can afford to lose
- Monitor the bot's performance regularly
- Multi-instrument trading increases complexity and risk

## Troubleshooting

### Connection Issues
- Check your internet connection
- Verify API token and App ID are correct
- Ensure you're using a valid demo account

### No Trading Signals
- Lower the confidence threshold (default: 0.4)
- Check if market conditions are suitable
- Review strategy parameters

### Risk Management Blocks
- Check daily loss limits
- Review consecutive loss count
- Verify account balance

### Multi-Instrument Performance
- Monitor individual instrument performance
- Consider reducing the number of instruments if performance is poor
- Check for correlation between instruments

## Support

For issues or questions:
1. Check the logs for error messages
2. Verify your API credentials
3. Ensure all dependencies are installed
4. Test with demo account first
5. Start with fewer instruments if needed 