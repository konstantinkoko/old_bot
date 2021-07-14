from flask import Flask, request
import requests

from db_operations import *
from aggregator import show_company_trading_info
import config, messages

app = Flask(__name__)

def get_api_url(method):
    api_url = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/{method}"
    return api_url

def send_message(chat_id, text):
    method = "sendMessage"
    url = get_api_url(method)
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)


@app.route("/", methods=["POST"])
def process():

    id = request.json["message"]["from"]["id"]
    name = request.json["message"]["from"]["first_name"]
    chat_id = request.json["message"]["chat"]["id"]
    text = request.json["message"]["text"]

    message = None
    if text == "/start":
        add_user(id, name)
        message = messages.welcome_message
    elif text == "/help":
        message = messages.help_message
    elif text.split()[0] == "/add":
        message = add_company(id, text.split()[1])
    elif text.split()[0] == "/remove":
        message = remove_company(id, text.split()[1])
    elif text == "/companies":
        message = show_companies(id)
    elif text.split()[0] == "/show":
        message = show_company_trading_info(id, text.split()[1], period='year')
    elif text.split()[0] == "/time":
        message = set_notification_time(id, text.split()[1])

    if message != None:
        send_message(chat_id, message)

    return {"ok": True}

if __name__ == "__main__":

    # server_url update (ngrok)
    requests.post(get_api_url("setWebhook"), data={'url': config.SERVER_URL})

    with sql.connect('test_data_base.db') as connect:
        connect.execute("""
            CREATE TABLE IF NOT EXISTS user (
                user_id INTEGER NOT NULL PRIMARY KEY,
                name TEXT
            );
        """)
        connect.execute("""
            CREATE TABLE IF NOT EXISTS users_companies (
                user_id INTEGER NOT NULL,
                ticker TEXT,
                CONSTRAINT p_key PRIMARY KEY (user_id, ticker)
            );
        """)

    app.run()
