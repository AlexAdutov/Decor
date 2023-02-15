import os
from datetime import datetime
import re
import csv


def logger(oldfunction):
    def new_function(*args, **kwargs):
        date_time = datetime.now()
        call_time = date_time.strftime('%Y-%m-%d время %H-%M-%S')
        func_name = oldfunction.__name__
        result = oldfunction(*args, **kwargs)
        with open(path, 'a') as file:
            file.write(f'\nВремя вызова функции: {call_time}\n'
                       f'Имя функции: {func_name}\n'
                       f'Аргументы функции: {args, kwargs}\n'
                       f'Возвращаемое значение функции: {result}\n'
                       f'{"___________________________________"}\n')
        return result

    return new_function


@logger
def hello_world():
    return 'Hello World'


def read_file(file_name):
    with open(file_name) as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    return contacts_list



def name_corrector(contacts_list):
    for item in contacts_list:
        full_name= ' '.join(item[:3]).split(' ')
        item[0] = full_name[0]
        item[1] = full_name[1]
        item[2] = full_name[2]

def phone_corrector(contacts_list):
    for item in contacts_list[1:]:
        re_exp=   r'(\+7|8)?\s*?\(?(\d{3})\)?[\s*-]?(\d{3})[\s*-]?(\d{2})[\s*-]?(\d{2})[\s,]?\(?(доб.)?\s?(\d{4})?\)?'

        sub = r'+7(\2)\3-\4-\5 \6\7'
        item[5] = re.sub(re_exp, sub, item[5])


def data_aggregation(contacts_list):

    contacts_list[2].append('')
    for item in contacts_list:
        first_name = item[0]
        last_name = item[1]
        for other_item in contacts_list:
            other_first_name = other_item[0]
            other_last_name = other_item[1]
            if first_name == other_first_name and last_name == other_last_name:
                if item[2] == '': item[2] = other_item[2]
                if item[3] == '': item[3] = other_item[3]
                if item[4] == '': item[4] = other_item[4]
                if item[5] == '': item[5] = other_item[5]
                if item[6] == '': item[6] = other_item[6]
    new_list = []
    for item in contacts_list:
        if item not in new_list:
            new_list.append(item)
    return new_list

@logger
def write_file(contacts_list, file_name):
    with open(file_name, "w") as f:
        data_writer = csv.writer(f, delimiter=',')
        data_writer.writerows(contacts_list)


def test_1():
    global path
    path = "main3.log"
    if os.path.exists(path):
        os.remove(path)

    contacts_list = read_file('phonebook_raw.csv')
    contacts_list = name_corrector(contacts_list)
    contacts_list = name_corrector(contacts_list)
    contacts_list = data_aggregation(contacts_list)
    write_file(contacts_list, 'phonebook.csv')

    with open(path) as log_file:
        log_file_content = log_file.read()

    print(log_file_content)


if __name__ == '__main__':
    test_1()