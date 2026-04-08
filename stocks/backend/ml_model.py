import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import GradientBoostingRegressor
from typing import Tuple, Dict
import pickle
import os


class StockPredictor:
    """Gradient Boosting stock price prediction model (scikit-learn based)"""

    def __init__(self, lookback: int = 30):
        self.lookback = lookback
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.model = None

    def _make_features(self, scaled_prices: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Build lag-feature matrix from scaled price array."""
        X, y = [], []
        for i in range(self.lookback, len(scaled_prices)):
            X.append(scaled_prices[i - self.lookback:i, 0])
            y.append(scaled_prices[i, 0])
        return np.array(X), np.array(y)

    def train(self, data: pd.DataFrame, epochs: int = 50, batch_size: int = 32):
        """Train the model (epochs/batch_size kept for API compatibility but unused)."""
        prices = data['Close'].values.reshape(-1, 1)
        scaled = self.scaler.fit_transform(prices)

        X, y = self._make_features(scaled)

        split = int(0.8 * len(X))
        X_train, X_test = X[:split], X[split:]
        y_train, y_test = y[:split], y[split:]

        self.model = GradientBoostingRegressor(
            n_estimators=200, learning_rate=0.05, max_depth=4, random_state=42
        )
        self.model.fit(X_train, y_train)

        scaled_preds = self.model.predict(X_test).reshape(-1, 1)
        actual_preds = self.scaler.inverse_transform(scaled_preds)
        actual_y = self.scaler.inverse_transform(y_test.reshape(-1, 1))

        rmse = float(np.sqrt(np.mean((actual_preds - actual_y) ** 2)))
        mae = float(np.mean(np.abs(actual_preds - actual_y)))
        return {'rmse': rmse, 'mae': mae}

    def predict(self, data: pd.DataFrame, days: int = 7) -> Dict:
        """Generate multi-step price predictions via recursive forecasting."""
        prices = data['Close'].values.reshape(-1, 1)
        scaled = self.scaler.transform(prices)

        sequence = scaled[-self.lookback:, 0].copy()
        predictions = []

        for _ in range(days):
            pred = self.model.predict(sequence.reshape(1, -1))[0]
            predictions.append(pred)
            sequence = np.append(sequence[1:], pred)

        result = self.scaler.inverse_transform(
            np.array(predictions).reshape(-1, 1)
        )
        return result.flatten().tolist()

    def save_model(self, ticker: str, path: str = 'models'):
        """Save trained model."""
        os.makedirs(path, exist_ok=True)
        with open(f'{path}/{ticker}_model.pkl', 'wb') as f:
            pickle.dump(self.model, f)
        with open(f'{path}/{ticker}_scaler.pkl', 'wb') as f:
            pickle.dump(self.scaler, f)

    def load_model(self, ticker: str, path: str = 'models'):
        """Load trained model."""
        with open(f'{path}/{ticker}_model.pkl', 'rb') as f:
            self.model = pickle.load(f)
        with open(f'{path}/{ticker}_scaler.pkl', 'rb') as f:
            self.scaler = pickle.load(f)
