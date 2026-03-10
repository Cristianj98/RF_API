"""Modelo de equipo."""
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Equipo(Base):
    """Clase que define el modelo equipo."""

    __tablename__ = "equipos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    logo_url = Column(String, nullable=True)
    campeonato_id = Column(Integer, ForeignKey(
        "campeonatos.id"), nullable=False)
    fundacion = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))

    campeonato = relationship("Campeonato", back_populates="equipos")
    jugadores = relationship("JugadorEquipo", back_populates="equipo")
    directiva = relationship("DirectivaEquipo", back_populates="equipo")
