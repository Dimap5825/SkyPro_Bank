import os
import pandas as pd
import logging
import json
import csv


def json_to_list(path)->list:
    with open(path) as file_json:
        result = json.load(file_json) # на выходе list
        return result


def csv_to_list(path) -> list:
    with open(path, 'r', newline='') as csv_file:
        result = csv.DictReader(csv_file) # возвращает итератор
        return list(result)


def xlsx_to_list(path) -> list:
    result = pd.read_excel(path) # тут уже DataFrame формат
    return result.to_dict('records')


def odf_to_list(path)->list:
    result = pd.read_excel(path, engine='odf') # тут уже DataFrame формат
    return result.to_dict('records')


def file_to_py_format(path) -> list | None:
    """
    будет принимать данные форматов:
         json
         csv
         xlsx
         odf
        и делать из них список транзакций в формате list[dict]
    """
    logger = logging.getLogger(f"{__name__}")
    # Настраиваем хендлер только если его еще нет
    if not logger.handlers:
        # Создаем папку для логов, если она не существует
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
        file_handler = logging.FileHandler('logs/utils.log')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        logger.addHandler(file_handler)
        logger.setLevel(logging.INFO)
        logger.debug(f"начало работы функции ")
    try:
        if isinstance(path, pd.DataFrame):  #это если например передаётся переменная, где уже данные в формате DataFrame(то есть уже было (pd.DataFrame)
            logger.info("DataFrame - преобразуем в list[dict]")
            return path.to_dict('records')  #преобразование не требуется

        elif isinstance(path, str):
            file_format = ((str(path).split("."))[-1]).lower()
            logger.info(f"формат файла : {file_format}")

            if file_format == "json":
                # преобразование в list[dict] из json
                return json_to_list(path)
            elif file_format == "csv":
                # преобразование в list[dict] из csv
                return csv_to_list(path)
            elif file_format == "xlsx":
                # преобразование в list[dict] из xlsx
                return xlsx_to_list(path)
            elif file_format == "odf":
                # преобразование в list[dict] из odf
                return odf_to_list(path)
            else:
                logger.debug(f"формат не известен,{file_format}")
                raise ValueError(f"неизвестный формат {file_format} ")
        else:
            return None
    except Exception as e:
        logger.error(f"{e}")
        raise Exception(f"{e}")


