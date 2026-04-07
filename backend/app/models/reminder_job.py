from __future__ import annotations

"""Persistent reminders queue metadata for Celery jobs."""

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.cita import Cita


def _utcnow_naive() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class ReminderJob(Base):
    """Tracks reminder scheduling state and avoids duplicate deliveries."""

    __tablename__ = "reminder_jobs"
    __table_args__ = (
        UniqueConstraint("cita_id", name="uq_reminder_job_cita_id"),
        CheckConstraint(
            "status IN ('pending', 'scheduled', 'processing', 'sent', 'cancelled', 'failed')",
            name="ck_reminder_jobs_status",
        ),
        Index("ix_reminder_jobs_status_run_at", "status", "run_at"),
        Index("ix_reminder_jobs_negocio_id", "negocio_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cita_id: Mapped[int] = mapped_column(ForeignKey("citas.id"), nullable=False)
    negocio_id: Mapped[int] = mapped_column(Integer, nullable=False)
    run_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    celery_task_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=_utcnow_naive)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=_utcnow_naive)

    cita: Mapped[Cita] = relationship("Cita")
