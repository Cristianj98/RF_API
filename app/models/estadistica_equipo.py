"""Modelo de EstadisticasEquipo."""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class EstadisticaEquipo(Base):
    """Estadísticas de un equipo por campeonato."""
    __tablename__ = "estadisticas_equipos"

    id = Column(Integer, primary_key=True, index=True)
    equipo_id = Column(Integer, ForeignKey("equipos.id"), nullable=False)
    campeonato_id = Column(Integer, ForeignKey(
        "campeonatos.id"), nullable=False)
    goles_favor = Column(Integer, default=0)
    goles_contra = Column(Integer, default=0)
    partidos_jugados = Column(Integer, default=0)
    victorias = Column(Integer, default=0)
    empates = Column(Integer, default=0)
    derrotas = Column(Integer, default=0)
    puntos = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))

    # Relaciones
    equipo = relationship("Equipo", back_populates="estadisticas")
    campeonato = relationship(
        "Campeonato", back_populates="estadisticas_equipos")
