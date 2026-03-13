"""Router de Directiva de Equipos."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.directiva_equipo import DirectivaEquipo
from app.models.usuario import Usuario
from app.models.equipo import Equipo
from app.schemas.jugador_directiva import (
    DirectivaEquipoCreate,
    DirectivaEquipoUpdate,
    DirectivaEquipoResponse
)
from app.core.dependencies import (
    require_authenticated,
    require_directivo_campeonato
)


router = APIRouter(prefix="/directiva-equipos", tags=["Directiva de Equipos"])


@router.post(
    "/",
    response_model=DirectivaEquipoResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_directivo_campeonato)]
)
async def asignar_directivo(
    datos: DirectivaEquipoCreate,
    db: AsyncSession = Depends(get_db)
):
    """Asignar un directivo a un equipo."""
    # Verificar que el usuario existe y tiene rol Directivo
    usuario = (await db.execute(
        select(Usuario).where(Usuario.id == datos.usuario_id)
    )).scalar_one_or_none()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
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

    if usuario.rol != "Directivo":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario no tiene rol de Directivo"
        )

    # Verificar que el directivo no esté ya en ese equipo
    existente = (await db.execute(
        select(DirectivaEquipo).where(
            DirectivaEquipo.usuario_id == datos.usuario_id,
            DirectivaEquipo.equipo_id == datos.equipo_id
        )
    )).scalar_one_or_none()

    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El directivo ya está asignado a este equipo"
        )

    db_directiva = DirectivaEquipo(**datos.model_dump())
    db.add(db_directiva)
    await db.commit()
    await db.refresh(db_directiva)
    return db_directiva


@router.get(
    "/equipo/{equipo_id}",
    response_model=List[DirectivaEquipoResponse],
    dependencies=[Depends(require_authenticated)]
)
async def listar_directiva_equipo(
    equipo_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Listar la directiva de un equipo."""
    result = await db.execute(
        select(DirectivaEquipo).where(DirectivaEquipo.equipo_id == equipo_id)
    )
    return result.scalars().all()


@router.put(
    "/{directiva_id}",
    response_model=DirectivaEquipoResponse,
    dependencies=[Depends(require_directivo_campeonato)]
)
async def actualizar_directivo(
    directiva_id: int,
    datos: DirectivaEquipoUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Actualizar el subrol de un directivo en el equipo."""
    db_directiva = (await db.execute(
        select(DirectivaEquipo).where(DirectivaEquipo.id == directiva_id)
    )).scalar_one_or_none()

    if not db_directiva:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Directivo en equipo no encontrado"
        )

    update_data = datos.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_directiva, field, value)

    await db.commit()
    await db.refresh(db_directiva)
    return db_directiva


@router.delete(
    "/{directiva_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_directivo_campeonato)]
)
async def remover_directivo(
    directiva_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Remover un directivo de un equipo."""
    db_directiva = (await db.execute(
        select(DirectivaEquipo).where(DirectivaEquipo.id == directiva_id)
    )).scalar_one_or_none()

    if not db_directiva:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Directivo en equipo no encontrado"
        )

    await db.delete(db_directiva)
    await db.commit()
    return None
