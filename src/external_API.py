import datetime
import requests
from src.decorators import apikey_load


@apikey_load
def transaction_sum_rub(transaction, api_key=None) -> float:
    """
    Возвращает сумму транзакции в рублях.

    Если валюта USD или EUR, конвертирует через API.
    # 1. Получить валюту и сумму из транзакции
    # 2. Если валюта RUB -> вернуть сумму
    # 3. Если валюта USD или EUR -> конвертировать через API
    # 4. Если другая валюта -> обработать как ошибку

    """
    # Получение названия валюты из списка словарей транзакции
    currency_code = transaction["operationAmount"]["currency"]["code"]
    # Получение численного значения из списка словарей транзакции
    amount_str = transaction["operationAmount"]["amount"]
    # Если рубль, то перевод не нужен
    if currency_code == "RUB":
        return float(amount_str)
    # Если currency_code-Валюта == доллар
    elif currency_code == "USD":
        # Пробуем с помощью API обратиться к apilayer.com и перевести из usd в rud
        try:
            usd_to_rub = requests.get(
                "https://api.apilayer.com/exchangerates_data/convert",
                params={
                    "amount": f"{float(amount_str)}",
                    "from": "USD",
                    "to": "RUB",
                    "date": f"{datetime.datetime.now().strftime('%Y-%m-%d')}",
                },
                headers={"apikey": api_key},
            )
            return round(float((usd_to_rub.json())["result"]), 2)
        # Если не получилось, выдаём ошибку
        except Exception as e:
            raise Exception(f"Ошибка {e}")
    # Если currency_code-Валюта == евро
    elif currency_code == "EUR":
        # Пробуем с помощью API обратиться к apilayer.com и перевести из eur в rud
        try:
            eur_to_rub = requests.get(
                "https://api.apilayer.com/exchangerates_data/convert",
                params={
                    "amount": amount_str,
                    "from": "EUR",
                    "to": "RUB",
                    "date": f"{datetime.datetime.now().strftime('%Y-%m-%d')}",
                },
                headers={"apikey": api_key},
            )
            return round(float((eur_to_rub.json())["result"]), 2)
        # Если не получилось, выдаём ошибку
        except Exception as e:
            raise Exception(f"Ошибка {e}")
    # Валюта не указана
    else:
        return float(0)
