"""add email column to clientes

Revision ID: b3f4c7a1d2e9
Revises: a8c4d2e9b1f0
Create Date: 2026-03-08 10:40:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "b3f4c7a1d2e9"
down_revision: Union[str, Sequence[str], None] = "a8c4d2e9b1f0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("clientes", sa.Column("email", sa.String(length=255), nullable=True))
    op.create_index(op.f("ix_clientes_email"), "clientes", ["email"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_clientes_email"), table_name="clientes")
    op.drop_column("clientes", "email")
