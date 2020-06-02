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

    if message.text == 'Границы':
        bot.send_message(message.chat.id, 'Где?', reply_markup=keyboards.part_world_keyboard)





@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    chat_id = call.message.chat.id
    if config.parts_world.index(str(call.data)) < 5:
        permission = 'Страны с открытыми границами в '
    else:
        permission = 'Страны с закрытыми границами в '
    if call.message:
        msg = permission + '"' + str(call.data)[4:] \
                         + '"' \
                         + ' на ' \
                         + functions.get_data_for_list_countries()
        bot.send_message(chat_id, msg)
        if call.data == config.parts_world[0]:
            bot.send_message(chat_id, functions.can_travel_country_europe())
        elif call.data == config.parts_world[1]:
            bot.send_message(chat_id, functions.can_travel_country_north())
        elif call.data == config.parts_world[2]:
            bot.send_message(chat_id, functions.can_travel_country_asia())
        elif call.data == config.parts_world[3]:
            bot.send_message(chat_id, functions.can_travel_country_africa())
        elif call.data == config.parts_world[4]:
            bot.send_message(chat_id, functions.can_travel_country_caribbean())
        elif call.data == config.parts_world[5]:
            bot.send_message(chat_id, functions.cant_travel_country_europe())
        elif call.data == config.parts_world[6]:
            bot.send_message(chat_id, functions.cant_travel_country_north())
        elif call.data == config.parts_world[7]:
            bot.send_message(chat_id, functions.cant_travel_country_south())
        elif call.data == config.parts_world[8]:
            bot.send_message(chat_id, functions.cant_travel_country_asia())
        elif call.data == config.parts_world[9]:
            bot.send_message(chat_id, functions.cant_travel_country_africa())
        elif call.data == config.parts_world[10]:
            bot.send_message(chat_id, functions.cant_travel_country_pacific())
        elif call.data == config.parts_world[11]:
            bot.send_message(chat_id, functions.cant_travel_country_caribbean())


bot.polling(none_stop=True)