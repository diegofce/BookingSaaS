"""Database session and engine configuration for SQLAlchemy."""
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings


def _make_sync_url(url_str: str) -> str:
    """Force a synchronous driver; switch asyncpg to psycopg2 if present."""

    url = make_url(url_str)
    if url.drivername == "postgresql+asyncpg":
        url = url.set(drivername="postgresql+psycopg2")
    return url.render_as_string(hide_password=False)


# Engine configured for PostgreSQL; pool_pre_ping keeps connections healthy behind load balancers.
engine = create_engine(_make_sync_url(
    settings.database_url), pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator:
    """Yield a database session for FastAPI dependencies and ensure cleanup."""

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
