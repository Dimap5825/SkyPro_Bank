import inspect
import os
import logging

def get_logger():
    """Создает и возвращает настроенный логгер"""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Формат сообщений
    formatter = logging.Formatter('%(filename)s - %(asctime)s - %(name)s - %(levelname)s - %(message)s - %(funcName)s')

    # # 1. ХЕНДЛЕР ДЛЯ КОНСОЛИ
    # console_handler = logging.StreamHandler()
    # console_handler.setFormatter(formatter)

    # 2. ХЕНДЛЕР ДЛЯ ФАЙЛА
    current_file = os.path.abspath(__file__)
    root_dir = os.path.abspath(os.path.join(current_file, "../../"))
    log_dir = os.path.join(root_dir,"log")


    os.makedirs(log_dir,exist_ok=True)

    log_name = os.path.splitext(os.path.basename(inspect.stack()[1].filename))[0]

    # хендлер для записи логов в отдельные файлы
    file_handler = logging.FileHandler(f"{log_dir}/{log_name}.log", encoding='utf-8')
    file_handler.setFormatter(formatter)

    # хендлер для записи в общий лог
    general_file_handler = logging.FileHandler(f"{root_dir}/log/общий.log",encoding="utf-8")
    general_file_handler.setFormatter(formatter)

    # Добавляем оба хендлера
    # logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    # Добавляем хендлер для общей записи
    logger.addHandler(general_file_handler)
    return logger