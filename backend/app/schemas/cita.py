"""Pydantic schemas for Cita entity."""

from datetime import datetime
from decimal import Decimal
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

EstadoCita = Literal["pendiente", "confirmada", "cancelada"]


class CitaCreate(BaseModel):
    cliente_id: int
    servicio_id: int
    empleado_id: Optional[int] = None
    # fecha_fin is computed automatically from servicio.duracion_minutos
    fecha_inicio: datetime
    monto_pagado: Decimal = Field(default=Decimal("0"), ge=0, decimal_places=2)


class CitaUpdate(BaseModel):
    cliente_id: Optional[int] = None
    servicio_id: Optional[int] = None
    empleado_id: Optional[int] = None
    fecha_inicio: Optional[datetime] = None
    estado: Optional[EstadoCita] = None
    monto_pagado: Optional[Decimal] = Field(default=None, ge=0, decimal_places=2)


class CitaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    negocio_id: int
    cliente_id: int
    servicio_id: int
    empleado_id: Optional[int]
    fecha_inicio: datetime
    fecha_fin: datetime
    estado: EstadoCita
    monto_pagado: Decimal
    created_at: datetime
