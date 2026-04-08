import pandas as pd
import numpy as np
from typing import Dict

class TechnicalIndicators:
    @staticmethod
    def calculate_rsi(data: pd.DataFrame, period: int = 14) -> pd.Series:
        if len(data) < period:
            return pd.Series([None] * len(data), index=data.index)
        
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss.replace(0, float('nan'))
        rsi = 100 - (100 / (1 + rs))
        # When loss is 0 (all gains), RSI should be 100
        rsi = rsi.fillna(100.0)
        return rsi
    
    @staticmethod
    def calculate_ema(data: pd.DataFrame, period: int) -> pd.Series:
        if len(data) < period:
            return pd.Series([None] * len(data), index=data.index)
        return data['Close'].ewm(span=period, adjust=False).mean()
    
    @staticmethod
    def calculate_macd(data: pd.DataFrame) -> Dict:
        if len(data) < 26:
            empty = pd.Series([None] * len(data), index=data.index)
            return {'macd': empty, 'signal': empty, 'histogram': empty}
        
        ema_12 = data['Close'].ewm(span=12, adjust=False).mean()
        ema_26 = data['Close'].ewm(span=26, adjust=False).mean()
        macd = ema_12 - ema_26
        signal = macd.ewm(span=9, adjust=False).mean()
        histogram = macd - signal
        
        return {'macd': macd, 'signal': signal, 'histogram': histogram}
    
    @classmethod
    def calculate_all(cls, data: pd.DataFrame) -> Dict:
        indicators = {}
        indicators['rsi'] = cls.calculate_rsi(data)
        indicators['ema_50'] = cls.calculate_ema(data, 50)
        indicators['ema_200'] = cls.calculate_ema(data, 200)
        macd_data = cls.calculate_macd(data)
        indicators.update(macd_data)
        
        signals = {}
        if not pd.isna(indicators['rsi'].iloc[-1]):
            rsi_val = indicators['rsi'].iloc[-1]
            signals['rsi'] = 'overbought' if rsi_val > 70 else 'oversold' if rsi_val < 30 else 'neutral'
        
        return {'indicators': indicators, 'signals': signals}
