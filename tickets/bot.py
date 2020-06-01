#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

import requests
import telebot
from bs4 import BeautifulSoup

import config


from telebot import types

bot = telebot.TeleBot(config.token)

keyboard1 = types.ReplyKeyboardMarkup(True)
keyboard1.row('Привет', 'Пока', '1')
keyboard1.row('/start')




# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
#            'X-Access-Token': 'f14fe0ba8027435931a2f6aac4281692',
#            'Accept-Encoding': 'gzip, deflate'}



def get_fun():
    url = "http://api.travelpayouts.com/v1/prices/cheap"
    querystring = {"origin": "MOW", "destination": "HKT"}
    headers = {'X-Access-Token': 'f14fe0ba8027435931a2f6aac4281692',
               'Accept-Encoding': 'gzip'}

    ur = 'http://map.aviasales.ru/prices.json?origin_iata=ABA&period=2020-06-01:season&direct=true&one_way=false&no_visa=true&schengen=true&need_visa=true&locale=ru&min_trip_duration_in_days=1&max_trip_duration_in_days=2'

    response = requests.get(ur).json()
    # response = requests.get(url, headers=headers, params=querystring).json()
    #
    # json_str = json.dumps(response)
    # resp = json.loads(json_str)['data']['HKT']
    #
    # for (k, v) in resp.items():
    #     print(k + ' ' + str(v))

    print(response)

    output = ''

    for i in response:
        url = 'https://www.air-port-codes.com/search/results/' + i['destination']

        full_page = requests.get(url)
        soup = BeautifulSoup(full_page.content, 'html.parser')
        table = soup.findAll('table', 'small')[0]

        name = table.select('a')[0].text
        country = table.select('a')[3].text

        output += ('- ' + name + ', ' + country + '\n')

    return output


def get_countries(iata):
    ur = 'http://map.aviasales.ru/prices.json?origin_iata='+iata+'&period=2020-06-01:season&direct=true&one_way=false&no_visa=true&schengen=true&need_visa=true&locale=ru&min_trip_duration_in_days=1&max_trip_duration_in_days=2'
    response = requests.get(ur).json()


@bot.message_handler(commands=['start'])
def start_message(message):
    msg = f"<b>Hello {message.from_user.first_name}!</b>\nПривет, ты написал мне /start"
    bot.send_message(message.chat.id, msg, parse_mode='html', reply_markup=keyboard1)


@bot.message_handler(content_types=["text"])
def default_test(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, get_fun())


bot.polling(none_stop=True)