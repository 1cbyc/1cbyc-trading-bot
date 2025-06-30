import time
import json
import signal
import sys
from datetime import datetime
from typing import Dict, List, Optional

from .api_client import DerivAPIClient
from .strategies import MultiStrategy, MovingAverageCrossover, RSIStrategy
from .risk_manager import RiskManager
from .config import DerivConfig

class DerivTradingBot:
    """Main trading bot for Deriv synthetic indices"""
    
    def __init__(self, symbols: List[str] = None, strategy_type: str = 'multi'):
        self.symbols = symbols or ['R_100']  # Default to Volatility 100
        self.strategy_type = strategy_type
        self.api_client = DerivAPIClient()
        self.risk_manager = RiskManager()
        self.strategies = {}
        self.running = False
        self.active_contracts = {}
        
        # Initialize strategies for each symbol
        for symbol in self.symbols:
            if strategy_type == 'multi':
                self.strategies[symbol] = MultiStrategy(symbol)
            elif strategy_type == 'ma':
                self.strategies[symbol] = MovingAverageCrossover(symbol)
            elif strategy_type == 'rsi':
                self.strategies[symbol] = RSIStrategy(symbol)
            else:
                self.strategies[symbol] = MultiStrategy(symbol)
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\n🛑 Received signal {signum}, shutting down gracefully...")
        self.stop()
        sys.exit(0)
    
    def start(self):
        """Start the trading bot"""
        print("🚀 Starting Deriv Trading Bot...")
        print(f"📈 Trading symbols: {', '.join(self.symbols)}")
        print(f"🎯 Strategy: {self.strategy_type}")
        
        # Validate configuration
        try:
            DerivConfig.validate_config()
        except ValueError as e:
            print(f"❌ Configuration error: {e}")
            return False
        
        # Connect to API
        if not self.api_client.connect():
            print("❌ Failed to connect to Deriv API")
            return False
        
        # Wait for authorization
        time.sleep(2)
        
        # Get initial balance
        self._get_balance()
        
        # Start trading
        self.running = True
        print("✅ Trading bot started successfully!")
        
        try:
            self._trading_loop()
        except KeyboardInterrupt:
            print("\n🛑 Trading interrupted by user")
        except Exception as e:
            print(f"❌ Trading error: {e}")
        finally:
            self.stop()
        
        return True
    
    def stop(self):
        """Stop the trading bot"""
        self.running = False
        self.api_client.disconnect()
        print("🛑 Trading bot stopped")
    
    def _get_balance(self):
        """Get and update account balance"""
        def balance_callback(data):
            if 'error' not in data:
                balance = float(data.get('get_settings', {}).get('balance', 0))
                self.risk_manager.update_balance(balance)
                print(f"💰 Current balance: ${balance:.2f}")
        
        self.api_client.get_balance(balance_callback)
        time.sleep(1)
    
    def _trading_loop(self):
        """Main trading loop"""
        print("🔄 Starting trading loop...")
        
        while self.running:
            try:
                # Check if we should stop trading
                if self.risk_manager.should_stop_trading():
                    print("⏸️  Risk limits reached, pausing trading...")
                    time.sleep(60)  # Wait 1 minute before checking again
                    continue
                
                # Process each symbol
                for symbol in self.symbols:
                    if not self.running:
                        break
                    
                    self._process_symbol(symbol)
                
                # Wait before next iteration
                time.sleep(5)
                
            except Exception as e:
                print(f"❌ Error in trading loop: {e}")
                time.sleep(10)
    
    def _process_symbol(self, symbol: str):
        """Process a single symbol for trading opportunities"""
        try:
            # Get historical data for analysis
            def candles_callback(data):
                if 'error' not in data and 'candles' in data:
                    candles = data['candles']
                    strategy = self.strategies[symbol]
                    
                    # Add candles to strategy
                    for candle in candles:
                        strategy.add_candle(candle)
                    
                    # Get trading signal
                    signal, confidence = strategy.get_signal()
                    
                    # Debug output
                    if signal != "HOLD":
                        print(f"🔍 Signal detected: {symbol} {signal} (confidence: {confidence:.2f})")
                    
                    # Original conservative threshold (commented out)
                    # if signal != "HOLD" and confidence > 0.6:
                    #     self._execute_trade(symbol, signal, confidence)
                    
                    # More aggressive threshold for faster trading
                    if signal != "HOLD" and confidence > 0.4:
                        self._execute_trade(symbol, signal, confidence)
            
            # Get recent candles (last 100)
            self.api_client.get_candles(symbol, 60, 100, candles_callback)
            
        except Exception as e:
            print(f"❌ Error processing {symbol}: {e}")
    
    def _execute_trade(self, symbol: str, direction: str, confidence: float):
        """Execute a trade based on signal"""
        try:
            # Calculate position size
            position_size = self.risk_manager.calculate_position_size(confidence)
            
            # Check if we can trade
            if not self.risk_manager.can_trade(position_size):
                return
            
            print(f"🎯 Signal: {symbol} {direction} (confidence: {confidence:.2f})")
            print(f"💰 Position size: ${position_size}")
            
            # Place the trade
            def trade_callback(data):
                if 'error' not in data and 'buy' in data:
                    contract_id = data['buy']['contract_id']
                    self.active_contracts[contract_id] = {
                        'symbol': symbol,
                        'direction': direction,
                        'amount': position_size,
                        'timestamp': datetime.now(),
                        'confidence': confidence
                    }
                    print(f"✅ Trade placed: {contract_id}")
                    
                    # Monitor the contract
                    self._monitor_contract(contract_id)
                else:
                    error_msg = data.get('error', {}).get('message', 'Unknown error')
                    print(f"❌ Trade failed: {error_msg}")
            
            # Buy contract (5 ticks duration)
            self.api_client.buy_contract(symbol, position_size, direction, 5, trade_callback)
            
        except Exception as e:
            print(f"❌ Error executing trade: {e}")
    
    def _monitor_contract(self, contract_id: str):
        """Monitor a contract for completion"""
        def contract_callback(data):
            if 'error' not in data and 'proposal_open_contract' in data:
                contract = data['proposal_open_contract']
                
                if contract.get('is_sold'):
                    # Contract completed
                    profit_loss = float(contract.get('profit', 0))
                    contract_info = self.active_contracts.pop(contract_id, {})
                    
                    # Record the trade
                    self.risk_manager.record_trade(
                        contract_info.get('amount', 0),
                        profit_loss,
                        contract_info.get('symbol', ''),
                        contract_info.get('direction', '')
                    )
                    
                    # Update balance
                    self._get_balance()
                    
                    # Print result
                    result = "✅ WIN" if profit_loss > 0 else "❌ LOSS"
                    print(f"{result}: ${profit_loss:.2f}")
                    
                    # Print risk summary
                    print(self.risk_manager.get_risk_summary())
        
        # Check contract status every few seconds
        def check_contract():
            time.sleep(2)
            if contract_id in self.active_contracts:
                self.api_client.send_request({
                    "proposal_open_contract": 1,
                    "contract_id": contract_id,
                    "subscribe": 1
                }, contract_callback)
        
        # Start monitoring in background
        import threading
        monitor_thread = threading.Thread(target=check_contract)
        monitor_thread.daemon = True
        monitor_thread.start()

def main():
    """Main entry point"""
    print("🎯 Deriv Synthetic Indices Trading Bot")
    print("=" * 50)
    
    # Configuration
    symbols = ['R_100', 'R_75']  # Volatility indices
    strategy = 'multi'  # multi, ma, rsi
    
    # Create and start bot
    bot = DerivTradingBot(symbols=symbols, strategy_type=strategy)
    bot.start()

if __name__ == "__main__":
    main() 