"""Pure database operations for Servicio — no HTTP concerns."""

from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.servicio import Servicio
from app.schemas.servicio import ServicioCreate, ServicioUpdate


def get(db: Session, servicio_id: int, negocio_id: int) -> Optional[Servicio]:
    return (
        db.query(Servicio)
        .filter(Servicio.id == servicio_id, Servicio.negocio_id == negocio_id)
        .first()
    )


def get_all(
    db: Session,
    negocio_id: int,
    skip: int = 0,
    limit: int = 100,
    solo_activos: bool = False,
) -> List[Servicio]:
    query = db.query(Servicio).filter(Servicio.negocio_id == negocio_id)
    if solo_activos:
        query = query.filter(Servicio.activo.is_(True))
    return query.offset(skip).limit(limit).all()


def create(db: Session, data: ServicioCreate, negocio_id: int) -> Servicio:
    servicio = Servicio(
        negocio_id=negocio_id,
        nombre=data.nombre,
        descripcion=data.descripcion,
        duracion_minutos=data.duracion_minutos,
        precio=data.precio,
        activo=data.activo,
    )
    db.add(servicio)
    db.commit()
    db.refresh(servicio)
    return servicio


def update(db: Session, servicio: Servicio, data: ServicioUpdate) -> Servicio:
    if data.nombre is not None:
        servicio.nombre = data.nombre
    if data.descripcion is not None:
        servicio.descripcion = data.descripcion
    if data.duracion_minutos is not None:
        servicio.duracion_minutos = data.duracion_minutos
    if data.precio is not None:
        servicio.precio = data.precio
    if data.activo is not None:
        servicio.activo = data.activo
    db.add(servicio)
    db.commit()
    db.refresh(servicio)
    return servicio


def delete(db: Session, servicio: Servicio) -> None:
    db.delete(servicio)
    db.commit()
