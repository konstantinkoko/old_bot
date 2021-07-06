from flask import Flask, request
import requests
from . import config

app = Flask(__name__)

api_url = config.api_url
telegram_token = config.telegram_token
server_url = config.server_url

@app.route("/", methods=["POST"])
def process():
    print(request.json)
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()