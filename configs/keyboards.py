from telebot import types

from configs import config

main_keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
main_keyboard_btn1 = types.KeyboardButton('Доллар')
main_keyboard_btn2 = types.KeyboardButton('Границы')
main_keyboard_btn3 = types.KeyboardButton('Билеты')
main_keyboard.add(main_keyboard_btn1,
                  main_keyboard_btn2,
                  main_keyboard_btn3)


part_world_keyboard = types.InlineKeyboardMarkup(row_width=2)
#Открыты
part_world_keyboard_btn1 = types.InlineKeyboardButton(text=config.parts_world[0], callback_data=config.parts_world[0])
part_world_keyboard_btn2 = types.InlineKeyboardButton(text=config.parts_world[1], callback_data=config.parts_world[1])
part_world_keyboard_btn3 = types.InlineKeyboardButton(text=config.parts_world[2], callback_data=config.parts_world[2])
part_world_keyboard_btn4 = types.InlineKeyboardButton(text=config.parts_world[3], callback_data=config.parts_world[3])
part_world_keyboard_btn5 = types.InlineKeyboardButton(text=config.parts_world[4], callback_data=config.parts_world[4])
#Закрыты
part_world_keyboard_btn6 = types.InlineKeyboardButton(text=config.parts_world[5], callback_data=config.parts_world[5])
part_world_keyboard_btn7 = types.InlineKeyboardButton(text=config.parts_world[6], callback_data=config.parts_world[6])
part_world_keyboard_btn8 = types.InlineKeyboardButton(text=config.parts_world[7], callback_data=config.parts_world[7])
part_world_keyboard_btn9 = types.InlineKeyboardButton(text=config.parts_world[8], callback_data=config.parts_world[8])
part_world_keyboard_btn10 = types.InlineKeyboardButton(text=config.parts_world[9], callback_data=config.parts_world[9])
part_world_keyboard_btn11 = types.InlineKeyboardButton(text=config.parts_world[10], callback_data=config.parts_world[10])
part_world_keyboard_btn12 = types.InlineKeyboardButton(text=config.parts_world[11], callback_data=config.parts_world[11])
part_world_keyboard_url_button = types.InlineKeyboardButton(text="Ссылка на источник", url=config.url_border_countries)
part_world_keyboard.add(part_world_keyboard_btn1,
                        part_world_keyboard_btn2,
                        part_world_keyboard_btn3,
                        part_world_keyboard_btn4,
                        part_world_keyboard_btn5,
                        part_world_keyboard_btn6,
                        part_world_keyboard_btn7,
                        part_world_keyboard_btn8,
                        part_world_keyboard_btn9,
                        part_world_keyboard_btn10,
                        part_world_keyboard_btn11,
                        part_world_keyboard_btn12)
part_world_keyboard.row(part_world_keyboard_url_button)




from_city_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
from_city_keyboard_btn1 =  types.KeyboardButton('Новосибирск')
from_city_keyboard_btn2 =  types.KeyboardButton('Москва')
from_city_keyboard.add(from_city_keyboard_btn1,
                       from_city_keyboard_btn2)

data_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
data_keyboard_btn1 = types.KeyboardButton('Текущий')
data_keyboard_btn2 = types.KeyboardButton('Следующий')
data_keyboard.add(data_keyboard_btn1,
                  data_keyboard_btn2)