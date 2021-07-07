from flask import Flask, request
import requests
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
    chat_id = request.json["message"]["chat"]["id"]
    text = request.json["message"]["text"]

    # print(request.json)

    if text == "/start":
        send_message(chat_id, messages.welcome_message)
    elif text == "/help":
        send_message(chat_id, messages.help_message)
    return {"ok": True}

if __name__ == "__main__":

    # server_url update (ngrok)
    requests.post(get_api_url("setWebhook"), data={'url': config.SERVER_URL})

    app.run()