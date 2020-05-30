#!/usr/bin/python
# -*- coding: utf-8 -*-

import telebot
import config

types = telebot.types

bot = telebot.TeleBot(config.token)

keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
keyboard1.row('Привет', 'Пока')
keyboard1.row('/start')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет, мой создатель')
    if message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Прощай, создатель')
    if message.text == 'Love':
        bot.send_sticker(message.chat.id, 'CAADAgADUAkAAnlc4gn1AAE2sQABMfNIAg')


bot.polling()
