# Deriv Synthetic Indices Trading Bot

🎯 **Automated trading bot for Deriv's synthetic indices with advanced risk management**

## Overview

This trading bot is specifically designed for Deriv's synthetic indices (Volatility, Boom, and Crash indices). It uses multiple technical analysis strategies and includes comprehensive risk management to protect your capital.

## Features

- **Multiple Trading Strategies**: Moving Average Crossover, RSI, Bollinger Bands, Volatility Breakout
- **Multi-Strategy Combination**: Combines all strategies for better signal accuracy
- **Advanced Risk Management**: Daily loss limits, position sizing, consecutive loss protection
- **Real-time Trading**: Live price feeds and instant trade execution
- **Demo & Live Support**: Works with both demo and live accounts
- **Comprehensive Logging**: Detailed trade logs and performance metrics

## Supported Synthetic Indices

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

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/1cbyc/1cbyc-trading-bot.git
   cd 1cbyc-trading-bot
   ```

2. **Install dependencies**:
   ```bash
   py -m pip install -r deriv_requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp deriv.env-example .env
   ```
   
   Edit the `.env` file with your Deriv API credentials.

## Configuration

### Getting Your Deriv API Token

1. Go to [Deriv Account Settings](https://app.deriv.com/account/api-token)
2. Create a new API token
3. Copy the token to your `.env` file

### Environment Variables

```env
# Your Deriv API token
DERIV_ACCOUNT_TOKEN=your_token_here

# Demo or Live account
DERIV_IS_DEMO=true

# Default trade amount
DERIV_DEFAULT_AMOUNT=1.00

# Risk management
DERIV_MAX_DAILY_LOSS=50.00
DERIV_MAX_DAILY_TRADES=20
```

## Usage

### Quick Start

1. **Set up your `.env` file** with your API token
2. **Run the bot**:
   ```bash
   py deriv_bot.py
   ```

### Custom Configuration

You can modify the trading parameters in `deriv_bot.py`:

```python
# Trading symbols
symbols = ['R_100', 'R_75']  # Volatility indices

# Strategy type
strategy = 'multi'  # 'multi', 'ma', 'rsi'
```

## Trading Strategies

### 1. Multi-Strategy (Recommended)
Combines all strategies for maximum accuracy:
- Moving Average Crossover
- RSI (Relative Strength Index)
- Bollinger Bands
- Volatility Breakout

### 2. Moving Average Crossover
- Short-term vs Long-term moving averages
- Generates signals on crossovers
- Good for trending markets

### 3. RSI Strategy
- Oversold/Overbought conditions
- Momentum-based signals
- Good for range-bound markets

## Risk Management

The bot includes comprehensive risk management:

- **Daily Loss Limit**: Stops trading if daily loss exceeds limit
- **Position Sizing**: Adjusts trade size based on confidence and risk
- **Consecutive Loss Protection**: Reduces position size after losses
- **Maximum Drawdown**: Stops trading if account drawdown is too high
- **Daily Trade Limit**: Limits number of trades per day

## Safety Features

- **Demo Mode**: Always test with demo account first
- **Small Position Sizes**: Starts with $1 trades
- **Automatic Stop Loss**: Built-in risk controls
- **Graceful Shutdown**: Handles interruptions safely

## Getting Started (Step by Step)

### Step 1: Create Deriv Account
1. Go to [Deriv.com](https://deriv.com)
2. Create a demo account
3. Verify your account

### Step 2: Get API Token
1. Go to Account Settings → API Token
2. Create a new token
3. Copy the token

### Step 3: Set Up Bot
1. Copy `deriv.env-example` to `.env`
2. Add your API token to `.env`
3. Set `DERIV_IS_DEMO=true`

### Step 4: Test with Demo
1. Run the bot: `py deriv_bot.py`
2. Monitor the trades
3. Check performance

### Step 5: Go Live (Optional)
1. Create a live account
2. Fund your account
3. Set `DERIV_IS_DEMO=false`
4. Start with small amounts

## Important Warnings

⚠️ **Risk Warning**: Trading involves substantial risk of loss. Only trade with money you can afford to lose.

⚠️ **Demo First**: Always test thoroughly with demo account before using real money.

⚠️ **Start Small**: Begin with small trade amounts and gradually increase.

⚠️ **Monitor**: Don't leave the bot unattended for long periods.

## Performance Monitoring

The bot provides real-time performance metrics:

```
📊 RISK SUMMARY:
├── Daily Trades: 5/20
├── Win Rate: 60.0%
├── Daily P&L: $2.50
├── Daily Loss: $5.00/$50.00
├── Consecutive Losses: 1/5
└── Balance: $102.50 (Initial: $100.00)
```

## Troubleshooting

### Common Issues

1. **Connection Failed**
   - Check your internet connection
   - Verify API token is correct
   - Ensure Deriv servers are accessible

2. **Authorization Failed**
   - Check API token format
   - Verify token permissions
   - Try regenerating the token

3. **No Trades Executed**
   - Check if market is open
   - Verify symbol names are correct
   - Check risk management settings

### Support

For issues and questions:
- Check the logs for error messages
- Verify your configuration
- Test with demo account first

## Disclaimer

This software is for educational purposes only. Trading involves substantial risk of loss. The authors are not responsible for any financial losses incurred through the use of this software.

## License

This project is open source and available under the MIT License. 