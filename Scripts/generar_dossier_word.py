# -*- coding: utf-8 -*-
"""
Genera el dossier EUDR como Word (.docx) para ISCAM-UP.
Estilo: Memorando de Trabajo Interno.
"""
from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

# ─── Colores institucionales ISCAM ───────────────────────────────────────────
COLOR_TITLE   = RGBColor(0x1A, 0x3A, 0x5C)  # azul oscuro
COLOR_H1      = RGBColor(0x1A, 0x3A, 0x5C)
COLOR_H2      = RGBColor(0x2E, 0x6D, 0xA4)  # azul medio
COLOR_H3      = RGBColor(0x4A, 0x90, 0xC0)  # azul claro
COLOR_BODY    = RGBColor(0x1E, 0x1E, 0x1E)
COLOR_NOTE    = RGBColor(0x55, 0x55, 0x55)
COLOR_TABLE_H = RGBColor(0x1A, 0x3A, 0x5C)
COLOR_ALT     = RGBColor(0xF2, 0xF5, 0xF9)

FONT = "Calibri"

# ─── Helpers ────────────────────────────────────────────────────────────────

def set_cell_bg(cell, hex_color):
    """Fondo de celda."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)

def set_cell_border(cell, **kwargs):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement("w:tcBorders")
    for edge in ("top","left","bottom","right"):
        tag = OxmlElement(f"w:{edge}")
        tag.set(qn("w:val"), "single")
        tag.set(qn("w:sz"), "4")
        tag.set(qn("w:space"), "0")
        tag.set(qn("w:color"), "AAAAAA")
        tcBorders.append(tag)
    tcPr.append(tcBorders)

def bold_cell(cell):
    for p in cell.paragraphs:
        for run in p.runs:
            run.bold = True

def add_styled_table(doc, headers, rows, col_widths=None):
    """Tabla con header oscuro, filas alternadas, bordes suaves."""
    n_cols = len(headers)
    table = doc.add_table(rows=1+len(rows), cols=n_cols)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.LEFT

    # Header row
    hdr_row = table.rows[0]
    for i, h in enumerate(headers):
        cell = hdr_row.cells[i]
        cell.text = ""
        p = cell.paragraphs[0]
        run = p.add_run(h)
        run.bold = True
        run.font.color.rgb = RGBColor(0xFF,0xFF,0xFF)
        run.font.size = Pt(9)
        run.font.name = FONT
        set_cell_bg(cell, "1A3A5C")
        set_cell_border(cell)
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)

    # Data rows
    for r_idx, row in enumerate(rows):
        tr = table.rows[r_idx+1]
        bg = "F2F5F9" if r_idx % 2 == 0 else "FFFFFF"
        for c_idx, val in enumerate(row):
            cell = tr.cells[c_idx]
            cell.text = ""
            p = cell.paragraphs[0]
            run = p.add_run(str(val))
            run.font.size = Pt(9)
            run.font.name = FONT
            run.font.color.rgb = COLOR_BODY
            set_cell_bg(cell, bg)
            set_cell_border(cell)
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)

    # Col widths
    if col_widths:
        for row in table.rows:
            for i, w in enumerate(col_widths):
                row.cells[i].width = Cm(w)

    return table


def h1(doc, text):
    p = doc.add_heading(text, level=1)
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(4)
    for run in p.runs:
        run.font.color.rgb = COLOR_H1
        run.font.name = FONT
        run.font.size = Pt(14)
        run.bold = True
    return p

def h2(doc, text):
    p = doc.add_heading(text, level=2)
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(3)
    for run in p.runs:
        run.font.color.rgb = COLOR_H2
        run.font.name = FONT
        run.font.size = Pt(12)
        run.bold = True
    return p

def h3(doc, text):
    p = doc.add_heading(text, level=3)
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    for run in p.runs:
        run.font.color.rgb = COLOR_H3
        run.font.name = FONT
        run.font.size = Pt(10.5)
        run.bold = True
    return p

def body(doc, text, bold=False, italic=False, color=None, size=10.5):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = FONT
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = color
    else:
        run.font.color.rgb = COLOR_BODY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = Pt(14)
    return p

def note(doc, text):
    """Nota al pie como bloque aside."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.5)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = Pt(13)
    run = p.add_run(text)
    run.font.name = FONT
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
    run.italic = True
    return p

def rule(doc):
    """Separador visual."""
    p = doc.add_paragraph()
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "6")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), "1A3A5C")
    pBdr.append(bottom)
    pPr.append(pBdr)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)

def bullet(doc, text, level=0):
    p = doc.add_paragraph(style="List Bullet")
    run = p.add_run(text)
    run.font.name = FONT
    run.font.size = Pt(10)
    run.font.color.rgb = COLOR_BODY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.left_indent = Cm(0.5 + level*0.4)
    return p


# ─── Documento principal ───────────────────────────────────────────────────

doc = Document()

# Márgenes
section = doc.sections[0]
section.top_margin    = Cm(2.5)
section.bottom_margin = Cm(2.5)
section.left_margin   = Cm(3.0)
section.right_margin  = Cm(2.5)

# ── Encabezado del memo ────────────────────────────────────────────────────
tbl = doc.add_table(rows=1, cols=2)
tbl.alignment = WD_TABLE_ALIGNMENT.LEFT
tbl.style = "Table Grid"

# Celda izquierda: ISCAM
lc = tbl.rows[0].cells[0]
lc.width = Cm(10)
lc.text = ""
lp = lc.paragraphs[0]
r1 = lp.add_run("GRUPO ISCAM\n")
r1.font.name = FONT
r1.font.size = Pt(9)
r1.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
r2 = lp.add_run("Universidad Peruana")
r2.font.name = FONT
r2.font.size = Pt(9)
r2.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
lp.paragraph_format.space_after = Pt(0)
set_cell_bg(lc, "F2F5F9")
lcPr = lc._tc.get_or_add_tcPr()
lcB = OxmlElement("w:tcBorders")
for edge in ("top","left","bottom","right"):
    t = OxmlElement(f"w:{edge}")
    t.set(qn("w:val"), "none")
    lcB.append(t)
lcPr.append(lcB)

# Celda derecha: MEMORANDO
rc = tbl.rows[0].cells[1]
rc.width = Cm(8)
rc.text = ""
rp = rc.paragraphs[0]
rh = rp.add_run("MEMORANDO DE TRABAJO INTERNO\n")
rh.font.name = FONT
rh.font.size = Pt(13)
rh.font.bold = True
rh.font.color.rgb = COLOR_TITLE
rd = rp.add_run("Uso interno — Grupo de Investigación ISCAM")
rd.font.name = FONT
rd.font.size = Pt(8.5)
rd.font.color.rgb = RGBColor(0x77, 0x77, 0x77)
rp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
rp.paragraph_format.space_after = Pt(0)
set_cell_bg(rc, "E8EEF5")

doc.add_paragraph()

# ── Datos del memo ────────────────────────────────────────────────────────
meta_tbl = doc.add_table(rows=4, cols=2)
meta_tbl.style = "Table Grid"
meta_data = [
    ("Para:", "Miembros del Grupo ISCAM — UP"),
    ("De:", "Mavis — Inteligencia y Datos, Grupo ISCAM"),
    ("Fecha:", "12 de octubre de 2026"),
    ("Asunto:", "Cooperativas Peruanas + EUDR — Dossier de Inteligencia, v3.0 con citas"),
]
for i, (label, value) in enumerate(meta_data):
    row = meta_tbl.rows[i]
    lc, rc = row.cells
    lc.text = ""
    lp = lc.paragraphs[0]
    r = lp.add_run(label)
    r.font.name = FONT
    r.font.size = Pt(9.5)
    r.bold = True
    r.font.color.rgb = COLOR_TITLE
    lp.paragraph_format.space_after = Pt(0)

    rc.text = ""
    rp = rc.paragraphs[0]
    rv = rp.add_run(value)
    rv.font.name = FONT
    rv.font.size = Pt(9.5)
    rv.font.color.rgb = COLOR_BODY
    rp.paragraph_format.space_after = Pt(0)

    set_cell_bg(lc, "E8EEF5")
    set_cell_border(lc)
    set_cell_bg(rc, "FFFFFF")
    set_cell_border(rc)

# Espacio
doc.add_paragraph()

# ── Resumen ejecutivo ──────────────────────────────────────────────────────
h1(doc, "Resumen Ejecutivo")
body(doc,
    "Perú está clasificado como país de riesgo estándar bajo el EUDR (Reglamento de Ejecución UE 2025/1093, "
    "22 de mayo de 2025). La Debida Diligencia completa en tres etapas es obligatoria para todo lote de "
    "café, cacao o palma aceitera que ingrese al mercado europeo. El país lleva ventaja en geolocalización "
    "(150,000+ polígonos a través de AGRODIGITAL), pero el cuello de botella real es documental: el 80% de "
    "los pequeños productores carece de título de propiedad claro. El estudio de Trase (septiembre 2026) añade "
    "una capa estratégica: el 79% del café global es manejado por importadores que también surten al mercado "
    "de la UE — por lo que la presión EUDR se extiende a toda la cadena, no solo a los lotes europeos."
)

rule(doc)

# ── 1. CONTEXTO NORMATIVO ────────────────────────────────────────────────
h1(doc, "1. Contexto Normativo")

body(doc,
    "El Reglamento (UE) 2023/1115 (EUDR) prohíbe importar, exportar o comercializar en la Unión Europea "
    "productos derivados de ganado bovino, cacao, café, palma aceitera, caucho, soja o madera que provengan "
    "de tierras deforestadas después del 31 de diciembre de 2020, que se hayan producido en violación de la "
    "legislación del país de origen, o que no estén respaldados por una Declaración de Debida Diligencia (DDS).",
    bold=False
)
note(doc, "[^1] Reglamento (UE) 2023/1115 (EUDR). eur-lex.europa.eu/eli/reg/2023/1115/oj/eng")

h2(doc, "1.1 Las tres condiciones para exportar a la UE")
bullet(doc, "Libre de deforestación — el suelo donde se produjo no fue deforestado después del 31/12/2020.")
bullet(doc, "Producción legal — se respetó la legislación aplicable del país de origen (tenencia de tierra, uso de suelo, derechos laborales, derechos de pueblos indígenas).")
bullet(doc, "Debida Diligencia (DD) — el importador europeo presenta una DDS ante el sistema TRACES/NTIS de la UE.")

h2(doc, "1.2 Las tres etapas de la DD completa (obligatoria para riesgo estándar)")
add_styled_table(doc,
    ["Etapa", "Qué exige", "Depende de"],
    [
        ["1. Recopilación de información", "Geolocalización WGS-84, código HS, cantidad, proveedor, fecha de cosecha, documentos de tenencia, historial de cobertura, registros de acopio", "El exportador peruano"],
        ["2. Evaluación de riesgos", "El importador UE determina si hay riesgo de incumplimiento de las condiciones 1 y 2", "Datos que solo el exportador puede proporcionar"],
        ["3. Medidas de mitigación", "Si se identifican riesgos, deben tomarse medidas antes del envío", "Si no se puede mitigar, no se envía el lote"],
    ],
    col_widths=[4.5, 9.0, 5.0]
)
note(doc, "[^1] Reglamento (UE) 2023/1115, Artículos 3 y 8-11.")

body(doc,
    "Nota: La DD simplificada (Artículo 13) — que solo requiere recopilación de información, sin evaluación ni "
    "mitigación de riesgos — NO aplica para Perú. Solo la aplica el importador UE cuando se abastece de un país "
    "clasificado como bajo riesgo. Perú está clasificado como riesgo estándar.",
    italic=True, color=RGBColor(0xAA, 0x00, 0x00)
)
note(doc, "[^2] Reglamento de Ejecución (UE) 2025/1093 (22 de mayo de 2025). Anexo: 140 países bajo riesgo, 4 alto riesgo, el resto estándar. eur-lex.europa.eu/eli/reg_impl/2025/1093/oj/eng")

h2(doc, "1.3 Fecha de entrada en vigencia")
body(doc,
    "30 de diciembre de 2026 para grandes y medianas empresas; 30 de junio de 2027 para micro y pequeñas empresas. "
    "Desde 2025, compradores europeos ya exigen evidencias de cumplimiento."
)
note(doc, "[^3] Reglamento de Postergación del EUDR, DOUE. Ver también Trase, EU Deforestation Regulation explained, trase.earth; [^4] PROMPERÚ, gob.pe/institucion/promperu/noticias/1354427")

h2(doc, "1.4 Clasificación de riesgo país")
add_styled_table(doc,
    ["Categoría", "Control autoridades UE", "DD requerida", "Países ejemplo"],
    [
        ["Bajo riesgo", "1% operadores/año", "Simplificada (solo recopilación)", "UE, Chile, Costa Rica, Kenia, Laos, PNG, Ruanda, Vietnam, EE.UU., China"],
        ["Estándar (Perú)", "3% operadores/año", "Completa en 3 etapas", "Perú, Brasil, Colombia, Indonesia, Bolivia, Paraguay, México"],
        ["Alto riesgo", "9% operadores + 9% volumen", "Completa reforzada", "Bielorrusia, Rusia, Myanmar, Corea del Norte"],
    ],
    col_widths=[3.2, 3.5, 4.0, 7.8]
)
note(doc, "[^2] Reglamento de Ejecución (UE) 2025/1093. Clasificación publicada el 22 de mayo de 2025.")

h2(doc, "1.5 Información que debe entregar el exportador por lote")
add_styled_table(doc,
    ["#", "Dato requerido", "Detalle"],
    [
        ["1", "Geolocalización", "WGS-84 (EPSG:4326): punto si <4 ha, polígono obligatorio si ≥4 ha. Mín. 6 decimales."],
        ["2", "Ubicación", "País + departamento + provincia (ej: Cajamarca – Jaén)"],
        ["3", "Código HS", "Código arancelario del producto"],
        ["4", "Proveedor", "Nombre, RUC y dirección"],
        ["5", "Comprador", "Nombre y dirección"],
        ["6", "Fecha de cosecha", ""],
        ["7", "Tenencia de tierra", "Título SUNARP, constancia COFOPRI, contrato de cesión en uso"],
        ["8", "Cobertura forestal", "Informe deforestación post-2020 (GeoBosques, Global Forest Watch)"],
        ["9", "Registros de acopio", "Guías de remisión, actas de entrega, pesaje — vínculo parcela-lote"],
        ["10", "Conservación", "5 años de todos los documentos"],
    ],
    col_widths=[0.7, 3.0, 14.8]
)
note(doc, "[^5] CBI, cbi.eu/market-information/coffee/tips-become-eudr-compliant; AYP Digital, aypdigital.com/blog/eudr-reglamento-ue-deforestacion-trazabilidad-exportadores-peru/")

body(doc,
    "~80% de los pequeños productores carece de título de propiedad claro. Sin documento de tenencia en regla, "
    "el expediente EUDR no se construye válidamente, por más buena que sea la geolocalización.",
    bold=True, color=RGBColor(0xAA, 0x00, 0x00)
)
note(doc, "[^6] AYP Digital, aypdigital.com/blog/eudr-reglamento-ue-deforestacion-trazabilidad-exportadores-peru/; CamcaféPeru, camcafeperu.com.pe/EN/article.php?id=236")

# ── 2. PANORAMA NACIONAL ────────────────────────────────────────────────────
h1(doc, "2. El Panorama Nacional")
body(doc,
    "MIDAGRI lidera una estrategia integral con geolocalización a través de AGRODIGITAL, interoperabilidad con "
    "FAO WHISP y Global Forest Watch Pro, y convenios con MINCETUR, ADEX, GIZ, IICA, Cooperación Suiza, "
    "Helvetas Perú y Solidaridad."
)

h2(doc, "2.1 Indicadores clave")
add_styled_table(doc,
    ["Indicador", "Dato", "Fuente"],
    [
        ["Polígonos geolocalizados", "+150,000 (café, cacao, palma)", "MIDAGRI / AGRODIGITAL"],
        ["Productores en PPA", "2.03 millones (410,000 café/cacao/palma)", "MIDAGRI"],
        ["Fincas verificadas libre deforestación post-2020", "99%", "MIDAGRI"],
        ["Sacos café con trazabilidad avanzada", "1.75 millones", "MIDAGRI"],
        ["Exportadores alineados EUDR", "150+", "MIDAGRI"],
        ["Productores en zonas pre-2020", "99% (inscritos PPA)", "MIDAGRI"],
    ],
    col_widths=[7.5, 5.0, 6.0]
)
note(doc, "[^7] MIDAGRI, múltiples comunicados: gob.pe/institucion/midagri/noticias/1319697; /1177401; /1319247; /1294143; /1255233; /1235541")

h2(doc, "2.2 Actores públicos y convenios")
add_styled_table(doc,
    ["Actor", "Rol"],
    [
        ["MIDAGRI", "Líder estrategia. Geolocalización (AGRODIGITAL/PPA), plataforma trazabilidad, coordinación interinstitucional"],
        ["MINCETUR / PROMPERÚ", "Preparación exportadores. Programa DD con 21 organizaciones y 7,880 productores (2025)"],
        ["Ministerio del Ambiente / GeoBosques", "Cruce parcelas con mapas de cobertura forestal"],
        ["ADEX", "Alianza estratégica MIDAGRI-MINCETUR-ADEX (convenio sep 2025)"],
        ["GIZ", "Apoyo técnico geolocalización y estrategia EUDR"],
        ["IICA", "Coordinación técnica, capacitación, articulación con gobiernos regionales"],
        ["FAO", "WHISP como plataforma de interoperabilidad internacional"],
        ["Cooperación Suiza / Helvetas / Solidaridad", "Financiamiento proyectos trazabilidad (AGROInnova, Amazonía Link)"],
    ],
    col_widths=[4.5, 14.0]
)
note(doc, "[^8] PROMPERÚ, gob.pe/institucion/promperu/noticias/1354427; [^9] MIDAGRI, gob.pe/institucion/midagri/noticias/1250933")

h2(doc, "2.3 Infraestructura pública en uso")
body(doc, "AGRODIGITAL / Identidad Digital del Productor Agrario (MIDAGRI): aplicativo móvil con GPS offline, cruce con GeoBosques, emisión de Constancia de Libre Deforestación. Objetivo: 100% productores en PPA + 50% con parcelas como polígono.", bold=False)
note(doc, "[^7][^11] MIDAGRI, gob.pe/institucion/midagri/noticias/1294143")
body(doc, "GeoBosques (Ministerio del Ambiente): cruza parcelas con mapas de cobertura forestal. Genera informe de 'cero deforestación' para el expediente DD.")
body(doc, "Plataforma de trazabilidad MIDAGRI (en desarrollo): conectará la chacra con el contenedor. Vinculación DNI del productor en manifiesto de carga con parcelas georreferenciadas. Esperada para 2026.")
note(doc, "[^7]")
body(doc, "MICACAO (Helvetas / Open Cocoa Chain): trazabilidad digital para cacao. Colombia y Perú. Valida cero deforestación en cadena de valor.")
note(doc, "[^12] GIZ, giz.de/en/downloads/giz2025-es-latin-america-digital-traceability-tools.pdf")

# ── 3. UNIVERSO DE COOPERATIVAS ────────────────────────────────────────────
h1(doc, "3. El Universo de Cooperativas y Organizaciones")

h2(doc, "3.1 Cadena de café")
h3(doc, "Nivel avanzado — trazabilidad operativa y exportadores activos")

add_styled_table(doc,
    ["Cooperativa / Org.", "Ubicación", "Miembros", "Estado EUDR", "Piloto 2025"],
    [
        ["Cenfrocafé", "Jaén, Cajamarca / Amazonas", "3,000", "Trazabilidad completa, RA, FT, orgánico. Filial Cenfrocafé AG (Suiza).", "Beneke (DE), ICAM (IT)"],
        ["APROCAM", "Bagua, Amazonas", "—", "Pilotos MIDAGRI, certificaciones internacionales.", "Sí"],
        ["PIMCOS Coffee", "Jaén, Cajamarca", "—", "Pilotos MIDAGRI.", "45 ton café"],
        ["Satipo (7 orgs.)", "Satipo, Junín", "3,350", "Programa SAFE (3 módulos). Misión EU-Holanda-DE.", "Sí"],
        ["Sonomoro", "Pangoa, Junín", "—", "Misma zona Satipo. Programa SAFE.", "—"],
        ["ACPC Pichanaki, Kemito Ene", "Junín", "—", "Visitadas misión europea. Sistemas agroforestales.", "—"],
        ["Cuencas del Huallaga", "San Martín", "—", "Pilotos MIDAGRI DD.", "—"],
        ["Org. Café Organero Gera", "Moyobamba, San Martín", "—", "Pilotos MIDAGRI 2025.", "—"],
    ],
    col_widths=[4.0, 3.0, 1.5, 7.0, 3.0]
)
note(doc, "[^13] MIDAGRI, gob.pe/institucion/midagri/noticias/1177401 y /1235541; Coop Coffees, coopcoffees.com/member/profile/cenfrocafe-943467")

h3(doc, "Nivel en preparación — geolocalización en curso")
bullet(doc, "Cooperativas El Dorado, San Martín — geolocalización con ADEL/IICA/DRASAM. [^17]")
bullet(doc, "Allima Cacao (Chazuta, San Martín) — trazabilidad parcela, piloto EUDR con Silva Cacao (Bélgica). [^13]")
bullet(doc, "Colpa de Loros (Ucayali) — visitado MIDAGRI. Zona amazónica café + palma. [^13]")

h2(doc, "3.2 Cadena de cacao")
body(doc, "Allima Cacao (Chazuta, San Martín): piloto EUDR 2025, exportación cacao a Silva Cacao (Bélgica), +45 toneladas, trazabilidad vía AGRODIGITAL, fine flavor y orgánico.")
body(doc, "Cooperativas Junín/Ucayali (Satipo, Sonomoro, ACPC Pichanaki, Kemito Ene): misma dinámica que café, sistemas agroforestales, programa SAFE.")
note(doc, "[^13][^15] Zero Deforestation Hub, zerodeforestationhub.eu/news/how-is-peru-progressing-towards-compliance-with-the-eudr/")

body(doc, "Amazonía Link / GeoCultivate: 737 productores con parcelas georreferenciadas y reportes cero deforestación. 60,000 km² analizados.", bold=False)
note(doc, "[^18] ANDINA, andina.pe/agencia//noticia-cafe-palma-y-cacao-productores-amazonicos-aplican-practicas-libres-deforestacion-1092048.aspx")

h2(doc, "3.3 Cadena de palma aceitera")
body(doc, "Estructura diferente a café/cacao: mayor concentración en grupos agroindustriales, con núcleos de pequeños productores integrados a plantas procesadoras.", italic=True)

add_styled_table(doc,
    ["Organización", "Ubicación", "Estado RSPO 2025", "Trazabilidad"],
    [
        ["APROMAN", "Ucayali", "Hito A (espera certificado)", "77% hasta plantación (Alicorp)"],
        ["ASPASH", "Ucayali", "Elegibilidad RSPO", "En proceso"],
        ["Asociación Santa Lucía", "Ucayali", "Hito A (oct 2025, con Alicorp)", "En proceso"],
        ["APPACHE, UNIPALMA", "Ucayali", "Solicitud membresía RSPO", "—"],
        ["Grupo Palmas / Alicorp", "Varias", "Programa Palma Sostenible", "77% trazabilidad corporativa polígono"],
    ],
    col_widths=[4.5, 2.5, 5.0, 6.5]
)
note(doc, "[^19] Alicorp, Reporte RSPO 2025, alicorp.com.pe/s3/media/PDF/reporte_de_responsabilidad_compartida_rspo_2025.pdf")

# ── 4. COMPRADORES EUROPEOS ────────────────────────────────────────────────
h1(doc, "4. Compradores Europeos Activos en Perú")
add_styled_table(doc,
    ["Comprador", "País", "Producto", "Perfil"],
    [
        ["Silva Cacao", "Bélgica", "Cacao", "Specialty, fine flavor. Piloto EUDR 2025 con Allima Cacao."],
        ["Beneke Coffee", "Alemania", "Café", "Tostador. Piloto EUDR 2025 con PIMCOS/Satipo."],
        ["ICAM", "Italia", "Cacao", "Chocolate de especialidad. Piloto EUDR 2025."],
        ["JDE Peet's", "Países Bajos", "Café", "Mayor comprador mundial. MoU con Perú. Enveritas verificador. Accionista Farmer Connect."],
    ],
    col_widths=[3.5, 2.0, 2.0, 11.0]
)
note(doc, "[^10] JDE Peet's, jdepeets.com/news-container/jde-peets-signs-mous-with-honduras-peru-and-rwanda-2865109/")

body(doc,
    "Dato estratégico (Trase, 1 sep 2026): el 79% del café global es manejado por importadores que también surten "
    "al mercado de la UE. Para empresas con alta exposición a la UE — JDE Peet's (84%), Louis Dreyfus (63%), "
    "Neumann Gruppe (53%) — mantener cadenas segregadas les sale más caro que aplicar EUDR a toda la cadena. "
    "La presión se extiende a todos los clientes, no solo a los europeos.",
    bold=True
)
note(doc, "[^20] Trase, trase.earth/insights/trase-brings-greater-transparency-to-global-coffee-supply-chains (1 sep 2026); Reuters, reuters.com/business/environment/eu-deforestation-law-force-compliance-even-non-eu-coffee-supply-chains-study-2026-09-02/ (2 sep 2026)")

# ── 5. PLATAFORMAS Y ESTÁNDARES ────────────────────────────────────────────
h1(doc, "5. Plataformas y Estándares en Uso")
add_styled_table(doc,
    ["Plataforma / Estándar", "Qué hace", "Usuarios en Perú"],
    [
        ["Enveritas", "Verificación drones + IA + satelital. Deforestación post-2020 territorial.", "JDE Peet's (MoU), grandes exportadores"],
        ["Farmer Connect (blockchain)", "Trazabilidad lote, 40+ datapoints, QR 'Thank My Farmer'. Accionista: JDE Peet's.", "Cooperativas grandes tostadores"],
        ["Rainforest Alliance", "Certificación con componente deforestación y legalidad.", "~40% café peruano certificado"],
        ["Fairtrade", "Group certification con trazabilidad a parcela.", "Cooperativas organizadas"],
        ["Organic (USDA, UE)", "Mapeo obligatorio por unidad productiva.", "Productores especialidad"],
        ["RSPO", "Certificación palma, trazabilidad hasta plantación.", "APROMAN, ASPASH, Santa Lucía, UNIPALMA"],
        ["Global Forest Watch / GeoBosques", "Monitoreo satelital deforestación.", "MIDAGRI, cooperativas"],
        ["FAO WHISP", "Plataforma geolocalización internacional.", "Interoperabilidad Perú lograda"],
        ["MICACAO (Helvetas)", "Trazabilidad digital cacao.", "Allima Cacao y otras cacaoteras"],
        ["AGRODIGITAL / Identidad Digital", "Geolocalización, constancia cero deforestación, PPA.", "150K+ polígonos, 410K+ productores"],
        ["4C / GRAS", "Verificación EUDR para código 4C.", "3er esquema verificación café mundo"],
    ],
    col_widths=[4.0, 8.0, 6.5]
)
note(doc, "[^21] Dataintelo, Blockchain Coffee Traceability Market 2034, dataintelo.com/report/blockchain-coffee-traceability-market")

body(doc,
    "En Perú se usan al menos 10 sistemas diferentes para cumplir requisitos EUDR. No hay un estándar único: "
    "problema de interoperabilidad y duplicidad de esfuerzos.",
    italic=True
)
note(doc, "[^4] CamcaféPeru, camcafeperu.com.pe/EN/article.php?id=236")

# ── 6. GAPS REALES ────────────────────────────────────────────────────────
h1(doc, "6. Los Gaps Reales")

gaps = [
    ("Gap 1: Titulación de tierra", "~80% pequeños productores sin título de propiedad claro. Sin documento de tenencia, la DDS no se construye válidamente. El MIDAGRI tiene soluciones intermedias (COFOPRI, contratos de cesión) pero funcionan parcialmente.", "[^6][^7]"),
    ("Gap 2: Trazabilidad de acopio", "Desde la parcela hasta la planta hay múltiples puntos de mezcla. El EUDR exige vincular cada lote con las parcelas específicas. La mayoría de cooperativas no tienen registro digital en estos puntos.", "[^5][^22]"),
    ("Gap 3: Excedente de geolocalización", "150,000 polígonos suena bien, pero la meta del MIDAGRI es 50% de productores con polígono — la mitad todavía no lo tiene. Y eso sin título ni acopio.", "[^7]"),
    ("Gap 4: Costos de adecuación", "Georreferenciación (US$5-15/parcela), sistemas digitales de acopio, consultoría DD, certificaciones adicionales. Parcialmente absorbidos por cooperación internacional.", "[^5][^7][^12]"),
    ("Gap 5: Sin índice de readiness", "No existe un indicador público, desagregado por cooperativa, que diga qué organización tiene qué nivel de preparación. El MIDAGRI hizo visitas técnicas pero no hay base de datos abierta.", ""),
    ("Gap 6: Providers de servicio sin mapear", "No hay directorio abierto de consultoras, tech providers o estudios jurídicos vendiendo DD EUDR a cooperativas peruanas. La demanda existe y crece.", ""),
]

for i, (title, desc, refs) in enumerate(gaps, 1):
    h2(doc, f"6.{i} {title}")
    body(doc, desc)
    if refs:
        note(doc, refs)

# ── 7. OPORTUNIDADES ──────────────────────────────────────────────────────
h1(doc, "7. Oportunidades de Inteligencia y Servicio")

add_styled_table(doc,
    ["Oportunidad", "Descripción", "Viabilidad"],
    [
        ["Índice de Readiness Cooperativo", "Dashboard por organización: % productores con polígono, título, sistema de acopio, expediente DD completado. No existe como producto.", "Alta"],
        ["Radar Exportaciones EUDR", "Monitorear flujos a la UE por cooperativa, volumen, frecuencia, destino. No hay API pública que haga esto.", "Media"],
        ["Plataforma Gestión Documental EUDR", "Herramienta B2B para que cooperativas/exportadores armen expediente DD completo.", "Media-alta"],
        ["Directorio Providers DD", "Mapeo de consultoras, tech companies, estudios jurídicos vendiendo DD EUDR a cooperativas.", "Alta"],
        ["Evaluación Risk Assessment", "Help cooperativas run their own risk self-assessment before buyers ask.", "Media"],
        ["Monitoreo Clasificación País", "Seguimiento de posibles reclasificaciones (estándar → bajo) en futuras actualizaciones del Anexo 2025/1093. Comisión proyecta actualizar en 2026.", "Media"],
    ],
    col_widths=[4.5, 11.0, 3.0]
)
note(doc, "[^23] European Parliament, SP-2025-10-27-TA-10-2025-0149_en.pdf, data.europarl.europa.eu")

# ── 8. FUENTES ─────────────────────────────────────────────────────────────
h1(doc, "8. Fuentes y Referencias")

note(doc, "[^1]  Reglamento (UE) 2023/1115 (EUDR). eur-lex.europa.eu/eli/reg/2023/1115/oj/eng")
note(doc, "[^2]  Reglamento de Ejecución (UE) 2025/1093 (22 may 2025). eur-lex.europa.eu/eli/reg_impl/2025/1093/oj/eng")
note(doc, "[^3]  Reglamento de Postergación EUDR, DOUE. Trase EUDR explained, trase.earth/insights/eu-deforestation-regulation-explained")
note(doc, "[^4]  CamcaféPeru, camcafeperu.com.pe/EN/article.php?id=236")
note(doc, "[^5]  CBI, cbi.eu/market-information/coffee/tips-become-eudr-compliant")
note(doc, "[^6]  AYP Digital, aypdigital.com/blog/eudr-reglamento-ue-deforestacion-trazabilidad-exportadores-peru/")
note(doc, "[^7]  MIDAGRI: gob.pe/institucion/midagri/noticias/1319697; /1177401; /1319247; /1294143; /1255233; /1235541; /1194374; /1250933")
note(doc, "[^8]  PROMPERÚ, gob.pe/institucion/promperu/noticias/1354427")
note(doc, "[^9]  MIDAGRI, gob.pe/institucion/midagri/noticias/1250933")
note(doc, "[^10] JDE Peet's, jdepeets.com/news-container/jde-peets-signs-mous-with-honduras-peru-and-rwanda-2865109/")
note(doc, "[^11] MIDAGRI / Cámara Peruana del Café y Cacao / IICA, evento socialización EUDR 2025")
note(doc, "[^12] GIZ, giz.de/en/downloads/giz2025-es-latin-america-digital-traceability-tools.pdf")
note(doc, "[^13] MIDAGRI, gob.pe/institucion/midagri/noticias/1177401 y /1235541; Coop Coffees, coopcoffees.com/member/profile/cenfrocafe-943467")
note(doc, "[^14] Trabocca, trabocca.com/our-coffees/peru/cajamarca/tabaconas/")
note(doc, "[^15] Zero Deforestation Hub, zerodeforestationhub.eu/news/how-is-peru-progressing-towards-compliance-with-the-eudr/")
note(doc, "[^16] MIDAGRI, gob.pe/institucion/midagri/noticias/1194374")
note(doc, "[^17] MIDAGRI / DRASAM, gob.pe/institucion/regionsanmartin-dra/noticias/1268490")
note(doc, "[^18] ANDINA, andina.pe/agencia//noticia-cafe-palma-y-cacao-productores-amazonicos-aplican-practicas-libres-deforestacion-1092048.aspx")
note(doc, "[^19] Alicorp, Reporte Responsabilidad Compartida RSPO 2025, alicorp.com.pe/s3/media/PDF/reporte_de_responsabilidad_compartida_rspo_2025.pdf")
note(doc, "[^20] Trase (1 sep 2026), trase.earth/insights/trase-brings-greater-transparency-to-global-coffee-supply-chains; Reuters (2 sep 2026), reuters.com/business/environment/eu-deforestation-law-force-compliance-even-non-eu-coffee-supply-chains-study-2026-09-02/")
note(doc, "[^21] Dataintelo, Blockchain Coffee Traceability Market 2034, dataintelo.com/report/blockchain-coffee-traceability-market")
note(doc, "[^22] EFI, EUDR Exercise Coffee Report, efi.int/sites/default/files/2026-06/eudr_exercise_coffee_report_2.pdf")
note(doc, "[^23] European Parliament, SP-2025-10-27-TA-10-2025-0149_en.pdf, data.europarl.europa.eu")

# ── FOOTER ─────────────────────────────────────────────────────────────────
from docx.oxml.ns import qn as qname
footer = section.footer
fp = footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
fr = fp.add_run("Grupo ISCAM — Universidad Peruana  |  Dossier EUDR — Uso Interno  |  12 de octubre de 2026")
fr.font.name = FONT
fr.font.size = Pt(8)
fr.font.color.rgb = RGBColor(0x88, 0x88, 0x88)

# ── Guardar ────────────────────────────────────────────────────────────────
output_path = r"C:\Users\acuba\ISCAM_UU_Peru_EUDR_Dossier_v3.docx"
doc.save(output_path)
print(f"DOCX guardado: {output_path}")
