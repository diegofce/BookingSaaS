"""CRUD endpoints for Servicios, scoped to the authenticated user's negocio."""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.roles import ensure_admin, ensure_staff
from app.models.usuario import Usuario
from app.schemas.servicio import ServicioCreate, ServicioResponse, ServicioUpdate
from app.services.servicio_service import ServicioService

router = APIRouter(prefix="/servicios", tags=["servicios"])


@router.get("", response_model=list[ServicioResponse])
def list_servicios(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    solo_activos: bool = Query(default=False),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> list[ServicioResponse]:
    ensure_staff(current_user)
    return ServicioService.get_all(
        db,
        negocio_id=current_user.negocio_id,
        skip=skip,
        limit=limit,
        solo_activos=solo_activos,
    )


@router.get("/{servicio_id}", response_model=ServicioResponse)
def get_servicio(
    servicio_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> ServicioResponse:
    ensure_staff(current_user)
    return ServicioService.get_by_id(
        db=db, servicio_id=servicio_id, negocio_id=current_user.negocio_id)


@router.post("", response_model=ServicioResponse, status_code=status.HTTP_201_CREATED)
def create_servicio(
    payload: ServicioCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> ServicioResponse:
    ensure_admin(current_user)
    return ServicioService.create(db=db, data=payload, negocio_id=current_user.negocio_id)


@router.put("/{servicio_id}", response_model=ServicioResponse)
def update_servicio(
    servicio_id: int,
    payload: ServicioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> ServicioResponse:
    ensure_admin(current_user)
    return ServicioService.update(
        db,
        servicio_id=servicio_id,
        data=payload,
        negocio_id=current_user.negocio_id,
    )


@router.delete("/{servicio_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_servicio(
    servicio_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> None:
    ensure_admin(current_user)
    ServicioService.delete(db=db, servicio_id=servicio_id, negocio_id=current_user.negocio_id)
    return None
