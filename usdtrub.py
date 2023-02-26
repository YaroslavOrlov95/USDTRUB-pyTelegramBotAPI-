import telebot
from telebot import types
import requests
import datetime
import time
import json

"""Введите токен своего бота вместо -> BOT-TOKEN"""
bot = telebot.TeleBot('BOT-TOKEN')

@bot.message_handler(commands = ['start'])
def start(message):
    try:
        kb_kurs = types.ReplyKeyboardMarkup(True)
        item = types.KeyboardButton('Курс USDTRUB на данный момент')
        item2 = types.KeyboardButton('Конвертировать')
        kb_kurs.add(item, item2)
        bot.send_message(message.from_user.id, 'Тут ты сможешь получить курс USDT в рублях\nс сайта binance и конвертировать его\n', reply_markup = kb_kurs)
    except:
        bot.send_message(message.from_user.id, 'Вы ввели, что то неккоректное!')
@bot.message_handler(content_types = ['text'])
def kurs(message):
    try:
        user_id = message.from_user.id


        if message.text == 'Курс USDTRUB на данный момент':
            try:
                base = requests.get('https://freecurrencyrates.com/api/action.php?s=fcr&iso=RUB-USDT&f=USD&v=1&do=cvals&ln=ru')
                y = base.text
                dict_ = json.loads(y)
                g = float(dict_['RUB'])
                bot.send_message(user_id, f'{g:.2f}')
            except:
                bot.send_message(message.from_user.id, 'Вы ввели, что то неккоректное!')

        elif message.text == 'Конвертировать':
            try:
                kb_konv = types.ReplyKeyboardMarkup(True)
                item = types.KeyboardButton('Из USDT в RUB')
                item2 = types.KeyboardButton('Из RUB в USDT')
                item3 = types.KeyboardButton('Назад')
                kb_konv.add(item, item2, item3)
                bot.send_message(message.from_user.id, 'Выберите способ конвертации', reply_markup=kb_konv)
            except:
                bot.send_message(message.from_user.id, 'Вы ввели, что то неккоректное!')
        elif message.text == 'Из USDT в RUB':
            try:
                base = requests.get('https://freecurrencyrates.com/api/action.php?s=fcr&iso=RUB-USDT&f=USD&v=1&do=cvals&ln=ru')
                y = base.text
                dict_ = json.loads(y)
                r = float(dict_['RUB'])
                bot.send_message(message.from_user.id, 'Напишите сколько USDT перевести в RUB')
                bot.register_next_step_handler(message, USDTRUB, r)
            except:
                bot.send_message(message.from_user.id, 'Вы ввели, что то неккоректное!')

        elif message.text == 'Из RUB в USDT':
            try:
                base = requests.get('https://freecurrencyrates.com/api/action.php?s=fcr&iso=RUB-USDT&f=USD&v=1&do=cvals&ln=ru')
                y = base.text
                dict_ = json.loads(y)
                e = float(dict_['RUB'])
                bot.send_message(message.from_user.id, 'Напишите сколько RUB перевести в USDT')
                bot.register_next_step_handler(message, RUBUSDT, e)
            except:
                bot.send_message(message.from_user.id, 'Вы ввели, что то неккоректное!')

        elif message.text == 'Назад':
            try:
                start(message)
            except:
                bot.send_message(message.from_user.id, 'Вы ввели, что то неккоректное!')

        else:
            bot.send_message(message.from_user.id, 'Вы ввели, что то неккоректное!')

    except:
        bot.send_message(message.from_user.id, 'Вы ввели, что то неккоректное!')


def USDTRUB(message, r):
    try:
        today = datetime.datetime.today()
        f = float(message.text)
        k = f * r
        bot.send_message(message.from_user.id, f'{f} USDT = {k:.2f} рублей\n\n{time.ctime()}')
    except:
        bot.send_message(message.from_user.id, 'Вы ввели, что то неккоректное!')

def RUBUSDT(message, e):
    try:
        today = datetime.datetime.today()
        f = float(message.text)
        k = f/e
        bot.send_message(message.from_user.id, f'{f} рублей = {k:.2f} USDT\n\n{time.ctime()}')
    except:
        bot.send_message(message.from_user.id, 'Вы ввели, что то неккоректное!')
bot.polling()