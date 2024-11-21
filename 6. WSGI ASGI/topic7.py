import json
from typing import Any

import requests


def fetch_exchange_rate(currency: str):
    """Получает курс валюты из API."""

    API_URL = f'https://api.exchangerate-api.com/v4/latest/{currency}'

    try:
        response = requests.get(API_URL)
        response.raise_for_status()

        data = response.json()

        if 'rates' not in data:
            raise ValueError('Неверный формат ответа от API')

        return data

    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 404:
            raise ValueError(f'Валюта {currency} не поддерживается API')

        raise ValueError(f'Ошибка запроса: {err}')

    except requests.exceptions.RequestException as err:
        raise ValueError(f'Ошибка запроса: {err}')

    except json.JSONDecodeError:
        raise ValueError('Неверный ответ от API')


async def send_response(send: Any, status: int, content: dict):
    """Унифицированный метод отправки ответа."""

    await send(
        {
            'type': 'http.response.start',
            'status': status,
            'headers': [(b'content-type', b'application/json')],
        }
    )
    await send(
        {
            'type': 'http.response.body',
            'body': json.dumps(content, ensure_ascii=False).encode('utf-8'),
        }
    )


async def app(scope: dict, receive: Any, send: Any):
    """ASGI-приложение для проксирования курса валют."""

    if scope['type'] != 'http':
        await send_response(send, 500, {'error': 'Неверный тип запроса'})

        return

    path = scope.get('path', '/').lstrip('/')

    if not path or len(path) != 3 or not path.isalpha():
        await send_response(
            send,
            400,
            {'error': 'Укажите валюту из 3 буквенных символов'},
        )

        return

    currency = path.upper()

    try:
        data = fetch_exchange_rate(currency)

        await send_response(send, 200, data)

    except ValueError as err:
        await send_response(send, 400, {'error': str(err)})
