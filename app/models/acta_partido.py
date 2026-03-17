"""Modelo de ActaPartido."""
from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    Boolean
)
from sqlalchemy.orm import relationship
from app.database import Base


class ActaPartido(Base):
    """Nómina de jugadores convocados por partido."""
    __tablename__ = "acta_partido"

    id = Column(Integer, primary_key=True, index=True)
    partido_id = Column(Integer, ForeignKey("partidos.id"), nullable=False)
    jugador_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    equipo_id = Column(Integer, ForeignKey("equipos.id"), nullable=False)
    convocado = Column(Boolean, default=True)
    titular = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(timezone.utc))

    # Relaciones
    partido = relationship("Partido", back_populates="acta")
    jugador = relationship("Usuario", back_populates="actas")
    equipo = relationship("Equipo", back_populates="actas")
