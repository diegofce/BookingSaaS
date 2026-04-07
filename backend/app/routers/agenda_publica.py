"""Public Calendly-like booking routes (no authentication required)."""

from datetime import date

from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.orm import Session

from app.core.rate_limit import limiter
from app.db.database import get_db
from app.schemas.agenda_publica import (
    AgendaPublicaReservaCreate,
    AgendaPublicaReservaResponse,
    AgendaServicioResponse,
)
from app.services.agenda_publica_service import AgendaPublicaService

router = APIRouter(prefix="/agenda/publica", tags=["agenda-publica"])


@router.get("/{negocio_slug}/servicios", response_model=list[AgendaServicioResponse])
@limiter.limit("60/minute")
def get_servicios_publicos(
    request: Request,
    negocio_slug: str,
    db: Session = Depends(get_db),
) -> list[AgendaServicioResponse]:
    return AgendaPublicaService.list_servicios(db, negocio_slug=negocio_slug)


@router.get("/{negocio_slug}/disponibilidad", response_model=list[str])
@limiter.limit("60/minute")
def get_disponibilidad_publica(
    request: Request,
    negocio_slug: str,
    servicio_id: int = Query(...),
    fecha: date = Query(...),
    db: Session = Depends(get_db),
) -> list[str]:
    return AgendaPublicaService.get_disponibilidad(
        db,
        negocio_slug=negocio_slug,
        servicio_id=servicio_id,
        fecha=fecha,
    )


@router.post(
    "/{negocio_slug}/reservar",
    response_model=AgendaPublicaReservaResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("20/minute")
def reservar_publicamente(
    request: Request,
    negocio_slug: str,
    payload: AgendaPublicaReservaCreate,
    db: Session = Depends(get_db),
) -> AgendaPublicaReservaResponse:
    cita = AgendaPublicaService.reservar(db, negocio_slug=negocio_slug, data=payload)
    return AgendaPublicaReservaResponse(cita=cita)

