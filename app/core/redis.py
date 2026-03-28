# pylint: disable=E0401,E0611
"""Configuración de conexión a Redis."""
from redis.asyncio import Redis
from app.config import settings


class RedisClient:
    """Singleton Redis client manager."""
    _instance: Redis = None

    @classmethod
    async def get_instance(cls) -> Redis:
        """Get or create Redis instance."""
        if cls._instance is None:
            cls._instance = Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=0,
                decode_responses=True
            )
            await cls._instance.ping()
        return cls._instance

    @classmethod
    async def close(cls) -> None:
        """Close Redis connection."""
        if cls._instance:
            await cls._instance.aclose()
            cls._instance = None


async def get_redis() -> Redis:
    """Obtener cliente Redis."""
    return await RedisClient.get_instance()


async def init_redis():
    """Inicializar conexión a Redis."""
    await RedisClient.get_instance()


async def close_redis():
    """Cerrar conexión a Redis."""
    await RedisClient.close()
