import telebot

from extensions import Converter
from tok import TOKEN, currencies

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.reply_to(message, 'Данный бот рассчитывает конвертацию валют на базе актуального курса ЦБ РФ.'
                          '\nФормат команд: <исходная валюта> <конечная валюта> <объём перевода исходной валюты>.'
                          '\nИспользуйте стандартные трёхбуквенные коды валют.'
                          '\nКоманда /values выводит перечень доступных валют с их кодами')

@bot.message_handler(commands=['values'])
def handle_values(message):
    text = 'Доступные валюты:'
    for i in currencies.keys():
        text = text + '\n' + i + ': ' + currencies[i]
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    text = Converter.convert(message)
    bot.reply_to(message, text)

bot.polling(none_stop=True)
