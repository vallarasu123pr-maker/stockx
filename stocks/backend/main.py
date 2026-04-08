from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import uvicorn
from pydantic import BaseModel
from typing import List, Optional, Dict
import pandas as pd
from datetime import datetime, timedelta
import os
import traceback

# Import modules with error handling
try:
    from indicators import TechnicalIndicators
    print("✓ Technical Indicators module loaded")
except Exception as e:
    print(f"✗ Failed to load Technical Indicators: {e}")
    raise

try:
    from ml_model import StockPredictor
    print("✓ ML Model module loaded")
except Exception as e:
    print(f"✗ Failed to load ML Model: {e}")
    StockPredictor = None

try:
    from gemini_service import GeminiService
    print("✓ Gemini Service module loaded")
except Exception as e:
    print(f"✗ Failed to load Gemini Service: {e}")
    raise

try:
    from database import AlertDatabase
    print("✓ Database module loaded")
except Exception as e:
    print(f"✗ Failed to load Database: {e}")
    raise

try:
    from alert_monitor import AlertMonitor
    print("✓ Alert Monitor module loaded")
except Exception as e:
    print(f"✗ Failed to load Alert Monitor: {e}")
    raise

try:
    from sample_data import generate_sample_data, get_sample_info
    print("✓ Sample Data module loaded")
except Exception as e:
    print(f"⚠ Sample Data module not available: {e}")
    generate_sample_data = None
    get_sample_info = None

app = FastAPI(title="Stock Analyzer API")

# Initialize services with error handling
try:
    gemini = GeminiService()
except Exception as e:
    print(f"⚠ Gemini service initialization failed: {e}")
    gemini = None

try:
    alert_db = AlertDatabase()
    print("✓ Alert database initialized")
except Exception as e:
    print(f"⚠ Alert database initialization failed: {e}")
    alert_db = None

try:
    alert_monitor = AlertMonitor(alert_db) if alert_db else None
    if alert_monitor:
        print("✓ Alert monitor initialized")
except Exception as e:
    print(f"⚠ Alert monitor initialization failed: {e}")
    alert_monitor = None

# Cache for predictions
prediction_cache = {}

print("=" * 60)
print("Stock Analyzer API - Ready!")
print("=" * 60)

class AlertCreate(BaseModel):
    user_id: str
    ticker: str
    type: str  # price_above, price_below, price_change_up, price_change_down
    target_price: Optional[float] = None
    target_percentage: Optional[float] = None
    base_price: Optional[float] = None
    email: Optional[str] = None

# Configure CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Stock Analyzer API"}

@app.get("/api/stock/{ticker}")
def get_stock_data(ticker: str, period: str = "1mo", interval: str = "1d"):
    use_sample_data = False

    try:
        print(f"Fetching data for {ticker}...")
        stock = yf.Ticker(ticker)

        # Try to fetch history
        hist = stock.history(period=period, interval=interval)

        if hist.empty:
            print(f"⚠ Yahoo Finance returned empty data for {ticker}, using sample data")
            use_sample_data = True
        else:
            print(f"✓ Fetched {len(hist)} data points for {ticker}")

    except Exception as yf_error:
        print(f"⚠ Yahoo Finance error: {yf_error}")
        use_sample_data = True

    # Use sample data if Yahoo Finance failed
    if use_sample_data:
        if generate_sample_data is None:
            raise HTTPException(
                status_code=503,
                detail="Yahoo Finance is unavailable and sample data module not loaded. Please try again later."
            )

        print(f"Using sample data for {ticker}")
        hist = generate_sample_data(ticker, days=30)
        info = get_sample_info(ticker)
        is_sample = True
    else:
        # Get stock info with error handling
        try:
            info = stock.info
        except Exception as info_error:
            print(f"⚠ Could not fetch stock info: {info_error}")
            info = get_sample_info(ticker) if get_sample_info else {}
        is_sample = False

    try:
        hist = hist.reset_index()
        if "Date" in hist.columns:
            hist["Date"] = hist["Date"].dt.strftime('%Y-%m-%d')
        elif "Datetime" in hist.columns:
            hist["Datetime"] = hist["Datetime"].dt.strftime('%Y-%m-%d %H:%M:%S')

        data = hist[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].to_dict(orient="records") if 'Date' in hist.columns else hist[['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']].to_dict(orient="records")

        # Get current price
        current_price = info.get("currentPrice", 0)
        if current_price == 0 and len(hist) > 0:
            current_price = float(hist['Close'].iloc[-1])

        # Calculate technical indicators
        print(f"Calculating technical indicators...")
        indicators_result = TechnicalIndicators.calculate_all(hist)
        indicators_data = {}
        for key, series in indicators_result['indicators'].items():
            # Replace NaN, Inf, -Inf with None for JSON serialization
            clean_series = series.replace([float('inf'), float('-inf')], None)
            indicators_data[key] = clean_series.where(pd.notna(clean_series), None).tolist()

        # Get current values for indicators
        current_indicators = {}
        for key, series in indicators_result['indicators'].items():
            last_val = series.iloc[-1] if len(series) > 0 else None
            if pd.notna(last_val) and abs(last_val) != float('inf'):
                current_indicators[key] = float(last_val)

        print(f"✓ Successfully processed {ticker}")

        result = {
            "ticker": ticker.upper(),
            "info": {
                "shortName": info.get("shortName", info.get("longName", ticker.upper())),
                "sector": info.get("sector", "N/A"),
                "industry": info.get("industry", "N/A"),
                "currentPrice": current_price,
                "currency": info.get("currency", "USD")
            },
            "data": data,
            "indicators": indicators_data,
            "current_indicators": current_indicators,
            "signals": indicators_result['signals']
        }

        if is_sample:
            result["_note"] = "Using sample data - Yahoo Finance unavailable"

        return result

    except HTTPException:
        raise
    except Exception as e:
        error_detail = f"{type(e).__name__}: {str(e)}"
        print(f"Error in get_stock_data: {error_detail}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=error_detail)

@app.get("/api/predict/{ticker}")
def predict_stock(ticker: str, days: int = 7):
    if StockPredictor is None:
        raise HTTPException(status_code=503, detail="ML prediction model is unavailable.")
    try:
        # Check cache
        cache_key = f"{ticker}_{days}"
        if cache_key in prediction_cache:
            cached = prediction_cache[cache_key]
            if datetime.now() - cached['timestamp'] < timedelta(hours=4):
                return cached['data']
        
        # Fetch historical data
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y", interval="1d")
        
        if hist.empty or len(hist) < 90:
            raise HTTPException(status_code=400, detail="Insufficient data for prediction. Need at least 90 days of history.")
        
        # Train and predict
        predictor = StockPredictor()
        metrics = predictor.train(hist, epochs=30, batch_size=16)
        predictions = predictor.predict(hist, days=days)
        
        # Calculate confidence score
        rmse_pct = (metrics['rmse'] / hist['Close'].mean()) * 100
        confidence = max(0, min(100, 100 - (rmse_pct * 10)))
        
        # Determine trend
        current_price = hist['Close'].iloc[-1]
        predicted_price = predictions[-1]
        price_change_pct = ((predicted_price - current_price) / current_price) * 100
        
        if price_change_pct > 2:
            trend = 'Bullish'
        elif price_change_pct < -2:
            trend = 'Bearish'
        else:
            trend = 'Neutral'
        
        # Generate prediction dates
        last_date = hist.index[-1]
        prediction_dates = [(last_date + timedelta(days=i+1)).strftime('%Y-%m-%d') for i in range(days)]
        
        # Get Gemini insights
        historical_data = {
            'high': float(hist['High'].max()),
            'low': float(hist['Low'].min()),
            'volume': float(hist['Volume'].mean())
        }
        
        if gemini:
            insights = gemini.generate_insights(
                ticker, 
                float(current_price), 
                predictions, 
                confidence, 
                trend, 
                historical_data
            )
        else:
            insights = "AI insights unavailable. Please configure GEMINI_API_KEY."
        
        result = {
            'ticker': ticker.upper(),
            'predictions': [{'date': d, 'price': float(p)} for d, p in zip(prediction_dates, predictions)],
            'confidence': round(confidence, 1),
            'trend': trend,
            'metrics': {
                'rmse': round(metrics['rmse'], 4),
                'mae': round(metrics['mae'], 4),
                'rmse_percentage': round(rmse_pct, 2)
            },
            'insights': insights,
            'current_price': float(current_price)
        }
        
        # Cache result
        prediction_cache[cache_key] = {
            'data': result,
            'timestamp': datetime.now()
        }
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def _require_alert_db():
    if alert_db is None:
        raise HTTPException(status_code=503, detail="Alert database is not available")

@app.post("/api/alerts")
def create_alert(alert: AlertCreate):
    _require_alert_db()
    try:
        alert_dict = alert.dict()
        alert_id = alert_db.create_alert(alert_dict)
        created_alert = alert_db.get_alert(alert_id)
        return {"success": True, "alert": created_alert}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/alerts")
def get_alerts(user_id: Optional[str] = None, status: Optional[str] = None):
    _require_alert_db()
    try:
        alerts = alert_db.get_alerts(user_id=user_id, status=status)
        return {"alerts": alerts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Static routes MUST come before parameterized /{alert_id} routes
@app.get("/api/alerts/history")
def get_alert_history(user_id: Optional[str] = None):
    _require_alert_db()
    try:
        history = alert_db.get_history(user_id=user_id)
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/alerts/check")
def check_alerts_now(background_tasks: BackgroundTasks):
    """Manually trigger alert checking"""
    _require_alert_db()
    if alert_monitor is None:
        raise HTTPException(status_code=503, detail="Alert monitor is not available")
    try:
        background_tasks.add_task(alert_monitor.check_alerts)
        return {"success": True, "message": "Alert check initiated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/alerts/{alert_id}")
def get_alert(alert_id: str):
    _require_alert_db()
    try:
        alert = alert_db.get_alert(alert_id)
        if not alert:
            raise HTTPException(status_code=404, detail="Alert not found")
        return {"alert": alert}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/alerts/{alert_id}")
def update_alert(alert_id: str, updates: Dict):
    _require_alert_db()
    try:
        success = alert_db.update_alert(alert_id, updates)
        if not success:
            raise HTTPException(status_code=404, detail="Alert not found")
        return {"success": True, "message": "Alert updated"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/alerts/{alert_id}")
def delete_alert(alert_id: str):
    _require_alert_db()
    try:
        success = alert_db.delete_alert(alert_id)
        if not success:
            raise HTTPException(status_code=404, detail="Alert not found")
        return {"success": True, "message": "Alert deleted"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
