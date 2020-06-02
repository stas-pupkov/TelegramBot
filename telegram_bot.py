#!/usr/bin/python
# -*- coding: utf-8 -*-

import telebot

from configs import keyboards, config, functions

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def start_message(message):
    msg = f"<b>Hello {message.from_user.first_name}!</b>\nПривет"
    bot.send_message(message.chat.id, msg, parse_mode='html', reply_markup=keyboards.main_keyboard)


@bot.message_handler(content_types=['text'])
def getting_information(message):
    if message.text == 'Доллар':
        value_cb, published_cb = functions.get_dollar_cb()
        value_google, published_google = functions.get_dollar_google()
        bot.send_message(message.chat.id,
                         'Курс от ЦБ: ' + value_cb
                         + '\nОпубликован: ' + published_cb
                         + '\n\nКурс от Google: ' + value_google
                         + '\nОпубликован: ' + published_google)





bot.polling(none_stop=True)