from models import Document, Record
import sqlite3
import threading
from typing import Tuple
import json
from datetime import datetime
from typing import List


class CreateDatabaseException(Exception):
    """
        Ошибка создания SQLite базы данных
    """
    pass


class DocumentsStorage:
    """
        Хранения документов в SQLite базы данных
    """

    def __init__(self, connection: sqlite3.Connection):
        """
        :param connection: подключение к базе данных
        """
        self.connection = connection
        # Lock нужен, чтобы базой данных пользовался только один thread
        self.connection_lock = threading.Lock()

    def create_table(self):
        """
            Создаст  необходимую таблицу в SQLite базе данных. Таблица будут пустой
        """
        with self.connection:
            self.connection.executescript("""
                                            CREATE TABLE documents (
                                            id INTEGER NOT NULL PRIMARY KEY,
                                            rubrics TEXT NOT NULL,
                                            text TEXT NOT NULL,
                                            created_date TEXT NOT NULL
                                            )
                                            """)

    def add_documents(self, documents: List[Document]):
        """
            Добавляет список документов базе данных
        :param documents: список документов
        """
        with self.connection_lock:
            with self.connection:
                sqltuples = [DocumentsStorage._to_tuple(d) for d in documents]
                self.connection.executemany("INSERT INTO DOCUMENTS(rubrics, text, created_date) VALUES(?, ?, ?)",
                                            sqltuples
                                            )

    def get_documents(self, ids: List[int]) -> List[Record[Document]]:
        """
            Получает список документов из базы данных
        :param ids: список идентификаторов
        :return: список документов
        """
        with self.connection_lock:
            with self.connection:
                sql = "SELECT ID, RUBRICS, TEXT, CREATED_DATE from documents where id in ({seq}) " \
                      "ORDER BY created_date".format(seq=','.join(['?'] * len(ids)))
                data = self.connection.execute(sql, ids)
                return DocumentsStorage._to_records(data)

    def get_all_documents(self) -> List[Record[Document]]:
        """
            Получает список всех документов из базы данных
        """
        with self.connection_lock:
            with self.connection:
                data = self.connection.execute("SELECT ID, RUBRICS, TEXT, CREATED_DATE from documents")
                return DocumentsStorage._to_records(data)

    def delete(self, id: int):
        """
            Удаляет документ из базы данных
        :param id: идентификатор документа
        """
        with self.connection_lock:
            with self.connection:
                self.connection.execute("DELETE from DOCUMENTS where ID = ?", (id, ))

    @staticmethod
    def _to_records(cursor: sqlite3.Cursor) -> List[Record[Document]]:
        records = []
        for record in cursor:
            id = record[0]
            document = DocumentsStorage._from_tuple((record[1], record[2], record[3]))
            records.append(Record(id=id, item=document))
        return records

    @staticmethod
    def _to_tuple(document: Document) -> Tuple[str, str, str]:
        return (json.dumps(document.rubrics), document.text, document.created_date.isoformat())

    @staticmethod
    def _from_tuple(t: Tuple[str, str, str]) -> Document:
        rubrics, text, created = t
        return Document(rubrics=json.loads(rubrics), text=text, created_date=datetime.fromisoformat(created))
