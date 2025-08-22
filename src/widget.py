from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_card: str) -> str:
    """
    записываем счёт и номер в виде 'счёт/карта' 'номер замаскированный (1234 56** **** 1234)'
    """
    space_index = -1

    for index,symb in enumerate(account_card):
        if symb.isdigit():
            space_index += index
            break

    if space_index == -1:
        raise ValueError("Не найден номер в строке")
    acc_name= account_card[:space_index].strip() # имя это всё до индекса выше
                                      # "Visa Classic 1234 5678 9012 3456"[:4] → "Visa"
    number = account_card[space_index:].replace(" ","")

    if acc_name.lower() not in ["счет","счёт"]: # если карта
        return f"{acc_name} {get_mask_card_number(number)}"
    else: # если счёт
        return f"{acc_name} {get_mask_account(number)}"


from datetime import datetime


def get_date(iso_datetime: str) -> str:
    """
    Принимает на вход строку с датой со временем в формате iso
    и возвращает в формате "ДД.ММ.ГГГГ".
    """
    if not iso_datetime:
        raise ValueError("Неверный формат даты")

    # Проверяем наличие 'T' в строке
    if "T" not in iso_datetime:
        raise ValueError("Неверный формат даты")

    try:
        # Разделяем дату и время
        iso_date, iso_time = iso_datetime.split("T")

        # Проверяем формат времени (должно быть HH:MM:SS)
        time_parts = iso_time.split(":")
        if len(time_parts) != 3:
            raise ValueError("Неверный формат даты")

        # Проверяем, что время состоит из цифр
        for part in time_parts:
            if not part.isdigit():
                raise ValueError("Неверный формат даты")

        # Разделяем дату на компоненты
        date_parts = iso_date.split("-")
        if len(date_parts) != 3:
            raise ValueError("Неверный формат даты")

        year, month, day = date_parts

        # Проверяем, что все компоненты даты состоят из цифр
        if not (year.isdigit() and month.isdigit() and day.isdigit()):
            raise ValueError("Неверный формат даты")

        # Преобразуем в числа для проверки диапазонов
        year_int = int(year)
        month_int = int(month)
        day_int = int(day)

        # Проверяем корректность месяца
        if not (1 <= month_int <= 12):
            raise ValueError("Неверный формат даты")

        # Проверяем корректность дня
        if not (1 <= day_int <= 31):
            raise ValueError("Неверный формат даты")

        # Проверяем специфичные ограничения для месяцев
        if month_int in [4, 6, 9, 11] and day_int > 30:
            raise ValueError("Неверный формат даты")

        # Проверяем февраль
        if month_int == 2:
            # Проверяем високосный год
            if (year_int % 4 == 0 and year_int % 100 != 0) or (year_int % 400 == 0):
                max_days = 29
            else:
                max_days = 28
            if day_int > max_days:
                raise ValueError("Неверный формат даты")

        # Если все проверки пройдены, возвращаем отформатированную дату
        return f"{day_int:02d}.{month_int:02d}.{year_int}"

    except (ValueError, IndexError):
        raise ValueError("Неверный формат даты")
