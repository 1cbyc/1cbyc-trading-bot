import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import time
import signal
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import os
from dotenv import load_dotenv

# Import our custom modules
from config import MT5Config
from strategies_mt5 import (
    SyntheticTradingStrategy, MovingAverageCrossover, RSIStrategy, 
    BollingerBandsStrategy, VolatilityBreakoutStrategy, MACDStrategy,
    StochasticStrategy, WilliamsRStrategy, ParabolicSARStrategy,
    IchimokuStrategy, MomentumStrategy, MeanReversionStrategy,
    TrendFollowingStrategy, AdvancedVolatilityStrategy, SupportResistanceStrategy,
    DivergenceStrategy, VolumePriceStrategy, FibonacciRetracementStrategy,
    AdaptiveStrategy, ElliottWaveStrategy, HarmonicPatternStrategy,
    OrderFlowStrategy, MarketMicrostructureStrategy, SentimentAnalysisStrategy,
    MomentumDivergenceStrategy, VolatilityRegimeStrategy, PriceActionStrategy,
    CorrelationStrategy, MachineLearningInspiredStrategy, MultiStrategy
)

class MT5TradingBot:
    """MT5 Trading Bot for Deriv Synthetic Indices with Advanced Strategies"""
    
    def __init__(self, symbols: Optional[List[str]] = None, strategy_type: str = 'multi'):
        # Use configuration for symbols and strategy
        if symbols is None:
            self.symbols = MT5Config.get_symbols_from_env()
        else:
            self.symbols = symbols
            
        self.strategy_type = strategy_type
        self.connected = False
        self.running = False
        self.active_positions = {}
        self.symbol_performance = {}
        self.strategies = {}
        
        # Initialize strategies for each symbol
        self._initialize_strategies()
        
        # Initialize performance tracking
        for symbol in self.symbols:
            self.symbol_performance[symbol] = {
                'trades': 0,
                'wins': 0,
                'losses': 0,
                'total_pnl': 0.0,
                'last_signal': None,
                'last_signal_time': None,
                'last_confidence': 0.0
            }
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _initialize_strategies(self):
        """Initialize strategies for each symbol"""
        strategy_class_name = MT5Config.get_strategy_class(self.strategy_type)
        
        for symbol in self.symbols:
            try:
                # Get the strategy class dynamically
                strategy_class = globals()[strategy_class_name]
                self.strategies[symbol] = strategy_class(symbol, MT5Config.TIMEFRAME)
                print(f"✅ Initialized {strategy_class_name} for {symbol}")
            except Exception as e:
                print(f"❌ Failed to initialize strategy for {symbol}: {e}")
                # Fallback to MultiStrategy
                self.strategies[symbol] = MultiStrategy(symbol, MT5Config.TIMEFRAME)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\n🛑 Received signal {signum}, shutting down gracefully...")
        self.stop()
        sys.exit(0)
    
    def connect(self):
        """Connect to Deriv MT5"""
        try:
            # Initialize MT5
            if not mt5.initialize():
                print(f"❌ MT5 initialization failed: {mt5.last_error()}")
                return False
            
            # Login to Deriv MT5 demo account using config
            if not mt5.login(login=MT5Config.MT5_LOGIN, password=MT5Config.MT5_PASSWORD, server=MT5Config.MT5_SERVER):
                print(f"❌ MT5 login failed: {mt5.last_error()}")
                return False
            
            print(f"✅ Logged in to Deriv MT5 account: {MT5Config.MT5_LOGIN}")
            
            # Get account info
            account_info = mt5.account_info()
            if account_info:
                print(f"💰 Balance: ${account_info.balance:.2f}")
                print(f"💳 Equity: ${account_info.equity:.2f}")
                print(f"🏦 Account: {account_info.login}")
                print(f"🏢 Broker: {account_info.company}")
            
            self.connected = True
            print("✅ Connected to Deriv MT5 successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from MT5"""
        if self.connected:
            mt5.shutdown()
            self.connected = False
            print("🔌 Disconnected from MT5")
    
    def get_historical_data(self, symbol: str, timeframe: str = 'M5', count: int = 100) -> pd.DataFrame:
        """Get historical data for a symbol"""
        try:
            # Convert timeframe string to MT5 timeframe
            tf_map = {
                'M1': mt5.TIMEFRAME_M1,
                'M5': mt5.TIMEFRAME_M5,
                'M15': mt5.TIMEFRAME_M15,
                'M30': mt5.TIMEFRAME_M30,
                'H1': mt5.TIMEFRAME_H1,
                'H4': mt5.TIMEFRAME_H4,
                'D1': mt5.TIMEFRAME_D1
            }
            
            mt5_timeframe = tf_map.get(timeframe, mt5.TIMEFRAME_M5)
            
            # Get rates
            rates = mt5.copy_rates_from_pos(symbol, mt5_timeframe, 0, count)
            
            if rates is None or len(rates) == 0:
                print(f"⚠️  No data received for {symbol}")
                return pd.DataFrame()
            
            # Convert to DataFrame
            df = pd.DataFrame(rates)
            df['time'] = pd.to_datetime(df['time'], unit='s')
            df.set_index('time', inplace=True)
            
            return df
            
        except Exception as e:
            print(f"❌ Error getting data for {symbol}: {e}")
            return pd.DataFrame()
    
    def calculate_signals(self, symbol: str, df: pd.DataFrame) -> Tuple[str, float]:
        """Calculate trading signals using the selected strategy"""
        if len(df) < 50:
            return "HOLD", 0.0
        
        try:
            # Update strategy data
            strategy = self.strategies.get(symbol)
            if strategy is None:
                print(f"❌ No strategy found for {symbol}")
                return "HOLD", 0.0
            
            strategy.update_data(df)
            
            # Get signal from strategy
            signal, confidence = strategy.get_signal()
            
            # Apply strategy weight
            strategy_weight = MT5Config.get_strategy_weight(strategy.__class__.__name__)
            adjusted_confidence = confidence * strategy_weight
            
            # Debug output
            if signal != "HOLD":
                print(f"🎯 {symbol} - {strategy.__class__.__name__}: {signal} (confidence: {adjusted_confidence:.2f})")
            
            return signal, adjusted_confidence
            
        except Exception as e:
            print(f"❌ Error calculating signals for {symbol}: {e}")
            return "HOLD", 0.0
    
    def place_order(self, symbol: str, order_type: str, volume: float, 
                   price: float = 0.0, sl: float = 0.0, tp: float = 0.0) -> bool:
        """Place an order on MT5"""
        try:
            # Prepare the request
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": volume,
                "type": mt5.ORDER_TYPE_BUY if order_type == "BUY" else mt5.ORDER_TYPE_SELL,
                "price": price,
                "deviation": 20,
                "magic": 234000,
                "comment": f"python-mt5-bot-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            
            # Add stop loss and take profit if provided
            if sl > 0:
                request["sl"] = sl
            if tp > 0:
                request["tp"] = tp
            
            # Send the order
            result = mt5.order_send(request)
            
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                print(f"❌ Order failed for {symbol}: {result.comment}")
                return False
            
            print(f"✅ Order placed: {symbol} {order_type} {volume} lots at {result.price}")
            
            # Store position info
            self.active_positions[result.order] = {
                'symbol': symbol,
                'type': order_type,
                'volume': volume,
                'price': result.price,
                'time': datetime.now()
            }
            
            return True
            
        except Exception as e:
            print(f"❌ Error placing order for {symbol}: {e}")
            return False
    
    def close_position(self, ticket: int) -> bool:
        """Close a position by ticket"""
        try:
            position = mt5.positions_get(ticket=ticket)
            if not position:
                print(f"❌ Position {ticket} not found")
                return False
            
            pos = position[0]
            
            # Prepare close request
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": pos.symbol,
                "volume": pos.volume,
                "type": mt5.ORDER_TYPE_SELL if pos.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY,
                "position": ticket,
                "price": mt5.symbol_info_tick(pos.symbol).bid if pos.type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(pos.symbol).ask,
                "deviation": 20,
                "magic": 234000,
                "comment": f"python-mt5-bot-close-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            
            result = mt5.order_send(request)
            
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                print(f"❌ Failed to close position {ticket}: {result.comment}")
                return False
            
            print(f"✅ Position closed: {ticket} - Profit: ${result.profit:.2f}")
            
            # Remove from active positions
            if ticket in self.active_positions:
                del self.active_positions[ticket]
            
            return True
            
        except Exception as e:
            print(f"❌ Error closing position {ticket}: {e}")
            return False
    
    def process_symbol(self, symbol: str):
        """Process a single symbol for trading opportunities"""
        try:
            print(f"📊 Processing {symbol}...")
            
            # Get historical data
            df = self.get_historical_data(symbol, MT5Config.TIMEFRAME, MT5Config.DATA_LOOKBACK)
            if df.empty:
                return
            
            # Calculate signals
            signal, confidence = self.calculate_signals(symbol, df)
            
            # Update performance tracking
            self.symbol_performance[symbol]['last_signal'] = signal
            self.symbol_performance[symbol]['last_signal_time'] = datetime.now()
            self.symbol_performance[symbol]['last_confidence'] = confidence
            
            # Debug output
            if signal != "HOLD":
                print(f"🔍 Signal detected: {symbol} {signal} (confidence: {confidence:.2f})")
            
            # Execute trades using config threshold
            if signal != "HOLD" and confidence > MT5Config.CONFIDENCE_THRESHOLD:
                print(f"🎯 Executing trade: {symbol} {signal} (confidence: {confidence:.2f})")
                
                # Use the correct minimum volume for this symbol
                position_size = MT5Config.get_min_volume(symbol)
                print(f"Using position size (min volume) for {symbol}: {position_size}")
                
                # Get current price
                tick = mt5.symbol_info_tick(symbol)
                if not tick:
                    print(f"❌ No price data for {symbol}")
                    return
                
                current_price = tick.ask if signal == "BUY" else tick.bid
                
                # Calculate stop loss and take profit
                sl = 0.0
                tp = 0.0
                if MT5Config.STOP_LOSS_PERCENT > 0:
                    sl = current_price * (1 - MT5Config.STOP_LOSS_PERCENT/100) if signal == "BUY" else current_price * (1 + MT5Config.STOP_LOSS_PERCENT/100)
                if MT5Config.TAKE_PROFIT_PERCENT > 0:
                    tp = current_price * (1 + MT5Config.TAKE_PROFIT_PERCENT/100) if signal == "BUY" else current_price * (1 - MT5Config.TAKE_PROFIT_PERCENT/100)
                
                # Place order
                if self.place_order(symbol, signal, position_size, current_price, sl, tp):
                    self.symbol_performance[symbol]['trades'] += 1
                    print(f"✅ Trade placed for {symbol}")
                else:
                    print(f"❌ Failed to place trade for {symbol}")
            
        except Exception as e:
            print(f"❌ Error processing {symbol}: {e}")
    
    def trading_loop(self):
        """Main trading loop"""
        print("🔄 Starting MT5 trading loop...")
        
        while self.running:
            try:
                print(f"🔄 Processing {len(self.symbols)} symbols...")
                
                # Process each symbol
                for i, symbol in enumerate(self.symbols):
                    if not self.running:
                        break
                    
                    self.process_symbol(symbol)
                    
                    # Small delay between symbols
                    if i < len(self.symbols) - 1:
                        time.sleep(1)
                
                # Wait before next iteration using config
                print(f"⏳ Waiting {MT5Config.TRADING_INTERVAL} seconds before next iteration...")
                time.sleep(MT5Config.TRADING_INTERVAL)
                
            except Exception as e:
                print(f"❌ Error in trading loop: {e}")
                time.sleep(10)
    
    def start(self):
        """Start the trading bot"""
        print("🚀 Starting MT5 Trading Bot...")
        print(f"📈 Trading symbols: {', '.join(self.symbols)}")
        print(f"🎯 Strategy: {self.strategy_type}")
        print(f"📊 Total instruments: {len(self.symbols)}")
        
        # Connect to MT5
        if not self.connect():
            print("❌ Failed to connect to MT5")
            return False
        
        # Start trading
        self.running = True
        print("✅ MT5 Trading bot started successfully!")
        
        try:
            self.trading_loop()
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
        self.disconnect()
        print("🛑 MT5 Trading bot stopped")
        self._print_final_statistics()
    
    def _print_final_statistics(self):
        """Print final trading statistics"""
        print("\n📊 FINAL TRADING STATISTICS:")
        print("=" * 50)
        
        total_trades = 0
        total_wins = 0
        total_losses = 0
        total_pnl = 0.0
        
        for symbol, perf in self.symbol_performance.items():
            if perf['trades'] > 0:
                win_rate = (perf['wins'] / perf['trades'] * 100) if perf['trades'] > 0 else 0
                print(f"{symbol}:")
                print(f"  Trades: {perf['trades']}")
                print(f"  Win Rate: {win_rate:.1f}%")
                print(f"  P&L: ${perf['total_pnl']:.2f}")
                print()
                
                total_trades += perf['trades']
                total_wins += perf['wins']
                total_losses += perf['losses']
                total_pnl += perf['total_pnl']
        
        if total_trades > 0:
            overall_win_rate = (total_wins / total_trades * 100)
            print(f"OVERALL:")
            print(f"  Total Trades: {total_trades}")
            print(f"  Win Rate: {overall_win_rate:.1f}%")
            print(f"  Total P&L: ${total_pnl:.2f}")

def main():
    """Main entry point"""
    # You can customize which symbols to trade
    # symbols = ['EURUSD', 'GBPUSD', 'USDJPY']  # Example: trade only specific ones
    
    bot = MT5TradingBot()  # Will trade all major forex pairs and indices
    bot.start()

if __name__ == "__main__":
    main() 