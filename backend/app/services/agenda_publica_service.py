"""Business logic for public booking endpoints."""

from datetime import date, datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud import cita as crud_cita
from app.crud import cliente as crud_cliente
from app.crud import servicio as crud_servicio
from app.models.cita import Cita
from app.models.negocio import Negocio
from app.models.servicio import Servicio
from app.schemas.agenda_publica import AgendaPublicaReservaCreate
from app.schemas.cliente import ClienteCreate
from app.services.horario_negocio_service import HorarioNegocioService
from app.services.notification_service import NotificationService
from app.services.negocio_service import NegocioService


class AgendaPublicaService:
    @staticmethod
    def _get_negocio_or_404(db: Session, negocio_slug: str) -> Negocio:
        negocio = NegocioService.get_by_dominio(db, dominio=negocio_slug)
        if not negocio or not negocio.activo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Negocio no encontrado.",
            )
        return negocio

    @staticmethod
    def _get_active_servicio_or_404(db: Session, negocio_id: int, servicio_id: int) -> Servicio:
        servicio = crud_servicio.get(db, servicio_id=servicio_id, negocio_id=negocio_id)
        if not servicio or not servicio.activo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Servicio no disponible.",
            )
        return servicio

    @staticmethod
    def _validate_inside_business_hours(
        db: Session,
        negocio_id: int,
        fecha_inicio: datetime,
        fecha_fin: datetime,
    ) -> None:
        horarios = HorarioNegocioService.get_for_day(
            db, negocio_id=negocio_id, dia_semana=fecha_inicio.weekday()
        )
        if not horarios:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="El negocio no tiene horario disponible para ese día.",
            )

        inicio_time = fecha_inicio.time()
        fin_time = fecha_fin.time()

        for horario in horarios:
            if horario.hora_inicio <= inicio_time and fin_time <= horario.hora_fin:
                return

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="La cita está fuera del horario del negocio.",
        )

    @staticmethod
    def list_servicios(db: Session, negocio_slug: str) -> list[Servicio]:
        negocio = AgendaPublicaService._get_negocio_or_404(db, negocio_slug=negocio_slug)
        return crud_servicio.get_all(
            db, negocio_id=negocio.id, skip=0, limit=500, solo_activos=True
        )

    @staticmethod
    def get_disponibilidad(
        db: Session,
        negocio_slug: str,
        servicio_id: int,
        fecha: date,
    ) -> list[str]:
        negocio = AgendaPublicaService._get_negocio_or_404(db, negocio_slug=negocio_slug)
        servicio = AgendaPublicaService._get_active_servicio_or_404(
            db, negocio_id=negocio.id, servicio_id=servicio_id
        )

        horarios = HorarioNegocioService.get_for_day(
            db, negocio_id=negocio.id, dia_semana=fecha.weekday()
        )
        if not horarios:
            return []

        duracion = timedelta(minutes=servicio.duracion_minutos)
        slots: list[str] = []
        for horario in horarios:
            limite = datetime.combine(fecha, horario.hora_fin)
            cursor = datetime.combine(fecha, horario.hora_inicio)
            while cursor + duracion <= limite:
                slot_fin = cursor + duracion
                if not crud_cita.has_overlap(
                    db,
                    negocio_id=negocio.id,
                    fecha_inicio=cursor,
                    fecha_fin=slot_fin,
                ):
                    slots.append(cursor.strftime("%H:%M"))
                cursor += duracion
        return slots

    @staticmethod
    def reservar(
        db: Session,
        negocio_slug: str,
        data: AgendaPublicaReservaCreate,
    ) -> Cita:
        negocio = AgendaPublicaService._get_negocio_or_404(db, negocio_slug=negocio_slug)
        servicio = AgendaPublicaService._get_active_servicio_or_404(
            db, negocio_id=negocio.id, servicio_id=data.servicio_id
        )

        fecha_fin = data.fecha_inicio + timedelta(minutes=servicio.duracion_minutos)
        AgendaPublicaService._validate_inside_business_hours(
            db,
            negocio_id=negocio.id,
            fecha_inicio=data.fecha_inicio,
            fecha_fin=fecha_fin,
        )

        if crud_cita.has_overlap(
            db,
            negocio_id=negocio.id,
            fecha_inicio=data.fecha_inicio,
            fecha_fin=fecha_fin,
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ese horario ya no está disponible.",
            )

        cliente = crud_cliente.create(
            db,
            negocio_id=negocio.id,
            data=ClienteCreate(
                nombre=data.cliente_nombre,
                email=data.cliente_email,
                telefono=data.cliente_telefono,
                direccion=data.cliente_direccion,
                barrio=data.cliente_barrio,
            ),
        )

        cita = crud_cita.create(
            db,
            negocio_id=negocio.id,
            cliente_id=cliente.id,
            servicio_id=servicio.id,
            empleado_id=None,
            fecha_inicio=data.fecha_inicio,
            fecha_fin=fecha_fin,
            monto_pagado=0,
        )

        NotificationService.send_appointment_confirmation(cita, cliente, servicio)
        return cita
