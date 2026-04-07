"""Schemas for public booking (Calendly-style) endpoints."""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.schemas.cita import CitaResponse


class AgendaServicioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    descripcion: Optional[str]
    duracion_minutos: int
    precio: Decimal
    activo: bool


class AgendaPublicaReservaCreate(BaseModel):
    servicio_id: int
    fecha_inicio: datetime
    cliente_nombre: str = Field(min_length=1, max_length=120)
    cliente_email: Optional[EmailStr] = None
    cliente_telefono: Optional[str] = Field(default=None, max_length=30)
    cliente_direccion: Optional[str] = Field(default=None, max_length=255)
    cliente_barrio: Optional[str] = Field(default=None, max_length=120)


class AgendaPublicaReservaResponse(BaseModel):
    cita: CitaResponse
