# AI-Powered Stock Analyzer & Predictor

A full-stack web application for stock analysis with technical indicators, AI-powered predictions, and price alerts.

## 🚀 Quick Start (If you're having installation issues)

**Having timeout errors?** Follow these steps:

1. **Install minimal dependencies:**
   ```bash
   cd backend
   install_minimal.bat
   ```

2. **Check what's installed:**
   ```bash
   python check_dependencies.py
   ```

3. **Run the minimal version:**
   ```bash
   python main_minimal.py
   ```

4. **Start frontend:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

5. **Open app:** http://localhost:5173

See [QUICK_START.md](QUICK_START.md) for detailed troubleshooting.

## ✨ Features

### 1. Technical Indicators Module ✅
- **RSI (Relative Strength Index)** - 14-period with overbought/oversold signals
- **EMA (Exponential Moving Average)** - 50-day and 200-day with crossover detection
- **MACD** - With signal line and histogram
- **Visual Overlays** - Toggle indicators on/off on the price chart
- **Color-Coded Signals** - Bullish (green), Bearish (red), Neutral (gray)

### 2. AI Prediction Engine ✅
- **LSTM Neural Network** - Deep learning for time series forecasting
- **7-Day Price Predictions** - With confidence intervals
- **Confidence Score** - Based on model accuracy (RMSE/MAE)
- **Trend Classification** - Bullish, Bearish, or Neutral
- **Google Gemini AI** - Contextual market insights and analysis
- **Smart Caching** - 4-hour cache for faster responses

### 3. Price Alerts System ✅
- **Multiple Alert Types:**
  - Price Above/Below target
  - Percentage Change Up/Down
- **Email Notifications** - Optional SMTP integration
- **Alert Management** - Create, view, edit, delete
- **Background Monitoring** - Checks every 60 seconds
- **Alert History** - Track triggered alerts

## 📋 Prerequisites

- Python 3.8+ (3.10 recommended)
- Node.js 16+ and npm
- Internet connection for stock data

## 🔧 Installation

### Option 1: Full Installation (All Features)

```bash
# Backend
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
python main.py

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

### Option 2: Minimal Installation (No AI Predictions)

```bash
# Backend
cd backend
install_minimal.bat
python main_minimal.py

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

### Option 3: Step-by-Step Installation

See [backend/INSTALL_HELP.md](backend/INSTALL_HELP.md) for detailed installation instructions and troubleshooting.

## 🎯 Usage

1. **Search for a stock** - Enter ticker symbol (e.g., AAPL, TSLA, GOOGL)
2. **View technical indicators** - RSI, EMA, MACD with signals
3. **Get AI predictions** - 7-day forecast with confidence score (full version only)
4. **Create price alerts** - Get notified when price targets are hit
5. **Toggle EMA overlays** - Show/hide moving averages on chart

## 📁 Project Structure

```
stocks/
├── backend/
│   ├── main.py                    # Full version with AI
│   ├── main_minimal.py            # Minimal version without AI
│   ├── indicators.py              # Technical indicators
│   ├── ml_model.py                # LSTM prediction model
│   ├── gemini_service.py          # Gemini AI integration
│   ├── database.py                # Alert database
│   ├── alert_monitor.py           # Alert monitoring
│   ├── scheduler.py               # Background scheduler
│   ├── requirements.txt           # Python dependencies
│   ├── install_minimal.bat        # Quick installer
│   ├── install_dependencies.bat   # Full installer
│   ├── check_dependencies.py      # Dependency checker
│   └── INSTALL_HELP.md            # Installation guide
├── frontend/
│   ├── src/
│   │   ├── App.jsx                # Main app component
│   │   └── components/
│   │       ├── TechnicalIndicators.jsx
│   │       ├── PredictionPanel.jsx
│   │       └── AlertsPanel.jsx
│   ├── package.json
│   └── vite.config.js
├── .kiro/specs/                   # Feature specifications
├── README.md                      # This file
├── QUICK_START.md                 # Quick start guide
└── SETUP.md                       # Detailed setup guide
```

## 🔑 Environment Variables

Create `backend/.env`:

```env
# Required for AI insights
GEMINI_API_KEY=your_gemini_api_key_here

# Optional - for email alerts
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

Get Gemini API Key: https://makersuite.google.com/app/apikey

## 🌐 API Endpoints

### Stock Data
- `GET /api/stock/{ticker}` - Get stock data with technical indicators

### Predictions
- `GET /api/predict/{ticker}?days=7` - Get AI price predictions

### Alerts
- `POST /api/alerts` - Create alert
- `GET /api/alerts` - Get all alerts
- `GET /api/alerts/{id}` - Get specific alert
- `PUT /api/alerts/{id}` - Update alert
- `DELETE /api/alerts/{id}` - Delete alert
- `GET /api/alerts/history` - Get alert history

## 🛠️ Tech Stack

### Backend
- **FastAPI** - High-performance API framework
- **yfinance** - Stock data fetching
- **TensorFlow/Keras** - LSTM neural networks
- **Google Gemini AI** - Market insights
- **pandas/numpy** - Data processing
- **schedule** - Background tasks

### Frontend
- **React** - UI framework
- **Recharts** - Chart visualization
- **Tailwind CSS** - Styling
- **Axios** - HTTP client
- **Lucide React** - Icons

## 📊 Features Comparison

| Feature | Minimal Version | Full Version |
|---------|----------------|--------------|
| Stock Data | ✅ | ✅ |
| Technical Indicators | ✅ | ✅ |
| Price Alerts | ✅ | ✅ |
| AI Predictions | ❌ | ✅ |
| Gemini Insights | ❌ | ✅ |
| Installation Time | 2-5 min | 10-30 min |
| Disk Space | ~500 MB | ~2 GB |

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'yfinance'"
```bash
pip install yfinance --timeout 300
```

### "Read timed out" errors
```bash
cd backend
install_minimal.bat
```

### TensorFlow installation fails
Use the minimal version - AI predictions are optional!

### Frontend won't start
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

See [backend/INSTALL_HELP.md](backend/INSTALL_HELP.md) for more solutions.

## 📈 Performance

- Stock data fetch: <1 second
- Technical indicators: <1 second
- AI predictions (first time): 5-10 seconds
- AI predictions (cached): <500ms
- Alert checking: Every 60 seconds

## 🔮 Future Enhancements

- [ ] User authentication (JWT)
- [ ] Database integration (MongoDB/MSSQL)
- [ ] WebSocket for real-time updates
- [ ] Watchlist feature
- [ ] More technical indicators (Bollinger Bands, Stochastic)
- [ ] Sentiment analysis from news
- [ ] Backtesting for predictions
- [ ] Mobile app

## 📄 License

MIT License - Feel free to use and modify!

## 🤝 Contributing

Contributions welcome! Please read the specs in `.kiro/specs/` for feature details.

## 📞 Support

Having issues? Check these resources:
1. [QUICK_START.md](QUICK_START.md) - Quick fixes
2. [backend/INSTALL_HELP.md](backend/INSTALL_HELP.md) - Installation help
3. [SETUP.md](SETUP.md) - Detailed setup guide

## 🎓 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [TensorFlow Tutorials](https://www.tensorflow.org/tutorials)
- [Technical Analysis Guide](https://www.investopedia.com/technical-analysis-4689657)

---

**Note:** This is a demo application for educational purposes. Not financial advice. Always do your own research before making investment decisions.
