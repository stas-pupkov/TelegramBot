#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib

import requests
import telebot
from bs4 import BeautifulSoup

import config


from telebot import types

bot = telebot.TeleBot(config.token)

keyboard1 = types.ReplyKeyboardMarkup(True)
keyboard1.row('Привет', 'Пока')
keyboard1.row('/start')


@bot.message_handler(commands=['start'])
def start_message(message):
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    r = requests.get(url).json()
    param = r['Valute']['USD']['Value']
    bot.send_message(message.chat.id, param, reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        mess_sender = get_dollar()
        bot.send_message(message.chat.id, mess_sender.text)
    else:
        bot.send_message(message.chat.id, 'Привет, мой создатель')


def get_dollar():
    html = urllib.request.urlopen('https://www.banki.ru/products/currency/cb/').read()
    soup = BeautifulSoup(html, 'html.parser')
    head = soup.find('table', class_='standard-table--row-highlight')
    line = head.find_next(attrs={'data-test': 'currency-table-row'})
    value = line.contents[7]
    print(value)
    return value


bot.polling()