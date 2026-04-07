"""extend reminder status check with processing

Revision ID: a8c4d2e9b1f0
Revises: f7b2c1a94d55
Create Date: 2026-03-08 09:30:00.000000

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "a8c4d2e9b1f0"
down_revision: Union[str, Sequence[str], None] = "f7b2c1a94d55"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("ck_reminder_jobs_status", "reminder_jobs", type_="check")
    op.create_check_constraint(
        "ck_reminder_jobs_status",
        "reminder_jobs",
        "status IN ('pending', 'scheduled', 'processing', 'sent', 'cancelled', 'failed')",
    )


def downgrade() -> None:
    op.drop_constraint("ck_reminder_jobs_status", "reminder_jobs", type_="check")
    op.create_check_constraint(
        "ck_reminder_jobs_status",
        "reminder_jobs",
        "status IN ('pending', 'scheduled', 'sent', 'cancelled', 'failed')",
    )
