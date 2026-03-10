"""Modelo para relación entre jugador y equipo."""
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class JugadorEquipo(Base):
    """Relación entre Jugador y Equipo."""

    __tablename__ = "jugadores_equipos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    equipo_id = Column(Integer, ForeignKey("equipos.id"), nullable=False)
    dorsal = Column(Integer, nullable=True)
    posicion = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(timezone.utc))

    usuario = relationship("Usuario", back_populates="equipos")
    equipo = relationship("Equipo", back_populates="jugadores")
