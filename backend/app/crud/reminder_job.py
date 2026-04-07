"""Pure database operations for reminder jobs."""

from datetime import datetime

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.reminder_job import ReminderJob


def get_by_id(db: Session, reminder_job_id: int) -> ReminderJob | None:
    return db.query(ReminderJob).filter(ReminderJob.id == reminder_job_id).first()


def get_by_cita_id(db: Session, cita_id: int) -> ReminderJob | None:
    return db.query(ReminderJob).filter(ReminderJob.cita_id == cita_id).first()


def get_by_id_for_update(db: Session, reminder_job_id: int) -> ReminderJob | None:
    return (
        db.query(ReminderJob)
        .filter(ReminderJob.id == reminder_job_id)
        .with_for_update()
        .first()
    )


def list_bootstrap_candidates(
    db: Session,
    now_utc: datetime,
    processing_stale_before: datetime,
    limit: int = 2000,
) -> list[ReminderJob]:
    return (
        db.query(ReminderJob)
        .filter(
            ReminderJob.sent_at.is_(None),
            or_(
                ReminderJob.status.in_(["pending", "scheduled"]),
                (ReminderJob.status == "processing")
                & (ReminderJob.updated_at <= processing_stale_before),
            ),
        )
        .order_by(ReminderJob.run_at.asc())
        .limit(limit)
        .all()
    )


def save(db: Session, job: ReminderJob) -> ReminderJob:
    db.add(job)
    db.flush()
    return job
