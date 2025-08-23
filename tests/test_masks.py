import pytest
from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number(data_for_test_get_mask_card_number):
    """Проверка get_mask_card_number"""
    card_number, expected = data_for_test_get_mask_card_number

    if expected == "Введите номер карты, должно быть 16 символов":
        with pytest.raises(ValueError):
            get_mask_card_number(card_number)
    else:
        assert get_mask_card_number(card_number) == expected


def test_get_mask_account(data_for_test_get_mask_account):
    """проверка get_mask_account"""
    account_number, expected = data_for_test_get_mask_account
    if expected == "Введите номер счёта, он включает в себя только цифры":
        with pytest.raises(ValueError, match=expected):
            get_mask_account(account_number)
    else:
        assert get_mask_account(account_number) == expected
