# ============================================================
#  GALILEO – Diagnóstico de Sostenibilidad para Proveedores
#  Datos del formulario: 14 secciones / 60 preguntas
#  Normativa: GRI 2021 | ISO 20400 | UNGPs | TCFD | ESRS | ISO 45001 | ISO 14001
# ============================================================

# Campos de identificación del proveedor (encabezado del formulario)
COMPANY_FIELDS = [
    {
        "id": "company_name",
        "label": "Razón social / Nombre de la empresa",
        "type": "text",
        "required": True,
        "placeholder": "Nombre completo de la organización",
    },
    {
        "id": "company_rut",
        "label": "RUT / NIF / Identificador fiscal",
        "type": "text",
        "required": True,
        "placeholder": "Ej: 76.123.456-7",
    },
    {
        "id": "company_sector",
        "label": "Sector / Industria",
        "type": "text",
        "required": True,
        "placeholder": "Ej: Manufactura, Servicios, Agroindustria…",
    },
    {
        "id": "company_country",
        "label": "País de operación principal",
        "type": "text",
        "required": True,
        "placeholder": "Ej: Argentina",
    },
    {
        "id": "company_contact",
        "label": "Nombre del responsable del formulario",
        "type": "text",
        "required": True,
        "placeholder": "Nombre y apellido",
    },
    {
        "id": "company_position",
        "label": "Cargo del responsable",
        "type": "text",
        "required": False,
        "placeholder": "Ej: Gerente de Sustentabilidad",
    },
    {
        "id": "company_email",
        "label": "Correo electrónico de contacto",
        "type": "email",
        "required": True,
        "placeholder": "contacto@empresa.com",
    },
    {
        "id": "company_employees",
        "label": "Número de empleados (aproximado)",
        "type": "number",
        "required": False,
        "placeholder": "Ej: 250",
    },
]


# ============================================================
#  TIPOS DE PREGUNTA:
#  "radio"         → Botones de opción (opciones en options[])
#  "open"          → Área de texto libre
#  "numeric"       → Campo numérico
#  "radio_text"    → Botones + campo de texto complementario
#  "radio_number"  → Botones + campo numérico complementario
#  "numeric_multi" → Varios campos numéricos (sub_fields[])
#  "checkboxes"    → Selección múltiple con campo adicional
# ============================================================

SECTIONS = [
    # ─────────────────────────────────────────────────────────
    {
        "id": 1,
        "title": "Gobernanza y Ética Empresarial",
        "ref": "GRI 2-23 · ISO 26000 · ESRS G1",
        "questions": [
            {
                "id": "q1",
                "num": 1,
                "text": "¿Su organización cuenta con un Código de Ética o Conducta formalmente aprobado por la alta dirección?",
                "type": "radio",
                "options": ["Sí", "No", "En desarrollo"],
            },
            {
                "id": "q2",
                "num": 2,
                "text": "¿Dispone de una política antisoborno y anticorrupción documentada y comunicada a todo el personal?",
                "type": "radio",
                "options": ["Sí", "No", "En desarrollo"],
            },
            {
                "id": "q3",
                "num": 3,
                "text": "¿Existe un canal de denuncias (whistleblower) confidencial disponible para empleados y partes interesadas externas?",
                "type": "radio",
                "options": ["Sí", "No"],
            },
            {
                "id": "q4",
                "num": 4,
                "text": "¿En los últimos 3 años se registraron casos confirmados de corrupción, soborno o conducta antiética? En caso afirmativo, ¿cómo se gestionaron?",
                "type": "radio_text",
                "options": ["Sí", "No"],
                "extra_label": "En caso afirmativo, describa cómo se gestionaron:",
                "extra_type": "textarea",
                "extra_trigger": "Sí",
                "placeholder": "Describa los casos y las acciones tomadas…",
            },
            {
                "id": "q5",
                "num": 5,
                "text": "¿Su empresa publica un informe de sostenibilidad o RSE anual, verificado por terceros?",
                "type": "radio",
                "options": ["Sí", "No", "En proceso"],
            },
        ],
    },
    # ─────────────────────────────────────────────────────────
    {
        "id": 2,
        "title": "Derechos Humanos y Condiciones Laborales",
        "ref": "UNGPs · GRI 401-407 · OIT · ESRS S1",
        "questions": [
            {
                "id": "q6",
                "num": 6,
                "text": "¿Cuenta con una política de derechos humanos alineada con los Principios Rectores de la ONU (UNGPs)?",
                "type": "radio",
                "options": ["Sí", "No", "En desarrollo"],
            },
            {
                "id": "q7",
                "num": 7,
                "text": "¿Realiza procesos de debida diligencia en derechos humanos en su cadena de valor?",
                "type": "radio",
                "options": ["Sí", "No", "En proceso"],
            },
            {
                "id": "q8",
                "num": 8,
                "text": "¿Garantiza el pago de un salario digno (living wage) a todos sus trabajadores, incluyendo subcontratistas directos?",
                "type": "radio",
                "options": ["Sí", "No", "Parcialmente"],
            },
            {
                "id": "q9",
                "num": 9,
                "text": "¿Permite y respeta la libertad de asociación sindical y la negociación colectiva de sus empleados?",
                "type": "radio",
                "options": ["Sí", "No", "No aplica"],
            },
            {
                "id": "q10",
                "num": 10,
                "text": "¿Tiene implementadas políticas para prevenir y gestionar el trabajo infantil y el trabajo forzoso?",
                "type": "radio",
                "options": ["Sí", "No", "En desarrollo"],
            },
            {
                "id": "q11",
                "num": 11,
                "text": "¿Cuál es la tasa de rotación de personal voluntaria en el último año fiscal?",
                "type": "numeric",
                "unit": "%",
                "placeholder": "Ej: 12.5",
            },
            {
                "id": "q12",
                "num": 12,
                "text": "¿Dispone de programas formales de capacitación y desarrollo profesional para sus empleados?",
                "type": "radio_number",
                "options": ["Sí", "No"],
                "extra_label": "Horas promedio de capacitación por empleado/año:",
                "extra_trigger": "Sí",
                "placeholder": "Ej: 40",
                "unit": "horas/año",
            },
            {
                "id": "q13",
                "num": 13,
                "text": "¿Cuenta con política de no discriminación e igualdad de oportunidades? ¿Incluye diversidad de género, etnia y discapacidad?",
                "type": "radio",
                "options": ["Sí", "No", "Parcialmente"],
            },
        ],
    },
    # ─────────────────────────────────────────────────────────
    {
        "id": 3,
        "title": "Salud y Seguridad Ocupacional",
        "ref": "ISO 45001 · GRI 403 · ESRS S1",
        "questions": [
            {
                "id": "q14",
                "num": 14,
                "text": "¿Cuenta con un Sistema de Gestión de Seguridad y Salud en el Trabajo (SST) certificado o en proceso de certificación?",
                "type": "radio",
                "options": ["Certificado ISO 45001", "En proceso de certificación", "No tiene"],
            },
            {
                "id": "q15",
                "num": 15,
                "text": "Indique su Tasa de Lesiones Registrables (TRIR) y Tasa de Días Perdidos (LTIFR) del último año.",
                "type": "numeric_multi",
                "sub_fields": [
                    {"id": "q15_trir", "label": "TRIR (Tasa de lesiones registrables)", "unit": "por millón h/h", "placeholder": "Ej: 2.3"},
                    {"id": "q15_ltifr", "label": "LTIFR (Tasa de días perdidos)", "unit": "por millón h/h", "placeholder": "Ej: 1.1"},
                ],
            },
            {
                "id": "q16",
                "num": 16,
                "text": "¿Se realizan simulacros de emergencia y programas de bienestar (salud mental, ergonomía) para los trabajadores?",
                "type": "radio",
                "options": ["Sí", "No", "Parcialmente"],
            },
        ],
    },
    # ─────────────────────────────────────────────────────────
    {
        "id": 4,
        "title": "Medio Ambiente – Cambio Climático y Energía",
        "ref": "GRI 302-305 · TCFD · SBTi · ESRS E1",
        "questions": [
            {
                "id": "q17",
                "num": 17,
                "text": "¿Ha realizado un inventario de Gases de Efecto Invernadero (GEI) de Alcances 1 y 2? ¿Incluye Alcance 3?",
                "type": "radio",
                "options": ["Sí – Alcances 1, 2 y 3", "Solo Alcances 1 y 2", "No"],
            },
            {
                "id": "q18",
                "num": 18,
                "text": "¿Cuál fue su consumo total de energía en el último año (MWh) y qué porcentaje proviene de fuentes renovables?",
                "type": "numeric_multi",
                "sub_fields": [
                    {"id": "q18_mwh", "label": "Consumo total de energía", "unit": "MWh", "placeholder": "Ej: 15000"},
                    {"id": "q18_pct", "label": "Porcentaje de energía renovable", "unit": "%", "placeholder": "Ej: 35"},
                ],
            },
            {
                "id": "q19",
                "num": 19,
                "text": "¿Tiene metas de reducción de emisiones GEI validadas por Science Based Targets initiative (SBTi) u otro estándar equivalente?",
                "type": "radio",
                "options": ["Sí – SBTi", "Sí – otro estándar", "En proceso", "No"],
            },
            {
                "id": "q20",
                "num": 20,
                "text": "¿Ha realizado análisis de riesgos climáticos físicos y de transición sobre sus operaciones y cadena de suministro?",
                "type": "radio",
                "options": ["Sí", "En proceso", "No"],
            },
            {
                "id": "q21",
                "num": 21,
                "text": "¿Cuenta con programa de eficiencia energética activo con metas medibles y seguimiento periódico?",
                "type": "radio_text",
                "options": ["Sí", "No"],
                "extra_label": "Describa las metas y el mecanismo de seguimiento:",
                "extra_type": "textarea",
                "extra_trigger": "Sí",
                "placeholder": "Ej: Reducción del 15 % al 2026 mediante renovación de equipos y monitoreo mensual…",
            },
        ],
    },
    # ─────────────────────────────────────────────────────────
    {
        "id": 5,
        "title": "Medio Ambiente – Agua y Biodiversidad",
        "ref": "GRI 303-304 · TNFD · ESRS E3-E4",
        "questions": [
            {
                "id": "q22",
                "num": 22,
                "text": "¿Cuál fue el volumen total de agua extraída (m³) en el último año? Diferencie por fuente (superficial, subterránea, municipal).",
                "type": "open",
                "placeholder": "Ej: Superficial: 5 000 m³ · Subterránea: 2 000 m³ · Municipal: 8 000 m³ · Total: 15 000 m³",
            },
            {
                "id": "q23",
                "num": 23,
                "text": "¿Sus instalaciones se ubican en zonas de estrés hídrico alto o muy alto según WRI Aqueduct u herramienta equivalente?",
                "type": "radio",
                "options": ["Sí", "No", "Evaluación en curso"],
            },
            {
                "id": "q24",
                "num": 24,
                "text": "¿Cuenta con política de protección de la biodiversidad y realiza evaluaciones de impacto en ecosistemas?",
                "type": "radio",
                "options": ["Sí", "No", "En desarrollo"],
            },
        ],
    },
    # ─────────────────────────────────────────────────────────
    {
        "id": 6,
        "title": "Medio Ambiente – Residuos y Economía Circular",
        "ref": "GRI 306 · ESRS E5 · ISO 14001",
        "questions": [
            {
                "id": "q25",
                "num": 25,
                "text": "¿Cuántas toneladas de residuos generó en el último año? Indique el desglose: peligrosos, no peligrosos, reciclados.",
                "type": "open",
                "placeholder": "Ej: Peligrosos: 50 t · No peligrosos: 300 t · Reciclados: 120 t · Total: 470 t",
            },
            {
                "id": "q26",
                "num": 26,
                "text": "¿Tiene implementada una estrategia de economía circular (diseño para el desmontaje, reutilización, remanufactura)?",
                "type": "radio",
                "options": ["Sí", "No", "En desarrollo"],
            },
            {
                "id": "q27",
                "num": 27,
                "text": "¿Ha implementado medidas específicas para reducir el uso de plásticos de un solo uso en sus productos o embalajes?",
                "type": "radio",
                "options": ["Sí", "No", "En proceso"],
            },
        ],
    },
    # ─────────────────────────────────────────────────────────
    {
        "id": 7,
        "title": "Cadena de Suministro Sostenible",
        "ref": "ISO 20400 · GRI 2-6 · ESRS G1",
        "questions": [
            {
                "id": "q28",
                "num": 28,
                "text": "¿Cuenta con una política de compras sostenibles que incorpore criterios ESG (ambiental, social, gobernanza)?",
                "type": "radio",
                "options": ["Sí", "No", "En desarrollo"],
            },
            {
                "id": "q29",
                "num": 29,
                "text": "¿Aplica criterios de sostenibilidad en la selección y evaluación periódica de sus propios proveedores?",
                "type": "radio_number",
                "options": ["Sí", "No"],
                "extra_label": "Porcentaje de proveedores evaluados con criterios ESG:",
                "extra_trigger": "Sí",
                "placeholder": "Ej: 65",
                "unit": "%",
            },
            {
                "id": "q30",
                "num": 30,
                "text": "¿Qué porcentaje de su gasto en compras corresponde a proveedores locales (dentro de un radio de 150 km o en la misma región)?",
                "type": "numeric",
                "unit": "%",
                "placeholder": "Ej: 40",
            },
            {
                "id": "q31",
                "num": 31,
                "text": "¿Realiza auditorías de sostenibilidad o visitas a instalaciones de sus proveedores críticos?",
                "type": "radio_text",
                "options": ["Sí", "No"],
                "extra_label": "Frecuencia de las auditorías:",
                "extra_type": "text",
                "extra_trigger": "Sí",
                "placeholder": "Ej: Anual para proveedores estratégicos, bienal para el resto",
            },
            {
                "id": "q32",
                "num": 32,
                "text": "¿Exige a sus proveedores estratégicos la firma de un Código de Conducta de Proveedores con requisitos ESG?",
                "type": "radio",
                "options": ["Sí", "No"],
            },
            {
                "id": "q33",
                "num": 33,
                "text": "¿Tiene programa de desarrollo de capacidades ESG (formación, asistencia técnica) para sus proveedores PYME?",
                "type": "radio",
                "options": ["Sí", "No"],
            },
            {
                "id": "q34",
                "num": 34,
                "text": "¿Sus contratos con proveedores incluyen cláusulas de sostenibilidad, penalizaciones o incentivos por desempeño ESG?",
                "type": "radio",
                "options": ["Sí", "No", "En implementación"],
            },
        ],
    },
    # ─────────────────────────────────────────────────────────
    {
        "id": 8,
        "title": "Minerales y Materiales Críticos",
        "ref": "OCDE Guía Minerales · GRI 2-6 · ESRS E5",
        "questions": [
            {
                "id": "q35",
                "num": 35,
                "text": "¿Utiliza minerales de zonas de conflicto (3TG: estaño, tántalo, tungsteno, oro) en sus productos o procesos?",
                "type": "radio",
                "options": ["Sí", "No", "Bajo evaluación"],
            },
            {
                "id": "q36",
                "num": 36,
                "text": "¿Puede rastrear el origen de sus materias primas críticas hasta el extractor o productor primario (trazabilidad)?",
                "type": "radio",
                "options": ["Sí – trazabilidad completa", "Parcialmente", "No"],
            },
            {
                "id": "q37",
                "num": 37,
                "text": "¿Qué porcentaje de los materiales utilizados en sus productos son reciclados o de origen secundario?",
                "type": "numeric",
                "unit": "%",
                "placeholder": "Ej: 20",
            },
        ],
    },
    # ─────────────────────────────────────────────────────────
    {
        "id": 9,
        "title": "Innovación, Productos y Servicios Sostenibles",
        "ref": "GRI 301 · ESRS E5 · ISO 14006",
        "questions": [
            {
                "id": "q38",
                "num": 38,
                "text": "¿Incorpora criterios de ecodiseño (análisis de ciclo de vida, durabilidad, reparabilidad) en el desarrollo de sus productos?",
                "type": "radio",
                "options": ["Sí", "No", "En proceso"],
            },
            {
                "id": "q39",
                "num": 39,
                "text": "¿Qué porcentaje de su portafolio de productos está etiquetado con certificación ambiental o social reconocida?",
                "type": "numeric",
                "unit": "%",
                "placeholder": "Ej: 25",
            },
            {
                "id": "q40",
                "num": 40,
                "text": "¿Invierte en I+D orientada a soluciones de sostenibilidad o transición verde? ¿Cuál es el % del presupuesto de I+D destinado a esto?",
                "type": "radio_number",
                "options": ["Sí", "No"],
                "extra_label": "Porcentaje del presupuesto de I+D destinado a sostenibilidad:",
                "extra_trigger": "Sí",
                "placeholder": "Ej: 18",
                "unit": "%",
            },
            {
                "id": "q41",
                "num": 41,
                "text": "¿Sus embalajes y materiales de marketing son 100 % reciclables, compostables o reutilizables?",
                "type": "radio",
                "options": ["Sí", "No", "En transición"],
            },
        ],
    },
    # ─────────────────────────────────────────────────────────
    {
        "id": 10,
        "title": "Comunidades y Valor Social",
        "ref": "GRI 411-413 · UNGPs · ESRS S3",
        "questions": [
            {
                "id": "q42",
                "num": 42,
                "text": "¿Realiza evaluaciones de impacto en las comunidades donde opera (ESIA – Environmental and Social Impact Assessment)?",
                "type": "radio",
                "options": ["Sí", "No", "En proceso"],
            },
            {
                "id": "q43",
                "num": 43,
                "text": "¿Tiene programas de inversión social comunitaria activos? Indique el monto invertido y número de beneficiarios.",
                "type": "radio_text",
                "options": ["Sí", "No"],
                "extra_label": "Monto invertido y número de beneficiarios:",
                "extra_type": "text",
                "extra_trigger": "Sí",
                "placeholder": "Ej: USD 50 000 – 1 200 beneficiarios directos",
            },
            {
                "id": "q44",
                "num": 44,
                "text": "¿Dispone de mecanismos formales de consulta y participación de comunidades indígenas o en situación de vulnerabilidad?",
                "type": "radio",
                "options": ["Sí", "No", "No aplica"],
            },
            {
                "id": "q45",
                "num": 45,
                "text": "¿Tiene política activa de fomento a la contratación de población vulnerable (personas con discapacidad, jóvenes, mujeres)?",
                "type": "radio_number",
                "options": ["Sí", "No"],
                "extra_label": "Porcentaje de este grupo en la plantilla total:",
                "extra_trigger": "Sí",
                "placeholder": "Ej: 12",
                "unit": "%",
            },
        ],
    },
    # ─────────────────────────────────────────────────────────
    {
        "id": 11,
        "title": "Cumplimiento Legal y Gestión de Riesgos ESG",
        "ref": "GRI 2-27 · ISO 31000 · ESRS G1",
        "questions": [
            {
                "id": "q46",
                "num": 46,
                "text": "¿Ha recibido sanciones, multas o incumplimientos regulatorios ambientales o laborales en los últimos 3 años?",
                "type": "radio_text",
                "options": ["Sí", "No"],
                "extra_label": "Descripción de las sanciones y acciones correctivas:",
                "extra_type": "textarea",
                "extra_trigger": "Sí",
                "placeholder": "Describa el tipo de infracción, la autoridad reguladora y las medidas adoptadas…",
            },
            {
                "id": "q47",
                "num": 47,
                "text": "¿Su organización cuenta con un sistema formal de identificación, evaluación y gestión de riesgos ESG integrado al ERM corporativo?",
                "type": "radio",
                "options": ["Sí", "No", "En desarrollo"],
            },
            {
                "id": "q48",
                "num": 48,
                "text": "¿Posee certificaciones ambientales vigentes (ISO 14001, EMAS, LEED, similar)? Indique cuáles y sus fechas de vencimiento.",
                "type": "radio_text",
                "options": ["Sí", "No"],
                "extra_label": "Listado de certificaciones y fechas de vencimiento:",
                "extra_type": "textarea",
                "extra_trigger": "Sí",
                "placeholder": "Ej: ISO 14001 – vence 31/03/2026 · LEED Gold – permanente",
            },
            {
                "id": "q49",
                "num": 49,
                "text": "¿Tiene identificados y mapeados todos los permisos ambientales vigentes necesarios para sus operaciones?",
                "type": "radio",
                "options": ["Sí", "No", "Parcialmente"],
            },
            {
                "id": "q50",
                "num": 50,
                "text": "¿Realiza ejercicios periódicos de materialidad ESG para priorizar sus temas de sostenibilidad más relevantes?",
                "type": "radio_text",
                "options": ["Sí", "No"],
                "extra_label": "Frecuencia del análisis de materialidad:",
                "extra_type": "text",
                "extra_trigger": "Sí",
                "placeholder": "Ej: Anual / Bienal",
            },
        ],
    },
    # ─────────────────────────────────────────────────────────
    {
        "id": 12,
        "title": "Digitalización, Datos y Privacidad",
        "ref": "ISO 27001 · GRI 418 · ESRS G1",
        "questions": [
            {
                "id": "q51",
                "num": 51,
                "text": "¿Cuenta con una política de seguridad de la información certificada o alineada a la norma ISO 27001?",
                "type": "radio",
                "options": ["Certificado ISO 27001", "Alineado sin certificar", "No tiene"],
            },
            {
                "id": "q52",
                "num": 52,
                "text": "¿Ha sufrido incidentes de ciberseguridad o filtraciones de datos personales en los últimos 3 años? ¿Cómo fueron gestionados?",
                "type": "radio_text",
                "options": ["Sí", "No"],
                "extra_label": "Descripción de los incidentes y gestión realizada:",
                "extra_type": "textarea",
                "extra_trigger": "Sí",
                "placeholder": "Describa el tipo de incidente, alcance y las medidas de respuesta implementadas…",
            },
            {
                "id": "q53",
                "num": 53,
                "text": "¿Tiene implementado un programa de privacidad de datos (Privacy by Design) y gestión del ciclo de vida de los datos personales?",
                "type": "radio",
                "options": ["Sí", "No", "En implementación"],
            },
        ],
    },
    # ─────────────────────────────────────────────────────────
    {
        "id": 13,
        "title": "Finanzas Sostenibles y Reporte",
        "ref": "GRI 2-14 · TCFD · ESRS · SASB",
        "questions": [
            {
                "id": "q54",
                "num": 54,
                "text": "¿Ha emitido instrumentos de deuda sostenible (bonos verdes, bonos sociales, bonos vinculados a sostenibilidad)?",
                "type": "radio_text",
                "options": ["Sí", "No", "En evaluación"],
                "extra_label": "Monto y tipo de instrumento emitido:",
                "extra_type": "text",
                "extra_trigger": "Sí",
                "placeholder": "Ej: Bono verde USD 10 M – emisión 2023",
            },
            {
                "id": "q55",
                "num": 55,
                "text": "¿Sus estados financieros incorporan la valoración de pasivos ambientales o riesgos climáticos?",
                "type": "radio",
                "options": ["Sí", "No", "En proceso"],
            },
            {
                "id": "q56",
                "num": 56,
                "text": "¿Utiliza estándares GRI, SASB, TCFD, TNFD o ESRS para la elaboración de sus reportes de sostenibilidad?",
                "type": "checkboxes",
                "options": ["GRI 2021", "SASB", "TCFD", "TNFD", "ESRS / CSRD", "Otro"],
                "extra_label": "Si seleccionó 'Otro', especifique el estándar utilizado:",
                "extra_trigger": "Otro",
                "placeholder": "Ej: CDP, B Corp, GHG Protocol…",
            },
            {
                "id": "q57",
                "num": 57,
                "text": "¿Ha realizado una evaluación de doble materialidad (impactos de adentro hacia afuera y de afuera hacia adentro)?",
                "type": "radio",
                "options": ["Sí", "No", "En proceso"],
            },
        ],
    },
    # ─────────────────────────────────────────────────────────
    {
        "id": 14,
        "title": "Estrategia y Compromiso de Alta Dirección",
        "ref": "GRI 2-22 · ESRS G1 · ISO 26000",
        "questions": [
            {
                "id": "q58",
                "num": 58,
                "text": "¿La estrategia corporativa tiene metas ESG integradas con KPI y horizonte temporal definido?",
                "type": "radio",
                "options": ["Sí", "No", "En desarrollo"],
            },
            {
                "id": "q59",
                "num": 59,
                "text": "¿La remuneración variable de la alta dirección está vinculada al cumplimiento de objetivos de sostenibilidad?",
                "type": "radio",
                "options": ["Sí", "No", "Parcialmente"],
            },
            {
                "id": "q60",
                "num": 60,
                "text": "¿Cuál es la principal barrera que enfrenta su organización para avanzar en sostenibilidad, y qué apoyo requeriría de sus clientes/compradores para superarla?",
                "type": "open",
                "placeholder": "Comparta sus reflexiones con total libertad. Esta información es clave para diseñar programas de apoyo…",
            },
        ],
    },
]
