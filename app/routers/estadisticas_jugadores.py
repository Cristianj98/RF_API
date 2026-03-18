"""Router de Estadísticas de Jugadores."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.estadistica_jugador import EstadisticaJugador
from app.models.campeonato import Campeonato
from app.schemas.estadisticas_jugador import EstadisticaJugadorResponse
from app.core.dependencies import require_authenticated

router = APIRouter(prefix="/estadisticas-jugadores",
                   tags=["Estadísticas Jugadores"])


@router.get(
    "/campeonato/{campeonato_id}",
    response_model=List[EstadisticaJugadorResponse],
    dependencies=[Depends(require_authenticated)]
)
async def listar_estadisticas_campeonato(
    campeonato_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Listar estadísticas de todos los jugadores en un campeonato."""
    campeonato = (await db.execute(
        select(Campeonato).where(Campeonato.id == campeonato_id)
    )).scalar_one_or_none()
    if not campeonato:
        raise HTTPException(status_code=404, detail="Campeonato no encontrado")

    result = await db.execute(
        select(EstadisticaJugador)
        .where(EstadisticaJugador.campeonato_id == campeonato_id)
        .order_by(EstadisticaJugador.goles.desc())
    )
    return result.scalars().all()


@router.get(
    "/jugador/{jugador_id}/campeonato/{campeonato_id}",
    response_model=EstadisticaJugadorResponse,
    dependencies=[Depends(require_authenticated)]
)
async def obtener_estadistica_jugador(
    jugador_id: int,
    campeonato_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Obtener estadísticas de un jugador en un campeonato específico."""
    estadistica = (await db.execute(
        select(EstadisticaJugador).where(
            EstadisticaJugador.jugador_id == jugador_id,
            EstadisticaJugador.campeonato_id == campeonato_id
        )
    )).scalar_one_or_none()
    if not estadistica:
        raise HTTPException(
            status_code=404,
            detail="Estadísticas no encontradas para este jugador"
        )
    return estadistica
