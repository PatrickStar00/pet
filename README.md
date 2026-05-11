# Pet-проект с микросервисной архитектурой

## Структура

Проект реализован как набор микросервисов в папке `microservices`:

- `auth` — регистрация пользователей и выдача JWT
- `menu` — меню, добавление и удаление блюд  
- `order` — создание и управление заказами
- `gateway` — HTTP proxy, маршрутизация запросов между сервисами

## Требования

- Python 3.10+
- База данных PostgreSQL (используется `asyncpg` + `SQLAlchemy`)

## P.S.
- В ветке main_docker лежит версия проекта с контейнеризацией Docker

## 1) Подготовка окружения 

### .env файлы

В проекте используется загрузка переменных окружения через `python-dotenv` (функция `load_dotenv()`), поэтому перед запуском необходимо создать `.env` файлы с адресами/параметрами подключения к БД и URL сервисов.

Ожидаемые переменные:

- `DB_URL` — строка подключения к PostgreSQL для конкретного сервиса (auth/menu/order)
- `AUTH_URL` — базовый URL сервиса auth
- `MENU_URL` — базовый URL сервиса menu 
- `ORDER_URL` — базовый URL сервиса order 

Практика создания:

- Создайте `.env` **в папках микросервисов** (`microservices/auth`, `microservices/menu`, `microservices/order`, `microservices/gateway`) — чтобы соответствующие переменные были доступны тому процессу, который вы запускаете.

Пример `.env`:

```env
DB_URL=postgresql+asyncpg://USER:PASSWORD@HOST:5432/DB_NAME

AUTH_URL=http://127.0.0.1:8001
MENU_URL=http://127.0.0.1:8002
ORDER_URL=http://127.0.0.1:8003
```

> ВАЖНО: для `DB_URL` используйте корректную БД/схему под каждый сервис или одну общую БД (как вам удобнее) — но значение должно быть определено до старта приложения.

### Папка certs для auth (обязательно)

В `auth` микросервисе используются RSA ключи JWT.

Сделайте папку:

- `microservices/auth/certs/`

И поместите в нее **приватный и публичный** ключи:

- `microservices/auth/certs/jwt-private.pem`
- `microservices/auth/certs/jwt-public.pem`

Ключи должны быть в формате PEM. Код `auth` читает ключи из путей:

- `certs/jwt-private.pem`
- `certs/jwt-public.pem`

Поэтому ключи должны лежать именно в этой папке относительно текущей рабочей директории запуска.

## 2) Установка зависимостей

### В корне проекта

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 3) Запуск сервисов

После старта любого сервиса(кроме gateway) нужно создать схему БД эндпоинтом:

- `POST /create_new_db`

### Auth

Запуск (пример):

```bash
uvicorn microservices.auth.main:app --reload --port 8001
```

### Menu

```bash
uvicorn microservices.menu.main:app --reload --port 8002
```

### Order

```bash
uvicorn microservices.order.main:app --reload --port 8003
```

### Gateway

```bash
uvicorn microservices.gateway.main:app --reload --port 8000
```

Gateway был добавлен для понимания того, как он используется в ообщем виде, поэтому реализация его сделана вручную через простые запросы:

- `GET  /{service}/{path}`
- `POST /{service}/{path}`
- `DELETE /{service}/{path}`

где `{service}` ∈ `auth`, `menu`.

## 4) Пример ручного теста

1. Зарегистрируйте пользователя в auth:

- `POST /register`

2. Получите JWT токен:

- `POST /login`

3. Используйте `token`, в запросах order сервиса через форму, отправляя через тело запроса массив "items" с параметрами "menu_item_id" и "quantity".

- `POST /orders`
