import requests
import json
from tok import currencies

class APIException(Exception):
    pass

class Converter():
    @staticmethod
    def get_price(quote, base, amount):
        page = 'https://www.cbr-xml-daily.ru/daily_json.js'
        r = requests.get(page)
        dic = json.loads(r.content)
        if quote != 'RUB':
            rubles = amount * dic['Valute'][quote]['Value'] / dic['Valute'][quote]['Nominal']
        else:
            rubles = amount
        if base != 'RUB':
            total = round((rubles * dic['Valute'][base]['Nominal'] / dic['Valute'][base]['Value']), 2)
        else:
            total = round(rubles, 2)
        return total