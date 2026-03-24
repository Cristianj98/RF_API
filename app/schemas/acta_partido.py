"""Schemas de ActaPartido."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class JugadorResumen(BaseModel):
    """Resumen de jugador para anidar en respuestas."""
    id: int
    nombres: str
    apellidos: str

    class Config:
        """Permite crear el modelo a partir de objetos con atributos."""
        from_attributes = True


class EquipoResumen(BaseModel):
    """Resumen de equipo para anidar en respuestas."""
    id: int
    nombre: str

    class Config:
        """Permite crear el modelo a partir de objetos con atributos."""
        from_attributes = True


class ActaPartidoBase(BaseModel):
    """Esquema base para ActaPartido."""
    partido_id: int
    jugador_id: int
    equipo_id: int
    convocado: Optional[bool] = True
    titular: Optional[bool] = False


class ActaPartidoCreate(ActaPartidoBase):
    """Esquema para crear un registro en el acta."""


class ActaPartidoUpdate(BaseModel):
    """Esquema para actualizar un registro del acta."""
    convocado: Optional[bool] = None
    titular: Optional[bool] = None


class ActaPartidoResponse(ActaPartidoBase):
    """Esquema de respuesta simple con IDs."""
    id: int
    created_at: datetime

    class Config:
        """Permite crear el modelo a partir de objetos con atributos."""
        from_attributes = True


class ActaPartidoDetalleResponse(BaseModel):
    """Esquema de respuesta enriquecido con nombres."""
    id: int
    partido_id: int
    convocado: bool
    titular: bool
    created_at: datetime
    jugador: JugadorResumen
    equipo: EquipoResumen

    class Config:
        """Permite crear el modelo a partir de objetos con atributos."""
        from_attributes = True
