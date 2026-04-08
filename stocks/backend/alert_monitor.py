import yfinance as yf
from typing import Dict, List
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from database import AlertDatabase

class AlertMonitor:
    """Monitor stock prices and trigger alerts"""
    
    def __init__(self, db: AlertDatabase):
        self.db = db
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_user = os.getenv('SMTP_USER')
        self.smtp_password = os.getenv('SMTP_PASSWORD')
    
    def check_alert_condition(self, alert: Dict, current_price: float) -> bool:
        """Check if alert condition is met"""
        alert_type = alert['type']
        
        if alert_type == 'price_above':
            return current_price >= alert['target_price']
        
        elif alert_type == 'price_below':
            return current_price <= alert['target_price']
        
        elif alert_type == 'price_change_up':
            base_price = alert.get('base_price', current_price)
            change_pct = ((current_price - base_price) / base_price) * 100
            return change_pct >= alert['target_percentage']
        
        elif alert_type == 'price_change_down':
            base_price = alert.get('base_price', current_price)
            change_pct = ((base_price - current_price) / base_price) * 100
            return change_pct >= alert['target_percentage']
        
        return False
    
    def send_email_notification(self, alert: Dict, current_price: float):
        """Send email notification"""
        if not self.smtp_user or not self.smtp_password:
            print("Email credentials not configured")
            return
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_user
            msg['To'] = alert['email']
            msg['Subject'] = f"Price Alert Triggered: {alert['ticker']}"
            
            body = f"""
            Your price alert has been triggered!
            
            Stock: {alert['ticker']}
            Alert Type: {alert['type']}
            Current Price: ${current_price:.2f}
            Target: {alert.get('target_price', alert.get('target_percentage', 'N/A'))}
            
            Time: {alert.get('triggered_at', 'Now')}
            
            This is an automated message from Nexus AI Stock Analyzer.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.send_message(msg)
            server.quit()
            
            print(f"Email sent to {alert['email']}")
            
        except Exception as e:
            print(f"Failed to send email: {e}")
    
    def check_alerts(self) -> List[Dict]:
        """Check all active alerts"""
        active_alerts = self.db.get_alerts(status='active')
        triggered_alerts = []
        
        # Group alerts by ticker to minimize API calls
        alerts_by_ticker = {}
        for alert in active_alerts:
            ticker = alert['ticker']
            if ticker not in alerts_by_ticker:
                alerts_by_ticker[ticker] = []
            alerts_by_ticker[ticker].append(alert)
        
        # Check each ticker
        for ticker, alerts in alerts_by_ticker.items():
            try:
                stock = yf.Ticker(ticker)
                current_price = stock.info.get('currentPrice', 0)
                
                if current_price == 0:
                    continue
                
                for alert in alerts:
                    if self.check_alert_condition(alert, current_price):
                        # Trigger alert
                        self.db.update_alert(alert['id'], {'status': 'triggered'})
                        self.db.add_to_history(alert, current_price)
                        
                        # Send notification
                        if alert.get('email'):
                            self.send_email_notification(alert, current_price)
                        
                        triggered_alerts.append({
                            'alert_id': alert['id'],
                            'ticker': ticker,
                            'current_price': current_price
                        })
                        
            except Exception as e:
                print(f"Error checking alerts for {ticker}: {e}")
        
        return triggered_alerts
