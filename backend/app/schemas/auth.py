"""Pydantic schemas for authentication workflows."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """Credentials used to obtain an access token."""

    email: EmailStr
    password: str = Field(min_length=8)
    negocio_id: int = Field(gt=0)


class Token(BaseModel):
    """Returned after a successful authentication."""

    access_token: str
    token_type: str = "bearer"


class SessionResponse(Token):
    """Session payload returned to browser clients."""

    user_id: int
    negocio_id: int


class TokenPayload(BaseModel):
    """Payload extracted from a validated JWT."""

    sub: str
    negocio_id: int
    exp: Optional[int] = None
    iat: Optional[int] = None


class RefreshToken(BaseModel):
    """Placeholder for future refresh token flows."""

    refresh_token: str
    issued_at: datetime
