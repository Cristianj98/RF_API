"""Router de autenticación."""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.auth import UserRegister, Token
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(prefix="/auth", tags=["Autenticación"])

# OAuth2 scheme para extraer el token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    """Registrar un nuevo usuario."""
    # Verificar si ya existe el username, email o cedula
    result = await db.execute(
        select(Usuario).where(
            (Usuario.username == user_data.username) |
            (Usuario.email == user_data.email) |
            (Usuario.cedula == user_data.cedula)
        )
    )

    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username, email o cédula ya registrados"
        )

    # Crear usuario y hash en la contraseña
    user_dict = user_data.model_dump()
    user_dict["password"] = get_password_hash(user_data.password)

    db_usuario = Usuario(**user_dict)
    db.add(db_usuario)
    await db.commit()
    await db.refresh(db_usuario)

    return {
        "message": "Usuario registrado exitosamente",
        "user_id": db_usuario.id,
        "username": db_usuario.username
    }


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """Iniciar sesión y obtener token JWT."""
    # Buscar usuario
    result = await db.execute(
        select(Usuario).where(Usuario.username == form_data.username)
    )
    usuario = result.scalar_one_or_none()

    # Validar usuario y contraseña
    if not usuario or not verify_password(
        form_data.password,
        usuario.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Crear token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": usuario.username,
            "user_id": usuario.id,
            "rol": usuario.rol
        },
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> Usuario:
    """Obtener usuario actual desde el token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Decodificar token
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    username: str = payload.get("sub")
    user_id: int = payload.get("user_id")

    if username is None or user_id is None:
        raise credentials_exception

    # Buscar usuario en BD
    result = await db.execute(select(Usuario).where(Usuario.id == user_id))
    usuario = result.scalar_one_or_none()

    if usuario is None:
        raise credentials_exception

    return usuario


@router.get("/me")
async def get_me(current_user: Usuario = Depends(get_current_user)):
    """Obtener información del usuario autenticado."""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "nombres": current_user.nombres,
        "apellidos": current_user.apellidos,
        "rol": current_user.rol
    }
