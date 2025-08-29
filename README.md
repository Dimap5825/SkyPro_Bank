
# SkyPro_Bank

Проект для работы с банковскими транзакциями. Набор утилит для фильтрации, сортировки, маскирования данных и генерации номеров карт.

## 📦 Установка

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/Dimap5825/SkyPro_Bank.git
cd SkyPro_Bank
```

2.**Установите зависимости:**
```bash
poetry install
```

3.**Активируйте виртуальное окружение:**
```bash
poetry shell
```

## 🚀 Использование

### 🏗️ Модуль `processing.py`

#### Фильтрация по статусу
```python
from src.processing import filter_by_state

transactions = [
    {'id': 1, 'state': 'EXECUTED'},
    {'id': 2, 'state': 'CANCELED'}
]

# Получить только выполненные операции
executed = filter_by_state(transactions)
```

#### Сортировка по дате
```python
from src.processing import sort_by_date

# По умолчанию - от новых к старым
sorted_ops = sort_by_date(transactions)

# От старых к новым
sorted_asc = sort_by_date(transactions, reverse=False)
```

### 🔢 Модуль `generators.py`

#### Фильтрация по валюте
```python
from generators import filter_by_currency

# Получение USD транзакций
usd_transactions = list(filter_by_currency(transactions, "USD"))
```

#### Генерация описаний
```python
from generators import transaction_descriptions

descriptions = list(transaction_descriptions(transactions))
for desc in descriptions:
    print(f"Описание: {desc}")
```

#### Генерация номеров карт
```python
from generators import card_number_generator

cards = list(card_number_generator(1, 5))
for card in cards:
    print(f"Номер карты: {card}")
```

### 🎭 Модуль `masks.py`

#### Маскирование карт и счетов
```python
from src.masks import get_mask_card_number, get_mask_account

# Маскирование карты
masked_card = get_mask_card_number("7000792289606361")  # 7000 79** **** 6361

# Маскирование счета  
masked_account = get_mask_account("73654108430135874305")  # **4305
```

### 🖥️ Модуль `widget.py`

#### Умное маскирование
```python
from src.widget import mask_account_card

# Автоматическое определение типа
masked_card = mask_account_card("Visa Platinum 7000792289606361")  # Visa Platinum 7000 79** **** 6361
masked_account = mask_account_card("Счет 73654108430135874305")  # Счет **4305
```

#### Форматирование даты
```python
from src.widget import get_date

formatted = get_date("2023-07-15T14:30:00.000000")  # 15.07.2023
```

## 📊 Формат данных

Данные хранятся в формате JSON (`data/operations.json`):

```json
{
    "id": 123,
    "state": "EXECUTED",
    "date": "2023-01-01T12:00:00.000000",
    "operationAmount": {
        "amount": "100.00",
        "currency": {
            "name": "USD",
            "code": "USD"
        }
    },
    "description": "Перевод организации",
    "from": "Счет 12345678901234567890",
    "to": "Счет 09876543210987654321"
}
```

## 🧪 Тестирование

```bash
# Все тесты
poetry run pytest

# Конкретные тесты
poetry run pytest tests/test_processing.py -v
poetry run pytest tests/test_generators.py -v
poetry run pytest tests/test_masks.py -v
poetry run pytest tests/test_widget.py -v

# Проверка стиля кода
poetry run flake8 .
poetry run black .
```

## 🏗️ Структура проекта

```
SkyPro_Bank/
├── src/
│   ├── processing.py    # Фильтрация и сортировка транзакций
│   ├── generators.py    # Функции-генераторы
│   ├── masks.py         # Маскирование данных
│   └── widget.py        # Основной интерфейс
├── tests/
│   ├── test_processing.py
│   ├── test_generators.py
│   ├── test_masks.py
│   └── test_widget.py
├── data/
│   └── operations.json  # Пример данных транзакций
├── pyproject.toml
└── README.md
```

## 📝 Особенности

- ✅ Полное покрытие тестами
- ✅ Обработка ошибок и edge cases
- ✅ Чистый и читаемый код
- ✅ Поддержка различных форматов данных
- ✅ Автоматическое форматирование кода

