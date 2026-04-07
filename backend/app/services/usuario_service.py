"""Service layer for Usuario operations (synchronous SQLAlchemy)."""

from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core import security
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate


class UsuarioService:
    """Encapsula la lógica de negocio para usuarios con filtrado por negocio."""

    @staticmethod
    def get_by_id(db: Session, usuario_id: int, negocio_id: int) -> Optional[Usuario]:
        return (
            db.query(Usuario)
            .filter(Usuario.id == usuario_id, Usuario.negocio_id == negocio_id)
            .first()
        )

    @staticmethod
    def get_by_email(db: Session, email: str, negocio_id: int) -> Optional[Usuario]:
        return (
            db.query(Usuario)
            .filter(Usuario.email == email, Usuario.negocio_id == negocio_id)
            .first()
        )

    @staticmethod
    def list_users(db: Session, negocio_id: int) -> List[Usuario]:
        return db.query(Usuario).filter(Usuario.negocio_id == negocio_id).all()

    @staticmethod
    def create_user(db: Session, data: UsuarioCreate, negocio_id: int) -> Usuario:
        existing = UsuarioService.get_by_email(db, data.email, negocio_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El email ya está registrado en este negocio.",
            )

        password_hash = security.hash_password(data.password)
        usuario = Usuario(
            nombre=data.nombre,
            email=data.email,
            password_hash=password_hash,
            rol=data.rol,
            activo=data.activo,
            negocio_id=negocio_id,
        )
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario

    @staticmethod
    def update_user(
        db: Session, usuario_id: int, data: UsuarioUpdate, negocio_id: int
    ) -> Usuario:
        usuario = UsuarioService.get_by_id(db, usuario_id, negocio_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado.")

        if data.email and data.email != usuario.email:
            duplicate = UsuarioService.get_by_email(db, data.email, negocio_id)
            if duplicate:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="El email ya está registrado en este negocio.",
                )

        if data.nombre is not None:
            usuario.nombre = data.nombre
        if data.email is not None:
            usuario.email = data.email
        if data.rol is not None:
            usuario.rol = data.rol
        if data.activo is not None:
            usuario.activo = data.activo
        if data.password is not None:
            usuario.password_hash = security.hash_password(data.password)

        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario

    @staticmethod
    def delete_user(db: Session, usuario_id: int, negocio_id: int) -> None:
        usuario = UsuarioService.get_by_id(db, usuario_id, negocio_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado.")

        db.delete(usuario)
        db.commit()

    @staticmethod
    def authenticate(db: Session, email: str, password: str, negocio_id: int) -> Usuario:
        usuario = UsuarioService.get_by_email(db, email, negocio_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not security.verify_password(password, usuario.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not usuario.activo:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario inactivo.",
            )

        return usuario
