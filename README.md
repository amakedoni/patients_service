# 💊 mAIsafe

Полностью готовый backend-проект для управления медицинскими данными (аналог Medisafe)  
Реализованы все таблицы, описанные в спецификации:

- **users** — пользователи (пациенты / мед-друзья)  
- **user_relations** — связи «пациент ↔ мед-друг»  
- **schedules** — расписания приёма лекарств  
- **medicines** — препараты  
- **intake_history** — история приёма лекарств  

---

## 🧩 Архитектура проекта
```
backend/
├── .env
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
│
├── alembic/
│ ├── env.py
│ └── versions/
│ └── 0001_initial_migration.py
│
├── app/
│ ├── main.py
│ ├── core/
│ │ └── config.py
│ ├── db/
│ │ ├── base.py
│ │ └── session.py
│ └── patients/
│ ├── router.py
│ ├── service.py
│ ├── models/
│ │ ├── user.py
│ │ ├── relation.py
│ │ ├── schedule.py
│ │ ├── medicine.py
│ │ └── intake.py
│ └── schemas/
│ ├── user.py
│ ├── relation.py
│ ├── schedule.py
│ ├── medicine.py
│ └── intake.py
│
└── tests/
└── conftest.py
```
---

## ⚙️ Установка и запуск

### 1. Установи Docker и Docker Compose

Проверь, что всё работает:
```bash
docker -v
docker compose version
```
2. Запуск проекта
Перейди в папку проекта:
```bash
cd backend
```
Собери и запусти контейнеры:
```bash
docker compose up --build
```
Приложение и база данных запустятся:
FastAPI: http://localhost:8000/docs
PostgreSQL: порт 5432

## 🧱 Таблицы базы данных
```
Таблица	       │          Назначение                │ Особенности
users	         │ Пользователи (пациенты/мед-друзья) │	UUID для синхронизации
user_relations │	Связь пациент ↔ мед-друг	        │ Один ко многим
schedules	     │       Расписания приёма	          │ Ограничения по длительности и циклам
medicines	     │        Препараты	                  │ FK на users и schedules
intake_history │ История приёма лекарств	          │ Лог состояния приёма, пропуска, дозы
```
## 📦 Описание окружения
```
.env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/medisafe
```
### Docker-сервисы:
```
Сервис	│ Назначение
db	    │ PostgreSQL 15
app	    │ FastAPI backend
```
## ⚡ Полезные команды
Команда	Описание
```docker compose up -d```	Запустить приложение в фоне
```docker compose logs -f app```	Смотреть логи приложения
```docker compose down -v```	Остановить и удалить контейнеры и volume
## 🧠 Примечания
Пароль пользователей (hash_password) хранится в виде текстового хэша (не открытым текстом).
uuid выдаётся клиенту для синхронизации с сервером.
Все внешние ключи каскадно удаляются при удалении родителя (ondelete="CASCADE").
Base.metadata.create_all() в main.py создаёт таблицы при первом старте, даже без миграций.

