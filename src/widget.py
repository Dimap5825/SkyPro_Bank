from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_card: str) -> str:
    name, number = account_card.rsplit(" ", maxsplit=1)
    if name == "счет":
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)
    return f"{name} {masked_number}"


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
