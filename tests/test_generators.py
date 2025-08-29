import pytest
from generators import filter_by_currency, transaction_descriptions,card_number_generator


class TestFilterByCurrency:
    """Тесты для функции filter_by_currency"""

    def test_filter_usd_transactions(self, sample_transactions):
        """Тест фильтрации USD транзакций"""
        usd_transactions = list(filter_by_currency(sample_transactions, "USD"))

        # В sample_transactions 2 USD транзакции (id: 1 и 3)
        assert len(usd_transactions) == 2

        for transaction in usd_transactions:
            assert transaction["operationAmount"]["currency"]["name"] == "USD"
            assert transaction["id"] in [1, 3]  # Проверяем ID USD транзакций

    def test_filter_eur_transactions(self, sample_transactions):
        """Тест фильтрации EUR транзакций"""
        eur_transactions = list(filter_by_currency(sample_transactions, "EUR"))

        # В sample_transactions 1 EUR транзакция (id: 2)
        assert len(eur_transactions) == 1
        assert eur_transactions[0]["operationAmount"]["currency"]["name"] == "EUR"
        assert eur_transactions[0]["id"] == 2

    def test_filter_nonexistent_currency(self, sample_transactions):
        """Тест фильтрации несуществующей валюты"""
        gbp_transactions = list(filter_by_currency(sample_transactions, "GBP"))
        assert len(gbp_transactions) == 0

    def test_empty_list(self, empty_transactions):
        """Тест с пустым списком транзакций"""
        usd_transactions = list(filter_by_currency(empty_transactions, "USD"))
        assert len(usd_transactions) == 0

    def test_transactions_without_currency(self, transactions_without_currency):
        """Тест с транзакциями без информации о валюте"""
        # Должен корректно обработать без ошибок
        usd_transactions = list(filter_by_currency(transactions_without_currency, "USD"))
        assert len(usd_transactions) == 0

    @pytest.mark.parametrize("currency,expected_count,expected_ids", [
        ("USD", 2, [1, 3]),
        ("EUR", 1, [2]),
        ("RUB", 1, [4]),
        ("GBP", 0, []),
    ])
    def test_parametrized_currency_filter(self, sample_transactions, currency, expected_count, expected_ids):
        """Параметризованный тест для разных валют"""
        filtered = list(filter_by_currency(sample_transactions, currency))

        assert len(filtered) == expected_count
        for transaction in filtered:
            assert transaction["id"] in expected_ids
            assert transaction["operationAmount"]["currency"]["name"] == currency



class TestTransactionDescriptions:
    """Тесты для функции transaction_descriptions"""

    def test_get_descriptions(self, sample_transactions):
        """Тест получения описаний транзакций"""
        descriptions = list(transaction_descriptions(sample_transactions))

        expected_descriptions = [
            "Перевод организации",
            "Перевод со счета на счет",
            "Оплата услуг",
            "Пополнение счета"
        ]

        assert descriptions == expected_descriptions

    def test_empty_list(self, empty_transactions):
        """Тест с пустым списком"""
        descriptions = list(transaction_descriptions(empty_transactions))
        assert descriptions == []

    def test_single_transaction(self, single_transaction):
        """Тест с одной транзакцией"""
        descriptions = list(transaction_descriptions(single_transaction))
        assert descriptions == ["Одиночный перевод"]

    def test_transactions_without_currency(self, transactions_without_currency):
        """Тест с транзакциями без валюты (должны быть описания)"""
        descriptions = list(transaction_descriptions(transactions_without_currency))
        assert descriptions == ["Тестовая операция без валюты"]




class TestCardNumberGenerator:
    """Тесты для генератора номеров карт"""

    @pytest.mark.parametrize("start,end,expected_count", [
        (1, 5, 5),
        (9999999999999995, 9999999999999999, 5),
        (1, 1, 1),
        (10, 15, 6),
    ])
    def test_generator_range(self, start, end, expected_count):
        """Тест генерации в разных диапазонах"""
        cards = list(card_number_generator(start, end))
        assert len(cards) == expected_count

    def test_card_format(self):
        """Тест формата номеров карт"""
        cards = list(card_number_generator(1, 3))

        expected_cards = [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003"
        ]

        assert cards == expected_cards

    def test_invalid_range(self):
        """Тест обработки неверного диапазона"""
        with pytest.raises(ValueError, match="Диапазон должен быть от 1 до 9999999999999999"):
            list(card_number_generator(0, 5))

        with pytest.raises(ValueError):
            list(card_number_generator(5, 1))

        with pytest.raises(ValueError):
            list(card_number_generator(10000000000000000, 10000000000000001))

    def test_edge_cases(self):
        """Тест крайних значений"""
        # Первая карта
        first_card = next(card_number_generator(1, 1))
        assert first_card == "0000 0000 0000 0001"

        # Последняя карта
        last_card = list(card_number_generator(9999999999999999, 9999999999999999))[0]
        assert last_card == "9999 9999 9999 9999"

    def test_specific_numbers(self):
        """Тест конкретных номеров карт"""
        cards = list(card_number_generator(1234567890123456, 1234567890123458))

        expected_cards = [
            "1234 5678 9012 3456",
            "1234 5678 9012 3457",
            "1234 5678 9012 3458"
        ]

        assert cards == expected_cards