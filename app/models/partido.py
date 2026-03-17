"""Modelo de Partido."""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Partido(Base):
    """Modelo de datos para un partido de fútbol."""
    __tablename__ = "partidos"

    id = Column(Integer, primary_key=True, index=True)
    campeonato_id = Column(Integer, ForeignKey(
        "campeonatos.id"), nullable=False)
    equipo_local_id = Column(Integer, ForeignKey("equipos.id"), nullable=False)
    equipo_visitante_id = Column(
        Integer, ForeignKey("equipos.id"), nullable=False)
    jornada = Column(Integer, nullable=False)
    fecha_hora = Column(DateTime(timezone=True), nullable=True)
    lugar = Column(String, nullable=True)
    estado = Column(String, default="Programado")
    # Programado, En curso, Finalizado, Suspendido
    goles_local = Column(Integer, default=0)
    goles_visitante = Column(Integer, default=0)
    observaciones = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))

    campeonato = relationship("Campeonato", back_populates="partidos")
    equipo_local = relationship(
        "Equipo", foreign_keys=[
            equipo_local_id], back_populates="partidos_local")
    equipo_visitante = relationship(
        "Equipo", foreign_keys=[
            equipo_visitante_id], back_populates="partidos_visitante")
    acta = relationship("ActaPartido", back_populates="partido")
    eventos = relationship("EventoPartido", back_populates="partido")
