import pytest
import sys
import os
from unittest.mock import patch, MagicMock
from io import StringIO

# Добавляем путь к src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Теперь импортируем модули из src
from src.processing import filter_by_state, sort_by_date
from src.generators import filter_by_currency
from src.find import process_search_bank, process_bank_operations

# Для main.py нужен специальный импорт
main_module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'main.py'))


class TestMainFunctionality:
    """Тесты основной функциональности"""

    @pytest.fixture
    def sample_transactions(self):
        """Фикстура с тестовыми транзакциями"""
        return [
            {
                'id': 1,
                'state': 'EXECUTED',
                'date': '2023-09-05T11:30:32Z',
                'amount': 1000,
                'currency_name': 'RUB',
                'currency_code': 'RUB',
                'from': 'Card 1234',
                'to': 'Account 5678',
                'description': 'Payment for groceries'
            },
            {
                'id': 2,
                'state': 'CANCELED',
                'date': '2023-08-01T10:15:00Z',
                'amount': 2000,
                'currency_name': 'USD',
                'currency_code': 'USD',
                'from': 'Card 5678',
                'to': 'Account 9012',
                'description': 'Hotel booking'
            }
        ]

    def test_filter_by_state_executed(self, sample_transactions):
        """Тест фильтрации по статусу EXECUTED"""
        result = filter_by_state(sample_transactions, 'EXECUTED')
        assert len(result) == 1
        assert all(t['state'] == 'EXECUTED' for t in result)

    def test_filter_by_state_canceled(self, sample_transactions):
        """Тест фильтрации по статусу CANCELED"""
        result = filter_by_state(sample_transactions, 'CANCELED')
        assert len(result) == 1
        assert all(t['state'] == 'CANCELED' for t in result)

    def test_sort_by_date_descending(self, sample_transactions):
        """Тест сортировки по убыванию даты"""
        result = sort_by_date(sample_transactions, reverse=True)
        dates = [t['date'] for t in result]
        assert dates == ['2023-09-05T11:30:32Z', '2023-08-01T10:15:00Z']

    def test_sort_by_date_ascending(self, sample_transactions):
        """Тест сортировки по возрастанию даты"""
        result = sort_by_date(sample_transactions, reverse=False)
        dates = [t['date'] for t in result]
        assert dates == ['2023-08-01T10:15:00Z', '2023-09-05T11:30:32Z']

    def test_filter_by_currency_rub(self, sample_transactions):
        """Тест фильтрации по рублевым транзакциям"""
        result = list(filter_by_currency(sample_transactions, 'RUB'))
        assert len(result) == 1
        assert all(t['currency_name'] == 'RUB' for t in result)

    def test_process_search_bank(self, sample_transactions):
        """Тест поиска по ключевым словам"""
        result = process_search_bank(sample_transactions, 'payment')
        assert len(result) == 1
        assert any('payment' in t['description'].lower() for t in result)

    def test_process_bank_operations(self, sample_transactions):
        """Тест статистики по категориям"""
        categories = ['groceries', 'hotel']
        result = process_bank_operations(sample_transactions, categories)
        assert isinstance(result, dict)
        assert 'groceries' in result
        assert 'hotel' in result


class TestEdgeCases:
    """Тесты граничных случаев"""

    def test_empty_transactions_list(self):
        """Тест с пустым списком транзакций"""
        result = filter_by_state([], 'EXECUTED')
        assert result == []

        result = sort_by_date([])
        assert result == []

        result = list(filter_by_currency([], 'RUB'))
        assert list(result) == []

    def test_case_insensitive_search(self):
        """Тест регистронезависимого поиска"""
        transactions = [
            {'description': 'PAYMENT for Groceries'},
            {'description': 'payment for restaurant'},
            {'description': 'Transfer money'}
        ]

        result = process_search_bank(transactions, 'payment')
        assert len(result) == 2