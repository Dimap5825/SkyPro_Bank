import json
from develop_fun.log_fun import get_logger



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
    logger = get_logger()
    logger.info("Пробуем открыть файл .json и преобразовать в лист словарей ")
    try:
        with open(jsonfile_name, "r", encoding="utf-8") as f: #.json
            data = json.load(f)        #list( список словарей Python)
            if isinstance(data, list):  # проверка, что data список
                return data
            else:
                return []
    except FileNotFoundError as e:
        logger.error(f"{e}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"{e}")

        return []
    except Exception as e:
        logger.error(f"{e}")
        return []
