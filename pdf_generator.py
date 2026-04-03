# ============================================================
#  pdf_generator.py
#  Genera el PDF de diagnóstico ESG usando ReportLab (puro Python)
#  Colores: verde militar · Tipografía: Helvetica (sans-serif)
# ============================================================

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from datetime import datetime

# ── Paleta verde militar ────────────────────────────────────
GREEN_DARK   = colors.HexColor("#3a4220")   # Verde militar oscuro
GREEN_MID    = colors.HexColor("#4b5320")   # Verde militar medio
GREEN_LIGHT  = colors.HexColor("#6b7a3a")   # Verde militar claro
GREEN_BG     = colors.HexColor("#eef0e8")   # Fondo muy suave
GREY_TEXT    = colors.HexColor("#3a3a3a")   # Texto principal
GREY_LIGHT   = colors.HexColor("#888888")   # Texto secundario
WHITE        = colors.white


def _build_styles():
    """Crea todos los estilos de párrafo del documento."""
    base = getSampleStyleSheet()

    styles = {
        "doc_title": ParagraphStyle(
            "doc_title",
            fontName="Helvetica-Bold",
            fontSize=18,
            textColor=WHITE,
            alignment=TA_LEFT,
            spaceAfter=4,
        ),
        "doc_subtitle": ParagraphStyle(
            "doc_subtitle",
            fontName="Helvetica",
            fontSize=9,
            textColor=colors.HexColor("#c8d4a0"),
            alignment=TA_LEFT,
        ),
        "section_title": ParagraphStyle(
            "section_title",
            fontName="Helvetica-Bold",
            fontSize=12,
            textColor=WHITE,
            alignment=TA_LEFT,
            spaceAfter=2,
        ),
        "section_ref": ParagraphStyle(
            "section_ref",
            fontName="Helvetica-Oblique",
            fontSize=7.5,
            textColor=colors.HexColor("#c8d4a0"),
            alignment=TA_LEFT,
        ),
        "q_num": ParagraphStyle(
            "q_num",
            fontName="Helvetica-Bold",
            fontSize=8,
            textColor=GREEN_MID,
        ),
        "q_text": ParagraphStyle(
            "q_text",
            fontName="Helvetica",
            fontSize=9.5,
            textColor=GREY_TEXT,
            spaceAfter=4,
            leading=13,
        ),
        "answer_label": ParagraphStyle(
            "answer_label",
            fontName="Helvetica-Bold",
            fontSize=8,
            textColor=GREY_LIGHT,
            spaceAfter=1,
        ),
        "answer_value": ParagraphStyle(
            "answer_value",
            fontName="Helvetica",
            fontSize=9.5,
            textColor=GREY_TEXT,
            leading=13,
        ),
        "answer_none": ParagraphStyle(
            "answer_none",
            fontName="Helvetica-Oblique",
            fontSize=9,
            textColor=GREY_LIGHT,
        ),
        "company_label": ParagraphStyle(
            "company_label",
            fontName="Helvetica-Bold",
            fontSize=8,
            textColor=GREEN_MID,
            spaceAfter=1,
        ),
        "company_value": ParagraphStyle(
            "company_value",
            fontName="Helvetica",
            fontSize=9.5,
            textColor=GREY_TEXT,
        ),
        "footer": ParagraphStyle(
            "footer",
            fontName="Helvetica",
            fontSize=7.5,
            textColor=GREY_LIGHT,
            alignment=TA_CENTER,
        ),
        "otros_label": ParagraphStyle(
            "otros_label",
            fontName="Helvetica-Bold",
            fontSize=9,
            textColor=GREEN_MID,
            spaceAfter=2,
        ),
        "otros_text": ParagraphStyle(
            "otros_text",
            fontName="Helvetica",
            fontSize=9.5,
            textColor=GREY_TEXT,
            leading=13,
        ),
    }
    return styles


def _header_table(styles):
    """Bloque de encabezado del documento (fondo verde militar)."""
    title_p    = Paragraph("DIAGNÓSTICO DE SOSTENIBILIDAD PARA PROVEEDORES", styles["doc_title"])
    subtitle_p = Paragraph(
        "60 preguntas · 14 dimensiones ESG · GRI 2021 | ISO 20400 | UNGPs | TCFD | ESRS | ISO 45001 | ISO 14001",
        styles["doc_subtitle"],
    )
    date_str = datetime.now().strftime("%d/%m/%Y – %H:%M h")
    date_p = Paragraph(
        f'Generado el {date_str} | Plataforma GALILEO',
        ParagraphStyle("d", fontName="Helvetica", fontSize=8,
                       textColor=colors.HexColor("#c8d4a0"), alignment=TA_RIGHT),
    )

    tbl = Table(
        [[title_p, date_p], [subtitle_p, ""]],
        colWidths=["70%", "30%"],
    )
    tbl.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, -1), GREEN_DARK),
        ("TOPPADDING",  (0, 0), (-1, -1), 16),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
        ("LEFTPADDING", (0, 0), (-1, -1), 18),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("VALIGN",      (0, 0), (-1, -1), "TOP"),
        ("SPAN",        (0, 1), (1, 1)),
    ]))
    return tbl


def _company_block(data, company_fields, styles, page_width):
    """Tabla con los datos de identificación del proveedor."""
    rows = []
    pairs = list(zip(company_fields[::2], company_fields[1::2]))
    if len(company_fields) % 2:
        pairs.append((company_fields[-1], None))

    for left, right in pairs:
        left_val  = data.get(left["id"], "").strip() or "—"
        right_val = (data.get(right["id"], "").strip() or "—") if right else ""

        rows.append([
            Paragraph(left["label"], styles["company_label"]),
            Paragraph(left_val,      styles["company_value"]),
            Paragraph(right["label"] if right else "", styles["company_label"]),
            Paragraph(right_val,     styles["company_value"]),
        ])

    tbl = Table(rows, colWidths=["22%", "28%", "22%", "28%"])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, -1), GREEN_BG),
        ("TOPPADDING",  (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [WHITE, GREEN_BG]),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#c0c8a0")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return tbl


def _section_header(section, styles, page_width):
    """Banda verde para el título de sección."""
    num_p  = Paragraph(f"SECCIÓN {section['id']:02d}", styles["section_ref"])
    tit_p  = Paragraph(section["title"].upper(), styles["section_title"])
    ref_p  = Paragraph(section.get("ref", ""), styles["section_ref"])

    tbl = Table([[num_p], [tit_p], [ref_p]], colWidths=[page_width])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), GREEN_MID),
        ("TOPPADDING",    (0, 0), (0, 0), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 14),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 14),
    ]))
    return tbl


def _answer_for_question(q, data, styles):
    """Extrae y formatea la respuesta de una pregunta."""
    flowables = []
    qid = q["id"]
    qtype = q["type"]

    def val(key):
        v = data.get(key, "")
        return v.strip() if isinstance(v, str) else ", ".join(v) if isinstance(v, list) else ""

    # ── Número + texto de la pregunta ──────────────────────
    num_p  = Paragraph(f"Pregunta {q['num']:02d}", styles["q_num"])
    text_p = Paragraph(q["text"], styles["q_text"])

    if qtype in ("radio", "radio_text", "radio_number"):
        raw = val(qid)
        ans = raw if raw else "Sin respuesta"
        ans_style = styles["answer_value"] if raw else styles["answer_none"]

        flowables.append(Table(
            [[num_p, Paragraph("Respuesta:", styles["answer_label"]),
              Paragraph(ans, ans_style)]],
            colWidths=["15%", "18%", "67%"],
        ))
        flowables.append(text_p)

        # Campo extra
        extra_key = f"{qid}_extra"
        extra = val(extra_key)
        if extra:
            flowables.append(Paragraph(q.get("extra_label", "Información adicional:"),
                                       styles["answer_label"]))
            flowables.append(Paragraph(extra, styles["answer_value"]))

    elif qtype == "open":
        flowables.append(Table(
            [[num_p, Paragraph("Respuesta abierta:", styles["answer_label"])]],
            colWidths=["15%", "85%"],
        ))
        flowables.append(text_p)
        raw = val(qid)
        flowables.append(Paragraph(raw if raw else "Sin respuesta",
                                   styles["answer_value"] if raw else styles["answer_none"]))

    elif qtype == "numeric":
        raw = val(qid)
        unit = q.get("unit", "")
        ans = f"{raw} {unit}".strip() if raw else "Sin respuesta"
        flowables.append(Table(
            [[num_p, Paragraph("Valor:", styles["answer_label"]),
              Paragraph(ans, styles["answer_value"] if raw else styles["answer_none"])]],
            colWidths=["15%", "15%", "70%"],
        ))
        flowables.append(text_p)

    elif qtype == "numeric_multi":
        flowables.append(num_p)
        flowables.append(text_p)
        for sf in q.get("sub_fields", []):
            raw = val(sf["id"])
            unit = sf.get("unit", "")
            ans = f"{raw} {unit}".strip() if raw else "Sin respuesta"
            flowables.append(Table(
                [[Paragraph(sf["label"] + ":", styles["answer_label"]),
                  Paragraph(ans, styles["answer_value"] if raw else styles["answer_none"])]],
                colWidths=["45%", "55%"],
            ))

    elif qtype == "checkboxes":
        selected = data.getlist(qid) if hasattr(data, "getlist") else data.get(qid, [])
        if isinstance(selected, str):
            selected = [selected]
        ans = ", ".join(selected) if selected else "Sin respuesta"
        flowables.append(Table(
            [[num_p, Paragraph("Estándares seleccionados:", styles["answer_label"]),
              Paragraph(ans, styles["answer_value"] if selected else styles["answer_none"])]],
            colWidths=["15%", "30%", "55%"],
        ))
        flowables.append(text_p)
        extra_key = f"{qid}_extra"
        extra = val(extra_key)
        if extra:
            flowables.append(Paragraph(q.get("extra_label", "Otro:"), styles["answer_label"]))
            flowables.append(Paragraph(extra, styles["answer_value"]))

    flowables.append(Spacer(1, 4))
    flowables.append(HRFlowable(width="100%", thickness=0.3,
                                color=colors.HexColor("#d0d8b0"), spaceAfter=6))
    return flowables


def generate_pdf(form_data, output_path: str, sections: list, company_fields: list):
    """
    Genera el PDF completo del diagnóstico ESG.

    Args:
        form_data : dict con todos los valores del formulario (request.form)
        output_path: ruta donde se escribirá el archivo PDF
        sections  : lista de secciones (de form_data.py)
        company_fields: campos de identificación (de form_data.py)
    """
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=1.8 * cm,
        rightMargin=1.8 * cm,
        topMargin=1.5 * cm,
        bottomMargin=2 * cm,
        title="Diagnóstico ESG – GALILEO",
        author="Plataforma GALILEO",
    )

    PAGE_W = A4[0] - 3.6 * cm   # ancho útil
    styles = _build_styles()
    story  = []

    # ── Encabezado ──────────────────────────────────────────
    story.append(_header_table(styles))
    story.append(Spacer(1, 10))

    # ── Datos del proveedor ─────────────────────────────────
    story.append(Paragraph("DATOS DEL PROVEEDOR", styles["section_ref"]))
    story.append(Spacer(1, 4))
    story.append(_company_block(form_data, company_fields, styles, PAGE_W))
    story.append(Spacer(1, 14))

    # ── Secciones y preguntas ───────────────────────────────
    for section in sections:
        block = []
        block.append(_section_header(section, styles, PAGE_W))
        block.append(Spacer(1, 6))

        for q in section["questions"]:
            block += _answer_for_question(q, form_data, styles)

        block.append(Spacer(1, 10))
        story.append(KeepTogether(block[:6]))   # evita cortes abruptos
        story += block[6:]

    # ── Sección Otros (opcional) ────────────────────────────
    otros_val = form_data.get("otros_comentarios", "").strip() if hasattr(form_data, "get") else ""
    if otros_val:
        story.append(_section_header(
            {"id": 15, "title": "Otros comentarios y observaciones",
             "ref": "Sección opcional – carácter libre"},
            styles, PAGE_W,
        ))
        story.append(Spacer(1, 6))
        story.append(Paragraph(otros_val, styles["otros_text"]))
        story.append(Spacer(1, 12))

    # ── Pie de página ───────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=0.5, color=GREEN_MID, spaceAfter=6))
    story.append(Paragraph(
        "Diagnóstico de Sostenibilidad para Proveedores · Plataforma GALILEO · "
        "Confidencial – uso exclusivo para evaluación ESG interna · "
        f"Generado el {datetime.now().strftime('%d/%m/%Y')}",
        styles["footer"],
    ))

    doc.build(story)
    return output_path
