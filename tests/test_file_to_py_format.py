import pytest
import pandas as pd
from unittest.mock import patch, mock_open
import json
import csv
from src.file_to_py_format import (
    file_to_py_format,
    json_to_list,
    csv_to_list,
    xlsx_to_list,
    odf_to_list
)


class TestJsonToList:
    """Тесты для функции json_to_list"""

    def test_json_to_list_valid(self, tmp_path):
        """Тест чтения валидного JSON файла"""
        test_data = [{"id": 1, "name": "test"}, {"id": 2, "name": "test2"}]
        json_file = tmp_path / "test.json"

        with open(json_file, 'w') as f:
            json.dump(test_data, f)

        result = json_to_list(str(json_file))
        assert result == test_data

    def test_json_to_list_invalid_path(self):
        """Тест чтения несуществующего JSON файла"""
        with pytest.raises(Exception):
            json_to_list("nonexistent.json")


class TestCsvToList:
    """Тесты для функции csv_to_list"""

    def test_csv_to_list_valid(self, tmp_path):
        """Тест чтения валидного CSV файла"""
        csv_file = tmp_path / "test.csv"

        with open(csv_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'name'])
            writer.writeheader()
            writer.writerow({'id': '1', 'name': 'test1'})
            writer.writerow({'id': '2', 'name': 'test2'})

        result = csv_to_list(str(csv_file))
        assert len(result) == 2
        assert result[0]['id'] == '1'
        assert result[1]['name'] == 'test2'

    def test_csv_to_list_invalid_path(self):
        """Тест чтения несуществующего CSV файла"""
        with pytest.raises(Exception):
            csv_to_list("nonexistent.csv")


class TestXlsxToList:
    """Тесты для функции xlsx_to_list"""

    @patch('src.file_to_py_format.pd.read_excel')
    def test_xlsx_to_list_valid(self, mock_read_excel):
        """Тест чтения XLSX файла"""
        mock_data = pd.DataFrame({
            'Статус': ['OK', 'CANCELED'],
            'Дата операции': ['2023-01-01', '2023-01-02'],
            'Сумма операции': [100, -50],
            'Валюта операции': ['RUB', 'USD'],
            'Номер карты': ['1234', '5678'],
            'Описание': ['Test1', 'Test2']
        })
        mock_read_excel.return_value = mock_data

        result = xlsx_to_list("test.xlsx")

        assert len(result) == 2
        assert result[0]['state'] == 'EXECUTED'
        assert result[1]['state'] == 'CANCELED'
        assert result[0]['amount'] == 100
        assert result[1]['amount'] == 50  # abs value


class TestOdfToList:
    """Тесты для функции odf_to_list"""

    @patch('src.file_to_py_format.pd.read_excel')
    def test_odf_to_list_valid(self, mock_read_excel):
        """Тест чтения ODF файла"""
        mock_data = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
        mock_read_excel.return_value = mock_data

        result = odf_to_list("test.odf")

        assert result == [{'col1': 1, 'col2': 'a'}, {'col1': 2, 'col2': 'b'}]


class TestFileToPyFormat:
    """Тесты для основной функции file_to_py_format"""

    def test_file_to_py_format_with_dataframe(self):
        """Тест с передачей DataFrame"""
        df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
        result = file_to_py_format(df)
        assert result == [{'col1': 1, 'col2': 'a'}, {'col1': 2, 'col2': 'b'}]

    @patch('src.file_to_py_format.json_to_list')
    def test_file_to_py_format_json(self, mock_json):
        """Тест с JSON форматом"""
        mock_json.return_value = [{"test": "data"}]
        result = file_to_py_format("test.json")
        mock_json.assert_called_once_with("test.json")
        assert result == [{"test": "data"}]

    @patch('src.file_to_py_format.csv_to_list')
    def test_file_to_py_format_csv(self, mock_csv):
        """Тест с CSV форматом"""
        mock_csv.return_value = [{"test": "data"}]
        result = file_to_py_format("test.csv")
        mock_csv.assert_called_once_with("test.csv")
        assert result == [{"test": "data"}]

    def test_file_to_py_format_unknown_format(self):
        """Тест с неизвестным форматом"""
        with pytest.raises(Exception, match="неизвестный формат unknown"):
            file_to_py_format("test.unknown")

    @patch('src.file_to_py_format.json_to_list')
    def test_file_to_py_format_with_file_format(self, mock_json):
        """Тест с указанием формата файла"""
        mock_json.return_value = [{"test": "data"}]
        result = file_to_py_format(file_format="json")
        mock_json.assert_called_once_with('data/operations.json')
        assert result == [{"test": "data"}]

    @patch('src.file_to_py_format.get_logger')
    def test_file_to_py_format_exception_handling(self, mock_logger):
        """Тест обработки исключений"""
        mock_logger.return_value.error = lambda x: None

        with pytest.raises(Exception):
            file_to_py_format("nonexistent.json")