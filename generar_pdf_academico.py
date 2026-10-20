# -*- coding: utf-8 -*-
"""
Genera PDF académico estilo Universidad del Pacífico con reportlab.
Título: Cooperativas Peruanas y EUDR
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, inch
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
import os

# ─── REGISTRO DE FUENTES ──────────────────────────────────────────────────
font_dir = r"C:\Windows\Fonts"
pdfmetrics.registerFont(TTFont("Times",      os.path.join(font_dir, "times.ttf")))
pdfmetrics.registerFont(TTFont("Times-Italic", os.path.join(font_dir, "timesi.ttf")))
pdfmetrics.registerFont(TTFont("Times-Bold",   os.path.join(font_dir, "timesbd.ttf")))
pdfmetrics.registerFont(TTFont("Times-BoldItalic", os.path.join(font_dir, "timesbi.ttf")))

# ─── CONSTANTES DE PÁGINA ─────────────────────────────────────────────────
PAGE_W, PAGE_H = A4  # 595.28 x 841.89 pt
MARGIN_H = 2.5 * cm
MARGIN_V = 2.5 * cm
BODY_W = PAGE_W - 2 * MARGIN_H

OUTPUT = r"C:\Users\acuba\ISCAM_UU_Peru_EUDR_DocumentoTrabajo.pdf"

# ─── ESTILOS ─────────────────────────────────────────────────────────────
def make_styles():
    base = getSampleStyleSheet()

    cover_title = ParagraphStyle("CoverTitle",
        fontName="Times-Bold", fontSize=16, leading=20,
        alignment=TA_CENTER, spaceAfter=6,
        textColor=colors.black)

    cover_subtitle = ParagraphStyle("CoverSubtitle",
        fontName="Times-Bold", fontSize=12, leading=16,
        alignment=TA_CENTER, spaceAfter=4,
        textColor=colors.black)

    cover_normal = ParagraphStyle("CoverNormal",
        fontName="Times", fontSize=10, leading=14,
        alignment=TA_CENTER, spaceAfter=4,
        textColor=colors.black)

    cover_label = ParagraphStyle("CoverLabel",
        fontName="Times-Bold", fontSize=10, leading=14,
        alignment=TA_CENTER, spaceAfter=4,
        textColor=colors.black)

    h1 = ParagraphStyle("H1",
        fontName="Times-Bold", fontSize=13, leading=16,
        alignment=TA_LEFT, spaceBefore=14, spaceAfter=6,
        textColor=colors.black)

    h2 = ParagraphStyle("H2",
        fontName="Times-Bold", fontSize=12, leading=15,
        alignment=TA_LEFT, spaceBefore=10, spaceAfter=4,
        textColor=colors.black)

    h3 = ParagraphStyle("H3",
        fontName="Times-BoldItalic", fontSize=11, leading=14,
        alignment=TA_LEFT, spaceBefore=8, spaceAfter=3,
        textColor=colors.black)

    body = ParagraphStyle("Body",
        fontName="Times", fontSize=11, leading=16,
        alignment=TA_JUSTIFY, spaceBefore=0, spaceAfter=8,
        firstLineIndent=30, textColor=colors.black)

    body_noindent = ParagraphStyle("BodyNoIndent",
        fontName="Times", fontSize=11, leading=16,
        alignment=TA_JUSTIFY, spaceBefore=0, spaceAfter=8,
        textColor=colors.black)

    kw = ParagraphStyle("Keywords",
        fontName="Times-Italic", fontSize=11, leading=16,
        alignment=TA_LEFT, spaceBefore=0, spaceAfter=10,
        firstLineIndent=30, textColor=colors.black)

    ref = ParagraphStyle("Reference",
        fontName="Times", fontSize=10, leading=14,
        alignment=TA_JUSTIFY, spaceBefore=0, spaceAfter=6,
        firstLineIndent=25, leftIndent=-25,
        textColor=colors.black)

    tbl_hdr = ParagraphStyle("TblHdr",
        fontName="Times-Bold", fontSize=9, leading=12,
        alignment=TA_CENTER, textColor=colors.black)

    tbl_cell = ParagraphStyle("TblCell",
        fontName="Times", fontSize=9, leading=12,
        alignment=TA_LEFT, textColor=colors.black)

    return dict(
        cover_title=cover_title, cover_subtitle=cover_subtitle,
        cover_normal=cover_normal, cover_label=cover_label,
        h1=h1, h2=h2, h3=h3,
        body=body, body_noindent=body_noindent,
        kw=kw, ref=ref,
        tbl_hdr=tbl_hdr, tbl_cell=tbl_cell
    )


# ─── HELPERS ─────────────────────────────────────────────────────────────
BL = colors.black
LG = colors.HexColor("#D9D9D9")
DG = colors.HexColor("#404040")

TBL_STYLE = TableStyle([
    ("GRID",       (0,0), (-1,-1), 0.4, BL),
    ("BACKGROUND", (0,0), (-1,0),  LG),
    ("FONTNAME",   (0,0), (-1,0),  "Times-Bold"),
    ("FONTSIZE",   (0,0), (-1,0),  9),
    ("FONTNAME",   (0,1), (-1,-1), "Times"),
    ("FONTSIZE",   (0,1), (-1,-1), 9),
    ("LEADING",    (0,0), (-1,-1), 12),
    ("TOPPADDING", (0,0), (-1,-1), 4),
    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ("LEFTPADDING",  (0,0), (-1,-1), 5),
    ("RIGHTPADDING", (0,0), (-1,-1), 5),
    ("ALIGN",     (0,0), (-1,0),  "CENTER"),
    ("VALIGN",    (0,0), (-1,-1), "TOP"),
])


def spacer(pt=8):
    return Spacer(1, pt)


def rule(width=BODY_W, thickness=0.5, color=BL):
    return HRFlowable(width=width, thickness=thickness, color=color,
                      spaceAfter=4, spaceBefore=4)


# ─── PÁGINA DE PORTADA ───────────────────────────────────────────────────
def build_cover(story, S):
    story.append(Spacer(1, 0.8 * cm))

    story.append(Paragraph("UNIVERSIDAD DEL PACÍFICO", S["cover_label"]))
    story.append(Paragraph("Grupo de Investigación ISCAM — Cadenas de Valor Agrarias", S["cover_normal"]))
    story.append(Paragraph("Centro de Investigación de la Universidad del Pacífico (CIUP)", S["cover_normal"]))
    story.append(spacer(0.3 * cm))
    story.append(rule(BODY_W, 1.0))
    story.append(spacer(0.3 * cm))

    story.append(Paragraph("DOCUMENTO DE TRABAJO", S["cover_label"]))
    story.append(Paragraph(
        "Serie: Documentos de Trabajo — Economía y Gestión de Cadenas de Valor / N.º DT-ISCAM-2026-001",
        S["cover_normal"]))
    story.append(spacer(0.5 * cm))

    story.append(Paragraph(
        "Cooperativas Peruanas y el Reglamento de la Unión Europea<br/>contra la Deforestación (EUDR)",
        S["cover_title"]))
    story.append(spacer(0.3 * cm))
    story.append(Paragraph(
        "Diagnóstico de la Cadena de Valor, Gaps de Trazabilidad<br/>y Agenda de Preparación",
        S["cover_subtitle"]))
    story.append(spacer(0.5 * cm))
    story.append(rule(BODY_W, 1.0))
    story.append(spacer(0.5 * cm))

    datos = [
        ("Autor:", "Investigador Principal, Grupo ISCAM"),
        ("Institución:", "Universidad del Pacífico — Lima, Perú"),
        ("Fecha:", "Octubre 2026"),
        ("Clasificación de riesgo país:",
         "Riesgo estándar — Reglamento de Ejecución (UE) 2025/1093"),
        ("Cadenas priorizadas:", "Café · Cacao · Palma aceitera"),
    ]
    for label, valor in datos:
        story.append(Paragraph(
            f"<b>{label}</b> {valor}", S["cover_normal"]))

    story.append(spacer(1.5 * cm))
    story.append(Paragraph(
        "<i>Documento de trabajo para uso interno del grupo de investigación ISCAM.</i>",
        ParagraphStyle("disclaimer", fontName="Times-Italic", fontSize=9,
                       leading=12, alignment=TA_CENTER, textColor=DG)))

    story.append(PageBreak())


# ─── ENCABEZADO / PIE DE PÁGINA ─────────────────────────────────────────
class AcademicNumberedCanvas:
    """Agrega número de página en la esquina inferior derecha."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __init__(self):
        pass

from reportlab.pdfgen import canvas as pdfcanvas

def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Times", 9)
    canvas.setFillColor(BL)
    page_num = canvas.getPageNumber()
    text = f"{page_num}"
    canvas.drawRightString(PAGE_W - MARGIN_H, 1.5 * cm, text)
    # línea superior de página
    canvas.setStrokeColor(BL)
    canvas.setLineWidth(0.3)
    canvas.line(MARGIN_H, PAGE_H - 1.3 * cm, PAGE_W - MARGIN_H, PAGE_H - 1.3 * cm)
    canvas.restoreState()


# ─── CONSTRUCCIÓN DEL PDF ────────────────────────────────────────────────
def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        leftMargin=MARGIN_H,
        rightMargin=MARGIN_H,
        topMargin=2.0 * cm,
        bottomMargin=2.0 * cm,
        title="Cooperativas Peruanas y EUDR — Documento de Trabajo ISCAM",
        author="Investigador ISCAM — Universidad del Pacífico",
        subject="EUDR, trazabilidad, cooperativas agrarias, Perú",
    )

    S = make_styles()
    story = []

    # PORTADA
    build_cover(story, S)

    # RESUMEN
    story.append(Paragraph("Resumen", S["h1"]))
    story.append(Paragraph(
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
        "cinco ejes prioritarios para la agenda de preparación: formalización de la propiedad, escalamiento "
        "de la geolocalización, interoperabilidad de plataformas, acceso a financiamiento para certificaciones, "
        "y fortalecimiento de la articulación con compradores europeos.",
        S["body"]))

    # ABSTRACT
    story.append(spacer(6))
    story.append(Paragraph("Abstract", S["h1"]))
    story.append(Paragraph(
        "This working paper examines the challenges and opportunities faced by Peruvian agricultural cooperatives "
        "in the context of the EU Deforestation Regulation (EUDR). It analyses the regulatory framework, "
        "Peru's country-risk classification as standard-risk under Commission Implementing Regulation (EU) "
        "2025/1093, and the institutional infrastructure deployed by the Peruvian state to prepare exporters. "
        "The document identifies leading cooperatives in the coffee, cocoa, and palm oil value chains that "
        "have achieved advanced traceability levels, as well as those still in preparation stages. Key gaps "
        "in geolocation, land tenure, aggregation traceability, and due diligence evidence generation are "
        "documented. The analysis concludes that organized cooperatives with existing digital infrastructure "
        "constitute the segment most likely to achieve timely compliance, and five priority axes are "
        "identified for the preparation agenda: property formalization, geolocation upscaling, platform "
        "interoperability, access to certification financing, and strengthened articulation with European buyers.",
        S["body"]))

    # PALABRAS CLAVE
    story.append(spacer(6))
    story.append(Paragraph("Palabras clave", S["h1"]))
    story.append(Paragraph(
        "EUDR · deforestación · trazabilidad · debida diligencia · cooperativas agrarias · café · cacao · "
        "palma aceitera · Perú · Unión Europea",
        S["kw"]))

    # ─── 1. INTRODUCCIÓN ─────────────────────────────────────────────────
    story.append(Paragraph("1. Introducción", S["h1"]))
    story.append(Paragraph(
        "El comercio internacional de commodities agrarios enfrenta desde finales de 2024 un cambio regulatorio "
        "estructural de alcance global. El Reglamento (UE) 2023/1115 relativo a los productos asociados a la "
        "deforestación y la degradación forestal (EUDR, por sus siglas en inglés), adoptado el 31 de mayo "
        "de 2023, prohíbe la comercialización, exportación e importación en el mercado de la Unión Europea "
        "de ganado bovino, cacao, café, palma aceitera, caucho, soja y madera que hayan sido producidos en "
        "tierras deforestadas con posterioridad al 31 de diciembre de 2020, o cuya producción haya vulnerado "
        "la legislación aplicable del país de origen en materia de tenencia de tierra, uso de suelo, derechos "
        "laborales o derechos de pueblos indígenas (Parlamento Europeo y Consejo de la Unión Europea, 2023).",
        S["body"]))
    story.append(Paragraph(
        "La norma exige que todo lote exportado a la Unión Europea esté respaldado por una Declaración de "
        "Debida Diligencia (DDS) presentada por el importador europeo ante el sistema TRACES/NTIS de la "
        "Comisión Europea. La DDS se fundamenta en información proporcionada por el exportador no comunitario: "
        "geolocalización de parcelas productoras en formato WGS-84, código arancelario, volumen, datos del "
        "proveedor y documentación de tenencia de tierra, entre otros requisitos. El importador debe además "
        "demostrar que evaluó y, en su caso, mitigó los riesgos identificados antes del envío "
        "(European Commission, 2024).",
        S["body"]))
    story.append(Paragraph(
        "Perú ha sido clasificado como país de riesgo estándar en el Anexo del Reglamento de Ejecución "
        "(UE) 2025/1093 de la Comisión Europea, publicado el 22 de mayo de 2025. Esta clasificación "
        "implica que el importador europeo debe cumplir la debida diligencia completa en sus tres etapas "
        "—recopilación de información, evaluación de riesgo y medidas de mitigación— para cada lote de "
        "café, cacao o palma aceitera de origen peruano. La debida diligencia simplificada, prevista en "
        "el Artículo 13 del EUDR para países de bajo riesgo, no resulta aplicable "
        "(European Commission, 2025).",
        S["body"]))
    story.append(Paragraph(
        "El presente documento de trabajo tiene como objetivo proporcionar un diagnóstico integral del "
        "estado de preparación de las cooperativas agrarias peruanas ante el EUDR. El documento se "
        "organiza en seis secciones: tras esta introducción, la segunda sección desarrolla el marco "
        "normativo y las obligaciones que la norma impone a exportadores y compradores. La tercera "
        "sección presenta la respuesta institucional del Estado peruano. La cuarta sección identifica "
        "y caracteriza a las cooperativas líderes en las cadenas de café, cacao y palma aceitera. La "
        "quinta sección documenta los compradores europeos activos en Perú y las plataformas tecnológicas "
        "en uso. La sexta sección presenta las conclusiones y la agenda de investigación.",
        S["body"]))

    # ─── 2. MARCO NORMATIVO ───────────────────────────────────────────────
    story.append(Paragraph("2. Marco Normativo del EUDR y Obligaciones para Exportadores", S["h1"]))

    story.append(Paragraph(
        "2.1 Las tres condiciones de cumplimiento para todo lote exportado a la UE", S["h2"]))
    story.append(Paragraph(
        "El EUDR establece tres condiciones simultáneas que deben cumplirse para cada lote exportado a "
        "la Unión Europea (Parlamento Europeo y Consejo de la Unión Europea, 2023). En primer lugar, "
        "la condición de no deforestación exige que la parcela donde se produjo el commodity no haya "
        "sido objeto de deforestación con posterioridad al 31 de diciembre de 2020. En segundo lugar, "
        "la condición de producción legal requiere que la producción haya respetado la legislación "
        " aplicable del país de origen en materia de tenencia de tierra, uso de suelo, ambiental, "
        "laboral y derechos de pueblos indígenas. En tercer lugar, la condición de debida diligencia "
        "exige que el importador europeo haya completado el procedimiento de DDS antes de la "
        "comercialización del lote en la UE.",
        S["body"]))

    story.append(Paragraph("2.2 Las tres etapas de la debida diligencia completa", S["h2"]))
    story.append(Paragraph(
        "La debida diligencia completa —aplicable a Perú como país de riesgo estándar— se despliega "
        "en tres etapas secuenciales (European Commission, 2024). La primera etapa consiste en la "
        "recopilación de información sobre el lote, que debe incluir: coordenadas de geolocalización "
        "de las parcelas productoras en formato WGS-84 (EPSG:4326), con polígono obligatorio para "
        "parcelas iguales o mayores a 4 hectáreas y punto GPS para parcelas menores; país, "
        "departamento y provincia de producción; código arancelario HS; nombre, RUC y dirección del "
        "proveedor; nombre y dirección del comprador; fecha de cosecha; documentos de tenencia de "
        "tierra; historial de cobertura forestal, y registros de acopio (guías de remisión, actas de "
        "entrega, registros de pesaje) que vinculen la parcela con el lote exportado (CBI, 2025). "
        "La segunda etapa corresponde a la evaluación de riesgo, mediante la cual el importador "
        "europeo determina si existen indicios de que el lote incumpla las condiciones 1 o 2. La "
        "tercera etapa, aplicable cuando se identifican riesgos, exige la adopción de medidas de "
        "mitigación antes del envío del lote.",
        S["body"]))

    story.append(Paragraph(
        "2.3 Fecha de entrada en vigencia y obligaciones del exportador peruano", S["h2"]))
    story.append(Paragraph(
        "El Reglamento de Postergación, acordado en diciembre de 2025, fijó la fecha de entrada en "
        "vigor del EUDR para grandes y medianas empresas en el 30 de diciembre de 2026, y para "
        "microempresas y pequeñas empresas europeas en el 30 de junio de 2027 (Parlamento Europeo "
        "y Consejo de la Unión Europea, 2025). Sin embargo, desde 2025 los compradores europeos "
        "vienen exigiendo evidencias de cumplimiento a sus proveedores como práctica comercial "
        "anticipatoria, independientemente de la fecha de aplicabilidad formal (PROMPERÚ, 2025; "
        "AYP Digital, 2025).",
        S["body"]))
    story.append(Paragraph(
        "Del lado del exportador peruano, la obligación central consiste en entregar al importador "
        "europeo, por cada lote, la información descrita en la primera etapa de la debida diligencia. "
        "Esta obligación se traduce en requisitos operativos concretos: sistemas de geolocalización a "
        "nivel de parcela, trazabilidad durante las etapas de acopio primario y secundario, y "
        "documentación legal de la cadena de custodia. Según fuentes del sector, aproximadamente "
        "el 80% de los pequeños productores carece de un título de propiedad formal que respalde la "
        "documentación de tenencia de tierra requerida. Esta brecha constituye uno de los obstáculos "
        "más significativos para el cumplimiento oportuno (AYP Digital, 2025; CamcaféPeru, 2025).",
        S["body"]))

    story.append(Paragraph("2.4 Clasificación de riesgo país y niveles de control", S["h2"]))
    story.append(Paragraph(
        "La primera clasificación oficial de países según nivel de riesgo fue publicada mediante el "
        "Reglamento de Ejecución (UE) 2025/1093 de la Comisión Europea, con fecha 22 de mayo de 2025. "
        "El Anexo del Reglamento clasifica 140 países como de bajo riesgo —entre los que se encuentran "
        "todos los países de la UE, Chile, Costa Rica, Kenia, Laos, Papúa Nueva Guinea, Ruanda, "
        "Vietnam, Estados Unidos, China y Japón—, cuatro países como de alto riesgo (Bielorrusia, "
        "Rusia, Myanmar y Corea del Norte), y el resto, incluyendo Perú, como riesgo estándar. Los "
        "países de bajo riesgo gozan de la posibilidad de aplicar la debida diligencia simplificada; "
        "los países de alto riesgo están sujetos a controles sobre el 9% de los operadores y el 9% "
        "del volumen de importación. Perú, como riesgo estándar, enfrenta controles sobre el 3% de "
        "los operadores que declaren productos covered (European Commission, 2025).",
        S["body"]))

    # Tabla clasificación
    tbl_data = [
        [Paragraph("<b>Categoría de riesgo</b>", S["tbl_hdr"]),
         Paragraph("<b>Control autoridades UE</b>", S["tbl_hdr"]),
         Paragraph("<b>DD requerida</b>", S["tbl_hdr"]),
         Paragraph("<b>Países ejemplo</b>", S["tbl_hdr"])],
        [Paragraph("Bajo riesgo", S["tbl_cell"]),
         Paragraph("1% operadores/año", S["tbl_cell"]),
         Paragraph("Simplificada (solo recopilación)", S["tbl_cell"]),
         Paragraph("UE, Chile, Costa Rica, Kenia, Laos, PNG, Ruanda, Vietnam, EE.UU., China, Japón", S["tbl_cell"])],
        [Paragraph("Riesgo estándar (Perú)", S["tbl_cell"]),
         Paragraph("3% operadores/año", S["tbl_cell"]),
         Paragraph("Completa en 3 etapas", S["tbl_cell"]),
         Paragraph("Perú, Brasil, Colombia, Indonesia, Bolivia, Paraguay, México, Argentina", S["tbl_cell"])],
        [Paragraph("Alto riesgo", S["tbl_cell"]),
         Paragraph("9% operadores + 9% volumen", S["tbl_cell"]),
         Paragraph("Completa reforzada", S["tbl_cell"]),
         Paragraph("Bielorrusia, Rusia, Myanmar, Corea del Norte", S["tbl_cell"])],
    ]
    tbl = Table(tbl_data, colWidths=[3.8*cm, 3.2*cm, 3.5*cm, 5.5*cm])
    tbl.setStyle(TBL_STYLE)
    story.append(tbl)
    story.append(spacer(10))

    # ─── 3. RESPUESTA INSTITUCIONAL ─────────────────────────────────────
    story.append(Paragraph("3. La Respuesta Institucional del Estado Peruano", S["h1"]))

    story.append(Paragraph(
        "3.1 Panorama cuantitativo de la preparación nacional", S["h2"]))
    story.append(Paragraph(
        "El Ministerio de Desarrollo Agrario y Riego (MIDAGRI) ha reportado avances significativos en "
        "la preparación del sector agrario peruano. A través de la plataforma AGRODIGITAL y el Padrón "
        "de Productores Agrarios (PPA), se han geolocalizado más de 150,000 polígonos de parcelas "
        "productoras de café, cacao y palma aceitera, cubriendo 13 regiones del país. El PPA registra "
        "2.03 millones de productores inscritos, de los cuales aproximadamente 410,000 corresponde a "
        "productores de café, cacao y palma aceitera. El análisis espacial del MIDAGRI confirma que el "
        "99% de los productores de estos tres commodities inscritos en el PPA se ubica en zonas "
        "instaladas antes del año 2020, dato que constituye la base de la constancia de libre "
        "deforestación emitida por la plataforma. El MIDAGRI ha reportado además que 150 exportadores "
        "peruanos se encuentran alineando sus procesos internos con los requisitos del EUDR, y que se "
        "han remitido más de 260 comunicaciones a asociaciones, cooperativas y empresas para la "
        "remisión de polígonos de parcelas (MIDAGRI, 2025a, 2025b, 2025c, 2025d).",
        S["body"]))

    story.append(Paragraph("3.2 Actores institucionales y roles", S["h2"]))
    story.append(Paragraph(
        "La respuesta institucional ha involucrado a múltiples actores públicos y privados. El MIDAGRI "
        "actúa como líder de la estrategia nacional, responsable de la plataforma AGRODIGITAL/PPA, "
        "la plataforma de trazabilidad en desarrollo y la coordinación interinstitucional. El Ministerio "
        "de Comercio Exterior y Turismo (MINCETUR), a través de PROMPERÚ, ejecuta programas de "
        "preparación de exportadores: en 2025 se beneficiaron 21 organizaciones y 7,880 productores "
        "de Cajamarca, San Martín y Lima (PROMPERÚ, 2025). El Ministerio del Ambiente, a través de "
        "la plataforma GeoBosques, realiza el cruce de parcelas geolocalizadas con mapas de cobertura "
        "forestal para verificar la existencia de la parcela previa a 2020. ADEX, mediante el "
        "convenio firmado con MIDAGRI y MINCETUR en septiembre de 2025, aporta asistencia técnica y "
        "capacitación a productores y exportadores durante un período de dos años (MIDAGRI, 2025e). "
        "La cooperación internacional ha desempeñado un rol relevante: la GIZ ha brindado apoyo "
        "técnico al MIDAGRI en geolocalización y estrategia EUDR; el IICA ha coordinado la "
        "capacitación y articulación con gobiernos regionales; la FAO ha facilitado la interoperabilidad "
        "con el WHISP; y la Cooperación Suiza, Helvetas Perú y Solidaridad ejecutan proyectos de "
        "trazabilidad en campo como AGROInnova y Amazonía Link.",
        S["body"]))

    story.append(Paragraph("3.3 Infraestructura pública en operación", S["h2"]))
    story.append(Paragraph(
        "La infraestructura digital pública desplegada comprende cuatro componentes principales. El "
        "aplicativo AGRODIGITAL, desarrollado por MIDAGRI, permite la geolocalización de parcelas "
        "con GPS y funciona en modo offline, característica fundamental para zonas rurales amazónicas "
        "sin conectividad. El aplicativo cruza las parcelas geolocalizadas con los datos de GeoBosques "
        "y emite la Constancia de Libre Deforestación, documento que integra el expediente de debida "
        "diligencia. La plataforma de trazabilidad del MIDAGRI, esperada para 2026, tiene como objetivo "
        "conectar la parcela del productor con el contenedor de exportación, vinculando el DNI del "
        "productor registrado en el manifiesto de carga con las parcelas georreferenciadas en el PPA. "
        "En el ámbito del cacao, la herramienta MICACAO, desarrollada por Helvetas Perú y Open Cocoa "
        "Chain, proporciona trazabilidad digital a lo largo de la cadena, conectando productores, "
        "cooperativas y exportadores, y validando la cero deforestación mediante un sistema de "
        "verificación estandarizado (GIZ, 2025; MIDAGRI, 2025d).",
        S["body"]))

    story.append(Paragraph("3.4 Convenios estratégicos con compradores europeos", S["h2"]))
    story.append(Paragraph(
        "Un hito relevante es el Memorando de Entendimiento firmado entre JDE Peet's —mayor tostador "
        "de café del mundo— y el Estado peruano, para la verificación de deforestación cero mediante "
        "la empresa Enveritas. El MoU contempla la identificación de parcelas ubicadas en tierras "
        "deforestadas con posterioridad a 2020 y el diseño de mecanismos de remediación. JDE Peet's "
        "utiliza además Farmer Connect (blockchain) para la trazabilidad lote por lote, con más de "
        "40 datapoints por lote, y ha extendido su acceso a la plataforma blockchain a sus "
        "proveedores en Perú (JDE Peet's, 2024, 2025).",
        S["body"]))

    # Tabla actores
    actores_data = [
        [Paragraph("<b>Actor</b>", S["tbl_hdr"]),
         Paragraph("<b>Rol en la preparación EUDR</b>", S["tbl_hdr"])],
        [Paragraph("MIDAGRI", S["tbl_cell"]),
         Paragraph("Líder de estrategia nacional. Geolocalización (AGRODIGITAL/PPA), plataforma de trazabilidad en desarrollo, coordinación interinstitucional.", S["tbl_cell"])],
        [Paragraph("MINCETUR / PROMPERÚ", S["tbl_cell"]),
         Paragraph("Preparación de exportadores. Programa DD con 21 organizaciones y 7,880 productores en 2025.", S["tbl_cell"])],
        [Paragraph("Ministerio del Ambiente / GeoBosques", S["tbl_cell"]),
         Paragraph("Cruce de parcelas geolocalizadas con mapas de cobertura forestal.", S["tbl_cell"])],
        [Paragraph("ADEX", S["tbl_cell"]),
         Paragraph("Alianza estratégica con MIDAGRI y MINCETUR (convenio septiembre 2025).", S["tbl_cell"])],
        [Paragraph("GIZ", S["tbl_cell"]),
         Paragraph("Apoyo técnico a MIDAGRI en geolocalización y estrategia EUDR.", S["tbl_cell"])],
        [Paragraph("IICA", S["tbl_cell"]),
         Paragraph("Coordinación técnica, capacitación, articulación con gobiernos regionales.", S["tbl_cell"])],
        [Paragraph("FAO", S["tbl_cell"]),
         Paragraph("WHISP como plataforma de interoperabilidad internacional.", S["tbl_cell"])],
        [Paragraph("Cooperación Suiza / Helvetas / Solidaridad", S["tbl_cell"]),
         Paragraph("Financiamiento y ejecución de proyectos de trazabilidad en campo (AGROInnova, Amazonía Link).", S["tbl_cell"])],
    ]
    tbl2 = Table(actores_data, colWidths=[5.0*cm, 11.0*cm])
    tbl2.setStyle(TBL_STYLE)
    story.append(tbl2)
    story.append(spacer(10))

    # ─── 4. COOPERATIVAS ─────────────────────────────────────────────────
    story.append(Paragraph("4. El Universo de Cooperativas y Organizaciones de Productores", S["h1"]))

    story.append(Paragraph("4.1 Cadena de café", S["h2"]))
    story.append(Paragraph(
        "4.1.1 Nivel avanzado: cooperativas con trazabilidad operativa y exportaciones EUDR", S["h3"]))
    story.append(Paragraph(
        "La Cooperativa de Servicios Múltiples Cenfrocafé Perú, con sede en Jaén, Cajamarca, y "
        "operaciones en el departamento de Amazonas, constituye una de las organizaciones más "
        "avanzadas del sector cafetalero peruano. Agrupa a 3,000 pequeños productores de café "
        "distribuidos en 12 distritos y opera una filial europea, Cenfrocafé AG (Suiza), que "
        "facilita el comercio directo con tostadores europeos. La cooperativa cuenta con trazabilidad "
        "completa a nivel de parcela, certificaciones Rainforest Alliance, Fairtrade y orgánica, y "
        "protocolos de no deforestación implementados desde hace varios ciclos productivos. Cenfrocafé "
        "participó en los pilotos de exportación EUDR organizados por el MIDAGRI en 2025, con envíos "
        "de café a Beneke Coffee (Alemania) e ICAM (Italia). En el distrito de Tabaconas, San "
        "Ignacio, la cooperativa trabaja con 154 productores individuales organizados en 12 "
        "asociaciones locales —entre ellas, El Laurel, La Palta y El Cedro— mediante esquemas de "
        "trazabilidad a nivel de parcela que constituyen un referente metodológico para el sector "
        "(Coop Coffees, 2025; Trabocca, 2025; MIDAGRI, 2025f).",
        S["body"]))
    story.append(Paragraph(
        "La Cooperativa Agraria Cafetalera Satipo, ubicada en la provincia de Satipo, Junín, "
        "agrupa aproximadamente 3,350 productores organizados en 7 organizaciones a través del "
        "programa SAFE. El programa SAFE opera en tres módulos: gestión de cadena, evaluación de "
        "riesgo EUDR y digitalización. La cooperativa fue visitada por una misión europea conjunta "
        "EU-Holanda-Alemania y participó en pilotos de exportación EUDR en 2025 (Zero Deforestation "
        "Hub, 2025; MIDAGRI, 2025g). La Cooperativa Agraria Sonomoro, en Pangoa, Junín, opera "
        "bajo dinámicas similares y forma parte del programa SAFE. La Cooperativa Agraria APROCAM, "
        "en Bagua, Amazonas, y PIMCOS Coffee, en Jaén, Cajamarca —que en 2025 ejecutó una "
        "exportación piloto de 45 toneladas—, completan el grupo de cooperativas con participación "
        "documentada en los pilotos de debida diligencia del MIDAGRI.",
        S["body"]))

    story.append(Paragraph(
        "4.1.2 Nivel en preparación: geolocalización en curso", S["h3"]))
    story.append(Paragraph(
        "Un conjunto de organizaciones de productores de café se encuentra en fase de "
        "geolocalización y preparación operativa. Las cooperativas de El Dorado, San Martín, "
        "están siendo apoyadas por la Agencia de Desarrollo Económico Local (ADEL) de El Dorado, "
        "el IICA y la DRASAM en la geolocalización de parcelas (MIDAGRI/DRASAM, 2025). La "
        "Asociación de Productores Cuencas del Huallaga, en San Martín, y la Asociación Productores "
        "Café Organero Gera, en Moyobamba, fueron visitadas por el MIDAGRI en el marco de los "
        "pilotos de debida diligencia. En la zona del VRAE, la ACPC Pichanaki y Kemito Ene, "
        "ambas en Junín, fueron visitadas por la misión europea y producen café y cacao bajo "
        "sistemas agroforestales que constituyen una base favorable para la demostración de "
        "producción libre de deforestación.",
        S["body"]))

    story.append(Paragraph("4.2 Cadena de cacao", S["h2"]))
    story.append(Paragraph(
        "En la cadena de cacao, Allima Cacao, organización de productores de Chazuta, San Martín, "
        "destaca como caso piloto de exportación EUDR. En 2025 ejecutó un piloto de exportación "
        "de más de 45 toneladas de cacao fine flavor y orgánico a Silva Cacao (Bélgica), con "
        "trazabilidad a nivel de parcela validada a través de la plataforma AGRODIGITAL. Las "
        "cooperativas de Junín y Ucayali —Satipo, Sonomoro, ACPC Pichanaki y Kemito Ene— operan "
        "en la producción de cacao bajo sistemas agroforestales en la amazonía central y cuentan "
        "con el componente de debida diligencia estructurado dentro del programa SAFE (Zero "
        "Deforestation Hub, 2025). El proyecto Amazonía Link, ejecutado por Solidaridad, ha "
        "logrado georreferenciar parcelas y generar reportes de cero deforestación para 737 "
        "productores de café, cacao y palma aceitera, analizando un territorio de 60,000 km² "
        "(ANDINA, 2025).",
        S["body"]))

    story.append(Paragraph("4.3 Cadena de palma aceitera", S["h2"]))
    story.append(Paragraph(
        "La cadena de palma aceitera presenta una estructura diferenciada, con mayor concentración "
        "en empresas agroindustriales y núcleos de pequeños productores integrados a plantas "
        "procesadoras. Los desafíos de titulación y geolocalización son análogos a los del café "
        "y cacao, pero la estructura de la cadena y la menor organización de los productores "
        "vegetales constituyen factores adicionales de complejidad. La organización APROMAN, en "
        "Ucayali, alcanzó el Hito A de certificación RSPO en agosto de 2025 y espera la emisión "
        "del certificado. ASPASH, también en Ucayali, obtuvo la elegibilidad RSPO en 2025 y se "
        "encuentra en proceso de certificación. La Asociación Santa Lucía alcanzó el Hito A de "
        "certificación RSPO en octubre de 2025, en el marco de su articulación comercial con "
        "Alicorp. Las organizaciones APPACHE y UNIPALMA se encuentran en proceso de solicitud de "
        "membresía RSPO (Alicorp, 2025). El Grupo Palmas/Alicorp, a través de su programa Palma "
        "Sostenible, ha alcanzado un nivel de trazabilidad corporativa del 77% hasta plantación "
        "por polígono en su cadena de abastecimiento, constituyendo el mayor avance de trazabilidad "
        "en la cadena de palma aceitera peruana (Alicorp, 2025).",
        S["body"]))

    # ─── 5. COMPRADORES Y PLATAFORMAS ─────────────────────────────────────
    story.append(Paragraph("5. Compradores Europeos y Plataformas Tecnológicas", S["h1"]))
    story.append(Paragraph(
        "El mercado europeo de café y cacao cuenta con cuatro compradores que han mantenido "
        "presencia documentada en Perú y que, por su perfil de riesgo de suministro, se encuentran "
        "entre los más expuestos al EUDR. Silva Cacao (Bélgica) opera en la cadena de cacao de "
        "especialidad, con el piloto EUDR 2025 con Allima Cacao como antecedente inmediato. "
        "Beneke Coffee (Alemania) y ICAM (Italia) participan en la cadena de café a través de los "
        "pilotos organizados por el MIDAGRI. JDE Peet's (Países Bajos), como mayor tostador de "
        "café del mundo, representa el caso de mayor escala: su MoU con el Estado peruano, la "
        "contratación de Enveritas como verificador independiente, y su participación accionaria "
        "en Farmer Connect le confieren una posición única en el ecosistema de trazabilidad "
        "(JDE Peet's, 2024, 2025).",
        S["body"]))
    story.append(Paragraph(
        "Desde la perspectiva de la economía de cadenas de suministro, el estudio de Trase "
        "publicado el 1 de septiembre de 2026 proyecta que el EUDR ejercerá presión sobre "
        "empresas con alta exposición a la UE para extender los requisitos de debida diligencia "
        "a toda su cadena global, y no únicamente a los lotes destinados al mercado europeo. "
        "Los datos de Trase revelan que el 79% del café global es manejado por importadores que "
        "simultáneamente surten al mercado de la Unión Europea. Para empresas como JDE Peet's "
        "(84% de su café con exposición a la UE), Louis Dreyfus (63%) y Neumann Gruppe (53%), "
        "mantener cadenas segregadas —una para la UE con cumplimiento EUDR y otra para mercados "
        "sin regulación— resulta más costoso que aplicar los estándares EUDR a toda su cadena de "
        "suministro. Este fenómeno de extensión extraterritorial de la regulación constituye un "
        "incentivo estructural para que los exportadores peruanos cumplan los requisitos EUDR "
        "incluso cuando venden a compradores no europeos (Trase, 2026; Reuters, 2026).",
        S["body"]))

    # Tabla compradores
    compr_data = [
        [Paragraph("<b>Comprador</b>", S["tbl_hdr"]),
         Paragraph("<b>País</b>", S["tbl_hdr"]),
         Paragraph("<b>Producto</b>", S["tbl_hdr"]),
         Paragraph("<b>Perfil EUDR</b>", S["tbl_hdr"])],
        [Paragraph("Silva Cacao", S["tbl_cell"]),
         Paragraph("Bélgica", S["tbl_cell"]),
         Paragraph("Cacao", S["tbl_cell"]),
         Paragraph("Specialty, fine flavor. Piloto EUDR 2025 con Allima Cacao.", S["tbl_cell"])],
        [Paragraph("Beneke Coffee", S["tbl_cell"]),
         Paragraph("Alemania", S["tbl_cell"]),
         Paragraph("Café", S["tbl_cell"]),
         Paragraph("Tostador. Piloto EUDR 2025 con PIMCOS y Satipo.", S["tbl_cell"])],
        [Paragraph("ICAM", S["tbl_cell"]),
         Paragraph("Italia", S["tbl_cell"]),
         Paragraph("Cacao", S["tbl_cell"]),
         Paragraph("Chocolate de especialidad. Piloto EUDR 2025.", S["tbl_cell"])],
        [Paragraph("JDE Peet's", S["tbl_cell"]),
         Paragraph("Países Bajos", S["tbl_cell"]),
         Paragraph("Café", S["tbl_cell"]),
         Paragraph("Mayor tostador del mundo. MoU con Perú. Enveritas como verificador. Accionista de Farmer Connect (blockchain).", S["tbl_cell"])],
    ]
    tbl3 = Table(compr_data, colWidths=[3.2*cm, 2.0*cm, 2.0*cm, 8.8*cm])
    tbl3.setStyle(TBL_STYLE)
    story.append(tbl3)
    story.append(spacer(10))

    story.append(Paragraph(
        "El ecosistema de trazabilidad disponible para las cooperativas peruanas comprende "
        "plataformas tecnológicas, estándares de certificación y sistemas de monitoreo satelital, "
        "con diferentes niveles de madurez y costos de implementación. Enveritas, empresa de "
        "verificación con uso de drones, inteligencia artificial e imágenes satelitales para el "
        "análisis de deforestación post-2020 a nivel territorial, es el verificador contratado "
        "por JDE Peet's. Farmer Connect, plataforma de trazabilidad basada en blockchain con "
        "más de 40 datapoints por lote, es accesible para cooperativas que surten a grandes "
        "tostadores con programas blockchain activos. En materia de certificación, Rainforest "
        "Alliance —que incluye un componente de deforestación y legalidad en sus estándares— "
        "certifica aproximadamente el 40% del café peruano exportado. La certificación RSPO "
        "en palma aceitera proporciona un marco de trazabilidad hasta plantación directamente "
        "alineable con los requisitos del EUDR. GeoBosques y Global Forest Watch proporcionan "
        "datos de cobertura forestal que permiten verificar la existencia de parcela previa a 2020.",
        S["body"]))

    # ─── 6. CONCLUSIONES ──────────────────────────────────────────────────
    story.append(Paragraph("6. Conclusiones", S["h1"]))
    story.append(Paragraph(
        "El presente documento de trabajo permite identificar cinco hallazgos principales. En "
        "primer lugar, Perú enfrenta el EUDR desde una posición de preparación institucional "
        "relativamente avanzada, sustentada en la geolocalización de más de 150,000 parcelas a "
        "través de AGRODIGITAL y en la interoperabilidad lograda con plataformas internacionales "
        "de monitoreo. No obstante, la brecha de formalización de la propiedad —el 80% de los "
        "pequeños productores carece de título de propiedad— constituye el principal obstáculo "
        "para la construcción de expedientes de debida diligencia válidos.",
        S["body"]))
    story.append(Paragraph(
        "En segundo lugar, las cooperativas organizadas con infraestructura digital preexistente "
        "—Cenfrocafé, la Cooperativa Agraria Cafetalera Satipo, Allima Cacao y las "
        "organizaciones de palma aceitera avanzadas— se encuentran en condiciones de cumplir "
        "los requisitos del EUDR para la fecha de entrada en vigencia. Estas organizaciones "
        "se benefician de certificaciones existentes, trazabilidad operativa a nivel de parcela, "
        "y relaciones comerciales establecidas con compradores europeos que ya aplican estándares "
        "de debida diligencia.",
        S["body"]))
    story.append(Paragraph(
        "En tercer lugar, el EUDR tendrá efectos de extensión extraterritorial significativos. "
        "El dato de Trase (2026) según el cual el 79% del café global es manejado por "
        "importadores con exposición a la UE implica que los estándares de debida diligencia se "
        "incorporarán a la práctica comercial habitual de los principales compradores de café "
        "y cacao peruano, independientemente de que el lote final se destine o no al mercado "
        "europeo.",
        S["body"]))
    story.append(Paragraph(
        "En cuarto lugar, la agenda de preparación prioritaria debe articularse en torno a "
        "cinco ejes: (i) la formalización masiva de la propiedad rural mediante COFOPRI y los "
        "mecanismos de titulación del MIDAGRI; (ii) el escalamiento de la geolocalización a "
        "las cooperativas que aún no cuentan con polígonos registrados en AGRODIGITAL; "
        "(iii) la interoperabilidad técnica de las plataformas existentes con el sistema "
        "TRACES/NTIS de la UE; (iv) el acceso a financiamiento para los costos de "
        "certificación, verificación y adecuación de sistemas, particularmente para "
        "organizaciones de pequeño y mediano tamaño; y (v) el fortalecimiento de la "
        "articulación comercial directa con compradores europeos mediante la cualificación "
        "de las capacidades de negociación y cumplimiento de las cooperativas.",
        S["body"]))
    story.append(Paragraph(
        "En quinto lugar, la investigación futura debería abordar la cuantificación del costo "
        "de cumplimiento EUDR para cooperativas de diferente escala, el análisis de mecanismos "
        "de financiamiento para la adecuación, y la evaluación de la efectividad de las "
        "plataformas públicas de trazabilidad en la generación de evidencia de debida "
        "diligencia reconocida por las autoridades europeas. El presente documento de trabajo "
        "busca contribuir a esta agenda proporcionando un diagnóstico integral del estado de "
        "situación que sirva como línea base para la investigación y la formulación de "
        "políticas.",
        S["body"]))

    # ─── REFERENCIAS ──────────────────────────────────────────────────────
    story.append(Paragraph("Referencias", S["h1"]))

    referencias = [
        "Alicorp. (2025). <i>Reporte de Responsabilidad Compartida RSPO 2025</i>. https://alicorp.com.pe/s3/media/PDF/reporte_de_responsabilidad_compartida_rspo_2025.pdf",
        "ANDINA. (2025). Café, palma y cacao: productores amazónicos aplican prácticas libres de deforestación. https://andina.pe/agencia//noticia.aspx?id=1092048",
        "AYP Digital. (2025). EUDR: Trazabilidad documental para exportadores peruanos. https://aypdigital.com/blog/eudr-reglamento-ue-deforestacion-trazabilidad-exportadores-peru/",
        "CamcaféPeru. (2025). EUDR y trazabilidad para pequeños productores. https://camcafeperu.com.pe/EN/article.php?id=236",
        "CBI. (2025). <i>7 Tips on How to Become EUDR Compliant in Coffee</i>. https://cbi.eu/market-information/coffee/tips-become-eudr-compliant",
        "Coop Coffees. (2025). CENFROCAFE Profile. https://coopcoffees.com/member/profile/cenfrocafe-943467",
        "European Commission. (2024). <i>EU Deforestation Regulation: Guidance for Operators and Customs Authorities</i>. https://environment.ec.europa.eu/topics/forests/deforestation/regulation-deforestation-free-products_en",
        "European Commission. (2025). Reglamento de Ejecución (UE) 2025/1093 de la Comisión, de 22 de mayo de 2025. https://eur-lex.europa.eu/eli/reg_impl/2025/1093/oj/eng",
        "GIZ. (2025). <i>Adaptación a las Normativas de Trazabilidad para la Inclusión de Pequeños Productores en América Latina</i>. https://giz.de/en/downloads/giz2025-es-latin-america-digital-traceability-tools.pdf",
        "JDE Peet's. (2024). <i>Green Coffee Human Rights &amp; Environmental Due Diligence Framework</i>. https://jdepeets.com/siteassets/.../jde-peets-green-coffee-hredd-framework.pdf",
        "JDE Peet's. (2025). <i>JDE Peet's Signs MOUs with Honduras, Peru and Rwanda to Combat Coffee-Related Deforestation</i>. https://jdepeets.com/news-container/jde-peets-signs-mous-with-honduras-peru-and-rwanda-2865109/",
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
        "Reuters. (2026, 2 de septiembre). <i>EU deforestation law to force compliance even on non-EU coffee supply chains, study finds</i>. Reuters. https://reuters.com/business/environment/eu-deforestation-law-force-compliance-even-non-eu-coffee-supply-chains-study-2026-09-02/",
        "Trase. (2026, 1 de septiembre). <i>Trase Brings Greater Transparency to Global Coffee Supply Chains</i>. Trase. https://trase.earth/insights/trase-brings-greater-transparency-to-global-coffee-supply-chains",
        "Trabocca. (2025). Tabaconas, Peru. https://trabocca.com/our-coffees/peru/cajamarca/tabaconas/",
        "Universidad del Pacífico. (2026). Café peruano libre de deforestación: desafíos y oportunidades en el mercado europeo. <i>Journal of Business UP</i>, 17(1). https://doi.org/10.21678/jb.2026.2498",
        "Zero Deforestation Hub. (2025). How Is Peru Progressing Towards Compliance with the EUDR? https://zerodeforestationhub.eu/news/how-is-peru-progressing-towards-compliance-with-the-eudr/",
    ]

    for ref in referencias:
        story.append(Paragraph(ref, S["ref"]))

    # BUILD
    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"PDF guardado en: {OUTPUT}")


if __name__ == "__main__":
    build_pdf()
