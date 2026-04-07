"""Routes for negocio registration."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core import security
from app.db.database import get_db
from app.schemas.negocio import NegocioRegister, NegocioRegisterResponse
from app.services.negocio_service import NegocioService

router = APIRouter(prefix="/negocios", tags=["negocios"])


@router.post("/register", response_model=NegocioRegisterResponse, status_code=status.HTTP_201_CREATED)
def register_negocio(
    payload: NegocioRegister,
    db: Session = Depends(get_db),
) -> NegocioRegisterResponse:
    negocio, admin = NegocioService.register_negocio(db, data=payload)
    access_token = security.create_access_token(
        subject=admin.id,
        extra_claims={"negocio_id": admin.negocio_id},
    )
    return NegocioRegisterResponse(
        access_token=access_token,
        negocio=negocio,
        usuario=admin,
    )
