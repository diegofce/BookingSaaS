# Booking SaaS Backend

## Production stack (Docker)

From repository root:

```bash
docker compose up --build -d
```

Services:
- `api`: FastAPI app (`:8000`)
- `worker`: Celery worker for reminder jobs
- `db`: PostgreSQL
- `redis`: broker for Celery

The API container runs `alembic upgrade head` on startup before serving requests.

## Environment variables

Use `backend/.env.example` as reference for production env values:
- `DATABASE_URL`
- `JWT_SECRET_KEY`
- `JWT_ALGORITHM`
- `REDIS_URL`
- `CELERY_BROKER_URL`
- `ENABLE_BACKGROUND_REMINDERS`
- `BOOTSTRAP_REMINDERS_ON_STARTUP`
- `REMINDER_MINUTES_BEFORE`
- `REMINDER_PROCESSING_TIMEOUT_MINUTES`
