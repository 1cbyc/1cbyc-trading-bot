#!/usr/bin/env python3
"""
Create a clean .env file for Deriv API
"""

def create_env():
    """Create a clean .env file"""
    
    env_content = """# Deriv API Configuration
# =======================

# Your Deriv API token (get from https://app.deriv.com/account/api-token)
DERIV_ACCOUNT_TOKEN=Ryw1syisun35psn

# Demo or Live account (true for demo, false for live)
DERIV_IS_DEMO=true

# Default trade amount in USD
DERIV_DEFAULT_AMOUNT=1.00

# Currency for trading
DERIV_CURRENCY=USD

# Risk Management
# ===============

# Maximum daily loss in USD
DERIV_MAX_DAILY_LOSS=50.00

# Maximum number of trades per day
DERIV_MAX_DAILY_TRADES=20

# App ID (usually 1089 for demo, 36544 for live)
DERIV_APP_ID=82871
"""
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✅ Clean .env file created successfully!")
    print("🔐 Your API token and App ID are securely stored")

if __name__ == "__main__":
    create_env() 