"""Modelo de la relación entre directiva y equipo."""
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class DirectivaEquipo(Base):
    """Relación entre (usuario) y equipo."""

    __tablename__ = "directiva_equipos"

    id = Column(Integer, primary_key=True, index=True)
    equipo_id = Column(Integer, ForeignKey("equipos.id"), nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    subrol = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(timezone.utc))

    usuario = relationship("Usuario", back_populates="directivas")
    equipo = relationship("Equipo", back_populates="directiva")
