"""Router de Estadísticas de Jugadores."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.equipo import Equipo
from app.models.estadistica_jugador import EstadisticaJugador
from app.models.campeonato import Campeonato
from app.models.jugador_equipo import JugadorEquipo
from app.schemas.estadisticas_jugador import EstadisticaJugadorDetalleResponse
from app.core.dependencies import require_authenticated

router = APIRouter(
    prefix="/estadisticas-jugadores",
    tags=["Estadísticas Jugadores"])


async def _get_equipo_jugador(
    db: AsyncSession,
    jugador_id: int,
    campeonato_id: int
):
    """Obtiene el equipo de un jugador en un campeonato."""
    jugador_equipo = (await db.execute(
        select(JugadorEquipo)
        .join(Equipo, JugadorEquipo.equipo_id == Equipo.id)
        .options(joinedload(JugadorEquipo.equipo))
        .where(
            JugadorEquipo.usuario_id == jugador_id,
            Equipo.campeonato_id == campeonato_id
        )
    )).scalar_one_or_none()
    return jugador_equipo.equipo if jugador_equipo else None


async def _build_response(
    db: AsyncSession,
    est: EstadisticaJugador,
    campeonato_id: int
) -> EstadisticaJugadorDetalleResponse:
    """Construye la respuesta enriquecida de una estadística."""
    equipo = await _get_equipo_jugador(db, est.jugador_id, campeonato_id)
    return EstadisticaJugadorDetalleResponse.model_validate({
        "id": est.id,
        "goles": est.goles,
        "asistencias": est.asistencias,
        "tarjetas_amarillas": est.tarjetas_amarillas,
        "tarjetas_rojas": est.tarjetas_rojas,
        "partidos_jugados": est.partidos_jugados,
        "jugador": est.jugador,
        "campeonato": est.campeonato,
        "equipo": equipo,
        "created_at": est.created_at,
        "updated_at": est.updated_at
    })


@router.get(
    "/campeonato/{campeonato_id}",
    response_model=List[EstadisticaJugadorDetalleResponse],
    dependencies=[Depends(require_authenticated)]
)
async def listar_estadisticas_campeonato(
    campeonato_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Listar estadísticas de todos los jugadores en un campeonato."""
    campeonato = (await db.execute(
        select(Campeonato).where(Campeonato.id == campeonato_id)
    )).scalar_one_or_none()
    if not campeonato:
        raise HTTPException(status_code=404, detail="Campeonato no encontrado")

    estadisticas = (await db.execute(
        select(EstadisticaJugador)
        .options(
            joinedload(EstadisticaJugador.jugador),
            joinedload(EstadisticaJugador.campeonato)
        )
        .where(EstadisticaJugador.campeonato_id == campeonato_id)
        .order_by(EstadisticaJugador.goles.desc())
    )).scalars().all()

    return [await _build_response(
        db, est, campeonato_id) for est in estadisticas]


@router.get(
    "/jugador/{jugador_id}/campeonato/{campeonato_id}",
    response_model=EstadisticaJugadorDetalleResponse,
    dependencies=[Depends(require_authenticated)]
)
async def obtener_estadistica_jugador(
    jugador_id: int,
    campeonato_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Obtener estadísticas de un jugador en un campeonato específico."""
    estadistica = (await db.execute(
        select(EstadisticaJugador)
        .options(
            joinedload(EstadisticaJugador.jugador),
            joinedload(EstadisticaJugador.campeonato)
        )
        .where(
            EstadisticaJugador.jugador_id == jugador_id,
            EstadisticaJugador.campeonato_id == campeonato_id
        )
    )).scalar_one_or_none()

    if not estadistica:
        raise HTTPException(
            status_code=404,
            detail="Estadísticas no encontradas para este jugador"
        )

    return await _build_response(db, estadistica, campeonato_id)
