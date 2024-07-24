# 1cbyc Trading Bot - For Stocks (v1 Release Notes)

## Overview

Welcome to the **1cbyc Trading Bot**, your go-to solution for automated stock trading. Designed with both novice and experienced traders in mind, this bot leverages powerful algorithms to trade stocks efficiently and effectively. Whether you're interested in cutting-edge AI companies or robust real estate stocks, 1cbyc Trading Bot can help you execute your trading strategy with ease.

## Features

- **Automated Trading:** Eliminate the hassle of manual trading. The bot automatically places buy and sell orders based on predefined strategies.
- **Customizable Strategies:** Implement and customize various trading strategies, including moving averages and other technical indicators.
- **Diverse Stock Selection:** Trade a wide range of stocks, including major AI companies like NVIDIA, Google, and Microsoft, as well as leading real estate firms.
- **Secure API Integration:** Safely connect to your trading account via secure APIs, ensuring your credentials are always protected.
- **Real-Time Market Data:** Fetch and analyze real-time market data to make informed trading decisions.
- **Error Handling:** Built-in error handling to manage API errors and trading exceptions smoothly.

## Installation

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/1cbyc/1cbyc-trading-bot.git
    cd 1cbyc-trading-bot
    ```

2. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Set Up Environment Variables:**
    Create a `.env` file in the root directory of the project using the `.env-example` file i added and add your API keys:
    ```plaintext
    ALPACA_API_KEY=your_api_key
    ALPACA_API_SECRET=your_api_secret
    ALPACA_BASE_URL=https://paper-api.alpaca.markets
    ```

## Usage

1. **Define Your Strategy:**
    Customize the trading strategy parameters in `main.py` to fit your preferences.

2. **Run the Bot:**
    ```bash
    python main.py
    ```

## Example Code

Here’s an example of how the bot can be used to trade stocks:

```python
from data.market_data import fetch_market_data
from strategies.moving_average import moving_average_strategy
from trading.order_execution import create_api_connection, place_order

def main():
    tickers_ai = ['NVDA', 'GOOGL', 'MSFT', 'IBM', 'AMZN', 'META', 'BIDU', 'CRM', 'ADBE', 'TSLA']
    tickers_real_estate = ['AMT', 'PLD', 'CCI', 'SPG', 'EQIX', 'PSA', 'DLR', 'AVB', 'EQR', 'O']
    
    tickers = tickers_ai + tickers_real_estate

    for ticker in tickers:
        data = fetch_market_data(ticker, "2024-01-01", "2024-12-31")
        data = moving_average_strategy(data, 20, 50)
        
        api = create_api_connection()
        
        for i in range(len(data)):
            if data['Position'][i] == 1:
                place_order(api, ticker, 1, 'buy')
            elif data['Position'][i] == -1:
                place_order(api, ticker, 1, 'sell')

    print("Trading bot has completed running.")

if __name__ == "__main__":
    main()