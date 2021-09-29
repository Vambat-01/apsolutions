from typing import TypeVar, Generic, List
from pydantic import BaseModel
from datetime import datetime


T = TypeVar('T')


class Record(Generic[T], BaseModel):
    """
        Запись в хранилище. Данные + id
    """
    id: int
    item: T


class Document(BaseModel):
    """
        Данные о документе
    """
    rubrics: List[str]
    text: str
    created_date: datetime
