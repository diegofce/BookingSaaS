"""SQLAlchemy listeners to keep reminder jobs in sync with cita changes.

The reminder sync runs after transaction commit to avoid scheduling jobs for
changes that are later rolled back.
"""

from __future__ import annotations

import logging

from sqlalchemy import event
from sqlalchemy.orm import Session

from app.models.cita import Cita
from app.db.database import SessionLocal
from app.services.reminder_scheduler_service import ReminderSchedulerService

logger = logging.getLogger(__name__)


def _sync_reminder(cita_id: int) -> None:
    db = SessionLocal()
    try:
        ReminderSchedulerService.sync_job_for_cita(db, cita_id=cita_id)
        db.commit()
    except Exception:
        db.rollback()
        logger.exception("Failed to sync reminder for cita_id=%s", cita_id)
    finally:
        db.close()


@event.listens_for(Session, "after_flush")
def _collect_changed_citas(session: Session, flush_context) -> None:
    cita_ids = session.info.setdefault("changed_cita_ids", set())

    for obj in session.new:
        if isinstance(obj, Cita) and obj.id is not None:
            cita_ids.add(obj.id)

    for obj in session.dirty:
        if isinstance(obj, Cita) and obj.id is not None and session.is_modified(obj):
            cita_ids.add(obj.id)

    for obj in session.deleted:
        if isinstance(obj, Cita) and obj.id is not None:
            cita_ids.add(obj.id)


@event.listens_for(Session, "after_commit")
def _after_commit_sync_reminders(session: Session) -> None:
    cita_ids = session.info.pop("changed_cita_ids", set())
    for cita_id in cita_ids:
        _sync_reminder(cita_id=cita_id)


@event.listens_for(Session, "after_rollback")
def _after_rollback_clear(session: Session) -> None:
    session.info.pop("changed_cita_ids", None)
