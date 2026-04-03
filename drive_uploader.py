# ============================================================
#  drive_uploader.py
#  Sube el PDF generado a una carpeta de Google Drive
#  usando cuenta de servicio (Service Account)
# ============================================================

import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

# Permisos mínimos necesarios
SCOPES = ["https://www.googleapis.com/auth/drive.file"]


def _get_service(credentials_path: str):
    """
    Crea el cliente autenticado de Google Drive.
    Requiere un archivo JSON de Service Account con acceso
    a la carpeta de destino en Drive.
    """
    if not os.path.exists(credentials_path):
        raise FileNotFoundError(
            f"No se encontró el archivo de credenciales: '{credentials_path}'\n"
            "Consulte README.md → Sección 'Configuración de Google Drive'."
        )

    creds = service_account.Credentials.from_service_account_file(
        credentials_path, scopes=SCOPES
    )
    return build("drive", "v3", credentials=creds, cache_discovery=False)


def upload_to_drive(
    local_path: str,
    filename: str,
    folder_id: str,
    credentials_path: str = "credentials.json",
) -> str:
    """
    Sube un archivo PDF a Google Drive.

    Args:
        local_path      : Ruta local del archivo PDF a subir.
        filename        : Nombre que tendrá el archivo en Drive.
        folder_id       : ID de la carpeta de Google Drive de destino.
        credentials_path: Ruta al JSON de la cuenta de servicio.

    Returns:
        URL pública del archivo (vista previa de Drive) si tiene permiso,
        o el ID del archivo en Drive.
    """
    if not folder_id:
        raise ValueError(
            "DRIVE_FOLDER_ID no configurado. "
            "Defínalo en el archivo .env (ver README.md)."
        )

    service = _get_service(credentials_path)

    file_metadata = {
        "name": filename,
        "parents": [folder_id],
        "mimeType": "application/pdf",
    }

    media = MediaFileUpload(local_path, mimetype="application/pdf", resumable=False)

    uploaded = (
        service.files()
        .create(body=file_metadata, media_body=media, fields="id, webViewLink")
        .execute()
    )

    file_id   = uploaded.get("id", "")
    view_link = uploaded.get("webViewLink", f"https://drive.google.com/file/d/{file_id}/view")

    return view_link


def list_recent_uploads(folder_id: str, credentials_path: str = "credentials.json", max_results: int = 10):
    """
    Lista los últimos archivos subidos a la carpeta de Drive.
    Útil para verificar que las subidas funcionan correctamente.
    """
    service = _get_service(credentials_path)
    query = f"'{folder_id}' in parents and trashed=false"
    results = (
        service.files()
        .list(
            q=query,
            pageSize=max_results,
            fields="files(id, name, createdTime, webViewLink)",
            orderBy="createdTime desc",
        )
        .execute()
    )
    return results.get("files", [])
