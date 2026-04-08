"""
Sample stock data for testing when Yahoo Finance is unavailable
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_data(ticker: str, days: int = 30) -> pd.DataFrame:
    """Generate realistic sample stock data"""
    
    # Base prices for different stocks
    base_prices = {
        'AAPL': 180.0,
        'TSLA': 250.0,
        'GOOGL': 140.0,
        'MSFT': 380.0,
        'AMZN': 170.0,
        'META': 480.0,
        'NVDA': 880.0,
    }
    
    base_price = base_prices.get(ticker.upper(), 100.0)
    
    # Generate dates
    end_date = datetime.now()
    dates = [end_date - timedelta(days=i) for i in range(days)]
    dates.reverse()
    
    # Generate price data with realistic movements
    np.random.seed(hash(ticker) % 2**32)
    
    prices = []
    current_price = base_price
    
    for i in range(days):
        # Random walk with slight upward bias
        change_pct = np.random.normal(0.002, 0.02)
        current_price *= (1 + change_pct)
        prices.append(current_price)
    
    # Generate OHLC data
    data = []
    for i, (date, close) in enumerate(zip(dates, prices)):
        volatility = close * 0.02
        high = close + abs(np.random.normal(0, volatility))
        low = close - abs(np.random.normal(0, volatility))
        open_price = low + (high - low) * np.random.random()
        volume = int(np.random.normal(50000000, 10000000))
        
        data.append({
            'Date': date,
            'Open': open_price,
            'High': high,
            'Low': low,
            'Close': close,
            'Volume': volume
        })
    
    df = pd.DataFrame(data)
    df.set_index('Date', inplace=True)
    
    return df

def get_sample_info(ticker: str) -> dict:
    """Get sample stock info"""
    
    info_data = {
        'AAPL': {
            'shortName': 'Apple Inc.',
            'sector': 'Technology',
            'industry': 'Consumer Electronics',
            'currency': 'USD'
        },
        'TSLA': {
            'shortName': 'Tesla, Inc.',
            'sector': 'Automotive',
            'industry': 'Auto Manufacturers',
            'currency': 'USD'
        },
        'GOOGL': {
            'shortName': 'Alphabet Inc.',
            'sector': 'Technology',
            'industry': 'Internet Content & Information',
            'currency': 'USD'
        },
        'MSFT': {
            'shortName': 'Microsoft Corporation',
            'sector': 'Technology',
            'industry': 'Software',
            'currency': 'USD'
        },
        'AMZN': {
            'shortName': 'Amazon.com, Inc.',
            'sector': 'Consumer Cyclical',
            'industry': 'Internet Retail',
            'currency': 'USD'
        },
        'META': {
            'shortName': 'Meta Platforms, Inc.',
            'sector': 'Technology',
            'industry': 'Internet Content & Information',
            'currency': 'USD'
        },
        'NVDA': {
            'shortName': 'NVIDIA Corporation',
            'sector': 'Technology',
            'industry': 'Semiconductors',
            'currency': 'USD'
        },
    }
    
    return info_data.get(ticker.upper(), {
        'shortName': f'{ticker.upper()} Corp.',
        'sector': 'Technology',
        'industry': 'Software',
        'currency': 'USD'
    })
