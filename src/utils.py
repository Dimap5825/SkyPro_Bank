import json
import logging

import os


logger = logging.getLogger(__name__)
# Настраиваем хендлер только если его еще нет
if not logger.handlers:

    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
This branch has conflicts that must be resolved

Use the web editor or the command line to resolve conflicts before continuing.

src/masks.py
src/utils.py

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
    file_handler = logging.FileHandler('logs/utils.log')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)

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
