import openpyxl
from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os

# Load data
wb_matriz = openpyxl.load_workbook('MATRIZ_IP_IV_v18_EUDRPERU.xlsx')
ws_matriz = wb_matriz['MATRIZ']

wb_dua = openpyxl.load_workbook('reports/DUA_CONSOLIDADO_con_atributos_20261002 (2).xlsx', read_only=True)
ws_por_ruc = wb_dua['por RUC']
ws_detalle = wb_dua['DETALLE_ITEMS']
ws_duas = wb_dua['DUAS']

# Top exporters by total FOB
top_exporters = [
    ('20542209951', 'ASOCIACION VALLE GRANDE', 11327633.45),
    ('20602650643', 'ASOCIACION AGROEXPORTADORA DE LA REGION SAN MARTIN', 6552453.01),
    ('20479595276', 'COOPERATIVA AGRARIA CAFETALERA CASIL LTD', 4468578.96),
    ('20136201213', 'CENTRAL DE COOPERATIVAS AGRARIAS CAFETALERAS COCLA LTDA. N 281', 4249505.80),
    ('20600263286', 'ASOCIACION DE PRODUCTORES SELVA NORORIENTAL', 4154567.83),
    ('20140181405', 'COOPERATIVA AGRARIA CAFETALERA LA FLORIDA', 4117387.45),
    ('20542264544', 'COOPERATIVA AGRARIA VALLE DEL BIAVO LTDA', 1034237.62),
    ('20603820691', 'COOPERATIVA AGRARIA DE SERVICIOS MULTIPLES CORDILLERA AZUL', 896994.95),
    ('20606451122', 'ASOCIACION DE PRODUCTORES CERRO BLANCO', 864647.85),
    ('20602054480', 'COOPERATIVA ECOLOGICA DE MUJERES CAFETALERAS VILLA RICA', 813479.67),
]

# Aggregate DUA detail data by RUC
from collections import defaultdict

ruc_detail = defaultdict(lambda: {
    'items': [],
    'organico': 0, 'fairtrade': 0, 'rainforest': 0, 'utz': 0,
    'marca': 0, 'lote': 0, 'contrato': 0,
    'bolsa': 0, 'granel': 0, 'en_grano': 0,
    'washed': 0, 'natural': 0, 'honey': 0,
    'arabica': 0, 'robusta': 0,
    'destinos': set(),
    'subpartidas': set(),
    'duas': set(),
    'total_fob_items': 0,
    'total_kg': 0,
})

for row in ws_detalle.iter_rows(min_row=2, max_row=ws_detalle.max_row, values_only=True):
    ruc = row[0]
    if ruc in [e[0] for e in top_exporters]:
        attrs = row[8] or ''
        d = ruc_detail[ruc]
        d['items'].append({
            'desc': row[7],
            'attrs': attrs,
            'organico': row[9],
            'fairtrade': row[10],
            'rainforest': row[11],
            'utz': row[12],
        })
        if row[9]: d['organico'] += 1
        if row[10]: d['fairtrade'] += 1
        if row[11]: d['rainforest'] += 1
        if row[12]: d['utz'] += 1
        if attrs:
            if 'marca' in attrs: d['marca'] += 1
            if 'lote' in attrs: d['lote'] += 1
            if 'contrato' in attrs: d['contrato'] += 1
            if 'bolsa' in attrs: d['bolsa'] += 1
            if 'granel' in attrs: d['granel'] += 1
            if 'en_grano' in attrs: d['en_grano'] += 1
            if 'washed' in attrs: d['washed'] += 1
            if 'natural' in attrs: d['natural'] += 1
            if 'honey' in attrs: d['honey'] += 1
            if 'arabica' in attrs: d['arabica'] += 1
            if 'robusta' in attrs: d['robusta'] += 1

# Get DUAS data for destinations, weights, FOB
for row in ws_duas.iter_rows(min_row=2, max_row=ws_duas.max_row, values_only=True):
    ruc = row[0]
    if ruc in [e[0] for e in top_exporters]:
        d = ruc_detail[ruc]
        d['destinos'].add(row[6])  # pais_codigo
        d['duas'].add(row[3])
        if row[17]:  # valor_neto_fob
            d['total_fob_items'] += row[17]
        if row[18]:  # total_peso_neto
            d['total_kg'] += row[18]

# Get subpartidas from detalle
for row in ws_detalle.iter_rows(min_row=2, max_row=ws_detalle.max_row, values_only=True):
    ruc = row[0]
    if ruc in [e[0] for e in top_exporters]:
        # subpartida not in DETALLE_ITEMS, get from base dua
        pass

# Get subpartidas from base dua 25 detallada
ws_base = wb_dua['base dua 25 detallada']
for row in ws_base.iter_rows(min_row=2, max_row=ws_base.max_row, values_only=True):
    ruc = row[0]
    if ruc in [e[0] for e in top_exporters]:
        if row[17]:  # subpartida
            ruc_detail[ruc]['subpartidas'].add(row[17])

# Get MATRIZ data for each RUC
matriz_data = {}
for row in ws_matriz.iter_rows(min_row=7, max_row=ws_matriz.max_row, values_only=True):
    ruc = row[1]  # column B
    if ruc in [e[0] for e in top_exporters]:
        matriz_data[ruc] = {
            'nombre': row[2],
            'tipo_prod': row[3],
            'departamento': row[5],
            'provincia': row[6],
            'macro_zona': row[7],
            'producto_pac': row[8],
            'exporta_produce': row[9],
            'fob_2024_miles': row[11],
            'fob_usd_sunat': row[12],
            'n_ops': row[13],
            'n_paises': row[14],
            'n_socios': row[15],
            'n_trabaj': row[16],
            'cert_pac': row[20],
            'cert_presente': row[21],
            'anios_oper': row[19],
            'lat': row[46],
            'lon': row[47],
            'paises_destino': row[52],
            'anio_inicio_exp': row[53],
            'anio_fin_exp': row[54],
            'isa_proxy': row[55],
            'ip_proxy': row[56],
            'iv_proxy': row[57],
            'dua_items_total': row[58] if len(row) > 58 else None,
            'dua_organico': row[59] if len(row) > 59 else None,
            'dua_fairtrade': row[60] if len(row) > 60 else None,
            'dua_marca': row[69] if len(row) > 69 else None,
            'dua_lote': row[70] if len(row) > 70 else None,
            'dua_contrato': row[71] if len(row) > 71 else None,
            'dua_traz_score': row[82] if len(row) > 82 else None,
            'dua_cert_score': row[83] if len(row) > 83 else None,
        }

def add_run(para, text, bold=False, italic=False, color=None, size=None):
    run = para.add_run(text)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = color
    if size:
        run.font.size = Pt(size)
    return run

def set_cell_bg(cell, hex_color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)

def create_scorecard(ruc, name, total_fob):
    doc = Document()
    
    # Margins
    section = doc.sections[0]
    section.left_margin = Cm(1.5)
    section.right_margin = Cm(1.5)
    section.top_margin = Cm(1.5)
    section.bottom_margin = Cm(1.5)
    
    # Style
    style = doc.styles['Normal']
    style.font.name = 'Calibri'
    style.font.size = Pt(9)
    
    # Colors
    DARK_GREEN = RGBColor(0x1B, 0x5E, 0x20)
    MID_GREEN = RGBColor(0x2E, 0x7D, 0x32)
    ACCENT = RGBColor(0x0D, 0x47, 0xA1)
    RED = RGBColor(0xC6, 0x28, 0x28)
    ORANGE = RGBColor(0xEF, 0x6C, 0x00)
    GREEN = RGBColor(0x2E, 0x7D, 0x32)
    
    d = ruc_detail[ruc]
    m = matriz_data.get(ruc, {})
    total_items = len(d['items'])
    
    # ===== HEADER =====
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_run(p, 'SCORECARD EUDR — COOPERATIVA EXPORTADORA', bold=True, size=14, color=DARK_GREEN)
    
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_run(p, name, bold=True, size=12, color=MID_GREEN)
    
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_run(p, f'RUC: {ruc}  |  FOB 2024-2025: US$ {total_fob:,.0f}  |  Items DUA: {total_items}', size=9, color=RGBColor(0x66,0x66,0x66))
    
    # ===== KPI ROW =====
    table = doc.add_table(rows=2, cols=6)
    table.style = 'Table Grid'
    
    kpis = [
        ('EXPOSICIÓN EU', f"{len(d['destinos'])} países", 'EU' in d['destinos'] or 'DE' in d['destinos'] or 'FR' in d['destinos'] or 'ES' in d['destinos'] or 'IT' in d['destinos'] or 'BE' in d['destinos'] or 'NL' in d['destinos']),
        ('OPERACIONES', f"{len(d['duas'])} DUAs", True),
        ('VOLUMEN', f"{d['total_kg']:,.0f} kg", True),
        ('ITEMS DUA', f"{total_items} líneas", True),
        ('SUBPARTIDAS', f"{len(d['subpartidas'])} códigos", True),
        ('AÑOS EXPORT.', f"{m.get('anio_inicio_exp', '—')}–{m.get('anio_fin_exp', '2025')}", True),
    ]
    
    for i, (label, value, is_good) in enumerate(kpis):
        cell = table.rows[0].cells[i]
        cell.text = ''
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_run(p, label + '\n', bold=True, size=8, color=RGBColor(0x66,0x66,0x66))
        add_run(p, value, bold=True, size=11, color=GREEN if is_good else ACCENT)
        set_cell_bg(cell, 'E8F5E9' if is_good else 'E3F2FD')
        
        cell2 = table.rows[1].cells[i]
        cell2.text = ''
    
    # ===== EUDR READINESS MATRIX =====
    doc.add_paragraph()
    p = doc.add_paragraph()
    add_run(p, 'MATRIZ DE PREPARACIÓN EUDR (D1–D11)', bold=True, size=10, color=DARK_GREEN)
    
    # D1-D7 from ISCAM (field required), D8-D11 from admin data
    dims = [
        ('D1', 'Trazabilidad lotes', '🔴 Campo requerido', '0%', RED),
        ('D2', 'Registro productores', f"DUA: marca={d['marca']}, lote={d['lote']}, contrato={d['contrato']}", f"{int(m.get('dua_traz_score', 0)*100) if m.get('dua_traz_score') else 0}%", ORANGE if d['marca']+d['lote']+d['contrato'] > 0 else RED),
        ('D3', 'Monitoreo deforest.', '🔴 Campo requerido', '0%', RED),
        ('D4', 'Manejo ambiental', '🔴 Campo requerido', '0%', RED),
        ('D5', 'Condiciones laborales', '🔴 Campo requerido', '0%', RED),
        ('D6', 'No trabajo infantil', '🔴 Campo requerido', '0%', RED),
        ('D7', 'Seguridad ocupacional', '🔴 Campo requerido', '0%', RED),
        ('D8', 'Antigüedad/Socios', f"{m.get('anios_oper', '?')} años, {m.get('n_socios', '?')} socios", '—', MID_GREEN),
        ('D9', 'Capacidad export.', f"{m.get('n_ops', '?')} ops, {m.get('n_paises', '?')} países", '—', MID_GREEN),
        ('D10', 'Certificaciones', f"Org:{d['organico']} FT:{d['fairtrade']} RF:{d['rainforest']} UTZ:{d['utz']}", f"{int(m.get('dua_cert_score', 0)*100) if m.get('dua_cert_score') else 0}%", GREEN if d['organico']+d['fairtrade'] > 0 else ORANGE),
        ('D11', 'Volumen FOB', f"US$ {total_fob:,.0f}", '—', MID_GREEN),
    ]
    
    t2 = doc.add_table(rows=len(dims)+1, cols=4)
    t2.style = 'Table Grid'
    
    # Header
    headers = ['DIM', 'DIMENSIÓN', 'EVIDENCIA DUA / ADMIN', 'SCORE']
    for i, h in enumerate(headers):
        cell = t2.rows[0].cells[i]
        cell.text = ''
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_run(p, h, bold=True, size=8, color=RGBColor(0xFF,0xFF,0xFF))
        set_cell_bg(cell, '1B5E20')
    
    for idx, (dim, title, evidence, score, color) in enumerate(dims):
        row = t2.rows[idx+1]
        row.cells[0].text = dim
        row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_run(row.cells[0].paragraphs[0], dim, bold=True, size=8)
        
        row.cells[1].text = title
        add_run(row.cells[1].paragraphs[0], title, size=8)
        
        row.cells[2].text = evidence
        add_run(row.cells[2].paragraphs[0], evidence, size=7)
        
        row.cells[3].text = score
        p = row.cells[3].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_run(p, score, bold=True, size=9, color=color)
        
        # Alternate row color
        if idx % 2 == 0:
            for c in row.cells:
                set_cell_bg(c, 'F5F5F5')
    
    # ===== PACKAGING & QUALITY PROFILE =====
    doc.add_paragraph()
    p = doc.add_paragraph()
    add_run(p, 'PERFIL DE EMPAQUE Y CALIDAD FÍSICA (DUA)', bold=True, size=10, color=DARK_GREEN)
    
    if total_items > 0:
        pct_bolsa = round(d['bolsa']/total_items*100, 1)
        pct_granel = round(d['granel']/total_items*100, 1)
        pct_en_grano = round(d['en_grano']/total_items*100, 1)
        pct_washed = round(d['washed']/total_items*100, 1)
        pct_organico = round(d['organico']/total_items*100, 1)
        pct_fairtrade = round(d['fairtrade']/total_items*100, 1)
    else:
        pct_bolsa = pct_granel = pct_en_grano = pct_washed = pct_organico = pct_fairtrade = 0
    
    t3 = doc.add_table(rows=8, cols=2)
    t3.style = 'Table Grid'
    
    pack_data = [
        ('Empaque bolsa (sacos)', f"{d['bolsa']} items ({pct_bolsa}%)"),
        ('Empaque granel', f"{d['granel']} items ({pct_granel}%)"),
        ('Estado: en grano', f"{d['en_grano']} items ({pct_en_grano}%)"),
        ('Proceso: lavado (washed)', f"{d['washed']} items ({pct_washed}%)"),
        ('Proceso: natural/honey', f"{d['natural']+d['honey']} items"),
        ('Orgánico certificado', f"{d['organico']} items ({pct_organico}%)"),
        ('Fairtrade certificado', f"{d['fairtrade']} items ({pct_fairtrade}%)"),
        ('Trazabilidad: marca/lote/contrato', f"Marca: {d['marca']} | Lote: {d['lote']} | Contrato: {d['contrato']}"),
    ]
    
    for idx, (label, val) in enumerate(pack_data):
        row = t3.rows[idx]
        row.cells[0].text = label
        add_run(row.cells[0].paragraphs[0], label, bold=True, size=8)
        row.cells[1].text = val
        add_run(row.cells[1].paragraphs[0], val, size=8)
        if idx % 2 == 0:
            for c in row.cells:
                set_cell_bg(c, 'F5F5F5')
    
    # ===== DESTINOS & SUBPARTIDAS =====
    doc.add_paragraph()
    p = doc.add_paragraph()
    add_run(p, 'MERCADOS Y CLASIFICACIÓN ARANCELARIA', bold=True, size=10, color=DARK_GREEN)
    
    t4 = doc.add_table(rows=2, cols=2)
    t4.style = 'Table Grid'
    
    destinos_str = ', '.join(sorted(d['destinos'])) if d['destinos'] else '—'
    subpartidas_str = ', '.join(sorted(d['subpartidas'])) if d['subpartidas'] else '—'
    
    row = t4.rows[0]
    row.cells[0].text = 'Países destino'
    add_run(row.cells[0].paragraphs[0], 'Países destino', bold=True, size=8)
    row.cells[1].text = destinos_str
    add_run(row.cells[1].paragraphs[0], destinos_str, size=7)
    
    row = t4.rows[1]
    row.cells[0].text = 'Subpartidas (HS)'
    add_run(row.cells[0].paragraphs[0], 'Subpartidas (HS)', bold=True, size=8)
    row.cells[1].text = subpartidas_str
    add_run(row.cells[1].paragraphs[0], subpartidas_str, size=7)
    
    # ===== RISK FLAGS =====
    doc.add_paragraph()
    p = doc.add_paragraph()
    add_run(p, 'ALERTAS DE RIESGO EUDR', bold=True, size=10, color=RED)
    
    flags = []
    if 'EU' not in d['destinos'] and 'DE' not in d['destinos'] and 'FR' not in d['destinos'] and 'ES' not in d['destinos'] and 'IT' not in d['destinos'] and 'BE' not in d['destinos'] and 'NL' not in d['destinos']:
        flags.append('⚠ Sin destino UE confirmado en muestra DUA')
    if d['organico'] == 0 and d['fairtrade'] == 0 and d['rainforest'] == 0:
        flags.append('🔴 Sin certificaciones ambientales declaradas en DUA')
    if d['marca'] == 0 and d['lote'] == 0 and d['contrato'] == 0:
        flags.append('🔴 Sin identificadores de origen (marca/lote/contrato) en DUA')
    if total_items == 0:
        flags.append('🔴 Sin items DUA en muestra — visibilidad nula')
    if m.get('cert_presente') != 'SÍ':
        flags.append('⚠ Directorio PAC: sin certificación registrada')
    
    # Perú = standard risk
    flags.append('📌 Perú = riesgo estándar (Art. 4a no aplica); DDS completo obligatorio')
    
    for flag in flags:
        p = doc.add_paragraph(style='List Bullet')
        add_run(p, flag, size=8, color=RED if flag.startswith('🔴') else ORANGE if flag.startswith('⚠') else ACCENT)
    
    # ===== RECOMMENDATIONS =====
    doc.add_paragraph()
    p = doc.add_paragraph()
    add_run(p, 'ACCIONES PRIORITARIAS (≤90 días al 30-dic-2026)', bold=True, size=10, color=DARK_GREEN)
    
    recs = [
        'Implementar sistema DDS por lote con reference number EUDR',
        'Registrar marca/lote/contrato en 100% items DUA (hoy <30% cobertura)',
        'Obtener certificación Rainforest Alliance EUDR-opt-in o equivalente',
        'Georreferenciar parcelas de socios y vincular a lotes de exportación',
        'Validar legalidad ambiental (Anexo VII) vía MIDAGRI — no SENACE',
    ]
    
    for rec in recs:
        p = doc.add_paragraph(style='List Bullet')
        add_run(p, rec, size=8)
    
    # Save
    safe_name = name.replace('/', '_').replace(' ', '_').replace('.', '').replace('°', '')
    out_path = f'reports/scorecards/SCORECARD_{safe_name}_{ruc}.docx'
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    doc.save(out_path)
    print(f'  Generated: {out_path}')

# Generate all scorecards
for ruc, name, fob in top_exporters:
    create_scorecard(ruc, name, fob)

print('All scorecards generated!')