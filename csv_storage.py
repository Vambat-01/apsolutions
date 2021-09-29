import pandas as pd
from documents_storage import Document
import json
import datetime
from typing import List
from pathlib import Path


def load_csv(filepath: Path) -> List[Document]:
    """
        Считывает документы из csv файла
    :param filepath: путь к файлу
    :return: список документов
    """
    df = pd.read_csv(filepath)
    data = []
    for d in df.itertuples():
        data.append(Document(rubrics=json.loads(d.rubrics.replace("'", '"')),
                             text=d.text,
                             created_date=datetime.datetime.strptime(d.created_date, "%Y-%m-%d %H:%M:%S")
                             )
                    )
    return data
