"""Router de Jugadores en Equipos."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.jugador_equipo import JugadorEquipo
from app.models.usuario import Usuario
from app.models.equipo import Equipo
from app.schemas.jugador_directiva import (
    JugadorEquipoCreate,
    JugadorEquipoUpdate,
    JugadorEquipoResponse
)
from app.core.dependencies import (
    require_authenticated,
    require_directivo_campeonato
)

router = APIRouter(prefix="/jugadores-equipos", tags=["Jugadores en Equipos"])


@router.post(
    "/",
    response_model=JugadorEquipoResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_directivo_campeonato)]
)
async def asignar_jugador(
    datos: JugadorEquipoCreate,
    db: AsyncSession = Depends(get_db)
):
    """Asignar un jugador (usuario) a un equipo."""
    # Verificar que el usuario existe y tiene rol Jugador
    usuario = (await db.execute(
        select(Usuario).where(Usuario.id == datos.usuario_id)
    )).scalar_one_or_none()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    if usuario.rol != "Jugador":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario no tiene rol de Jugador"
        )

    # Verificar que el equipo existe
    equipo = (await db.execute(
        select(Equipo).where(Equipo.id == datos.equipo_id)
    )).scalar_one_or_none()

    if not equipo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Equipo no encontrado"
        )

    # Verificar que el jugador no esté ya en ese equipo
    existente = (await db.execute(
        select(JugadorEquipo).where(
            JugadorEquipo.usuario_id == datos.usuario_id,
            JugadorEquipo.equipo_id == datos.equipo_id
        )
    )).scalar_one_or_none()

    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El jugador ya está asignado a este equipo"
        )

    db_jugador = JugadorEquipo(**datos.model_dump())
    db.add(db_jugador)
    await db.commit()
    await db.refresh(db_jugador)
    return db_jugador


@router.get(
    "/equipo/{equipo_id}",
    response_model=List[JugadorEquipoResponse],
    dependencies=[Depends(require_authenticated)]
)
async def listar_jugadores_equipo(
    equipo_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Listar todos los jugadores de un equipo."""
    result = await db.execute(
        select(JugadorEquipo).where(JugadorEquipo.equipo_id == equipo_id)
    )
    return result.scalars().all()


@router.put(
    "/{jugador_equipo_id}",
    response_model=JugadorEquipoResponse,
    dependencies=[Depends(require_directivo_campeonato)]
)
async def actualizar_jugador_equipo(
    jugador_equipo_id: int,
    datos: JugadorEquipoUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Actualizar número de camiseta o posición de un jugador."""
    db_jugador = (await db.execute(
        select(JugadorEquipo).where(JugadorEquipo.id == jugador_equipo_id)
    )).scalar_one_or_none()

    if not db_jugador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro no encontrado"
        )

    update_data = datos.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_jugador, field, value)

    await db.commit()
    await db.refresh(db_jugador)
    return db_jugador


@router.delete(
    "/{jugador_equipo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_directivo_campeonato)]
)
async def remover_jugador_equipo(
    jugador_equipo_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Remover un jugador de un equipo."""
    db_jugador = (await db.execute(
        select(JugadorEquipo).where(JugadorEquipo.id == jugador_equipo_id)
    )).scalar_one_or_none()

    if not db_jugador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro no encontrado"
        )

    await db.delete(db_jugador)
    await db.commit()
    return None
