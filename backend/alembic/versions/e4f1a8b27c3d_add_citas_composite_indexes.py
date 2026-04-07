"""add composite indexes for citas performance

Revision ID: e4f1a8b27c3d
Revises: c1a2b3d4e5f6
Create Date: 2026-03-07 15:20:00.000000

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "e4f1a8b27c3d"
down_revision: Union[str, Sequence[str], None] = "c1a2b3d4e5f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        "ix_citas_negocio_fecha_inicio",
        "citas",
        ["negocio_id", "fecha_inicio"],
        unique=False,
    )
    op.create_index(
        "ix_citas_negocio_fecha_fin",
        "citas",
        ["negocio_id", "fecha_fin"],
        unique=False,
    )
    op.create_index(
        "ix_citas_empleado_fecha_inicio",
        "citas",
        ["empleado_id", "fecha_inicio"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_citas_empleado_fecha_inicio", table_name="citas")
    op.drop_index("ix_citas_negocio_fecha_fin", table_name="citas")
    op.drop_index("ix_citas_negocio_fecha_inicio", table_name="citas")

