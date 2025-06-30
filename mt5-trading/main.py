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

class MT5TradingBot:
    """MT5 Trading Bot for Deriv Synthetic Indices"""
    
    def __init__(self, symbols: Optional[List[str]] = None, strategy_type: str = 'multi'):
        # Default symbols - Deriv synthetic indices
        if symbols is None:
            self.symbols = [
                # Popular Deriv Synthetic Indices
                'R_100', 'R_75', 'R_50', 'R_25', 'R_10',
                'VIXBEAR', 'VIXBULL', 'BOOM1000', 'CRASH1000'
            ]
        else:
            self.symbols = symbols
            
        self.strategy_type = strategy_type
        self.connected = False
        self.running = False
        self.active_positions = {}
        self.symbol_performance = {}
        
        # Initialize performance tracking
        for symbol in self.symbols:
            self.symbol_performance[symbol] = {
                'trades': 0,
                'wins': 0,
                'losses': 0,
                'total_pnl': 0.0,
                'last_signal': None,
                'last_signal_time': None
            }
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
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
            
            # Login to Deriv MT5 demo account
            login = 40704618
            password = "Wallet2020!"
            server = "Deriv-Demo"
            
            if not mt5.login(login=login, password=password, server=server):
                print(f"❌ MT5 login failed: {mt5.last_error()}")
                return False
            
            print(f"✅ Logged in to Deriv MT5 account: {login}")
            
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
    
    def calculate_signals(self, df: pd.DataFrame) -> Tuple[str, float]:
        """Calculate trading signals using multiple strategies"""
        if len(df) < 50:
            return "HOLD", 0.0
        
        signals = []
        confidences = []
        
        # Strategy 1: Moving Average Crossover
        if len(df) >= 20:
            short_ma = df['close'].rolling(window=10).mean()
            long_ma = df['close'].rolling(window=20).mean()
            
            if short_ma.iloc[-1] > long_ma.iloc[-1] and short_ma.iloc[-2] <= long_ma.iloc[-2]:
                signals.append("BUY")
                confidences.append(0.7)
            elif short_ma.iloc[-1] < long_ma.iloc[-1] and short_ma.iloc[-2] >= long_ma.iloc[-2]:
                signals.append("SELL")
                confidences.append(0.7)
        
        # Strategy 2: RSI
        if len(df) >= 14:
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            current_rsi = rsi.iloc[-1]
            if current_rsi < 30:
                signals.append("BUY")
                confidences.append(0.8)
            elif current_rsi > 70:
                signals.append("SELL")
                confidences.append(0.8)
        
        # Strategy 3: Bollinger Bands
        if len(df) >= 20:
            sma = df['close'].rolling(window=20).mean()
            std = df['close'].rolling(window=20).std()
            upper_band = sma + (std * 2)
            lower_band = sma - (std * 2)
            
            current_price = df['close'].iloc[-1]
            if current_price <= lower_band.iloc[-1]:
                signals.append("BUY")
                confidences.append(0.6)
            elif current_price >= upper_band.iloc[-1]:
                signals.append("SELL")
                confidences.append(0.6)
        
        # Strategy 4: MACD
        if len(df) >= 26:
            ema12 = df['close'].ewm(span=12).mean()
            ema26 = df['close'].ewm(span=26).mean()
            macd = ema12 - ema26
            signal_line = macd.ewm(span=9).mean()
            
            if macd.iloc[-1] > signal_line.iloc[-1] and macd.iloc[-2] <= signal_line.iloc[-2]:
                signals.append("BUY")
                confidences.append(0.7)
            elif macd.iloc[-1] < signal_line.iloc[-1] and macd.iloc[-2] >= signal_line.iloc[-2]:
                signals.append("SELL")
                confidences.append(0.7)
        
        # Combine signals
        if not signals:
            return "HOLD", 0.0
        
        # Count signals
        buy_count = signals.count("BUY")
        sell_count = signals.count("SELL")
        
        # Calculate average confidence
        avg_confidence = np.mean(confidences)
        
        # Determine final signal
        if buy_count > sell_count and buy_count >= 2:
            return "BUY", avg_confidence
        elif sell_count > buy_count and sell_count >= 2:
            return "SELL", avg_confidence
        else:
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
            df = self.get_historical_data(symbol, 'M5', 100)
            if df.empty:
                return
            
            # Calculate signals
            signal, confidence = self.calculate_signals(df)
            
            # Update performance tracking
            self.symbol_performance[symbol]['last_signal'] = signal
            self.symbol_performance[symbol]['last_signal_time'] = datetime.now()
            
            # Debug output
            if signal != "HOLD":
                print(f"🔍 Signal detected: {symbol} {signal} (confidence: {confidence:.2f})")
            
            # Execute trades
            if signal != "HOLD" and confidence > 0.6:
                print(f"🎯 Executing trade: {symbol} {signal} (confidence: {confidence:.2f})")
                
                # Calculate position size (0.01 lot = $1 risk)
                position_size = 0.01  # Start with minimum lot size
                
                # Get current price
                tick = mt5.symbol_info_tick(symbol)
                if not tick:
                    print(f"❌ No price data for {symbol}")
                    return
                
                current_price = tick.ask if signal == "BUY" else tick.bid
                
                # Place order
                if self.place_order(symbol, signal, position_size, current_price):
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
                
                # Wait before next iteration
                print("⏳ Waiting 60 seconds before next iteration...")
                time.sleep(60)
                
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