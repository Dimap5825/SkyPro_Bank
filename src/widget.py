from src.masks import get_mask_account, get_mask_card_number
def mask_account_card(card_or_account_number: [str]) -> str:
    """ умеет обрабатывать информацию как о картах, так и о счетах."""
    try:
        card_or_account_number = str(card_or_account_number)
        parts = card_or_account_number.split()
        parts = [x.lower() for x in parts]

        if len(parts) < 2:  # проверка чтобы было минимум 2 аргумента в словаре (название и номер)
            return "введите название карточного счёта и его номер"
        number = ''.join(num for num in parts[-1] if num.isdigit())

        if not number :  # проверка, что последний аргумент (номер) и это число
            return "номер счёта должен состоять из цифр"

        if parts[0] == "счет" or parts[0] == "счёт":  # если счёт
            return get_mask_account(number)
        elif parts[0] == "visa" or parts[0] == "maestro" or parts[0] == "mastercard":  # если карта
            return get_mask_card_number(number)

        else:  # если не понял счёт или карта
            return f"Ошибка: Неизвестный тип карты/счета: {parts[0]}"
    except (AttributeError, TypeError, ValueError):
        # Ловим случаи когда:
        # - передан None (AttributeError)
        # - передан объект без __str__ (TypeError)
        # - другие ошибки преобразования (ValueError)
        return "ошибка введите повторно"


def get_date(iso_datetime: str) -> str:
    """
    Принимает на вход строку с датой со временем в формате iso
    и возвращает в формате "ДД.ММ.ГГГГ".
    """
    try:
        iso_date, _ = iso_datetime.split("T")
        year, month, day = iso_date.split("-")
        return f"{day}.{month}.{year}"
    except (IndexError, ValueError):
        raise ValueError("Неверный формат даты")
