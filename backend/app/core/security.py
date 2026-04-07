"""
Security utilities for password hashing and JWT token handling.
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings


# Password hashing configuration
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    """Hash a plain text password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a plain password against its hashed version."""
    return pwd_context.verify(password, password_hash)


def create_access_token(
    subject: str | int,
    expires_delta: Optional[timedelta] = None,
    extra_claims: Optional[dict[str, Any]] = None,
) -> str:
    """
    Create a signed JWT access token.

    subject: usually user ID
    extra_claims: used to include negocio_id
    """

    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )

    to_encode: dict[str, Any] = {
        "sub": str(subject),
        "exp": expire,
    }

    if extra_claims:
        to_encode.update(extra_claims)

    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

    return encoded_jwt


def create_refresh_token(
    subject: str | int,
    negocio_id: int,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create a signed refresh JWT token."""

    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(days=settings.refresh_token_expire_days)
    )
    to_encode: dict[str, Any] = {
        "sub": str(subject),
        "negocio_id": negocio_id,
        "type": "refresh",
        "exp": expire,
    }
    return jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> dict[str, Any]:
    """Decode and validate a JWT token."""
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        return payload
    except JWTError as exc:
        raise ValueError("Invalid token") from exc


def decode_refresh_token(token: str) -> dict[str, Any]:
    """Decode and validate a refresh JWT token."""
    payload = decode_access_token(token)
    if payload.get("type") != "refresh":
        raise ValueError("Invalid refresh token")
    return payload
