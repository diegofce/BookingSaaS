# Booking SaaS

Plataforma SaaS para gestion de reservas y agenda de negocios. El proyecto permite registrar un negocio, autenticar usuarios del tenant, administrar clientes, servicios, empleados, horarios y citas, y ofrecer una agenda publica para que clientes finales puedan reservar en linea. Ademas, incorpora recordatorios programados en segundo plano con Celery y Redis.

## Caracteristicas principales

- Autenticacion con `access token` y `refresh token` por cookie.
- Arquitectura multi-tenant basada en `negocio` y `dominio`.
- CRUD de clientes, servicios, empleados, horarios y citas.
- Agenda publica por negocio para consultar disponibilidad y reservar.
- Recordatorios asincronos para citas usando Celery + Redis.
- Backend con migraciones de base de datos mediante Alembic.
- Frontend SPA en React con rutas privadas y flujo publico de reservas.

## Roles y permisos

El sistema define tres roles de usuario:

- `admin`: acceso total al negocio. Puede crear, editar y eliminar usuarios, servicios, horarios, clientes y citas, ademas de administrar la configuracion operativa del tenant.
- `empleado`: acceso operativo al backoffice. Puede consultar y gestionar citas y acceder a informacion necesaria para la operacion diaria, con permisos mas limitados que el administrador.
- `cliente`: rol de usuario final sin acceso al backoffice administrativo.

Notas importantes sobre el modelo funcional:

- El primer usuario `admin` no viene precargado por defecto; se crea cuando se registra un negocio mediante `POST /negocios/register`.
- La reserva publica no depende de que exista un usuario autenticado con rol `cliente`. En ese flujo, el sistema crea registros en la entidad `Cliente` asociada al negocio para agendar citas.
- En otras palabras, `usuarios` representa cuentas autenticables del sistema y `clientes` representa personas atendidas por el negocio.

## Stack tecnologico

### Backend

- FastAPI
- SQLAlchemy 2.0
- Alembic
- PostgreSQL
- Celery
- Redis
- Pydantic Settings
- SlowAPI

### Frontend

- React 18
- TypeScript
- Vite
- Axios
- Tailwind CSS
- FullCalendar
- Vitest
- Playwright

### Infraestructura y desarrollo

- Docker Compose
- Python 3.13
- Node.js 20+ recomendado

## Estructura del proyecto

```text
booking_saas/
|-- backend/
|   |-- app/
|   |   |-- routers/
|   |   |-- services/
|   |   |-- crud/
|   |   |-- models/
|   |   |-- schemas/
|   |   |-- core/
|   |   `-- db/
|   |-- alembic/
|   |-- scripts/
|   |-- requirements.txt
|   `-- .env.example
|-- frontend/
|   |-- src/
|   |-- tests/
|   `-- package.json
|-- docker-compose.yml
|-- .gitignore
`-- README.md
```

## Que hace el sistema

El backend expone endpoints para autenticacion, registro de negocios, usuarios, clientes, servicios, horarios, citas y agenda publica. El frontend incluye un panel privado para la operacion del negocio y una experiencia publica para que un cliente consulte servicios, vea horarios disponibles y cree su reserva.

## Capturas de pantalla

Las capturas del proyecto se organizan en `docs/screenshots/`.

### Login



### Dashboard



### Agenda



Rutas y modulos relevantes:

- `backend/app/routers/auth.py`: login, refresh, logout y usuario autenticado.
- `backend/app/routers/negocios.py`: registro de negocio.
- `backend/app/routers/clientes.py`: gestion de clientes.
- `backend/app/routers/servicios.py`: gestion de servicios.
- `backend/app/routers/usuarios.py`: gestion de empleados/usuarios.
- `backend/app/routers/citas.py`: agenda interna y recordatorios.
- `backend/app/routers/agenda_publica.py`: agenda publica por dominio.
- `frontend/src/router/AppRouter.tsx`: rutas privadas y publicas del frontend.

## Requisitos previos

### Opcion 1: Docker

- Docker
- Docker Compose

### Opcion 2: Ejecucion local

- Python 3.13
- Node.js 20 o superior
- PostgreSQL
- Redis

## Variables de entorno

### Backend

Existe un archivo de referencia en `backend/.env.example`. Copia ese archivo a `backend/.env` y ajusta los valores segun tu entorno.

Variables principales:

- `DATABASE_URL`
- `JWT_SECRET_KEY`
- `JWT_ALGORITHM`
- `REDIS_URL`
- `CELERY_BROKER_URL`
- `CELERY_RESULT_BACKEND`
- `ENABLE_BACKGROUND_REMINDERS`
- `BOOTSTRAP_REMINDERS_ON_STARTUP`
- `REMINDER_MINUTES_BEFORE`
- `REMINDER_PROCESSING_TIMEOUT_MINUTES`
- `CORS_ORIGINS`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `REFRESH_TOKEN_EXPIRE_DAYS`
- `REFRESH_COOKIE_NAME`
- `REFRESH_COOKIE_SECURE`
- `REFRESH_COOKIE_SAMESITE`

### Frontend

Crea `frontend/.env` con:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## Como correr el proyecto

### Opcion recomendada: Docker Compose

Desde la raiz del repositorio:

```bash
docker compose up --build -d
```

Servicios levantados:

- `db`: PostgreSQL
- `redis`: Redis
- `api`: FastAPI en `http://127.0.0.1:8000`
- `worker`: Celery para recordatorios

Verificar estado:

```bash
docker compose ps
docker compose logs --tail=200 api
docker compose logs --tail=200 worker
```

La API expone un health check en:

```text
http://127.0.0.1:8000/health
```

### Opcion local: backend

Desde `backend/`:

```bash
pip install -r requirements.txt
python -m alembic upgrade head
uvicorn app.main:app --reload
```

Si vas a usar recordatorios en segundo plano, ejecuta tambien:

```bash
celery -A app.core.celery_app:celery_app worker -Q reminders -l info --without-gossip --without-mingle
```

### Opcion local: frontend

Desde `frontend/`:

```bash
npm install
npm run dev
```

Frontend disponible por defecto en:

```text
http://127.0.0.1:5173
```

## Migraciones

Desde `backend/`:

```bash
python -m alembic upgrade head
python -m alembic revision --autogenerate -m "describe_change"
python -m alembic downgrade -1
```

## Pruebas

### Backend

Desde la raiz del proyecto:

```bash
pytest backend/tests -q
```

O desde `backend/`:

```bash
pytest tests -q
```

### Frontend

Desde `frontend/`:

```bash
npm run lint
npm run test:unit
npm run test:integration
npm run test:e2e
```

## Endpoints y rutas utiles

- API docs: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/health`
- Frontend local: `http://127.0.0.1:5173`
- Agenda publica: `http://127.0.0.1:5173/agenda/<dominio>`

## Que subir a GitHub

Sube el codigo fuente, configuraciones, migraciones y documentacion. En este proyecto, lo normal es subir:

- `backend/app/`
- `backend/alembic/`
- `backend/requirements.txt`
- `backend/.env.example`
- `frontend/src/`
- `frontend/tests/`
- `frontend/package.json`
- `frontend/package-lock.json`
- `docker-compose.yml`
- `.gitignore`
- `README.md`
- `.github/workflows/` si usas CI

No deberias subir:

- `backend/.env`
- `frontend/.env`
- `backend/venv/`
- `frontend/node_modules/`
- `frontend/dist/`
- caches temporales de pytest
- logs, coberturas y archivos temporales del editor

## Recomendaciones antes de publicar

- Reemplaza secretos locales por valores seguros en produccion.
- Verifica que ningun `.env` real quede trackeado antes del primer commit.
- Si algun archivo sensible ya fue agregado por error, eliminalo del indice antes de subirlo.
- Manten `backend/.env.example` como plantilla publica sin secretos reales.

## Licencia

Define aqui la licencia que vayas a usar para el repositorio, por ejemplo `MIT`.
