# -*- coding: utf-8 -*-
"""
Genera DT-ISCAM-001: Documento de Trabajo — Índice ISCAM
Versión 4.0 — Formato Universidad del Pacífico · APA 7ma · Solo blanco y negro
100% español · python-docx 1.2.0
"""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ── PALETA BLANCO Y NEGRO ──────────────────────────────────
NEGRO        = RGBColor(0x00, 0x00, 0x00)
GRIS_FONDON  = RGBColor(0xF2, 0xF2, 0xF2)   # para celdas alternas
GRIS_LIGHT   = RGBColor(0xD9, 0xD9, 0xD9)   # bordes sutiles

OUT = r'C:\Users\acuba\eudrperu\DT-ISCAM-001_Indice_ISCAM_Trabajo.docx'

# ── HELPERS ───────────────────────────────────────────────
def cell_border_bottom(cell, color_hex='000000'):
    """Borde inferior negro en celda."""
    tc = cell._tc; tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '4')
    bottom.set(qn('w:space'), '0')
    bottom.set(qn('w:color'), color_hex)
    tcBorders.append(bottom)
    tcPr.append(tcBorders)

def cell_bg(cell, hex_color):
    tc = cell._tc; tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color.upper().lstrip('#')); tcPr.append(shd)

def set_para_spacing(para, before=0, after=6, line_rule=None, line=None):
    """Espaciado párrafo: before Pt, after Pt, interlineado 1.5."""
    para.paragraph_format.space_before = Pt(before)
    para.paragraph_format.space_after  = Pt(after)
    if line_rule:
        para.paragraph_format.line_spacing_rule = line_rule
    if line:
        para.paragraph_format.line_spacing = line

def set_justified(para):
    para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

def body_para(doc, text, italic=False, size=12, before=0, after=6):
    """Párrafo de cuerpo — Times New Roman 12, justificado, 1.5 líneas."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after  = Pt(after)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.5
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(size)
    run.italic = italic
    run.font.color.rgb = NEGRO
    # Sangría primera línea (excepto epígrafes y fórmulas)
    if before == 0:
        pf.first_line_indent = Cm(1.25)
    return p

def heading1(doc, text):
    """H1 — negrita, centrado, 14pt, espacio 12/6, sin sangría."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf = p.paragraph_format
    pf.space_before = Pt(18)
    pf.space_after  = Pt(6)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.5
    pf.keep_with_next = True
    pf.first_line_indent = Cm(0)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(14)
    run.bold = True
    run.font.color.rgb = NEGRO
    return p

def heading2(doc, text):
    """H2 — negrita, 12pt, espacio 10/4, sin sangría."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf = p.paragraph_format
    pf.space_before = Pt(12)
    pf.space_after  = Pt(4)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.5
    pf.keep_with_next = True
    pf.first_line_indent = Cm(0)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.bold = True
    run.font.color.rgb = NEGRO
    return p

def heading3(doc, text):
    """H3 — negrita cursiva, 12pt, espacio 8/4, sin sangría."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf = p.paragraph_format
    pf.space_before = Pt(8)
    pf.space_after  = Pt(4)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.5
    pf.keep_with_next = True
    pf.first_line_indent = Cm(0)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.bold = True
    run.italic = True
    run.font.color.rgb = NEGRO
    return p

def epigrafe(doc, text):
    """Cita destacada — cursiva, cuerpo 11, justificado."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf = p.paragraph_format
    pf.space_before = Pt(6); pf.space_after = Pt(6)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.5
    pf.first_line_indent = Cm(0)
    pf.left_indent = Cm(1.5)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(11)
    run.italic = True
    run.font.color.rgb = RGBColor(0x40, 0x40, 0x40)
    return p

def bullet_item(doc, text, size=12):
    p = doc.add_paragraph(style='List Bullet')
    pf = p.paragraph_format
    pf.space_before = Pt(0); pf.space_after = Pt(3)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.5
    pf.first_line_indent = Cm(0)
    pf.left_indent = Cm(1.0)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(size)
    run.font.color.rgb = NEGRO
    return p

def formula_block(doc, text, size=10):
    """Bloque de fórmula — Courier New 10, justificado, fondo gris claro."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf = p.paragraph_format
    pf.space_before = Pt(5); pf.space_after = Pt(5)
    pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
    pf.first_line_indent = Cm(0)
    pf.left_indent = Cm(1.0)
    run = p.add_run(text)
    run.font.name = 'Courier New'
    run.font.size = Pt(size)
    run.font.color.rgb = NEGRO
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), 'F2F2F2'); pPr.append(shd)
    return p

def th_row(table, headers, bg='000000'):
    """Fila de encabezado — texto blanco, fondo negro."""
    row = table.rows[0]
    for i, h in enumerate(headers):
        c = row.cells[i]; c.text = ''
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pf = p.paragraph_format
        pf.space_before = Pt(3); pf.space_after = Pt(3)
        pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
        run = p.add_run(h)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        c.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        cell_bg(c, bg)
    return row

def add_row(table, values, bg=None, bold=False, fs=9.5, center_cols=None):
    row = table.add_row()
    for i, v in enumerate(values):
        c = row.cells[i]; c.text = ''
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        if center_cols and i in center_cols:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pf = p.paragraph_format
        pf.space_before = Pt(2); pf.space_after = Pt(2)
        pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
        pf.first_line_indent = Cm(0)
        run = p.add_run(str(v))
        run.font.name = 'Times New Roman'
        run.font.size = Pt(fs)
        run.bold = bold
        run.font.color.rgb = NEGRO
        c.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        if bg: cell_bg(c, bg)
    return row

def page_break(doc):
    p = doc.add_paragraph()
    run = p.add_run()
    from docx.enum.text import WD_BREAK
    run.add_break(WD_BREAK.PAGE)
    # Página en blanco → sin numerar

def footnote_para(doc, text):
    """Nota al pie — 9pt, espacio simple."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf = p.paragraph_format
    pf.space_before = Pt(2); pf.space_after = Pt(2)
    pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
    pf.first_line_indent = Cm(0)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(9)
    run.font.color.rgb = NEGRO
    return p

# ═══════════════════════════════════════════════════════════
# CONSTRUCCIÓN DEL DOCUMENTO
# ═══════════════════════════════════════════════════════════
doc = Document()

# Márgenes 2.54 cm (1 pulgada) — estándar APA
for section in doc.sections:
    section.top_margin    = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin  = Cm(2.54)
    section.right_margin  = Cm(2.54)
    # Pie de página: número a la derecha
    footer = section.footer
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pfp = fp.paragraph_format
    pfp.space_before = Pt(4)
    r1 = fp.add_run('DT-ISCAM-001 · Índice ISCAM · Universidad del Pacífico 2026       pág. ')
    r1.font.name = 'Times New Roman'; r1.font.size = Pt(9)
    r1.font.color.rgb = NEGRO
    r2 = fp.add_run()
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    r2._r.append(fldChar1)
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = ' PAGE '
    r3 = fp.add_run()
    r3._r.append(instrText)
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')
    r4 = fp.add_run('1')
    r4.font.name = 'Times New Roman'; r4.font.size = Pt(9)
    r4.font.color.rgb = NEGRO

# ── PORTADA ───────────────────────────────────────────────
# Estilo: Documento de Trabajo UP — sin color, tipografía simple

def portada_line(doc, text, size, bold, space_before, centered=True):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if centered else WD_ALIGN_PARAGRAPH.LEFT
    pf = p.paragraph_format
    pf.space_before = Pt(space_before)
    pf.space_after  = Pt(0)
    pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
    pf.first_line_indent = Cm(0)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(size)
    run.bold = bold
    run.font.color.rgb = NEGRO
    return p

portada_line(doc, 'UNIVERSIDAD DEL PACÍFICO', 12, True,  80)
portada_line(doc, 'DOCUMENTO DE TRABAJO', 12, False,  6)
portada_line(doc, 'DT-ISCAM-001', 12, True,  4)

portada_line(doc, '', 12, False, 20)  # espacio

portada_line(doc, 'ÍNDICE ISCAM DE SOSTENIBILIDAD Y CONFORMIDAD', 14, True,  0)
portada_line(doc, 'El impacto del Pacto Verde Europeo en la performance', 13, True,  6)
portada_line(doc, 'de las cooperativas de café y cacao del Perú', 13, True,  0)

portada_line(doc, '', 12, False, 14)

# Línea separadora
p_line = doc.add_paragraph()
p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_line.paragraph_format.space_before = Pt(0)
p_line.paragraph_format.space_after  = Pt(0)
r = p_line.add_run('_' * 62)
r.font.name = 'Times New Roman'; r.font.size = Pt(10)
r.font.color.rgb = NEGRO

portada_line(doc, '', 12, False, 10)
portada_line(doc, 'Elaborado por: Equipo Técnico ISCAM', 11, False,  0)
portada_line(doc, 'Proyecto EUDR Perú — Universidad del Pacífico', 11, False,  4)
portada_line(doc, '', 12, False, 8)
portada_line(doc, 'Pregunta de investigación:', 11, True, 0)
portada_line(doc,
    '"¿En qué medida el alineamiento con los pilares del Pacto Verde Europeo'
    ' mejora o compromete la performance comercial de las cooperativas '
    'de café y cacao del Perú?"',
    11, False, 2)

portada_line(doc, '', 12, False, 14)
portada_line(doc, 'Lima, octubre de 2026', 11, True, 0)

page_break(doc)

# ── ÍNDICE DE CONTENIDO (guía) ────────────────────────────
def toc_entry(doc, text, dots=True, size=12):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf = p.paragraph_format
    pf.space_before = Pt(0); pf.space_after = Pt(3)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.5
    pf.first_line_indent = Cm(0)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(size)
    run.font.color.rgb = NEGRO

heading1(doc, 'ÍNDICE DE CONTENIDO')
for item in [
    '1.  El problema económico: el Pacto Verde como restricción de mercado ......... 1',
    '2.  Mecanismos de transmisión: cómo llega la presión regulatoria a la cooperativa  ......... 2',
    '3.  Los seis pilares: el paisaje regulatorio visto desde la cadena de valor  ......... 3',
    '4.  Arquitectura del ISA-Completo: la lógica económica de la fórmula  ......... 5',
    '5.  La matriz IP × IV → RE: priorización operativa con lógica de intervención  ......... 7',
    '6.  Estado de la plantilla PLANTILLA_INDICE_PVE_ISCAM.xlsx  ......... 10',
    '7.  Limitaciones metodológicas  ......... 12',
    '8.  Hoja de ruta: cómo usar el índice para proteger el acceso al mercado  ......... 13',
    '     Anexo. Tabla de ponderadores ISCAM  ......... 15',
]:
    toc_entry(doc, item)

page_break(doc)

# ══════════════════════════════════════════════════════════
# 1. EL PROBLEMA ECONÓMICO
# ══════════════════════════════════════════════════════════
heading1(doc, '1. El problema económico: el Pacto Verde como restricción de mercado')

body_para(doc, (
    'Europa no está exportando regulación. Está exportando demanda. '
    'A partir de 2024, los compradores europeos de café y cacao — tostadores, '
    'distribuidores, marcas de consumo masivo — enfrentan obligaciones legales '
    'que les exigen verificar que lo que compran no contribuye a la deforestación, '
    'no implica trabajo forzoso y no viene de una cadena contaminada con plaguicidas '
    'prohibidos. Esas obligaciones no son opciones de sostenibilidad: '
    'son requisitos legales cuyo incumplimiento lleva multas de hasta el 4% de la '
    'facturación global.'
))

body_para(doc, (
    'La cadena de transmisión es directa y acelerada. '
    'Cuando un tostador alemán sabe que tiene que certificar la deforestación cero '
    'de cada lote que compra, le pide a su proveedor peruano — el exportador — '
    'que le demuestre trazabilidad lote a parcela. El exportador se lo pide '
    'a la cooperativa. La cooperativa tiene que pedírselo al productor. '
    'Todo esto ocurre antes de enero de 2025 para grandes operadores '
    'y antes de enero de 2026 para las pymes del sector. '
    'El que no puede responder a esa cadena queda fuera.'
))

epigrafe(doc, (
    '"El primer efecto del Pacto Verde no es ambiental. '
    'Es competitivo: excluye proveedores que no pueden probar '
    'que lo que venden cumple."'
))

body_para(doc, (
    'El objetivo del proyecto ISCAM es medir exactamente eso: '
    'cuánto alineamiento tiene cada organización con los seis pilares '
    'del Pacto Verde Europeo, dónde están sus vulnerabilidades más graves, '
    'y cómo asignar los recursos de cooperación técnica de forma que '
    'maximice el número de organizaciones que siguen pudiendo exportar a Europa. '
    'No es un ejercicio de cumplimiento normativo. Es un análisis de riesgo '
    'de mercado con enfoque de cadena de valor.'
))

# ══════════════════════════════════════════════════════════
# 2. MECANISMOS DE TRANSMISIÓN
# ══════════════════════════════════════════════════════════
heading1(doc, '2. Mecanismos de transmisión: cómo llega la presión regulatoria a la cooperativa')

body_para(doc, (
    'La presión del Pacto Verde no llega de golpe ni de forma uniforme. '
    'Llega a través de cuatro canales que operan en tiempos distintos y '
    'activan resortes diferentes en la organización.'
))

t_can = doc.add_table(rows=1, cols=4)
t_can.style = 'Table Grid'; t_can.alignment = WD_TABLE_ALIGNMENT.CENTER
t_can.columns[0].width = Cm(1.0)
t_can.columns[1].width = Cm(3.8)
t_can.columns[2].width = Cm(3.5)
t_can.columns[3].width = Cm(7.7)
th_row(t_can, ['Canal', 'Descripción', 'Horizonte', 'Qué le pide al exportador / cooperativa'], bg='000000')

canales = [
    ('1', 'Exigencia contractual de trazabilidad',
     'Ya vigente',
     'Coordenadas geográficas de parcela, segregación de lotes, evidencia de no deforestación. Fuente: EUDR Art. 2 y 3.'),
    ('2', 'Diligencia debida del comprador europeo',
     '2024–2026',
     'Evaluación de riesgos en la cadena, plan de mitigación, reporte anual. Fuente: CSDDD y EUDR Art. 2(40).'),
    ('3', 'Presión de mercado por huella de carbono',
     '2025–2028',
     'Datos de emisiones Scope 3, métrica de intensidad por kg de café/cacao exportado. Fuente: CSRD, CalCafé v2.1.'),
    ('4', 'Restricciones fitosanitarias en frontera',
     'Permanente',
     'Límites máximos de residuos (LMR) en frontera UE. Rechazo en puerto = pérdida efectiva del envío. Fuente: RASFF, Farm to Fork -50%.'),
]
for rd in canales:
    add_row(t_can, rd, fs=9.5, center_cols=[0, 2])

body_para(doc, '', after=4)

body_para(doc, (
    'La implicación clave para las organizaciones peruanas es que estos canales '
    'no operan de forma aislada: un exportador que no puede dar trazabilidad '
    'lote a parcela pierde primero su certificado EUDR; '
    'después, sus compradores europeos no pueden cumplir su propia diligencia debida '
    'y buscan otro proveedor. '
    'La falla en un canal acelera la falla en los demás. '
    'Esto es lo que hace que el riesgo sea sistémico y no puntual.'
), italic=True, size=11)

# ══════════════════════════════════════════════════════════
# 3. LOS SEIS PILARES
# ══════════════════════════════════════════════════════════
heading1(doc, '3. Los seis pilares: el paisaje regulatorio visto desde la cadena de valor')

body_para(doc, (
    'El Pacto Verde Europeo se traduce en seis pilares normativos '
    'que afectan directamente a la cadena de café y cacao del Perú. '
    'Cada pilar tiene un canal de transmisión a la cooperativa, '
    'un instrumento de verificación, y un costo de no cumplir: '
    'no el costo ambiental —ese es el problema de Europa— '
    'sino el costo de mercado: la exclusión del comprador.'
))

t_pilar = doc.add_table(rows=1, cols=5)
t_pilar.style = 'Table Grid'; t_pilar.alignment = WD_TABLE_ALIGNMENT.CENTER
t_pilar.columns[0].width = Cm(1.4)
t_pilar.columns[1].width = Cm(3.2)
t_pilar.columns[2].width = Cm(3.4)
t_pilar.columns[3].width = Cm(3.4)
t_pilar.columns[4].width = Cm(4.6)
th_row(t_pilar, ['Pilar', 'Nombre', 'Normativa UE', 'Qué le piden a la cooperativa', 'Costo de no cumplir'], bg='000000')

pilares = [
    ('(i)', 'Huella de carbono y GEI',
     'Taxonomía UE · CSRD · CBAM',
     'Medición de emisiones Scope 1–3; intensidad por kg exportado',
     'Exclusión de compradores con obligación CSRD; pérdida de prima de carbono'),
    ('(ii)', 'Deforestación y trazabilidad',
     'EUDR 2023/1115',
     'Geolocalización parcelas, verificación cero deforestación, trazabilidad lote a parcela',
     'Multas hasta 4% facturación global; exclusión del mercado UE'),
    ('(iii)', 'Diligencia debida DD.HH.',
     'EUDR Art. 2(40) · CSDDD',
     'Evaluación de riesgos, medidas de mitigación, monitoreo de productores',
     'Ruptura contractual con comprador EU; responsabilidad compartida en la cadena'),
    ('(iv)', 'Reporte de sostenibilidad',
     'CSRD · ESRS · Taxonomía Verde',
     'Indicadores ESG, reporte de riesgos ambientales y sociales en la cadena',
     'Descalificación como proveedor por compradores con obligación CSRD'),
    ('(v)', 'Economía circular y envases',
     'PPWR · Plan Acción EC UE',
     'Diseño de envases, contenido reciclado, gestión de residuos del beneficio',
     'Barreras no arancelarias; rechazo en puerto por packaging'),
    ('(vi)', 'Farm to Fork — Pesticidas y LMR',
     'Directiva 2009/128/CE · RASFF',
     'Gestión fitosanitaria, LMR dentro de umbrales UE, manejo integrado de plagas',
     'Retención o rechazo en frontera UE — misma consecuencia que la deforestación'),
]
for i, rd in enumerate(pilares):
    bg = 'F2F2F2' if i % 2 == 1 else None
    add_row(t_pilar, rd, bg=bg, fs=9, center_cols=[0])

body_para(doc, '', after=4)
body_para(doc, (
    'Lo que revela esta tabla es que los seis pilares no son normas independientes: '
    'son las diferentes caras de un mismo sistema de señales que los compradores europeos '
    'usan para filtrar proveedores. '
    'Una cooperativa que domina la trazabilidad (pilar ii) '
    'ya tiene buena parte del camino andado hacia el pilar iii y el pilar iv. '
    'La estrategia inteligente no es cumplir cada norma por separado, '
    'sino construir capacidades transversales — trazabilidad, gestión ambiental, '
    'gobierno de datos, gobernanza — que respondan a varios pilares a la vez.'
), italic=True, size=11)

# ══════════════════════════════════════════════════════════
# 4. ARQUITECTURA DEL ISA-COMPLETO
# ══════════════════════════════════════════════════════════
heading1(doc, '4. Arquitectura del ISA-Completo: la lógica económica de la fórmula')

heading2(doc, '4.1  Por qué un índice unificado y por qué la ponderación 70/30')

body_para(doc, (
    'El ISA-Completo es el score que condensa en un solo número (escala 0–100) '
    'la posición de cada organización frente al ecosistema regulatorio europeo. '
    'Su diseño responde a una pregunta económica: '
    '¿cuál es el riesgo de mercado más urgente y cuál es el de mediano plazo?'
))

body_para(doc, (
    'La respuesta inmediata es el Reglamento de Deforestación (EUDR, pilar ii). '
    'Es la norma que ya tiene fecha de cumplimiento para pyme (enero 2026), '
    'multas concretas, y un mecanismo de verificación en frontera. '
    'Si una organización no puede demostrar trazabilidad lote a parcela hoy, '
    'el EUDR la excluye del mercado mañana. '
    'Eso hace que el cumplimiento del EUDR sea la restricción binding '
    'en el corto plazo: el cuello de botella.'
))

body_para(doc, (
    'Los otros cinco pilares (huella de carbono, diligencia debida, reporte, '
    'economía circular, fitosanitario) son igualmente reales y sus costos de '
    'no cumplir son significativos, pero su entrada en vigor es más gradual, '
    'su verificación menos automatizada, y su costo inmediato menos binario. '
    'Son condiciones de competitividad de mediano plazo: '
    'definen qué exportadores siguen siendo relevantes para los compradores europeos '
    'en 2028 y 2030, cuando el mercado se haya filtrado.'
))

body_para(doc, (
    'Por eso la ponderación 70/30. '
    'El 70% al EUDR (ISA-EUDR) refleja que es la restricción actual, '
    'la más verificable y la más binaria en sus consecuencias. '
    'El 30% a los módulos del Pacto Verde (ISA-PactoVerde) '
    'refleja que son condiciones necesarias de competitividad, no opcionales. '
    'Una cooperativa que hoy cumple EUDR pero ignora su huella de carbono '
    'y su gestión fitosanitaria está jugando solo el partido de hoy. '
    'El 30% es la asignación correcta para el partido de mañana.'
))

heading2(doc, '4.2  Fórmulas')

formula_block(doc, 'ISA-EUDR  = 0.875 × (D1×D2×...×D7)^(1/7) + 0.125 × (D8+D9)/2        [70% del ISA-Completo]')
formula_block(doc, 'ISA-PV    = (D12 + D13 + D14 + D15) / 4                                    [30% del ISA-Completo]')
formula_block(doc, 'ISA-Completo = 0.70 × ISA-EUDR + 0.30 × ISA-PV                              [escala 0–100]')

body_para(doc, '', after=2)

body_para(doc, (
    'ISA-EUDR usa media geométrica para el núcleo D1–D7. '
    'La decisión no es técnica: es económica. '
    'Las siete dimensiones núcleo — clasificación regulatoria, trazabilidad, '
    'deforestación, manejo ambiental, diligencia debida, información y documentación, '
    'relación con compradores — no son sustituibles entre sí. '
     'Un cero en diligencia debida (D5) no se compensa con un puntaje máximo en trazabilidad (D2): '
    'si un lote fue obtenido con trabajo forzoso, la trazabilidad perfecta '
    'no lo hace aceptable para el mercado UE. '
    'La geométrica captura esa lógica: el mínimo común denominador prevalece. '
    'El bloque extendido (D8–D9: gobernanza y riesgo financiero) '
    'usa media aritmética porque sí son sustituibles razonablemente: '
    'una gobernanza débil puede compensarse con financiamiento robusto, y viceversa.'
))

heading2(doc, '4.3  Los módulos del ISA-PactoVerde: estado actual')

t_dim = doc.add_table(rows=1, cols=4)
t_dim.style = 'Table Grid'; t_dim.alignment = WD_TABLE_ALIGNMENT.CENTER
t_dim.columns[0].width = Cm(1.6)
t_dim.columns[1].width = Cm(4.0)
t_dim.columns[2].width = Cm(4.2)
t_dim.columns[3].width = Cm(6.2)
th_row(t_dim, ['Dim.', 'Módulo', 'Herramienta de cálculo', 'Estado en la plantilla'], bg='000000')
for rd in [
    ('D12', 'Huella de carbono y GEI',
     'CalCafé v2.1 (café) · ISO 14040/44 · PEFCR',
     'Proxy IPCC/FAO; dato real al aplicar Instrumento 2'),
    ('D13', 'Reporte de sostenibilidad',
     'GRI · ESRS simplificado · Taxonomía UE · SFDR',
     'Pendiente Instrumento 2'),
    ('D14', 'Economía circular y envases',
     'PPWR · Plan Acción Economía Circular UE 2020',
     'Pendiente Instrumento 2'),
    ('D15', 'Gestión fitosanitaria y LMR',
     'Directiva 2009/128/CE · RASFF · Farm to Fork -50%',
     'Pendiente Instrumento 2 — brecha cacao abierta'),
]:
    add_row(t_dim, rd, fs=9.5, center_cols=[0])

body_para(doc, '', after=4)
body_para(doc, (
    'La cobertura de D12 (huella de carbono) tiene una brecha específica para cacao: '
    'CalCafé v2.1 cubre café pero no cacao. '
    'El Instrumento 2 aplica preguntas genéricas de gestión fitosanitaria '
    'a ambas cadenas, pero la cuantificación de huella de carbono para cacao '
    'requiere una herramienta separada que aún no existe validada.'
), italic=True, size=11)

# ══════════════════════════════════════════════════════════
# 5. MATRIZ IP × IV → RE
# ══════════════════════════════════════════════════════════
heading1(doc, '5. La matriz IP × IV → RE: priorización operativa con lógica de intervención')

body_para(doc, (
    'El ISA-Completo mide alineamiento. La matriz IP × IV → RE '
    'mide otra cosa: dada la posición de una organización frente al Pacto Verde, '
    '¿dónde hay que poner los recursos de cooperación técnica para que '
    'el mayor número de organizaciones sigan exportando a Europa?'
))

body_para(doc, (
    'La lógica es directa. '
    'Una organización puede tener un ISA alto (conoce los requisitos, '
    'tiene buena trazabilidad) pero estar altamente expuesta: '
    'es grande, depende de un solo comprador europeo, opera en zona deforestada. '
    'Ahí el riesgo no es de preparación sino de vulnerabilidad estructural: '
    'un shock de mercado —el comprador cambia de proveedor— la deja fuera. '
    'Necesita financiamiento verde, no capacitación.'
))

body_para(doc, (
    'Otra organización puede tener un ISA bajo y una vulnerabilidad baja: '
    'es pequeña, vende al mercado local, aún no siente la presión del Pacto Verde. '
    'Aquí el riesgo es el más peligroso de todos: el de la sorpresa. '
    'Cuando su exportador le diga que necesita geolocalización de parcela, '
    'puede ser demasiado tarde para reaccionar. '
    'Necesita intervención preventiva, no solo capacitación.'
))

heading2(doc, '5.1  Fórmulas de IP, IV y RE')

formula_block(doc, 'IP = REDONDEAR(PROMEDIO(IP1, IP2, IP3, IP4, IP5), 1)         [0–100]')
formula_block(doc, 'IV = REDONDEAR(PROMEDIO(IV1, IV2, IV3, IV4, IV5), 1)         [0–100]')
formula_block(doc, 'RE = REDONDEAR(IV × (1 − IP / 100), 1)                      [0–100]')

heading2(doc, '5.2  Sub-dimensiones del IP: qué capacidades importan para cumplir')

t_ip = doc.add_table(rows=1, cols=3)
t_ip.style = 'Table Grid'
t_ip.columns[0].width = Cm(2.6)
t_ip.columns[1].width = Cm(5.2)
t_ip.columns[2].width = Cm(8.2)
th_row(t_ip, ['Sub-dimensión', 'Qué capacidad mide', 'Fuente en Instrumento 2'], bg='000000')
for rd in [
    ('IP1 — Trazabilidad',
     'Capacidad de registrar productores, geolocalizar parcelas, segregar lotes',
     'D2 (Instrumento 2)'),
    ('IP2 — Cumplimiento ambiental',
     'Verificación de no deforestación, uso de suelo, manejo ambiental operativo',
     'D3 × D4 (media geométrica)'),
    ('IP3 — Gobernanza organizacional',
     'Control interno, sistemas de gestión, estructura de toma de decisiones',
     'D8 + D5 + D6 (parcial)'),
    ('IP4 — Información y documentación',
     'Bases de datos, evidencia documental, capacidad de monitoreo y reporte',
     'D6.23 + D2.9 (dimensión delgada — 2 ítems)'),
     ('IP5 — Capacidad de adaptación',
      'Acceso a financiamiento, certificaciones, relación con compradores',
      'D7 + D9 + Certificación (conteo 0/33/66/100; sin D11, que es inventario)'),
]:
    add_row(t_ip, rd, fs=9.5)

heading2(doc, '5.3  Sub-dimensiones del IV: dónde está la exposición')

t_iv = doc.add_table(rows=1, cols=3)
t_iv.style = 'Table Grid'
t_iv.columns[0].width = Cm(2.6)
t_iv.columns[1].width = Cm(5.2)
t_iv.columns[2].width = Cm(8.2)
th_row(t_iv, ['Sub-dimensión', 'Qué vulnerabilidad mide', 'Fuente de datos'], bg='000000')
for rd in [
    ('IV1 — Presión de mercado EU',
     'Dependencia de compradores europeos, concentración en pocos clientes EU',
     'Bloque P (P1, P1b, P4)'),
    ('IV2 — Exposición regulatoria',
     'Tipo de operador, nivel de responsabilidad declarativa frente al EUDR',
     'D1 (clasificación regulatoria, reúso invertido)'),
    ('IV3 — Fragilidad territorial',
     'Dispersión geográfica, tamaño de parcela, zona de riesgo de conversión',
     'D3.14 + Bloque 0 (preguntas de campo)'),
    ('IV4 — Brecha tecnológica',
     'Conectividad, acceso a herramientas digitales, capacidad de gestión de datos',
     'D6.24 + D9 (reúso invertido)'),
    ('IV5 — Riesgo social',
     'Concentración en un comprador, fricción interna, brecha de género en la directiva',
     'D7 + D8 + %mujeres en órgano directivo'),
]:
    add_row(t_iv, rd, fs=9.5)

heading2(doc, '5.4  Tipología 2×2: los cuatro cuadrantes operativos')

body_para(doc, (
    'Con IP e IV calculados, cada organización cae en uno de cuatro cuadrantes. '
    'El corte en 50 (escala 0–100) es una proxy de mediana muestral, '
    'pendiente de validar con datos reales del Instrumento 2.'
))

t_tip = doc.add_table(rows=1, cols=3)
t_tip.style = 'Table Grid'
t_tip.columns[0].width = Cm(2.6)
t_tip.columns[1].width = Cm(2.4)
t_tip.columns[2].width = Cm(11.0)
th_row(t_tip, ['Condición', 'Tipo', 'Implicación y acción'], bg='000000')
for rd in [
    ('IP ≥ 50 · IV < 50',
     'Resilientes',
     'Preparación alta, vulnerabilidad baja. Cumplen EUDR y módulos PV sin apoyo intensivo. '
     'Acción: monitoreo pasivo, conexión con compradores premium, acceso a financiamiento verde, '
     'posicionamiento en nichos de prima de carbono o certificación de biodiversidad.'),
    ('IP ≥ 50 · IV ≥ 50',
     'Expuestas-Adaptables',
     'Preparación alta pero exposición estructural. Conocen los requisitos pero dependen '
     'de un comprador o operan en zona vulnerable. '
     'Acción: financiamiento verde para diversificación, gestión fitosanitaria, '
     'apoyo en huella de carbono para cumplir CSRD de sus compradores.'),
    ('IP < 50 · IV < 50',
     'Riesgo Latente',
     'Baja preparación y baja vulnerabilidad aparente. Aún no sienten la presión del Pacto Verde. '
     'Son el grupo más peligroso: cuando sus compradores exijan trazabilidad, '
     'pueden quedar fuera sin aviso. '
     'Acción: intervención preventiva inmediata — la más rentable en términos de costo de oportunidad.'),
    ('IP < 50 · IV ≥ 50',
     'Riesgo Crítico',
     'Baja preparación y alta vulnerabilidad. Riesgo inminente de exclusión del mercado EU. '
     'Acción: apoyo técnico intensivo priorizado, financiamiento de adecuación, '
     'acompañamiento en trazabilidad, gestión fitosanitaria y huella de carbono.'),
]:
    add_row(t_tip, rd, fs=9.5, center_cols=[1])

body_para(doc, '', after=4)
body_para(doc, (
    'Las banderas duras — inh. vigente OSCE, trabajo forzoso confirmado, '
    'mezcla deliberada de lotes de origen no verificado — '
    'se reportan en la columna AD de ISCAM_Score y tienen precedencia '
    'sobre cualquier score. Son señales de exclusión directa del mercado.'
), italic=True, size=11)

# ══════════════════════════════════════════════════════════
# 6. ESTADO DE LA PLANTILLA
# ══════════════════════════════════════════════════════════
heading1(doc, '6. Estado de la plantilla PLANTILLA_INDICE_PVE_ISCAM.xlsx')

heading2(doc, '6.1  Arquitectura implementada')

t_hojas = doc.add_table(rows=1, cols=4)
t_hojas.style = 'Table Grid'
t_hojas.columns[0].width = Cm(2.8)
t_hojas.columns[1].width = Cm(5.5)
t_hojas.columns[2].width = Cm(4.2)
t_hojas.columns[3].width = Cm(3.5)
th_row(t_hojas, ['Hoja', 'Contenido', 'Estado', 'Score principal'], bg='000000')
for rd in [
    ('ISCAM_Score',
     '174 orgs × 38 cols — D1–D15, ISA-EUDR, ISA-Completo, IP, IV, RE, banderas duras',
     'Fórmula viva', 'ISA-Completo col AL'),
    ('SCORECARDS',
     'Dashboard IP/ISA — semáforo, tipología 2×2, ranking',
     'Actualizado', 'ISA-Completo col C'),
    ('MATRIZ_174',
     'Datos maestros — RUC, FOB, D3 Neon, D12–D15 proxy, Bloque P',
     'Intacta', '—'),
    ('PONDERADORES',
     'Pesos ISA-EUDR, ISA-PV, ISA-Completo, IP, IV, RE',
     'Actualizado', '—'),
    ('RADAR_BRECHAS',
     'D3 referenciando MATRIZ_174!U (scores Neon/OSCE)',
     'Actualizado', '—'),
    ('INSTRUCCIONES', 'Guía de uso de la plantilla', 'Original', '—'),
]:
    add_row(t_hojas, rd, fs=9)

heading2(doc, '6.2  Columnas clave del ISA-Completo')

t_ref = doc.add_table(rows=1, cols=3)
t_ref.style = 'Table Grid'
t_ref.columns[0].width = Cm(2.2)
t_ref.columns[1].width = Cm(6.5)
t_ref.columns[2].width = Cm(7.3)
th_row(t_ref, ['Columna', 'Fórmula', 'Qué representa'], bg='000000')
for rd in [
    ('AK (col 37)',
     '=SI.ERROR(REDONDEAR(RAIZ((D1*D2*...*D7)^(1/7)*0,875+((D8+D9)/2)*0,125),1),"N/A")',
     'ISA-EUDR: cumplimiento EUDR — 70% del score total'),
    ('AL (col 38)',
     '=SI.ERROR(SI(AK="N/A","N/A",REDONDEAR(0,70*AK+0,30*AI,1)),"N/A")',
     'ISA-Completo: score unificado 0–100 — ISA-EUDR 70% + ISA-PV 30%'),
    ('SCORECARDS!C',
     '=SI.ERROR(ISCAM_Score!AL4,"—")',
     'Referencia viva al ISA-Completo en el dashboard'),
    ('AI (col 35)',
     '=MATRIZ_174!AP (ISA-PV = promedio D12:D15)',
     'ISA-PactoVerde: módulos ambientales y de desempeño — 30% del score total'),
]:
    add_row(t_ref, rd, fs=9)

heading2(doc, '6.3  Qué está vivo y qué falta')

body_para(doc, 'Ya activo en la plantilla:')
for item in [
    'D2, D5, D6: datos de trazabilidad referencing SCORECARDS.',
    'D3: scores Neon/OSCE poblad en MATRIZ_174!U (36 organizaciones con inh. vigente).',
    'D12–D15: proxy compuesto direccional — no es dato medido.',
    'ISA-EUDR (col AK): fórmula geométrica viva, recalcula al llenar D1–D9.',
    'ISA-Completo (col AL): = 0.70×ISA-EUDR + 0.30×ISA-PV.',
    'IP, IV, RE: fórmulas vivas, recalculan al aplicar Instrumento 2.',
]:
    bullet_item(doc, item)

body_para(doc, 'Pendiente de aplicar en campo (Instrumento 2):')
for item in [
    'D1 — Clasificación regulatoria: afecta ISA-EUDR e IV2.',
    'D4 — Deforestación cero: afecta IP2 e ISA-EUDR.',
    'D7, D8, D9 — Presión comprador, gobernanza, riesgo financiero.',
    'D10, D11 — ítems pendientes de captura; se reportan aparte (bandera e inventario), no alimentan índices.',
    'D13, D14, D15 — Reporte sostenibilidad, economía circular, fitosanitario.',
]:
    bullet_item(doc, item)

# ══════════════════════════════════════════════════════════
# 7. LIMITACIONES
# ══════════════════════════════════════════════════════════
heading1(doc, '7. Limitaciones metodológicas')

body_para(doc, (
    'El índice ISCAM es una herramienta de trabajo construida sobre datos '
    'disponibles a octubre de 2026. Las siguientes limitaciones condicionan '
    'su uso y deben comunicarse a cualquier actor que tome decisiones '
    'basadas en los scores.'
))

limitaciones = [
    ('Proxy de D12 (huella de carbono): señal direccional, no dato medido.',
     'Las 45 organizaciones con D12=1 se determinaron por certificación orgánica/fairtrade '
     'o FOB UE > $500.000 sin certificación. No es la huella real. '
     'CalCafé v2.1 cubre café pero no cacao.'),
    ('IP4 (Información y documentación) es una dimensión delgada.',
     'Se sustenta en solo 2 ítems (D6.23 y D2.9), '
     'por debajo de las 4 sub-dimensiones que describe el diseño ISCAM. '
     'Se recomienda agregar 1–2 preguntas al Instrumento 2.'),
    ('ISA-EUDR requiere D1–D9 completos para funcionar correctamente.',
     'Si alguna dimensión D1–D7 falta, la geométrica produce 0 y el score se distorsiona. '
     'La lógica de re-ponderación por datos faltantes '
     '(excluir dimensión + redistribuir peso proporcionalmente) '
     'aún no está implementada en la fórmula Excel.'),
    ('D15 (gestión fitosanitaria): brecha cacao sin herramienta validada.',
     'Las preguntas aplican a ambas cadenas pero el umbral LMR del mercado UE '
     'puede diferir para cacao. La cuantificación requiere desarrollo adicional.'),
    ('Corte tipológico (50) es una proxy de validación pendiente.',
     'Se validará con datos reales una vez completado el Instrumento 2 en campo.'),
    ('Pesos sin panel AHP: los ponderadores son puntos de partida justificados.',
     'La estructura 87,5%/12,5% y 70%/30% se sustenta en bibliografía de OECD y JRC. '
     'El panel AHP con 8–10 expertos está pendiente de convocatoria.'),
    ('CBAM no aplica a café ni cacao hoy.',
     'El Mecanismo de Ajuste en Frontera por Carbono cubre acero, cemento, electricidad, '
     'fertilizantes, aluminio e hidrógeno. '
     'Expansión futura a productos agrícolas es un riesgo a monitorear.'),
    ('Biodiversidad sin peso en el ISA-Completo.',
     'Cubierta en la encuesta de productores (Instrumento 2) '
     'pero fuera del scope del índice por decisión metodológica documentada.'),
]

for label, texto in limitaciones:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf = p.paragraph_format
    pf.space_before = Pt(4); pf.space_after = Pt(4)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.5
    pf.first_line_indent = Cm(0)
    r1 = p.add_run(f'{label} ')
    r1.bold = True; r1.font.name = 'Times New Roman'
    r1.font.size = Pt(12); r1.font.color.rgb = NEGRO
    r2 = p.add_run(texto)
    r2.font.name = 'Times New Roman'; r2.font.size = Pt(12)
    r2.font.color.rgb = NEGRO

# ══════════════════════════════════════════════════════════
# 8. HOJA DE RUTA
# ══════════════════════════════════════════════════════════
heading1(doc, '8. Hoja de ruta: cómo usar el índice para proteger el acceso al mercado')

body_para(doc, (
    'La pregunta que responde esta sección no es "qué falta hacer" en abstracto. '
    'Es: dado que el EUDR está vigente y el mercado europeo se está filtrando, '
    '¿en qué orden hacemos las cosas para que el mayor número de organizaciones '
    'sigan pudiendo exportar a Europa?'
))

fases = [
    ('Fase 1 — Inmediato (0–30 días): proteger el acceso', [
        'Aplicar Instrumento 2 v0.2 (89 preguntas) en campo, comenzar con 5–8 organizaciones piloto '
        'para calibrar comprensión de preguntas y tiempo de aplicación.',
        'Poblar el registro de certificaciones vigentes (B0.9 → MATRIZ_174!AU/AV) con '
        'certificaciones conocidas (Rainforest, UTZ, Orgánico, Fairtrade, 4C) — dato accesible '
        'sin visita de campo; alimenta IP5 por conteo. D10 mismo es bandera: sus ítems se '
        'reportan aparte.',
        'Calibrar D3 con consulta directa a OSCE para organizaciones sin score en Neon.',
        'Evaluar comprensibilidad de D15.Q56–Q60 (gestión fitosanitaria) '
        'con técnicos de campo antes de escalar.',
    ]),
    ('Fase 2 — Corto plazo (1–3 meses): completar el mapa', [
        'Completar Instrumento 2 para las 174 organizaciones.',
        'Ejecutar panel AHP para validar pesos de IP, IV y la proporción 70/30 del ISA-Completo.',
        'Incorporar dato real de hectáreas deforestadas si disponible vía MIDAGRI o Gobierno Regional.',
        'Validar el corte tipológico (50) con datos completos y ajustar si la distribución lo amerita.',
        'Desarrollar o adaptar herramienta de huella de carbono para cacao '
        '(colaboración con CIFF, CATIE, CIPCA o aliado similar).',
    ]),
    ('Fase 3 — Mediano plazo (3–6 meses): convertir scores en acciones', [
        'Generar el primer ISA-Completo validado con datos de Instrumento 2.',
        'Clasificar las 174 organizaciones en los cuatro cuadrantes IP×IV.',
        'Diseñar plan de intervención por cuadrante: preventivo para Riesgo Latente, '
        'intensivo para Riesgo Crítico, estratégico para Expuestas-Adaptables.',
        'Preparar a organizaciones para requisitos CSRD de sus compradores europeos — '
        'los tostadores europeos grandes ya están en plena implementación.',
        'Evaluar necesidad de integrar datos SEACE para trazabilidad de contratos de compraventa.',
        'Publicar primera versión validada del índice en la plataforma EUDR Perú.',
    ]),
]

for fase, items in fases:
    heading2(doc, fase)
    for item in items:
        bullet_item(doc, item)

# ══════════════════════════════════════════════════════════
# ANEXO
# ══════════════════════════════════════════════════════════
page_break(doc)
heading1(doc, 'Anexo. Tabla de ponderadores ISCAM — Versión de trabajo')

body_para(doc, (
    'Los ponderadores de IP e IV (pesos iguales al 20% por sub-dimensión) '
    'son puntos de partida validados por bibliografía de OECD y JRC. '
    'El panel AHP con 8–10 expertos de cadena de valor café/cacao '
    'validará los pesos antes de la versión final. '
    'Se pueden modificar en la hoja PONDERADORES de la plantilla '
    'para análisis de sensibilidad.'
), size=11, after=6)

t_pond = doc.add_table(rows=1, cols=3)
t_pond.style = 'Table Grid'
t_pond.columns[0].width = Cm(3.4)
t_pond.columns[1].width = Cm(6.2)
t_pond.columns[2].width = Cm(3.4)
th_row(t_pond, ['Sub-dimensión', 'Fórmula de cálculo', 'Peso'], bg='000000')

datos_pond = [
    ('ISA-EUDR',      '= 0,875×∛(D1×D2×...×D7) + 0,125×(D8+D9)/2',     '100%'),
    ('ISA-PactoVerde','= PROMEDIO(D12:D15)',                             '100%'),
    ('ISA-Completo',  '= 0,70×ISA-EUDR + 0,30×ISA-PV',                  '100%'),
    ('',              '',                                                  ''),
    ('IP1',           '= D2',                                            '20%'),
    ('IP2',           '= √(D3 × D4)',                                    '20%'),
    ('IP3',           '= (D5 + D6 + D8) / 3',                            '20%'),
    ('IP4',           '= (D6.23 + D2.9) / 2',                            '20%'),
    ('IP5',           '= (D7 + D9 + Cert) / 3 · Cert = conteo 0/33/66/100', '20%'),
    ('IP (total)',    '= PROMEDIO(IP1:IP5)',                              '100%'),
    ('',              '',                                                  ''),
    ('IV1',           '= presión EU × ISA-PV (Bloque P)',                 '20%'),
    ('IV2',           '= D1 (clasificación, base 50 si pendiente)',       '20%'),
    ('IV3',           '= ha>0? → 65 : 35 (fragilidad territorial)',      '20%'),
    ('IV4',           '= cert=0? → 70 : 30 (brecha tecnológica)',         '20%'),
    ('IV5',           '= tipo Asoc? → 65 : 40 (riesgo social)',           '20%'),
    ('IV (total)',    '= PROMEDIO(IV1:IV5)',                             '100%'),
    ('',              '',                                                  ''),
    ('RE',            '= IV × (1 − IP/100)',                               '—'),
    ('Cuadrante 2×2', 'IP≥50 vs <50  ×  IV≥50 vs <50',                 'Corte=50'),
]

for rd in datos_pond:
    if rd[0] in ['ISA-EUDR', 'ISA-PactoVerde', 'ISA-Completo']:
        add_row(t_pond, rd, bg='D9D9D9', bold=True, fs=9)
    elif rd[0] in ['IP (total)', 'IV (total)', 'RE', 'Cuadrante 2×2']:
        add_row(t_pond, rd, bg='E8E8E8', bold=True, fs=9)
    elif rd[0] == '':
        add_row(t_pond, rd, fs=9)
    else:
        add_row(t_pond, rd, fs=9)

body_para(doc, '', after=4)
body_para(doc, (
    'ISA-EUDR e ISA-PV usan pesos FIJOS (87,5%/12,5% y 70%/30%). '
    'IP e IV usan pesos IGUALES (20% por sub-dimensión). '
    'Los scores se recalculan automáticamente al modificar cualquier '
    'valor en la hoja ISCAM_Score de la plantilla.'
), size=10, italic=True)

# ── REFERENCIAS ───────────────────────────────────────────
page_break(doc)
heading1(doc, 'REFERENCIAS')

refs = [
    'European Commission. (2023). Regulation (EU) 2023/1115 on the making available on the Union market and the export from the Union of certain commodities and products associated with deforestation and forest degradation. Official Journal of the European Union, L 150/206.',
    'European Commission. (2024). Directive (EU) 2024/1760 on corporate sustainability due diligence and on the amendment of Directive (EU) 2019/1937 and Regulation (EU) 2023/2859. Official Journal of the European Union.',
    'European Commission. (2019). The European Green Deal. COM(2019) 640 final. Brussels.',
    'European Commission. (2020). Farm to Fork Strategy. COM(2020) 381 final. Brussels.',
    'Ministerio de Economía y Finanzas. (2026). Ejecución presupuestal 2026. Sistema Integrado de Administración Financiera. Lima.',
    'Organismo de Evaluación y Fiscalización Ambiental. (2025). Registro de infracciones ambientales 2024. OEFA. Lima.',
    'Organismo Supervisor de las Contrataciones del Estado. (2025). Registro de proveedores sancionados. OSCE. Lima.',
    'PromPerú. (2024). CalCafé v2.1: Metodología de cálculo de huella de carbono para la cadena de valor del café. Lima.',
    'Sunat. (2025). Exportaciones de café y cacao 2024. Departamento de Estadísticas. Lima.',
]
for ref in refs:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf = p.paragraph_format
    pf.space_before = Pt(0); pf.space_after = Pt(4)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.5
    pf.first_line_indent = Cm(-1.25)
    pf.left_indent = Cm(1.25)
    run = p.add_run(ref)
    run.font.name = 'Times New Roman'; run.font.size = Pt(11)
    run.font.color.rgb = NEGRO

doc.save(OUT)
print(f'Guardado: {OUT}')
