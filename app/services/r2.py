"""Servicio para manejo de Cloudflare R2."""
import uuid
from datetime import timedelta
from minio import Minio
from app.config import settings


def get_r2_client() -> Minio:
    """Retorna un cliente Minio apuntando a Cloudflare R2."""
    return Minio(
        f"{settings.r2_account_id}.r2.cloudflarestorage.com",
        access_key=settings.r2_access_key_id,
        secret_key=settings.r2_secret_access_key,
        secure=True,
    )


def generar_presigned_url(
    filename: str,
    content_type: str,
    carpeta: str = "logos"
) -> dict:
    """Genera una presigned URL para subir un archivo a R2."""
    extension = filename.rsplit(".", 1)[-1] if "." in filename else "jpg"
    key = f"{carpeta}/{uuid.uuid4()}.{extension}"

    client = get_r2_client()

    upload_url = client.presigned_put_object(
        bucket_name=settings.r2_bucket_name,
        object_name=key,
        expires=timedelta(minutes=5),
    )

    public_url = f"{settings.r2_public_url}/{key}"

    return {"upload_url": upload_url, "public_url": public_url}
