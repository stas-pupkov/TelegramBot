#!/usr/bin/python
# -*- coding: utf-8 -*-

import telebot
from configs import config

from telebot import types

bot = telebot.TeleBot(config.token)

keyboard1 = types.ReplyKeyboardMarkup(True)
keyboard1.row('Привет', 'Пока', '1')
keyboard1.row('/start')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup=keyboard1)



@bot.message_handler(content_types=["text"])
def default_test(message):
    if message.text.lower() == 'привет':
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text="Перейти на Яндекс", url="https://ya.ru")
        keyboard.add(url_button)
        bot.send_message(message.chat.id, "Привет! Нажми на кнопку и перейди в поисковик.", reply_markup=keyboard)
    if message.text.lower() == 'пока':
        any_message(message)
    if message.text.lower() == '1':
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        callback_button = types.InlineKeyboardButton(text="Нажми меня", callback_data="test")
        callback_button2  = types.InlineKeyboardButton(text="Нажми меня2", callback_data="test2")
        keyboard.add(callback_button, callback_button2)
        bot.send_message(message.chat.id, "Я – сообщение из обычного режима", reply_markup=keyboard)


@bot.message_handler(func=lambda message: True)
def any_message(message):
    bot.reply_to(message, "Сам {!s}".format(message.text))






@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    if call.message:
        if call.data == "test":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Пыщь")
        if call.data == "test2":
            bot.send_message(call.message.chat.id, 'Hi')
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text='333')



@bot.inline_handler(lambda query: query.query)
def query_text(inline_query):
    print(inline_query)
    try:
        r = types.InlineQueryResultArticle('1', 'Result', types.InputTextMessageContent('Result message.'))
        r2 = types.InlineQueryResultArticle('2', 'Result2', types.InputTextMessageContent('Result message2.'))
        bot.answer_inline_query(inline_query.id, [r, r2])
    except Exception as e:
        print(e)


bot.polling()