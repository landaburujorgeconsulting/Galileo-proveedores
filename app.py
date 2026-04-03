# ============================================================
#  app.py  –  Plataforma GALILEO
#  Aplicación Flask: formulario ESG → PDF → Telegram
# ============================================================

import os
import tempfile
import logging
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

from form_data import SECTIONS, COMPANY_FIELDS
from pdf_generator import generate_pdf
from telegram_sender import send_pdf_telegram

# ── Configuración ─────────────────────────────────────────────
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "galileo-esg-dev-key-cambiar-en-prod")

# Variables de entorno
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID   = os.getenv("TELEGRAM_CHAT_ID", "")
SKIP_TELEGRAM      = os.getenv("SKIP_TELEGRAM", "false").lower() == "true"


# ── Helpers ───────────────────────────────────────────────────

def _sanitize_filename(name: str) -> str:
    """Normaliza el nombre de empresa para usarlo en el nombre del PDF."""
    import re
    name = name.strip().upper()
    name = re.sub(r"[^A-Z0-9\s_-]", "", name)
    name = re.sub(r"\s+", "_", name)
    return name[:40] or "PROVEEDOR"


def _count_answered(form) -> tuple:
    """Devuelve (preguntas respondidas, total preguntas)."""
    total    = sum(len(s["questions"]) for s in SECTIONS)
    answered = 0

    for section in SECTIONS:
        for q in section["questions"]:
            qid = q["id"]

            if q["type"] == "numeric_multi":
                if any(form.get(sf["id"], "").strip() for sf in q.get("sub_fields", [])):
                    answered += 1

            elif q["type"] == "checkboxes":
                if form.getlist(qid):
                    answered += 1

            else:
                val = form.get(qid, "")
                if str(val).strip():
                    answered += 1

    return answered, total


# ── Rutas ──────────────────────────────────────────────────────

@app.route("/", methods=["GET"])
def index():
    """Página principal: muestra el formulario ESG."""
    return render_template(
        "form.html",
        sections=SECTIONS,
        company_fields=COMPANY_FIELDS,
        total_questions=sum(len(s["questions"]) for s in SECTIONS),
        total_sections=len(SECTIONS),
    )


@app.route("/enviar", methods=["POST"])
def submit():
    """Recibe el formulario, genera el PDF y lo envía por Telegram."""

    # ── 1. Validación mínima ──────────────────────────────────
    company_name  = request.form.get("company_name", "").strip()
    company_email = request.form.get("company_email", "").strip()

    if not company_name:
        flash("Por favor completá el nombre de la empresa antes de enviar.", "error")
        return redirect(url_for("index") + "#top")

    if not company_email:
        flash("Por favor ingresá un correo electrónico de contacto.", "error")
        return redirect(url_for("index") + "#top")

    # ── 2. Nombre del archivo PDF ─────────────────────────────
    date_str  = datetime.now().strftime("%Y%m%d_%H%M")
    safe_name = _sanitize_filename(company_name)
    filename  = f"ESG_Diagnostico_{safe_name}_{date_str}.pdf"

    answered, total = _count_answered(request.form)
    logger.info(
        "Formulario recibido | empresa=%s | respondidas=%d/%d",
        company_name, answered, total
    )

    # ── 3. Generar PDF en archivo temporal ────────────────────
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp_path = tmp.name

        generate_pdf(request.form, tmp_path, SECTIONS, COMPANY_FIELDS)
        size_kb = round(os.path.getsize(tmp_path) / 1024, 1)
        logger.info("PDF generado: %s (%s KB)", filename, size_kb)

    except Exception as exc:
        logger.exception("Error al generar el PDF")
        flash(f"No se pudo generar el PDF: {exc}", "error")
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)
        return redirect(url_for("index"))

    # ── 4. Enviar por Telegram ────────────────────────────────
    send_error = None

    if SKIP_TELEGRAM:
        logger.warning("SKIP_TELEGRAM=true → el PDF no se envió por Telegram.")
        send_error = "Modo prueba: envío por Telegram desactivado (SKIP_TELEGRAM=true)."
    else:
        try:
            send_pdf_telegram(
                pdf_path=tmp_path,
                filename=filename,
                company_name=company_name,
                answered=answered,
                total=total,
                bot_token=TELEGRAM_BOT_TOKEN,
                chat_id=TELEGRAM_CHAT_ID,
            )
        except Exception as exc:
            logger.exception("Error al enviar por Telegram")
            send_error = str(exc)

    # ── 5. Borrar el temporal ─────────────────────────────────
    if tmp_path and os.path.exists(tmp_path):
        os.unlink(tmp_path)
        logger.info("Archivo temporal eliminado: %s", tmp_path)

    # ── 6. Responder al usuario ───────────────────────────────
    return render_template(
        "success.html",
        company=company_name,
        filename=filename,
        send_error=send_error,
        answered=answered,
        total=total,
        date_str=datetime.now().strftime("%d/%m/%Y a las %H:%M"),
    )


@app.route("/healthcheck")
def healthcheck():
    """Endpoint de verificación de estado."""
    return {
        "status": "ok",
        "telegram_token_set": bool(TELEGRAM_BOT_TOKEN),
        "telegram_chat_set":  bool(TELEGRAM_CHAT_ID),
        "skip_telegram":      SKIP_TELEGRAM,
    }


# ── Arranque ───────────────────────────────────────────────────
if __name__ == "__main__":
    port  = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    logger.info("Iniciando GALILEO en http://0.0.0.0:%d  debug=%s", port, debug)
    app.run(host="0.0.0.0", port=port, debug=debug)
