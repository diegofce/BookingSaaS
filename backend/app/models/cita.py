from __future__ import annotations

"""Modelo de citas agendadas entre clientes y servicios."""
from datetime import datetime, timezone
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Index, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.cliente import Cliente
    from app.models.negocio import Negocio
    from app.models.servicio import Servicio
    from app.models.usuario import Usuario


_ESTADOS_CITA = ("pendiente", "confirmada", "cancelada")


def _utcnow_naive() -> datetime:
    """Return a UTC naive datetime to keep compatibility with DateTime columns."""

    return datetime.now(timezone.utc).replace(tzinfo=None)


class Cita(Base):
    """Cita agendada para un cliente en un negocio."""

    __tablename__ = "citas"
    __table_args__ = (
        Index("ix_citas_negocio_fecha_inicio", "negocio_id", "fecha_inicio"),
        Index("ix_citas_negocio_fecha_fin", "negocio_id", "fecha_fin"),
        Index("ix_citas_empleado_fecha_inicio", "empleado_id", "fecha_inicio"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    negocio_id: Mapped[int] = mapped_column(
        ForeignKey("negocios.id"), nullable=False, index=True)
    cliente_id: Mapped[int] = mapped_column(
        ForeignKey("clientes.id"), nullable=False, index=True)
    servicio_id: Mapped[int] = mapped_column(
        ForeignKey("servicios.id"), nullable=False, index=True)
    empleado_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuarios.id"), nullable=True, index=True)
    fecha_inicio: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    fecha_fin: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    estado: Mapped[str] = mapped_column(
        Enum(*_ESTADOS_CITA, name="estado_cita"), nullable=False, default="pendiente")
    monto_pagado: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False, default=Decimal("0"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=_utcnow_naive)

    negocio: Mapped[Negocio] = relationship(
        "Negocio", back_populates="citas")
    cliente: Mapped[Cliente] = relationship(
        "Cliente", back_populates="citas")
    servicio: Mapped[Servicio] = relationship(
        "Servicio", back_populates="citas")
    empleado: Mapped[Usuario | None] = relationship(
        "Usuario", back_populates="citas_asignadas", foreign_keys=[empleado_id])

    def __repr__(self) -> str:
        return f"<Cita id={self.id} estado={self.estado}>"
