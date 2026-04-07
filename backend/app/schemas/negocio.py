"""Pydantic schemas for Negocio entity and registration flow."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class NegocioBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=120)
    dominio: str = Field(min_length=1, max_length=120)
    activo: bool = True


class NegocioCreate(NegocioBase):
    pass


class NegocioResponse(NegocioBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class NegocioRegister(BaseModel):
    negocio_nombre: str = Field(min_length=1, max_length=120)
    dominio: str = Field(min_length=1, max_length=120)
    admin_nombre: str = Field(min_length=1, max_length=120)
    admin_email: EmailStr
    admin_password: str = Field(min_length=8)


class NegocioRegisterResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    negocio: NegocioResponse
    usuario: "UsuarioResponse"


# Avoid circular import issues
from app.schemas.usuario import UsuarioResponse  # noqa: E402  # isort:skip

NegocioRegisterResponse.model_rebuild()
