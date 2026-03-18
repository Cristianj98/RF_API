"""Schemas de ActaPartido."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


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
    """Esquema de respuesta para ActaPartido."""
    id: int
    created_at: datetime

    class Config:
        """Clase de configuración para ActaPartidoResponse."""
        from_attributes = True
