import React, { useState, useEffect } from 'react';
import { Bell, Plus, Trash2, Check, X } from 'lucide-react';
import axios from 'axios';

export default function AlertsPanel({ ticker, currentPrice }) {
  const [alerts, setAlerts] = useState([]);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newAlert, setNewAlert] = useState({
    type: 'price_above',
    target_price: '',
    target_percentage: '',
    email: ''
  });

  const userId = 'demo_user'; // In production, get from auth

  useEffect(() => {
    fetchAlerts();
  }, []);

  const fetchAlerts = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/api/alerts?user_id=${userId}`);
      setAlerts(response.data.alerts);
    } catch (err) {
      console.error('Failed to fetch alerts:', err);
    }
  };

  const createAlert = async () => {
    if (!ticker) {
      alert('Please select a stock first');
      return;
    }

    try {
      const alertData = {
        user_id: userId,
        ticker: ticker,
        type: newAlert.type,
        email: newAlert.email || null
      };

      if (!newAlert.type.includes('change')) {
        alertData.target_price = parseFloat(newAlert.target_price);
      } else {
        alertData.target_percentage = parseFloat(newAlert.target_percentage);
        alertData.base_price = currentPrice;
      }

      await axios.post('http://localhost:8000/api/alerts', alertData);
      
      setNewAlert({
        type: 'price_above',
        target_price: '',
        target_percentage: '',
        email: ''
      });
      setShowCreateForm(false);
      fetchAlerts();
    } catch (err) {
      alert('Failed to create alert: ' + (err.response?.data?.detail || err.message));
    }
  };

  const deleteAlert = async (alertId) => {
    try {
      await axios.delete(`http://localhost:8000/api/alerts/${alertId}`);
      fetchAlerts();
    } catch (err) {
      console.error('Failed to delete alert:', err);
    }
  };

  const getAlertDescription = (alert) => {
    if (alert.type === 'price_above') {
      return `Price above $${alert.target_price}`;
    } else if (alert.type === 'price_below') {
      return `Price below $${alert.target_price}`;
    } else if (alert.type === 'price_change_up') {
      return `Price up ${alert.target_percentage}%`;
    } else if (alert.type === 'price_change_down') {
      return `Price down ${alert.target_percentage}%`;
    }
    return alert.type;
  };

  const getStatusColor = (status) => {
    if (status === 'active') return 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30';
    if (status === 'triggered') return 'bg-blue-500/20 text-blue-400 border-blue-500/30';
    return 'bg-slate-500/20 text-slate-400 border-slate-500/30';
  };

  return (
    <div className="glass-panel rounded-2xl p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold flex items-center gap-2">
          <Bell className="w-5 h-5 text-blue-400" />
          Price Alerts
        </h3>
        <button
          onClick={() => setShowCreateForm(!showCreateForm)}
          className="p-2 hover:bg-slate-800 rounded-lg transition-colors"
        >
          {showCreateForm ? <X className="w-4 h-4" /> : <Plus className="w-4 h-4" />}
        </button>
      </div>

      {showCreateForm && (
        <div className="mb-4 p-4 bg-slate-800/50 rounded-xl border border-slate-700/50 space-y-3">
          <select
            value={newAlert.type}
            onChange={(e) => setNewAlert({ ...newAlert, type: e.target.value })}
            className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
          >
            <option value="price_above">Price Above</option>
            <option value="price_below">Price Below</option>
            <option value="price_change_up">Price Change Up %</option>
            <option value="price_change_down">Price Change Down %</option>
          </select>

          {!newAlert.type.includes('change') ? (
            <input
              type="number"
              placeholder="Target Price"
              value={newAlert.target_price}
              onChange={(e) => setNewAlert({ ...newAlert, target_price: e.target.value })}
              className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
            />
          ) : (
            <input
              type="number"
              placeholder="Target Percentage"
              value={newAlert.target_percentage}
              onChange={(e) => setNewAlert({ ...newAlert, target_percentage: e.target.value })}
              className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
            />
          )}

          <input
            type="email"
            placeholder="Email (optional)"
            value={newAlert.email}
            onChange={(e) => setNewAlert({ ...newAlert, email: e.target.value })}
            className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
          />

          <button
            onClick={createAlert}
            className="w-full bg-blue-500 hover:bg-blue-600 text-white rounded-lg px-4 py-2 text-sm font-semibold transition-colors"
          >
            Create Alert
          </button>
        </div>
      )}

      <div className="space-y-2 max-h-96 overflow-y-auto">
        {alerts.length === 0 ? (
          <p className="text-sm text-slate-400 text-center py-8">No alerts yet. Create one to get started!</p>
        ) : (
          alerts.map((alert) => (
            <div
              key={alert.id}
              className="flex items-center justify-between p-3 bg-slate-800/50 rounded-lg border border-slate-700/50 hover:border-slate-600 transition-colors"
            >
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-sm font-semibold">{alert.ticker}</span>
                  <span className={`text-xs px-2 py-0.5 rounded-full border ${getStatusColor(alert.status)}`}>
                    {alert.status}
                  </span>
                </div>
                <p className="text-xs text-slate-400">{getAlertDescription(alert)}</p>
              </div>
              <button
                onClick={() => deleteAlert(alert.id)}
                className="p-2 hover:bg-red-500/20 rounded-lg transition-colors text-red-400"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
