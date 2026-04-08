# Quick Start Guide - Fix Installation Issues

## Problem: Timeout errors and missing modules

You're seeing these errors because pip is timing out when downloading large packages like TensorFlow.

## Solution: Use the step-by-step installation

### Step 1: Install minimal dependencies first

Open Command Prompt in the `backend` folder and run:

```bash
cd backend
install_minimal.bat
```

This installs only the essential packages needed to run the app.

### Step 2: Run the minimal version

```bash
python main_minimal.py
```

This starts the server with:
- ✅ Technical Indicators (RSI, EMA, MACD)
- ✅ Price Alerts
- ❌ AI Predictions (disabled for now)

### Step 3: Start the frontend

Open a new Command Prompt:

```bash
cd frontend
npm install
npm run dev
```

### Step 4: Test the app

1. Open http://localhost:5173
2. Search for a stock (e.g., AAPL)
3. View technical indicators
4. Create price alerts

The AI predictions will show "temporarily unavailable" - that's expected!

## Optional: Install AI features later

When you have a better internet connection or more time:

```bash
cd backend

# Install TensorFlow (large package, may take 10-30 minutes)
pip install tensorflow==2.15.0 --timeout 600

# Install Gemini AI
pip install google-generativeai==0.3.1 --timeout 300
```

Then switch to the full version:

```bash
python main.py
```

## Alternative: Install with increased timeout

If you want to try installing everything at once:

```bash
cd backend
install_dependencies.bat
```

This installs packages one by one with 5-10 minute timeouts.

## Troubleshooting

### Still getting "ModuleNotFoundError: No module named 'yfinance'"?

Install it manually:

```bash
pip install yfinance --timeout 300
```

### Timeout errors persist?

Try using a mirror (faster in some regions):

```bash
pip install yfinance pandas numpy fastapi uvicorn -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Want to skip TensorFlow entirely?

Just use `main_minimal.py` - it works great without AI predictions!

## What works in minimal version?

✅ Stock data fetching
✅ Technical indicators (RSI, EMA 50/200, MACD)
✅ Interactive charts with EMA overlays
✅ Price alerts (all types)
✅ Alert management
✅ Background alert monitoring

❌ AI price predictions (requires TensorFlow)
❌ Gemini AI insights (requires google-generativeai)

## Next Steps

1. Run `python main_minimal.py` in backend folder
2. Run `npm run dev` in frontend folder
3. Open http://localhost:5173
4. Search for stocks and explore!

The app is fully functional without AI predictions. You can add them later when you have time to install TensorFlow.
