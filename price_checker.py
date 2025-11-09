import json
import time
import yfinance as yf
from send_email import send_alert_email
import os

ALERT_FILE = 'alerts.json'
PROCESSED_FILE = 'processed_alerts.json'

def load_alerts():
    if not os.path.exists(ALERT_FILE):
        return []

    with open(ALERT_FILE, 'r') as f:
        return json.load(f)

def save_processed_alerts(alerts):
    with open(PROCESSED_FILE, 'w') as f:
        json.dump(alerts, f, indent=2)

def check_prices():
    alerts = load_alerts()
    processed = []

    for alert in alerts:
        symbol = alert['symbol']
        target_price = float(alert['price'])
        email = alert['email']

        try:
            stock = yf.Ticker(symbol)
            data = stock.history(period="1d")
            current_price = data['Close'].iloc[-1]

            print(f"{symbol}: ₹{current_price:.2f} (target ₹{target_price})")

            if current_price >= target_price:
                send_alert_email(email, symbol, target_price, current_price)
                processed.append(alert)
        except Exception as e:
            print(f"❌ Error fetching data for {symbol}: {e}")

    # Remove processed alerts
    if processed:
        remaining_alerts = [a for a in alerts if a not in processed]
        with open(ALERT_FILE, 'w') as f:
            json.dump(remaining_alerts, f, indent=2)

        save_processed_alerts(processed)

if __name__ == "__main__":
    print("📈 Running price checker...")
    check_prices()