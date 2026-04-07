"""FastAPI entrypoint for the Booking SaaS backend."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler

from app.core.config import settings
from app.core.rate_limit import limiter
from app.db.database import Base, engine
from app.events import cita_events  # noqa: F401  # Register SQLAlchemy listeners.
from app.routers import (
    agenda_publica,
    auth,
    citas,
    clientes,
    horarios_negocio,
    negocios,
    servicios,
    usuarios,
)
# Import models so Alembic has metadata available without creating tables explicitly.
from app.models import cita, cliente, horario_negocio, negocio, reminder_job, servicio, usuario  # noqa: F401
from app.services.reminder_scheduler_service import ReminderSchedulerService


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    if settings.enable_background_reminders and settings.bootstrap_reminders_on_startup:
        ReminderSchedulerService.bootstrap_pending_jobs()
    yield


app = FastAPI(title="Booking SaaS API", version="0.1.0", lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    """Lightweight liveness probe for infrastructure monitoring."""

    return {"status": "ok", "database": "configured" if settings.database_url else "missing"}


app.include_router(auth.router)
app.include_router(negocios.router)
app.include_router(usuarios.router)
app.include_router(clientes.router)
app.include_router(servicios.router)
app.include_router(citas.router)
app.include_router(horarios_negocio.router)
app.include_router(agenda_publica.router)


__all__ = ["app", "Base", "engine"]
