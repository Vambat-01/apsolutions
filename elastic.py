from elasticsearch import Elasticsearch, NotFoundError
from typing import List
from pydantic import BaseModel
import requests
from time import sleep
from datetime import date, datetime


class ElasticData(BaseModel):
    """
        Данные для ElasticSearch
    """
    text: str


class ResponseHitItem(BaseModel):
    """
        Данные поиска
    """
    id: int
    source: ElasticData

    class Config:
        fields = {'id': '_id', 'source': '_source'}


class ResponseHit(BaseModel):
    """
        Подкласс поиска
    """
    hits: List[ResponseHitItem]


class Response(BaseModel):
    """
        Ответ поиска в Elastic
    """
    hits: ResponseHit


class SearchIndex:
    """
        Текстовый индекс на основе Elastic
    """
    def __init__(self, elastic_search: Elasticsearch, index: str):
        """
            :param elastic_search: Подключение к Elasticsearch
            :param index: индекс в Elasticsearch
        """
        self.index = index
        self._es = elastic_search

    def add(self, id: int, text: str):
        """
            Добавляет элемент в поисковый индекс.
        :param id: идентификатор
        :param text: текст
        """
        body = {"text": text}
        self._es.index(index=self.index, id=id, body=body)

    def search(self, text: str, size: int) -> List[int]:
        """
            Возвращает элементы из индекса содержащие `text`
        :param text: текст
        :param size: количество результатов
        :return: список ids
        """
        search_data = self._es.search(index=self.index,
                                      body={"from": 0,
                                            "size": size,
                                            "query":
                                                {"match": {"text": {"query": text}}}
                                            }
                                      )
        data = Response.parse_obj(search_data)
        ids = [d.id for d in data.hits.hits]
        return ids

    def delete(self, id: int):
        """
            Удаляет елемент из индекса
        :param id: идентификатор документа
        """
        self._es.delete(index=self.index, id=id)


def wait_elastic_to_load(es: SearchIndex):
    while True:
        try:
            es.search('whatever', 1)
        except NotFoundError:
            print('elastic is ready')
            return
        except Exception as e:
            print(f'{datetime.now()} Elastic is not ready')
            print(e)
            sleep(1)
