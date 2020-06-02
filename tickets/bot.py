#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

import requests
import telebot
from bs4 import BeautifulSoup

from configs import config

from telebot import types


bot = telebot.TeleBot(config.token)

keyboard1 = types.ReplyKeyboardMarkup(True)
keyboard1.row('Привет', 'ABAs', 'OVB')
keyboard1.row('/start')


def get_info_ticket(chat_id, from_city, month):
    response = get_tickets(from_city, month)
    url = 'https://www.aviasales.ru/search/'
    if 'Error' in str(response):
        bot.send_message(chat_id, response)
    else:
        counter = 0
        for ticket in response:
            ticket = json.loads(ticket)
            destination_iata = ticket['destination']
            airport, country = get_info_iata(destination_iata)
            if country in config.europe:
                price = ticket['value']
                if len(str(price)) < 8:
                    depart_date = str(ticket['depart_date'])
                    return_date = str(ticket['return_date'])
                    transfer = str(ticket['number_of_changes'])
                    msg = ('- ' + airport + ', ' + country
                           + '\nPrice: ' + str(price) + ' rub'
                           + '\nDepart: ' + depart_date
                           + '\nReturn: ' + return_date
                           + '\nTransfer: ' + transfer)

                    depart_day = str(depart_date)[8:9]
                    depart_month = str(depart_date)[6:7]
                    return_day = str(depart_date)[8:9]
                    return_month = str(depart_date)[6:7]
                    website = url \
                              + from_city \
                              + depart_day \
                              + depart_month \
                              + destination_iata \
                              + return_day \
                              + return_month \
                              + '1'
                    keyboard = types.InlineKeyboardMarkup()
                    url_button = types.InlineKeyboardButton(text='Посмотреть на Aviasales', url=website)
                    keyboard.add(url_button)
                    bot.send_message(chat_id, msg, reply_markup=keyboard)
                    counter = counter + 1
                    if counter > 3:
                        break



def get_tickets(from_city, month):
    if len(str(from_city)) != 3:
        return 'Error: неверный город отправления'
    if str(month).replace('-', '').isdigit() is not True:
        return 'Error: неверный месяц отправления'

    url = 'http://map.aviasales.ru/prices.json'
    querystring = {'origin_iata': from_city,
                   'period': month + ':month',
                   'locale': 'ru'}
    response = requests.get(url, params=querystring).json()

    output = []
    for i in response:
        output.append(str(i)
                      .replace('\'', '\"')
                      .replace('True', 'true')
                      .replace('False', 'false'))
    output = sorted(output)
    if len(output) != 0:
        return output
    else:
        return 'Error: неверный данные отправления'


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
    #msg = get_info_ticket(message.text)
    #if message.text == '1':
    get_info_ticket(message.chat.id, message.text, '2020-06-01')
        #bot.send_message(message.chat.id, msg)
    # else:
    #     bot.send_message(message.chat.id, "Empty")
    bot.send_message(message.chat.id, "Поиск закончен")


bot.polling(none_stop=True)