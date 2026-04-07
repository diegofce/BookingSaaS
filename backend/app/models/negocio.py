from __future__ import annotations

"""Modelo de negocio (tenant) para la plataforma Booking SaaS."""
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.cita import Cita
    from app.models.cliente import Cliente
    from app.models.horario_negocio import HorarioNegocio
    from app.models.servicio import Servicio
    from app.models.usuario import Usuario


def _utcnow_naive() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Negocio(Base):
    """Entidad que representa un negocio/tenant dentro de la plataforma."""

    __tablename__ = "negocios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    dominio: Mapped[str] = mapped_column(
        String(120), nullable=False, unique=True)
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=_utcnow_naive)

    usuarios: Mapped[List[Usuario]] = relationship(
        "Usuario",
        back_populates="negocio",
        cascade="all, delete-orphan",
    )
    servicios: Mapped[List[Servicio]] = relationship(
        "Servicio",
        back_populates="negocio",
        cascade="all, delete-orphan",
    )
    clientes: Mapped[List[Cliente]] = relationship(
        "Cliente",
        back_populates="negocio",
        cascade="all, delete-orphan",
    )
    citas: Mapped[List[Cita]] = relationship(
        "Cita",
        back_populates="negocio",
        cascade="all, delete-orphan",
    )
    horarios: Mapped[List[HorarioNegocio]] = relationship(
        "HorarioNegocio",
        back_populates="negocio",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Negocio id={self.id} nombre={self.nombre}>"
