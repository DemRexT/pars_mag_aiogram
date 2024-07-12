import os

from aiogram import Bot, Dispatcher, types, executor
from aiogram import types

from pyaterochka_parser_js import pyaterochka_main
from magnit_parser_js import magnit_main
from fasol_parser import fasol_main

import datetime


import logging

TOKEN = token

bot = Bot(TOKEN)
dp = Dispatcher(bot)



logging.basicConfig(level=logging.INFO)
# logging.info("вывод в консоль")

current_date = datetime.datetime.now().strftime('%m-%d')

first_text = '''
Здравствуйте! 
Этот бот поможет вам узнать все скидки и акции
в популярных торговых точках города Санкт-Петербург. 
'''



@dp.message_handler(commands = "start")
async def start_command(message: types.Message, ):
    keyboard = types.ReplyKeyboardMarkup()
    button_1 = types.KeyboardButton(text="Магнит")
    button_2 = types.KeyboardButton(text="Пятерочка")
    button_3 = types.KeyboardButton(text="Фасоль")
    keyboard.add(button_1, button_2, button_3)
    await message.reply(text=first_text, reply_markup=keyboard)


@dp.message_handler(lambda message: message.text.lower() == "магнит")
async def magnit_parser(message: types.Message, ):
    chat_id = message.chat.id
    await bot.send_message(chat_id, 'Подождите...')
    name = await magnit_main()
    with open(name, 'rb') as file:
        await message.answer_document(file)
    os.remove(name)


@dp.message_handler(lambda message: message.text.lower() == "пятерочка")
async def pyaterochka_parser(message: types.Message, ):
    chat_id = message.chat.id
    await bot.send_message(chat_id, 'Подождите...')
    name = await pyaterochka_main()
    with open(name, 'rb') as file:
        await message.answer_document(file)
    os.remove(name)


@dp.message_handler(lambda message: message.text.lower() == "фасоль")
async def fasol_parser(message: types.Message, ):
    chat_id = message.chat.id
    await bot.send_message(chat_id, 'Подождите...')
    name = await fasol_main()
    with open(name, 'rb') as file:
        await message.answer_document(file)
    os.remove(name)





if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
