"""add reminder jobs table for celery scheduling

Revision ID: f7b2c1a94d55
Revises: e4f1a8b27c3d
Create Date: 2026-03-07 16:40:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "f7b2c1a94d55"
down_revision: Union[str, Sequence[str], None] = "e4f1a8b27c3d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "reminder_jobs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("cita_id", sa.Integer(), nullable=False),
        sa.Column("negocio_id", sa.Integer(), nullable=False),
        sa.Column("run_at", sa.DateTime(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("celery_task_id", sa.String(length=255), nullable=True),
        sa.Column("attempts", sa.Integer(), nullable=False),
        sa.Column("sent_at", sa.DateTime(), nullable=True),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint(
            "status IN ('pending', 'scheduled', 'sent', 'cancelled', 'failed')",
            name="ck_reminder_jobs_status",
        ),
        sa.ForeignKeyConstraint(["cita_id"], ["citas.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("cita_id", name="uq_reminder_job_cita_id"),
    )
    op.create_index(op.f("ix_reminder_jobs_id"), "reminder_jobs", ["id"], unique=False)
    op.create_index(
        "ix_reminder_jobs_negocio_id",
        "reminder_jobs",
        ["negocio_id"],
        unique=False,
    )
    op.create_index(
        "ix_reminder_jobs_status_run_at",
        "reminder_jobs",
        ["status", "run_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_reminder_jobs_status_run_at", table_name="reminder_jobs")
    op.drop_index("ix_reminder_jobs_negocio_id", table_name="reminder_jobs")
    op.drop_index(op.f("ix_reminder_jobs_id"), table_name="reminder_jobs")
    op.drop_table("reminder_jobs")
