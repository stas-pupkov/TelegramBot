#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import telebot

import config


from telebot import types

bot = telebot.TeleBot(config.token)

keyboard1 = types.ReplyKeyboardMarkup(True)



keyboard1.row('Привет', 'Пока')
keyboard1.row('/start')

url = 'https://www.wanderlust.co.uk/content/coronavirus-travel-updates/'
body = requests.get(url).text
long_body = 7000

keyboard = types.InlineKeyboardMarkup(row_width=4)
button1 = types.InlineKeyboardButton(text="Eu Can't", callback_data="EuNo")
button2 = types.InlineKeyboardButton(text="Eu Can", callback_data="EuYes")
button3 = types.InlineKeyboardButton(text="Nor Can't", callback_data="NorNo")
button4 = types.InlineKeyboardButton(text="Nor Can", callback_data="NorYes")
button5 = types.InlineKeyboardButton(text="Sou Can't", callback_data="SouNo")
button6 = types.InlineKeyboardButton(text="As Can't", callback_data="AsNo")
button7 = types.InlineKeyboardButton(text="As Can", callback_data="AsYes")
button8 = types.InlineKeyboardButton(text="Af Can't", callback_data="AfNo")
button9 = types.InlineKeyboardButton(text="Af Can", callback_data="AfYes")
button10 = types.InlineKeyboardButton(text="Pac Can't", callback_data="PacNo")
button11 = types.InlineKeyboardButton(text="Car Can't", callback_data="CarNo")
button12 = types.InlineKeyboardButton(text="Car Can", callback_data="CarYes")
url_button = types.InlineKeyboardButton(text="Resource website", url=url)
keyboard.add(button1,
             button2,
             button3,
             button4,
             button5,
             button6,
             button7,
             button8,
             button9,
             button10,
             button11,
             button12)
keyboard.row(url_button)

questions = [
        'Which European countries have travel restrictions?',
        'Which European countries you can still travel to?',
        'Which North American places have travel restrictions?',
        'Which North American countries have their borders open?',
        'Which Central and South America Countries have travel restrictions?',
        'Which Asian countries have travel restrictions?',
        'Which Asian countries have their borders open?',
        'Which African countries have travel restrictions?',
        'Which African countries still have their borders open?',
        'Which South Pacific countries can you not travel to?',
        'Which Caribbean countries have travel restrictions?',
        'Which Caribbean countries still have their borders open?',
        'Can\'t wait to travel again?'
    ]

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == '1':
        mess_sender = cant_travel_country_europe()
        bot.send_message(message.chat.id, mess_sender)
    if message.text.lower() == 'привет':
        keyboard2 = types.InlineKeyboardMarkup(row_width=1)

        keyboard2.add(url_button)
        bot.send_message(message.chat.id, 'Country', reply_markup=keyboard)


def get_list_countries(question1, question2):
    begin = body.find(question1)
    b = body[begin: begin + long_body]
    need_part = b[: b.find(question2)]
    need_part = need_part.replace('<li>', '') \
        .replace('<span>', '') \
        .replace('</span>', '') \
        .replace('<br />', '') \
        .replace('<br /><br />', '') \
        .replace('</li>', '') \
        .replace('<p>', '') \
        .replace('</p>', '') \
        .replace('<ul>', '') \
        .replace('<li style="text-align: left;">', '\n') \
        .replace('</h3>', '')
    need_part = need_part.replace(': ', '')
    need_part = need_part.replace(':', '')
    param = need_part.replace('<strong></strong>', '')
    countries_list = param.split('<strong>')
    del countries_list[0]

    output = ''
    for i in countries_list:
        i = i[0: i.find('</strong>')]
        if len(i) > 0 and i[0].isupper():
            output += ('- ' + i + '\n')
    return output


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "EuNo":
            bot.send_message(call.message.chat.id, cant_travel_country_europe())
        if call.data == "EuYes":
            bot.send_message(call.message.chat.id, can_travel_country_europe())
        if call.data == "NorNo":
            bot.send_message(call.message.chat.id, cant_travel_country_north())
        if call.data == "NorYes":
            bot.send_message(call.message.chat.id, can_travel_country_north())
        if call.data == "SouNo":
            bot.send_message(call.message.chat.id, cant_travel_country_south())
        if call.data == "AsNo":
            bot.send_message(call.message.chat.id, cant_travel_country_asia())
        if call.data == "AsYes":
            bot.send_message(call.message.chat.id, can_travel_country_asia())
        if call.data == "AfNo":
            bot.send_message(call.message.chat.id, cant_travel_country_africa())
        if call.data == "AfYes":
            bot.send_message(call.message.chat.id, can_travel_country_africa())
        if call.data == "PacNo":
            bot.send_message(call.message.chat.id, cant_travel_country_pacific())
        if call.data == "CarNo":
            bot.send_message(call.message.chat.id, cant_travel_country_caribbean())
        if call.data == "CarYes":
            bot.send_message(call.message.chat.id, can_travel_country_caribbean())




def cant_travel_country_europe():
    return get_list_countries(questions[0], questions[1])


def can_travel_country_europe():
    return get_list_countries(questions[1], questions[2])


def cant_travel_country_north():
    return get_list_countries(questions[2], questions[3])


def can_travel_country_north():
    return get_list_countries(questions[3], questions[4])


def cant_travel_country_south():
    return get_list_countries(questions[4], questions[5])


def cant_travel_country_asia():
    return get_list_countries(questions[5], questions[6])


def can_travel_country_asia():
    return get_list_countries(questions[6], questions[7])


def cant_travel_country_africa():
    return get_list_countries(questions[7], questions[8])


def can_travel_country_africa():
    return get_list_countries(questions[8], questions[9])


def cant_travel_country_pacific():
    return get_list_countries(questions[9], questions[10])


def cant_travel_country_caribbean():
    return get_list_countries(questions[10], questions[11])


def can_travel_country_caribbean():
    return get_list_countries(questions[11], questions[12])




bot.polling(none_stop=True)