import pytest
from src.decorators import log
from unittest.mock import Mock
from pathlib import Path
from unittest.mock import patch
import os


@pytest.fixture(
    params=[
        ("7000792289606361", "7000 79** **** 6361"),
        ("0000 0000 0000 0000", "0000 00** **** 0000"),
        ("00000 000 000 00 0 0 0", "0000 00** **** 0000"),
        # ниже жду ошибку
        (0000000000000000, "Введите номер карты, должно быть 16 символов"),
        ("", "Введите номер карты, должно быть 16 символов"),
        ("строка слов", "Введите номер карты, должно быть 16 символов"),
        ({}, "Введите номер карты, должно быть 16 символов"),
        ([], "Введите номер карты, должно быть 16 символов"),
        (True, "Введите номер карты, должно быть 16 символов"),
        (False, "Введите номер карты, должно быть 16 символов"),
    ]
)
def data_for_test_get_mask_card_number(request):
    return request.param


# Фикстуры для test_get_mask_account(src/masks.py)


@pytest.fixture(
    params=[  # Корректные номера счетов
        ("12345678901234567890", "**7890"),
        ("00000000000000000000", "**0000"),
        ("99999999999999999999", "**9999"),
        # Некорректные номера - должны вызывать ошибку
        (
            "123",
            "Введите номер счёта, он включает в себя только цифры",
        ),  # слишком короткий
        ("", "Введите номер счёта, он включает в себя только цифры"),  # пустая строка
        (
            "abcdefghijklmnopqrst",
            "Введите номер счёта, он включает в себя только цифры",
        ),  # буквы
        (
            "1234567890123456789",
            "Введите номер счёта, он включает в себя только цифры",
        ),  # 19 цифр
        (
            "123456789012345678901",
            "Введите номер счёта, он включает в себя только цифры",
        ),  # 21 цифра
        (
            "12345 67890 12345 67890",
            "Введите номер счёта, он включает в себя только цифры",
        ),  # с пробелами
        (
            "1234567890abcdefghij",
            "Введите номер счёта, он включает в себя только цифры",
        ),  # цифры и буквы
    ]
)
def data_for_test_get_mask_account(request):
    return request.param


# Фикстуры для test_widget(src/widget.py)


@pytest.fixture(
    params=[
        # Тест для банковской карты (Visa)
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        # Тест для счета (с заглавной буквы)
        ("Счет 73654108430135874305", "Счет **4305"),
        # Тест для счета (со строчной буквы)
        ("счет 64686473678894779589", "счет **9589"),
        # Тест для другой карты (MasterCard)
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        # Тест для Maestro
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        # Тест для American Express
        ("American Express 1234567812345678", "American Express 1234 56** **** 5678"),
        # Тест для карты с пробелами в номере (должны быть удалены)
        ("Visa Classic 1234 5678 9012 3456", "Visa Classic 1234 56** **** 3456"),
        # Тест для счета с пробелами (должны быть удалены)
        ("Счет 1234 5678 9012 3456 7890", "Счет **7890"),
        # Edge case: минимальная длина номера карты
        ("Card 1234567890123456", "Card 1234 56** **** 3456"),
        # Тесты с ошибками (ожидаем исключение)
        ("Visa Classic 123", "ValueError"),  # слишком короткий номер карты
        ("Счет 1234567890", "ValueError"),  # слишком короткий номер счета
        ("Card abcdefghijklmnop", "ValueError"),  # не цифры в номере карты
        ("Счет abcdefghijklmnopqrst", "ValueError"),  # не цифры в номере счета
        ("", "ValueError"),  # пустая строка
        ("Just Text", "ValueError"),  # нет номера
        ("1234567890123456", "ValueError"),  # только номер, нет названия
    ]
)
def data_test_mask_account_card(request):
    return request.param


@pytest.fixture(
    params=[
        ("2024-03-15T12:30:45", "15.03.2024"),
        ("2020-12-31T23:59:59", "31.12.2020"),
        ("1999-01-01T00:00:00", "01.01.1999"),
        ("2024-02-29T10:15:30", "29.02.2024"),  # високосный год
        ("2023-02-28T08:45:12", "28.02.2023"),  # не високосный год
        ("2024-03-15", "Неверный формат даты"),  # нет 'T'
        ("2024-03-15 12:30:45", "Неверный формат даты"),  # пробел вместо 'T'
        ("2024/03/15T12:30:45", "Неверный формат даты"),  # неправильные разделители
        ("15-03-2024T12:30:45", "Неверный формат даты"),  # день на первом месте
        ("2024-13-15T12:30:45", "Неверный формат даты"),  # месяц > 12
        ("2024-03-32T12:30:45", "Неверный формат даты"),  # день > 31
        ("", "Неверный формат даты"),  # пустая строка
        ("just text", "Неверный формат даты"),  # произвольный текст
        ("2024-03-T12:30:45", "Неверный формат даты"),  # отсутствует день
        ("2024--15T12:30:45", "Неверный формат даты"),  # отсутствует месяц
    ]
)
def data_test_get_date_valid(request):
    return request.param


# Фикстуры для test_processing.py(src/processing.py)


@pytest.fixture
def mixed_transactions():
    """Смешанные транзакции с разными статусами"""
    return [
        {"state": "EXECUTED", "id": 1},
        {"state": "PENDING", "id": 2},
        {"state": "EXECUTED", "id": 3},
    ]


@pytest.fixture
def executed_transactions():
    """Только EXECUTED транзакции"""
    return [
        {"state": "EXECUTED", "id": 1},
        {"state": "EXECUTED", "id": 2},
    ]


# ФИКСТУРЫ ДЛЯ ПРОВЕРКИ sort_by_date


@pytest.fixture
def transactions_with_dates():
    """Транзакции с датами для сортировки"""
    return [
        {"date": "2024-01-15", "id": 1},
        {"date": "2024-01-10", "id": 2},
        {"date": "2024-01-20", "id": 3},
    ]


@pytest.fixture
def empty_transactions():
    """Пустой список транзакций"""
    return []


@pytest.fixture
def transactions_without_state():
    """Транзакции без ключа state"""
    return [
        {"id": 1},
        {"state": "EXECUTED", "id": 2},
    ]


# Фикстуры для проверки generators.py


@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми транзакциями разных валют"""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2023-01-01T12:00:00.000000",
            "operationAmount": {
                "amount": "100.00",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод организации",
            "from": "Счет 12345678901234567890",
            "to": "Счет 09876543210987654321",
        },
        {
            "id": 2,
            "state": "EXECUTED",
            "date": "2023-01-02T12:00:00.000000",
            "operationAmount": {
                "amount": "200.00",
                "currency": {"name": "EUR", "code": "EUR"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 11111111111111111111",
            "to": "Счет 22222222222222222222",
        },
        {
            "id": 3,
            "state": "EXECUTED",
            "date": "2023-01-03T12:00:00.000000",
            "operationAmount": {
                "amount": "300.00",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Оплата услуг",
            "from": "Счет 33333333333333333333",
            "to": "Счет 44444444444444444444",
        },
        {
            "id": 4,
            "state": "EXECUTED",
            "date": "2023-01-04T12:00:00.000000",
            "operationAmount": {
                "amount": "400.00",
                "currency": {"name": "RUB", "code": "RUB"},
            },
            "description": "Пополнение счета",
            "from": "Счет 55555555555555555555",
            "to": "Счет 66666666666666666666",
        },
    ]


@pytest.fixture
def transactions_without_currency():
    """Фикстура с транзакциями без информации о валюте"""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2023-01-01T12:00:00.000000",
            "description": "Тестовая операция без валюты",
            "from": "Счет 12345678901234567890",
            "to": "Счет 09876543210987654321",
        }
    ]


@pytest.fixture
def single_transaction():
    """Фикстура с одной транзакцией"""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2023-01-01T12:00:00.000000",
            "operationAmount": {
                "amount": "100.00",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Одиночный перевод",
            "from": "Счет 12345678901234567890",
            "to": "Счет 09876543210987654321",
        }
    ]


# Фикстуры для проверки decorators.py


@pytest.fixture
def test_func_with_file(tmp_path):
    """Фикстура для функции с записью в файл"""
    test_file = tmp_path / "test_log.txt"

    @log(filename=str(test_file))
    def add_numbers(a, b):
        return a + b

    return add_numbers, test_file


@pytest.fixture
def test_func_without_file():
    """Фикстура для функции с выводом в консоль"""

    @log()
    def add_numbers(a, b):
        return a + b

    return add_numbers


@pytest.fixture
def error_func_with_file(tmp_path):
    """Фикстура для функции с ошибкой (файл)"""
    test_file = tmp_path / "error_log.txt"

    @log(filename=str(test_file))
    def divide(a, b):
        return a / b  # Будет ошибка при b=0

    return divide, test_file


@pytest.fixture
def error_func_without_file():
    """Фикстура для функции с ошибкой (консоль)"""

    @log()
    def divide(a, b):
        return a / b

    return divide


# Для test_utils.py
@pytest.fixture
def operations_data():
    """Фикстура с реальными данными из operations.json"""
    data_path = Path(__file__).parent.parent / "data" / "operations.json"

    if not data_path.exists():
        raise pytest.skip("Файл operations.json не найден")

    import json

    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def sample_transaction_rub():
    """Фикстура с транзакцией в RUB"""
    return {"operationAmount": {"amount": "1000.0", "currency": {"code": "RUB"}}}


@pytest.fixture
def sample_transaction_usd():
    """Фикстура с транзакцией в USD"""
    return {"operationAmount": {"amount": "100.0", "currency": {"code": "USD"}}}


@pytest.fixture
def sample_transaction_eur():
    """Фикстура с транзакцией в EUR"""
    return {"operationAmount": {"amount": "50.0", "currency": {"code": "EUR"}}}


@pytest.fixture
def sample_transaction_unknown():
    """Фикстура с неизвестной валютой"""
    return {"operationAmount": {"amount": "200.0", "currency": {"code": "GBP"}}}


@pytest.fixture
def mock_api_response_success():
    """Фикстура с успешным ответом API"""

    def _mock_response(converted_amount):
        mock_response = Mock()
        mock_response.json.return_value = {"success": True, "result": converted_amount}
        return mock_response

    return _mock_response


@pytest.fixture
def mock_api_response_error():
    """Фикстура с ошибкой API"""

    def _mock_response():
        mock_response = Mock()
        mock_response.json.side_effect = Exception("API error")
        return mock_response

    return _mock_response


@pytest.fixture(autouse=True)
def mock_env_vars():
    """Мок для переменных окружения во всех тестах"""
    with patch.dict(os.environ, {"api_key": "test_api_key_123"}):
        yield
