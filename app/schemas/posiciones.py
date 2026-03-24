"""Schemas de Posicion."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class EquipoResumen(BaseModel):
    """Resumen de equipo para anidar en respuestas."""
    id: int
    nombre: str
    logo_url: Optional[str] = None

    class Config:
        """Crear desde atributos de objetos ORM."""
        from_attributes = True


class CampeonatoResumen(BaseModel):
    """Crear desde atributos de objetos ORM."""
    id: int
    nombre: str

    class Config:
        """Crear desde atributos de objetos ORM."""
        from_attributes = True


class PosicionBase(BaseModel):
    """Esquema base para Posicion."""
    campeonato_id: int
    equipo_id: int
    serie: Optional[str] = Field(None, description="Serie A, Serie B")
    partidos_jugados: Optional[int] = Field(default=0, ge=0)
    ganados: Optional[int] = Field(default=0, ge=0)
    empatados: Optional[int] = Field(default=0, ge=0)
    perdidos: Optional[int] = Field(default=0, ge=0)
    goles_favor: Optional[int] = Field(default=0, ge=0)
    goles_contra: Optional[int] = Field(default=0, ge=0)
    puntos: Optional[int] = Field(default=0, ge=0)


class PosicionCreate(PosicionBase):
    """Esquema para crear una Posicion."""


class PosicionUpdate(BaseModel):
    """Esquema para actualizar una Posicion."""
    serie: Optional[str] = None
    partidos_jugados: Optional[int] = Field(None, ge=0)
    ganados: Optional[int] = Field(None, ge=0)
    empatados: Optional[int] = Field(None, ge=0)
    perdidos: Optional[int] = Field(None, ge=0)
    goles_favor: Optional[int] = Field(None, ge=0)
    goles_contra: Optional[int] = Field(None, ge=0)
    puntos: Optional[int] = Field(None, ge=0)


class PosicionResponse(PosicionBase):
    """Esquema de respuesta simple con IDs."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Crear desde atributos de objetos ORM."""
        from_attributes = True


class PosicionDetalleResponse(BaseModel):
    """Esquema de respuesta enriquecido para tabla de posiciones."""
    id: int
    serie: Optional[str]
    partidos_jugados: int
    ganados: int
    empatados: int
    perdidos: int
    goles_favor: int
    goles_contra: int
    puntos: int
    equipo: EquipoResumen
    campeonato: CampeonatoResumen
    created_at: datetime
    updated_at: datetime

    class Config:
        """Crear desde atributos de objetos ORM."""
        from_attributes = True
