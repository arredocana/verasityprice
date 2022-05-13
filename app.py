import os
import json
from requests import Session
import schedule
import logging
from config import create_twitter_api

# create logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# COINMARKETCAP

API_KEY = os.environ['COINMARKETCAP']


url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': API_KEY,
}

session = Session()
session.headers.update(headers)

def get_price(coin_id='3816', currency='USD'):
  parameters = {
    'id': coin_id,
    'convert': currency
    }
  try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    price = round(data['data'][coin_id]['quote'][currency]['price'], 6)
    return price
  except (ConnectionError, Timeout, TooManyRedirects):
    return 0

def send_tweet():
    vra_price = f'${get_price()} | €{get_price(currency="EUR")} \n#verasity $VRA'
    twitter = create_twitter_api()
    twitter.update_status(status=vra_price)
    logger.info("tweet sent!")


if __name__ == '__main__':
  schedule.every(2).minutes.do(send_tweet)

  while True:
    schedule.run_pending()