"""Router de Acta de Partido."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.acta_partido import ActaPartido
from app.models.partido import Partido
from app.models.usuario import Usuario
from app.models.equipo import Equipo
from app.models.jugador_equipo import JugadorEquipo
from app.schemas.acta_partido import (
    ActaPartidoCreate,
    ActaPartidoUpdate,
    ActaPartidoResponse,
    ActaPartidoDetalleResponse
)
from app.core.dependencies import require_authenticated, require_admin

router = APIRouter(prefix="/acta-partido", tags=["Acta de Partido"])


@router.post(
    "/",
    response_model=ActaPartidoResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)]
)
async def agregar_jugador_acta(
    datos: ActaPartidoCreate,
    db: AsyncSession = Depends(get_db)
):
    """Agregar un jugador al acta de un partido."""
    # Verificar que el partido existe
    partido = (await db.execute(
        select(Partido).where(Partido.id == datos.partido_id)
    )).scalar_one_or_none()
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")

    # No se puede modificar el acta de un partido finalizado
    if partido.estado == "Finalizado":
        raise HTTPException(
            status_code=400,
            detail="No se puede modificar el acta de un partido finalizado"
        )

    # Verificar que el jugador existe
    jugador = (await db.execute(
        select(Usuario).where(Usuario.id == datos.jugador_id)
    )).scalar_one_or_none()
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")

    # Verificar que el equipo existe y es parte del partido
    if datos.equipo_id not in [
            partido.equipo_local_id, partido.equipo_visitante_id]:
        raise HTTPException(
            status_code=400,
            detail="El equipo no es parte de este partido"
        )

    # Verificar que el jugador pertenece al equipo en ese campeonato
    pertenece = (await db.execute(
        select(JugadorEquipo)
        .join(Equipo, JugadorEquipo.equipo_id == Equipo.id)
        .where(
            JugadorEquipo.usuario_id == datos.jugador_id,
            JugadorEquipo.equipo_id == datos.equipo_id,
            Equipo.campeonato_id == partido.campeonato_id
        )
    )).scalar_one_or_none()
    if not pertenece:
        raise HTTPException(
            status_code=400,
            detail="El jugador no pertenece a este equipo en el campeonato"
        )

    # Verificar que el jugador no esté ya en el acta de este partido
    existente = (await db.execute(
        select(ActaPartido).where(
            ActaPartido.partido_id == datos.partido_id,
            ActaPartido.jugador_id == datos.jugador_id
        )
    )).scalar_one_or_none()
    if existente:
        raise HTTPException(
            status_code=400,
            detail="El jugador ya está en el acta de este partido"
        )

    db_acta = ActaPartido(**datos.model_dump())
    db.add(db_acta)
    await db.commit()
    await db.refresh(db_acta)
    return db_acta


@router.get(
    "/partido/{partido_id}",
    response_model=List[ActaPartidoDetalleResponse],
    dependencies=[Depends(require_authenticated)]
)
async def listar_acta_partido(
    partido_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Listar el acta completa de un partido."""
    partido = (await db.execute(
        select(Partido).where(Partido.id == partido_id)
    )).scalar_one_or_none()
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")

    result = await db.execute(
        select(ActaPartido)
        .options(
            joinedload(ActaPartido.jugador),
            joinedload(ActaPartido.equipo)
        )
        .where(ActaPartido.partido_id == partido_id)
    )
    return result.scalars().all()


@router.put(
    "/{acta_id}",
    response_model=ActaPartidoResponse,
    dependencies=[Depends(require_admin)]
)
async def actualizar_acta(
    acta_id: int,
    datos: ActaPartidoUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Actualizar convocatoria o titularidad de un jugador en el acta."""
    db_acta = (await db.execute(
        select(ActaPartido).where(ActaPartido.id == acta_id)
    )).scalar_one_or_none()
    if not db_acta:
        raise HTTPException(
            status_code=404, detail="Registro de acta no encontrado")

    # Verificar que el partido no esté finalizado
    partido = (await db.execute(
        select(Partido).where(Partido.id == db_acta.partido_id)
    )).scalar_one_or_none()
    if partido.estado == "Finalizado":
        raise HTTPException(
            status_code=400,
            detail="No se puede modificar el acta de un partido finalizado"
        )

    update_data = datos.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_acta, field, value)

    await db.commit()
    await db.refresh(db_acta)
    return db_acta


@router.delete(
    "/{acta_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)]
)
async def eliminar_acta(
    acta_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Eliminar un jugador del acta."""
    db_acta = (await db.execute(
        select(ActaPartido).where(ActaPartido.id == acta_id)
    )).scalar_one_or_none()
    if not db_acta:
        raise HTTPException(
            status_code=404, detail="Registro de acta no encontrado")

    # Verificar que el partido no esté finalizado
    partido = (await db.execute(
        select(Partido).where(Partido.id == db_acta.partido_id)
    )).scalar_one_or_none()
    if partido.estado == "Finalizado":
        raise HTTPException(
            status_code=400,
            detail="No se puede modificar el acta de un partido finalizado"
        )

    await db.delete(db_acta)
    await db.commit()
    return None
