# ============================================================
#  app.py  –  Plataforma GALILEO
#  Aplicación Flask: formulario ESG → PDF → Google Drive
# ============================================================

import os
import tempfile
import logging
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

from form_data import SECTIONS, COMPANY_FIELDS
from pdf_generator import generate_pdf
from drive_uploader import upload_to_drive

# ── Configuración ────────────────────────────────────────────
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "galileo-esg-dev-key-cambiar-en-prod")

# Variables de entorno requeridas
DRIVE_FOLDER_ID      = os.getenv("DRIVE_FOLDER_ID", "")
GOOGLE_CREDENTIALS   = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")
SKIP_DRIVE_UPLOAD    = os.getenv("SKIP_DRIVE_UPLOAD", "false").lower() == "true"


# ── Helpers ──────────────────────────────────────────────────

def _sanitize_filename(name: str) -> str:
    """Normaliza el nombre de empresa para usarlo en el filename del PDF."""
    import re
    name = name.strip().upper()
    name = re.sub(r"[^A-Z0-9\s_-]", "", name)
    name = re.sub(r"\s+", "_", name)
    return name[:40] or "PROVEEDOR"


def _build_form_data(raw: dict, multi: dict) -> dict:
    """
    Combina los datos simples y los datos de selección múltiple
    en un único objeto accesible por get() / getlist().
    """
    combined = dict(raw)
    for k, v in multi.items():
        combined[k] = v
    return combined


def _count_answered(form_data: dict) -> tuple[int, int]:
    """Devuelve (preguntas respondidas, total preguntas)."""
    total = sum(len(s["questions"]) for s in SECTIONS)
    answered = 0
    for section in SECTIONS:
        for q in section["questions"]:
            qid = q["id"]
            if q["type"] == "numeric_multi":
                if any(form_data.get(sf["id"], "").strip() for sf in q.get("sub_fields", [])):
                    answered += 1
            elif form_data.get(qid, ""):
                val = form_data.get(qid)
                if isinstance(val, list):
                    if val:
                        answered += 1
                elif str(val).strip():
                    answered += 1
    return answered, total


# ── Rutas ────────────────────────────────────────────────────

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
    """Recibe el formulario, genera el PDF y lo sube a Drive."""

    # ── 1. Recoger datos del formulario ─────────────────────
    raw_data  = request.form.to_dict(flat=True)
    multi_data = {k: request.form.getlist(k) for k in request.form.keys()
                  if len(request.form.getlist(k)) > 1}
    form_data = _build_form_data(raw_data, multi_data)

    # Hack: adjuntar getlist para que el generador de PDF pueda usarlo
    form_data["_raw_request"] = request.form

    # ── 2. Validación mínima ─────────────────────────────────
    company_name  = form_data.get("company_name", "").strip()
    company_email = form_data.get("company_email", "").strip()

    if not company_name:
        flash("Por favor complete el nombre de la empresa antes de enviar.", "error")
        return redirect(url_for("index") + "#top")

    if not company_email:
        flash("Por favor ingrese un correo electrónico de contacto.", "error")
        return redirect(url_for("index") + "#top")

    # ── 3. Armar nombre del archivo ─────────────────────────
    date_str  = datetime.now().strftime("%Y%m%d_%H%M")
    safe_name = _sanitize_filename(company_name)
    filename  = f"ESG_Diagnostico_{safe_name}_{date_str}.pdf"

    answered, total = _count_answered(form_data)
    logger.info("Formulario recibido: empresa=%s | respondidas=%d/%d", company_name, answered, total)

    # ── 4. Generar PDF en archivo temporal ──────────────────
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp_path = tmp.name

        # Pasar el objeto ImmutableMultiDict original al generador
        # para que getlist() funcione con checkboxes
        generate_pdf(request.form, tmp_path, SECTIONS, COMPANY_FIELDS)
        logger.info("PDF generado: %s (%d bytes)", filename, os.path.getsize(tmp_path))

    except Exception as exc:
        logger.exception("Error al generar el PDF")
        flash(f"No se pudo generar el PDF: {exc}", "error")
        return redirect(url_for("index"))

    # ── 5. Subir a Google Drive ──────────────────────────────
    file_url = None
    upload_error = None

    if SKIP_DRIVE_UPLOAD:
        logger.warning("SKIP_DRIVE_UPLOAD=true → el PDF no se subió a Drive.")
        upload_error = "Modo de prueba: subida a Drive desactivada (SKIP_DRIVE_UPLOAD=true)."
    else:
        try:
            file_url = upload_to_drive(tmp_path, filename, DRIVE_FOLDER_ID, GOOGLE_CREDENTIALS)
            logger.info("PDF subido a Drive correctamente: %s", file_url)
        except Exception as exc:
            logger.exception("Error al subir a Drive")
            upload_error = str(exc)

    # ── 6. Limpiar temporal ──────────────────────────────────
    if tmp_path and os.path.exists(tmp_path):
        os.unlink(tmp_path)

    # ── 7. Responder al usuario ──────────────────────────────
    return render_template(
        "success.html",
        company=company_name,
        filename=filename,
        file_url=file_url,
        upload_error=upload_error,
        answered=answered,
        total=total,
        date_str=datetime.now().strftime("%d/%m/%Y a las %H:%M"),
    )


@app.route("/healthcheck")
def healthcheck():
    """Endpoint de verificación de estado para monitoreo."""
    return {
        "status": "ok",
        "drive_folder_configured": bool(DRIVE_FOLDER_ID),
        "credentials_found": os.path.exists(GOOGLE_CREDENTIALS),
        "skip_drive": SKIP_DRIVE_UPLOAD,
    }


# ── Arranque ─────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    logger.info("Iniciando GALILEO en http://0.0.0.0:%d  debug=%s", port, debug)
    app.run(host="0.0.0.0", port=port, debug=debug)
