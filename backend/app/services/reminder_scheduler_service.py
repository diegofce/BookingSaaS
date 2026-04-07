"""Reminder scheduling and processing using Celery + Redis."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core.celery_app import celery_app
from app.core.config import settings
from app.crud import cliente as crud_cliente
from app.crud import reminder_job as crud_reminder_job
from app.crud import servicio as crud_servicio
from app.models.cita import Cita
from app.models.reminder_job import ReminderJob
from app.services.notification_service import NotificationService

logger = logging.getLogger(__name__)


class ReminderSchedulerService:
    @staticmethod
    def _utcnow_naive() -> datetime:
        return datetime.now(timezone.utc).replace(tzinfo=None)

    @staticmethod
    def _compute_run_at(cita: Cita) -> datetime:
        return cita.fecha_inicio - timedelta(minutes=settings.reminder_minutes_before)

    @staticmethod
    def _processing_stale_before(now_utc: datetime) -> datetime:
        return now_utc - timedelta(minutes=settings.reminder_processing_timeout_minutes)

    @staticmethod
    def _task_id_for(job: ReminderJob) -> str:
        return f"reminder-job:{job.id}:{int(job.run_at.timestamp())}"

    @staticmethod
    def _enqueue_job(db: Session, job: ReminderJob) -> None:
        if not settings.enable_background_reminders:
            return
        task_id = ReminderSchedulerService._task_id_for(job)
        eta = max(job.run_at, ReminderSchedulerService._utcnow_naive())
        celery_app.send_task(
            "app.tasks.send_reminder",
            args=[job.id],
            eta=eta,
            task_id=task_id,
            queue="reminders",
            ignore_result=True,
            retry=False,
        )
        job.celery_task_id = task_id
        job.status = "scheduled"
        job.updated_at = ReminderSchedulerService._utcnow_naive()
        crud_reminder_job.save(db, job)

    @staticmethod
    def _cancel_job(db: Session, job: ReminderJob, reason: str) -> None:
        if job.celery_task_id:
            try:
                celery_app.control.revoke(job.celery_task_id, terminate=False)
            except Exception:
                logger.exception("Failed to revoke task_id=%s", job.celery_task_id)
        job.status = "cancelled"
        job.last_error = reason
        job.celery_task_id = None
        job.updated_at = ReminderSchedulerService._utcnow_naive()
        crud_reminder_job.save(db, job)

    @staticmethod
    def sync_job_for_cita(db: Session, cita_id: int) -> None:
        cita = db.query(Cita).filter(Cita.id == cita_id).first()
        job = crud_reminder_job.get_by_cita_id(db, cita_id=cita_id)
        now_utc = ReminderSchedulerService._utcnow_naive()

        if not cita:
            if job:
                ReminderSchedulerService._cancel_job(db, job, "Cita eliminada.")
            return

        if cita.estado == "cancelada":
            if job and job.status != "sent":
                ReminderSchedulerService._cancel_job(db, job, "Cita cancelada.")
            return

        run_at = ReminderSchedulerService._compute_run_at(cita)
        if run_at <= now_utc:
            if job and job.status not in {"sent", "cancelled"}:
                ReminderSchedulerService._cancel_job(
                    db, job, "No se agenda recordatorio para citas inminentes/pasadas."
                )
            return

        if not job:
            job = ReminderJob(
                cita_id=cita.id,
                negocio_id=cita.negocio_id,
                run_at=run_at,
                status="pending",
                attempts=0,
                created_at=now_utc,
                updated_at=now_utc,
            )
            crud_reminder_job.save(db, job)
        else:
            if job.status == "sent":
                return
            run_at_changed = job.run_at != run_at
            if run_at_changed and job.celery_task_id:
                try:
                    celery_app.control.revoke(job.celery_task_id, terminate=False)
                except Exception:
                    logger.exception("Failed to revoke previous task_id=%s", job.celery_task_id)
                job.celery_task_id = None
            job.run_at = run_at
            job.status = "pending"
            job.last_error = None
            job.updated_at = now_utc
            crud_reminder_job.save(db, job)

        if job.celery_task_id and job.status == "scheduled":
            return

        try:
            ReminderSchedulerService._enqueue_job(db, job)
        except Exception:
            # Keep persisted as pending to retry on startup bootstrap.
            job.status = "pending"
            job.last_error = "No se pudo encolar en Celery; se reintentara en startup."
            job.updated_at = ReminderSchedulerService._utcnow_naive()
            crud_reminder_job.save(db, job)
            logger.exception("Failed to enqueue reminder for cita_id=%s", cita.id)

    @staticmethod
    def bootstrap_pending_jobs() -> None:
        if not settings.enable_background_reminders:
            return
        from app.db.database import SessionLocal

        db = SessionLocal()
        try:
            now_utc = ReminderSchedulerService._utcnow_naive()
            processing_stale_before = ReminderSchedulerService._processing_stale_before(
                now_utc=now_utc
            )
            candidates = crud_reminder_job.list_bootstrap_candidates(
                db,
                now_utc=now_utc,
                processing_stale_before=processing_stale_before,
            )
            for job in candidates:
                cita = db.query(Cita).filter(Cita.id == job.cita_id).first()
                if not cita or cita.estado == "cancelada":
                    ReminderSchedulerService._cancel_job(
                        db, job, "Bootstrap: cita inexistente o cancelada."
                    )
                    continue

                expected_run_at = ReminderSchedulerService._compute_run_at(cita)
                if expected_run_at <= now_utc:
                    ReminderSchedulerService._cancel_job(
                        db, job, "Bootstrap: cita inminente/pasada."
                    )
                    continue

                if job.run_at != expected_run_at:
                    job.run_at = expected_run_at
                    job.celery_task_id = None
                    job.status = "pending"
                    job.updated_at = now_utc
                    crud_reminder_job.save(db, job)

                if job.status == "processing":
                    job.status = "pending"
                    job.celery_task_id = None
                    job.updated_at = now_utc
                    crud_reminder_job.save(db, job)

                if not job.celery_task_id or job.status != "scheduled":
                    ReminderSchedulerService._enqueue_job(db, job)

            db.commit()
        except Exception:
            db.rollback()
            logger.exception("Failed to bootstrap reminder jobs.")
        finally:
            db.close()

    @staticmethod
    def process_job(reminder_job_id: int) -> None:
        if not settings.enable_background_reminders:
            return
        from app.db.database import SessionLocal

        db = SessionLocal()
        try:
            now_utc = ReminderSchedulerService._utcnow_naive()
            job = crud_reminder_job.get_by_id_for_update(
                db, reminder_job_id=reminder_job_id)
            if not job:
                db.rollback()
                return
            if job.status in {"sent", "cancelled"}:
                db.rollback()
                return

            if job.status == "processing" and job.updated_at > ReminderSchedulerService._processing_stale_before(now_utc):
                db.rollback()
                return

            job.status = "processing"
            job.updated_at = now_utc
            crud_reminder_job.save(db, job)

            cita = db.query(Cita).filter(Cita.id == job.cita_id).first()
            if not cita or cita.estado == "cancelada":
                ReminderSchedulerService._cancel_job(
                    db, job, "Proceso: cita inexistente o cancelada."
                )
                db.commit()
                return

            expected_run_at = ReminderSchedulerService._compute_run_at(cita)
            if expected_run_at != job.run_at:
                job.run_at = expected_run_at
                job.status = "pending"
                job.celery_task_id = None
                job.updated_at = now_utc
                crud_reminder_job.save(db, job)
                ReminderSchedulerService._enqueue_job(db, job)
                db.commit()
                return

            if cita.fecha_inicio <= now_utc:
                ReminderSchedulerService._cancel_job(
                    db, job, "Proceso: la cita ya inicio y no aplica recordatorio."
                )
                db.commit()
                return

            cliente = crud_cliente.get(db, cliente_id=cita.cliente_id, negocio_id=cita.negocio_id)
            servicio = crud_servicio.get(db, servicio_id=cita.servicio_id, negocio_id=cita.negocio_id)
            if not cliente or not servicio:
                job.status = "failed"
                job.attempts += 1
                job.last_error = "Referencias invalidas para enviar recordatorio."
                job.updated_at = now_utc
                crud_reminder_job.save(db, job)
                db.commit()
                return

            NotificationService.send_appointment_reminder(cita, cliente, servicio)
            job.status = "sent"
            job.sent_at = now_utc
            job.attempts += 1
            job.last_error = None
            job.updated_at = now_utc
            crud_reminder_job.save(db, job)
            db.commit()
        except Exception as exc:
            db.rollback()
            logger.exception("Error processing reminder_job_id=%s", reminder_job_id)
            raise exc
        finally:
            db.close()
