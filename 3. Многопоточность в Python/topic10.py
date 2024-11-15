import asyncio
import json
import os

import aiohttp

urls = [
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
]


async def fetch_url(session: aiohttp.ClientSession, url: str):
    """Функция для выполнения запроса и возврата URL и статус-кода."""

    try:
        async with session.get(url) as response:
            return url, response.status
    except aiohttp.ClientError:
        return url, 0


def save_results_to_file(results: dict[str, int], file_path: str):
    """Функция для сохранения результатов в файл JSON."""

    try:
        with open(file_path, 'w') as file:
            for url, status_code in results.items():
                json.dump({'url': url, 'status_code': status_code}, file)
                file.write('\n')

    except IOError as e:
        print(f'Ошибка при записи в файл {file_path}: {e}')


async def fetch_urls(urls: list[str], file_path: str):
    """Функция для асинхронного получения статусов URL с ограничением запросов."""

    timeout = aiohttp.ClientTimeout(total=10)
    results = {}

    connector = aiohttp.TCPConnector(limit=5)

    async with aiohttp.ClientSession(
        connector=connector, timeout=timeout
    ) as session:
        tasks = [fetch_url(session, url) for url in urls]

        for task in asyncio.as_completed(tasks):
            url, status_code = await task
            results[url] = status_code

    save_results_to_file(results, file_path)


current_dir = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(current_dir, 'results.json')

if __name__ == '__main__':
    asyncio.run(fetch_urls(urls, file_path))
    asyncio.run(fetch_urls(urls, file_path))
