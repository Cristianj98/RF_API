"""Router de Partidos."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.database import get_db
from app.models.partido import Partido
from app.models.campeonato import Campeonato
from app.models.equipo import Equipo
from app.schemas.partido import (
    PartidoCreate,
    PartidoDetalleResponse,
    PartidoUpdate,
    PartidoResponse
)
from app.core.dependencies import require_authenticated, require_admin
from app.services.partido_service import finalizar_partido

router = APIRouter(prefix="/partidos", tags=["Partidos"])

ESTADOS_VALIDOS = ["Programado", "En curso", "Finalizado", "Suspendido"]


@router.post(
    "/",
    response_model=PartidoResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)]
)
async def crear_partido(
    datos: PartidoCreate,
    db: AsyncSession = Depends(get_db)
):
    """Crear un nuevo partido. Solo Administrador o SuperAdministrador."""
    # Verificar que el campeonato existe
    campeonato = (await db.execute(
        select(Campeonato).where(Campeonato.id == datos.campeonato_id)
    )).scalar_one_or_none()
    if not campeonato:
        raise HTTPException(status_code=404, detail="Campeonato no encontrado")

    # Verificar que el equipo local existe y pertenece al campeonato
    equipo_local = (await db.execute(
        select(Equipo).where(
            Equipo.id == datos.equipo_local_id,
            Equipo.campeonato_id == datos.campeonato_id
        )
    )).scalar_one_or_none()
    if not equipo_local:
        raise HTTPException(
            status_code=404,
            detail="Equipo local no encontrado o no pertenece al campeonato"
        )

    # Verificar que el equipo visitante existe y pertenece al campeonato
    equipo_visitante = (await db.execute(
        select(Equipo).where(
            Equipo.id == datos.equipo_visitante_id,
            Equipo.campeonato_id == datos.campeonato_id
        )
    )).scalar_one_or_none()
    if not equipo_visitante:
        raise HTTPException(
            status_code=404,
            detail="Equipo visitante no encontrado o no asignado al campeonato"
        )

    # Verificar que no sea el mismo equipo contra sí mismo
    if datos.equipo_local_id == datos.equipo_visitante_id:
        raise HTTPException(
            status_code=400,
            detail="El equipo local y visitante no pueden ser el mismo"
        )

    # Verificar estado válido
    if datos.estado and datos.estado not in ESTADOS_VALIDOS:
        raise HTTPException(
            status_code=400,
            detail=f"Estado inválido. Debe ser uno de: {ESTADOS_VALIDOS}"
        )

    db_partido = Partido(**datos.model_dump())
    db.add(db_partido)
    await db.commit()
    await db.refresh(db_partido)
    return db_partido


@router.get(
    "/",
    response_model=List[PartidoDetalleResponse],
    dependencies=[Depends(require_authenticated)]
)
async def listar_partidos(
    skip: int = 0,
    limit: int = 100,
    campeonato_id: Optional[int] = None,
    jornada: Optional[int] = None,
    estado: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Listar partidos con filtros opcionales."""
    query = select(Partido).options(
        joinedload(Partido.campeonato),
        joinedload(Partido.equipo_local),
        joinedload(Partido.equipo_visitante)
    )
    if campeonato_id:
        query = query.where(Partido.campeonato_id == campeonato_id)
    if jornada:
        query = query.where(Partido.jornada == jornada)
    if estado:
        query = query.where(Partido.estado == estado)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get(
    "/{partido_id}",
    response_model=PartidoDetalleResponse,
    dependencies=[Depends(require_authenticated)]
)
async def obtener_partido(
    partido_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Obtener un partido por su ID."""
    partido = (await db.execute(
        select(Partido)
        .options(
            joinedload(Partido.campeonato),
            joinedload(Partido.equipo_local),
            joinedload(Partido.equipo_visitante)
        )
        .where(Partido.id == partido_id)
    )).scalar_one_or_none()
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return partido


@router.put(
    "/{partido_id}",
    response_model=PartidoDetalleResponse,
    dependencies=[Depends(require_admin)]
)
async def actualizar_partido(
    partido_id: int,
    datos: PartidoUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Actualizar un partido."""
    db_partido = (await db.execute(
        select(Partido).where(Partido.id == partido_id)
    )).scalar_one_or_none()
    if not db_partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")

    # Verificar estado válido
    if datos.estado and datos.estado not in ESTADOS_VALIDOS:
        raise HTTPException(
            status_code=400,
            detail=f"Estado inválido. Debe ser uno de: {ESTADOS_VALIDOS}"
        )

    # No permitir editar un partido ya finalizado
    if db_partido.estado == "Finalizado":
        raise HTTPException(
            status_code=400,
            detail="No se puede editar un partido finalizado"
        )

    # Dentro de actualizar_partido, antes del commit:
    update_data = datos.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_partido, field, value)

    if datos.estado == "Finalizado":
        await finalizar_partido(db, db_partido)
    else:
        await db.commit()

    return (await db.execute(
        select(Partido)
        .options(
            joinedload(Partido.campeonato),
            joinedload(Partido.equipo_local),
            joinedload(Partido.equipo_visitante)
        )
        .where(Partido.id == partido_id)
    )).scalar_one()


@router.delete(
    "/{partido_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)]
)
async def eliminar_partido(
    partido_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Eliminar un partido."""
    db_partido = (await db.execute(
        select(Partido).where(Partido.id == partido_id)
    )).scalar_one_or_none()
    if not db_partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")

    # No permitir eliminar un partido finalizado
    if db_partido.estado == "Finalizado":
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar un partido finalizado"
        )

    await db.delete(db_partido)
    await db.commit()
    return None
