# Pochta Chat

Лёгкий и быстрый чат в реальном времени на базе FastAPI и WebSocket

---

## Описание

Pochta Chat — это SPA с фронтендом на Bootstrap и jQuery и бекендом на FastAPI + TortoiseORM, поддерживающий регистрацию, аутентификацию, групповые и приватные чаты в реальном времени через WebSocket.

---

## Документация API

- **OpenAPI**: `http://localhost:8000/openapi.json`  
- **Swagger UI**: `http://localhost:8000/docs`  
- **Redoc**: `http://localhost:8000/redoc`  

---

## Требования

- Docker & Docker Compose  
- Git  

---

## Установка и запуск

1. **Клонировать репозиторий**  
   ```bash
   git clone https://github.com/GabbasovDinar/pochta-chat
   cd pochta-chat
   ```

2. **Настроить переменные окружения**  
   - Переименуйте файл  
     ```bash
     mv .env.example .env
     ```  
   - При необходимости отредактируйте значения в `.env`. По умолчанию используются:
     ```env
     POSTGRES_USER=postgres
     POSTGRES_PASSWORD=postgres
     POSTGRES_DB=pochta_chat_db
     DATABASE_HOST=db
     DATABASE_PORT=5432

     SECRET_KEY=your-secret-key
     ALGORITHM=HS256
     ACCESS_TOKEN_EXPIRE_MINUTES=60
     PASSWORD_CRYPT_ALGORITHM=bcrypt
     PASSWORD_HASHING_ROUNDS=12
     ```
   
3. **Собрать и запустить контейнеры**  
   ```bash
   docker compose build
   docker compose up
   ```

4. **Перейти в браузере**  
   - Фронтенд: `http://localhost`  
   - Бекенд API: `http://localhost:8000`  

---

## Структура проекта

```
.
├── backend/          # FastAPI + TortoiseORM
│   ├── app/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/         # SPA на Bootstrap + jQuery
│   ├── index.html
│   ├── api.js
│   └── Dockerfile
├── docker-compose.yml
└── .env.example
```

---

## Полезные команды

- **Пересобрать и поднять всегда заново**  
  ```bash
  docker compose down
  docker compose up --build
  ```

- **Просмотр логов контейнеров**  
  ```bash
  docker compose logs -f
  ```

- **Остановка**  
  ```bash
  docker compose down
  ```

---

## Лицензия

MIT License
