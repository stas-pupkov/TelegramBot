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
keyboard1.row('Привет', 'ABA', 'OVB')
keyboard1.row('/start')


def get_fun(from_city):
    response = get_countries(from_city)
    if 'Unknown city iata' in str(response):
        return 'Error'
    else:
        output = ''
        for i in response:
            price = i['value']

            if price < 40000:
                destination_iata = i['destination']
                airport, country = get_info_iata(destination_iata)
                if country in config.europe:
                    output += ('- ' + airport + ', ' + country + '\nPrice: ' + str(price) + ' rub\n\n')
    return output


def get_countries(from_city):
    url = 'http://map.aviasales.ru/prices.json'
    querystring = {'origin_iata': from_city,
                   'period': '2020-06-01:month',
                   'direct': True,
                   'one_way': True,
                   'no_visa': True,
                   'schengen': True,
                   'need_visa ': True,
                   'locale': 'ru',
                   'min_trip_duration_in_days ': 1,
                   'max_trip_duration_in_days ': 2}
    response = requests.get(url, params=querystring).json()
    for i in response:
        print(i)
    return response


def get_info_iata(iata):
    url = 'https://www.air-port-codes.com/search/results/' + iata
    full_page = requests.get(url)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    table = soup.findAll('table', 'small')[0]

    airport = table.select('a')[0].text
    country = table.select('a')[3].text

    return airport, country



@bot.message_handler(commands=['start'])
def start_message(message):
    msg = f"<b>Hello {message.from_user.first_name}!</b>\nПривет, ты написал мне /start"
    bot.send_message(message.chat.id, msg, parse_mode='html', reply_markup=keyboard1)


@bot.message_handler(content_types=["text"])
def default_test(message):
    bot.send_message(message.chat.id, "Wait a second...")
    msg = get_fun(message.text)
    if len(msg) > 0:
        bot.send_message(message.chat.id, msg)
    else:
        bot.send_message(message.chat.id, "Empty")

bot.polling(none_stop=True)