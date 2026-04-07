"""add horarios negocio and empleado assignment for citas

Revision ID: c1a2b3d4e5f6
Revises: 9b9e2cb6dca9
Create Date: 2026-03-07 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c1a2b3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "9b9e2cb6dca9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "horarios_negocio",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("negocio_id", sa.Integer(), nullable=False),
        sa.Column("dia_semana", sa.Integer(), nullable=False),
        sa.Column("hora_inicio", sa.Time(), nullable=False),
        sa.Column("hora_fin", sa.Time(), nullable=False),
        sa.CheckConstraint("dia_semana >= 0 AND dia_semana <= 6", name="ck_horario_dia_semana"),
        sa.ForeignKeyConstraint(["negocio_id"], ["negocios.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_horarios_negocio_id"), "horarios_negocio", ["id"], unique=False)
    op.create_index(
        op.f("ix_horarios_negocio_negocio_id"),
        "horarios_negocio",
        ["negocio_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_horarios_negocio_dia_semana"),
        "horarios_negocio",
        ["dia_semana"],
        unique=False,
    )

    op.add_column("citas", sa.Column("empleado_id", sa.Integer(), nullable=True))
    op.create_index(op.f("ix_citas_empleado_id"), "citas", ["empleado_id"], unique=False)
    op.create_foreign_key(
        "fk_citas_empleado_id_usuarios",
        "citas",
        "usuarios",
        ["empleado_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint("fk_citas_empleado_id_usuarios", "citas", type_="foreignkey")
    op.drop_index(op.f("ix_citas_empleado_id"), table_name="citas")
    op.drop_column("citas", "empleado_id")

    op.drop_index(op.f("ix_horarios_negocio_dia_semana"), table_name="horarios_negocio")
    op.drop_index(op.f("ix_horarios_negocio_negocio_id"), table_name="horarios_negocio")
    op.drop_index(op.f("ix_horarios_negocio_id"), table_name="horarios_negocio")
    op.drop_table("horarios_negocio")

