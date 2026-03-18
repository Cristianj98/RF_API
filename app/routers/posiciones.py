"""Router de Posiciones."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.posicion import Posicion
from app.models.campeonato import Campeonato
from app.models.equipo import Equipo
from app.schemas.posiciones import (
    PosicionCreate,
    PosicionResponse,
    PosicionUpdate
)
from app.core.dependencies import require_authenticated, require_admin

router = APIRouter(prefix="/posiciones", tags=["Posiciones"])


@router.post(
    "/",
    response_model=PosicionResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)]
)
async def crear_posicion(
    datos: PosicionCreate,
    db: AsyncSession = Depends(get_db)
):
    """Crear registro de posición para un equipo en un campeonato."""
    # Verificar que el campeonato existe
    campeonato = (await db.execute(
        select(Campeonato).where(Campeonato.id == datos.campeonato_id)
    )).scalar_one_or_none()
    if not campeonato:
        raise HTTPException(status_code=404, detail="Campeonato no encontrado")

    # Verificar que el equipo existe y pertenece al campeonato
    equipo = (await db.execute(
        select(Equipo).where(
            Equipo.id == datos.equipo_id,
            Equipo.campeonato_id == datos.campeonato_id
        )
    )).scalar_one_or_none()
    if not equipo:
        raise HTTPException(
            status_code=404,
            detail="Equipo no encontrado o no pertenece al campeonato"
        )

    # Verificar que no exista ya una posición para ese equipo en ese campeonato
    existente = (await db.execute(
        select(Posicion).where(
            Posicion.equipo_id == datos.equipo_id,
            Posicion.campeonato_id == datos.campeonato_id
        )
    )).scalar_one_or_none()
    if existente:
        raise HTTPException(
            status_code=400,
            detail="El equipo ya tiene registrada una posición"
        )

    db_posicion = Posicion(**datos.model_dump())
    db.add(db_posicion)
    await db.commit()
    await db.refresh(db_posicion)
    return db_posicion


@router.get(
    "/campeonato/{campeonato_id}",
    response_model=List[PosicionResponse],
    dependencies=[Depends(require_authenticated)]
)
async def tabla_posiciones(
    campeonato_id: int,
    serie: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Obtener tabla de posiciones de un campeonato ordenada por puntos."""
    campeonato = (await db.execute(
        select(Campeonato).where(Campeonato.id == campeonato_id)
    )).scalar_one_or_none()
    if not campeonato:
        raise HTTPException(status_code=404, detail="Campeonato no encontrado")

    query = select(Posicion).where(Posicion.campeonato_id == campeonato_id)
    if serie:
        query = query.where(Posicion.serie == serie)

    # Ordenar por puntos desc, luego por diferencia de goles desc
    query = query.order_by(
        Posicion.puntos.desc(),
        (Posicion.goles_favor - Posicion.goles_contra).desc()
    )

    result = await db.execute(query)
    return result.scalars().all()


@router.get(
    "/{posicion_id}",
    response_model=PosicionResponse,
    dependencies=[Depends(require_authenticated)]
)
async def obtener_posicion(
    posicion_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Obtener posición por ID."""
    posicion = (await db.execute(
        select(Posicion).where(Posicion.id == posicion_id)
    )).scalar_one_or_none()
    if not posicion:
        raise HTTPException(status_code=404, detail="Posición no encontrada")
    return posicion


@router.put(
    "/{posicion_id}",
    response_model=PosicionResponse,
    dependencies=[Depends(require_admin)]
)
async def actualizar_posicion(
    posicion_id: int,
    datos: PosicionUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Actualizar posición manualmente. Normalmente se actualiza automático."""
    db_posicion = (await db.execute(
        select(Posicion).where(Posicion.id == posicion_id)
    )).scalar_one_or_none()
    if not db_posicion:
        raise HTTPException(status_code=404, detail="Posición no encontrada")

    update_data = datos.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_posicion, field, value)

    await db.commit()
    await db.refresh(db_posicion)
    return db_posicion
