"""Schemas de EventoPartido."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

TIPOS_VALIDOS = ["Gol", "TarjetaAmarilla", "TarjetaRoja", "Cambio"]


class JugadorResumen(BaseModel):
    """Resumen de jugador para anidar en respuestas."""
    id: int
    nombres: str
    apellidos: str

    class Config:
        """Crear desde atributos de objetos ORM."""
        from_attributes = True


class EquipoResumen(BaseModel):
    """Resumen de equipo para anidar en respuestas."""
    id: int
    nombre: str

    class Config:
        """Crear desde atributos de objetos ORM."""
        from_attributes = True


class EventoPartidoBase(BaseModel):
    """Esquema base para EventoPartido."""
    partido_id: int
    jugador_id: int
    equipo_id: int
    tipo: str = Field(
        ..., description="Gol, TarjetaAmarilla, TarjetaRoja, Cambio")
    minuto: Optional[int] = Field(
        None, ge=1, le=120, description="Minuto del evento")
    jugador_sale_id: Optional[int] = Field(
        None, description="Solo requerido cuando tipo es Cambio"
    )


class EventoPartidoCreate(EventoPartidoBase):
    """Esquema para crear un EventoPartido."""


class EventoPartidoUpdate(BaseModel):
    """Esquema para actualizar un EventoPartido."""
    minuto: Optional[int] = Field(None, ge=1, le=120)
    jugador_sale_id: Optional[int] = None


class EventoPartidoResponse(EventoPartidoBase):
    """Esquema de respuesta simple con IDs."""
    id: int
    created_at: datetime

    class Config:
        """Crear desde atributos de objetos ORM."""
        from_attributes = True


class EventoPartidoDetalleResponse(BaseModel):
    """Esquema de respuesta enriquecido con nombres."""
    id: int
    partido_id: int
    tipo: str
    minuto: Optional[int]
    created_at: datetime
    jugador: JugadorResumen
    jugador_sale: Optional[JugadorResumen] = None  # Solo para cambios
    equipo: EquipoResumen

    class Config:
        """Crear desde atributos de objetos ORM."""
        from_attributes = True
