import telebot

from extensions import APIException, Converter
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
    try:
        divided = message.text.split(' ')
        if len(divided) != 3:
            raise APIException('Неверное количество параметров')
        quote, base, amount = divided
        quote = quote.upper()
        base = base.upper()
        if quote not in currencies.keys():
            raise APIException(f'Введена недоступная валюта {quote}')
        if base not in currencies.keys():
            raise APIException(f'Введена недоступная валюта {base}')
        if quote == base:
            raise APIException(f'Невозможно конвертировать одинаковые валюты {base}')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException('Количество переводимой валюты должно быть числом')
    except APIException as e:
        bot.reply_to(message, f'Неверный формат команды.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        total = Converter.get_price(quote, base, amount)
        bot.reply_to(message, f'{amount} {currencies[quote]} соответствует {total} {currencies[base]}')

bot.polling(none_stop=True)
