import json
import math
import os
import random
import time
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool, Process, Queue


def generate_data(n):
    """Генерирует список из n случайных целых чисел."""

    return [random.randint(1, 1000) for _ in range(n)]


def process_number(number):
    """Выполняет ресурсоемкую операцию — вычисляет факториал числа."""

    return math.factorial(number)


def process_single_thread(data):
    """Однопоточная обработка."""

    start_time = time.time()
    results = [process_number(number) for number in data]
    elapsed_time = time.time() - start_time

    return results, elapsed_time


def process_with_threads(data):
    """Пул потоков."""

    start_time = time.time()

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(process_number, data))

    elapsed_time = time.time() - start_time

    return results, elapsed_time


def process_with_pool(data):
    """Пул процессов."""

    start_time = time.time()

    with Pool() as pool:
        results = pool.map(process_number, data)
        pool.close()
        pool.join()

    elapsed_time = time.time() - start_time

    return results, elapsed_time


def worker(input_queue, output_queue):
    """Отдельные процессы c очередями."""

    while not input_queue.empty():
        number = input_queue.get()
        output_queue.put((number, process_number(number)))


def process_with_processes(data):
    """Отдельные процессы."""

    start_time = time.time()
    input_queue = Queue()
    output_queue = Queue()

    for number in data:
        input_queue.put(number)

    num_processes = os.cpu_count()

    processes = [
        Process(target=worker, args=(input_queue, output_queue))
        for _ in range(num_processes)
    ]

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    results = []

    while not output_queue.empty():
        results.append(output_queue.get()[1])

    elapsed_time = time.time() - start_time

    return results, elapsed_time


def save_to_json(data, file_path):
    """Запись данных в JSON файл."""

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

    print(f'Результаты сохранены в {file_path}')


if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_dir, 'results2.json')
    n = 10
    data = generate_data(n)

    single_results, single_time = process_single_thread(data)
    print(f'Однопоточная обработка: {single_time:.2f} сек')

    thread_results, thread_time = process_with_threads(data)
    print(f'Пул потоков: {thread_time:.2f} сек')

    pool_results, pool_time = process_with_pool(data)
    print(f'Пул процессов: {pool_time:.2f} сек')

    process_results, process_time = process_with_processes(data)
    print(f'Отдельные процессы: {process_time:.2f} сек')

    results = {
        'Single-threaded': single_time,
        'ThreadPool': thread_time,
        'ProcessPool': pool_time,
        'Processes': process_time,
    }

    save_to_json(results, file_path)
