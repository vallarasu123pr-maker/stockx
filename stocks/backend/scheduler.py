import schedule
import time
from database import AlertDatabase
from alert_monitor import AlertMonitor
import threading

def run_alert_checker():
    """Background task to check alerts periodically"""
    alert_db = AlertDatabase()
    monitor = AlertMonitor(alert_db)
    
    def check_job():
        print(f"Checking alerts at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        triggered = monitor.check_alerts()
        if triggered:
            print(f"Triggered {len(triggered)} alerts")
    
    # Schedule to run every minute
    schedule.every(1).minutes.do(check_job)
    
    print("Alert monitoring scheduler started...")
    while True:
        schedule.run_pending()
        time.sleep(30)

def start_scheduler():
    """Start the scheduler in a background thread"""
    scheduler_thread = threading.Thread(target=run_alert_checker, daemon=True)
    scheduler_thread.start()
    print("Background alert scheduler initialized")

if __name__ == "__main__":
    run_alert_checker()
