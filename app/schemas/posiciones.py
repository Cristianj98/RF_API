"""Schemas de Posicion."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


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
    """Esquema de respuesta para Posicion."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Clase de configuración para PosicionResponse."""
        from_attributes = True
