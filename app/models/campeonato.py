""""Modelo de Campeonato."""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database import Base


class Campeonato(Base):
    """Modelo de Campeonatos"""

    __tablename__ = "campeonatos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    descripcion = Column(String, nullable=True)
    fecha_inicio = Column(DateTime(timezone=True), nullable=True)
    fecha_fin = Column(DateTime(timezone=True), nullable=True)
    canton = Column(String, nullable=True)
    parroquia = Column(String, nullable=True)
    estado = Column(String, default="activo")
    created_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))

    reportes = relationship("ReporteJugador", back_populates="campeonato")
    equipos = relationship("Equipo", back_populates="campeonato")
    partidos = relationship("Partido", back_populates="campeonato")
    posiciones = relationship("Posicion", back_populates="campeonato")
    estadisticas_jugadores = relationship(
        "EstadisticaJugador", back_populates="campeonato")
    estadisticas_equipos = relationship(
        "EstadisticaEquipo", back_populates="campeonato")
