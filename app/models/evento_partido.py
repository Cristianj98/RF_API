"""Modelo de EventoPartido."""
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


class EventoPartido(Base):
    """Goles, tarjetas y cambios de un partido."""
    __tablename__ = "eventos_partido"

    id = Column(Integer, primary_key=True, index=True)
    partido_id = Column(Integer, ForeignKey("partidos.id"), nullable=False)
    jugador_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    equipo_id = Column(Integer, ForeignKey("equipos.id"), nullable=False)
    # Gol, TarjetaAmarilla, TarjetaRoja, Cambio
    tipo = Column(String, nullable=False)
    minuto = Column(Integer, nullable=True)
    jugador_sale_id = Column(Integer, ForeignKey(
        "usuarios.id"), nullable=True)  # Solo para cambios
    created_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(timezone.utc))

    # Relaciones
    partido = relationship(
        "Partido", back_populates="eventos")
    jugador = relationship(
        "Usuario", foreign_keys=[
            jugador_id], back_populates="eventos")
    jugador_sale = relationship("Usuario", foreign_keys=[jugador_sale_id])
    equipo = relationship("Equipo", back_populates="eventos")
