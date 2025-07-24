def get_mask_card_number(card_number: str) -> str:
    """Функцию маскировки номера банковской карты"""
    # 7000792289606361 входной аргумент
    card_number = str(card_number).replace(" ", "")
    if not (len(card_number)) == 16 and card_number.isdigit():
        raise ValueError("Введите номер карты, должно быть 16 символов")
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"  # 7000 79** **** 6361 выход


def get_mask_account(account_number: str) -> str:
    """Функцию маскировки номера банковского счета"""
    if not (len(account_number) == 20 and account_number.isdigit()):
        raise ValueError("Введите номер счёта, он включает в себя только цифры")

    return f"**{account_number[-4:]}"
