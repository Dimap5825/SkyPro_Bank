import pytest
from src.widget import mask_account_card, get_date

# Проверка mask_account_card


def test_mask_account_card(data_test_mask_account_card):
    account_card, expected = data_test_mask_account_card
    if expected == "ValueError":
        with pytest.raises(ValueError):
            mask_account_card(account_card)
    else:
        assert mask_account_card(account_card) == expected


# Проверка get_date_valid


def test_get_date_valid(data_test_get_date_valid):
    """
    Тестирование правильного преобразования даты
    """
    iso_datetime, expected = data_test_get_date_valid
    if expected == "Неверный формат даты":
        with pytest.raises(ValueError):
            get_date(iso_datetime)
    else:
        assert get_date(iso_datetime) == expected
