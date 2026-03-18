"""Servicio para manejar la lógica de negocio de partidos."""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.partido import Partido
from app.models.acta_partido import ActaPartido
from app.models.evento_partido import EventoPartido
from app.models.posicion import Posicion
from app.models.estadistica_jugador import EstadisticaJugador
from app.models.estadistica_equipo import EstadisticaEquipo


async def _get_or_create_estadistica_jugador(
    db: AsyncSession,
    jugador_id: int,
    campeonato_id: int
) -> EstadisticaJugador:
    """Obtiene o crea estadísticas de un jugador en un campeonato."""
    estadistica = (await db.execute(
        select(EstadisticaJugador).where(
            EstadisticaJugador.jugador_id == jugador_id,
            EstadisticaJugador.campeonato_id == campeonato_id
        )
    )).scalar_one_or_none()

    if not estadistica:
        estadistica = EstadisticaJugador(
            jugador_id=jugador_id,
            campeonato_id=campeonato_id
        )
        db.add(estadistica)
        await db.flush()  # Para obtener el id sin hacer commit

    return estadistica


async def _get_or_create_estadistica_equipo(
    db: AsyncSession,
    equipo_id: int,
    campeonato_id: int
) -> EstadisticaEquipo:
    """Obtiene o crea estadísticas de un equipo en un campeonato."""
    estadistica = (await db.execute(
        select(EstadisticaEquipo).where(
            EstadisticaEquipo.equipo_id == equipo_id,
            EstadisticaEquipo.campeonato_id == campeonato_id
        )
    )).scalar_one_or_none()

    if not estadistica:
        estadistica = EstadisticaEquipo(
            equipo_id=equipo_id,
            campeonato_id=campeonato_id
        )
        db.add(estadistica)
        await db.flush()

    return estadistica


async def _get_or_create_posicion(
    db: AsyncSession,
    equipo_id: int,
    campeonato_id: int
) -> Posicion:
    """Obtiene o crea la posición de un equipo en un campeonato."""
    posicion = (await db.execute(
        select(Posicion).where(
            Posicion.equipo_id == equipo_id,
            Posicion.campeonato_id == campeonato_id
        )
    )).scalar_one_or_none()

    if not posicion:
        posicion = Posicion(
            equipo_id=equipo_id,
            campeonato_id=campeonato_id
        )
        db.add(posicion)
        await db.flush()

    return posicion


async def finalizar_partido(
    db: AsyncSession,
    partido: Partido
) -> None:
    """
    Lógica completa al finalizar un partido.
    Actualiza estadísticas de jugadores, equipos y tabla de posiciones.
    """
    campeonato_id = partido.campeonato_id
    equipo_local_id = partido.equipo_local_id
    equipo_visitante_id = partido.equipo_visitante_id
    goles_local = partido.goles_local
    goles_visitante = partido.goles_visitante

    # ── 1. Actualizar estadísticas de jugadores ──────────────────────────
    # Obtener jugadores del acta que estuvieron convocados
    actas = (await db.execute(
        select(ActaPartido).where(
            ActaPartido.partido_id == partido.id,
            ActaPartido.convocado.is_(True)
        )
    )).scalars().all()

    for acta in actas:
        est = await _get_or_create_estadistica_jugador(
            db, acta.jugador_id, campeonato_id
        )
        est.partidos_jugados += 1

    # Obtener todos los eventos del partido
    eventos = (await db.execute(
        select(EventoPartido).where(EventoPartido.partido_id == partido.id)
    )).scalars().all()

    for evento in eventos:
        est = await _get_or_create_estadistica_jugador(
            db, evento.jugador_id, campeonato_id
        )
        if evento.tipo == "Gol":
            est.goles += 1
        elif evento.tipo == "TarjetaAmarilla":
            est.tarjetas_amarillas += 1
        elif evento.tipo == "TarjetaRoja":
            est.tarjetas_rojas += 1

    # ── 2. Actualizar estadísticas de equipos ────────────────────────────
    est_local = await _get_or_create_estadistica_equipo(
        db, equipo_local_id, campeonato_id
    )
    est_visitante = await _get_or_create_estadistica_equipo(
        db, equipo_visitante_id, campeonato_id
    )

    est_local.partidos_jugados += 1
    est_local.goles_favor += goles_local
    est_local.goles_contra += goles_visitante

    est_visitante.partidos_jugados += 1
    est_visitante.goles_favor += goles_visitante
    est_visitante.goles_contra += goles_local

    if goles_local > goles_visitante:
        est_local.victorias += 1
        est_local.puntos += 3
        est_visitante.derrotas += 1
    elif goles_local < goles_visitante:
        est_visitante.victorias += 1
        est_visitante.puntos += 3
        est_local.derrotas += 1
    else:
        est_local.empates += 1
        est_local.puntos += 1
        est_visitante.empates += 1
        est_visitante.puntos += 1

    # ── 3. Actualizar tabla de posiciones ────────────────────────────────
    pos_local = await _get_or_create_posicion(
        db, equipo_local_id, campeonato_id)
    pos_visitante = await _get_or_create_posicion(
        db, equipo_visitante_id, campeonato_id)

    pos_local.partidos_jugados += 1
    pos_local.goles_favor += goles_local
    pos_local.goles_contra += goles_visitante

    pos_visitante.partidos_jugados += 1
    pos_visitante.goles_favor += goles_visitante
    pos_visitante.goles_contra += goles_local

    if goles_local > goles_visitante:
        pos_local.ganados += 1
        pos_local.puntos += 3
        pos_visitante.perdidos += 1
    elif goles_local < goles_visitante:
        pos_visitante.ganados += 1
        pos_visitante.puntos += 3
        pos_local.perdidos += 1
    else:
        pos_local.empatados += 1
        pos_local.puntos += 1
        pos_visitante.empatados += 1
        pos_visitante.puntos += 1

    await db.commit()
