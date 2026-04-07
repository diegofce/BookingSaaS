"""Simple notification simulation service."""

from app.models.cita import Cita
from app.models.cliente import Cliente
from app.models.servicio import Servicio


class NotificationService:

    @staticmethod
    def send_appointment_confirmation(cita: Cita, cliente: Cliente, servicio: Servicio) -> None:
        # Simulación de envío; en producción se integra email/SMS/WhatsApp.
        print(
            f"[NOTIFY][CONFIRMACION] cita_id={cita.id} cliente={cliente.nombre} "
            f"servicio={servicio.nombre} inicio={cita.fecha_inicio.isoformat()}"
        )

    @staticmethod
    def send_appointment_reminder(cita: Cita, cliente: Cliente, servicio: Servicio) -> None:
        # Simulación de envío; en producción se integra un job scheduler.
        print(
            f"[NOTIFY][RECORDATORIO] cita_id={cita.id} cliente={cliente.nombre} "
            f"servicio={servicio.nombre} inicio={cita.fecha_inicio.isoformat()}"
        )

