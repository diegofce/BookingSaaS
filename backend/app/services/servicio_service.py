"""Business logic for Servicio operations."""

from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud import servicio as crud
from app.models.servicio import Servicio
from app.schemas.servicio import ServicioCreate, ServicioUpdate


class ServicioService:

    @staticmethod
    def get_or_404(db: Session, servicio_id: int, negocio_id: int) -> Servicio:
        servicio = crud.get(db, servicio_id=servicio_id, negocio_id=negocio_id)
        if not servicio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Servicio no encontrado.",
            )
        return servicio

    @staticmethod
    def list_servicios(
        db: Session,
        negocio_id: int,
        skip: int = 0,
        limit: int = 100,
        solo_activos: bool = False,
    ) -> List[Servicio]:
        return crud.get_all(
            db,
            negocio_id=negocio_id,
            skip=skip,
            limit=limit,
            solo_activos=solo_activos,
        )

    @staticmethod
    def create_servicio(db: Session, data: ServicioCreate, negocio_id: int) -> Servicio:
        return crud.create(db, data=data, negocio_id=negocio_id)

    @staticmethod
    def update_servicio(
        db: Session,
        servicio_id: int,
        data: ServicioUpdate,
        negocio_id: int,
    ) -> Servicio:
        servicio = ServicioService.get_or_404(db, servicio_id, negocio_id)
        return crud.update(db, servicio=servicio, data=data)

    @staticmethod
    def delete_servicio(db: Session, servicio_id: int, negocio_id: int) -> None:
        servicio = ServicioService.get_or_404(db, servicio_id, negocio_id)
        crud.delete(db, servicio=servicio)

    @staticmethod
    def create(db: Session, data: ServicioCreate, negocio_id: int) -> Servicio:
        return ServicioService.create_servicio(db, data=data, negocio_id=negocio_id)

    @staticmethod
    def get_by_id(db: Session, servicio_id: int, negocio_id: int) -> Servicio:
        return ServicioService.get_or_404(db, servicio_id=servicio_id, negocio_id=negocio_id)

    @staticmethod
    def get_all(
        db: Session,
        negocio_id: int,
        skip: int = 0,
        limit: int = 100,
        solo_activos: bool = False,
    ) -> List[Servicio]:
        return ServicioService.list_servicios(
            db,
            negocio_id=negocio_id,
            skip=skip,
            limit=limit,
            solo_activos=solo_activos,
        )

    @staticmethod
    def update(
        db: Session,
        servicio_id: int,
        data: ServicioUpdate,
        negocio_id: int,
    ) -> Servicio:
        return ServicioService.update_servicio(
            db, servicio_id=servicio_id, data=data, negocio_id=negocio_id)

    @staticmethod
    def delete(db: Session, servicio_id: int, negocio_id: int) -> None:
        ServicioService.delete_servicio(db, servicio_id=servicio_id, negocio_id=negocio_id)
