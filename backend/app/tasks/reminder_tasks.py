"""Celery tasks for reminder processing."""

from app.core.celery_app import celery_app
from app.services.reminder_scheduler_service import ReminderSchedulerService


@celery_app.task(
    bind=True,
    name="app.tasks.send_reminder",
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_jitter=True,
    retry_kwargs={"max_retries": 3},
)
def send_reminder_task(self, reminder_job_id: int) -> None:
    ReminderSchedulerService.process_job(reminder_job_id=reminder_job_id)

