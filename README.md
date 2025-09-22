````````# SkyGit - Bank Operations Processing System

![Python](https://img.shields.io/badge/Python-3.13+-blue)
![Poetry](https://img.shields.io/badge/Poetry-✓-green)
![Pytest](https://img.shields.io/badge/Pytest-✓-success)
![Coverage](https://img.shields.io/badge/Coverage-80%25+-brightgreen)
![Black](https://img.shields.io/badge/Code%20Style-Black-000000)

Профессиональная система для обработки банковских операций и транзакций. Разработана для использования в банковской сфере с поддержкой многопоточности, логирования и интеграции с внешними API.

## 📋 Оглавление

- [Возможности](#возможности)
- [Быстрый старт](#быстрый-старт)
- [Установка](#установка)
- [Использование](#использование)
- [API документация](#api-документация)
- [Тестирование](#тестирование)
- [Разработка](#разработка)

## 🚀 Возможности

- **📊 Мультиформатная обработка** - JSON, CSV, XLSX, ODF файлы
- **🔒 Безопасность данных** - Маскирование карт и счетов
- **🌐 Интеграция с API** - Конвертация валют в реальном времени
- **📈 Фильтрация и сортировка** - По статусу, дате, валюте
- **🔍 Генерация данных** - Номера карт, описания операций
- **📝 Логирование** - Детальное отслеживание операций
- **🎯 Декораторы** - Умное кэширование и обработка ошибок

## ⚡ Быстрый старт

```bash
# Клонирование и установка
git clone https://github.com/Dimap5825/SkyPro_Bank.git
cd SkyPro_Bank
poetry install
poetry shell

# Запуск обработки данных
python -c "
from src.file_to_py_format import file_to_py_format
from src.processing import filter_by_state, sort_by_date

# Загрузка и обработка данных
transactions = file_to_py_format('data/operations.json')
executed_ops = filter_by_state(transactions, 'EXECUTED')
sorted_ops = sort_by_date(executed_ops)

print(f'Обработано {len(sorted_ops)} операций')
"

# Запуск тестов
pytest
```

## 📦 Установка

### Предварительные требования

- Python 3.13 или выше
- Poetry (менеджер зависимостей)

### Пошаговая установка

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/Dimap5825/SkyPro_Bank.git
cd SkyPro_Bank
```

2. **Установите зависимости:**
```bash
poetry install
```

3. **Настройте переменные окружения:**
```bash
cp .env.example .env
# Добавьте ваш API ключ в .env файл:
# api_key=your_api_key_here
```

4. **Активируйте виртуальное окружение:**
```bash
poetry shell
```

## 🏃‍♂️ Использование

### Основной модуль widget.py

```python
from src.widget import mask_account_card, get_date

# Умное маскирование карт и счетов
masked_card = mask_account_card("Visa Platinum 7000792289606361")
print(masked_card)  # Visa Platinum 7000 79** **** 6361

masked_account = mask_account_card("Счет 73654108430135874305")
print(masked_account)  # Счет **4305

# Форматирование даты
formatted_date = get_date("2023-07-15T14:30:00.000000")
print(formatted_date)  # 15.07.2023
```

### Обработка транзакций (processing.py)

```python
from src.processing import filter_by_state, sort_by_date

transactions = [
    {"id": 1, "state": "EXECUTED", "date": "2023-01-01T12:00:00.000000"},
    {"id": 2, "state": "CANCELED", "date": "2023-01-02T12:00:00.000000"}
]

# Фильтрация по статусу
executed_ops = filter_by_state(transactions, "EXECUTED")

# Сортировка по дате (новые сначала)
sorted_ops = sort_by_date(transactions)
```

### Маскирование данных (masks.py)

```python
from src.masks import get_mask_card_number, get_mask_account

# Маскирование номера карты
card_mask = get_mask_card_number("7000792289606361")  # 7000 79** **** 6361

# Маскирование номера счета
account_mask = get_mask_account("73654108430135874305")  # **4305
```

### Генераторы данных (generators.py)

```python
from src.generators import filter_by_currency, card_number_generator, transaction_descriptions

# Фильтрация по валюте
usd_transactions = list(filter_by_currency(transactions, "USD"))

# Генерация номеров карт
card_numbers = list(card_number_generator(1, 5))
for card in card_numbers:
    print(f"Сгенерированная карта: {card}")

# Получение описаний операций
descriptions = list(transaction_descriptions(transactions))
```

### Конвертация файлов (file_to_py_format.py)

```python
from src.file_to_py_format import file_to_py_format

# Автоматическое определение формата и конвертация
transactions_json = file_to_py_format("data/operations.json")
transactions_csv = file_to_py_format("data/transactions.csv")
transactions_xlsx = file_to_py_format("data/operations.xls")

print(f"Загружено {len(transactions_json)} операций из JSON")
```

### Внешние API (external_API.py)

```python
from src.external_API import transaction_sum_rub

# Конвертация суммы в рубли через API
transaction = {
    "operationAmount": {
        "amount": "100.00",
        "currency": {"code": "USD"}
    }
}

amount_rub = transaction_sum_rub(transaction)
print(f"Сумма в рублях: {amount_rub}")
```

### Утилиты (utils.py)

```python
from src.utils import get_list_financial_transactions

# Безопасная загрузка JSON транзакций
transactions = get_list_financial_transactions("data/operations.json")
```

### Декораторы (decorators.py)

```python
from src.decorators import log, apikey_load

@log("operations.log")
def process_transaction(transaction):
    """Функция с логированием"""
    return transaction_sum_rub(transaction)

@apikey_load
def secure_api_call():
    """Функция с автоматической загрузкой API ключа"""
    return "API call successful"
```

## 📊 Формат данных

### Структура операции (data/operations.json)

```json
{
    "id": 441945886,
    "state": "EXECUTED",
    "date": "2019-08-26T10:50:58.294041",
    "operationAmount": {
        "amount": "31957.58",
        "currency": {
            "name": "руб.",
            "code": "RUB"
        }
    },
    "description": "Перевод организации",
    "from": "Maestro 1596837868705199",
    "to": "Счет 64686473678894779589"
}
```

### Поддерживаемые форматы файлов

- **JSON** (`operations.json`) - основной формат
- **CSV** (`transactions.csv`) - табличные данные
- **XLSX** (`operations.xls`) - Excel файлы
- **ODF** - OpenDocument Format

## 🧪 Тестирование

### Запуск всех тестов

```bash
pytest
```

### Запуск с покрытием

```bash
pytest --cov=src --cov-report=html:coverage_report
```

### Конкретные тестовые модули

```bash
# Тесты обработки данных
pytest tests/test_processing.py -v

# Тесты маскирования
pytest tests/test_masks.py -v

# Тесты виджета
pytest tests/test_widget.py -v

# Тесты генераторов
pytest tests/test_generators.py -v

# Тесты API
pytest tests/test_external_API.py -v
```

### Просмотр отчета покрытия

```bash
open coverage_report/index.html  # macOS
start coverage_report/index.html # Windows
xdg-open coverage_report/index.html  # Linux
```

## 🔧 Разработка

### Установка для разработки

```bash
git clone https://github.com/Dimap5825/SkyPro_Bank.git
cd SkyPro_Bank
poetry install --with dev
poetry shell
```

### Проверка качества кода

```bash
# Форматирование кода
black src/ tests/

# Проверка стиля
flake8 src/ tests/

# Статическая типизация
mypy src/

# Сортировка импортов
isort src/ tests/
```

### Структура проекта

```
SkyGit/
├── src/
│   ├── widget.py              # Основной интерфейс
│   ├── processing.py          # Фильтрация и сортировка
│   ├── masks.py               # Маскирование данных
│   ├── generators.py          # Генераторы данных
│   ├── external_API.py        # Работа с внешними API
│   ├── file_to_py_format.py   # Конвертер файлов
│   ├── utils.py               # Вспомогательные функции
│   └── decorators.py          # Декораторы
├── tests/                     # Полный набор тестов
├── data/                      # Примеры данных
├── coverage_report/           # Отчет покрытия
├── logs/                      # Логи приложения
└── pyproject.toml            # Конфигурация
```

## 🌐 API Интеграция

Проект интегрируется с [APILayer](https://apilayer.com) для конвертации валют. Для работы необходим API ключ:

1. Получите ключ на [apilayer.com](https://apilayer.com/marketplace/exchangerates_data-api)
2. Добавьте в файл `.env`:
```env
api_key=your_actual_api_key_here
```

## 👤 Автор

**Dmitry** - [Dimap5825](https://github.com/Dimap5825)
