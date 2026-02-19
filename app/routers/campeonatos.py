"""Router de Campeonatos."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.campeonato import Campeonato
from app.schemas.campeonato import (
    CampeonatoCreate,
    CampeonatoResponse,
    CampeonatoUpdate
)

router = APIRouter(prefix="/campeonatos", tags=["Campeonatos"])


@router.post(
    "/",
    response_model=CampeonatoResponse,
    status_code=status.HTTP_201_CREATED
    )
async def crear_campeonato(
    campeonato: CampeonatoCreate,
    db: AsyncSession = Depends(get_db)
):
    """Crear un nuevo campeonato."""
    # Verificar si ya existe un campeonato con el mismo nombre
    result = await db.execute(
        select(Campeonato).where(Campeonato.nombre == campeonato.nombre)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un campeonato con ese nombre."
        )

    db_campeonato = Campeonato(**campeonato.model_dump())
    db.add(db_campeonato)
    await db.commit()
    await db.refresh(db_campeonato)
    return db_campeonato


@router.get("/", response_model=List[CampeonatoResponse])
async def listar_campeonatos(
    skip: int = 0,
    limit: int = 100,
    estado: str | None = None,
    db: AsyncSession = Depends(get_db)
):
    """Listar campeonatos con filtro opcional por estado."""
    query = select(Campeonato)
    if estado:
        query = query.where(Campeonato.estado == estado)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{campeonato_id}", response_model=CampeonatoResponse)
async def obtener_campeonato(
    campeonato_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Obtener un campeonato por su ID."""
    campeonato = (await db.execute(
        select(Campeonato).where(Campeonato.id == campeonato_id)
    )).scalar_one_or_none()

    if not campeonato:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campeonato no encontrado."
        )
    return campeonato


@router.put("/{campeonato_id}", response_model=CampeonatoResponse)
async def actualizar_campeonato(
    campeonato_id: int,
    campeonato_update: CampeonatoUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Actualizar un campeonato."""
    result = await db.execute(
        select(Campeonato).where(Campeonato.id == campeonato_id)
    )
    db_campeonato = result.scalar_one_or_none()

    if not db_campeonato:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campeonato no encontrado"
        )

    update_data = campeonato_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_campeonato, field, value)

    await db.commit()
    await db.refresh(db_campeonato)
    return db_campeonato


@router.delete("/{campeonato_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_campeonato(
    campeonato_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Eliminar un campeonato."""
    result = await db.execute(
        select(Campeonato).where(Campeonato.id == campeonato_id)
    )
    db_campeonato = result.scalar_one_or_none()

    if not db_campeonato:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campeonato no encontrado"
        )

    await db.delete(db_campeonato)
    await db.commit()
    return None
