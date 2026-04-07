"""CRUD endpoints for Citas, scoped to the authenticated user's negocio."""

from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.orm import Session

from app.core.rate_limit import limiter
from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.roles import ensure_admin
from app.models.usuario import Usuario
from app.schemas.cita import CitaCreate, CitaResponse, CitaUpdate
from app.services.cita_service import CitaService

router = APIRouter(prefix="/citas", tags=["citas"])


# ── Disponibilidad (must be defined before /{cita_id} to avoid route conflict) ─

@router.get(
    "/disponibilidad",
    response_model=list[str],
    summary="Horarios disponibles para un servicio en un día dado",
)
@limiter.limit("60/minute")
def get_disponibilidad(
    request: Request,
    servicio_id: int = Query(..., description="ID del servicio"),
    fecha: date = Query(..., description="Fecha a consultar (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> list[str]:
    return CitaService.get_available_slots(
        db,
        negocio_id=current_user.negocio_id,
        servicio_id=servicio_id,
        fecha=fecha,
    )


# ── CRUD ────────────────────────────────────────────────────────────────────────

@router.get("", response_model=list[CitaResponse])
@limiter.limit("60/minute")
def list_citas(
    request: Request,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    cliente_id: Optional[int] = Query(default=None),
    servicio_id: Optional[int] = Query(default=None),
    empleado_id: Optional[int] = Query(default=None),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> list[CitaResponse]:
    return CitaService.get_all(
        db,
        negocio_id=current_user.negocio_id,
        current_user=current_user,
        skip=skip,
        limit=limit,
        cliente_id=cliente_id,
        servicio_id=servicio_id,
        empleado_id=empleado_id,
    )


@router.get("/{cita_id}", response_model=CitaResponse)
def get_cita(
    cita_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> CitaResponse:
    return CitaService.get_by_id(
        db=db,
        cita_id=cita_id,
        negocio_id=current_user.negocio_id,
        current_user=current_user,
    )


@router.post("", response_model=CitaResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("30/minute")
def create_cita(
    request: Request,
    payload: CitaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> CitaResponse:
    return CitaService.create(
        db=db,
        data=payload,
        negocio_id=current_user.negocio_id,
        current_user=current_user,
    )


@router.put("/{cita_id}", response_model=CitaResponse)
def update_cita(
    cita_id: int,
    payload: CitaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> CitaResponse:
    return CitaService.update(
        db,
        cita_id=cita_id,
        data=payload,
        negocio_id=current_user.negocio_id,
        current_user=current_user,
    )


@router.delete("/{cita_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cita(
    cita_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> None:
    ensure_admin(current_user)
    CitaService.delete(
        db=db,
        cita_id=cita_id,
        negocio_id=current_user.negocio_id,
        current_user=current_user,
    )
    return None


@router.post("/{cita_id}/recordatorio", status_code=status.HTTP_204_NO_CONTENT)
def send_recordatorio(
    cita_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> None:
    CitaService.send_reminder(
        db=db,
        cita_id=cita_id,
        negocio_id=current_user.negocio_id,
        current_user=current_user,
    )
    return None
