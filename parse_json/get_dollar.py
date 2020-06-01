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

url_google = 'https://www.google.com/search?sxsrf=ALeKk03RR756WLVS2xpoVDpulrupdvUItA%3A1590978628310&ei=RGjUXpSGEvSLk74PvtiE4AI&q=dollar&oq=dolla&gs_lcp=CgZwc3ktYWIQAxgDMgQIABBDMgQIABBDMgQIABBDMgIIADIECAAQQzIECAAQQzIFCAAQywEyBAgAEEMyBAgAEEMyBAgAEEM6BAgAEEc6BAgjECdQoPUBWIr-AWD1jwJoAHADeACAAcEBiAG-BpIBAzAuNZgBAKABAaoBB2d3cy13aXo&sclient=psy-ab'
url_cb = 'https://www.cbr-xml-daily.ru/daily_json.js'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}



@bot.message_handler(commands=['start'])
def start_message(message):
    msg = f"<b>Hello {message.from_user.first_name}!</b>\nПривет, ты написал мне /start"
    bot.send_message(message.chat.id, msg, parse_mode='html', reply_markup=keyboard1)


def get_dollar_cb():
    body = requests.get(url_cb).json()
    value = str(body['Valute']['USD']['Value'])
    date_pub = str(body['Date']).replace('T', ' ').replace('+03:00', '')
    return value, date_pub



def get_dollar_google():
    full_page = requests.get(url_google, headers=headers)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    price = soup.findAll('span', {'class': 'DFlfde SwHCTb'})
    price = price[0].text
    for el in soup.select('#knowledge-currency__updatable-data-column'):
        data_pub = el.select('.hqAUc ')[0].text
        data_pub = str(data_pub).replace(' · Отказ от обязательств', '')
    return price, data_pub


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        price, publish = get_dollar_cb()
        bot.send_message(message.chat.id, 'Курс ЦБ: ' + price + '\n' + publish)
    if message.text.lower() == 'пока':
        price, publish = get_dollar_google()
        bot.send_message(message.chat.id, 'Курс инет: ' + price + '\n' + publish)



bot.polling(none_stop=True)