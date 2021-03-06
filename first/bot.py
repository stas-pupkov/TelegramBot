#!/usr/bin/python
# -*- coding: utf-8 -*-

import telebot
from telegram_bot import config
import os


from telebot import types

bot = telebot.TeleBot(config.token)

keyboard1 = types.ReplyKeyboardMarkup(True)
keyboard1.row('Привет', 'Пока')
keyboard1.row('/start')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup=keyboard1)

    #работа с файлами из других директорий
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    filename = os.path.join(fileDir, '../stickers/sticker.webp')
    filename = os.path.abspath(os.path.realpath(filename))
    sti = open(filename, 'rb')
    bot.send_sticker(message.chat.id, sti)



@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет, мой создатель')
    if message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Прощай, создатель')
    if message.text == 'Love':
        bot.send_sticker(message.chat.id, 'CAADAgADUAkAAnlc4gn1AAE2sQABMfNIAg')
    if message.text == '1':
        msg = bot.send_message(message.chat.id, 'Сколько вам лет?')
        bot.register_next_step_handler(msg, askAge)


def askAge(message):
    chat_id = message.chat.id
    text = message.text
    if not text.isdigit():
        msg = bot.send_message(chat_id, 'Возраст должен быть числом, введите ещё раз.')
        bot.register_next_step_handler(msg, askAge) #askSource
        return
    msg = bot.send_message(chat_id, 'Спасибо, я запомнил что вам ' + text + ' лет.')



bot.polling()
