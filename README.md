```markdown
# SkyPro_Bank

Проект для работы с банковскими транзакциями

## Установка
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Dimap5825/SkyPro_Bank.git
   cd SkyPro_Bank
   ```

2. Установите зависимости:
   ```bash
   poetry install
   ```

## Использование
### Фильтрация транзакций
```python
from processing import filter_by_state

transactions = [
    {'id': 1, 'state': 'EXECUTED'},
    {'id': 2, 'state': 'CANCELED'}
]

# Получить только выполненные операции
executed = filter_by_state(transactions)
```

### Сортировка по дате
```python
from processing import sort_by_date

# По умолчанию - от новых к старым
sorted_ops = sort_by_date(transactions)

# От старых к новым
sorted_asc = sort_by_date(transactions, reverse=False)
```

## Тестирование
```bash
poetry run pytest
poetry run flake8 .
poetry run black .
```

## Данные
Транзакции хранятся в `data/operations.json` в формате:
```json
{
    "id": 123,
    "state": "EXECUTED",
    "date": "2023-01-01"
}
```
