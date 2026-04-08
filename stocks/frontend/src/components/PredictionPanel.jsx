import React, { useState, useEffect } from 'react';
import { TrendingUp, TrendingDown, Activity, Sparkles } from 'lucide-react';
import axios from 'axios';

export default function PredictionPanel({ ticker }) {
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (ticker) {
      fetchPrediction();
    }
  }, [ticker]);

  const fetchPrediction = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get(`http://localhost:8000/api/predict/${ticker}?days=7`);
      setPrediction(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch prediction');
      setPrediction(null);
    } finally {
      setLoading(false);
    }
  };

  if (!ticker) return null;

  if (loading) {
    return (
      <div className="glass-panel rounded-2xl p-6 relative overflow-hidden">
        <div className="flex flex-col items-center justify-center h-48 space-y-4">
          <div className="w-8 h-8 border-4 border-purple-500/30 border-t-purple-500 rounded-full animate-spin"></div>
          <p className="text-slate-400 text-sm animate-pulse">Training AI Model...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="glass-panel rounded-2xl p-6 relative overflow-hidden">
        <div className="p-4 bg-red-500/10 border border-red-500/20 rounded-xl text-red-400 text-sm">
          {error}
        </div>
      </div>
    );
  }

  if (!prediction) return null;

  const getTrendIcon = () => {
    if (prediction.trend === 'Bullish') return <TrendingUp className="text-emerald-400 w-5 h-5" />;
    if (prediction.trend === 'Bearish') return <TrendingDown className="text-red-400 w-5 h-5" />;
    return <Activity className="text-slate-400 w-5 h-5" />;
  };

  const getTrendColor = () => {
    if (prediction.trend === 'Bullish') return 'text-emerald-400';
    if (prediction.trend === 'Bearish') return 'text-red-400';
    return 'text-slate-400';
  };

  const predicted7Day = prediction.predictions[6]?.price || 0;
  const priceChange = predicted7Day - prediction.current_price;
  const priceChangePct = (priceChange / prediction.current_price) * 100;

  return (
    <div className="glass-panel rounded-2xl p-6 relative overflow-hidden group">
      <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/10 to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity"></div>
      
      <h3 className="text-lg font-semibold flex items-center gap-2 mb-4">
        <Sparkles className="w-5 h-5 text-purple-400" />
        AI Forecast
      </h3>

      <div className="space-y-4 relative z-10">
        {/* Predicted Trend */}
        <div className="bg-slate-800/50 rounded-xl p-4 border border-slate-700/50">
          <p className="text-sm text-slate-400 mb-1">Predicted 7-Day Trend</p>
          <div className="flex items-center gap-2">
            {getTrendIcon()}
            <span className={`text-xl font-bold ${getTrendColor()}`}>
              {prediction.trend}
            </span>
          </div>
          <div className="mt-2 text-sm text-slate-400">
            <span className={priceChange >= 0 ? 'text-emerald-400' : 'text-red-400'}>
              {priceChange >= 0 ? '+' : ''}{priceChangePct.toFixed(2)}%
            </span>
            {' '}(${predicted7Day.toFixed(2)})
          </div>
        </div>

        {/* Confidence Score */}
        <div className="bg-slate-800/50 rounded-xl p-4 border border-slate-700/50">
          <p className="text-sm text-slate-400 mb-1">Confidence Score</p>
          <div className="flex items-end gap-2 text-xl font-bold">
            {prediction.confidence.toFixed(1)}%
          </div>
          <div className="w-full bg-slate-700 h-1.5 rounded-full mt-3 overflow-hidden">
            <div 
              className="bg-purple-500 h-full rounded-full transition-all duration-1000"
              style={{ width: `${prediction.confidence}%` }}
            ></div>
          </div>
        </div>

        {/* AI Insights */}
        {prediction.insights && (
          <div className="bg-slate-800/50 rounded-xl p-4 border border-slate-700/50">
            <p className="text-sm text-slate-400 mb-2">AI Insights</p>
            <p className="text-xs text-slate-300 leading-relaxed">
              {prediction.insights}
            </p>
          </div>
        )}

        {/* Metrics */}
        <div className="grid grid-cols-2 gap-3">
          <div className="bg-slate-800/50 rounded-lg p-3 border border-slate-700/50">
            <p className="text-xs text-slate-400 mb-1">RMSE</p>
            <p className="text-sm font-semibold">{prediction.metrics.rmse_percentage.toFixed(2)}%</p>
          </div>
          <div className="bg-slate-800/50 rounded-lg p-3 border border-slate-700/50">
            <p className="text-xs text-slate-400 mb-1">MAE</p>
            <p className="text-sm font-semibold">{prediction.metrics.mae.toFixed(4)}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
