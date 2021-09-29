FROM python:3.9

COPY ./resources /app/resources
COPY ./requirements.txt /app/requirements.txt
COPY ./documents_storage.py /app/documents_storage.py
COPY ./elastic.py /app/elastic.py
COPY ./models.py /app/models.py
COPY ./server.py /app/server.py
COPY ./csv_storage.py /app/csv_storage.py

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "server.py", "0.0.0.0", "8000", "elastic", "9200", "--populate"]
