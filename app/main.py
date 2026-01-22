"""
Módulo principal de la aplicación RF App API.

Este módulo define la aplicación FastAPI y configura los routers.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import ejemplo  # Importa tu router

app = FastAPI(
    title="RF App API",
    description="API para aplicación RF",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(ejemplo.router)


@app.get("/")
def read_root():
    """
    Endpoint raíz de la API.
    Returns:
        dict: Mensaje de bienvenida y metadata de la API
    """
    return {
        "message": "Bienvenido a RF App API",
        "documentation": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    """
    Endpoint de verificación de salud.

    Returns:
        dict: Estado del servicio
    """
    return {"status": "healthy", "service": "RF App"}
