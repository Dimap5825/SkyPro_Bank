from typing import Union

from lib.masks import get_mask_account, get_mask_card_number


def mask_account_card (card_or_account_number: Union[int, str]) -> str:
    """ умеет обрабатывать информацию как о картах, так и о счетах."""
    try:
        card_or_account_number = str(card_or_account_number)

        parts = card_or_account_number.split()
        parts = [x.lower() for x in parts]

        if len(parts) < 2: # проверка чтобы было минимум 2 аргумента в словаре (название и номер)
            return "введите название карточного счёта и его номер"
        number = ''.join(c for c in parts[-1] if c.isdigit())

        if not number : # проверка, что последний аргумент (номер) и это число
            return "номер счёта должен состоять из чисел"

        if parts[0] == "счет" or parts[0] == "счёт": # если счёт
            return get_mask_account(number)
        elif parts[0] == "visa" or parts[0] == "maestro" or parts[0] == "mastercard": # если карта
            return get_mask_card_number(number)

        else: # если не понял счёт или карта
            return f"Ошибка: Неизвестный тип карты/счета: {parts[0]}"
    except (AttributeError, TypeError, ValueError):
          # Ловим случаи когда:
          # - передан None (AttributeError)
          # - передан объект без __str__ (TypeError)
          # - другие ошибки преобразования (ValueError)
          return "ошибка введите повторно"
def get_date (data_incomprehensible_format: str) -> str:
    """ принимает на вход строку с датой в формате
"2024-03-11T02:26:18.671407"
 и возвращает строку с датой в формате
"ДД.ММ.ГГГГ" """
    try:
        data_incomprehensible_format = data_incomprehensible_format.split("T")[0]
        year, month, day = data_incomprehensible_format.split("-")
        return f"{day}.{month}.{year}"
    except (IndexError, ValueError):
        return "Ошибка: неверный формат даты"




