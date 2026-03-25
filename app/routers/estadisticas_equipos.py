"""Router de Estadísticas de Equipos."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.estadistica_equipo import EstadisticaEquipo
from app.models.campeonato import Campeonato
from app.schemas.estadisticas_equipo import (
    EstadisticaEquipoDetalleResponse
)
from app.core.dependencies import require_authenticated

router = APIRouter(
    prefix="/estadisticas-equipos",
    tags=["Estadísticas Equipos"]
    )


@router.get(
    "/campeonato/{campeonato_id}",
    response_model=List[EstadisticaEquipoDetalleResponse],
    dependencies=[Depends(require_authenticated)]
)
async def listar_estadisticas_campeonato(
    campeonato_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Listar estadísticas de todos los equipos en un campeonato."""
    campeonato = (await db.execute(
        select(Campeonato).where(Campeonato.id == campeonato_id)
    )).scalar_one_or_none()
    if not campeonato:
        raise HTTPException(status_code=404, detail="Campeonato no encontrado")

    result = await db.execute(
        select(EstadisticaEquipo)
        .options(
            joinedload(EstadisticaEquipo.equipo),
            joinedload(EstadisticaEquipo.campeonato)
        )
        .where(EstadisticaEquipo.campeonato_id == campeonato_id)
        .order_by(EstadisticaEquipo.puntos.desc())
    )
    return result.scalars().all()


@router.get(
    "/equipo/{equipo_id}/campeonato/{campeonato_id}",
    response_model=EstadisticaEquipoDetalleResponse,
    dependencies=[Depends(require_authenticated)]
)
async def obtener_estadistica_equipo(
    equipo_id: int,
    campeonato_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Obtener estadísticas de un equipo en un campeonato específico."""
    estadistica = (await db.execute(
        select(EstadisticaEquipo)
        .options(
            joinedload(EstadisticaEquipo.equipo),
            joinedload(EstadisticaEquipo.campeonato)
        ).where(
            EstadisticaEquipo.equipo_id == equipo_id,
            EstadisticaEquipo.campeonato_id == campeonato_id
        )
    )).scalar_one_or_none()
    if not estadistica:
        raise HTTPException(
            status_code=404,
            detail="Estadísticas no encontradas para este equipo"
        )
    return estadistica
