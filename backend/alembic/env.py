"""Alembic environment configuration for Booking SaaS backend."""
from __future__ import annotations
from sqlalchemy.engine.url import make_url

from logging.config import fileConfig
from pathlib import Path
import sys

from alembic import context
from sqlalchemy import engine_from_config, pool

# Ensure application modules are discoverable when Alembic runs.
BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))


from app.core.config import settings  # noqa: E402
from app.db.database import Base  # noqa: E402
from app import models  # noqa: E402,F401  # Load models for metadata discovery

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Use runtime settings to configure the database URL; avoids hardcoding credentials.


def _sync_url(url_str: str) -> str:
    url = make_url(url_str)
    if url.drivername == "postgresql+asyncpg":
        url = url.set(drivername="postgresql+psycopg2")
    return url.render_as_string(hide_password=False)


config.set_main_option("sqlalchemy.url", _sync_url(settings.database_url))

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode using URL configuration."""

    context.configure(
        url=settings.database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode with an engine connection."""

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
