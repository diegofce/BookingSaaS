from __future__ import annotations


def _auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_crear_cita(client, seed_data):
    response = client.post(
        "/citas",
        headers=_auth_headers(seed_data["token"]),
        json={
            "cliente_id": seed_data["cliente_id"],
            "servicio_id": seed_data["servicio_id"],
            "fecha_inicio": "2026-03-09T09:00:00",
            "monto_pagado": "0.00",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["cliente_id"] == seed_data["cliente_id"]
    assert body["servicio_id"] == seed_data["servicio_id"]
    assert body["fecha_fin"].startswith("2026-03-09T09:30:00")


def test_evitar_doble_reserva(client, seed_data):
    payload = {
        "cliente_id": seed_data["cliente_id"],
        "servicio_id": seed_data["servicio_id"],
        "fecha_inicio": "2026-03-09T09:00:00",
        "monto_pagado": "0.00",
    }
    first = client.post("/citas", headers=_auth_headers(seed_data["token"]), json=payload)
    assert first.status_code == 201

    second = client.post("/citas", headers=_auth_headers(seed_data["token"]), json=payload)
    assert second.status_code == 409
    assert "horario" in second.json()["detail"].lower()


def test_disponibilidad_excluye_slots_ocupados(client, seed_data):
    create = client.post(
        "/citas",
        headers=_auth_headers(seed_data["token"]),
        json={
            "cliente_id": seed_data["cliente_id"],
            "servicio_id": seed_data["servicio_id"],
            "fecha_inicio": "2026-03-09T09:00:00",
            "monto_pagado": "0.00",
        },
    )
    assert create.status_code == 201

    response = client.get(
        "/citas/disponibilidad",
        headers=_auth_headers(seed_data["token"]),
        params={"servicio_id": seed_data["servicio_id"], "fecha": "2026-03-09"},
    )
    assert response.status_code == 200
    slots = response.json()
    assert "09:00" not in slots
    assert "09:30" in slots


def test_agenda_publica_servicios_disponibilidad_y_reserva(client, seed_data):
    servicios = client.get(f"/agenda/publica/{seed_data['negocio_slug']}/servicios")
    assert servicios.status_code == 200
    assert any(s["id"] == seed_data["servicio_id"] for s in servicios.json())

    disponibilidad = client.get(
        f"/agenda/publica/{seed_data['negocio_slug']}/disponibilidad",
        params={"servicio_id": seed_data["servicio_id"], "fecha": "2026-03-09"},
    )
    assert disponibilidad.status_code == 200
    assert "09:00" in disponibilidad.json()

    reserva = client.post(
        f"/agenda/publica/{seed_data['negocio_slug']}/reservar",
        json={
            "servicio_id": seed_data["servicio_id"],
            "fecha_inicio": "2026-03-09T09:00:00",
            "cliente_nombre": "Cliente Publico",
            "cliente_telefono": "3010000000",
        },
    )
    assert reserva.status_code == 201
    assert reserva.json()["cita"]["servicio_id"] == seed_data["servicio_id"]

    doble = client.post(
        f"/agenda/publica/{seed_data['negocio_slug']}/reservar",
        json={
            "servicio_id": seed_data["servicio_id"],
            "fecha_inicio": "2026-03-09T09:00:00",
            "cliente_nombre": "Otro Cliente",
        },
    )
    assert doble.status_code == 409

