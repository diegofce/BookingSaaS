"""CRUD endpoints for Clientes, scoped to the authenticated user's negocio."""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.roles import ensure_admin, ensure_staff
from app.models.usuario import Usuario
from app.schemas.cliente import ClienteCreate, ClienteResponse, ClienteUpdate
from app.services.cliente_service import ClienteService

router = APIRouter(prefix="/clientes", tags=["clientes"])


@router.get("", response_model=list[ClienteResponse])
def list_clientes(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> list[ClienteResponse]:
    ensure_staff(current_user)
    return ClienteService.get_all(
        db=db, negocio_id=current_user.negocio_id, skip=skip, limit=limit)


@router.get("/{cliente_id}", response_model=ClienteResponse)
def get_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> ClienteResponse:
    ensure_staff(current_user)
    return ClienteService.get_by_id(
        db=db, cliente_id=cliente_id, negocio_id=current_user.negocio_id)


@router.post("", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def create_cliente(
    payload: ClienteCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> ClienteResponse:
    ensure_staff(current_user)
    return ClienteService.create(db=db, data=payload, negocio_id=current_user.negocio_id)


@router.put("/{cliente_id}", response_model=ClienteResponse)
def update_cliente(
    cliente_id: int,
    payload: ClienteUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> ClienteResponse:
    ensure_staff(current_user)
    return ClienteService.update(
        db,
        cliente_id=cliente_id,
        data=payload,
        negocio_id=current_user.negocio_id,
    )


@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> None:
    ensure_admin(current_user)
    ClienteService.delete(db=db, cliente_id=cliente_id, negocio_id=current_user.negocio_id)
    return None
