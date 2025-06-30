import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from .config import DerivConfig

class RiskManager:
    """Risk management system for Deriv trading"""
    
    def __init__(self):
        self.daily_trades = []
        self.daily_loss = 0.0
        self.daily_start = datetime.now().date()
        self.max_consecutive_losses = 5
        self.consecutive_losses = 0
        self.max_drawdown = 0.20  # 20% max drawdown
        self.initial_balance = None
        self.current_balance = None
        
    def reset_daily_stats(self):
        """Reset daily statistics if it's a new day"""
        current_date = datetime.now().date()
        if current_date != self.daily_start:
            self.daily_trades = []
            self.daily_loss = 0.0
            self.daily_start = current_date
            print(f"📅 New trading day started: {current_date}")
    
    def can_trade(self, amount: float) -> bool:
        """Check if we can place a trade based on risk rules"""
        self.reset_daily_stats()
        
        # Check daily trade limit
        if len(self.daily_trades) >= DerivConfig.MAX_DAILY_TRADES:
            print(f"❌ Daily trade limit reached ({DerivConfig.MAX_DAILY_TRADES})")
            return False
        
        # Check daily loss limit
        if self.daily_loss >= DerivConfig.MAX_DAILY_LOSS:
            print(f"❌ Daily loss limit reached (${self.daily_loss:.2f})")
            return False
        
        # Check consecutive losses
        if self.consecutive_losses >= self.max_consecutive_losses:
            print(f"❌ Too many consecutive losses ({self.consecutive_losses})")
            return False
        
        # Check drawdown
        if self.initial_balance and self.current_balance:
            drawdown = (self.initial_balance - self.current_balance) / self.initial_balance
            if drawdown >= self.max_drawdown:
                print(f"❌ Maximum drawdown reached ({drawdown:.2%})")
                return False
        
        # Check if trade amount is reasonable
        if self.current_balance:
            trade_percentage = amount / self.current_balance
            if trade_percentage > 0.05:  # Max 5% per trade
                print(f"❌ Trade amount too high ({trade_percentage:.2%} of balance)")
                return False
        
        return True
    
    def calculate_position_size(self, confidence: float, base_amount: float = None) -> float:
        """Calculate position size based on confidence and risk"""
        if base_amount is None:
            base_amount = DerivConfig.DEFAULT_AMOUNT
        
        # Adjust position size based on confidence
        if confidence >= 0.8:
            size_multiplier = 1.0  # Full position for high confidence
        elif confidence >= 0.6:
            size_multiplier = 0.7  # Reduced position for medium confidence
        else:
            size_multiplier = 0.5  # Small position for low confidence
        
        # Adjust for consecutive losses (reduce position size)
        if self.consecutive_losses > 0:
            loss_multiplier = max(0.3, 1.0 - (self.consecutive_losses * 0.1))
            size_multiplier *= loss_multiplier
        
        # Adjust for daily loss (reduce position size)
        if self.daily_loss > 0:
            daily_loss_ratio = self.daily_loss / DerivConfig.MAX_DAILY_LOSS
            daily_multiplier = max(0.5, 1.0 - daily_loss_ratio)
            size_multiplier *= daily_multiplier
        
        position_size = base_amount * size_multiplier
        
        # Ensure minimum and maximum limits
        position_size = max(1.0, min(position_size, 50.0))
        
        return round(position_size, 2)
    
    def record_trade(self, amount: float, profit_loss: float, symbol: str, direction: str):
        """Record a completed trade"""
        self.reset_daily_stats()
        
        trade_record = {
            'timestamp': datetime.now(),
            'symbol': symbol,
            'direction': direction,
            'amount': amount,
            'profit_loss': profit_loss,
            'balance_after': self.current_balance + profit_loss if self.current_balance else None
        }
        
        self.daily_trades.append(trade_record)
        
        # Update daily loss
        if profit_loss < 0:
            self.daily_loss += abs(profit_loss)
        
        # Update consecutive losses
        if profit_loss < 0:
            self.consecutive_losses += 1
        else:
            self.consecutive_losses = 0
        
        # Update current balance
        if self.current_balance:
            self.current_balance += profit_loss
        
        print(f"📊 Trade recorded: {symbol} {direction} ${amount} → ${profit_loss:.2f}")
        print(f"💰 Daily P&L: ${self.daily_loss:.2f} | Consecutive losses: {self.consecutive_losses}")
    
    def update_balance(self, balance: float):
        """Update current account balance"""
        if self.initial_balance is None:
            self.initial_balance = balance
            print(f"💰 Initial balance set: ${balance:.2f}")
        
        self.current_balance = balance
    
    def get_daily_stats(self) -> Dict:
        """Get daily trading statistics"""
        self.reset_daily_stats()
        
        total_trades = len(self.daily_trades)
        winning_trades = len([t for t in self.daily_trades if t['profit_loss'] > 0])
        losing_trades = len([t for t in self.daily_trades if t['profit_loss'] < 0])
        
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        total_profit = sum(t['profit_loss'] for t in self.daily_trades if t['profit_loss'] > 0)
        total_loss = sum(abs(t['profit_loss']) for t in self.daily_trades if t['profit_loss'] < 0)
        
        return {
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': win_rate,
            'total_profit': total_profit,
            'total_loss': total_loss,
            'net_pnl': total_profit - total_loss,
            'daily_loss': self.daily_loss,
            'consecutive_losses': self.consecutive_losses
        }
    
    def should_stop_trading(self) -> bool:
        """Check if we should stop trading for the day"""
        stats = self.get_daily_stats()
        
        # Stop if win rate is too low
        if stats['total_trades'] >= 5 and stats['win_rate'] < 30:
            print(f"❌ Win rate too low ({stats['win_rate']:.1f}%) - stopping for the day")
            return True
        
        # Stop if daily loss limit reached
        if self.daily_loss >= DerivConfig.MAX_DAILY_LOSS:
            print(f"❌ Daily loss limit reached - stopping for the day")
            return True
        
        # Stop if too many consecutive losses
        if self.consecutive_losses >= self.max_consecutive_losses:
            print(f"❌ Too many consecutive losses - stopping for the day")
            return True
        
        return False
    
    def get_risk_summary(self) -> str:
        """Get a summary of current risk status"""
        stats = self.get_daily_stats()
        
        summary = f"""
📊 RISK SUMMARY:
├── Daily Trades: {stats['total_trades']}/{DerivConfig.MAX_DAILY_TRADES}
├── Win Rate: {stats['win_rate']:.1f}%
├── Daily P&L: ${stats['net_pnl']:.2f}
├── Daily Loss: ${self.daily_loss:.2f}/${DerivConfig.MAX_DAILY_LOSS}
├── Consecutive Losses: {self.consecutive_losses}/{self.max_consecutive_losses}
└── Balance: ${self.current_balance:.2f} (Initial: ${self.initial_balance:.2f})
"""
        return summary 