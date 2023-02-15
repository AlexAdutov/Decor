# Доработать декоратор logger в коде ниже.
# Должен получиться декортор, который записывает
# в файл 'main.log' дату и время вызова функции,
# имя функции, аргументы, с которыми вызвалась и
# возвращаемое значение. Функция test_1 в коде
# ниже также должна отработать без ошибок.

import os
from datetime import datetime

def logger(old_function):

    def new_function(*args, **kwargs):
        date_time =datetime.now()
        call_time = date_time.strftime('%Y-%m-%d время %H-%M-%S')
        func_name = old_function.__name__
        result = old_function(*args, **kwargs)
        with open(path, 'a') as file:
            file.write(f'\nВремя вызова функции: {call_time}\n'
                       f'Имя функции: {func_name}\n'
                       f'Аргументы функции: {args, kwargs}\n'
                       f'Возвращаемое значение функции: {result}\n'
                       f'{"___________________________________"}\n')
        return result
    return new_function


def test_1():
    global path
    path = 'main1.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    print(log_file_content)
    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_1()