"""Schemas de EstadisticaEquipo."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class EquipoResumen(BaseModel):
    """Enriquecedor de JSON"""
    id: int
    nombre: str
    logo_url: Optional[str] = None

    class Config:
        """Crear desde atributos de objetos ORM."""
        from_attributes = True


class CampeonatoResumen(BaseModel):
    """Atributos para nombres de campeonatos"""
    id: int
    nombre: str

    class Config:
        """Crear desde atributos de objetos ORM."""
        from_attributes = True


class EstadisticaEquipoBase(BaseModel):
    """Esquema base para EstadisticaEquipo."""
    equipo_id: int
    campeonato_id: int
    goles_favor: Optional[int] = Field(default=0, ge=0)
    goles_contra: Optional[int] = Field(default=0, ge=0)
    partidos_jugados: Optional[int] = Field(default=0, ge=0)
    victorias: Optional[int] = Field(default=0, ge=0)
    empates: Optional[int] = Field(default=0, ge=0)
    derrotas: Optional[int] = Field(default=0, ge=0)
    puntos: Optional[int] = Field(default=0, ge=0)


class EstadisticaEquipoCreate(EstadisticaEquipoBase):
    """Esquema para crear una EstadisticaEquipo."""


class EstadisticaEquipoUpdate(BaseModel):
    """Esquema para actualizar una EstadisticaEquipo."""
    goles_favor: Optional[int] = Field(None, ge=0)
    goles_contra: Optional[int] = Field(None, ge=0)
    partidos_jugados: Optional[int] = Field(None, ge=0)
    victorias: Optional[int] = Field(None, ge=0)
    empates: Optional[int] = Field(None, ge=0)
    derrotas: Optional[int] = Field(None, ge=0)
    puntos: Optional[int] = Field(None, ge=0)


class EstadisticaEquipoResponse(EstadisticaEquipoBase):
    """Esquema de respuesta simple con IDs."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Crear desde atributos de objetos ORM."""
        from_attributes = True


class EstadisticaEquipoDetalleResponse(BaseModel):
    """Esquema de respuesta enriquecido."""
    id: int
    goles_favor: int
    goles_contra: int
    partidos_jugados: int
    victorias: int
    empates: int
    derrotas: int
    puntos: int
    equipo: EquipoResumen
    campeonato: CampeonatoResumen
    created_at: datetime
    updated_at: datetime

    class Config:
        """Crear desde atributos de objetos ORM."""
        from_attributes = True
