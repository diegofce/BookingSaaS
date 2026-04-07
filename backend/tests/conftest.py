from __future__ import annotations

import os
from pathlib import Path
from datetime import time
import sys
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault("ENABLE_BACKGROUND_REMINDERS", "false")

from app.core import security
from app.db.database import Base, get_db
from app.main import app
from app.models.cliente import Cliente
from app.models.horario_negocio import HorarioNegocio
from app.models.negocio import Negocio
from app.models.servicio import Servicio
from app.models.usuario import Usuario


@pytest.fixture
def client() -> TestClient:
    tmp_dir = Path(__file__).resolve().parent / ".tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    db_file = tmp_dir / f"test_booking_{uuid4().hex}.db"
    test_db_url = f"sqlite:///{db_file}"
    os.environ["DATABASE_URL"] = test_db_url
    os.environ["JWT_SECRET_KEY"] = "test-secret"
    os.environ["JWT_ALGORITHM"] = "HS256"

    engine = create_engine(test_db_url, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()
    if db_file.exists():
        try:
            db_file.unlink()
        except PermissionError:
            pass


@pytest.fixture
def seed_data(client: TestClient) -> dict[str, int | str]:
    db_generator = app.dependency_overrides[get_db]()
    db = next(db_generator)

    try:
        negocio = Negocio(nombre="Acme Spa", dominio="acme-spa", activo=True)
        db.add(negocio)
        db.flush()

        admin = Usuario(
            negocio_id=negocio.id,
            nombre="Admin",
            email="admin@acme.com",
            password_hash="test-hash",
            rol="admin",
            activo=True,
        )
        cliente = Cliente(
            negocio_id=negocio.id,
            nombre="Cliente Demo",
            telefono="3000000000",
            direccion=None,
            barrio=None,
        )
        servicio = Servicio(
            negocio_id=negocio.id,
            nombre="Corte",
            descripcion="Corte basico",
            duracion_minutos=30,
            precio=25000,
            activo=True,
        )
        horario = HorarioNegocio(
            negocio_id=negocio.id,
            dia_semana=0,
            hora_inicio=time(9, 0),
            hora_fin=time(11, 0),
        )

        db.add_all([admin, cliente, servicio, horario])
        db.commit()
        token = security.create_access_token(
            subject=admin.id,
            extra_claims={"negocio_id": negocio.id},
        )

        return {
            "negocio_id": negocio.id,
            "negocio_slug": negocio.dominio,
            "cliente_id": cliente.id,
            "servicio_id": servicio.id,
            "token": token,
        }
    finally:
        db_generator.close()
