import json
from datetime import datetime

import requests
import telebot
from bs4 import BeautifulSoup
from telebot import types

from configs import config, keyboards

bot = telebot.TeleBot(config.token)


def get_dollar_cb():
    body = requests.get(config.url_dollar_cb).json()
    value = str(body['Valute']['USD']['Value'])
    date_pub = str(body['Date']).replace('T', ' ').replace('+03:00', '')
    return value, date_pub



def get_dollar_google():
    full_page = requests.get(config.url_dollar_google, headers=config.headers_dollar_google)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    price = soup.findAll('span', {'class': 'DFlfde SwHCTb'})
    price = price[0].text
    for el in soup.select('#knowledge-currency__updatable-data-column'):
        data_pub = el.select('.hqAUc ')[0].text
        data_pub = str(data_pub).replace(' · Отказ от обязательств', '')
    return price, data_pub


def get_list_countries(question1, question2):
    body = requests.get(config.url_border_countries).text
    begin = body.find(question1)
    b = body[begin: begin + config.long_body]
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


def get_data_for_list_countries():
    full_page = requests.get(config.url_border_countries)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    current_date = soup.findAll('h4', {'class': 'byline'})[0].text
    current_date = str(current_date)\
        .replace('Rosie Fitzgerald  |', '')\
        .replace('  ', '').replace('\n', '')
    return current_date


def cant_travel_country_europe():
    return get_list_countries(config.questions_borders[0], config.questions_borders[1])


def can_travel_country_europe():
    return get_list_countries(config.questions_borders[1], config.questions_borders[2])


def cant_travel_country_north():
    return get_list_countries(config.questions_borders[2], config.questions_borders[3])


def can_travel_country_north():
    return get_list_countries(config.questions_borders[3], config.questions_borders[4])


def cant_travel_country_south():
    return get_list_countries(config.questions_borders[4], config.questions_borders[5])


def cant_travel_country_asia():
    return get_list_countries(config.questions_borders[5], config.questions_borders[6])


def can_travel_country_asia():
    return get_list_countries(config.questions_borders[6], config.questions_borders[7])


def cant_travel_country_africa():
    return get_list_countries(config.questions_borders[7], config.questions_borders[8])


def can_travel_country_africa():
    return get_list_countries(config.questions_borders[8], config.questions_borders[9])


def cant_travel_country_pacific():
    return get_list_countries(config.questions_borders[9], config.questions_borders[10])


def cant_travel_country_caribbean():
    return get_list_countries(config.questions_borders[10], config.questions_borders[11])


def can_travel_country_caribbean():
    return get_list_countries(config.questions_borders[11], config.questions_borders[12])


def get_tickets(from_city, date):
    querystring = {'origin_iata': from_city,
                   'period': date + '01:month',
                   'locale': 'ru'}
    response = requests.get(config.url_aviasales, params=querystring).json()

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
    url = config.url_iata_info + iata
    full_page = requests.get(url)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    table = soup.findAll('table', 'small')[0]
    airport = table.select('a')[0].text
    country = table.select('a')[3].text
    return airport, country


def get_message_one_ticket(ticket, chat_id, from_city, airport, country, destination_iata):
    price = ticket['value']
    if len(str(price)) < 8:
        depart_date = str(ticket['depart_date'])
        return_date = str(ticket['return_date'])
        transfer = str(ticket['number_of_changes'])
        msg = ('- ' + airport + ', ' + country
               + '\nЦена билета: ' + str(price) + ' рублей'
               + '\nОтправление: ' + depart_date
               + '\nВозвращение: ' + return_date
               + '\nПересадок: ' + transfer)

        depart_day = str(depart_date)[8:9]
        depart_month = str(depart_date)[6:7]
        return_day = str(depart_date)[8:9]
        return_month = str(depart_date)[6:7]
        website = config.url_aviasales_search \
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


def get_info_tickets(chat_id, from_city, date):
    response = get_tickets(from_city, date)
    if 'Error' in str(response):
        bot.send_message(chat_id, response)
    else:
        for ticket in response:
            ticket = json.loads(ticket)
            destination_iata = ticket['destination']
            airport, country = get_info_iata(destination_iata)
            if country in config.europe:
                counter = 0
                bot.send_message(chat_id, 'В Европе')
                get_message_one_ticket(ticket,
                                       chat_id,
                                       from_city,
                                       airport,
                                       country,
                                       destination_iata)
                counter = counter + 1
                if counter > 2:
                    break




    bot.send_message(chat_id, 'Поиск завершен')