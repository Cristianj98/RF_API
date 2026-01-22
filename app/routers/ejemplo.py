"""
Router de ejemplo para la API RF App.

Este módulo contiene endpoints de ejemplo para demostrar la funcionalidad.
"""
from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1",
    tags=["ejemplo"]
)


@router.get("/ejemplo")
def obtener_ejemplo():
    """
    Endpoint de ejemplo.

    Returns:
        dict: Mensaje de ejemplo con información de la funcionalidad
    """
    return {
        "mensaje": "Este es un endpoint de ejemplo",
        "funcionalidad": "RF App"
    }
