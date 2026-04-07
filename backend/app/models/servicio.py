from __future__ import annotations

"""Modelo de servicio ofrecido por un negocio."""
from datetime import datetime, timezone
from decimal import Decimal
from typing import TYPE_CHECKING, List

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.cita import Cita
    from app.models.negocio import Negocio


def _utcnow_naive() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Servicio(Base):
    """Servicios que un negocio puede agendar para sus clientes."""

    __tablename__ = "servicios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    negocio_id: Mapped[int] = mapped_column(
        ForeignKey("negocios.id"), nullable=False, index=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    duracion_minutos: Mapped[int] = mapped_column(Integer, nullable=False)
    precio: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=_utcnow_naive)

    negocio: Mapped[Negocio] = relationship(
        "Negocio", back_populates="servicios")
    citas: Mapped[List[Cita]] = relationship(
        "Cita", back_populates="servicio", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Servicio id={self.id} nombre={self.nombre}>"
