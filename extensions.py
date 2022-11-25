import requests
import json
from config1 import keys


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f"Нельзя переводить одинаковые валюты {base}")

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f"Не удалось обрабоать валюту {quote}")

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f"Не удалось обрабоать валюту {base}")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не удалось обработать количество {amount}")

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}")
        total_base = json.loads(r.content)[keys[base]]*amount

        return total_base
