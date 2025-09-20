import logging
import os


logger = logging.getLogger(__name__)
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
