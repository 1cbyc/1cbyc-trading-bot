# Deriv Trading Bot - Output Guide

## 🎯 **Bot Startup Messages**

### Initial Configuration
```
🎯 Deriv Synthetic Indices Trading Bot
==================================================
📈 Trading symbols: R_100, R_75
🎯 Strategy: multi
```
**What it means:** Bot is starting with Volatility 100 and 75 indices using the multi-strategy approach.

### Connection Status
```
🚀 Starting Deriv Trading Bot...
⚠️  Running in DEMO mode - no real money will be traded
🔗 WebSocket connection opened
✅ Connected to Deriv API
✅ Authorization successful
💰 Balance: $10000.00 USD
🏦 Account: 40704618
```
**What it means:** 
- Bot connected successfully to Deriv
- Running in demo mode (safe)
- Your demo account has $10,000 virtual money
- Account ID is displayed for verification

---

## 📊 **Trading Signals & Execution**

### Signal Detection
```
🎯 Signal: R_100 UP (confidence: 0.75)
💰 Position size: $1.00
```
**What it means:**
- **Signal**: Bot detected a buy signal for Volatility 100
- **Direction**: UP (expecting price to rise)
- **Confidence**: 75% - high confidence trade
- **Position**: $1.00 stake (adjusted for risk)

### Trade Execution
```
✅ Trade placed: 123456789
```
**What it means:** 
- Trade successfully executed
- Contract ID: 123456789 (for tracking)

### Trade Results
```
✅ WIN: $1.80
```
**What it means:**
- Trade was profitable
- Won $1.80 (80% profit on $1 stake)

```
❌ LOSS: -$1.00
```
**What it means:**
- Trade lost money
- Lost $1.00 (full stake)

---

## 📈 **Risk Management Outputs**

### Daily Statistics
```
📊 Trade recorded: R_100 UP $1.00 → $1.80
💰 Daily P&L: $5.00 | Consecutive losses: 0
```
**What it means:**
- Trade details recorded
- Daily profit/loss tracking
- Consecutive loss counter

### Risk Summary
```
📊 RISK SUMMARY:
├── Daily Trades: 5/20
├── Win Rate: 60.0%
├── Daily P&L: $2.50
├── Daily Loss: $5.00/$50.00
├── Consecutive Losses: 1/5
└── Balance: $102.50 (Initial: $100.00)
```
**What it means:**
- **Daily Trades**: 5 trades used out of 20 limit
- **Win Rate**: 60% of trades are profitable
- **Daily P&L**: Net profit/loss for the day
- **Daily Loss**: Current loss vs $50 limit
- **Consecutive Losses**: 1 loss in a row (max 5)
- **Balance**: Current vs initial balance

---

## ⚠️ **Warning & Error Messages**

### Risk Limit Warnings
```
❌ Daily trade limit reached (20)
❌ Daily loss limit reached ($50.00)
❌ Too many consecutive losses (5)
❌ Maximum drawdown reached (20%)
```
**What it means:** Bot stops trading to protect your capital.

### Connection Issues
```
❌ WebSocket error: [error details]
❌ Connection failed: Failed to connect to Deriv API
```
**What it means:** Network or API issues - bot will retry.

### Authorization Issues
```
❌ Authorization failed: [error message]
```
**What it means:** API token or App ID problem.

---

## 🔄 **Trading Loop Messages**

### Normal Operation
```
🔄 Starting trading loop...
```
**What it means:** Bot is actively monitoring markets.

### Pause Messages
```
⏸️  Risk limits reached, pausing trading...
```
**What it means:** Bot paused due to risk limits.

### Strategy Analysis
```
📊 Processing R_100...
📊 Processing R_75...
```
**What it means:** Bot analyzing each symbol for opportunities.

---

## 🎯 **Strategy Confidence Levels**

### High Confidence (0.8-1.0)
```
🎯 Signal: R_100 UP (confidence: 0.85)
💰 Position size: $1.00
```
**What it means:** Strong signal, full position size.

### Medium Confidence (0.6-0.79)
```
🎯 Signal: R_75 DOWN (confidence: 0.65)
💰 Position size: $0.70
```
**What it means:** Moderate signal, reduced position size.

### Low Confidence (0.0-0.59)
```
🎯 Signal: HOLD (confidence: 0.45)
```
**What it means:** No trade - signal too weak.

---

## 📊 **Performance Metrics Explained**

### Win Rate Calculation
```
Win Rate = (Winning Trades / Total Trades) × 100
Example: 6 wins out of 10 trades = 60% win rate
```

### Position Sizing
```
Base Amount: $1.00
Confidence Multiplier: 0.7 (for 70% confidence)
Risk Multiplier: 0.8 (after 2 consecutive losses)
Final Position: $1.00 × 0.7 × 0.8 = $0.56
```

### Daily Loss Tracking
```
Daily Loss = Sum of all losing trades today
Limit: $50.00
Status: $15.00/$50.00 (30% of limit used)
```

---

## 🚨 **Important Status Indicators**

### ✅ **Good Status**
- ✅ Connected to Deriv API
- ✅ Authorization successful
- ✅ Trade placed
- ✅ WIN

### ⚠️ **Warning Status**
- ⚠️ Running in DEMO mode
- ⚠️ Risk limits approaching
- ⚠️ Low confidence signal

### ❌ **Error Status**
- ❌ Connection failed
- ❌ Authorization failed
- ❌ Risk limits reached
- ❌ LOSS

---

## 📈 **What to Monitor**

### Daily Performance
- **Win Rate**: Should be above 50%
- **Daily P&L**: Track profit/loss trends
- **Trade Count**: Monitor activity level

### Risk Management
- **Daily Loss**: Should stay under $50
- **Consecutive Losses**: Should stay under 5
- **Balance**: Should grow over time

### System Health
- **Connection**: Should stay connected
- **Authorization**: Should remain valid
- **Error Rate**: Should be minimal

---

## 🎯 **Expected Performance**

### Good Performance
- Win Rate: 55-70%
- Daily P&L: Positive
- Few consecutive losses
- Growing balance

### Poor Performance
- Win Rate: Below 45%
- Daily P&L: Negative
- Many consecutive losses
- Declining balance

### When to Adjust
- **Lower position sizes** if losing too much
- **Change symbols** if one isn't working
- **Adjust strategy** if win rate is low
- **Check market conditions** if performance drops

---

## 🔧 **Troubleshooting Common Issues**

### Bot Not Trading
- Check if risk limits reached
- Verify market is open
- Check connection status
- Review strategy settings

### Poor Performance
- Review win rate
- Check market conditions
- Consider strategy changes
- Adjust risk parameters

### Connection Issues
- Check internet connection
- Verify API token
- Confirm App ID
- Restart bot if needed

---

## 📞 **Getting Help**

If you see unexpected behavior:
1. **Check this guide** for message meanings
2. **Review the logs** for error details
3. **Verify settings** in `.env` file
4. **Monitor performance** metrics
5. **Adjust parameters** as needed

**Remember:** The bot is designed to be safe and conservative. It prioritizes capital preservation over aggressive profits. 