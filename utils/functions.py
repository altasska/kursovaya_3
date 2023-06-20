import json

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
