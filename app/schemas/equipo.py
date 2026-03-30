"""Schemas de Equipo."""
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel


class EquipoBase(BaseModel):
    """Campos base compartidos."""
    nombre: str
    logo_url: Optional[str] = None
    campeonato_id: int
    fundacion: Optional[datetime] = None


class EquipoCreate(EquipoBase):
    """Schema para crear un equipo."""


class EquipoUpdate(BaseModel):
    """Schema para actualizar un equipo (todos opcionales)."""
    nombre: Optional[str] = None
    logo_url: Optional[str] = None
    fundacion: Optional[date] = None


class EquipoResponse(EquipoBase):
    """Schema de respuesta con campos de BD."""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PresignedUrlRequest(BaseModel):
    """Request para generar una presigned URL."""
    filename: str
    content_type: str


class PresignedUrlResponse(BaseModel):
    """Respuesta con las URLs para subir el logo."""
    upload_url: str
    public_url: str