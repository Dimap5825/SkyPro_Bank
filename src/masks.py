from develop_fun.log_fun import get_logger

logger = get_logger()
def get_mask_card_number(card_number: str) -> str:
    """Функцию маскировки номера банковской карты"""
    # 7000792289606361 входной аргумент
    # 7000 79** **** 6361 выход
    logger.info(f"Маскировка карты: {card_number}")
    card_number_str = str(card_number).replace(" ", "")

    if (len(card_number_str)) != 16 or not card_number_str.isdigit():
        logger.error("Введите номер карты, должно быть 16 цифр")
        raise ValueError("Введите номер карты, должно быть 16 цифр")
    logger.info(f"Результат маскировки карты: {f"{card_number_str[:4]} {card_number_str[4:6]}** **** {card_number_str[-4:]}"}")
    return f"{card_number_str[:4]} {card_number_str[4:6]}** **** {card_number_str[-4:]}"  # 7000 79** **** 6361 выход


def get_mask_account(account_number: str) -> str:
    """Функцию маскировки номера банковского счета"""
    logger.info(f"Маскировка счета: {account_number}")
    if not (len(account_number) == 20 and account_number.isdigit()):
        error_msg = "Введите номер счёта, он включает в себя только цифры"
        logger.error(error_msg)
        raise ValueError("Введите номер счёта, он включает в себя только цифры")

    logger.info(f"Результат маскировки счета: {f"**{account_number[-4:]}"}")
    return f"**{account_number[-4:]}"
