

import time
import yfinance as yf
from plyer import notification

THRESHOLD = 592.51  # Fixed threshold

def get_spy_price():
    spy = yf.Ticker("SPY")
    return spy.history(period="1d", interval="1m").iloc[-1]['Close']

def send_notification(price):
    notification.notify(
        title="SPY Price Alert",
        message=f"SPY has crossed {THRESHOLD}. Current price: ${price:.2f}",
        app_name="Python",
        timeout=5
    )

def monitor_price():
    while True:
        price = get_spy_price()
        print(f"Current SPY price: {price}")  # Debugging line
        if price >= THRESHOLD:
            send_notification(price)
        time.sleep(300)

if __name__ == "__main__":
    monitor_price()
