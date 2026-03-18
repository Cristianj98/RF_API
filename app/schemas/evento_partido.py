"""Schemas de EventoPartido."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

TIPOS_VALIDOS = ["Gol", "TarjetaAmarilla", "TarjetaRoja", "Cambio"]


class EventoPartidoBase(BaseModel):
    """Esquema base para EventoPartido."""
    partido_id: int
    jugador_id: int
    equipo_id: int
    tipo: str = Field(...,
                      description="Gol, TarjetaAmarilla, TarjetaRoja, Cambio")
    minuto: Optional[int] = Field(
        None, ge=1, le=120, description="Minuto del evento")
    jugador_sale_id: Optional[int] = Field(
        None,
        description="Solo requerido cuando tipo es Cambio"
    )


class EventoPartidoCreate(EventoPartidoBase):
    """Esquema para crear un EventoPartido."""


class EventoPartidoUpdate(BaseModel):
    """Esquema para actualizar un EventoPartido."""
    minuto: Optional[int] = Field(None, ge=1, le=120)
    jugador_sale_id: Optional[int] = None


class EventoPartidoResponse(EventoPartidoBase):
    """Esquema de respuesta para EventoPartido."""
    id: int
    created_at: datetime

    class Config:
        """Clase de configuración para EventoPartidoResponse."""
        from_attributes = True
