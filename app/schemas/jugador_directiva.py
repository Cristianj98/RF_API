"""Schemas de JugadorEquipo y DirectivaEquipo."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


# ── JugadorEquipo ──────────────────────────────────────────────

class JugadorEquipoCreate(BaseModel):
    """Schema para asignar un jugador a un equipo."""
    usuario_id: int
    equipo_id: int
    numero_camiseta: Optional[int] = None
    posicion: Optional[str] = None


class JugadorEquipoUpdate(BaseModel):
    """Schema para actualizar datos del jugador en el equipo."""
    numero_camiseta: Optional[int] = None
    posicion: Optional[str] = None


class JugadorEquipoResponse(BaseModel):
    """Schema de respuesta de JugadorEquipo."""
    id: int
    usuario_id: int
    equipo_id: int
    numero_camiseta: Optional[int]
    posicion: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


# ── DirectivaEquipo ────────────────────────────────────────────

SUBROLES_VALIDOS = ["Presidente", "Vicepresidente", "Secretario", "Vocal"]


class DirectivaEquipoCreate(BaseModel):
    """Schema para asignar un directivo a un equipo."""
    equipo_id: int
    usuario_id: int
    subrol: Optional[str] = None

    def model_post_init(self, __context):
        if self.subrol and self.subrol not in SUBROLES_VALIDOS:
            raise ValueError(
                f"Subrol inválido. Debe ser uno de: {SUBROLES_VALIDOS}"
            )


class DirectivaEquipoUpdate(BaseModel):
    """Schema para actualizar el subrol del directivo."""
    subrol: Optional[str] = None

    def model_post_init(self, __context):
        if self.subrol and self.subrol not in SUBROLES_VALIDOS:
            raise ValueError(
                f"Subrol inválido. Debe ser uno de: {SUBROLES_VALIDOS}"
            )


class DirectivaEquipoResponse(BaseModel):
    """Schema de respuesta de DirectivaEquipo."""
    id: int
    equipo_id: int
    usuario_id: int
    subrol: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}
