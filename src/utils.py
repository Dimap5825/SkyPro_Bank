import json


def get_list_financial_transactions(jsonfile_name: str) -> list:
    """
    1.Получает: название файла .json в формате 'str' (jsonfile_name)

    2.Пробует получить из него python 'list' с транзакциями
    3.1. Если получается возвращает список 'list' с данными из .json файла (с транзакциями)
    3.2. Если не получается возвращает пустой список 'list'

    Примеры работы:
    # Нормальный файл
    get_list_financial_transactions("data/operations.json") → [транзакции...]

    # Файл не существует
    get_list_financial_transactions("nonexistent.json") → []

    # Битый JSON
    get_list_financial_transactions("corrupted.json") → []

    # Файл есть, но там не список (например dict)
    get_list_financial_transactions("config.json") → []

    # Ошибка прав доступа
    get_list_financial_transactions("/root/file.json") → [] + print ошибки
    """
    try:
        with open(jsonfile_name, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            else:
                return []
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []
    except Exception as e:
        print(f"Произошла ошибка {e}")
        return []
