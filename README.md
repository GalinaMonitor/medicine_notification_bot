# Телеграм-бот для записи пациентов, участвующих в исследовании

Для сбора статистики пациентов, участвующих в исследованиях, нужно через определенное время повторно брать анализы.
Бот позволяет записывать пациентов и назначать их на исследования. После этого ответственным врачам в определенное время приходят оповещения о повторном взятии анализов.
## Технологии
- Aiogram
- Celery
- Docker/Docker-compose
## Getting started
Создать в корневой директории .env файл с переменными redis_url, bot_token

`docker compose up -d`
