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

    class Config:
        """Configuración de Pydantic para Settings."""
        env_file = ".env"


settings = Settings()
