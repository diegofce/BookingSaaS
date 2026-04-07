from __future__ import annotations

"""Modelo de cliente asociado a un negocio."""
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.cita import Cita
    from app.models.negocio import Negocio


def _utcnow_naive() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Cliente(Base):
    """Clientes a quienes se les agendan servicios."""

    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    negocio_id: Mapped[int] = mapped_column(
        ForeignKey("negocios.id"), nullable=False, index=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    telefono: Mapped[str | None] = mapped_column(String(30), nullable=True)
    direccion: Mapped[str | None] = mapped_column(String(255), nullable=True)
    barrio: Mapped[str | None] = mapped_column(String(120), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=_utcnow_naive)

    negocio: Mapped[Negocio] = relationship(
        "Negocio", back_populates="clientes")
    citas: Mapped[List[Cita]] = relationship(
        "Cita", back_populates="cliente", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Cliente id={self.id} nombre={self.nombre}>"
