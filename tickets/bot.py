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

    ur = 'http://map.aviasales.ru/prices.json?origin_iata=OVB&period=2020-06-01:season&direct=true&one_way=false&no_visa=true&schengen=true&need_visa=true&locale=ru&min_trip_duration_in_days=13&max_trip_duration_in_days=15'

    response = requests.get(ur).json()
    # response = requests.get(url, headers=headers, params=querystring).json()
    #
    # json_str = json.dumps(response)
    # resp = json.loads(json_str)['data']['HKT']
    #
    # for (k, v) in resp.items():
    #     print(k + ' ' + str(v))

    for i in response:
        print(i)

    return str(response['data'])



@bot.message_handler(commands=['start'])
def start_message(message):
    msg = f"<b>Hello {message.from_user.first_name}!</b>\nПривет, ты написал мне /start"
    bot.send_message(message.chat.id, msg, parse_mode='html', reply_markup=keyboard1)


@bot.message_handler(content_types=["text"])
def default_test(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, get_fun())


bot.polling(none_stop=True)