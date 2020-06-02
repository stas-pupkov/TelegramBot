import re

import requests
import telebot
from telebot import types

from configs import config

bot = telebot.TeleBot(config.token)

keyboard1 = types.ReplyKeyboardMarkup(True)
keyboard1.row('Привет', 'Пока')
keyboard1.row('/start')


@bot.message_handler(commands=['start'])
def start_message(message):
    print(get_image_url())
    bot.send_photo(message.chat.id, get_image_url(), reply_markup=keyboard1)



def get_image_url():
    allowed_extension = ['jpg', 'jpeg', 'png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    return url


def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url

bot.polling()