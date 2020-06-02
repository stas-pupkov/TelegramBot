from telebot import types

main_keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
main_keyboard_btn1 = types.KeyboardButton('Доллар')
main_keyboard_btn2 = types.KeyboardButton('Границы')
main_keyboard_btn3 = types.KeyboardButton('Билеты')
main_keyboard.add(main_keyboard_btn1,
                  main_keyboard_btn2,
                  main_keyboard_btn3)