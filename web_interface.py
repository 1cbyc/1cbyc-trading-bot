#!/usr/bin/env python3
"""
Web Interface for Deriv Trading Bot
===================================

A Flask web application to monitor and control the trading bot from any device.
"""

from flask import Flask, render_template, jsonify, request, redirect, url_for
import threading
import time
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Import the trading bot
from deriv_trading.main import DerivTradingBot

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Global variables
bot = None
bot_thread = None
bot_status = "stopped"
bot_stats = {}
bot_errors = []

class WebBotManager:
    """Manages the trading bot for web interface"""
    
    def __init__(self):
        self.bot = None
        self.bot_thread = None
        self.status = "stopped"
        self.stats = {}
        self.errors = []
        self.last_update = datetime.now()
        
    def start_bot(self, symbols=None, strategy='multi'):
        """Start the trading bot in a separate thread"""
        if self.status == "running":
            return False, "Bot is already running"
        
        try:
            # Create bot instance
            self.bot = DerivTradingBot(symbols=symbols, strategy_type=strategy)
            self.status = "starting"
            
            # Start bot in separate thread
            self.bot_thread = threading.Thread(target=self._run_bot)
            self.bot_thread.daemon = True
            self.bot_thread.start()
            
            return True, "Bot started successfully"
            
        except Exception as e:
            self.errors.append(f"Failed to start bot: {str(e)}")
            self.status = "error"
            return False, str(e)
    
    def stop_bot(self):
        """Stop the trading bot"""
        if self.bot:
            self.bot.stop()
            self.status = "stopping"
            return True, "Bot stopping..."
        return False, "No bot running"
    
    def _run_bot(self):
        """Run the bot (called in separate thread)"""
        try:
            self.status = "running"
            self.bot.start()
        except Exception as e:
            self.errors.append(f"Bot error: {str(e)}")
            self.status = "error"
        finally:
            self.status = "stopped"
    
    def get_status(self):
        """Get current bot status"""
        if self.bot and hasattr(self.bot, 'symbol_performance'):
            self.stats = {
                'symbols': list(self.bot.symbol_performance.keys()),
                'performance': self.bot.symbol_performance,
                'risk_stats': self.bot.risk_manager.get_daily_stats() if self.bot.risk_manager else {},
                'active_contracts': len(self.bot.active_contracts) if hasattr(self.bot, 'active_contracts') else 0
            }
        
        return {
            'status': self.status,
            'stats': self.stats,
            'errors': self.errors[-5:],  # Last 5 errors
            'last_update': self.last_update.strftime('%Y-%m-%d %H:%M:%S')
        }

# Create bot manager instance
bot_manager = WebBotManager()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/status')
def get_status():
    """API endpoint to get bot status"""
    return jsonify(bot_manager.get_status())

@app.route('/api/start', methods=['POST'])
def start_bot():
    """API endpoint to start the bot"""
    data = request.get_json() or {}
    symbols = data.get('symbols', None)
    strategy = data.get('strategy', 'multi')
    
    success, message = bot_manager.start_bot(symbols, strategy)
    return jsonify({'success': success, 'message': message})

@app.route('/api/stop', methods=['POST'])
def stop_bot():
    """API endpoint to stop the bot"""
    success, message = bot_manager.stop_bot()
    return jsonify({'success': success, 'message': message})

@app.route('/api/config')
def get_config():
    """Get current configuration"""
    return jsonify({
        'symbols': [
            'R_10', 'R_25', 'R_50', 'R_75', 'R_100', 'R_150', 'R_200',
            'BOOM1000', 'CRASH1000', 'BOOM500', 'CRASH500',
            'STEP_INDEX', 'BEAR_INDEX', 'BULL_INDEX',
            'R_10_1HZ10V', 'R_25_1HZ10V', 'R_50_1HZ10V', 'R_75_1HZ10V', 'R_100_1HZ10V',
            'R_BEAR', 'R_BULL', 'R_BEAR_1HZ10V', 'R_BULL_1HZ10V'
        ],
        'strategies': ['multi', 'ma', 'rsi', 'bb', 'vb', 'macd', 'stoch', 'williams', 'sar', 'ichimoku', 'momentum']
    })

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Create the HTML template
    create_html_template()
    
    print("🌐 Starting Web Interface...")
    print("📱 Access from your phone at: http://[YOUR_PC_IP]:5000")
    print("💻 Access from your PC at: http://localhost:5000")
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=False)

def create_html_template():
    """Create the HTML template for the web interface"""
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Deriv Trading Bot - Web Interface</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2rem;
            margin-bottom: 10px;
        }
        
        .header p {
            opacity: 0.9;
            font-size: 1.1rem;
        }
        
        .content {
            padding: 30px;
        }
        
        .status-card {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 25px;
            border-left: 5px solid #007bff;
        }
        
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 10px;
        }
        
        .status-running { background: #28a745; }
        .status-stopped { background: #dc3545; }
        .status-starting { background: #ffc107; }
        .status-stopping { background: #fd7e14; }
        .status-error { background: #dc3545; }
        
        .controls {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 25px;
        }
        
        .btn {
            padding: 15px 25px;
            border: none;
            border-radius: 10px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .btn-primary {
            background: #007bff;
            color: white;
        }
        
        .btn-primary:hover {
            background: #0056b3;
            transform: translateY(-2px);
        }
        
        .btn-danger {
            background: #dc3545;
            color: white;
        }
        
        .btn-danger:hover {
            background: #c82333;
            transform: translateY(-2px);
        }
        
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 25px;
        }
        
        .stat-card {
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 2rem;
            font-weight: bold;
            color: #007bff;
            margin-bottom: 5px;
        }
        
        .stat-label {
            color: #6c757d;
            font-size: 0.9rem;
        }
        
        .performance-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        
        .performance-table th,
        .performance-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e9ecef;
        }
        
        .performance-table th {
            background: #f8f9fa;
            font-weight: 600;
        }
        
        .error-log {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            border-radius: 10px;
            padding: 15px;
            margin-top: 20px;
        }
        
        .error-log h3 {
            color: #721c24;
            margin-bottom: 10px;
        }
        
        .error-item {
            color: #721c24;
            margin-bottom: 5px;
            font-size: 0.9rem;
        }
        
        .refresh-btn {
            background: #6c757d;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin-bottom: 20px;
        }
        
        @media (max-width: 768px) {
            .controls {
                grid-template-columns: 1fr;
            }
            
            .stats-grid {
                grid-template-columns: 1fr;
            }
            
            .header h1 {
                font-size: 1.5rem;
            }
            
            .content {
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Deriv Trading Bot</h1>
            <p>Web Interface - Monitor & Control</p>
        </div>
        
        <div class="content">
            <div class="status-card">
                <h2>
                    <span id="status-indicator" class="status-indicator status-stopped"></span>
                    Bot Status: <span id="status-text">Stopped</span>
                </h2>
                <p>Last Update: <span id="last-update">Never</span></p>
            </div>
            
            <div class="controls">
                <button id="start-btn" class="btn btn-primary" onclick="startBot()">Start Bot</button>
                <button id="stop-btn" class="btn btn-danger" onclick="stopBot()" disabled>Stop Bot</button>
            </div>
            
            <button class="refresh-btn" onclick="refreshStatus()">🔄 Refresh Status</button>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value" id="total-trades">0</div>
                    <div class="stat-label">Total Trades</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="win-rate">0%</div>
                    <div class="stat-label">Win Rate</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="daily-pnl">$0.00</div>
                    <div class="stat-label">Daily P&L</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="active-contracts">0</div>
                    <div class="stat-label">Active Contracts</div>
                </div>
            </div>
            
            <div id="performance-section" style="display: none;">
                <h3>📊 Instrument Performance</h3>
                <table class="performance-table" id="performance-table">
                    <thead>
                        <tr>
                            <th>Instrument</th>
                            <th>Trades</th>
                            <th>Win Rate</th>
                            <th>P&L</th>
                        </tr>
                    </thead>
                    <tbody id="performance-body">
                    </tbody>
                </table>
            </div>
            
            <div id="error-section" style="display: none;">
                <div class="error-log">
                    <h3>⚠️ Recent Errors</h3>
                    <div id="error-list"></div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let statusInterval;
        
        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            refreshStatus();
            statusInterval = setInterval(refreshStatus, 5000); // Refresh every 5 seconds
        });
        
        async function refreshStatus() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                updateUI(data);
            } catch (error) {
                console.error('Error fetching status:', error);
            }
        }
        
        function updateUI(data) {
            // Update status
            const statusText = document.getElementById('status-text');
            const statusIndicator = document.getElementById('status-indicator');
            const lastUpdate = document.getElementById('last-update');
            
            statusText.textContent = data.status.charAt(0).toUpperCase() + data.status.slice(1);
            statusIndicator.className = `status-indicator status-${data.status}`;
            lastUpdate.textContent = data.last_update;
            
            // Update buttons
            const startBtn = document.getElementById('start-btn');
            const stopBtn = document.getElementById('stop-btn');
            
            if (data.status === 'running') {
                startBtn.disabled = true;
                stopBtn.disabled = false;
            } else {
                startBtn.disabled = false;
                stopBtn.disabled = true;
            }
            
            // Update stats
            if (data.stats && data.stats.risk_stats) {
                const stats = data.stats.risk_stats;
                document.getElementById('total-trades').textContent = stats.total_trades || 0;
                document.getElementById('win-rate').textContent = (stats.win_rate || 0).toFixed(1) + '%';
                document.getElementById('daily-pnl').textContent = '$' + (stats.net_pnl || 0).toFixed(2);
                document.getElementById('active-contracts').textContent = data.stats.active_contracts || 0;
            }
            
            // Update performance table
            if (data.stats && data.stats.performance) {
                updatePerformanceTable(data.stats.performance);
            }
            
            // Update errors
            if (data.errors && data.errors.length > 0) {
                updateErrorList(data.errors);
            }
        }
        
        function updatePerformanceTable(performance) {
            const tableBody = document.getElementById('performance-body');
            const section = document.getElementById('performance-section');
            
            tableBody.innerHTML = '';
            
            Object.entries(performance).forEach(([symbol, data]) => {
                if (data.trades > 0) {
                    const row = document.createElement('tr');
                    const winRate = data.trades > 0 ? (data.wins / data.trades * 100) : 0;
                    
                    row.innerHTML = `
                        <td><strong>${symbol}</strong></td>
                        <td>${data.trades}</td>
                        <td>${winRate.toFixed(1)}%</td>
                        <td>$${data.total_pnl.toFixed(2)}</td>
                    `;
                    tableBody.appendChild(row);
                }
            });
            
            section.style.display = tableBody.children.length > 0 ? 'block' : 'none';
        }
        
        function updateErrorList(errors) {
            const errorList = document.getElementById('error-list');
            const section = document.getElementById('error-section');
            
            errorList.innerHTML = '';
            errors.forEach(error => {
                const div = document.createElement('div');
                div.className = 'error-item';
                div.textContent = error;
                errorList.appendChild(div);
            });
            
            section.style.display = errors.length > 0 ? 'block' : 'none';
        }
        
        async function startBot() {
            try {
                const response = await fetch('/api/start', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        strategy: 'multi'
                    })
                });
                
                const data = await response.json();
                if (data.success) {
                    alert('Bot started successfully!');
                    refreshStatus();
                } else {
                    alert('Failed to start bot: ' + data.message);
                }
            } catch (error) {
                alert('Error starting bot: ' + error.message);
            }
        }
        
        async function stopBot() {
            if (confirm('Are you sure you want to stop the bot?')) {
                try {
                    const response = await fetch('/api/stop', {
                        method: 'POST'
                    });
                    
                    const data = await response.json();
                    if (data.success) {
                        alert('Bot stopping...');
                        refreshStatus();
                    } else {
                        alert('Failed to stop bot: ' + data.message);
                    }
                } catch (error) {
                    alert('Error stopping bot: ' + error.message);
                }
            }
        }
    </script>
</body>
</html>'''
    
    with open('templates/dashboard.html', 'w') as f:
        f.write(html_content) 