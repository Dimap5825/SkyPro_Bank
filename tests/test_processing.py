import pytest
from src.processing import filter_by_state, sort_by_date


# Тесты для filter_by_state с использованием фикстур


def test_filter_executed(mixed_transactions):
    """Фильтрация по EXECUTED"""
    result = filter_by_state(mixed_transactions, "EXECUTED")
    assert len(result) == 2
    assert [item["id"] for item in result] == [1, 3]

def test_filter_pending(mixed_transactions):
    """Фильтрация по PENDING"""
    result = filter_by_state(mixed_transactions, "PENDING")
    assert len(result) == 1
    assert result[0]["id"] == 2

def test_filter_canceled(mixed_transactions):
    """Фильтрация по несуществующему статусу"""
    result = filter_by_state(mixed_transactions, "CANCELED")
    assert result == []

def test_filter_multiple_executed(executed_transactions):
    """Фильтрация нескольких EXECUTED"""
    result = filter_by_state(executed_transactions, "EXECUTED")
    assert len(result) == 2
    assert [item["id"] for item in result] == [1, 2]

def test_filter_empty(empty_transactions):
    """Фильтрация пустого списка"""
    result = filter_by_state(empty_transactions, "EXECUTED")
    assert result == []

def test_filter_no_state_key(transactions_without_state):
    """Фильтрация без ключа state"""
    result = filter_by_state(transactions_without_state, "EXECUTED")
    assert len(result) == 1
    assert result[0]["id"] == 2

def test_filter_default(mixed_transactions):
    """Фильтрация с параметром по умолчанию"""
    result = filter_by_state(mixed_transactions)
    assert len(result) == 2
    assert all(item["state"] == "EXECUTED" for item in result)



# Тесты для sort_by_date с использованием фикстур



def test_sort_descending(transactions_with_dates):
    """Сортировка по убыванию"""
    result = sort_by_date(transactions_with_dates, True)
    assert [item["id"] for item in result] == [3, 1, 2]

def test_sort_ascending(transactions_with_dates):
    """Сортировка по возрастанию"""
    result = sort_by_date(transactions_with_dates, False)
    assert [item["id"] for item in result] == [2, 1, 3]

def test_sort_default(transactions_with_dates):
    """Сортировка с параметром по умолчанию"""
    result = sort_by_date(transactions_with_dates)
    assert [item["id"] for item in result] == [3, 1, 2]  # reverse=True по умолчанию

def test_sort_empty(empty_transactions):
    """Сортировка пустого списка"""
    result = sort_by_date(empty_transactions)
    assert result == []

def test_sort_single_item():
    """Сортировка одного элемента"""
    result = sort_by_date([{"date": "2024-01-15", "id": 1}])
    assert result == [{"date": "2024-01-15", "id": 1}]

def test_sort_duplicate_dates():
    """Сортировка с одинаковыми датами"""
    result = sort_by_date([
        {"date": "2024-01-15", "id": 1},
        {"date": "2024-01-15", "id": 2}
    ], True)
    # Должны сохранить порядок при одинаковых датах
    assert [item["id"] for item in result] == [1, 2]

# Тесты для обработки ошибок (оставляем как есть)
def test_sort_by_date_errors():
    """Тестирование обработки ошибок в sort_by_date"""
    # Некорректный формат даты
    try:
        sort_by_date([{"date": "invalid-date", "id": 1}])
        assert False, "Expected ValueError or TypeError"
    except (ValueError, TypeError):
        pass
    # Отсутствие ключа date
    with pytest.raises(KeyError):
        sort_by_date([{"id": 1}])
