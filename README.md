# 🍽️ SQLAlchemy Project Restaurant

Учебный проект для практики **FastAPI**, **SQLAlchemy**, **Pydantic** и асинхронной работы с базой данных. Реализован минимальный REST API для управления рестораном: заказ блюд, готовка, отображение меню и админские действия.

## 📁 Структура проекта

```
src/
└── restaurant/
    ├── core/         # Настройки, база данных и вспомогательные данные
    ├── crud/         # Логика работы с БД (Create, Read, Update, Delete)
    ├── models/       # SQLAlchemy ORM модели
    ├── routers/      # FastAPI ручки (эндпоинты)
    ├── main.py       # Точка входа в приложение
    └── schemas.py    # Pydantic-схемы (DTO)
```

## 🚀 Возможности

- Заказ блюд (доставка или на месте)
- Асинхронная готовка заказов
- Получение меню
- Админский CRUD по сотрудникам, блюдам и заказам
- DTO-валидация с Pydantic
- Обработка ошибок и корректные ответы API

## 🛠️ Стек технологий

- Python 3.11+
- FastAPI
- SQLAlchemy 2.0 (async)
- Pydantic
- Uvicorn
- PostgreSQL (или SQLite для локального теста)

## ▶️ Запуск

1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

2. Настройте `.env` файл (пример ниже):
   ```env
   DB_URL=postgresql+asyncpg://user:password@localhost/db_name
   ```

3. Запустите сервер:
   ```bash
   uvicorn src.restaurant.main:app --reload
   ```

## ⚙️ Пример .gitignore

```gitignore
__pycache__/
*.pyc
*.pyo
*.pyd
.env
```

## 🔧 Планируемые улучшения (v2.0)

- Авторизация и роли (JWT)
- Кеширование
- Фоновые задачи (например, доставка)
- WebSocket-оповещения
- Тесты

---

**Автор**: W1lden  
*Проект сделан в образовательных целях.*
