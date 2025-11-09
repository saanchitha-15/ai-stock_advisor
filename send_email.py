# send_email.py
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def send_alert_email(to_email, stock_symbol, target_price, current_price):
    subject = f"📢 Stock Alert: {stock_symbol} has hit ₹{current_price}"
    body = (
        f"The stock {stock_symbol} has reached your target price of ₹{target_price}.\n"
        f"Current Price: ₹{current_price}\n\n"
        f"Check your trading platform or portfolio!"
    )

    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASS)
            smtp.send_message(msg)
        print(f"✅ Email sent to {to_email} for {stock_symbol}")
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")
