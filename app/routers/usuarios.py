"""Routes de usuarios."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.security import get_password_hash
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from app.core.dependencies import require_admin, require_authenticated


router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post(
    "/",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)]
)
async def crear_usuario(
    usuario: UsuarioCreate,
    db: AsyncSession = Depends(get_db)
):
    """Crear un nuevo usuario."""
    # Verificar si ya existe el username o cedula o email
    result = await db.execute(
        select(Usuario).where(
            (Usuario.username == usuario.username) |
            (Usuario.cedula == usuario.cedula) |
            (Usuario.email == usuario.email)
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario, cédula o email ya existe"
        )
    user_dict = usuario.model_dump()
    user_dict["password"] = get_password_hash(usuario.password)

    db_usuario = Usuario(**user_dict)
    db.add(db_usuario)
    await db.commit()
    await db.refresh(db_usuario)
    return db_usuario


@router.get(
    "/",
    response_model=List[UsuarioResponse],
    dependencies=[Depends(require_authenticated)]
)
async def listar_usuarios(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Listar todos los usuarios."""
    return (await db.execute(
        select(Usuario).offset(skip).limit(limit)
    )).scalars().all()


@router.get(
    "/{usuario_id}",
    response_model=UsuarioResponse,
    dependencies=[Depends(require_authenticated)]
)
async def obtener_usuario(
    usuario_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Obtener un usuario por ID."""
    usuario = (await db.execute(
        select(Usuario).where(Usuario.id == usuario_id)
    )).scalar_one_or_none()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return usuario


@router.put("/{usuario_id}", response_model=UsuarioResponse)
async def actualizar_usuario(
    usuario_id: int,
    usuario_update: UsuarioUpdate,
    current_user: Usuario = Depends(require_authenticated),
    db: AsyncSession = Depends(get_db)
):
    """Actualizar un usuario."""
    result = await db.execute(select(Usuario).where(Usuario.id == usuario_id))
    db_usuario = result.scalar_one_or_none()
    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    # Validar que actualice su propia información o que sea admin
    if db_usuario.id != current_user.id and current_user.rol not in [
        "Administrador",
        "SuperAdministrador"
    ]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No puedes editar la información de otro usuario"
        )

    update_data = usuario_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_usuario, field, value)

    await db.commit()
    await db.refresh(db_usuario)
    return db_usuario


@router.delete(
    "/{usuario_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)]
)
async def eliminar_usuario(
    usuario_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Eliminar un usuario."""
    result = await db.execute(select(Usuario).where(Usuario.id == usuario_id))
    db_usuario = result.scalar_one_or_none()
    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    await db.delete(db_usuario)
    await db.commit()
    return None
