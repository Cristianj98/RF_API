"""Schemas de autenticación."""
from pydantic import BaseModel, EmailStr, Field


class UserLogin(BaseModel):
    """Schema para login."""
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)


class UserRegister(BaseModel):
    """Schema para registro de usuario."""
    nombres: str = Field(..., min_length=1, max_length=100)
    apellidos: str = Field(..., min_length=1, max_length=100)
    cedula: str = Field(..., min_length=10, max_length=10)
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=128)
    email: EmailStr
    telefono: str | None = None
    rol: str = Field(default="Jugador")


class Token(BaseModel):
    """Schema de respuesta de token."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Datos dentro del token."""
    username: str | None = None
    user_id: int | None = None
