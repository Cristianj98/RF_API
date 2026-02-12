"""Modelo de Jugadores."""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database import Base


class Usuario(Base):
    """"Modelo de Usuario."""
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombres = Column(String, nullable=False)
    apellidos = Column(String, nullable=False)
    cedula = Column(String, unique=True, nullable=False, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    telefono = Column(String, nullable=True)
    direction = Column(String, nullable=True)
    canton = Column(String, nullable=True)
    parroquia = Column(String, nullable=True)
    barrio = Column(String, nullable=True)
    rol = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))

    reportes = relationship("ReporteJugador", back_populates="jugador")
