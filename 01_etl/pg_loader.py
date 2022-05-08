import logging
from typing import List

import psycopg2
from data_classes import Movies
from psycopg2.extras import RealDictCursor
from utility import backoff


class PGLoader:
    """
    Класс подгружает данные из Postgres
    :param credentials - Параметры для подключения
    :param chunk - Размер доставаемых данных
    """
    def __init__(self, credentials: dict, chunk=500):
        self.db_connect = None
        self.cursor = None
        self.credentials = credentials
        self.chunk = chunk
        self.connection()

    @backoff()
    def connection(self):
        self.db_connect = psycopg2.connect(**self.credentials, cursor_factory=RealDictCursor)
        self.cursor = self.db_connect.cursor()

    @backoff()
    def make_request(self, sql):
        try:
            self.cursor.execute(sql)
        except psycopg2.OperationalError:
            logging.error('Возникла ошибки при подключении к базе данных.')
            self.connection()
            self.cursor.execute(sql)

        data = []
        rows = self.cursor.fetchmany(self.chunk)
        while rows:
            for row in rows:
                data.append(row)
            rows = self.cursor.fetchmany(self.chunk)
        return self._generate_data(data)

    def _generate_data(self, data) -> List:
        # Полученные данные переводим в Movies
        if not data:
            return []
        list_data = []

        for row in data:
            row = dict(row)
            list_data.append(Movies(**row))

        self.cursor.close()
        return list_data
