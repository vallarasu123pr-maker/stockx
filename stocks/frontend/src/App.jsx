import React, { useState } from 'react';
import { Search, Activity, Bell, Settings, Layers } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import axios from 'axios';
import TechnicalIndicators from './components/TechnicalIndicators';
import PredictionPanel from './components/PredictionPanel';
import AlertsPanel from './components/AlertsPanel';

function App() {
  const [ticker, setTicker] = useState('');
  const [stockData, setStockData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showEMA, setShowEMA] = useState(true);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!ticker.trim()) return;

    setLoading(true);
    setError(null);
    try {
      const response = await axios.get(`http://localhost:8000/api/stock/${ticker}`);
      const formattedData = response.data.data.map((item, idx) => ({
        ...item,
        Date: item.Date || item.Datetime,
        Close: parseFloat(item.Close.toFixed(2)),
        ema_50: response.data.indicators?.ema_50?.[idx],
        ema_200: response.data.indicators?.ema_200?.[idx]
      }));
      setStockData({
        ...response.data,
        data: formattedData
      });
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to fetch stock data");
      setStockData(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-slate-200 font-sans selection:bg-blue-500/30">
      <nav className="glass-panel sticky top-0 z-50 border-b border-slate-700/50 px-6 py-4 flex justify-between items-center">
        <div className="flex items-center gap-2">
          <Activity className="text-blue-500 w-8 h-8" />
          <h1 className="text-xl font-bold bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">
            Nexus AI
          </h1>
        </div>

        <div className="flex-1 max-w-xl mx-8">
          <form onSubmit={handleSearch} className="relative group">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400 group-focus-within:text-blue-400 transition-colors" />
            <input
              type="text"
              placeholder="Search ticker (e.g. AAPL, TSLA)"
              className="w-full bg-slate-800/50 border border-slate-700 rounded-full py-2.5 pl-10 pr-4 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all placeholder:text-slate-500 text-slate-200 shadow-inner"
              value={ticker}
              onChange={(e) => setTicker(e.target.value.toUpperCase())}
            />
            <button type="submit" className="hidden">Search</button>
          </form>
        </div>

        <div className="flex items-center gap-4">
          <button className="p-2 hover:bg-slate-800 rounded-full transition-colors text-slate-400 hover:text-white">
            <Bell className="w-5 h-5" />
          </button>
          <button className="p-2 hover:bg-slate-800 rounded-full transition-colors text-slate-400 hover:text-white">
            <Settings className="w-5 h-5" />
          </button>
          <div className="w-9 h-9 rounded-full bg-gradient-to-tr from-blue-600 to-indigo-500 p-0.5 ml-2 cursor-pointer shadow-lg shadow-blue-500/20 hover:shadow-blue-500/40 transition-all">
            <div className="w-full h-full rounded-full bg-slate-900 border-2 border-transparent"></div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-6 py-8">
        {loading && (
          <div className="flex flex-col items-center justify-center h-64 space-y-4">
            <div className="w-10 h-10 border-4 border-blue-500/30 border-t-blue-500 rounded-full animate-spin"></div>
            <p className="text-slate-400 animate-pulse">Analyzing Market Data...</p>
          </div>
        )}

        {error && (
          <div className="p-4 bg-red-500/10 border border-red-500/20 rounded-xl text-red-400 flex items-center gap-3">
            <Activity className="w-5 h-5" /> {error}
          </div>
        )}

        {!loading && stockData && (
          <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="flex justify-between items-end">
              <div>
                <p className="text-blue-400 font-medium tracking-wider text-sm mb-1">{stockData.info.sector} • {stockData.info.industry}</p>
                <h2 className="text-4xl font-bold flex items-center gap-3">
                  {stockData.info.shortName}
                  <span className="text-slate-400 text-2xl font-normal">({stockData.ticker})</span>
                </h2>
              </div>
              <div className="text-right">
                <p className="text-sm text-slate-400 mb-1">Current Price</p>
                <div className="text-4xl font-bold flex items-center gap-2 justify-end">
                  ${stockData.info.currentPrice?.toFixed(2) || stockData.data[stockData.data.length - 1]?.Close}
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2 space-y-6">
                <div className="glass-panel rounded-2xl p-6 relative overflow-hidden">
                  <div className="absolute top-0 right-0 w-64 h-64 bg-blue-500/10 blur-3xl rounded-full -translate-y-1/2 translate-x-1/2 pointer-events-none"></div>
                  <div className="flex justify-between items-center mb-6">
                    <h3 className="text-lg font-semibold flex items-center gap-2">
                      <Layers className="w-5 h-5 text-blue-400" /> Performance History
                    </h3>
                    <button
                      onClick={() => setShowEMA(!showEMA)}
                      className="px-3 py-1 text-xs font-semibold rounded-lg bg-slate-800 hover:bg-slate-700 transition-colors"
                    >
                      {showEMA ? 'Hide' : 'Show'} EMA
                    </button>
                  </div>

                  <div className="h-80 w-full">
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={stockData.data}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.4} vertical={false} />
                        <XAxis
                          dataKey="Date"
                          stroke="#64748b"
                          tick={{ fill: '#64748b', fontSize: 12 }}
                          tickMargin={10}
                          minTickGap={30}
                        />
                        <YAxis
                          domain={['auto', 'auto']}
                          stroke="#64748b"
                          tick={{ fill: '#64748b', fontSize: 12 }}
                          width={60}
                          tickMargin={10}
                        />
                        <Tooltip
                          contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', borderRadius: '12px' }}
                          itemStyle={{ color: '#f8fafc' }}
                        />
                        <Line type="monotone" dataKey="Close" stroke="#3B82F6" strokeWidth={2} dot={false} />
                        {showEMA && (
                          <>
                            <Line type="monotone" dataKey="ema_50" stroke="#10b981" strokeWidth={1.5} dot={false} strokeDasharray="5 5" />
                            <Line type="monotone" dataKey="ema_200" stroke="#f59e0b" strokeWidth={1.5} dot={false} strokeDasharray="5 5" />
                          </>
                        )}
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                <TechnicalIndicators
                  data={stockData.data}
                  indicators={stockData.indicators}
                  signals={stockData.signals}
                  currentIndicators={stockData.current_indicators}
                />
              </div>

              <div className="space-y-6">
                <PredictionPanel ticker={stockData?.ticker} />
                <AlertsPanel
                  ticker={stockData?.ticker}
                  currentPrice={stockData?.info?.currentPrice || stockData?.data[stockData.data.length - 1]?.Close}
                />
              </div>
            </div>
          </div>
        )}

        {!loading && !stockData && !error && (
          <div className="h-[60vh] flex flex-col items-center justify-center text-center">
            <div className="w-20 h-20 bg-blue-500/10 rounded-full flex items-center justify-center mb-6">
              <Activity className="w-10 h-10 text-blue-500" />
            </div>
            <h2 className="text-2xl font-bold mb-2">Welcome to Nexus AI</h2>
            <p className="text-slate-400 max-w-md">Search for a stock ticker above to view real-time historical data, technical indicators, and AI-powered market predictions.</p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
