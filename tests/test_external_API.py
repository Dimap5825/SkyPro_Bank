import pytest
from unittest.mock import patch
from src.external_API import transaction_sum_rub


class TestTransactionSumRub:
    """Тесты для функции transaction_sum_rub"""

    def test_rub_transaction(self, sample_transaction_rub):
        """Тест транзакции в RUB"""
        result = transaction_sum_rub(sample_transaction_rub)  # ✅ Убрал api_key
        assert result == 1000.0
        assert isinstance(result, float)

    @patch("src.external_API.requests.get")
    def test_usd_transaction_success(
        self, mock_get, sample_transaction_usd, mock_api_response_success
    ):
        """Тест успешной конвертации USD в RUB"""
        # Мокируем успешный ответ API
        mock_response = mock_api_response_success(7500.0)
        mock_get.return_value = mock_response

        result = transaction_sum_rub(sample_transaction_usd)  # ✅ Убрал api_key

        assert result == 7500.0
        assert isinstance(result, float)

        # Проверяем что запрос был сделан с правильными параметрами
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert call_args[0][0] == "https://api.apilayer.com/exchangerates_data/convert"

    @patch("src.external_API.requests.get")
    def test_eur_transaction_success(
        self, mock_get, sample_transaction_eur, mock_api_response_success
    ):
        """Тест успешной конвертации EUR в RUB"""
        mock_response = mock_api_response_success(4500.0)
        mock_get.return_value = mock_response

        result = transaction_sum_rub(sample_transaction_eur)  # ✅ Убрал api_key

        assert result == 4500.0
        assert isinstance(result, float)

    @patch("src.external_API.requests.get")
    def test_api_error_usd(
        self, mock_get, sample_transaction_usd, mock_api_response_error
    ):
        """Тест ошибки API при конвертации USD"""
        mock_response = mock_api_response_error()
        mock_get.return_value = mock_response

        with pytest.raises(Exception, match="Ошибка API error"):
            transaction_sum_rub(sample_transaction_usd)  # ✅ Убрал api_key

    @patch("src.external_API.requests.get")
    def test_api_error_eur(
        self, mock_get, sample_transaction_eur, mock_api_response_error
    ):
        """Тест ошибки API при конвертации EUR"""
        mock_response = mock_api_response_error()
        mock_get.return_value = mock_response

        with pytest.raises(Exception, match="Ошибка API error"):
            transaction_sum_rub(sample_transaction_eur)  # ✅ Убрал api_key

    def test_unknown_currency(self, sample_transaction_unknown):
        """Тест неизвестной валюты"""
        result = transaction_sum_rub(sample_transaction_unknown)  # ✅ Убрал api_key
        assert result == "Валюта не указана"

    @patch("src.external_API.requests.get")
    def test_api_call_parameters_usd(
        self, mock_get, sample_transaction_usd, mock_api_response_success
    ):
        """Тест параметров API запроса для USD"""
        mock_response = mock_api_response_success(7500.0)
        mock_get.return_value = mock_response

        transaction_sum_rub(sample_transaction_usd)  # ✅ Убрал api_key

        call_kwargs = mock_get.call_args[1]
        params = call_kwargs["params"]

        assert params["from"] == "USD"
        assert params["to"] == "RUB"
        assert params["amount"] == "100.0"
        assert "date" in params  # Проверяем что дата передается

    @patch("src.external_API.requests.get")
    def test_api_call_parameters_eur(
        self, mock_get, sample_transaction_eur, mock_api_response_success
    ):
        """Тест параметров API запроса для EUR"""
        mock_response = mock_api_response_success(4500.0)
        mock_get.return_value = mock_response

        transaction_sum_rub(sample_transaction_eur)  # ✅ Убрал api_key

        call_kwargs = mock_get.call_args[1]
        params = call_kwargs["params"]

        assert params["from"] == "EUR"
        assert params["to"] == "RUB"
        assert params["amount"] == "50.0"
        assert "date" in params

    def test_decorator_integration(self, sample_transaction_rub):
        """Тест что декоратор правильно работает с функцией"""
        result = transaction_sum_rub(sample_transaction_rub)
        assert result == 1000.0
