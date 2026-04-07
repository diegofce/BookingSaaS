#!/usr/bin/env sh
set -eu

echo "Starting Celery worker..."
exec celery -A app.core.celery_app:celery_app worker -Q reminders -l info --without-gossip --without-mingle
