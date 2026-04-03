# ============================================================
#  telegram_sender.py
#  Envía el PDF generado al chat privado del administrador
#  via Telegram Bot API. No requiere OAuth ni cuentas de servicio.
# ============================================================

import os
import requests
import logging

logger = logging.getLogger(__name__)


def send_pdf_telegram(
    pdf_path: str,
    filename: str,
    company_name: str = "",
    answered: int = 0,
    total: int = 0,
    bot_token: str = "",
    chat_id: str = "",
) -> bool:
    """
    Envía el PDF del diagnóstico ESG al chat de Telegram del administrador.

    Args:
        pdf_path     : Ruta local del archivo PDF temporal.
        filename     : Nombre del archivo (se muestra en el mensaje).
        company_name : Nombre de la empresa que completó el formulario.
        answered     : Cantidad de preguntas respondidas.
        total        : Total de preguntas del formulario.
        bot_token    : Token del bot de Telegram (desde .env).
        chat_id      : ID del chat del administrador (desde .env).

    Returns:
        True si el envío fue exitoso, False si hubo algún error.
    """
    if not bot_token or not chat_id:
        raise ValueError(
            "Faltan TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID en las variables de entorno.\n"
            "Consultá el README.md para configurarlos."
        )

    # ── Armar el mensaje de notificación ────────────────────
    pct = round((answered / total * 100)) if total else 0
    caption = (
        f"📋 *Nuevo diagnóstico ESG recibido*\n"
        f"🏢 *Empresa:* {company_name or '(sin nombre)'}\n"
        f"✅ *Respondidas:* {answered} de {total} ({pct}%)\n"
        f"📄 *Archivo:* `{filename}`"
    )

    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"

    try:
        with open(pdf_path, "rb") as pdf_file:
            response = requests.post(
                url,
                data={
                    "chat_id": chat_id,
                    "caption": caption,
                    "parse_mode": "Markdown",
                },
                files={
                    "document": (filename, pdf_file, "application/pdf"),
                },
                timeout=30,
            )

        if response.status_code == 200 and response.json().get("ok"):
            logger.info("PDF enviado a Telegram correctamente: %s", filename)
            return True
        else:
            error = response.json().get("description", "Error desconocido")
            logger.error("Telegram respondió con error: %s", error)
            raise RuntimeError(f"Telegram API error: {error}")

    except requests.exceptions.Timeout:
        logger.error("Timeout al conectar con Telegram API")
        raise RuntimeError("No se pudo conectar con Telegram (timeout). Verificá tu conexión.")

    except requests.exceptions.ConnectionError:
        logger.error("Error de conexión con Telegram API")
        raise RuntimeError("No se pudo conectar con Telegram. Verificá tu conexión a internet.")
