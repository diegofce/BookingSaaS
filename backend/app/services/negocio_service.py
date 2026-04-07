"""Service layer for Negocio registration and management."""

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core import security
from app.models.negocio import Negocio
from app.models.usuario import Usuario
from app.schemas.negocio import NegocioRegister


class NegocioService:
    """Encapsula la lógica relacionada con negocios."""

    @staticmethod
    def get_by_nombre(db: Session, nombre: str) -> Negocio | None:
        return db.query(Negocio).filter(Negocio.nombre == nombre).first()

    @staticmethod
    def get_by_dominio(db: Session, dominio: str) -> Negocio | None:
        return db.query(Negocio).filter(Negocio.dominio == dominio).first()

    @staticmethod
    def register_negocio(db: Session, data: NegocioRegister) -> tuple[Negocio, Usuario]:
        if NegocioService.get_by_nombre(db, data.negocio_nombre):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un negocio con ese nombre.",
            )

        if NegocioService.get_by_dominio(db, data.dominio):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un negocio con ese dominio.",
            )

        password_hash = security.hash_password(data.admin_password)

        negocio = Negocio(
            nombre=data.negocio_nombre,
            dominio=data.dominio,
            activo=True,
        )
        admin = Usuario(
            nombre=data.admin_nombre,
            email=data.admin_email,
            password_hash=password_hash,
            rol="admin",
            activo=True,
            negocio=negocio,
        )

        db.add(negocio)
        db.add(admin)

        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Violación de unicidad al crear el negocio o usuario.",
            )

        db.refresh(negocio)
        db.refresh(admin)
        return negocio, admin
