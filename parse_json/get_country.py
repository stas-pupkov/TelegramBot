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


@bot.message_handler(commands=['start'])
def start_message(message):
    url = 'https://www.iatatravelcentre.com/international-travel-document-news/1580226297.htm'
    r = requests.get(url).text
    a = r.find('RU: ')
    b = r[a: a + 5000]
    c = b[: b.find(',\n gdpAdjusted:') - 1]
    print(c)
    param = c.replace('&#32;', ' ').replace('<br/>', '\n').replace('{\ngdp: \'', '\n')
    print(param)
    bot.send_message(message.chat.id, param, reply_markup=keyboard1)


# @bot.message_handler(content_types=['text'])
# def send_text(message):
#     if message.text.lower() == 'привет':
#         mess_sender = get_country()
#         bot.send_message(message.chat.id, mess_sender)
#     else:
#         bot.send_message(message.chat.id, 'Привет, мой создатель')


def get_country():
    html = urllib.request.urlopen('https://www.wanderlust.co.uk/content/coronavirus-travel-updates/').read()
    soup = BeautifulSoup(html, 'html.parser')
    head = soup.find_all('li')
    #line = head.find_next(attrs={'data-test': 'currency-table-row'})
    #value = line.contents[7]
    print(head)
    output = ''
    for i in head:
        i = i.get_text()
        output += ('- "'+i+'",\n')
    return output


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        mess_sender = get_can_travel_country()
        bot.send_message(message.chat.id, mess_sender)
    if message.text.lower() == 'пока':
        mess_sender = get_cant_travel_country()
        bot.send_message(message.chat.id, mess_sender)



def get_cant_travel_country():
    url = 'https://www.wanderlust.co.uk/content/coronavirus-travel-updates/'
    body = requests.get(url).text
    begin = body.find('Which European countries have travel restrictions?')
    b = body[begin: begin + 6000]
    need_part = b[: b.find('Which European countries you can still travel to?') - 1]

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
        output += ('- ' + i + '\n')
    return output


def get_can_travel_country():
    url = 'https://www.wanderlust.co.uk/content/coronavirus-travel-updates/'
    body = requests.get(url).text
    begin = body.find('Which European countries you can still travel to?')
    b = body[begin: begin + 6000]
    need_part = b[: b.find('<h2 style="text-align: center;"><a name="usa"></a>North America</h2>') - 1]

    need_part = need_part.replace('<li>', '')\
        .replace('<span>', '')\
        .replace('</span>', '')\
        .replace('<br />', '')\
        .replace('<br /><br />', '')\
        .replace('</li>', '') \
        .replace('<p>', '') \
        .replace('</p>', '') \
        .replace('<ul>', '')\
        .replace('<li style="text-align: left;">', '\n')\
        .replace('</h3>', '')
    need_part = need_part.replace(': ', '')
    need_part = need_part.replace(':', '')
    param = need_part.replace('<strong></strong>', '')
    countries_list = param.split('<strong>')
    del countries_list[0]

    output = ''
    for i in countries_list:
        i = i[0: i.find('</strong>')]
        output += ('- ' + i + '\n')
    return output


bot.polling()