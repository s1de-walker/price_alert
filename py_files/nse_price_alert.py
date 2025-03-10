
import time
import yfinance as yf
from plyer import notification
from datetime import datetime

RZ = 250.52  # Resistance Zone
SZ = 249.45  # Support Zone

last_alert = None  # Track the last alert type

def get_niftybees_price():
    niftybees = yf.Ticker("NIFTYBEES.NS")
    return niftybees.history(period="1d", interval="1m").iloc[-1]['Close']

def send_notification(price, alert_type):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current timestamp
    message = f"NIFTYBEES {'crossed above' if alert_type == 'Resistance' else 'fell below'} " \
              f"{RZ if alert_type == 'Resistance' else SZ}.\nCurrent price: ₹{price:.2f}"

    notification.notify(
        title="NIFTYBEES Price Alert",
        message=message,
        app_name="Python",
        timeout=5
    )

def monitor_price():
    global last_alert  # Allow modification of last_alert variable

    while True:
        try:
            price = get_niftybees_price()
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Timestamp for debugging
            print(f"{current_time} - Current NIFTYBEES price: {price}")  # Debugging line
            
            if price >= RZ and last_alert != "Resistance":
                send_notification(price, "Resistance")
                last_alert = "Resistance"  # Update last alert type
            
            elif price <= SZ and last_alert != "Support":
                send_notification(price, "Support")
                last_alert = "Support"  # Update last alert type

            elif SZ < price < RZ:
                last_alert = None  # Reset alert when back in range
            
        except Exception as e:
            print(f"Error fetching price: {e}")
        
        time.sleep(120)  # Check every 2 minutes

if __name__ == "__main__":
    monitor_price()
