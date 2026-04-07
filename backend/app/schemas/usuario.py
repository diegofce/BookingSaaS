"""Pydantic schemas for Usuario entity."""

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

RolUsuario = Literal["admin", "empleado", "cliente"]


class UsuarioBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=120)
    email: EmailStr
    rol: RolUsuario
    activo: bool = True


class UsuarioCreate(UsuarioBase):
    password: str = Field(min_length=8)


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=120)
    email: Optional[EmailStr] = None
    rol: Optional[RolUsuario] = None
    password: Optional[str] = Field(default=None, min_length=8)
    activo: Optional[bool] = None


class UsuarioResponse(UsuarioBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    negocio_id: int
    created_at: datetime
