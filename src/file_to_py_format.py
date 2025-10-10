import pandas as pd
import json
import csv
from develop_fun.log_fun import get_logger


def json_to_list(path)->list:
    with open(path) as file_json:
        result = json.load(file_json) # на выходе list
        return result


def csv_to_list(path) -> list:
    with open(path, 'r', newline='') as csv_file:
        result = csv.DictReader(csv_file) # возвращает итератор
        return list(result)


def xlsx_to_list(path) -> list:
    result = pd.read_excel(path)  # тут уже DataFrame формат
    data = result.to_dict('records')

    # Нормализация структуры данных XLSX к структуре CSV
    normalized_data = []
    for transaction in data:
        normalized_transaction = {
            'id': None,  # В XLSX нет ID
            'state': 'EXECUTED' if transaction.get('Статус') == 'OK' else 'CANCELED',  # Преобразуем статус
            'date': transaction.get('Дата операции'),  # Дата может потребовать преобразования формата
            'amount': abs(transaction.get('Сумма операции', 0)),  # Берем модуль суммы
            'currency_name': transaction.get('Валюта операции'),
            'currency_code': transaction.get('Валюта операции'),
            'from': transaction.get('Номер карты'),
            'to': None,  # В XLSX нет получателя
            'description': transaction.get('Описание')
        }
        normalized_data.append(normalized_transaction)

    return normalized_data


def odf_to_list(path)->list:
    result = pd.read_excel(path, engine='odf') # тут уже DataFrame формат
    return result.to_dict('records')


def file_to_py_format(path = None, file_format = None) -> list | None:
    """
    будет принимать данные форматов:
         json
         csv
         xlsx
         odf
        и делать из них список транзакций в формате list[dict]
    """


    logger = get_logger()
    try:
        # если указан формат, значит в main.py просто вводит пользователь значит берет из наших данных
        if file_format:
            # стандартные пути {file_format:path}
            base_path = {
                "json":'data/operations.json',
                'csv':'data/transactions.csv',
                'xlsx':'data/operations.xlsx'
            }
            path = base_path[file_format]
        # если нет формата файла
        if not file_format:

        # уже было (pd.DataFrame)
            if isinstance(path, pd.DataFrame,):
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

    except Exception as e:
        logger.error(f"{e}")
        raise Exception(f"{e}")


