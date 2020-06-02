#!/usr/bin/python
# -*- coding: utf-8 -*-

import telebot
from configs import config

from telebot import types

bot = telebot.TeleBot(config.token)

keyboard = types.ReplyKeyboardMarkup(True)
btn_address = types.KeyboardButton('Address', request_location=True)
keyboard.row('/start')
keyboard.row('Привет')
keyboard.add(btn_address)

# НЕ работает
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup=keyboard)


@bot.message_handler(content_types=['location'])
def send_text(message):
    bot.send_message(message.chat.id, 'Locat')
    lon = message.location.longitude
    lat = message.location.latitude

    print(message.location)

    bot.send_message(message.chat.id, "Locat", reply_markup=keyboard)
    bot.send_venue(message.chat.id, lat, lon, "Home")







bot.polling()