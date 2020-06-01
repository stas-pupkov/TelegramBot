#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import telebot
from bs4 import BeautifulSoup

import config


from telebot import types

bot = telebot.TeleBot(config.token)

keyboard1 = types.ReplyKeyboardMarkup(True)
keyboard1.row('Привет', 'Пока', '1')
keyboard1.row('/start')



url = 'https://www.google.com/search?sxsrf=ALeKk03RR756WLVS2xpoVDpulrupdvUItA%3A1590978628310&ei=RGjUXpSGEvSLk74PvtiE4AI&q=dollar&oq=dolla&gs_lcp=CgZwc3ktYWIQAxgDMgQIABBDMgQIABBDMgQIABBDMgIIADIECAAQQzIECAAQQzIFCAAQywEyBAgAEEMyBAgAEEMyBAgAEEM6BAgAEEc6BAgjECdQoPUBWIr-AWD1jwJoAHADeACAAcEBiAG-BpIBAzAuNZgBAKABAaoBB2d3cy13aXo&sclient=psy-ab'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}



def get_currency_price():
    full_page = requests.get(url, headers=headers)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    convert = soup.findAll('span', {'class': 'DFlfde SwHCTb'})
    return convert[0].text


@bot.message_handler(commands=['start'])
def start_message(message):
    msg = f"<b>Hello {message.from_user.first_name}!</b>\nПривет, ты написал мне /start"
    bot.send_message(message.chat.id, msg, parse_mode='html', reply_markup=keyboard1)


@bot.message_handler(content_types=["text"])
def default_test(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, "Price = " + get_currency_price())


bot.polling(none_stop=True)