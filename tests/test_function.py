import pytest
import json
import os
import utils.functions


@pytest.fixture
def random_operations():
    """
    фикстура для отработки навыков работы с ней в упрощенном формате
    """
    return [
        {
            "id": 214024827,
            "state": "EXECUTED",
            "date": "2018-12-20T16:43:26.929246",
            "operationAmount": {
                "amount": "70946.18",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 10848359769870775355",
            "to": "Счет 21969751544412966366"
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657"
        },
    ]


def test_get_masked_number():
    """
    тест для проверки правильности маскировки номера карты, а также корректной отработки
    случая, когда в номере карты не содержится ничего
    """
    assert utils.functions.get_masked_number("Maestro 1308795367077170") == "Maestro 1308 79** **** 7170"
    assert utils.functions.get_masked_number("") == "Неизвестный счет"

def test_get_formatted_date():
    """
    тест для проверки корректного форматирования даты
    """
    assert utils.functions.get_formatted_date("2019-07-13T18:51:29.313309") == "13.07.2019"

def test_get_masked_account():
    """
    тест для проверки правильности маскировки самого номера счета и вывода полного содержания,
    в т.ч название карты\счета
    """
    assert utils.functions.get_masked_account("96527012349577388612") == " **8612"
    assert utils.functions.get_masked_account("Cчёт 96527012349577388612") == "Cчёт **8612"

def test_get_executed_operations(random_operations):
    """
    тест с использованием фикстуры, проверка создания выборки по значению "EXECUTED"
    """
    result = utils.functions.get_executed_operations(random_operations)
    expected_results = [
        {    "id": 214024827,
            "state": "EXECUTED",
            "date": "2018-12-20T16:43:26.929246",
            "operationAmount": {
                "amount": "70946.18",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 10848359769870775355",
            "to": "Счет 21969751544412966366"
        }
    ]
    assert result == expected_results

def test_get_length_file():
    """
    тест для проверки правильности возвращаемого типа и наличие в полученном файле информации
    """
    date = utils.functions.get_all_operation()
    assert isinstance(date, list)
    assert len(date) > 0


def test_get_last_five_executed_operations():
    """
    тест для проверки правильности возвращаемого типа и выборки необходимого количества
    операций
    """
    result = utils.functions.get_last_five_executed_operations()
    assert isinstance(result, list)
    assert len(result) == 5

def test_print_last_executed_formatted_operations(capsys):
    """
    тест для проверки того, что вывод в консоли не пустой
    """
    utils.functions.print_last_executed_formatted_operations()
    captured = capsys.readouterr()
    assert captured.out != ""