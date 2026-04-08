"""
Test script to check if yfinance is working
"""
import yfinance as yf
from datetime import datetime, timedelta

print("Testing yfinance...")
print("=" * 60)

# Test 1: Simple ticker
print("\nTest 1: Fetching AAPL data...")
try:
    ticker = yf.Ticker("AAPL")
    hist = ticker.history(period="5d")
    if not hist.empty:
        print(f"✓ Success! Got {len(hist)} days of data")
        print(f"  Latest close: ${hist['Close'].iloc[-1]:.2f}")
    else:
        print("✗ Failed: Empty data")
except Exception as e:
    print(f"✗ Failed: {e}")

# Test 2: Using download
print("\nTest 2: Using yf.download...")
try:
    end_date = datetime.now()
    start_date = end_date - timedelta(days=5)
    data = yf.download("AAPL", start=start_date, end=end_date, progress=False)
    if not data.empty:
        print(f"✓ Success! Got {len(data)} days of data")
        print(f"  Latest close: ${data['Close'].iloc[-1]:.2f}")
    else:
        print("✗ Failed: Empty data")
except Exception as e:
    print(f"✗ Failed: {e}")

# Test 3: Multiple tickers
print("\nTest 3: Testing other tickers...")
for symbol in ["MSFT", "GOOGL", "TSLA"]:
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1d")
        if not hist.empty:
            print(f"✓ {symbol}: ${hist['Close'].iloc[-1]:.2f}")
        else:
            print(f"✗ {symbol}: Empty data")
    except Exception as e:
        print(f"✗ {symbol}: {e}")

print("\n" + "=" * 60)
print("\nIf all tests failed, Yahoo Finance API might be down.")
print("This is a known issue that happens occasionally.")
print("\nSolutions:")
print("1. Wait a few minutes and try again")
print("2. Check https://finance.yahoo.com/ to see if it's accessible")
print("3. Try using a VPN if you're in a restricted region")
print("4. Use alternative data sources (Alpha Vantage, IEX Cloud)")
