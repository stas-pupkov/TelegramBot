#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime

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
        value_website = functions.get_dollar_website()
        msg = 'Курс от ЦБ: ' \
              + '\n' + f"<b>{value_cb}</b>" + ' рублей' \
              + '\nОпубликован: ' + published_cb \
              + '\n\nКурс от ProFinance:'\
              + '\n' + f"<b>{value_website}</b>" + ' рублей'
        bot.send_message(message.chat.id, msg, parse_mode='html')

    if message.text == 'Границы':
        bot.send_message(message.chat.id, 'Выбери категорию', reply_markup=keyboards.part_world_keyboard)
    if message.text == 'Билеты':
        msg = bot.send_message(message.chat.id, 'Выбери город вылета', reply_markup=keyboards.from_city_keyboard)
        bot.register_next_step_handler(msg, ask_month)




def ask_month(message):
    iata = list(config.departure_cities.keys())[list(config.departure_cities.values()).index(message.text)]
    config.departure_city = iata
    msg = bot.send_message(message.chat.id, 'Выбери месяц вылета', reply_markup=keyboards.data_keyboard)
    bot.register_next_step_handler(msg, ask_tickets)


def ask_tickets(message):
    now = datetime.datetime.now()
    if message.text == 'Текущий':
        config.departure_date = str(now)[:8]
    elif message.text == 'Следующий':
        if now.month < 10:
            config.departure_date = str(now)[:8].replace(str(now)[5:7], '0' + str(now.month + 1))
        else:
            if now.month == 12:
                config.departure_date = str(now)[:8]\
                    .replace(str(now)[:3], now.year + 1)\
                    .replace(str(now)[5:7], '01')
            else:
                config.departure_date = str(now)[:8].replace(str(now)[5:7], '0' + str(now.month + 1))

    bot.send_message(message.chat.id, 'Поиск авиабилетов...'
                     + '\n\nПоиск завершится, когда появится сообщение '
                     + '"Поиск завершен"', reply_markup=keyboards.main_keyboard)
    functions.get_info_tickets(message.chat.id, config.departure_city, config.departure_date)


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