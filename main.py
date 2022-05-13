import os
import json
import requests
from requests import Session
import schedule
import logging
from bs4 import BeautifulSoup
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

# def bot_send_text(bot_message):
    
#     bot_token = os.environ['TOKEN']
#     bot_chatID = os.environ['CHAT_ID']
#     send_text = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={bot_chatID}&parse_mode=Markdown&text={bot_message}'

#     response = requests.get(send_text)

#     return response


# COIN = 'verasity-vra'

# def bot_scraping(currency: str = 'USD'):
#     url = requests.get(f'https://awebanalysis.com/es/coin-details/{COIN}/{currency}')
#     soup = BeautifulSoup(url.content, 'html.parser')
#     result = soup.find('td', {'class': 'wbreak_word align-middle coin_price'})
#     format_result = result.text

#     return format_result


def send_tweet():
    vra_price = f'${get_price()} | €{get_price(currency="EUR")} \n#verasity $VRA'
    twitter = create_twitter_api()
    twitter.update_status(status=vra_price)
    logger.info("tweet sent!")


if __name__ == '__main__':
  schedule.every().hour.at(":00").do(send_tweet)

  while True:
    schedule.run_pending()