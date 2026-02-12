"""
Módulo principal de la aplicación RF App API.

Este módulo define la aplicación FastAPI y configura los routers.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

from app.database import Base, engine, get_db
# importar modelos para crear tablas
from app.models import Base, Usuario, Campeonato, ReporteJugador
from app.routers import usuarios


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Código que se ejecuta al iniciar"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Código que se ejecuta al cerrar (opcional)
    await engine.dispose()


app = FastAPI(
    title="LDPSA App API",
    description="API para aplicación LDPSA",
    version="1.0.0",
    lifespan=lifespan
)


# Routes
app.include_router(usuarios.router)


@app.get("/")
def root():
    """Ruta raíz de la API."""
    return {"mensaje": "API Campeonatos funcionando"}


@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """Verifica la conexión a la base de datos."""
    try:
        await db.execute(text("SELECT 1"))  # <- Envuelve en text()
        return {
            "status": "ok",
            "database": "connected",
            "message": "Conexión exitosa a PostgreSQL"
        }
    except SQLAlchemyError as e:
        return {
            "status": "error",
            "database": "disconnected",
            "error": str(e)
        }


# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
