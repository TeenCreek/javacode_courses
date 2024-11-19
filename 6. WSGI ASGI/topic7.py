import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

BASE_URL = 'https://api.exchangerate-api.com/v4/latest'


@app.get(
    '/{currency}',
    summary='Получить курс валют',
    description='Возвращает курс указанной валюты к доллару США.',
)
async def get_exchange_rate(currency: str):
    """Функция для получения курса валют к доллару."""

    if len(currency) != 3 or not currency.isalpha():
        raise HTTPException(
            status_code=400,
            detail='Некорректный код валюты. Используйте 3 буквы, например USD',
        )

    url = f'{BASE_URL}/{currency.upper()}'

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        return JSONResponse(content=data)

    except requests.exceptions.HTTPError as http_error:
        if (
            response.status_code == 404
            or 'currency not found' in response.text.lower()
        ):
            raise HTTPException(
                status_code=404,
                detail=f'Валюта "{currency}" не найдена',
            )
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f'Ошибка от API: {response.text}',
            )


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='127.0.0.1', port=8000)
