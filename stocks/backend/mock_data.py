"""
Mock stock data for testing when Yahoo Finance API is down
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_mock_stock_data(ticker: str, days: int = 30) -> pd.DataFrame:
    """Generate realistic mock stock data"""
    
    # Base prices for common stocks
    base_prices = {
        'AAPL': 180,
        'MSFT': 380,
        'GOOGL': 140,
        'TSLA': 250,
        'AMZN': 170,
        'META': 480,
        'NVDA': 880,
    }
    
    base_price = base_prices.get(ticker.upper(), 100)
    
    # Generate dates
    end_date = datetime.now()
    dates = [end_date - timedelta(days=i) for i in range(days-1, -1, -1)]
    
    # Generate realistic price movements
    np.random.seed(hash(ticker) % 2**32)  # Consistent data for same ticker
    returns = np.random.normal(0.001, 0.02, days)  # 0.1% daily return, 2% volatility
    
    prices = [base_price]
    for ret in returns[1:]:
        prices.append(prices[-1] * (1 + ret))
    
    # Generate OHLCV data
    data = []
    for i, (date, close) in enumerate(zip(dates, prices)):
        high = close * (1 + abs(np.random.normal(0, 0.01)))
        low = close * (1 - abs(np.random.normal(0, 0.01)))
        open_price = close * (1 + np.random.normal(0, 0.005))
        volume = int(np.random.normal(50000000, 10000000))
        
        data.append({
            'Date': date,
            'Open': open_price,
            'High': max(high, open_price, close),
            'Low': min(low, open_price, close),
            'Close': close,
            'Volume': max(volume, 1000000)
        })
    
    df = pd.DataFrame(data)
    df.set_index('Date', inplace=True)
    return df

def get_mock_stock_info(ticker: str) -> dict:
    """Generate mock stock info"""
    
    info_data = {
        'AAPL': {
            'shortName': 'Apple Inc.',
            'sector': 'Technology',
            'industry': 'Consumer Electronics',
            'currency': 'USD'
        },
        'MSFT': {
            'shortName': 'Microsoft Corporation',
            'sector': 'Technology',
            'industry': 'Software',
            'currency': 'USD'
        },
        'GOOGL': {
            'shortName': 'Alphabet Inc.',
            'sector': 'Technology',
            'industry': 'Internet Content & Information',
            'currency': 'USD'
        },
        'TSLA': {
            'shortName': 'Tesla, Inc.',
            'sector': 'Consumer Cyclical',
            'industry': 'Auto Manufacturers',
            'currency': 'USD'
        },
        'AMZN': {
            'shortName': 'Amazon.com, Inc.',
            'sector': 'Consumer Cyclical',
            'industry': 'Internet Retail',
            'currency': 'USD'
        },
    }
    
    return info_data.get(ticker.upper(), {
        'shortName': f'{ticker.upper()} Inc.',
        'sector': 'Technology',
        'industry': 'Software',
        'currency': 'USD'
    })
