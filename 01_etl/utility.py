import abc
import json
import logging
from functools import wraps
from json import JSONDecodeError
from pathlib import Path
from time import sleep
from typing import Any, Optional

from queryes import ALL_DATA_SQL, FW_SQL


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10):
    """
    Функция для повторного выполнения функции через некоторое время, если возникла ошибка.
    Использует наивный экспоненциальный рост времени повтора (factor) до граничного времени ожидания (border_sleep_time)

    Формула:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time
    :param start_sleep_time: начальное время повтора
    :param factor: во сколько раз нужно увеличить время ожидания
    :param border_sleep_time: граничное время ожидания
    :return: результат выполнения функции
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            time = start_sleep_time
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    msg = f'An error - "{e}" occurred while executing the function - "{func.__name__}"'
                    logging.error(msg)
                    time = border_sleep_time if time >= border_sleep_time else min(time * factor, border_sleep_time)
                    sleep(time)
        return inner
    return func_wrapper


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище"""
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        """Загрузить состояние локально из постоянного хранилища"""
        pass


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: Optional[str] = None):
        self.file_path = Path(file_path)
        open(self.file_path, 'a').close()

    def save_state(self, state: dict) -> None:
        Path(self.file_path).write_text(json.dumps(state))

    def retrieve_state(self) -> dict:
        return json.loads(Path(self.file_path).read_text())


class State:
    """
    Класс для хранения состояния при работе с данными, чтобы постоянно не перечитывать данные с начала.
    Здесь представлена реализация с сохранением состояния в файл.
    В целом ничего не мешает поменять это поведение на работу с БД или распределённым хранилищем.
    """

    def __init__(self, storage: BaseStorage):
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа"""
        self.storage.save_state({key: value})

    def get_state(self, key: str) -> Any:
        """Получить состояние по определённому ключу"""
        try:
            data = self.storage.retrieve_state()
        except JSONDecodeError:
            return '{}'
        return data.get(key, None)


def get_or_set_stage(date_time=None):
    # Функция сохраняет дату, если она была отправлена. В случаи отсутствия даты, возвращает
    # сохраненную.
    if date_time:
        State(JsonFileStorage('stage.json')).set_state(key='date_time', value=date_time)
    else:
        return State(JsonFileStorage('stage.json')).get_state('date_time')


def get_sql(date_time):
    # Относительно полученных данных возвращает SQL
    if date_time == '{}':
        return ALL_DATA_SQL
    else:
        return FW_SQL.format(date_time=date_time)
