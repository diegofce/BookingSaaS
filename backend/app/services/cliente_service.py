"""Business logic for Cliente operations."""

from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud import cliente as crud
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate


class ClienteService:

    @staticmethod
    def get_or_404(db: Session, cliente_id: int, negocio_id: int) -> Cliente:
        cliente = crud.get(db, cliente_id=cliente_id, negocio_id=negocio_id)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado.",
            )
        return cliente

    @staticmethod
    def list_clientes(
        db: Session,
        negocio_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Cliente]:
        return crud.get_all(db, negocio_id=negocio_id, skip=skip, limit=limit)

    @staticmethod
    def create_cliente(db: Session, data: ClienteCreate, negocio_id: int) -> Cliente:
        return crud.create(db, data=data, negocio_id=negocio_id)

    @staticmethod
    def update_cliente(
        db: Session,
        cliente_id: int,
        data: ClienteUpdate,
        negocio_id: int,
    ) -> Cliente:
        cliente = ClienteService.get_or_404(db, cliente_id, negocio_id)
        return crud.update(db, cliente=cliente, data=data)

    @staticmethod
    def delete_cliente(db: Session, cliente_id: int, negocio_id: int) -> None:
        cliente = ClienteService.get_or_404(db, cliente_id, negocio_id)
        crud.delete(db, cliente=cliente)

    @staticmethod
    def create(db: Session, data: ClienteCreate, negocio_id: int) -> Cliente:
        return ClienteService.create_cliente(db, data=data, negocio_id=negocio_id)

    @staticmethod
    def get_by_id(db: Session, cliente_id: int, negocio_id: int) -> Cliente:
        return ClienteService.get_or_404(db, cliente_id=cliente_id, negocio_id=negocio_id)

    @staticmethod
    def get_all(
        db: Session,
        negocio_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Cliente]:
        return ClienteService.list_clientes(db, negocio_id=negocio_id, skip=skip, limit=limit)

    @staticmethod
    def update(
        db: Session,
        cliente_id: int,
        data: ClienteUpdate,
        negocio_id: int,
    ) -> Cliente:
        return ClienteService.update_cliente(
            db, cliente_id=cliente_id, data=data, negocio_id=negocio_id)

    @staticmethod
    def delete(db: Session, cliente_id: int, negocio_id: int) -> None:
        ClienteService.delete_cliente(db, cliente_id=cliente_id, negocio_id=negocio_id)
