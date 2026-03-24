"""Schemas de EstadisticaJugador."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class JugadorResumen(BaseModel):
    """Descripción del jugador."""
    id: int
    nombres: str
    apellidos: str

    class Config:
        """Crear desde atributos de objetos ORM."""
        from_attributes = True


class EquipoResumen(BaseModel):
    """Descripción del equipo."""
    id: int
    nombre: str
    logo_url: Optional[str] = None

    class Config:
        """Crear desde atributos de objetos ORM."""
        from_attributes = True


class CampeonatoResumen(BaseModel):
    """Descripción del campeonato."""
    id: int
    nombre: str

    class Config:
        """Crear desde atributos de objetos ORM."""
        from_attributes = True


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
    """Esquema de respuesta simple con IDs."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Crear desde atributos de objetos ORM."""
        from_attributes = True


class EstadisticaJugadorDetalleResponse(BaseModel):
    """Esquema de respuesta enriquecido."""
    id: int
    goles: int
    asistencias: int
    tarjetas_amarillas: int
    tarjetas_rojas: int
    partidos_jugados: int
    jugador: JugadorResumen
    equipo: Optional[EquipoResumen] = None
    campeonato: CampeonatoResumen
    created_at: datetime
    updated_at: datetime

    class Config:
        """Crear desde atributos de objetos ORM."""
        from_attributes = True
