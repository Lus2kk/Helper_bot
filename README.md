# TelegramBot

Многофункциональный Telegram-бот на Python с асинхронной архитектурой. Объединяет в одном боте определение погоды по геолокации, получение новостной ленты по категориям и (в планах) менеджер задач.

## Стек

- **Язык**: Python 3.12
- **Telegram-фреймворк**: aiogram 3.x (асинхронный, webhook-режим)
- **Веб-сервер**: FastAPI + uvicorn (ASGI)
- **БД**: PostgreSQL 17
- **ORM**: SQLAlchemy 2.0 (async) + asyncpg
- **Миграции**: Alembic
- **HTTP-клиент**: httpx
- **Конфигурация**: pydantic-settings (валидация `.env`)
- **Линтинг/форматирование**: ruff
- **Тестирование**: pytest + pytest-asyncio
- **Контейнеризация**: Docker Compose (Postgres)

## Архитектура

Слоистая архитектура с разделением ответственности:

```
app/
  bot/           # инициализация Bot и Dispatcher
  handler/       # хендлеры Telegram-команд и событий
  keyboards/     # определение клавиатур (Reply/Inline)
  service/       # бизнес-логика фичей
  repository/    # (план) запросы к БД
  external/      # HTTP-клиенты к внешним API
  routes/        # FastAPI-эндпоинты (webhook, /health)
  db/            # SQLAlchemy-модели, engine, сессии
  config.py      # конфигурация (pydantic-settings)
  main.py        # точка входа: сборка FastAPI-приложения
alembic/         # миграции БД
alembic.ini      # конфиг Alembic
pyproject.toml   # зависимости и конфиги инструментов
docker-compose.yml
```

**Принцип**: `handler` → `service` → `external` (внешние API) / `repository` (БД). Handler не лезет в внешние API напрямую, service не знает про Telegram. Клавиатуры вынесены в отдельный модуль, handler содержит только обработчики событий.

## Внешние API

- [Open-Meteo](https://open-meteo.com/) — погода по координатам, бесплатно, без ключа
- [GNews API](https://gnews.io/) — новости по категориям (спорт, технологии, бизнес, и т.д.)

## Что сделано

- [x] Базовая конфигурация (`pydantic-settings`, `.env`)
- [x] Docker Compose с Postgres 17
- [x] SQLAlchemy-модели: `User`, `Task`
- [x] Alembic-миграции
- [x] Каркас бота: webhook-эндпоинт на FastAPI, `/health`
- [x] Команда `/start` (welcome-сообщение + главное меню кнопок)
- [x] Команда `/help`
- [x] Главное меню (Reply-кнопки: Погода, Новости, Мои задачи, Помощь)
- [x] Фича **Погода**: `/weather` или кнопка → запрос геолокации → погода по координатам
- [x] Фича **Новости**: `/news` или кнопка → inline-кнопки выбора категории → новость с обложкой + список

## В планах

- [ ] **Task Manager**: команды для создания, просмотра, обновления статуса задач (`/tasks`, `/add_task`, `/done`)
- [ ] **Репозиторий**: слой работы с БД (через async-сессии)
- [ ] **Сохранение пользователя в БД** при `/start` (с запоминанием последней геолокации)
- [ ] **Докеризация бота** (сервис `bot` в docker-compose)
- [ ] **Логирование** (structlog)
- [ ] **Тесты** (с pytest-asyncio)
- [ ] Улучшения погоды: WMO weather codes → человекочитаемые описания, прогноз на несколько дней
- [ ] Улучшения новостей: пагинация по статьям, выбор количества
- [ ] Прогноз погоды на ближайшие часы
- [ ] Настройка языка новостей пользователем
- [ ] Inline-режим для поиска новостей

## Запуск локально

1. Клонировать репозиторий
2. Создать `.env` по образцу `.env.example`
3. Установить зависимости:
   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate.fish  # или activate для bash/zsh
   pip install -e ".[dev]"
   ```
4. Поднять Postgres:
   ```bash
   docker compose up -d
   ```
5. Применить миграции:
   ```bash
   alembic upgrade head
   ```
6. Поднять туннель для webhook (например cloudflared):
   ```bash
   cloudflared tunnel --url http://localhost:3001
   ```
7. Вписать полученный URL в `WEBHOOK_URL` в `.env`
8. Запустить бота:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 3001 --reload
   ```

## Команды бота

| Команда   | Описание                                  |
|-----------|-------------------------------------------|
| `/start`  | Приветствие                               |
| `/help`   | Справка по командам                        |
| `/weather`| Запрос погоды по геолокации               |
| `/news`   | Выбор категории новостей                  |

## Лицензия

MIT