# Contacts REST API 

REST API для зберігання та управління контактами, побудований за допомогою **FastAPI**, **SQLAlchemy** та **PostgreSQL**.

---

## Запуск проєкту

### Варіант 1 — Docker Compose (рекомендовано)

```bash
# Клонувати репозиторій
git clone https://github.com/nikita-kotliar/UMT-pythonweb-hw-08.git
cd UMT-pythonweb-hw-08
# Запустити сервіси
docker compose up --build
```

API доступне за адресою: http://localhost:8000  
Swagger UI: http://localhost:8000/docs
OpenAPI JSON: http://localhost:8000/openapi.json

---


### Пошук контактів

```
GET /contacts/?first_name=John
GET /contacts/?last_name=Doe
GET /contacts/?email=john
GET /contacts/?first_name=John&last_name=Doe
```

Пошук нечутливий до регістру, підтримує часткове співпадіння.

### Приклад тіла запиту (створення)

```json
{
  "first_name": "Нікіта",
  "last_name": "Котляр",
  "email": "knr200710@gmail.com",
  "phone": "+380976731529",
  "birthday": "2007-04-22",
  "additional_data": "..."
}
```
