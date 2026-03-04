# URL Shortener
Микросервис для сокращения ссылок на

# Связь с автором
https://t.me/ProstoKiReal

# Технологии
- `FastAPI` (http фрэймворк)
- `PostgreSQL` (база данных)
- `Alembic` (миграции)
- `Dishka` (Di фрэймворк)

## Требования
Для запуска необходим `Docker` и `python` для тестов.

## Функционал
`POST /shorten` — создать короткую ссылку

Ожидает:
```json
{
  "original_link": "https://github.com/"
}
```
Отдаёт:
```
{
  "short_id": "LFCk4O"
}
```

`GET /{short_id}` — редирект на оригинальную ссылку
Редиректит по ссылке.

`GET /stats/{short_id}` — количество переходов.
Отдаёт:
```json
{
"count_redirects": 3
}
```

## Запуск
```bash
# Склонируйте репозиторий
git clone https://github.com/KnightCode1024/url-shortener.git

# Перейдите в папку проекта
cd url-shortener

# Создайте .env файл
copy .env.example .env

# Запуск прилажения и БД
docker compose up --build -d
```

Перейдите на http://localhost:8000/docs

## Тестирование
```bash
# Создайте виртуальное окружение
python -m venv venv
# Для python 3.14
py -m venv venv

# Активируйте виртуальное окружение
# Для windows
venv\Scripts\activate
# Для linux/macos
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Запуск тестов
pytest -v
```
