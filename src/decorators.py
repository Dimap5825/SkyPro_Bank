from functools import wraps  # Этот модуль будет использоваться для размещения декораторов, включая декоратор log


def log(filename=None):
    """
    Логирование файла
    принимает файл 'filename', если нет, то запись логов идёт в консоль
    если успех: name_func ok. Где 'name_func' - логируемая функция
    если ошибка: name_func error:{название ошибки(формат)}. Inputs: {args}, {kwargs}. Где "args" и "kwargs" - параметры функции
    Returns: function - Декорированная функция с логированием.
    """
    def wrapper(func):
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
                        f.write(f"{name_func} error: {type(e).__name__}. Inputs: {args}, {kwargs}\n")
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
                    print(f"{name_func} error: {type(e).__name__}. Inputs: {args}, {kwargs}")
                    raise

        return inner
    return wrapper
