"""Pure database operations for Cita — no HTTP concerns."""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.models.cita import Cita
from app.schemas.cita import CitaUpdate


def get(db: Session, cita_id: int, negocio_id: int) -> Optional[Cita]:
    return (
        db.query(Cita)
        .filter(Cita.id == cita_id, Cita.negocio_id == negocio_id)
        .first()
    )


def get_all(
    db: Session,
    negocio_id: int,
    skip: int = 0,
    limit: int = 100,
    cliente_id: Optional[int] = None,
    servicio_id: Optional[int] = None,
    empleado_id: Optional[int] = None,
) -> List[Cita]:
    query = db.query(Cita).filter(Cita.negocio_id == negocio_id)
    if cliente_id is not None:
        query = query.filter(Cita.cliente_id == cliente_id)
    if servicio_id is not None:
        query = query.filter(Cita.servicio_id == servicio_id)
    if empleado_id is not None:
        query = query.filter(Cita.empleado_id == empleado_id)
    return query.order_by(Cita.fecha_inicio).offset(skip).limit(limit).all()


def has_overlap(
    db: Session,
    negocio_id: int,
    fecha_inicio: datetime,
    fecha_fin: datetime,
    exclude_cita_id: Optional[int] = None,
) -> bool:
    """Return True if any non-cancelled appointment overlaps the given time range."""
    query = db.query(Cita).filter(
        Cita.negocio_id == negocio_id,
        Cita.estado != "cancelada",
        # Overlap condition: existing.start < new.end AND existing.end > new.start
        Cita.fecha_inicio < fecha_fin,
        Cita.fecha_fin > fecha_inicio,
    )
    if exclude_cita_id is not None:
        query = query.filter(Cita.id != exclude_cita_id)
    return db.query(query.exists()).scalar()


def create(
    db: Session,
    negocio_id: int,
    cliente_id: int,
    servicio_id: int,
    empleado_id: Optional[int],
    fecha_inicio: datetime,
    fecha_fin: datetime,
    monto_pagado,
) -> Cita:
    cita = Cita(
        negocio_id=negocio_id,
        cliente_id=cliente_id,
        servicio_id=servicio_id,
        empleado_id=empleado_id,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        monto_pagado=monto_pagado,
    )
    db.add(cita)
    db.commit()
    db.refresh(cita)
    return cita


def update(db: Session, cita: Cita, data: CitaUpdate) -> Cita:
    if data.cliente_id is not None:
        cita.cliente_id = data.cliente_id
    if data.servicio_id is not None:
        cita.servicio_id = data.servicio_id
    if data.empleado_id is not None:
        cita.empleado_id = data.empleado_id
    if data.fecha_inicio is not None:
        cita.fecha_inicio = data.fecha_inicio
    if data.estado is not None:
        cita.estado = data.estado
    if data.monto_pagado is not None:
        cita.monto_pagado = data.monto_pagado
    db.add(cita)
    db.commit()
    db.refresh(cita)
    return cita


def delete(db: Session, cita: Cita) -> None:
    db.delete(cita)
    db.commit()
