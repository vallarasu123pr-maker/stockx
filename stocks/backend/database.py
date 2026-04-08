from datetime import datetime
from typing import List, Dict, Optional
import json
import os

class AlertDatabase:
    """Simple file-based database for alerts (can be replaced with MongoDB/MSSQL)"""
    
    def __init__(self, db_path: str = 'data/alerts.json'):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """Initialize database file"""
        if not os.path.exists(self.db_path):
            with open(self.db_path, 'w') as f:
                json.dump({'alerts': [], 'alert_history': []}, f)
    
    def _read_db(self) -> Dict:
        """Read database"""
        with open(self.db_path, 'r') as f:
            return json.load(f)
    
    def _write_db(self, data: Dict):
        """Write to database"""
        with open(self.db_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def create_alert(self, alert: Dict) -> str:
        """Create a new alert"""
        db = self._read_db()
        alert['id'] = f"alert_{len(db['alerts']) + 1}_{int(datetime.now().timestamp())}"
        alert['created_at'] = datetime.now().isoformat()
        alert['status'] = 'active'
        db['alerts'].append(alert)
        self._write_db(db)
        return alert['id']
    
    def get_alerts(self, user_id: str = None, status: str = None) -> List[Dict]:
        """Get alerts with optional filters"""
        db = self._read_db()
        alerts = db['alerts']
        
        if user_id:
            alerts = [a for a in alerts if a.get('user_id') == user_id]
        if status:
            alerts = [a for a in alerts if a.get('status') == status]
        
        return alerts
    
    def get_alert(self, alert_id: str) -> Optional[Dict]:
        """Get a specific alert"""
        db = self._read_db()
        for alert in db['alerts']:
            if alert['id'] == alert_id:
                return alert
        return None
    
    def update_alert(self, alert_id: str, updates: Dict) -> bool:
        """Update an alert"""
        db = self._read_db()
        for i, alert in enumerate(db['alerts']):
            if alert['id'] == alert_id:
                db['alerts'][i].update(updates)
                self._write_db(db)
                return True
        return False
    
    def delete_alert(self, alert_id: str) -> bool:
        """Delete an alert"""
        db = self._read_db()
        initial_len = len(db['alerts'])
        db['alerts'] = [a for a in db['alerts'] if a['id'] != alert_id]
        
        if len(db['alerts']) < initial_len:
            self._write_db(db)
            return True
        return False
    
    def add_to_history(self, alert: Dict, triggered_price: float):
        """Add triggered alert to history"""
        db = self._read_db()
        history_entry = {
            **alert,
            'triggered_at': datetime.now().isoformat(),
            'triggered_price': triggered_price
        }
        db['alert_history'].append(history_entry)
        self._write_db(db)
    
    def get_history(self, user_id: str = None) -> List[Dict]:
        """Get alert history"""
        db = self._read_db()
        history = db['alert_history']
        
        if user_id:
            history = [h for h in history if h.get('user_id') == user_id]
        
        return history
