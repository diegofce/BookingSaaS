"""Pure database operations for Cliente — no HTTP concerns."""

from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate


def get(db: Session, cliente_id: int, negocio_id: int) -> Optional[Cliente]:
    return (
        db.query(Cliente)
        .filter(Cliente.id == cliente_id, Cliente.negocio_id == negocio_id)
        .first()
    )


def get_all(
    db: Session,
    negocio_id: int,
    skip: int = 0,
    limit: int = 100,
) -> List[Cliente]:
    return (
        db.query(Cliente)
        .filter(Cliente.negocio_id == negocio_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create(db: Session, data: ClienteCreate, negocio_id: int) -> Cliente:
    cliente = Cliente(
        negocio_id=negocio_id,
        nombre=data.nombre,
        email=data.email,
        telefono=data.telefono,
        direccion=data.direccion,
        barrio=data.barrio,
    )
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente


def update(db: Session, cliente: Cliente, data: ClienteUpdate) -> Cliente:
    if data.nombre is not None:
        cliente.nombre = data.nombre
    if data.email is not None:
        cliente.email = data.email
    if data.telefono is not None:
        cliente.telefono = data.telefono
    if data.direccion is not None:
        cliente.direccion = data.direccion
    if data.barrio is not None:
        cliente.barrio = data.barrio
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente


def delete(db: Session, cliente: Cliente) -> None:
    db.delete(cliente)
    db.commit()
