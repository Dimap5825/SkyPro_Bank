import re
from collections import Counter

def process_search_bank(data:list[dict], search:str)->list[dict]:
    """
    Фильтрует список банковских операций, оставляя только те,
    где в любом строковом поле найдена искомая строка.

    Поиск выполняется без учета регистра (регистронезависимый).

    Args:
        data (list[dict]): Список словарей с данными о банковских операциях
        search (str): Строка для поиска в значениях словарей

    Returns:
        list[dict]: Список словарей, где в хотя бы одном поле найдена искомая строка

    Example:
        >>> operations = [
        ...     {"description": "Payment for groceries", "amount": 100},
        ...     {"description": "Salary", "note": "October salary"}
        ... ]
        >>> process_search_bank(operations, "salary")
        [{"description": "Salary", "note": "October salary"}]
    """

    result = []
    for item in data:
        for key,value in item.items():
            if isinstance(value,str) and re.findall(pattern=search,string=value,flags=re.I):
                result.append(item)


    return result


def process_bank_operations(data:list[dict], categories:list)->dict:
    """
    Подсчитывает количество банковских операций по заданным категориям.

    Категория считается найденной, если её название содержится в любом строковом поле
    словаря с операцией. Поиск осуществляется без учёта регистра.

    Args:
        data (list[dict]): Список словарей с банковскими операциями.
                          Каждая операция представлена в виде словаря.
        categories (list): Список строк-названий категорий для поиска.

    Returns:
        dict: Словарь, где ключи - названия категорий,
              значения - количество операций в каждой категории.

    Example:
        >>> data = [
        ...     {"description": "Payment for groceries", "amount": 100},
        ...     {"description": "Salary October", "amount": 2000},
        ...     {"description": "Grocery store", "note": "weekly shopping"}
        ... ]
        >>> categories = ["grocery", "salary"]
        >>> process_bank_operations(data, categories)
        {'grocery': 2, 'salary': 1}
    """
    counter: Counter = Counter()
    # сначала запускаем цикл получаем каждую операцию
    for item in data:
        # получаем описание каждой операции
        for description in item.values():
            # сканируем каждую категорию
            for category in categories:
                if isinstance(description,str) and re.findall(category,description,flags=re.I):
                    counter[category] +=1


    return counter