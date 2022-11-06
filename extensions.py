import requests
import json
from tok import currencies

class APIException(Exception):
    pass

class Converter():
    @staticmethod
    def get_price(quote, base, amount):
        page = f'https://api.exchangerate.host/convert?from={quote}&to={base}&amount={amount}'
        r = requests.get(page)
        dic = json.loads(r.content)
        reply = dic['result']
        total = round(reply, 2)
        return total

    @staticmethod
    def convert(message):
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
            return f'Неверный формат команды.\n{e}'
        except Exception as e:
            return f'Не удалось обработать команду.\n{e}'
        else:
            total = Converter.get_price(quote, base, amount)
            return f'{amount} {currencies[quote]} соответствует {total} {currencies[base]}'
