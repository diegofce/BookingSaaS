"""Schemas for the Calendly-style availability endpoint."""

from datetime import datetime, time

from pydantic import BaseModel, Field


class SlotResponse(BaseModel):
    """Represents a single time slot with its availability status."""

    hora_inicio: datetime
    hora_fin: datetime
    disponible: bool
