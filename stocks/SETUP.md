# Setup Guide - AI Stock Analyzer with Technical Indicators, Predictions & Alerts

## Features Implemented

### 1. Technical Indicators Module ✅
- RSI (Relative Strength Index) with overbought/oversold signals
- EMA 50 & 200 with crossover detection
- MACD with signal line and histogram
- Visual overlays on price chart
- Dedicated indicator panels with color-coded signals

### 2. AI Prediction Engine ✅
- LSTM neural network for price forecasting
- 7-day price predictions
- Confidence score based on model accuracy
- Trend classification (Bullish/Bearish/Neutral)
- Google Gemini AI integration for market insights
- Prediction caching for performance

### 3. Price Alerts System ✅
- Create custom price alerts
- Multiple alert types (price above/below, percentage change)
- Email notifications (optional)
- Alert management dashboard
- Background monitoring service
- Alert history tracking

## Backend Setup

### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the `backend` directory:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
# Required for AI insights
GEMINI_API_KEY=your_gemini_api_key_here

# Optional - for email alerts
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

**Get Gemini API Key:**
1. Visit https://makersuite.google.com/app/apikey
2. Create a new API key
3. Copy and paste into `.env`

### 3. Start the Backend Server

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### 4. Start Alert Monitoring (Optional)

In a separate terminal:

```bash
cd backend
python scheduler.py
```

This runs a background service that checks alerts every minute.

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:5173`

## Usage Guide

### Technical Indicators

1. Search for a stock (e.g., AAPL, TSLA)
2. View technical indicators in the dedicated panel
3. Toggle EMA lines on/off using the button
4. Check RSI, MACD charts below the main chart
5. Color-coded signals show bullish/bearish/neutral conditions

### AI Predictions

1. After searching for a stock, predictions load automatically
2. View 7-day price forecast with confidence score
3. Read AI-generated insights from Gemini
4. Check trend classification and metrics (RMSE, MAE)

### Price Alerts

1. Search for a stock first
2. Click the "+" button in the Alerts Panel
3. Choose alert type:
   - Price Above: Trigger when price goes above target
   - Price Below: Trigger when price goes below target
   - Price Change Up %: Trigger when price increases by X%
   - Price Change Down %: Trigger when price decreases by X%
4. Enter target price or percentage
5. Optionally add email for notifications
6. Click "Create Alert"
7. Alerts are checked every minute by the background service

## API Endpoints

### Stock Data with Indicators
```
GET /api/stock/{ticker}?period=1mo&interval=1d
```

Returns historical data + technical indicators (RSI, EMA, MACD)

### AI Predictions
```
GET /api/predict/{ticker}?days=7
```

Returns LSTM predictions with Gemini AI insights

### Alerts Management
```
POST /api/alerts - Create alert
GET /api/alerts?user_id={id} - Get user alerts
GET /api/alerts/{alert_id} - Get specific alert
PUT /api/alerts/{alert_id} - Update alert
DELETE /api/alerts/{alert_id} - Delete alert
GET /api/alerts/history?user_id={id} - Get alert history
POST /api/alerts/check - Manually trigger alert check
```

## Architecture

### Backend
- **FastAPI**: High-performance API framework
- **yfinance**: Stock data fetching
- **TensorFlow/Keras**: LSTM model training
- **Google Gemini AI**: Market insights generation
- **pandas/numpy**: Data processing
- **schedule**: Background alert monitoring

### Frontend
- **React**: UI framework
- **Recharts**: Chart visualization
- **Tailwind CSS**: Styling
- **Axios**: API requests
- **Lucide React**: Icons

### Data Flow
1. User searches for stock ticker
2. Backend fetches historical data from yfinance
3. Technical indicators calculated using pandas
4. LSTM model trains on historical data
5. Gemini AI generates contextual insights
6. Frontend displays all data with interactive charts
7. Background service monitors alerts every minute

## Troubleshooting

### Backend Issues

**Import errors:**
```bash
pip install --upgrade -r requirements.txt
```

**TensorFlow issues on Windows:**
```bash
pip install tensorflow-cpu==2.15.0
```

**Gemini API errors:**
- Check API key is correct in `.env`
- Verify API key has proper permissions
- Check rate limits

### Frontend Issues

**Component not found:**
```bash
cd frontend
npm install
```

**Chart not rendering:**
- Check browser console for errors
- Verify API is running on port 8000
- Check CORS settings in backend

### Alert Issues

**Alerts not triggering:**
- Ensure `scheduler.py` is running
- Check alert status is "active"
- Verify stock ticker is valid

**Email not sending:**
- Check SMTP credentials in `.env`
- For Gmail, use App Password (not regular password)
- Enable "Less secure app access" or use OAuth2

## Performance Notes

- First prediction takes ~5-10 seconds (model training)
- Subsequent predictions are cached for 4 hours
- Technical indicators calculate in <1 second
- Alert checking runs every 60 seconds
- Recommended: 1000+ alerts max per instance

## Next Steps

1. Add user authentication (JWT tokens)
2. Implement database (MongoDB/MSSQL) for persistent storage
3. Add WebSocket for real-time price updates
4. Implement watchlist feature
5. Add more technical indicators (Bollinger Bands, Stochastic)
6. Enhance LSTM model with more features
7. Add sentiment analysis from news
8. Implement backtesting for predictions

## License

MIT License - Feel free to use and modify!
