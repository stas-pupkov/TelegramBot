import requests
from bs4 import BeautifulSoup

from configs import config




def get_dollar_cb():
    body = requests.get(config.url_dollar_cb).json()
    value = str(body['Valute']['USD']['Value'])
    date_pub = str(body['Date']).replace('T', ' ').replace('+03:00', '')
    return value, date_pub



def get_dollar_google():
    full_page = requests.get(config.url_dollar_google, headers=config.headers_dollar_google)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    price = soup.findAll('span', {'class': 'DFlfde SwHCTb'})
    price = price[0].text
    for el in soup.select('#knowledge-currency__updatable-data-column'):
        data_pub = el.select('.hqAUc ')[0].text
        data_pub = str(data_pub).replace(' · Отказ от обязательств', '')
    return price, data_pub