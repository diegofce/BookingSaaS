"""Business logic for HorarioNegocio operations."""

from datetime import time
from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.horario_negocio import HorarioNegocio
from app.schemas.horario_negocio import HorarioNegocioCreate, HorarioNegocioUpdate


class HorarioNegocioService:

    @staticmethod
    def create(db: Session, data: HorarioNegocioCreate, negocio_id: int) -> HorarioNegocio:
        horario = HorarioNegocio(
            negocio_id=negocio_id,
            dia_semana=data.dia_semana,
            hora_inicio=data.hora_inicio,
            hora_fin=data.hora_fin,
        )
        db.add(horario)
        db.commit()
        db.refresh(horario)
        return horario

    @staticmethod
    def get_by_id(db: Session, horario_id: int, negocio_id: int) -> Optional[HorarioNegocio]:
        return (
            db.query(HorarioNegocio)
            .filter(HorarioNegocio.id == horario_id, HorarioNegocio.negocio_id == negocio_id)
            .first()
        )

    @staticmethod
    def get_all(
        db: Session,
        negocio_id: int,
        dia_semana: Optional[int] = None,
    ) -> List[HorarioNegocio]:
        query = db.query(HorarioNegocio).filter(HorarioNegocio.negocio_id == negocio_id)
        if dia_semana is not None:
            query = query.filter(HorarioNegocio.dia_semana == dia_semana)
        return query.order_by(HorarioNegocio.dia_semana, HorarioNegocio.hora_inicio).all()

    @staticmethod
    def get_for_day(db: Session, negocio_id: int, dia_semana: int) -> List[HorarioNegocio]:
        return HorarioNegocioService.get_all(db, negocio_id=negocio_id, dia_semana=dia_semana)

    @staticmethod
    def update(
        db: Session,
        horario_id: int,
        data: HorarioNegocioUpdate,
        negocio_id: int,
    ) -> HorarioNegocio:
        horario = HorarioNegocioService.get_by_id(db, horario_id, negocio_id)
        if not horario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Horario no encontrado.",
            )

        if data.dia_semana is not None:
            horario.dia_semana = data.dia_semana
        if data.hora_inicio is not None:
            horario.hora_inicio = data.hora_inicio
        if data.hora_fin is not None:
            horario.hora_fin = data.hora_fin

        if horario.hora_inicio >= horario.hora_fin:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="hora_inicio debe ser menor que hora_fin.",
            )

        db.add(horario)
        db.commit()
        db.refresh(horario)
        return horario

    @staticmethod
    def delete(db: Session, horario_id: int, negocio_id: int) -> None:
        horario = HorarioNegocioService.get_by_id(db, horario_id, negocio_id)
        if not horario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Horario no encontrado.",
            )
        db.delete(horario)
        db.commit()

