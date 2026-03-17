"""Modelo de EstadisticasJugador."""
from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from app.database import Base


class EstadisticaJugador(Base):
    """Estadísticas de un jugador por campeonato."""
    __tablename__ = "estadisticas_jugadores"

    id = Column(Integer, primary_key=True, index=True)
    jugador_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    campeonato_id = Column(Integer, ForeignKey(
        "campeonatos.id"), nullable=False)
    goles = Column(Integer, default=0)
    asistencias = Column(Integer, default=0)
    tarjetas_amarillas = Column(Integer, default=0)
    tarjetas_rojas = Column(Integer, default=0)
    partidos_jugados = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))

    # Relaciones
    jugador = relationship("Usuario", back_populates="estadisticas")
    campeonato = relationship(
        "Campeonato", back_populates="estadisticas_jugadores")
