"""Schemas de campeonato."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class CampeonatoBase(BaseModel):
    """Esquema base para Campeonato."""
    nombre: str = Field(..., min_length=1, max_length=100)
    descripcion: str = Field(..., min_length=1, max_length=1000)
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    canton: Optional[str] = Field(None, min_length=1, max_length=100)
    parroquia: Optional[str] = Field(None, min_length=1, max_length=100)
    estado: Optional[str] = Field(
        default="activo",
        description="activo, suspendido, finalizado"
    )


class CampeonatoCreate(CampeonatoBase):
    """Esquema para crear un Campeonato."""


class CampeonatoUpdate(CampeonatoBase):
    """Esquema para actualizar un Campeonato."""
    nombre: Optional[str] = Field(None, min_length=1, max_length=200)
    descripcion: Optional[str] = Field(None, max_length=1000)
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    canton: Optional[str] = None
    parroquia: Optional[str] = None
    estado: Optional[str] = None


class CampeonatoResponse(CampeonatoBase):
    """Esquema de respuesta para Campeonato."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Clase de configuración para CampeonatoResponse."""
        from_attributes = True
