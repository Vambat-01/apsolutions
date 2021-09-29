from fastapi import FastAPI
from elastic import SearchIndex, wait_elastic_to_load
from documents_storage import DocumentsStorage
import sqlite3
import asyncio
from uvicorn import Config, Server
from pathlib import Path
from csv_storage import load_csv
import typer
from elasticsearch import Elasticsearch

ELASTIC_INDEX = "documents"
DATABASE_PATH = Path("documents_db.sqlite")
CSV_PATH = Path("resources/posts.csv")


def main(server_host: str, server_port: int, search_host: str, search_port: int, populate: bool = False):
    es = Elasticsearch(host=search_host, port=search_port)
    search_index = SearchIndex(es, ELASTIC_INDEX)
    wait_elastic_to_load(search_index)
    app = FastAPI()
    path_to_database = DATABASE_PATH
    connection = sqlite3.connect(path_to_database, check_same_thread=False)
    documents_storage = DocumentsStorage(connection)

    if populate:
        data = load_csv(CSV_PATH)
        documents_storage.create_table()
        documents_storage.add_documents(data)
        for record in documents_storage.get_all_documents():
            search_index.add(record.id, record.item.text)

    async def do_main():
        @app.get("/documents")
        async def get_documents(text: str):
            ids = search_index.search(text, 20)
            response = documents_storage.get_documents(ids)
            return response

        @app.delete("/documents/{id}")
        async def delete_documents(id: int):
            search_index.delete(id)
            documents_storage.delete(id)
            return {"status": "ok"}

        config = Config(app=app, host=server_host, port=server_port)
        server = Server(config)
        await server.serve()
        connection.close()

    asyncio.run(do_main())


if __name__ == "__main__":
    typer.run(main)
