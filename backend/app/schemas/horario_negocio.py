"""Pydantic schemas for HorarioNegocio."""

from datetime import time
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class HorarioNegocioBase(BaseModel):
    dia_semana: int = Field(ge=0, le=6, description="0=Lunes, 6=Domingo")
    hora_inicio: time
    hora_fin: time

    @model_validator(mode="after")
    def validate_range(self) -> "HorarioNegocioBase":
        if self.hora_inicio >= self.hora_fin:
            raise ValueError("hora_inicio debe ser menor que hora_fin.")
        return self


class HorarioNegocioCreate(HorarioNegocioBase):
    pass


class HorarioNegocioUpdate(BaseModel):
    dia_semana: Optional[int] = Field(default=None, ge=0, le=6)
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None

    @model_validator(mode="after")
    def validate_range(self) -> "HorarioNegocioUpdate":
        if self.hora_inicio is not None and self.hora_fin is not None:
            if self.hora_inicio >= self.hora_fin:
                raise ValueError("hora_inicio debe ser menor que hora_fin.")
        return self


class HorarioNegocioResponse(HorarioNegocioBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    negocio_id: int

