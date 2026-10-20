# -*- coding: utf-8 -*-
"""
Genera un documento de trabajo académico estilo Universidad del Pacífico
Título: Cooperativas Peruanas y EUDR
Autor: Investigador ISCAM - Universidad del Pacífico
"""
from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

# ─── CONSTANTES DE FORMATO ─────────────────────────────────────────────────
FONT = "Times New Roman"
FONT_SIZE_BODY = Pt(12)
FONT_SIZE_H1   = Pt(13)
FONT_SIZE_H2   = Pt(12)
FONT_SIZE_H3   = Pt(12)
FONT_SIZE_TITLE = Pt(16)
FONT_SIZE_COVER_TITLE = Pt(14)

MARGIN = Inches(1.0)
LINE_SPACING = 2.0  # doble espaciado
PARA_SPACING_AFTER = Pt(6)
PARA_SPACING_BEFORE_H = Pt(12)

BLACK = RGBColor(0, 0, 0)
DARK_GRAY = RGBColor(64, 64, 64)

OUTPUT_PATH = r"C:\Users\acuba\ISCAM_UU_Peru_EUDR_DocumentoTrabajo.docx"


# ─── HELPERS ────────────────────────────────────────────────────────────────

def set_font(run, bold=False, italic=False, size=None, font_name=None):
    run.bold = bold
    run.italic = italic
    if size:
        run.font.size = size
    if font_name:
        run.font.name = font_name
    run.font.color.rgb = BLACK

def add_paragraph(doc, text, style_name=None, bold=False, italic=False,
                  size=None, align=None, space_before=0, space_after=6,
                  first_line_indent=None, keep_with_next=False):
    p = doc.add_paragraph()
    if style_name:
        p.style = style_name
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    if align:
        p.alignment = align
    if keep_with_next:
        p.paragraph_format.keep_with_next = True
    if first_line_indent is not None:
        p.paragraph_format.first_line_indent = first_line_indent
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    p.paragraph_format.line_spacing = LINE_SPACING

    run = p.add_run(text)
    set_font(run, bold=bold, italic=italic, size=size or FONT_SIZE_BODY)
    return p


def add_heading(doc, text, level=1, numbered=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16 if level == 1 else 12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    p.paragraph_format.line_spacing = LINE_SPACING
    p.paragraph_format.keep_with_next = True

    prefix = ""
    if numbered:
        prefix = numbered + " "

    run = p.add_run(prefix + text)
    run.bold = True
    run.font.size = FONT_SIZE_H1 if level == 1 else (FONT_SIZE_H2 if level == 2 else FONT_SIZE_H3)
    run.font.name = FONT
    run.font.color.rgb = BLACK
    return p


def add_body(doc, text, first_indent=True):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = PARA_SPACING_AFTER
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    p.paragraph_format.line_spacing = LINE_SPACING
    if first_indent:
        p.paragraph_format.first_line_indent = Inches(0.5)

    run = p.add_run(text)
    run.font.name = FONT
    run.font.size = FONT_SIZE_BODY
    run.font.color.rgb = BLACK
    return p


def add_table(doc, headers, rows, col_widths=None):
    """Tabla con bordes negros mínimos, estilo académico."""
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Table Grid'

    # Header
    hdr = table.rows[0]
    for i, h in enumerate(headers):
        cell = hdr.cells[i]
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        p.paragraph_format.line_spacing = 1.0
        run = p.add_run(h)
        run.bold = True
        run.font.name = FONT
        run.font.size = Pt(10)
        run.font.color.rgb = BLACK
        # Fondo gris claro para header
        shading = OxmlElement('w:shd')
        shading.set(qn('w:fill'), 'D9D9D9')
        cell._tc.get_or_add_tcPr().append(shading)

    # Rows
    for r_idx, row_data in enumerate(rows):
        row = table.rows[r_idx + 1]
        for c_idx, cell_text in enumerate(row_data):
            cell = row.cells[c_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
            p.paragraph_format.line_spacing = 1.0
            run = p.add_run(str(cell_text))
            run.font.name = FONT
            run.font.size = Pt(10)
            run.font.color.rgb = BLACK

    # Anchos de columna
    if col_widths:
        for row in table.rows:
            for i, w in enumerate(col_widths):
                row.cells[i].width = Inches(w)

    # Espacio después de tabla
    p_space = doc.add_paragraph()
    p_space.paragraph_format.space_before = Pt(0)
    p_space.paragraph_format.space_after = Pt(6)
    p_space.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    p_space.paragraph_format.line_spacing = LINE_SPACING

    return table


def add_cover_page(doc):
    """Página de portada institucional UP."""
    # Espacio en blanco para simular encuadernación
    for _ in range(4):
        sp = doc.add_paragraph()
        sp.paragraph_format.space_before = Pt(0)
        sp.paragraph_format.space_after = Pt(0)
        sp.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        sp.paragraph_format.line_spacing = 1.0

    # Universidad del Pacífico
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(24)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run("UNIVERSIDAD DEL PACÍFICO")
    run.bold = True
    run.font.size = Pt(14)
    run.font.name = FONT
    run.font.color.rgb = BLACK

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run("Grupo de Investigación ISCAM — Cadenas de Valor Agrarias")
    run.font.size = Pt(11)
    run.font.name = FONT
    run.font.color.rgb = BLACK

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run("Centro de Investigación de la Universidad del Pacífico (CIUP)")
    run.font.size = Pt(11)
    run.font.name = FONT
    run.font.color.rgb = BLACK

    # Línea separadora
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(12)
    run = p.add_run("─" * 72)
    run.font.size = Pt(10)
    run.font.name = FONT
    run.font.color.rgb = BLACK

    # Serie y número
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run("DOCUMENTO DE TRABAJO")
    run.bold = True
    run.font.size = Pt(12)
    run.font.name = FONT
    run.font.color.rgb = BLACK

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(24)
    run = p.add_run("Serie: Documentos de Trabajo — Economía y Gestión de Cadenas de Valor / N.º DT-ISCAM-2026-001")
    run.font.size = Pt(10)
    run.font.name = FONT
    run.font.color.rgb = DARK_GRAY

    # Título principal
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    p.paragraph_format.line_spacing = 1.5
    run = p.add_run("Cooperativas Peruanas y el Reglamento de la Unión Europea contra la Deforestación (EUDR)")
    run.bold = True
    run.font.size = Pt(14)
    run.font.name = FONT
    run.font.color.rgb = BLACK

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(24)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    p.paragraph_format.line_spacing = 1.5
    run = p.add_run("Diagnóstico de la Cadena de Valor, Gaps de Trazabilidad y Agenda de Preparación")
    run.bold = True
    run.font.size = Pt(12)
    run.font.name = FONT
    run.font.color.rgb = BLACK

    # Línea separadora
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(24)
    run = p.add_run("─" * 72)
    run.font.size = Pt(10)
    run.font.name = FONT
    run.font.color.rgb = BLACK

    # Autor y datos
    datos = [
        ("Autor:", "Investigador Principal, Grupo ISCAM"),
        ("Institución:", "Universidad del Pacífico — Lima, Perú"),
        ("Fecha:", "Octubre 2026"),
        ("Clasificación de riesgo país:", "Riesgo estándar — Reglamento de Ejecución (UE) 2025/1093"),
        ("Cadenas priorizadas:", "Café · Cacao · Palma aceitera"),
    ]
    for label, valor in datos:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        p.paragraph_format.line_spacing = 1.5
        r1 = p.add_run(label + " ")
        r1.bold = True
        r1.font.size = Pt(11)
        r1.font.name = FONT
        r1.font.color.rgb = BLACK
        r2 = p.add_run(valor)
        r2.font.size = Pt(11)
        r2.font.name = FONT
        r2.font.color.rgb = BLACK

    # Nota de disclaimer
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(32)
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run("Documento de trabajo para uso interno del grupo de investigación ISCAM.")
    run.italic = True
    run.font.size = Pt(9)
    run.font.name = FONT
    run.font.color.rgb = DARK_GRAY

    doc.add_page_break()


def configure_document(doc):
    """Aplica configuración global de página y estilos."""
    # Márgenes
    for section in doc.sections:
        section.top_margin = MARGIN
        section.bottom_margin = MARGIN
        section.left_margin = MARGIN
        section.right_margin = MARGIN
        section.page_width = Inches(8.27)   # A4
        section.page_height = Inches(11.69)

    # Estilos del documento
    styles = doc.styles

    # Modificar estilo Normal
    try:
        normal = styles['Normal']
        normal.font.name = FONT
        normal.font.size = FONT_SIZE_BODY
        normal.font.color.rgb = BLACK
        pPr = normal.element.get_or_add_pPr()
        spacing = OxmlElement('w:spacing')
        spacing.set(qn('w:line'), '480')
        spacing.set(qn('w:lineRule'), 'auto')
        spacing.set(qn('w:after'), '120')
        # aplicar a pPr
        for child in pPr:
            if child.tag.endswith('}spacing'):
                pPr.remove(child)
        pPr.append(spacing)
    except Exception:
        pass

    # Agregar página en blanco al final (Word lo genera)
    # Agregar pagebreak al final del documento


# ─── CONTENIDO DEL DOCUMENTO ───────────────────────────────────────────────

def build_document():
    doc = Document()
    configure_document(doc)

    # ── PORTADA ────────────────────────────────────────────────────────────
    add_cover_page(doc)

    # ── RESUMEN ───────────────────────────────────────────────────────────
    add_heading(doc, "Resumen", level=1)
    add_body(doc, (
        "El presente documento de trabajo analiza los desafíos y oportunidades que enfrentan las cooperativas "
        "agrarias peruanas ante la entrada en vigor del Reglamento (UE) 2023/1115 contra la deforestación (EUDR). "
        "Se examina el marco normativo, la clasificación de riesgo país asignada a Perú —riesgo estándar según "
        "el Reglamento de Ejecución (UE) 2025/1093—, y la arquitectura institucional desplegada por el Estado "
        "peruano para la preparación de exportadores. El documento identifica las cooperativas líderes en las "
        "cadenas de café, cacao y palma aceitera que han alcanzado niveles avanzados de trazabilidad, así como "
        "aquellas que permanecen en fase de preparación. Se documentan los principales gaps en materia de "
        "geolocalización, tenencia de tierra, trazabilidad de acopio y capacidad de generación de evidencia de "
        "debida diligencia. El análisis concluye que las cooperativas organizadas con infraestructura digital "
        "existente constituyen el segmento con mayor probabilidad de cumplimiento oportuno, y se identifican "
        "cinco ejes prioritarios para la agenda de preparación: formalización de la propiedad, escalamiento de "
        "la geolocalización, interoperabilidad de plataformas, acceso a financiamiento para certificaciones, y "
        "fortalecimiento de la articulación con compradores europeos."
    ))

    # ── ABSTRACT ───────────────────────────────────────────────────────────
    add_heading(doc, "Abstract", level=1)
    add_body(doc, (
        "This working paper examines the challenges and opportunities faced by Peruvian agricultural cooperatives "
        "in the context of the EU Deforestation Regulation (EUDR). It analyses the regulatory framework, Peru's "
        "country-risk classification as standard-risk under Commission Implementing Regulation (EU) 2025/1093, "
        "and the institutional infrastructure deployed by the Peruvian state to prepare exporters. The document "
        "identifies leading cooperatives in the coffee, cocoa, and palm oil value chains that have achieved "
        "advanced traceability levels, as well as those still in preparation stages. Key gaps in geolocation, "
        "land tenure, aggregation traceability, and due diligence evidence generation are documented. The "
        "analysis concludes that organized cooperatives with existing digital infrastructure constitute the "
        "segment most likely to achieve timely compliance, and five priority axes are identified for the "
        "preparation agenda: property formalization, geolocation upscaling, platform interoperability, "
        "access to certification financing, and strengthened articulation with European buyers."
    ))

    # ── PALABRAS CLAVE ─────────────────────────────────────────────────────
    add_heading(doc, "Palabras clave", level=1)
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    p.paragraph_format.line_spacing = LINE_SPACING
    p.paragraph_format.first_line_indent = Inches(0.5)
    run = p.add_run("EUDR · deforestación · trazabilidad · debida diligencia · cooperativas agrarias · café · cacao · palma aceitera · Perú · Unión Europea")
    run.font.name = FONT
    run.font.size = FONT_SIZE_BODY
    run.font.color.rgb = BLACK

    # ── 1. INTRODUCCIÓN ───────────────────────────────────────────────────
    add_heading(doc, "1. Introducción", level=1)

    add_body(doc, (
        "El comercio internacional de commodities agrarios enfrenta desde finales de 2024 un cambio regulatorio "
        "estructural de alcance global. El Reglamento (UE) 2023/1115 relativo a los productos asociados a la "
        "deforestación y la degradación forestal (EUDR, por sus siglas en inglés), adoptado el 31 de mayo de "
        "2023, prohíbe la comercialización, exportación e importación en el mercado de la Unión Europea de "
        "ganado bovino, cacao, café, palma aceitera, caucho, soja y madera que hayan sido producidos en "
        "tierras deforestadas con posterioridad al 31 de diciembre de 2020, o cuya producción haya vulnerado "
        "la legislación aplicable del país de origen en materia de tenencia de tierra, uso de suelo, derechos "
        "laborales o derechos de pueblos indígenas (Parlamento Europeo y Consejo de la Unión Europea, 2023)."
    ))

    add_body(doc, (
        "La norma exige que todo lote exportado a la Unión Europea esté respaldado por una Declaración de "
        "Debida Diligencia (DDS) presentada por el importador europeo ante el sistema TRACES/NTIS de la "
        "Comisión Europea. La DDS se fundamenta en información proporcionada por el exportador no comunitario: "
        "geolocalización de parcelas productoras en formato WGS-84, código arancelario, volumen, datos del "
        "proveedor y documentación de tenencia de tierra, entre otros requisitos. El importador debe además "
        "demostrar que evaluó y, en su caso, mitigó los riesgos identificados antes del envío "
        "(European Commission, 2024)."
    ))

    add_body(doc, (
        "Perú ha sido clasificado como país de riesgo estándar en el Anexo del Reglamento de Ejecución (UE) "
        "2025/1093 de la Comisión Europea, publicado el 22 de mayo de 2025. Esta clasificación implica que "
        "el importador europeo debe cumplir la debida diligencia completa en sus tres etapas —recopilación de "
        "información, evaluación de riesgo y medidas de mitigación— para cada lote de café, cacao o palma "
        "aceitera de origen peruano. La debida diligencia simplificada, prevista en el Artículo 13 del EUDR "
        "para países de bajo riesgo, no resulta aplicable (European Commission, 2025)."
    ))

    add_body(doc, (
        "El presente documento de trabajo tiene como objetivo proporcionar un diagnóstico integral del estado "
        "de preparación de las cooperativas agrarias peruanas ante el EUDR. El documento se organiza en seis "
        "secciones: tras esta introducción, la segunda sección desarrolla el marco normativo y las obligaciones "
        "que la norma impone a exportadores y compradores. La tercera sección presenta la respuesta "
        "institucional del Estado peruano. La cuarta sección identifica y caracteriza a las cooperativas "
        "líderes en las cadenas de café, cacao y palma aceitera. La quinta sección documenta los compradores "
        "europeos activos en Perú y las plataformas tecnológicas en uso. La sexta sección presenta las "
        "conclusiones y la agenda de investigación."
    ))

    # ── 2. MARCO NORMATIVO ────────────────────────────────────────────────
    add_heading(doc, "2. Marco Normativo del EUDR y Obligaciones para Exportadores", level=1)

    add_heading(doc, "2.1 Las tres condiciones de cumplimiento para todo lote exportado a la UE", level=2)

    add_body(doc, (
        "El EUDR establece tres condiciones simultáneas que deben cumplirse para cada lote exportado a la "
        "Unión Europea (Parlamento Europeo y Consejo de la Unión Europea, 2023). En primer lugar, la "
        "condición de no deforestación exige que la parcela donde se produjo el commodity no haya sido "
        "objeto de deforestación con posterioridad al 31 de diciembre de 2020. En segundo lugar, la "
        "condición de producción legal requiere que la producción haya respetado la legislación aplicable del "
        "país de origen en materia de tenencia de tierra, uso de suelo, ambiental, laboral y derechos de "
        "pueblos indígenas. En tercer lugar, la condición de debida diligencia exige que el importador "
        "europeo haya completado el procedimiento de DDS antes de la comercialización del lote en la UE."
    ))

    add_heading(doc, "2.2 Las tres etapas de la debida diligencia completa", level=2)

    add_body(doc, (
        "La debida diligencia completa —aplicable a Perú como país de riesgo estándar— se despliega en tres "
        "etapas secuenciales (European Commission, 2024). La primera etapa consiste en la recopilación de "
        "información sobre el lote, que debe incluir: coordenadas de geolocalización de las parcelas "
        "productoras en formato WGS-84 (EPSG:4326), con polígono obligatorio para parcelas iguales o "
        "mayores a 4 hectáreas y punto GPS para parcelas menores; país, departamento y provincia de "
        "producción; código arancelario HS; nombre, RUC y dirección del proveedor; nombre y dirección del "
        "comprador; fecha de cosecha; documentos de tenencia de tierra; historial de cobertura forestal, y "
        "registros de acopio (guías de remisión, actas de entrega, registros de pesaje) que vinculen la "
        "parcela con el lote exportado (CBI, 2025). La segunda etapa corresponde a la evaluación de riesgo, "
        "mediante la cual el importador europeo determina si existen indicios de que el lote incumpla las "
        "condiciones 1 o 2. La tercera etapa, aplicable cuando se identifican riesgos, exige la adopción "
        "de medidas de mitigación antes del envío del lote."
    ))

    add_heading(doc, "2.3 Fecha de entrada en vigencia y obligaciones del exportador peruano", level=2)

    add_body(doc, (
        "El Reglamento de Postergación, acordado en diciembre de 2025, fijó la fecha de entrada en vigor "
        "del EUDR para grandes y medianas empresas en el 30 de diciembre de 2026, y para microempresas y "
        "pequeñas empresas europeas en el 30 de junio de 2027 (Parlamento Europeo y Consejo de la Unión "
        "Europea, 2025). Sin embargo, desde 2025 los compradores europeos vienen exigiendo evidencias de "
        "cumplimiento a sus proveedores como práctica comercial anticipatoria, independientemente de la fecha "
        "de aplicabilidad formal (PROMPERÚ, 2025; AYP Digital, 2025)."
    ))

    add_body(doc, (
        "Del lado del exportador peruano, la obligación central consiste en entregar al importador europeo, "
        "por cada lote, la información descrita en la primera etapa de la debida diligencia. Esta obligación "
        "se traduce en requisitos operativos concretos: sistemas de geolocalización a nivel de parcela, "
        "trazabilidad durante las etapas de acopio primario y secundario, y documentación legal de la cadena "
        "de custodia. Según fuentes del sector, aproximadamente el 80% de los pequeños productores carece "
        "de un título de propiedad formal que respalde la documentación de tenencia de tierra requerida. "
        "Esta brecha constituye uno de los obstáculos más significativos para el cumplimiento oportuno "
        "(AYP Digital, 2025; CamcaféPeru, 2025)."
    ))

    add_heading(doc, "2.4 Clasificación de riesgo país y niveles de control", level=2)

    add_body(doc, (
        "La primera clasificación oficial de países según nivel de riesgo fue publicada mediante el "
        "Reglamento de Ejecución (UE) 2025/1093 de la Comisión Europea, con fecha 22 de mayo de 2025. El "
        "Anexo del Reglamento clasifica 140 países como de bajo riesgo —entre los que se encuentran todos "
        "los países de la UE, Chile, Costa Rica, Kenia, Laos, Papúa Nueva Guinea, Ruanda, Vietnam, Estados "
        "Unidos, China y Japón—, cuatro países como de alto riesgo (Bielorrusia, Rusia, Myanmar y Corea "
        "del Norte), y el resto, incluyendo Perú, como riesgo estándar. Los países de bajo riesgo gozan de "
        "la posibilidad de aplicar la debida diligencia simplificada; los países de alto riesgo están "
        "sujetos a controles sobre el 9% de los operadores y el 9% del volumen de importación. Perú, como "
        "riesgo estándar, enfrenta controles sobre el 3% de los operadores que declaren productos covered "
        "(European Commission, 2025)."
    ))

    # Tabla de clasificación
    add_table(doc,
        headers=["Categoría de riesgo", "Control autoridades UE", "DD requerida", "Países ejemplo"],
        rows=[
            ["Bajo riesgo", "1% operadores/año", "Simplificada (solo recopilación)", "UE, Chile, Costa Rica, Kenia, Laos, PNG, Ruanda, Vietnam, EE.UU., China, Japón"],
            ["Riesgo estándar (Perú)", "3% operadores/año", "Completa en 3 etapas", "Perú, Brasil, Colombia, Indonesia, Bolivia, Paraguay, México, Argentina"],
            ["Alto riesgo", "9% operadores + 9% volumen", "Completa reforzada", "Bielorrusia, Rusia, Myanmar, Corea del Norte"],
        ],
        col_widths=[1.4, 1.2, 1.6, 2.5]
    )

    # ── 3. RESPUESTA INSTITUCIONAL ────────────────────────────────────────
    add_heading(doc, "3. La Respuesta Institucional del Estado Peruano", level=1)

    add_heading(doc, "3.1 Panorama cuantitativo de la preparación nacional", level=2)

    add_body(doc, (
        "El Ministerio de Desarrollo Agrario y Riego (MIDAGRI) ha reportado avances significativos en la "
        "preparación del sector agrario peruano. A través de la plataforma AGRODIGITAL y el Padrón de "
        "Productores Agrarios (PPA), se han geolocalizado más de 150,000 polígonos de parcelas productoras "
        "de café, cacao y palma aceitera, cubriendo 13 regiones del país. El PPA registra 2.03 millones de "
        "productores inscritos, de los cuales aproximadamente 410,000 corresponde a productores de café, "
        "cacao y palma aceitera. El análisis espacial del MIDAGRI confirma que el 99% de los productores de "
        "estos tres commodities inscritos en el PPA se ubica en zonas instaladas antes del año 2020, dato "
        "que constituye la base de la constancia de libre deforestación emitida por la plataforma. El MIDAGRI "
        "ha reportado además que 150 exportadores peruanos se encuentran alineando sus procesos internos con "
        "los requisitos del EUDR, y que se han remitido más de 260 comunicaciones a asociaciones, "
        "cooperativas y empresas para la remisión de polígonos de parcelas (MIDAGRI, 2025a, 2025b, 2025c, "
        "2025d)."
    ))

    add_heading(doc, "3.2 Actores institucionales y roles", level=2)

    add_body(doc, (
        "La respuesta institucional ha involucrado a múltiples actores públicos y privados. El MIDAGRI "
        "actúa como líder de la estrategia nacional, responsable de la plataforma AGRODIGITAL/PPA, la "
        "plataforma de trazabilidad en desarrollo y la coordinación interinstitucional. El Ministerio de "
        "Comercio Exterior y Turismo (MINCETUR), a través de PROMPERÚ, ejecuta programas de preparación de "
        "exportadores: en 2025 se beneficiaron 21 organizaciones y 7,880 productores de Cajamarca, San "
        "Martín y Lima (PROMPERÚ, 2025). El Ministerio del Ambiente, a través de la plataforma GeoBosques, "
        "realiza el cruce de parcelas geolocalizadas con mapas de cobertura forestal para verificar la "
        "existencia de la parcela previa a 2020. ADEX, mediante el convenio firmado con MIDAGRI y MINCETUR "
        "en septiembre de 2025, aporta asistencia técnica y capacitación a productores y exportadores "
        "durante un período de dos años (MIDAGRI, 2025e)."
    ))

    add_body(doc, (
        "La cooperación internacional ha desempeñado un rol relevante. La GIZ ha brindado apoyo técnico al "
        "MIDAGRI en geolocalización y estrategia EUDR. El Instituto Interamericano de Cooperación para la "
        "Agricultura (IICA) ha coordinado la capacitación y articulación con gobiernos regionales. La FAO "
        "ha facilitado la interoperabilidad de la plataforma nacional con el World Forestld Cover "
        "Information System for Producers (WHISP), permitiendo la generación de reportes de cumplimiento "
        "gratuitos y estandarizados. La Cooperación Suiza, Helvetas Perú y Solidaridad ejecutan proyectos "
        "de trazabilidad en campo, como AGROInnova y Amazonía Link."
    ))

    add_heading(doc, "3.3 Infraestructura pública en operación", level=2)

    add_body(doc, (
        "La infraestructura digital pública desplegada comprende cuatro componentes principales. El "
        "aplicativo AGRODIGITAL, desarrollado por MIDAGRI, permite la geolocalización de parcelas con GPS "
        "y funciona en modo offline, característica fundamental para zonas rurales amazónicas sin "
        "conectividad. El aplicativo cruza las parcelas geolocalizadas con los datos de GeoBosques y emite "
        "la Constancia de Libre Deforestación, documento que integra el expediente de debida diligencia. La "
        "plataforma de trazabilidad del MIDAGRI, esperada para 2026, tiene como objetivo conectar la parcela "
        "del productor con el contenedor de exportación, vinculando el DNI del productor registrado en el "
        "manifiesto de carga con las parcelas georreferenciadas en el PPA. En el ámbito del cacao, la "
        "herramienta MICACAO, desarrollada por Helvetas Perú y Open Cocoa Chain, proporciona trazabilidad "
        "digital a lo largo de la cadena, conectando productores, cooperativas y exportadores, y validando "
        "la cero deforestación mediante un sistema de verificación estandarizado (GIZ, 2025; MIDAGRI, 2025d)."
    ))

    add_heading(doc, "3.4 Convenios estratégicos con compradores europeos", level=2)

    add_body(doc, (
        "Un hito relevante es el Memorando de Entendimiento firmado entre JDE Peet's —mayor tostador de "
        "café del mundo— y el Estado peruano, para la verificación de deforestación cero mediante la empresa "
        "Enveritas. El MoU contempla la identificación de parcelas ubicadas en tierras deforestadas con "
        "posterioridad a 2020 y el diseño de mecanismos de remediación. JDE Peet's utiliza además Farmer "
        "Connect (blockchain) para la trazabilidad lote por lote, con más de 40 datapoints por lote, y ha "
        "extendido su acceso a la plataforma blockchain a sus proveedores en Perú (JDE Peet's, 2024, 2025)."
    ))

    # Tabla de actores
    add_table(doc,
        headers=["Actor", "Rol en la preparación EUDR"],
        rows=[
            ["MIDAGRI", "Líder de estrategia nacional. Geolocalización (AGRODIGITAL/PPA), plataforma de trazabilidad en desarrollo, coordinación interinstitucional."],
            ["MINCETUR / PROMPERÚ", "Preparación de exportadores. Programa DD con 21 organizaciones y 7,880 productores en 2025."],
            ["Ministerio del Ambiente / GeoBosques", "Cruce de parcelas geolocalizadas con mapas de cobertura forestal."],
            ["ADEX", "Alianza estratégica con MIDAGRI y MINCETUR (convenio septiembre 2025)."],
            ["GIZ", "Apoyo técnico a MIDAGRI en geolocalización y estrategia EUDR."],
            ["IICA", "Coordinación técnica, capacitación, articulación con gobiernos regionales."],
            ["FAO", "WHISP como plataforma de interoperabilidad internacional."],
            ["Cooperación Suiza / Helvetas / Solidaridad", "Financiamiento y ejecución de proyectos de trazabilidad en campo."],
        ],
        col_widths=[1.8, 4.9]
    )

    # ── 4. COOPERATIVAS ───────────────────────────────────────────────────
    add_heading(doc, "4. El Universo de Cooperativas y Organizaciones de Productores", level=1)

    add_heading(doc, "4.1 Cadena de café", level=2)
    add_heading(doc, "4.1.1 Nivel avanzado: cooperativas con trazabilidad operativa y exportaciones EUDR", level=3)

    add_body(doc, (
        "La Cooperativa de Servicios Múltiples Cenfrocafé Perú, con sede en Jaén, Cajamarca, y operaciones "
        "en el departamento de Amazonas, constituye una de las organizaciones más avanzadas del sector "
        "cafetalero peruano. Agrupa a 3,000 pequeños productores de café distribuidos en 12 distritos y "
        "opera una filial europea, Cenfrocafé AG (Suiza), que facilita el comercio directo con tostadores "
        "europeos. La cooperativa cuenta con trazabilidad completa a nivel de parcela, certificaciones "
        "Rainforest Alliance, Fairtrade y orgánica, y protocolos de no deforestación implementados desde "
        "hace varios ciclos productivos. Cenfrocafé participó en los pilotos de exportación EUDR organizados "
        "por el MIDAGRI en 2025, con envíos de café a Beneke Coffee (Alemania) e ICAM (Italia). En el "
        "distrito de Tabaconas, San Ignacio, la cooperativa trabaja con 154 productores individuales "
        "organizados en 12 asociaciones locales —entre ellas, El Laurel, La Palta y El Cedro— mediante "
        "esquemas de trazabilidad a nivel de parcela que constituyen un referente metodológico para el "
        "sector (Coop Coffees, 2025; Trabocca, 2025; MIDAGRI, 2025f)."
    ))

    add_body(doc, (
        "La Cooperativa Agraria Cafetalera Satipo, ubicada en la provincia de Satipo, Junín, agrupa "
        "aproximadamente 3,350 productores organizados en 7 organizaciones a través del programa SAFE. El "
        "programa SAFE opera en tres módulos: gestión de cadena, evaluación de riesgo EUDR y digitalización. "
        "La cooperativa fue visitada por una misión europea conjunta EU-Holanda-Alemania y participó en "
        "pilotos de exportación EUDR en 2025 (Zero Deforestation Hub, 2025; MIDAGRI, 2025g). La "
        "Cooperativa Agraria Sonomoro, en Pangoa, Junín, opera bajo dinámicas similares y forma parte del "
        "programa SAFE. La Cooperativa Agraria APROCAM, en Bagua, Amazonas, y PIMCOS Coffee, en Jaén, "
        "Cajamarca —que en 2025 ejecutó una exportación piloto de 45 toneladas—, completan el grupo de "
        "cooperativas con participación documentada en los pilotos de debida diligencia del MIDAGRI."
    ))

    add_heading(doc, "4.1.2 Nivel en preparación: geolocalización en curso", level=3)

    add_body(doc, (
        "Un conjunto de organizaciones de productores de café se encuentra en fase de geolocalización y "
        "preparación operativa. Las cooperativas de El Dorado, San Martín, están siendo apoyadas por la "
        "Agencia de Desarrollo Económico Local (ADEL) de El Dorado, el IICA y la DRASAM en la geolocalización "
        "de parcelas (MIDAGRI/DRASAM, 2025). La Asociación de Productores Cuencas del Huallaga, en San "
        "Martín, y la Asociación Productores Café Organero Gera, en Moyobamba, fueron visitadas por el MIDAGRI "
        "en el marco de los pilotos de debida diligencia. En la zona del VRAE, la ACPC Pichanaki y Kemito "
        "Ene, ambas en Junín, fueron visitadas por la misión europea y producen café y cacao bajo sistemas "
        "agroforestales que constituyen una base favorable para la demostración de producción libre de "
        "deforestación."
    ))

    add_heading(doc, "4.2 Cadena de cacao", level=2)

    add_body(doc, (
        "En la cadena de cacao, Allima Cacao, organización de productores de Chazuta, San Martín, destaca "
        "como caso piloto de exportación EUDR. En 2025 ejecutó un piloto de exportación de más de 45 "
        "toneladas de cacao fine flavor y orgánico a Silva Cacao (Bélgica), con trazabilidad a nivel de "
        "parcela validada a través de la plataforma AGRODIGITAL. Las cooperativas de Junín y Ucayali "
        "—Satipo, Sonomoro, ACPC Pichanaki y Kemito Ene— operan en la producción de cacao bajo sistemas "
        "agroforestales en la amazonía central y cuentan con el componente de debida diligencia estructurado "
        "dentro del programa SAFE (Zero Deforestation Hub, 2025)."
    ))

    add_body(doc, (
        "El proyecto Amazonía Link, ejecutado por Solidaridad, ha logrado georreferenciar parcelas y "
        "generar reportes de cero deforestación para 737 productores de café, cacao y palma aceitera, "
        "analizando un territorio de 60,000 km² (ANDINA, 2025)."
    ))

    add_heading(doc, "4.3 Cadena de palma aceitera", level=2)

    add_body(doc, (
        "La cadena de palma aceitera presenta una estructura diferenciada, con mayor concentración en "
        "empresas agroindustriales y núcleos de pequeños productores integrados a plantas procesadoras. Los "
        "desafíos de titulación y geolocalización son análogos a los del café y cacao, pero la estructura "
        "de la cadena y la menor organización de los productores vegetales constituyen factores adicionales "
        "de complejidad. La organización APROMAN, en Ucayali, alcanzó el Hito A de certificación RSPO en "
        "agosto de 2025 y espera la emisión del certificado. ASPASH, también en Ucayali, obtuvo la "
        "elegibilidad RSPO en 2025 y se encuentra en proceso de certificación. La Asociación Santa Lucía "
        "alcanzó el Hito A de certificación RSPO en octubre de 2025, en el marco de su articulación "
        "comercial con Alicorp. Las organizaciones APPACHE y UNIPALMA se encuentran en proceso de solicitud "
        "de membresía RSPO (Alicorp, 2025)."
    ))

    add_body(doc, (
        "El Grupo Palmas/Alicorp, a través de su programa Palma Sostenible, ha alcanzado un nivel de "
        "trazabilidad corporativa del 77% hasta plantación por polígono en su cadena de abastecimiento, "
        "constituyendo el mayor avance de trazabilidad en la cadena de palma aceitera peruana (Alicorp, 2025)."
    ))

    # ── 5. COMPRADORES Y PLATAFORMAS ─────────────────────────────────────
    add_heading(doc, "5. Compradores Europeos y Plataformas Tecnológicas", level=1)

    add_body(doc, (
        "El mercado europeo de café y cacao cuenta con cuatro compradores que han mantenido presencia "
        "documentada en Perú y que, por su perfil de riesgo de suministro, se encuentran entre los más "
        "expuestos al EUDR. Silva Cacao (Bélgica) opera en la cadena de cacao de especialidad, con el "
        "piloto EUDR 2025 con Allima Cacao como antecedente inmediato. Beneke Coffee (Alemania) y ICAM "
        "(Italia) participan en la cadena de café a través de los pilotos organizados por el MIDAGRI. JDE "
        "Peet's (Países Bajos), como mayor tostador de café del mundo, representa el caso de mayor escala: "
        "su MoU con el Estado peruano, la contratación de Enveritas como verificador independiente, y su "
        "participación accionaria en Farmer Connect le confieren una posición única en el ecosistema de "
        "trazabilidad (JDE Peet's, 2024, 2025)."
    ))

    add_body(doc, (
        "Desde la perspectiva de la economía de cadenas de suministro, el estudio de Trase publicado el "
        "1 de septiembre de 2026 proyecta que el EUDR ejercerá presión sobre empresas con alta exposición "
        "a la UE para extender los requisitos de debida diligencia a toda su cadena global, y no únicamente "
        "a los lotes destinados al mercado europeo. Los datos de Trase revelan que el 79% del café global "
        "es manejado por importadores que simultáneamente surten al mercado de la Unión Europea. Para "
        "empresas como JDE Peet's (84% de su café con exposición a la UE), Louis Dreyfus (63%) y Neumann "
        "Gruppe (53%), mantener cadenas segregadas —una para la UE con cumplimiento EUDR y otra para "
        "mercados sin regulación— resulta más costoso que aplicar los estándares EUDR a toda su cadena de "
        "suministro. Este fenómeno de extensión extraterritorial de la regulación constituye un incentivo "
        "estructural para que los exportadores peruanos cumplan los requisitos EUDR incluso cuando venden "
        "a compradores no europeos (Trase, 2026; Reuters, 2026)."
    ))

    # Tabla de compradores
    add_table(doc,
        headers=["Comprador", "País", "Producto", "Perfil EUDR"],
        rows=[
            ["Silva Cacao", "Bélgica", "Cacao", "Specialty, fine flavor. Piloto EUDR 2025 con Allima Cacao."],
            ["Beneke Coffee", "Alemania", "Café", "Tostador. Piloto EUDR 2025 con PIMCOS y Satipo."],
            ["ICAM", "Italia", "Cacao", "Chocolate de especialidad. Piloto EUDR 2025."],
            ["JDE Peet's", "Países Bajos", "Café", "Mayor tostador del mundo. MoU con Perú. Enveritas como verificador. Accionista de Farmer Connect (blockchain)."],
        ],
        col_widths=[1.4, 0.9, 0.9, 3.5]
    )

    add_body(doc, (
        "El ecosistema de trazabilidad disponible para las cooperativas peruanas comprende plataformas "
        "tecnológicas, estándares de certificación y sistemas de monitoreo satelital, con diferentes "
        "niveles de madurez y costos de implementación. Enveritas, empresa de verificación con uso de "
        "drones, inteligencia artificial e imágenes satelitales para el análisis de deforestación post-2020 "
        "a nivel territorial, es el verificador contratado por JDE Peet's. Farmer Connect, plataforma de "
        "trazabilidad basada en blockchain con más de 40 datapoints por lote, es accesible para cooperativas "
        "que surten a grandes tostadores con programas blockchain activos. En materia de certificación, "
        "Rainforest Alliance —que incluye un componente de deforestación y legalidad en sus estándares— "
        "certifica aproximadamente el 40% del café peruano exportado. La certificación RSPO en palma "
        "aceitera proporciona un marco de trazabilidad hasta plantación directamente alineable con los "
        "requisitos del EUDR. GeoBosques y Global Forest Watch proporcionan datos de cobertura forestal "
        "que permiten verificar la existencia de parcela previa a 2020."
    ))

    # ── 6. CONCLUSIONES ────────────────────────────────────────────────────
    add_heading(doc, "6. Conclusiones", level=1)

    add_body(doc, (
        "El presente documento de trabajo permite identificar cinco hallazgos principales. En primer lugar, "
        "Perú enfrenta el EUDR desde una posición de preparación institucional relativamente avanzada, "
        "sustentada en la geolocalización de más de 150,000 parcelas a través de AGRODIGITAL y en la "
        "interoperabilidad lograda con plataformas internacionales de monitoreo. No obstante, la brecha de "
        "formalización de la propiedad —el 80% de los pequeños productores carece de título de propiedad— "
        "constituye el principal obstáculo para la construcción de expedientes de debida diligencia válidos."
    ))

    add_body(doc, (
        "En segundo lugar, las cooperativas organizadas con infraestructura digital preexistente —Cenfrocafé, "
        "la Cooperativa Agraria Cafetalera Satipo, Allima Cacao y las organizaciones de palma aceitera "
        "avanzadas— se encuentran en condiciones de cumplir los requisitos del EUDR para la fecha de "
        "entrada en vigencia. Estas organizaciones se benefician de certificaciones existentes, trazabilidad "
        "operativa a nivel de parcela, y relaciones comerciales establecidas con compradores europeos que ya "
        "aplican estándares de debida diligencia."
    ))

    add_body(doc, (
        "En tercer lugar, el EUDR tendrá efectos de extensión extraterritorial significativos. El dato de "
        "Trase (2026) según el cual el 79% del café global es manejado por importadores con exposición a "
        "la UE implica que los estándares de debida diligencia se incorporarán a la práctica comercial "
        "habitual de los principales compradores de café y cacao peruano, independientemente de que el lote "
        "final se destine o no al mercado europeo."
    ))

    add_body(doc, (
        "En cuarto lugar, la agenda de preparación prioritaria debe articularse en torno a cinco ejes: "
        "(i) la formalización masiva de la propiedad rural mediante COFOPRI y los mecanismos de titulación "
        "del MIDAGRI; (ii) el escalamiento de la geolocalización a las cooperativas que aún no cuentan con "
        "polígonos registrados en AGRODIGITAL; (iii) la interoperabilidad técnica de las plataformas "
        "existentes con el sistema TRACES/NTIS de la UE; (iv) el acceso a financiamiento para los costos "
        "de certificación, verificación y adecuación de sistemas, particularmente para organizaciones de "
        "pequeño y mediano tamaño; y (v) el fortalecimiento de la articulación comercial directa con "
        "compradores europeos mediante la cualificación de las capacidades de negociación y cumplimiento "
        "de las cooperativas."
    ))

    add_body(doc, (
        "En quinto lugar, la investigación futura debería abordar la cuantificación del costo de cumplimiento "
        "EUDR para cooperativas de diferente escala, el análisis de mecanismos de financiamiento para la "
        "adecuación, y la evaluación de la efectividad de las plataformas públicas de trazabilidad en la "
        "generación de evidencia de debida diligencia reconocida por las autoridades europeas. El presente "
        "documento de trabajo busca contribuir a esta agenda proporcionando un diagnóstico integral del "
        "estado de situación que sirva como línea base para la investigación y la formulación de políticas."
    ))

    # ── REFERENCIAS ────────────────────────────────────────────────────────
    add_heading(doc, "Referencias", level=1)

    referencias = [
        "Alicorp. (2025). Reporte de Responsabilidad Compartida RSPO 2025. https://alicorp.com.pe/s3/media/PDF/reporte_de_responsabilidad_compartida_rspo_2025.pdf",
        "ANDINA. (2025). Café, palma y cacao: productores amazónicos aplican prácticas libres de deforestación. https://andina.pe/agencia//noticia.aspx?id=1092048",
        "AYP Digital. (2025). EUDR: Trazabilidad documental para exportadores peruanos. https://aypdigital.com/blog/eudr-reglamento-ue-deforestacion-trazabilidad-exportadores-peru/",
        "CamcaféPeru. (2025). EUDR y trazabilidad para pequeños productores. https://camcafeperu.com.pe/EN/article.php?id=236",
        "CBI. (2025). 7 Tips on How to Become EUDR Compliant in Coffee. https://cbi.eu/market-information/coffee/tips-become-eudr-compliant",
        "Coop Coffees. (2025). CENFROCAFE Profile. https://coopcoffees.com/member/profile/cenfrocafe-943467",
        "European Commission. (2024). EU Deforestation Regulation: Guidance for Operators and Customs Authorities. https://environment.ec.europa.eu/topics/forests/deforestation/regulation-deforestation-free-products_en",
        "European Commission. (2025). Reglamento de Ejecución (UE) 2025/1093 de la Comisión, de 22 de mayo de 2025. https://eur-lex.europa.eu/eli/reg_impl/2025/1093/oj/eng",
        "GIZ. (2025). Adaptación a las Normativas de Trazabilidad para la Inclusión de Pequeños Productores en América Latina. https://giz.de/en/downloads/giz2025-es-latin-america-digital-traceability-tools.pdf",
        "JDE Peet's. (2024). Green Coffee Human Rights & Environmental Due Diligence Framework. https://jdepeets.com/siteassets/.../jde-peets-green-coffee-hredd-framework.pdf",
        "JDE Peet's. (2025). JDE Peet's Signs MOUs with Honduras, Peru and Rwanda to Combat Coffee-Related Deforestation. https://jdepeets.com/news-container/jde-peets-signs-mous-with-honduras-peru-and-rwanda-2865109/",
        "MIDAGRI. (2025a). Peru Has Made Significant Progress in Complying with the EUDR Regulation. https://gob.pe/institucion/midagri/noticias/1319697",
        "MIDAGRI. (2025b). Perú se alista para exportar café y cacao sostenibles bajo reglamento europeo EUDR. https://gob.pe/institucion/midagri/noticias/1177401",
        "MIDAGRI. (2025c). Perú Drive Agrarian Modernization with the Geolocation of More Than 140,000 Plots. https://gob.pe/institucion/midagri/noticias/1294143",
        "MIDAGRI. (2025d). MIDAGRI Drives Agrarian Modernization with the Geolocation of More Than 140,000 Plots. https://gob.pe/institucion/midagri/noticias/1294143",
        "MIDAGRI. (2025e). Estado y sector privado sellan alianza estratégica para cumplir con el EUDR. https://gob.pe/institucion/midagri/noticias/1250933",
        "MIDAGRI. (2025f). Piloto de exportación EUDR — Cenfrocafé. https://gob.pe/institucion/midagri/noticias/1235541",
        "MIDAGRI. (2025g). Peru Promotes Sustainable Coffee and Cocoa Production Models within the Framework of Compliance with the New EUDR Regulation. https://gob.pe/institucion/midagri/noticias/1194374",
        "MIDAGRI/DRASAM. (2025). San Martín impulsa agricultura digital con geolocalización de parcelas de cacao y café. https://gob.pe/institucion/regionsanmartin-dra/noticias/1268490",
        "Parlamento Europeo y Consejo de la Unión Europea. (2023). Reglamento (UE) 2023/1115 relativo a los productos asociados a la deforestación y la degradación forestal. https://eur-lex.europa.eu/eli/reg/2023/1115/oj/eng",
        "Parlamento Europeo y Consejo de la Unión Europea. (2025). Reglamento de Postergación — entrada en vigor diferida para grandes empresas (30 de diciembre de 2026) y pymes europeas (30 de junio de 2027).",
        "PROMPERÚ. (2025). PROMPERÚ prepara a exportadores de café y cacao para el reglamento europeo contra la deforestación. https://gob.pe/institucion/promperu/noticias/1354427",
        "Reuters. (2026, 2 de septiembre). EU deforestation law to force compliance even on non-EU coffee supply chains, study finds. Reuters. https://reuters.com/business/environment/eu-deforestation-law-force-compliance-even-non-eu-coffee-supply-chains-study-2026-09-02/",
        "Trase. (2026, 1 de septiembre). Trase Brings Greater Transparency to Global Coffee Supply Chains. Trase. https://trase.earth/insights/trase-brings-greater-transparency-to-global-coffee-supply-chains",
        "Trabocca. (2025). Tabaconas, Peru. https://trabocca.com/our-coffees/peru/cajamarca/tabaconas/",
        "Universidad del Pacífico. (2026). Café peruano libre de deforestación: desafíos y oportunidades en el mercado europeo. Journal of Business UP, 17(1). https://doi.org/10.21678/jb.2026.2498",
        "Zero Deforestation Hub. (2025). How Is Peru Progressing Towards Compliance with the EUDR? https://zerodeforestationhub.eu/news/how-is-peru-progressing-towards-compliance-with-the-eudr/",
    ]

    for ref in referencias:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        p.paragraph_format.line_spacing = LINE_SPACING
        p.paragraph_format.first_line_indent = Inches(0.5)
        p.paragraph_format.left_indent = Inches(0)
        run = p.add_run(ref)
        run.font.name = FONT
        run.font.size = FONT_SIZE_BODY
        run.font.color.rgb = BLACK

    # Guardar
    doc.save(OUTPUT_PATH)
    print(f"Documento guardado en: {OUTPUT_PATH}")


if __name__ == "__main__":
    build_document()
