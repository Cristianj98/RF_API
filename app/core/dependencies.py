"""Dependencias de autorización."""
from fastapi import Depends, HTTPException, status
from app.models.usuario import Usuario
from app.routers.auth import get_current_user


async def require_authenticated(
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    """Requiere que el usuario esté autenticado."""
    return current_user


async def require_admin(
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    """Requiere que el usuario sea Administrador o SuperAdministrador."""
    if current_user.rol not in ["Administrador", "SuperAdministrador"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para realizar esta acción"
        )
    return current_user


async def require_directivo_campeonato(
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    """Requiere que el usuario sea Directivo, Administrador o SuperAdmin."""
    if current_user.rol not in [
        "DirectivoCampeonato",
        "Administrador",
        "SuperAdministrador"
    ]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para realizar esta acción"
        )
    return current_user
