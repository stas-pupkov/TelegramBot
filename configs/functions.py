import requests
import telebot
from bs4 import BeautifulSoup

from configs import config

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


def select_fun_for_part_world(message):
    part = ''
    title = message.text
    list_parts_world = config.parts_world
    if list_parts_world[0] in title:
        return can_travel_country_europe()




@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == config.parts_world[0]:
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
