from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import json
import os

class Alert(BaseModel):
    id: str
    user_id: str
    ticker: str
    alert_type: str  # 'price_above', 'price_below', 'percent_change'
    target_value: float
    status: str = 'active'  # 'active', 'triggered', 'expired'
    created_at: str
    triggered_at: Optional[str] = None

class AlertManager:
    def __init__(self, db_file: str = "alerts.json"):
        self.db_file = db_file
        self.alerts = self.load_alerts()
    
    def load_alerts(self) -> List[Alert]:
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r') as f:
                data = json.load(f)
                return [Alert(**alert) for alert in data]
        return []
    
    def save_alerts(self):
        with open(self.db_file, 'w') as f:
            json.dump([alert.dict() for alert in self.alerts], f, indent=2)
    
    def create_alert(self, alert: Alert) -> Alert:
        self.alerts.append(alert)
        self.save_alerts()
        return alert
    
    def get_user_alerts(self, user_id: str) -> List[Alert]:
        return [a for a in self.alerts if a.user_id == user_id]
    
    def delete_alert(self, alert_id: str, user_id: str) -> bool:
        initial_len = len(self.alerts)
        self.alerts = [a for a in self.alerts if not (a.id == alert_id and a.user_id == user_id)]
        if len(self.alerts) < initial_len:
            self.save_alerts()
            return True
        return False
    
    def check_alerts(self, ticker: str, current_price: float):
        triggered = []
        for alert in self.alerts:
            if alert.ticker == ticker and alert.status == 'active':
                should_trigger = False
                
                if alert.alert_type == 'price_above' and current_price >= alert.target_value:
                    should_trigger = True
                elif alert.alert_type == 'price_below' and current_price <= alert.target_value:
                    should_trigger = True
                
                if should_trigger:
                    alert.status = 'triggered'
                    alert.triggered_at = datetime.now().isoformat()
                    triggered.append(alert)
        
        if triggered:
            self.save_alerts()
        
        return triggered

alert_manager = AlertManager()
