"""CRUD endpoints for business weekly availability."""

from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.roles import ensure_admin, ensure_staff
from app.models.usuario import Usuario
from app.schemas.horario_negocio import (
    HorarioNegocioCreate,
    HorarioNegocioResponse,
    HorarioNegocioUpdate,
)
from app.services.horario_negocio_service import HorarioNegocioService

router = APIRouter(prefix="/horarios-negocio", tags=["horarios-negocio"])


@router.post("", response_model=HorarioNegocioResponse, status_code=status.HTTP_201_CREATED)
def create_horario(
    payload: HorarioNegocioCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> HorarioNegocioResponse:
    ensure_admin(current_user)
    return HorarioNegocioService.create(
        db=db, data=payload, negocio_id=current_user.negocio_id)


@router.get("", response_model=list[HorarioNegocioResponse])
def get_horarios(
    dia_semana: Optional[int] = Query(default=None, ge=0, le=6),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> list[HorarioNegocioResponse]:
    ensure_staff(current_user)
    return HorarioNegocioService.get_all(
        db=db, negocio_id=current_user.negocio_id, dia_semana=dia_semana)


@router.put("/{horario_id}", response_model=HorarioNegocioResponse)
def update_horario(
    horario_id: int,
    payload: HorarioNegocioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> HorarioNegocioResponse:
    ensure_admin(current_user)
    return HorarioNegocioService.update(
        db=db,
        horario_id=horario_id,
        data=payload,
        negocio_id=current_user.negocio_id,
    )


@router.delete("/{horario_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_horario(
    horario_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> None:
    ensure_admin(current_user)
    HorarioNegocioService.delete(
        db=db, horario_id=horario_id, negocio_id=current_user.negocio_id)
    return None

