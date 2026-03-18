"""Schemas de EstadisticaJugador."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class EstadisticaJugadorBase(BaseModel):
    """Esquema base para EstadisticaJugador."""
    jugador_id: int
    campeonato_id: int
    goles: Optional[int] = Field(default=0, ge=0)
    asistencias: Optional[int] = Field(default=0, ge=0)
    tarjetas_amarillas: Optional[int] = Field(default=0, ge=0)
    tarjetas_rojas: Optional[int] = Field(default=0, ge=0)
    partidos_jugados: Optional[int] = Field(default=0, ge=0)


class EstadisticaJugadorCreate(EstadisticaJugadorBase):
    """Esquema para crear una EstadisticaJugador."""


class EstadisticaJugadorUpdate(BaseModel):
    """Esquema para actualizar una EstadisticaJugador."""
    goles: Optional[int] = Field(None, ge=0)
    asistencias: Optional[int] = Field(None, ge=0)
    tarjetas_amarillas: Optional[int] = Field(None, ge=0)
    tarjetas_rojas: Optional[int] = Field(None, ge=0)
    partidos_jugados: Optional[int] = Field(None, ge=0)


class EstadisticaJugadorResponse(EstadisticaJugadorBase):
    """Esquema de respuesta para EstadisticaJugador."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Clase de configuración para EstadisticaJugadorResponse."""
        from_attributes = True
