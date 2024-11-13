"""паттерн синглтон тремя способами:

с помощью метаклассов
с помощью метода __new__ класса
через механизм импортов.
"""


class SingletonMeta(type):
    """Паттерн синглтон с помощью метаклассов."""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(
                *args, **kwargs
            )

        return cls._instances[cls]


class Singleton(metaclass=SingletonMeta):
    def __init__(self):
        print('Создание экземпляра Singleton')


class Singleton2:
    """Паттерн синглтон с помощью метода __new__ класса."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton2, cls).__new__(
                cls, *args, **kwargs
            )

        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            print('Создание экземпляра Singleton2')
            self._initialized = True


if __name__ == '__main__':
    s1 = Singleton()
    s2 = Singleton()
    s3 = Singleton2()
    s4 = Singleton2()

    assert s1 is s2, 'Экземпляры класса должны быть одинаковые'
    assert s3 is s4, 'Экземпляры класса должны быть одинаковые'

    print('Тесты прошли успешно')
