"""Задача - Атрибуты класса."""

import datetime


class DateMeta(type):
    def __new__(cls, name, bases, attrs):
        attrs['created_at'] = datetime.datetime.now()

        return super().__new__(cls, name, bases, attrs)


class Date(metaclass=DateMeta):
    pass


if __name__ == '__main__':
    d1 = Date()
    created_at = d1.created_at

    assert (
        abs((datetime.datetime.now() - created_at).total_seconds()) < 1
    ), 'Время не совпадает'

    print('Тест пройден успешно')
