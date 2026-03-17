"""Modelo de Posiciones."""
from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    String
)
from sqlalchemy.orm import relationship
from app.database import Base


class Posicion(Base):
    """Tabla de posiciones por campeonato."""
    __tablename__ = "posiciones"

    id = Column(Integer, primary_key=True, index=True)
    campeonato_id = Column(Integer, ForeignKey(
        "campeonatos.id"), nullable=False)
    equipo_id = Column(Integer, ForeignKey("equipos.id"), nullable=False)
    serie = Column(String, nullable=True)  # Serie A, Serie B
    partidos_jugados = Column(Integer, default=0)
    ganados = Column(Integer, default=0)
    empatados = Column(Integer, default=0)
    perdidos = Column(Integer, default=0)
    goles_favor = Column(Integer, default=0)
    goles_contra = Column(Integer, default=0)
    puntos = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))

    # Relaciones
    campeonato = relationship("Campeonato", back_populates="posiciones")
    equipo = relationship("Equipo", back_populates="posicion")
