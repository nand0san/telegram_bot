#!/usr/bin/env python
# -*- coding: utf-8 -*-
# get cryptocurrency from api
# create with bot father
# create a flask app and handle erequests from telegram
# combine api data and telegram bot
# deploy to pythonanywhere and flaskutility to ssl problem


from secret import coinmarketcap_token
from secret import apikey_telegram
import requests
import json
from flask import Flask
from flask import request
from flask import Response
import re

app = Flask(__name__)


def get_coinmarketcap_data(ticker):

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    headers = {'X-CMC_PRO_API_KEY': coinmarketcap_token}
    params = {'symbol': ticker, 'convert': 'USD'}

    r = requests.get(url, headers=headers, params=params).json()

    price = r['data'][ticker]['quote']['USD']['price']

    return price


def parse_message(message):
    chat_id = message['message']['chat']['id']
    txt = message['message']['text']            # /btc or /eth
    pattern = r'/[a-zA-Z]{2,4}'

    ticker_msg = re.findall(pattern, txt)  # this returns a list
    print(ticker_msg)
    if ticker_msg:
        ticker = ticker_msg[0][1:].upper()  # this returns /btc in example
        print(ticker)
    else:
        ticker = ''

    return chat_id, ticker



def write_json(data, filename='response.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def send_message(chat_id, text='bla-bla-bla'):
    url = 'https://api.telegram.org/bot{}/sendMessage'.format(apikey_telegram)
    payload = {'chat_id': chat_id, 'text': text} # pst method

    r = requests.post(url, json=payload)

    return r

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        msg = request.get_json()

        chat_id, ticker = parse_message(msg)

        if not ticker:
            send_message(chat_id, 'Wrong data!')
            return Response('Ok', status=200)

        price = get_coinmarketcap_data(ticker)
        # write_json(msg, 'telegram_request.json')
        send_message(chat_id, price)

        return Response('Ok', status=200)  # if telegram dont get 200 it keeps asking and asking
    else:
        return '<h1>CoinMarketCap Bot Get Request</h1>'


def main():

    # TODO: BOT
    # 1. CREATE LOCAL FLASK APP
    # 2. SET UP TUNNEL
    # 3. SET A WEBHOOK
    # 4. RECEIVE AND PARSE USER MESSAGES
    # 5. SEND MESSAGE TO USER

    print(get_coinmarketcap_data('BTC'))

    # https://api.telegram.org/bot--------------apikey----------/getMe
    # https://api.telegram.org/bot--------------apikey----------/getUpdates
    # notificamos a la api de telegram la url del bot
    # https://api.telegram.org/bot--------------apikey-----------/setWebhook?url=sisifostation.synology.me:8443

    # https://api.telegram.org/bot------------apikey----------/setWebhook?url=https://careo.serveo.net

    # to get webhook accesible run:     ssh -R 80:localhost:5000 serveo.net


if __name__ == '__main__':
    # main()
    app.run(debug=True, host='0.0.0.0')
