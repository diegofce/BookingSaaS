# Repository Guidelines

## Project Structure & Module Organization
This repository has a FastAPI backend and a React frontend:

- `backend/app/`: FastAPI application code.
- `backend/app/routers/`: API endpoints (HTTP layer only).
- `backend/app/services/`: Business rules and orchestration.
- `backend/app/crud/`: SQLAlchemy data-access helpers.
- `backend/app/models/`: ORM models (SQLAlchemy 2.0 `Mapped[...]` style).
- `backend/app/schemas/`: Pydantic request/response models.
- `backend/app/core/`, `backend/app/db/`, `backend/alembic/`: config, database setup, and migrations.
- `frontend/src/`: React + TypeScript app (Vite, Axios, Tailwind, FullCalendar).
- `frontend/tests/`: unit, integration, and e2e smoke tests.
- `.github/workflows/`: CI pipelines.

Follow the layering rule: `Routers -> Services -> CRUD -> Models -> Database`.

## Build, Test, and Development Commands
Backend (run from `backend/`):

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
python -m alembic upgrade head
python -m alembic revision --autogenerate -m "describe_change"
python -m alembic downgrade -1
```

- `uvicorn ... --reload`: starts local API server.
- `alembic upgrade head`: applies all migrations.
- `alembic revision --autogenerate`: creates migration after model changes.

Frontend (run from `frontend/`):

```bash
npm install
npm run dev
npm run build
npm run lint
npm run test:unit
npm run test:integration
npm run test:e2e
```

Docker (run from repo root):

```bash
docker compose up --build -d
docker compose ps
docker compose logs --tail=200 api
docker compose logs --tail=200 worker
docker compose run --rm api alembic upgrade head
```

## Coding Style & Naming Conventions
- Python: 4-space indentation, type hints on new/changed code.
- TypeScript/React: strict typing, modular components, hooks for shared behavior.
- Domain naming is Spanish (`negocio`, `usuario`, `cita`, `servicio`, `cliente`) and should stay consistent.
- Keep routers thin; place validation/business logic in services.
- CRUD functions should be persistence-focused and avoid HTTP concerns.
- Never commit secrets; use `backend/.env` and `frontend/.env`.
- Do not hardcode API URLs; use `VITE_API_BASE_URL`.

## Testing Guidelines
When adding tests:

- Use `pytest` under `backend/tests/`.
- Name files `test_<feature>.py` and test functions `test_<behavior>()`.
- Prioritize service and CRUD coverage for new logic.
- Run backend tests with `pytest backend/tests -q` (from repo root) or `pytest tests -q` (from `backend/`).
- Keep frontend coverage split by scope:
  - `frontend/tests/unit/`
  - `frontend/tests/integration/`
  - `frontend/tests/e2e/`

## Commit & Pull Request Guidelines
Local Git history is not available in this workspace snapshot, so use Conventional Commits:

- `feat: add citas availability filter`
- `fix: prevent cross-tenant servicio access`
- `chore: update alembic migration`

PRs should include:

- Clear summary and scope.
- Linked issue/ticket (if available).
- Migration notes (if schema changed).
- API examples or screenshots for endpoint/UI behavior changes.
