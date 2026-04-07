"""Celery application configuration for background jobs."""

from celery import Celery

from app.core.config import settings


broker_url = settings.celery_broker_url or settings.redis_url
result_backend = settings.celery_result_backend

celery_app = Celery(
    "booking_saas",
    broker=broker_url,
    backend=result_backend,
    include=["app.tasks.reminder_tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_ignore_result=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_default_queue="reminders",
    broker_connection_retry_on_startup=True,
    broker_connection_max_retries=50,
    broker_transport_options={
        "socket_connect_timeout": 5,
        "socket_timeout": 5,
    },
)

# Keep autodiscovery for future task modules, but ensure current tasks are always loaded via `include`.
celery_app.autodiscover_tasks(["app"], related_name="tasks")
