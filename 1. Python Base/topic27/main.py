"""Паттерн синглтон через механизм импортов."""

from topic27_singleton import Singleton2

if __name__ == '__main__':
    s5 = Singleton2()
    s6 = Singleton2()

    assert s5 is s6, 'Экземпляры класса должны быть одинаковые'

    print('Тест прошел успешно')
