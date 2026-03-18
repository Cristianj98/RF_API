"""Router de Eventos de Partido."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.evento_partido import EventoPartido
from app.models.partido import Partido
from app.models.acta_partido import ActaPartido
from app.schemas.evento_partido import (
    EventoPartidoCreate,
    EventoPartidoResponse
)
from app.core.dependencies import require_authenticated, require_admin

router = APIRouter(prefix="/eventos-partido", tags=["Eventos de Partido"])

TIPOS_VALIDOS = ["Gol", "TarjetaAmarilla", "TarjetaRoja", "Cambio"]


@router.post(
    "/",
    response_model=EventoPartidoResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)]
)
async def registrar_evento(
    datos: EventoPartidoCreate,
    db: AsyncSession = Depends(get_db)
):
    """Registrar un evento en un partido."""
    # Verificar que el partido existe
    partido = (await db.execute(
        select(Partido).where(Partido.id == datos.partido_id)
    )).scalar_one_or_none()
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")

    # No se puede registrar eventos en un partido finalizado o programado
    if partido.estado == "Finalizado":
        raise HTTPException(
            status_code=400,
            detail="No se pueden registrar eventos en un partido finalizado"
        )
    if partido.estado == "Programado":
        raise HTTPException(
            status_code=400,
            detail="No se pueden registrar eventos en un partido programado"
        )

    # Verificar tipo válido
    if datos.tipo not in TIPOS_VALIDOS:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo inválido. Debe ser uno de: {TIPOS_VALIDOS}"
        )

    # Verificar que el equipo es parte del partido
    if datos.equipo_id not in [
            partido.equipo_local_id, partido.equipo_visitante_id]:
        raise HTTPException(
            status_code=400,
            detail="El equipo no es parte de este partido"
        )

    # Verificar que el jugador está en el acta del partido
    en_acta = (await db.execute(
        select(ActaPartido).where(
            ActaPartido.partido_id == datos.partido_id,
            ActaPartido.jugador_id == datos.jugador_id,
            ActaPartido.equipo_id == datos.equipo_id,
            ActaPartido.convocado.is_(True)
        )
    )).scalar_one_or_none()
    if not en_acta:
        raise HTTPException(
            status_code=400,
            detail="El jugador no está convocado en el acta de este partido"
        )

    # Si es cambio, verificar que jugador_sale_id esté presente y en el acta
    if datos.tipo == "Cambio":
        if not datos.jugador_sale_id:
            raise HTTPException(
                status_code=400,
                detail="Para un cambio se requiere jugador_sale_id"
            )
        jugador_sale = (await db.execute(
            select(ActaPartido).where(
                ActaPartido.partido_id == datos.partido_id,
                ActaPartido.jugador_id == datos.jugador_sale_id,
                ActaPartido.equipo_id == datos.equipo_id,
                ActaPartido.convocado.is_(True)
            )
        )).scalar_one_or_none()
        if not jugador_sale:
            raise HTTPException(
                status_code=400,
                detail="El jugador que sale no está convocado en el acta"
            )

    db_evento = EventoPartido(**datos.model_dump())
    db.add(db_evento)
    await db.commit()
    await db.refresh(db_evento)
    return db_evento


@router.get(
    "/partido/{partido_id}",
    response_model=List[EventoPartidoResponse],
    dependencies=[Depends(require_authenticated)]
)
async def listar_eventos_partido(
    partido_id: int,
    tipo: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Listar eventos de un partido con filtro opcional por tipo."""
    partido = (await db.execute(
        select(Partido).where(Partido.id == partido_id)
    )).scalar_one_or_none()
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")

    query = select(EventoPartido).where(EventoPartido.partido_id == partido_id)
    if tipo:
        if tipo not in TIPOS_VALIDOS:
            raise HTTPException(
                status_code=400,
                detail=f"Tipo inválido. Debe ser uno de: {TIPOS_VALIDOS}"
            )
        query = query.where(EventoPartido.tipo == tipo)

    result = await db.execute(query)
    return result.scalars().all()


@router.delete(
    "/{evento_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)]
)
async def eliminar_evento(
    evento_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Eliminar un evento de un partido."""
    db_evento = (await db.execute(
        select(EventoPartido).where(EventoPartido.id == evento_id)
    )).scalar_one_or_none()
    if not db_evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    # Verificar que el partido no esté finalizado
    partido = (await db.execute(
        select(Partido).where(Partido.id == db_evento.partido_id)
    )).scalar_one_or_none()
    if partido.estado == "Finalizado":
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar un evento de un partido finalizado"
        )

    await db.delete(db_evento)
    await db.commit()
    return None
