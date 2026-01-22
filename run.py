"""
Script para ejecutar la aplicación FastAPI.

Este script inicia el servidor Uvicorn con la configuración especificada.
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
