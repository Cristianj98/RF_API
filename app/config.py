"""
Configuración de la aplicación RF App.
Este módulo contiene la configuración de
la aplicación usando Pydantic Settings.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuración de la aplicación.

    Attributes:
        app_name: Nombre de la aplicación
        debug: Modo de depuración
    """
    app_name: str = "RF App API"
    debug: bool = False

    """
    Data Base settings.
    """
    database_url: str
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str

    class Config:
        """Configuración de Pydantic para Settings."""
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = Settings()
