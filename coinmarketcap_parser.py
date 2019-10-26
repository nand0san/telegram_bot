#!/usr/bin/env python
# -*- coding: utf-8 -*-
# get cryptocurrency from api
# create with bot father
# create a flask app and handle erequests from telegram
# combine api data and telegram bot
# deploy to pythonanywhere and flaskutility to ssl problem


from secret import coinmarketcap_token
import requests
import json


# endpoints api marketcap
baseurl = 'https://pro-api.coinmarketcap.com'
latest_quotes = '/v1/cryptocurrency/quotes/latest'


def get_coinmarketcap_data(ticker):

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    headers = {'X-CMC_PRO_API_KEY': coinmarketcap_token}
    params = {'symbol': ticker, 'convert': 'USD'}

    r = requests.get(url, headers=headers, params=params).json()

    price = r['data'][ticker]['quote']['USD']['price']

    return price
    # write_json(r)
    # print(r)


def write_json(data, filename='response.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def main():
    print(get_coinmarketcap_data('BTC'))


if __name__ == '__main__':
    main()
