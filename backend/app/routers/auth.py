"""Authentication routes for the Booking SaaS API."""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session

from app.core.rate_limit import limiter
from app.core import security
from app.core.config import settings
from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.usuario import Usuario
from app.schemas.auth import LoginRequest, SessionResponse
from app.schemas.usuario import UsuarioResponse
from app.services.usuario_service import UsuarioService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=SessionResponse)
@limiter.limit("10/minute")
def login(
    request: Request,
    response: Response,
    payload: LoginRequest,
    db: Session = Depends(get_db),
) -> SessionResponse:
    usuario = UsuarioService.authenticate(
        db=db,
        email=payload.email,
        password=payload.password,
        negocio_id=payload.negocio_id,
    )
    access_token = security.create_access_token(
        subject=usuario.id,
        extra_claims={"negocio_id": usuario.negocio_id},
    )
    refresh_token = security.create_refresh_token(
        subject=usuario.id,
        negocio_id=usuario.negocio_id,
    )
    response.set_cookie(
        key=settings.refresh_cookie_name,
        value=refresh_token,
        httponly=True,
        secure=settings.refresh_cookie_secure,
        samesite=settings.refresh_cookie_samesite,
        max_age=settings.refresh_token_expire_days * 24 * 3600,
        path="/auth",
    )
    return SessionResponse(
        access_token=access_token,
        user_id=usuario.id,
        negocio_id=usuario.negocio_id,
    )


@router.post("/refresh", response_model=SessionResponse)
@limiter.limit("20/minute")
def refresh_session(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
) -> SessionResponse:
    refresh_token = request.cookies.get(settings.refresh_cookie_name)
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token requerido.",
        )
    try:
        payload = security.decode_refresh_token(refresh_token)
        usuario_id = int(payload.get("sub", "0"))
        negocio_id = int(payload.get("negocio_id", 0))
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido.",
        )

    usuario = UsuarioService.get_by_id(db, usuario_id=usuario_id, negocio_id=negocio_id)
    if not usuario or not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sesión inválida.",
        )

    access_token = security.create_access_token(
        subject=usuario.id,
        extra_claims={"negocio_id": usuario.negocio_id},
    )
    rotated_refresh = security.create_refresh_token(
        subject=usuario.id,
        negocio_id=usuario.negocio_id,
        expires_delta=timedelta(days=settings.refresh_token_expire_days),
    )
    response.set_cookie(
        key=settings.refresh_cookie_name,
        value=rotated_refresh,
        httponly=True,
        secure=settings.refresh_cookie_secure,
        samesite=settings.refresh_cookie_samesite,
        max_age=settings.refresh_token_expire_days * 24 * 3600,
        path="/auth",
    )
    return SessionResponse(
        access_token=access_token,
        user_id=usuario.id,
        negocio_id=usuario.negocio_id,
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response) -> None:
    response.delete_cookie(key=settings.refresh_cookie_name, path="/auth")
    return None


@router.get("/me", response_model=UsuarioResponse)
def read_me(current_user: Usuario = Depends(get_current_user)) -> UsuarioResponse:
    return current_user
