"""Modelo de Reportes de Jugadores."""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class ReporteJugador(Base):
    """Modelo de reportes de jugadores con PDF."""

    __tablename__ = "reportes_jugadores"

    id = Column(Integer, primary_key=True, index=True)
    jugador_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    campeonato_id = Column(Integer, ForeignKey(
        "campeonatos.id"), nullable=False)
    titulo = Column(String, nullable=False)
    descripcion = Column(Text, nullable=True)
    archivo_pdf_url = Column(String, nullable=True)  # Ruta del PDF
    # Ficha técnica, Informe, etc.
    tipo_reporte = Column(String, nullable=True)
    fecha_reporte = Column(
        DateTime, default=lambda: datetime.now(timezone.utc))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))

    jugador = relationship("Usuario", back_populates="reportes")
    campeonato = relationship("Campeonato", back_populates="reportes")
