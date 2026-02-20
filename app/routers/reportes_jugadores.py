"""Router de Reportes de Jugadores."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.campeonato import Campeonato
from app.models.reporte_jugador import ReporteJugador
from app.models.usuario import Usuario
from app.schemas.reporte_jugador import (
    ReporteJugadorCreate,
    ReporteJugadorResponse,
    ReporteJugadorUpdate,
)

router = APIRouter(prefix="/reportes", tags=["Reportes de Jugadores"])


@router.post(
    "/",
    response_model=ReporteJugadorResponse,
    status_code=status.HTTP_201_CREATED
)
async def crear_reporte_jugador(
    reporte: ReporteJugadorCreate,
    db: AsyncSession = Depends(get_db)
):
    """Crear un nuevo reporte de jugador."""
    # Verificar que el jugador existe
    jugador = (await db.execute(
        select(Usuario).where(Usuario.id == reporte.jugador_id)
    )).scalar_one_or_none()

    if not jugador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Jugador no encontrado"
        )

    # Verificar si el campeonato existe
    campeonato = (await db.execute(
        select(Campeonato).where(Campeonato.id == reporte.campeonato_id)
    )).scalar_one_or_none()

    if not campeonato:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campeonato no encontrado"
        )

    db_reporte = ReporteJugador(**reporte.model_dump())
    db.add(db_reporte)
    await db.commit()
    await db.refresh(db_reporte)
    return db_reporte


@router.get("/", response_model=List[ReporteJugadorResponse])
async def listar_reportes(
    skip: int = 0,
    limit: int = 100,
    jugador_id: int | None = None,
    campeonato_id: int | None = None,
    db: AsyncSession = Depends(get_db)
):
    """Listar reportes de jugadores con filtros opcionales."""
    query = select(ReporteJugador)

    if jugador_id is not None:
        query = query.where(ReporteJugador.jugador_id == jugador_id)

    if campeonato_id is not None:
        query = query.where(ReporteJugador.campeonato_id == campeonato_id)

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{reporte_id}", response_model=ReporteJugadorResponse)
async def obtener_reporte(
    reporte_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Obtener un reporte por ID."""
    reporte = (await db.execute(
        select(ReporteJugador).where(ReporteJugador.id == reporte_id)
    )).scalar_one_or_none()

    if not reporte:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reporte no encontrado"
        )
    return reporte


@router.put("/{reporte_id}", response_model=ReporteJugadorResponse)
async def actualizar_reporte(
    reporte_id: int,
    reporte_update: ReporteJugadorUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Actualizar un reporte."""
    result = await db.execute(
        select(ReporteJugador).where(ReporteJugador.id == reporte_id)
    )
    db_reporte = result.scalar_one_or_none()

    if not db_reporte:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reporte no encontrado"
        )

    # Actualizar solo campos no nulos
    update_data = reporte_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_reporte, field, value)

    await db.commit()
    await db.refresh(db_reporte)
    return db_reporte


@router.delete("/{reporte_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_reporte(
    reporte_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Eliminar un reporte."""
    result = await db.execute(
        select(ReporteJugador).where(ReporteJugador.id == reporte_id)
    )
    db_reporte = result.scalar_one_or_none()

    if not db_reporte:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reporte no encontrado"
        )

    await db.delete(db_reporte)
    await db.commit()
    return None
