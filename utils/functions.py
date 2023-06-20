import json
import re
from datetime import datetime


def get_all_operation():
    """
    функция для сбора всей информации из json-файла в одну переменную для последующей
    работы с ней
    """
    with open("operations.json", encoding='utf-8') as file:
        all_data = json.load(file)

    return all_data


def get_executed_operations(all_data):
    """
    функция для выделения только выполненных операций из словаря со всеми операциями
    """
    executed_operations = []
    for operation_status in all_data:
        if 'state' in operation_status and operation_status['state'] == "EXECUTED":
            executed_operations.append(operation_status)

    return executed_operations


def get_last_five_executed_operations():
    """
    функция для выборки пяти последних по дате операций
    """
    all_data = get_all_operation()
    executed_operations = get_executed_operations(all_data)
    sorted_executed_operations = sorted(executed_operations, key=lambda x: x['date'], reverse=True)
    last_five_executed_operations = sorted_executed_operations[:5]

    return last_five_executed_operations


def get_formatted_date(date):
    """
    функция для форматирования полученной даты в формат ДД.ММ.ГГГГ
    """
    datetime_object = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")
    formatted_date = datetime_object.strftime("%d.%m.%Y")
    return formatted_date


def get_masked_number(who_send):
    """
    функция, позволяющая замаскировать номер карты в формате  XXXX XX** **** XXXX
    """
    if len(who_send) > 0:
        # разделение строки с инфой о карте на буквенную и численную часть, где буквы - там пробелы после каждой
        # большой буквы, для корректности вывода карт, состоящих из более чем 1 слова
        card_name = ''.join(filter(str.isalpha, who_send))
        card_name_with_chunks = re.sub(r'(?=[A-Z])', " ", card_name)
        card_name_with_chunks_ = card_name_with_chunks.replace(" ", "", 1)

        # работа с численной составляющшей, маскировка *
        card_account = ''.join(filter(str.isdigit, who_send))
        masked_card_account = card_account[:6]
        masked_card_account += "*" * (len(card_account) - 6 - 4)
        masked_card_account += who_send[-4:]

        # разделение на блоки по 4 и вывод полного наименования карты и номера счета
        chunks = " ".join([masked_card_account[i:i + 4] for i in range(0, len(masked_card_account), 4)])
        result = f"{card_name_with_chunks_} {chunks}"

        return result
    # возвращается, если отсутствует информация, откуда перевод
    return "Неизвестный счет"


def get_masked_account(who_get):
    """
    функция для маскировки номе6ра счета получателя в формате **XXXX
    """
    account_name = ''.join(filter(str.isalpha, who_get))
    account_number = ''.join(filter(str.isdigit, who_get))
    masked_account = "**" + account_number[-4:]
    result = f"{account_name} {masked_account}"
    return result


def print_last_executed_formatted_operations():
    """
    основная функция, выводящая 5 последних выполненных операций в необходимом формате
    {дата} {описание перевода}
    {откуда} -> {куда}
    {сумма перевода} {валюта}
    """
    last_five_executed_operations = get_last_five_executed_operations()

    for operation in last_five_executed_operations:

        # сбор неотформатированных значений из словаря с последними выполненными операциями
        date = operation.get('date', '')
        description = operation.get('description', '')
        who_send = operation.get('from', '')
        who_get = operation.get('to', '')
        amount = operation.get('operationAmount', '{}').get('amount', '')
        currency = operation.get('operationAmount', {}).get('currency', {}).get('name', '')

        # форматированние данных с помощью вышеописанных функций
        format_date = get_formatted_date(date)
        masked_card_account = get_masked_number(who_send)
        masked_account = get_masked_account(who_get)

        # непосредственно вывод данных в заданном формате
        print(f"{format_date} {description}\n{masked_card_account} -> {masked_account}\n{amount} {currency}\n")
