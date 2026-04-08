import google.generativeai as genai
from typing import Dict, List
import os

class GeminiService:
    """Service for integrating Google Gemini AI"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.model = None
        
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-pro')
                print("✓ Gemini AI initialized successfully")
            except Exception as e:
                print(f"⚠ Gemini AI initialization failed: {e}")
                self.model = None
        else:
            print("⚠ Gemini API key not found. AI insights will be unavailable.")
            print("  To enable: Set GEMINI_API_KEY in .env file")
    
    def generate_insights(self, ticker: str, current_price: float, 
                         predictions: List[float], confidence: float,
                         trend: str, historical_data: Dict) -> str:
        """Generate AI insights about stock predictions"""
        
        if not self.model:
            return "AI insights unavailable. Please configure GEMINI_API_KEY."
        
        try:
            prompt = f"""
            Analyze the following stock prediction data and provide actionable insights:
            
            Stock: {ticker}
            Current Price: ${current_price:.2f}
            Predicted Prices (7 days): {[f'${p:.2f}' for p in predictions[:7]]}
            Confidence Score: {confidence:.1f}%
            Trend: {trend}
            
            Recent Performance:
            - High: ${historical_data.get('high', 0):.2f}
            - Low: ${historical_data.get('low', 0):.2f}
            - Volume: {historical_data.get('volume', 0):,.0f}
            
            Provide a brief analysis (3-4 sentences) covering:
            1. Key factors that might influence this prediction
            2. Risk assessment
            3. Actionable recommendation for investors
            
            Keep the response concise and professional.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"AI insights temporarily unavailable: {str(e)}"
    
    def analyze_technical_indicators(self, ticker: str, indicators: Dict, 
                                    signals: Dict) -> str:
        """Generate insights about technical indicators"""
        
        if not self.model:
            return "AI insights unavailable. Please configure GEMINI_API_KEY."
        
        try:
            prompt = f"""
            Analyze these technical indicators for {ticker}:
            
            RSI: {indicators.get('rsi', 'N/A')} - Signal: {signals.get('rsi', 'N/A')}
            EMA 50: {indicators.get('ema_50', 'N/A')}
            EMA 200: {indicators.get('ema_200', 'N/A')} - Signal: {signals.get('ema', 'N/A')}
            MACD: {indicators.get('macd', 'N/A')} - Signal: {signals.get('macd', 'N/A')}
            
            Provide a brief technical analysis (2-3 sentences) about what these indicators suggest.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"Technical analysis unavailable: {str(e)}"
