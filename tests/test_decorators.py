import os
import pytest


def test_success_with_file(test_func_with_file):
    """1. Функция выполняется и файл указан"""
    add_func, test_file = test_func_with_file

    result = add_func(2, 3)
    assert result == 5
    assert os.path.exists(test_file)

    with open(test_file, "r", encoding="utf-8") as f:
        content = f.read()
    assert "add_numbers ok" in content


def test_success_without_file(test_func_without_file, capsys):
    """2. Функция выполняется и файл не указан"""
    add_func = test_func_without_file

    result = add_func(2, 3)
    captured = capsys.readouterr()

    assert result == 5
    assert "add_numbers ok\n" in captured.out


def test_error_with_file(error_func_with_file):
    """3. Ошибка: файл указан"""
    divide_func, test_file = error_func_with_file

    with pytest.raises(ZeroDivisionError):
        divide_func(10, 0)

    assert os.path.exists(test_file)
    with open(test_file, "r", encoding="utf-8") as f:
        content = f.read()
    assert "divide error: ZeroDivisionError" in content
    assert "Inputs: (10, 0)" in content


def test_error_without_file(error_func_without_file, capsys):
    """4. Ошибка: файл не указан"""
    divide_func = error_func_without_file

    with pytest.raises(ZeroDivisionError):
        divide_func(10, 0)

    captured = capsys.readouterr()
    assert "divide error: ZeroDivisionError" in captured.out
    assert "Inputs: (10, 0)" in captured.out
