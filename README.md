# Web-приложение для поиска по текстам документов

## Запуск Web-приложения используя [Docker](https://www.docker.com/)
1. Cоздайте `Docker` образ приложения: `docker build -t web-app .`
1. Запустите web-приложение: `docker-compose up`

## Проверьте работоспособность web-приложения
1. Установите зависимости: `pip install -r requirements.txt`
1. Запустите системные тесты: `python -m unittest tests/system_tests.py`
1. Тесты должны успешно пройти

## Документация к сервису
- Перейдите по ссылке [openapi](http://localhost:8000/docs)