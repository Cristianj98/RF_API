"""Schemas de Reporte de Jugador."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ReporteJugadorBase(BaseModel):
    """Schema base de Reporte de Jugador."""
    jugador_id: int
    campeonato_id: int
    titulo: str = Field(..., min_length=1, max_length=200)
    descripcion: Optional[str] = Field(None, max_length=2000)
    tipo_reporte: Optional[str] = Field(
        None,
        description="Ficha técnica, Informe médico, Evaluación, etc."
    )


class ReporteJugadorCreate(ReporteJugadorBase):
    """Schema para crear Reporte de Jugador."""
    # archivo_pdf_url se manejará después cuando subamos archivos


class ReporteJugadorUpdate(BaseModel):
    """Schema para actualizar Reporte de Jugador."""
    titulo: Optional[str] = Field(None, min_length=1, max_length=200)
    descripcion: Optional[str] = Field(None, max_length=2000)
    tipo_reporte: Optional[str] = None
    archivo_pdf_url: Optional[str] = None


class ReporteJugadorResponse(ReporteJugadorBase):
    """Schema de respuesta de Reporte de Jugador."""
    id: int
    archivo_pdf_url: Optional[str] = None
    fecha_reporte: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        """Clase de configuración do Pydantic."""
        from_attributes = True
