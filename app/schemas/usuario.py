"""Schemas de Usuario."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UsuarioBase(BaseModel):
    """Schema base de Usuario."""
    nombres: str = Field(..., min_length=1, max_length=100)
    apellidos: str = Field(..., min_length=1, max_length=100)
    cedula: str = Field(..., min_length=1, max_length=20)
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    telefono: Optional[str] = None
    direction: Optional[str] = None
    canton: Optional[str] = None
    parroquia: Optional[str] = None
    barrio: Optional[str] = None
    rol: str = Field(
        ...,
        description=(
            "Jugador, Directivo, DirectivoCampeonato, "
            "Administrador, SuperAdministrador"
        )
    )


class UsuarioCreate(UsuarioBase):
    """Schema para crear Usuario."""
    password: str = Field(..., min_length=6, max_length=128)


class UsuarioUpdate(BaseModel):
    """Schema para actualizar Usuario."""
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    direction: Optional[str] = None


class UsuarioResponse(UsuarioBase):
    """Schema de respuesta de Usuario."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Clase de configuración para UsuarioResponse."""
        from_attributes = True
