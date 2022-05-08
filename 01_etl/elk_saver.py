import logging

from elasticsearch import Elasticsearch, helpers
from elasticsearch.exceptions import ConnectionError
from utility import backoff
from typing import Optional
from data_classes import Movies


class ELKConnections:
    """
       Класс загружает данные в ELK
       :param credentials - Параметры для подключения
       :param index - Имя индекса
       """
    def __init__(self, credentials: dict, index: dict):
        self.credentials = credentials
        self.index = index
        self.connect()

    @backoff()
    def connect(self):
        self.client = Elasticsearch(**self.credentials)
        self.create_index()

    def create_index(self):
        if not self.client.indices.exists(index=self.index.get('index')):
            self.client.indices.create(**self.index)

    def generate_data(self, rows: Optional[Movies]):
        for row in rows:
            yield {
                '_index': self.index.get('index'),
                '_id': row.id,
                '_source': row.json()
            }

    @backoff()
    def bulk_update(self, rows):
        try:
            helpers.bulk(self.client, self.generate_data(rows))
        except ConnectionError:
            logging.error('Отсутствует соединение с ELK')
            self.connect()
            helpers.bulk(self.client, self.generate_data(rows))
