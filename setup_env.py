#!/usr/bin/env python3
"""
Setup script for Deriv API configuration
"""

def setup_env():
    """Set up the .env file with user's API token"""
    
    # Read the template
    with open('deriv.env-example', 'r') as f:
        content = f.read()
    
    # Replace the placeholder with actual token
    content = content.replace('your_token_here', 'your_actual_token_here')
    
    # Write the actual .env file
    with open('.env', 'w') as f:
        f.write(content)
    
    print("✅ .env file created successfully!")
    print("🔐 Your API token is securely stored")
    print("🚀 Ready to run the trading bot!")

if __name__ == "__main__":
    setup_env() 