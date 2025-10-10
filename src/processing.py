from datetime import datetime


def filter_by_state(transactions: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
    Фильтрует список словарей, оставляя только те, где значение ключа 'state' совпадает с заданным.

    :param transactions: Список словарей для фильтрации.
    :param state: Значение ключа 'state' для фильтрации (по умолчанию 'EXECUTED').
    :return: Отфильтрованный список словарей.
    """
    return [
        transaction for transaction in transactions if transaction.get("state") == state
    ]


def sort_by_date(transactions: list[dict], reverse: bool = True) -> list[dict]:
    """Сортирует список словарей по дате с проверкой корректности формата"""

    def date_key(item):
        date_str = item["date"]
        try:
            # Парсим ISO формат с временем, берем только дату
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except ValueError:
            # Если не получается - пробуем старый формат для обратной совместимости
            try:
                return datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                raise ValueError(f"Неверный формат даты: {date_str}")

    return sorted(transactions, key=date_key, reverse=reverse)