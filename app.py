from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from chatbot import ask_ai
from send_email import send_price_alert
import json
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

ALERTS_FILE = 'alerts.json'

# === Route 1: Chatbot ===
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_question = data.get('question', '')
    if not user_question:
        return jsonify({'error': 'No question provided'}), 400
    response = ask_ai(user_question)
    return jsonify({'answer': response})


# === Route 2: Set Alert ===
@app.route('/api/alert', methods=['POST'])
def set_alert():
    data = request.get_json()
    email = data.get('email')
    stock = data.get('stock')
    price = data.get('price')

    if not all([email, stock, price]):
        return jsonify({'error': 'Missing required fields'}), 400

    alert = {'email': email, 'stock': stock.upper(), 'price': float(price)}

    # Save to alerts.json
    if os.path.exists(ALERTS_FILE):
        with open(ALERTS_FILE, 'r') as f:
            alerts = json.load(f)
    else:
        alerts = []

    alerts.append(alert)
    with open(ALERTS_FILE, 'w') as f:
        json.dump(alerts, f, indent=2)

    return jsonify({'message': 'Alert set successfully'})


# === Route 3: Health Check ===
@app.route('/')
def index():
    return jsonify({'message': 'API is running'})


if __name__ == '__main__':
    app.run(debug=True)
