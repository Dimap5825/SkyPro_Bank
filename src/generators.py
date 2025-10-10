# Этот модуль будет содержать все новые функции, реализующие генераторы для обработки данных.
from typing import Iterator


def filter_by_currency(transactions: list[dict], currency: str) -> Iterator[dict]:
    """
    Фильтрует транзакции по валюте операции (поддерживает разные структуры данных).

    Args:
        transactions: Список словарей с транзакциями
        currency: Название или код валюты для фильтрации

    Returns:
        Iterator[dict]: Итератор, который поочечередно возвращает транзакции
                      в указанной валюте
    """
    for transaction in transactions:
        # Стандартная структура (operationAmount -> currency -> name/code)
        operation_amount = transaction.get("operationAmount", {})
        currency_info = operation_amount.get("currency", {})

        # Альтернативная структура (прямые поля currency_name/currency_code)
        currency_name = transaction.get("currency_name")
        currency_code = transaction.get("currency_code")

        # Проверяем все возможные варианты
        if (currency_info.get("name") == currency or
                currency_info.get("code") == currency or
                currency_name == currency or
                currency_code == currency):
            yield transaction

def transaction_descriptions(transcriptions: list[dict]) -> Iterator[str]:
    """
    принимает список словарей с транзакциями и возвращает описание каждой операции по очереди
    """
    yield from (transaction["description"] for transaction in transcriptions)


def card_number_generator(start, end):
    """
    Выдает номера банковских карт в формате XXXX XXXX XXXX XXXX, где X— цифра номера карты.
    Генератор может сгенерировать номера карт в заданном диапазоне от 0000 0000 0000 0001 до 9999 9999 9999 9999.
    Генератор должен принимать начальное и конечное значения для генерации диапазона номеров
    """
    if not (1 <= start <= end <= 9999999999999999):
        raise ValueError("Диапазон должен быть от 1 до 9999999999999999")

    for number in range(start, end + 1):
        formated_number = f"{number:016d}"
        yield f"{formated_number[:4]} {formated_number[4:8]} {formated_number[8:12]} {formated_number[12:16]}"
