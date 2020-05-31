#!/usr/bin/python
# -*- coding: utf-8 -*-
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
    URL = 'https://api.telegram.org/bot' + config.token + '/'
    url = URL + 'getMe'
    r = requests.get(url).json()
    print(r)
    param = r['result']['username']

    bot.send_message(message.chat.id, param, reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        mess_sender = get_head(get_html('https://kurs2015.ru/kurs-dollara-onlajn.html'))
        text = ''
        for text_tmp in mess_sender:
            text = text + text_tmp + '\n' + '\n'
        bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, 'Привет, мой создатель')


def get_html(url):
    r = requests.get(url)
    r.encoding = 'utf8'
    return r.text


def get_head(html):
    soup = BeautifulSoup(html, 'html')
    head = soup.find('main', id='content').find_next('h2')
    heads = []
    for i in head:
       heads.append(i.string)
    return heads


bot.polling()