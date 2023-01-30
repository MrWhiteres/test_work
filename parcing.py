from ast import literal_eval
from os import listdir, path
from pathlib import Path
from re import sub, match

from click import command, option
from dateutil.parser import parse
from elasticsearch import Elasticsearch
from numpy import array
from pandas import read_csv

email_regex = r"^([\w\.]+@[\w]+\.[a-zA-Z]+)$"
clear_regex = r"\"|\'|[\[\]\(\)\{\}]|nan|`|\B:\B|\B/{2,}|\B//\w\B|^\?\B|\B\?\B"


@command()
@option("--filename", default="test.csv")
def init_work(filename: str):
    """The method sta"""
    exist_file = check_file(filename)
    if not not exist_file:
        data_in_csv = read_csv(filename, error_bad_lines=False, engine="python", converters={'Sequence': clean})
        head, values = return_data_list(data_in_csv)
        data = append_data(head, values)

        data_sort_date = False
        data_sort_alphabet = False

        if question_input('Print data?'):
            print_data(convert_data(data))

        if question_input('Sort by date?'):
            data_sort_date = sort_by_key(data, 'date', 'login_time')
            if data_sort_date and question_input('Print result?'):
                print_data(convert_data(data_sort_date))

        if question_input('Sort by alphabet?'):
            data_sort_alphabet = sort_by_key(data, 'alphabet', 'customers_firstname')
            if data_sort_alphabet and question_input('Print result?'):
                print_data(convert_data(data_sort_alphabet))

        if question_input('Search data that contain an email?'):
            search_element = search(data, email_regex)
            if search_element and question_input('Print result?'):
                print_data(convert_data(search_element))

        if question_input('Push data to elasticsearch?'):
            push_data(convert_data(data))
    else:
        print(f'File-"{filename}" not found!')


def check_file(filename: str) -> bool:
    """Checks if there is a file in the current directory or in the given path"""
    file_path = Path().resolve()
    if ('/' in filename) and path.exists(filename[:filename.rfind('/') + 1]) or \
            ('\\' in filename) and path.exists(filename[:filename.rfind('\\') + 1]):
        file_path = filename[:filename.rfind('\\') + 1] if '\\' in filename else filename[:filename.rfind('/') + 1]
        filename = filename[filename.rfind('\\') + 1:] if '\\' in filename else filename[filename.rfind('/') + 1:]
    dir_list = listdir(file_path)
    return filename in dir_list


def return_data_list(data: array) -> tuple:
    """Clears data from garbage elements"""
    head = {key: [] for key in data.keys()}
    values = [
        sub(clear_regex, '', ''.join(map(str, value.tolist()))).split(',')
        for value in
        data.values]
    values = [convert_data_type(data_list) for data_list in values]
    return head, values


def convert_data_type(data: list) -> list:
    """Converts a data type"""
    for index in range(len(data)):
        data[index] = convert_type(data[index])
    return data


def convert_type(element: str) -> int | float | str:
    """Sub worker for 'Converts a data type'"""
    try:
        if '.' not in element:
            return int(element)
        return float(element)
    except (TypeError, ValueError):
        return element


def append_data(headers: dict, values: list) -> dict:
    """Return data dict"""
    data = dict()
    for index, keys in enumerate(headers.keys()):
        data[keys] = get_list_data(index, values)
    return data


def get_list_data(index, data_list) -> list:
    """Sub worker 'Return data dict'"""
    return [{list_data[index]: value_index} for value_index, list_data in enumerate(data_list)]


def question_input(question: str) -> bool:
    """Method validates answers to questions"""
    answer_dict = {'y': True, 'n': False}
    while True:
        answer = input(fr'{question} Y\N: ').lower()
        if answer in answer_dict:
            return answer_dict[answer]
        question = r'An incorrect answer was given, the available options are'


def print_data(data: list or dict):
    """Print data"""
    if type(data) == list:
        print(*data, sep='\n')
    if type(data) == dict:
        for key, value in data.items():
            print(fr'{key} {value}')
    for i in range(3):
        print()


def sort_by_key(data: dict, key: str, key_for_search: str) -> dict | None:
    """Sorted data by key"""
    sorted_dict = dict()
    check = check_key(key, data.get(key_for_search, None))

    if not check:
        print("Invalid key")
        return None

    data[key_for_search] = check
    if key == 'date':
        data[key_for_search] = sorted(data[key_for_search],
                                      key=lambda element: parse(list(element.keys())[0], fuzzy=True))
    if key == 'alphabet':
        data[key_for_search] = sorted(data[key_for_search], key=lambda element: list(element.keys())[0].lower())
    check_id = [list(element.values())[0] for element in data[key_for_search]]

    for key, value in data.items():
        sorted_dict[key] = return_new_data_list(check_id, value)

    return sorted_dict


def check_key(type_sort: str, data_list: list) -> bool | list:
    """Check correct data for a key"""
    if not data_list:
        return False
    data_return = [False for _ in range(len(data_list))]
    result = list()

    for index, element in enumerate(data_list):
        try:
            date = None
            if type_sort == 'date':
                date = return_new_date(list(element.keys())[0])
                parse(date, fuzzy=True)
            if type_sort == 'alphabet':
                date = str(list(element.keys())[0])
            result.append(True)
            data_return[index] = {date: index}
        except (ValueError, TypeError):
            result.append(False)
    if not not all(result):
        return data_return
    return False


def return_new_date(date: str) -> str:
    """Delete date error"""
    if "0000" in date:
        return '1970-01-01 00:00:00'
    return date


def return_new_data_list(check_list: list, data_list: list) -> list:
    """Return sorted data list"""
    result = list()
    for i in check_list:
        for element in data_list:
            for key, value in element.items():
                if value == i:
                    result.append({key: value})
    return result


def search(data: dict, regex_pattern: str) -> dict | None:
    """Search element by regex"""
    search_index = find_index_for_regex(regex_pattern, data)
    if len(search_index) == 0:
        print('Element not found')
        return None
    filter_element = return_element_by_id(search_index, data)
    return filter_element


def find_index_for_regex(regex: str, data: dict) -> list:
    """Sub worker for 'Search element by regex'"""
    index_list = list()
    for value in data.values():
        for data_list in value:
            for key_2, value_2 in data_list.items():
                if match(regex, str(key_2)):
                    index_list.append(value_2)
    return index_list


def return_element_by_id(id_list: list, data: dict) -> dict:
    """Create new data dict by id"""
    result_dict = dict()
    for key, value in data.items():
        find_element_list = list()
        for data_list in value:
            for key_2, value_2 in data_list.items():
                if value_2 in id_list:
                    find_element_list.append({key_2: value_2})
            result_dict[key] = find_element_list
    return result_dict


def create_connection() -> Elasticsearch:
    """The method returns a connection to Elasticsearch"""
    return Elasticsearch(['localhost:9200'])


def push_data(data: list):
    """Push data in elastic"""
    es = create_connection()
    for data_dict in data:
        es.index(index='upload_data', document=data_dict)
    print(es.search(index='upload_data'))


def return_length_data(data: dict) -> int:
    """Return length data element"""
    for value in data.values():
        return len(value)


def convert_data(data: dict) -> list:
    """Return converted data"""
    length = return_length_data(data)
    new_data = []
    for index in range(length):
        data_dict = dict()
        for key, data_list in data.items():
            data_value = [element for value in data_list for element, element_index in value.items() if
                          element_index == index]
            data_dict[key] = data_value[0] if data_value else ''
        new_data.append(data_dict)
    return new_data


def clean(x):
    return literal_eval(x)


if __name__ == '__main__':
    init_work()
