"""Pydantic schemas for Servicio entity."""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ServicioBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=120)
    descripcion: Optional[str] = None
    duracion_minutos: int = Field(gt=0)
    precio: Decimal = Field(ge=0, decimal_places=2)
    activo: bool = True


class ServicioCreate(ServicioBase):
    pass


class ServicioUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=120)
    descripcion: Optional[str] = None
    duracion_minutos: Optional[int] = Field(default=None, gt=0)
    precio: Optional[Decimal] = Field(default=None, ge=0, decimal_places=2)
    activo: Optional[bool] = None


class ServicioResponse(ServicioBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    negocio_id: int
    created_at: datetime
