from __future__ import annotations

"""Modelo de usuario para la plataforma Booking SaaS."""
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.cita import Cita
    from app.models.negocio import Negocio


def _utcnow_naive() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Usuario(Base):
    """Usuarios que pertenecen a un negocio; pueden ser administradores o clientes."""

    __tablename__ = "usuarios"
    __table_args__ = (
        UniqueConstraint("negocio_id", "email",
                         name="uq_usuario_negocio_email"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    negocio_id: Mapped[int] = mapped_column(
        ForeignKey("negocios.id"), nullable=False, index=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    rol: Mapped[str] = mapped_column(
        String(20), nullable=False)  # admin | empleado | cliente
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=_utcnow_naive)

    negocio: Mapped[Negocio] = relationship(
        "Negocio", back_populates="usuarios")
    citas_asignadas: Mapped[List[Cita]] = relationship(
        "Cita", back_populates="empleado", foreign_keys="Cita.empleado_id")

    def __repr__(self) -> str:
        return f"<Usuario id={self.id} email={self.email}>"
