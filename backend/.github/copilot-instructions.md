# Copilot Instructions – Booking SaaS Backend

## Commands

```bash
# Run dev server
uvicorn app.main:app --reload

# Run database migrations
alembic upgrade head

# Generate a new migration after model changes
alembic revision --autogenerate -m "describe_change"

# Downgrade one step
alembic downgrade -1
```

Install dependencies:
```bash
pip install -r requirements.txt
```

> There is no test suite yet.

## Architecture

FastAPI backend using a strict layered pattern:

```
Routers → Services → CRUD → Models → Database
```

- **`app/routers/`** — HTTP endpoints; only handle request/response validation and call service functions
- **`app/services/`** — All business logic lives here (validations, overlap checks, slot generation)
- **`app/crud/`** — Pure SQLAlchemy DB operations; no HTTP exceptions, return `None` on not-found
- **`app/models/`** — SQLAlchemy ORM models; imported in `main.py` so Alembic can detect them
- **`app/schemas/`** — Pydantic v2 models for request/response serialization (separate from ORM models)
- **`app/dependencies/`** — FastAPI `Depends()` providers: `auth.py` (token → Usuario), `roles.py` (RBAC)
- **`app/core/`** — Config (`pydantic-settings`) and security utilities (JWT, password hashing)
- **`app/db/database.py`** — SQLAlchemy engine, `SessionLocal`, `Base`, and `get_db()` generator

## Multi-tenancy

Every entity (`Usuario`, `Cliente`, `Servicio`, `Cita`) is scoped to a `Negocio` via a `negocio_id` foreign key. Tenant isolation is enforced at two layers:

1. **JWT token** — includes a `negocio_id` claim embedded at login time
2. **`get_current_user` dependency** — validates both `user_id` and `negocio_id` from the token, ensuring the user belongs to the right tenant

All service-layer queries must include `negocio_id` as a filter. Never query cross-tenant.

## Role-Based Access Control

`app/dependencies/roles.py` provides two composable dependencies:

| Dependency | Allowed roles | Typical use |
|---|---|---|
| `require_staff` | `admin`, `empleado` | Read operations, create/update citas & clientes |
| `require_admin` | `admin` only | Create/update/delete servicios, delete clientes/citas |

Usage in routers: replace `Depends(get_current_user)` with `Depends(require_staff)` or `Depends(require_admin)`. Both return the authenticated `Usuario` object.

## Disponibilidad (Calendly-style)

`GET /citas/disponibilidad?servicio_id=1&fecha=2024-03-15&hora_inicio=09:00&hora_fin=18:00`

- Returns a list of `SlotResponse` objects: `{hora_inicio, hora_fin, disponible}`
- Step between slots = `servicio.duracion_minutos`
- A slot is `disponible: false` if `crud.cita.has_overlap()` finds a non-cancelled appointment
- The endpoint **must stay before** `GET /citas/{cita_id}` in the router to avoid FastAPI treating "disponibilidad" as an integer path param

Overlap query logic (in `app/crud/cita.py::has_overlap`):
```sql
WHERE negocio_id = :negocio_id
  AND estado != 'cancelada'
  AND fecha_inicio < :nueva_fecha_fin
  AND fecha_fin    > :nueva_fecha_inicio
```

- `POST /negocios/register` — Public endpoint; creates a new `Negocio` + admin `Usuario` atomically and returns a JWT
- `POST /auth/login` — Takes `{email, password, negocio_id}`; returns a JWT
- All other routes use `Depends(get_current_user)` which extracts both `user_id` and `negocio_id` from the Bearer token

Token creation always passes `negocio_id` as an extra claim:
```python
security.create_access_token(subject=user.id, extra_claims={"negocio_id": user.negocio_id})
```

## Key Conventions

- **Spanish domain names** — models, routes, and variables use Spanish: `negocio`, `usuario`, `cita`, `servicio`, `cliente`
- **Soft activation** — entities have an `activo: bool` field; inactive users are rejected at auth time with `403`
- **User uniqueness** — email is unique per tenant via a composite constraint `(negocio_id, email)`, not globally unique
- **Appointment state machine** — `Cita.estado` is a PostgreSQL `Enum("pendiente", "confirmada", "cancelada", name="estado_cita")`
- **ORM style** — use SQLAlchemy 2.0 `Mapped[T]` / `mapped_column()` annotation style for all new models
- **Schemas vs Models** — always return Pydantic schema instances from routers, never raw ORM objects; use `response_model=` on all routes
- **204 on delete** — `DELETE` endpoints return `status_code=204` with `None` return type
- **DB session** — always inject via `db: Session = Depends(get_db)`; never create sessions manually
- **`created_at`** — all models include a `created_at: Mapped[datetime]` set at the service layer, not via `server_default`

## Environment & Database

- PostgreSQL; default dev URL: `postgresql://postgres:admin@localhost:5433/booking_saas`
- The real URL is loaded from `.env` via `pydantic-settings` in `app/core/config.py`
- Alembic reads the URL from `app/core/config.settings.database_url` in `alembic/env.py` (not hardcoded in `alembic.ini`)
