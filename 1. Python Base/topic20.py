"""Задача - Декоратор управления доступом."""

from functools import wraps

current_user_role = None


def set_current_user_role(role):
    """Функция для установки текущей роли пользователя."""

    global current_user_role
    current_user_role = role


def access_control(roles):
    """Декоратор для управления доступом на основе ролей пользователя."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user_role not in roles:
                raise PermissionError(
                    f'Доступ запрещен. Требуется одна из ролей: {", ".join(roles)}'
                )
            return func(*args, **kwargs)

        return wrapper

    return decorator


@access_control(roles=['admin', 'moderator'])
def delete_post(post_id):
    return f'Пост {post_id} удален'


if __name__ == '__main__':
    set_current_user_role('admin')

    assert delete_post(1) == 'Пост 1 удален', 'Пост не был удален'

    set_current_user_role('user')

    try:
        delete_post(2)
        assert False, 'PermissionError'
    except PermissionError as e:
        assert (
            str(e)
            == 'Доступ запрещен. Требуется одна из ролей: admin, moderator'
        )

    print('Тесты прошли успешно')
