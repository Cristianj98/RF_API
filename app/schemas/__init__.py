"""Schemas de la aplicación."""
from app.schemas.usuario import (
    UsuarioBase,
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioResponse
)
from app.schemas.campeonato import (
    CampeonatoBase,
    CampeonatoCreate,
    CampeonatoUpdate,
    CampeonatoResponse
)
from app.schemas.reporte_jugador import (
    ReporteJugadorBase,
    ReporteJugadorCreate,
    ReporteJugadorUpdate,
    ReporteJugadorResponse
)

__all__ = [
    "UsuarioBase",
    "UsuarioCreate",
    "UsuarioUpdate",
    "UsuarioResponse",
    "CampeonatoBase",
    "CampeonatoCreate",
    "CampeonatoUpdate",
    "CampeonatoResponse",
    "ReporteJugadorBase",
    "ReporteJugadorCreate",
    "ReporteJugadorUpdate",
    "ReporteJugadorResponse",
]
