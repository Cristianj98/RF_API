"""Schemas de Partido."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

ESTADOS_VALIDOS = ["Programado", "En curso", "Finalizado", "Suspendido"]


class CampeonatoResumen(BaseModel):
    """Resumen de campeonato para anidar en respuestas."""
    id: int
    nombre: str

    class Config:
        """Crear desde atributos de objetos ORM."""
        from_attributes = True


class EquipoResumen(BaseModel):
    """Resumen de equipo para anidar en respuestas."""
    id: int
    nombre: str
    logo_url: Optional[str] = None

    class Config:
        """Crear desde atributos de objetos ORM."""
        from_attributes = True


class PartidoBase(BaseModel):
    """Esquema base para Partido."""
    campeonato_id: int
    equipo_local_id: int
    equipo_visitante_id: int
    jornada: int = Field(..., ge=1, description="Número de jornada, mínimo 1")
    fecha_hora: Optional[datetime] = None
    lugar: Optional[str] = Field(None, min_length=1, max_length=200)
    estado: Optional[str] = Field(
        default="Programado",
        description="Programado, En curso, Finalizado, Suspendido"
    )
    goles_local: Optional[int] = Field(default=0, ge=0)
    goles_visitante: Optional[int] = Field(default=0, ge=0)
    observaciones: Optional[str] = Field(None, max_length=1000)


class PartidoCreate(PartidoBase):
    """Esquema para crear un Partido."""


class PartidoUpdate(BaseModel):
    """Esquema para actualizar un Partido."""
    fecha_hora: Optional[datetime] = None
    lugar: Optional[str] = Field(None, min_length=1, max_length=200)
    estado: Optional[str] = Field(
        None, description="Programado, En curso, Finalizado, Suspendido")
    goles_local: Optional[int] = Field(None, ge=0)
    goles_visitante: Optional[int] = Field(None, ge=0)
    observaciones: Optional[str] = Field(None, max_length=1000)
    jornada: Optional[int] = Field(None, ge=1)


class PartidoResponse(PartidoBase):
    """Esquema de respuesta simple con IDs."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Crear desde atributos de objetos ORM."""
        from_attributes = True


class PartidoDetalleResponse(BaseModel):
    """Esquema de respuesta enriquecido con nombres en lugar de IDs."""
    id: int
    jornada: int
    fecha_hora: Optional[datetime]
    lugar: Optional[str]
    estado: str
    goles_local: int
    goles_visitante: int
    observaciones: Optional[str]
    campeonato: CampeonatoResumen
    equipo_local: EquipoResumen
    equipo_visitante: EquipoResumen
    created_at: datetime
    updated_at: datetime

    class Config:
        """Crear desde atributos de objetos ORM."""
        from_attributes = True
