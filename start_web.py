#!/usr/bin/env python3
"""
Quick Start Script for Web Interface
====================================

This script starts the web interface for the Deriv trading bot.
"""

import os
import socket
import subprocess
import sys

def get_local_ip():
    """Get the local IP address of the computer"""
    try:
        # Connect to a remote address to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "localhost"

def main():
    print("🌐 Deriv Trading Bot - Web Interface")
    print("=" * 50)
    
    # Check if required packages are installed
    try:
        import flask
        print("✅ Flask is installed")
    except ImportError:
        print("❌ Flask not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
        print("✅ Flask installed successfully")
    
    # Get local IP
    local_ip = get_local_ip()
    
    print(f"\n📱 Access from your phone:")
    print(f"   http://{local_ip}:5000")
    print(f"\n💻 Access from your PC:")
    print(f"   http://localhost:5000")
    print(f"\n🔧 Make sure your phone and PC are on the same WiFi network!")
    print(f"\n🚀 Starting web interface...")
    print("=" * 50)
    
    # Start the web interface
    try:
        from web_interface import app
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n🛑 Web interface stopped by user")
    except Exception as e:
        print(f"❌ Error starting web interface: {e}")

if __name__ == "__main__":
    main() 