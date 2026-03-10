"""Router de Equipos."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.equipo import Equipo
from app.models.campeonato import Campeonato
from app.schemas.equipo import EquipoCreate, EquipoResponse, EquipoUpdate
from app.core.dependencies import (
    require_authenticated,
    require_directivo_campeonato
)

router = APIRouter(prefix="/equipos", tags=["Equipos"])


@router.post(
    "/",
    response_model=EquipoResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_directivo_campeonato)]
)
async def crear_equipo(
    equipo: EquipoCreate,
    db: AsyncSession = Depends(get_db)
):
    """Crear un nuevo equipo. Solo DirectivoCampeonato, Admin o SuperAdmin."""
    # Verificar que el campeonato existe
    campeonato = (await db.execute(
        select(Campeonato).where(Campeonato.id == equipo.campeonato_id)
    )).scalar_one_or_none()

    if not campeonato:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campeonato no encontrado"
        )

    # Verificar que no exista un equipo con el mismo nombre en ese campeonato
    existente = (await db.execute(
        select(Equipo).where(
            Equipo.nombre == equipo.nombre,
            Equipo.campeonato_id == equipo.campeonato_id
        )
    )).scalar_one_or_none()

    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un equipo con ese nombre en este campeonato"
        )

    db_equipo = Equipo(**equipo.model_dump())
    db.add(db_equipo)
    await db.commit()
    await db.refresh(db_equipo)
    return db_equipo


@router.get(
    "/",
    response_model=List[EquipoResponse],
    dependencies=[Depends(require_authenticated)]
)
async def listar_equipos(
    skip: int = 0,
    limit: int = 100,
    campeonato_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """Listar equipos. Filtro opcional por campeonato."""
    query = select(Equipo)
    if campeonato_id:
        query = query.where(Equipo.campeonato_id == campeonato_id)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get(
    "/{equipo_id}",
    response_model=EquipoResponse,
    dependencies=[Depends(require_authenticated)]
)
async def obtener_equipo(
    equipo_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Obtener un equipo por su ID."""
    equipo = (await db.execute(
        select(Equipo).where(Equipo.id == equipo_id)
    )).scalar_one_or_none()

    if not equipo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Equipo no encontrado"
        )
    return equipo


@router.put(
    "/{equipo_id}",
    response_model=EquipoResponse,
    dependencies=[Depends(require_directivo_campeonato)]
)
async def actualizar_equipo(
    equipo_id: int,
    equipo_update: EquipoUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Actualizar un equipo."""
    db_equipo = (await db.execute(
        select(Equipo).where(Equipo.id == equipo_id)
    )).scalar_one_or_none()

    if not db_equipo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Equipo no encontrado"
        )

    update_data = equipo_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_equipo, field, value)

    await db.commit()
    await db.refresh(db_equipo)
    return db_equipo


@router.delete(
    "/{equipo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_directivo_campeonato)]
)
async def eliminar_equipo(
    equipo_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Eliminar un equipo."""
    db_equipo = (await db.execute(
        select(Equipo).where(Equipo.id == equipo_id)
    )).scalar_one_or_none()

    if not db_equipo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Equipo no encontrado"
        )

    await db.delete(db_equipo)
    await db.commit()
    return None
