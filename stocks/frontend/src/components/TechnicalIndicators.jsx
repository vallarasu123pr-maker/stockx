import React from 'react';
import { TrendingUp, TrendingDown, Activity } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';

export default function TechnicalIndicators({ data, indicators, signals, currentIndicators }) {
  if (!indicators || !data) return null;

  // Prepare RSI chart data
  const rsiData = data.map((item, idx) => ({
    date: item.Date,
    rsi: indicators.rsi?.[idx]
  })).filter(d => d.rsi !== null);

  // Prepare MACD chart data
  const macdData = data.map((item, idx) => ({
    date: item.Date,
    macd: indicators.macd?.[idx],
    signal: indicators.signal?.[idx],
    histogram: indicators.histogram?.[idx]
  })).filter(d => d.macd !== null);

  const getSignalIcon = (signal) => {
    if (signal === 'bullish') return <TrendingUp className="w-4 h-4 text-emerald-400" />;
    if (signal === 'bearish') return <TrendingDown className="w-4 h-4 text-red-400" />;
    return <Activity className="w-4 h-4 text-slate-400" />;
  };

  const getSignalColor = (signal) => {
    if (signal === 'bullish') return 'text-emerald-400';
    if (signal === 'bearish') return 'text-red-400';
    if (signal === 'overbought') return 'text-red-400';
    if (signal === 'oversold') return 'text-emerald-400';
    return 'text-slate-400';
  };

  return (
    <div className="space-y-6">
      {/* Indicator Values Panel */}
      <div className="glass-panel rounded-2xl p-6">
        <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <Activity className="w-5 h-5 text-blue-400" />
          Technical Indicators
        </h3>
        
        <div className="grid grid-cols-2 gap-4">
          {/* RSI */}
          <div className="bg-slate-800/50 rounded-xl p-4 border border-slate-700/50">
            <p className="text-xs text-slate-400 mb-1">RSI (14)</p>
            <div className="flex items-center justify-between">
              <span className={`text-xl font-bold ${getSignalColor(signals?.rsi)}`}>
                {currentIndicators?.rsi?.toFixed(1) || '--'}
              </span>
              {getSignalIcon(signals?.rsi)}
            </div>
            <p className="text-xs text-slate-500 mt-1 capitalize">{signals?.rsi || 'neutral'}</p>
          </div>

          {/* EMA 50 */}
          <div className="bg-slate-800/50 rounded-xl p-4 border border-slate-700/50">
            <p className="text-xs text-slate-400 mb-1">EMA 50</p>
            <div className="flex items-center justify-between">
              <span className="text-xl font-bold">
                ${currentIndicators?.ema_50?.toFixed(2) || '--'}
              </span>
            </div>
          </div>

          {/* EMA 200 */}
          <div className="bg-slate-800/50 rounded-xl p-4 border border-slate-700/50">
            <p className="text-xs text-slate-400 mb-1">EMA 200</p>
            <div className="flex items-center justify-between">
              <span className="text-xl font-bold">
                ${currentIndicators?.ema_200?.toFixed(2) || '--'}
              </span>
              {getSignalIcon(signals?.ema)}
            </div>
            <p className="text-xs text-slate-500 mt-1 capitalize">{signals?.ema || 'neutral'}</p>
          </div>

          {/* MACD */}
          <div className="bg-slate-800/50 rounded-xl p-4 border border-slate-700/50">
            <p className="text-xs text-slate-400 mb-1">MACD</p>
            <div className="flex items-center justify-between">
              <span className={`text-xl font-bold ${getSignalColor(signals?.macd)}`}>
                {currentIndicators?.macd?.toFixed(2) || '--'}
              </span>
              {getSignalIcon(signals?.macd)}
            </div>
            <p className="text-xs text-slate-500 mt-1 capitalize">{signals?.macd || 'neutral'}</p>
          </div>
        </div>
      </div>

      {/* RSI Chart */}
      <div className="glass-panel rounded-2xl p-6">
        <h4 className="text-sm font-semibold mb-4 text-slate-300">RSI Indicator</h4>
        <div className="h-48">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={rsiData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.4} />
              <XAxis dataKey="date" stroke="#64748b" tick={{ fill: '#64748b', fontSize: 10 }} />
              <YAxis domain={[0, 100]} stroke="#64748b" tick={{ fill: '#64748b', fontSize: 10 }} />
              <Tooltip contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', borderRadius: '8px' }} />
              <ReferenceLine y={70} stroke="#ef4444" strokeDasharray="3 3" />
              <ReferenceLine y={30} stroke="#10b981" strokeDasharray="3 3" />
              <Line type="monotone" dataKey="rsi" stroke="#8b5cf6" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* MACD Chart */}
      <div className="glass-panel rounded-2xl p-6">
        <h4 className="text-sm font-semibold mb-4 text-slate-300">MACD Indicator</h4>
        <div className="h-48">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={macdData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.4} />
              <XAxis dataKey="date" stroke="#64748b" tick={{ fill: '#64748b', fontSize: 10 }} />
              <YAxis stroke="#64748b" tick={{ fill: '#64748b', fontSize: 10 }} />
              <Tooltip contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', borderRadius: '8px' }} />
              <ReferenceLine y={0} stroke="#64748b" />
              <Line type="monotone" dataKey="macd" stroke="#3b82f6" strokeWidth={2} dot={false} />
              <Line type="monotone" dataKey="signal" stroke="#f59e0b" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
