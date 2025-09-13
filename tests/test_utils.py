def test_with_real_data(operations_data):
    """Тест с реальными данными через фикстуру"""
    from src.utils import get_list_financial_transactions
    from pathlib import Path

    data_path = Path(__file__).parent.parent / "data" / "operations.json"
    result = get_list_financial_transactions(data_path)

    # Сравниваем с данными из фикстуры
    assert result == operations_data
