from functools import (
    wraps,
)  # Этот модуль будет использоваться для размещения декораторов, включая декоратор log
import os
from dotenv import load_dotenv


# Логирование файла
def log(filename=None):
    """
    Логирование файла
    принимает файл 'filename', если нет, то запись логов идёт в консоль
    если успех: name_func ok. Где 'name_func' - логируемая функция
    если ошибка: name_func error:{название ошибки(формат)}. Inputs: {args}, {kwargs}. Где "args" и "kwargs" - параметры функции
    Returns: function - Декорированная функция с логированием.
    """

    def wrapper(func):
        # сохранение оригинального имени функции
        @wraps(func)
        def inner(*args, **kwargs):
            name_func = func.__name__
            # запись в файл если указан
            if filename:
                # выполняет функцию
                try:
                    result = func(*args, **kwargs)
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(f"{name_func} ok\n")
                        return result
                # если ошибка
                except Exception as e:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(
                            f"{name_func} error: {type(e).__name__}. Inputs: {args}, {kwargs}\n"
                        )
                    raise
            # если нет файла, вывод в консоль
            else:
                # выполняет функцию
                try:
                    result = func(*args, **kwargs)
                    print(f"{name_func} ok")
                    return result
                # если ошибка
                except Exception as e:
                    print(
                        f"{name_func} error: {type(e).__name__}. Inputs: {args}, {kwargs}"
                    )
                    raise

        return inner

    return wrapper


# api_key из .env файла подгружает
def apikey_load(func):
    """
    Для src/external_API.py для функции transaction_sum_rub
    или
    доступа к https://apilayer.com
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Загружаем переменные из .env файла
        load_dotenv()
        # Получаем API ключ из переменных окружения
        api_key = os.getenv("api_key")

        if not api_key:  # если нет api_key
            raise ValueError("API_KEY не найден. Проверьте файл .env")
        return func(*args, api_key=api_key, **kwargs)

    return wrapper
