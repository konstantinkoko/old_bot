from flask import Flask, request
import requests
from . import config

app = Flask(__name__)

api_url = config.API_URL
telegram_token = config.TELEGRAM_TOKEN
server_url = config.SERVER_URL

@app.route("/", methods=["POST"])
def process():
    print(request.json)

'''
def hello():
    return "Hello World!"
'''

if __name__ == "__main__":

    # server_url update (ngrok)
    requests.post('https://api.telegram.org/bot' + telegram_token + '/setWebhook', data={'url': server_url})

    app.run()