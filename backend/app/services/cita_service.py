"""Business logic for Cita operations."""

from datetime import date, datetime, timedelta
from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud import cita as crud
from app.crud import cliente as crud_cliente
from app.crud import servicio as crud_servicio
from app.models.cita import Cita
from app.models.usuario import Usuario
from app.schemas.cita import CitaCreate, CitaUpdate
from app.services.horario_negocio_service import HorarioNegocioService
from app.services.notification_service import NotificationService
from app.services.usuario_service import UsuarioService


class CitaService:
    @staticmethod
    def _validate_staff(user: Usuario) -> None:
        if user.rol not in {"admin", "empleado"}:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Se requiere rol 'admin' o 'empleado' para esta acción.",
            )

    @staticmethod
    def _resolve_empleado_id(
        db: Session,
        negocio_id: int,
        current_user: Usuario,
        requested_empleado_id: Optional[int],
    ) -> Optional[int]:
        if current_user.rol == "empleado":
            return current_user.id

        if requested_empleado_id is None:
            return None

        empleado = UsuarioService.get_by_id(
            db, usuario_id=requested_empleado_id, negocio_id=negocio_id)
        if not empleado or empleado.rol not in {"admin", "empleado"}:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empleado asignado no encontrado.",
            )
        return requested_empleado_id

    @staticmethod
    def get_or_404(
        db: Session,
        cita_id: int,
        negocio_id: int,
        current_user: Usuario,
    ) -> Cita:
        CitaService._validate_staff(current_user)
        cita = crud.get(db, cita_id=cita_id, negocio_id=negocio_id)
        if not cita:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cita no encontrada.",
            )
        if current_user.rol == "empleado" and cita.empleado_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo puedes ver citas asignadas a tu usuario.",
            )
        return cita

    @staticmethod
    def list_citas(
        db: Session,
        negocio_id: int,
        current_user: Usuario,
        skip: int = 0,
        limit: int = 100,
        cliente_id: Optional[int] = None,
        servicio_id: Optional[int] = None,
        empleado_id: Optional[int] = None,
    ) -> List[Cita]:
        CitaService._validate_staff(current_user)
        if current_user.rol == "empleado":
            empleado_id = current_user.id
        return crud.get_all(
            db,
            negocio_id=negocio_id,
            skip=skip,
            limit=limit,
            cliente_id=cliente_id,
            servicio_id=servicio_id,
            empleado_id=empleado_id,
        )

    @staticmethod
    def create_cita(
        db: Session,
        data: CitaCreate,
        negocio_id: int,
        current_user: Usuario,
    ) -> Cita:
        CitaService._validate_staff(current_user)

        cliente = crud_cliente.get(db, cliente_id=data.cliente_id, negocio_id=negocio_id)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado.",
            )

        servicio = crud_servicio.get(
            db, servicio_id=data.servicio_id, negocio_id=negocio_id)
        if not servicio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Servicio no encontrado.",
            )
        if not servicio.activo:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="El servicio no está activo.",
            )

        empleado_id = CitaService._resolve_empleado_id(
            db=db,
            negocio_id=negocio_id,
            current_user=current_user,
            requested_empleado_id=data.empleado_id,
        )

        fecha_fin = data.fecha_inicio + timedelta(minutes=servicio.duracion_minutos)

        if crud.has_overlap(db, negocio_id=negocio_id,
                            fecha_inicio=data.fecha_inicio, fecha_fin=fecha_fin):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe una cita en ese horario.",
            )

        cita = crud.create(
            db,
            negocio_id=negocio_id,
            cliente_id=data.cliente_id,
            servicio_id=data.servicio_id,
            empleado_id=empleado_id,
            fecha_inicio=data.fecha_inicio,
            fecha_fin=fecha_fin,
            monto_pagado=data.monto_pagado,
        )
        NotificationService.send_appointment_confirmation(cita, cliente, servicio)
        return cita

    @staticmethod
    def update_cita(
        db: Session,
        cita_id: int,
        data: CitaUpdate,
        negocio_id: int,
        current_user: Usuario,
    ) -> Cita:
        cita = CitaService.get_or_404(db, cita_id, negocio_id, current_user)

        cliente_id = data.cliente_id if data.cliente_id is not None else cita.cliente_id
        servicio_id = data.servicio_id if data.servicio_id is not None else cita.servicio_id

        cliente = crud_cliente.get(db, cliente_id=cliente_id, negocio_id=negocio_id)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado.",
            )

        servicio = crud_servicio.get(db, servicio_id=servicio_id, negocio_id=negocio_id)
        if not servicio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Servicio no encontrado.",
            )

        nuevo_inicio = data.fecha_inicio if data.fecha_inicio is not None else cita.fecha_inicio
        nuevo_fin = nuevo_inicio + timedelta(minutes=servicio.duracion_minutos)

        if crud.has_overlap(
            db,
            negocio_id=negocio_id,
            fecha_inicio=nuevo_inicio,
            fecha_fin=nuevo_fin,
            exclude_cita_id=cita.id,
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe una cita en ese horario.",
            )

        cita.fecha_fin = nuevo_fin
        data.empleado_id = CitaService._resolve_empleado_id(
            db=db,
            negocio_id=negocio_id,
            current_user=current_user,
            requested_empleado_id=(data.empleado_id if data.empleado_id is not None else cita.empleado_id),
        )
        return crud.update(db, cita=cita, data=data)

    @staticmethod
    def delete_cita(
        db: Session,
        cita_id: int,
        negocio_id: int,
        current_user: Usuario,
    ) -> None:
        cita = CitaService.get_or_404(db, cita_id, negocio_id, current_user)
        crud.delete(db, cita=cita)

    @staticmethod
    def get_available_slots(
        db: Session,
        negocio_id: int,
        servicio_id: int,
        fecha: date,
    ) -> List[str]:
        servicio = crud_servicio.get(db, servicio_id=servicio_id, negocio_id=negocio_id)
        if not servicio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Servicio no encontrado.",
            )
        if not servicio.activo:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="El servicio no está activo.",
            )

        horarios = HorarioNegocioService.get_for_day(
            db, negocio_id=negocio_id, dia_semana=fecha.weekday())
        if not horarios:
            return []

        duracion = timedelta(minutes=servicio.duracion_minutos)
        slots: List[str] = []

        for horario in horarios:
            limite = datetime.combine(fecha, horario.hora_fin)
            cursor = datetime.combine(fecha, horario.hora_inicio)

            while cursor + duracion <= limite:
                slot_fin = cursor + duracion
                if not crud.has_overlap(
                    db,
                    negocio_id=negocio_id,
                    fecha_inicio=cursor,
                    fecha_fin=slot_fin,
                ):
                    slots.append(cursor.strftime("%H:%M"))
                cursor += duracion

        return slots

    @staticmethod
    def send_reminder(
        db: Session,
        cita_id: int,
        negocio_id: int,
        current_user: Usuario,
    ) -> None:
        cita = CitaService.get_or_404(db, cita_id, negocio_id, current_user)
        cliente = crud_cliente.get(db, cliente_id=cita.cliente_id, negocio_id=negocio_id)
        servicio = crud_servicio.get(db, servicio_id=cita.servicio_id, negocio_id=negocio_id)
        if not cliente or not servicio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se pudo enviar recordatorio por referencias inválidas.",
            )
        NotificationService.send_appointment_reminder(cita, cliente, servicio)

    @staticmethod
    def create(db: Session, data: CitaCreate, negocio_id: int, current_user: Usuario) -> Cita:
        return CitaService.create_cita(
            db=db, data=data, negocio_id=negocio_id, current_user=current_user)

    @staticmethod
    def get_by_id(db: Session, cita_id: int, negocio_id: int, current_user: Usuario) -> Cita:
        return CitaService.get_or_404(
            db=db, cita_id=cita_id, negocio_id=negocio_id, current_user=current_user)

    @staticmethod
    def get_all(
        db: Session,
        negocio_id: int,
        current_user: Usuario,
        skip: int = 0,
        limit: int = 100,
        cliente_id: Optional[int] = None,
        servicio_id: Optional[int] = None,
        empleado_id: Optional[int] = None,
    ) -> List[Cita]:
        return CitaService.list_citas(
            db=db,
            negocio_id=negocio_id,
            current_user=current_user,
            skip=skip,
            limit=limit,
            cliente_id=cliente_id,
            servicio_id=servicio_id,
            empleado_id=empleado_id,
        )

    @staticmethod
    def update(
        db: Session,
        cita_id: int,
        data: CitaUpdate,
        negocio_id: int,
        current_user: Usuario,
    ) -> Cita:
        return CitaService.update_cita(
            db=db,
            cita_id=cita_id,
            data=data,
            negocio_id=negocio_id,
            current_user=current_user,
        )

    @staticmethod
    def delete(db: Session, cita_id: int, negocio_id: int, current_user: Usuario) -> None:
        CitaService.delete_cita(
            db=db, cita_id=cita_id, negocio_id=negocio_id, current_user=current_user)
