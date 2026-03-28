# pylint: disable=E0401,E0611
"""Servicio de caché con Redis."""
import json
from typing import Optional
from redis.asyncio import Redis

DEFAULT_TTL = 300  # 5 minutos


async def get_cache(redis: Redis, key: str) -> Optional[dict]:
    """Obtener datos del caché."""
    data = await redis.get(key)
    return json.loads(data) if data else None


async def set_cache(redis: Redis, key: str, data, ttl: int = DEFAULT_TTL):
    """Guardar datos en el caché."""
    await redis.setex(key, ttl, json.dumps(data, default=str))


async def delete_cache(redis: Redis, key: str):
    """Eliminar una clave del caché."""
    await redis.delete(key)


async def delete_pattern(redis: Redis, pattern: str):
    """Eliminar todas las claves que coincidan con un patrón."""
    keys = await redis.keys(pattern)
    if keys:
        await redis.delete(*keys)
