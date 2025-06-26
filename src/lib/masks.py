from typing import Union


def get_mask_card_number(card_number: Union[int, str]) -> str:
    """Функцию маскировки номера банковской карты"""
    # 7000792289606361 входной аргумент
    card_number = str(card_number).replace(" ", "")
    if len(card_number) != 16 or not card_number.isdigit():
        return "Введите номер карты, должно быть 16 символов"

    else:
        return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"  # 7000 79** **** 6361 выход


def get_mask_account(account_number: Union[int, str]) -> str:
    """Функцию маскировки номера банковского счета"""
    account_number = str(account_number).replace(" ", "")  # 73654108430135874305
    if not account_number.isdigit():
        return "Введите номер счёта, он включает в себя только цифры"

    return f"**{account_number[-4:]}"  # ** 4305
