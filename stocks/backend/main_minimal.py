"""
Minimal version of main.py that works without TensorFlow and Gemini AI
Run this if you're having trouble installing all dependencies
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import uvicorn
from pydantic import BaseModel
from typing import List, Optional, Dict
import pandas as pd
from datetime import datetime, timedelta
import os

# Import only the modules that don't require TensorFlow/Gemini
from indicators import TechnicalIndicators
from database import AlertDatabase
from alert_monitor import AlertMonitor

app = FastAPI(title="Stock Analyzer API - Minimal Version")
alert_db = AlertDatabase()
alert_monitor = AlertMonitor(alert_db)

class AlertCreate(BaseModel):
    user_id: str
    ticker: str
    type: str
    target_price: Optional[float] = None
    target_percentage: Optional[float] = None
    base_price: Optional[float] = None
    email: Optional[str] = None

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Stock Analyzer API - Minimal Version",
        "features": ["Technical Indicators", "Price Alerts"],
        "note": "AI Predictions disabled. Install TensorFlow and Gemini AI to enable."
    }

@app.get("/api/stock/{ticker}")
def get_stock_data(ticker: str, period: str = "1mo", interval: str = "1d"):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period, interval=interval)
        
        if hist.empty:
            raise HTTPException(status_code=404, detail="Stock data not found or invalid ticker.")
        
        hist = hist.reset_index()
        if "Date" in hist.columns:
            hist["Date"] = hist["Date"].dt.strftime('%Y-%m-%d')
        elif "Datetime" in hist.columns:
            hist["Datetime"] = hist["Datetime"].dt.strftime('%Y-%m-%d %H:%M:%S')
            
        data = hist[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].to_dict(orient="records") if 'Date' in hist.columns else hist[['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']].to_dict(orient="records")
        
        info = stock.info
        
        # Calculate technical indicators
        indicators_result = TechnicalIndicators.calculate_all(hist)
        indicators_data = {}
        for key, series in indicators_result['indicators'].items():
            clean_series = series.replace([float('inf'), float('-inf')], None)
            indicators_data[key] = clean_series.where(pd.notna(clean_series), None).tolist()
        
        # Get current values for indicators
        current_indicators = {}
        for key, series in indicators_result['indicators'].items():
            last_val = series.iloc[-1] if len(series) > 0 else None
            if pd.notna(last_val) and abs(last_val) != float('inf'):
                current_indicators[key] = float(last_val)
        
        return {
            "ticker": ticker.upper(),
            "info": {
                "shortName": info.get("shortName", info.get("longName", ticker.upper())),
                "sector": info.get("sector", "N/A"),
                "industry": info.get("industry", "N/A"),
                "currentPrice": info.get("currentPrice", 0),
                "currency": info.get("currency", "USD")
            },
            "data": data,
            "indicators": indicators_data,
            "current_indicators": current_indicators,
            "signals": indicators_result['signals']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/predict/{ticker}")
def predict_stock(ticker: str, days: int = 7):
    """Prediction endpoint - disabled in minimal version"""
    raise HTTPException(
        status_code=503, 
        detail="AI Predictions are disabled. Install TensorFlow and google-generativeai packages to enable this feature."
    )

# Alert endpoints
@app.post("/api/alerts")
def create_alert(alert: AlertCreate):
    try:
        alert_dict = alert.dict()
        alert_id = alert_db.create_alert(alert_dict)
        created_alert = alert_db.get_alert(alert_id)
        return {"success": True, "alert": created_alert}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/alerts")
def get_alerts(user_id: Optional[str] = None, status: Optional[str] = None):
    try:
        alerts = alert_db.get_alerts(user_id=user_id, status=status)
        return {"alerts": alerts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Static routes MUST come before parameterized /{alert_id} routes
@app.get("/api/alerts/history")
def get_alert_history(user_id: Optional[str] = None):
    try:
        history = alert_db.get_history(user_id=user_id)
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/alerts/check")
def check_alerts_now(background_tasks: BackgroundTasks):
    """Manually trigger alert checking"""
    try:
        background_tasks.add_task(alert_monitor.check_alerts)
        return {"success": True, "message": "Alert check initiated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/alerts/{alert_id}")
def get_alert(alert_id: str):
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
    print("=" * 60)
    print("Starting Stock Analyzer API - Minimal Version")
    print("=" * 60)
    print("Features enabled:")
    print("  ✓ Technical Indicators (RSI, EMA, MACD)")
    print("  ✓ Price Alerts")
    print("  ✗ AI Predictions (install TensorFlow to enable)")
    print("=" * 60)
    uvicorn.run("main_minimal:app", host="0.0.0.0", port=8000, reload=True)
