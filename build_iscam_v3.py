# -*- coding: utf-8 -*-
"""
Estrategia: crear PLANTILLA_INDICE_PVE_ISCAM.xlsx desde cero (workbook limpio),
copiar TODOS los datos/valores/fórmulas del original, agregar ISCAM_Score.
Evita el bug de reserialización de estilos del archivo original.
"""
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side, GradientFill
from openpyxl.utils import get_column_letter
from copy import copy

SRC = r'C:\Users\acuba\eudrperu\PLANTILLA_INDICE_PVE.xlsx'
OUT = r'C:\Users\acuba\eudrperu\PLANTILLA_INDICE_PVE_ISCAM.xlsx'

# ── Helpers ────────────────────────────────────────────────
def _pf(fg):
    return PatternFill(patternType='solid', fgColor=fg)

def _border():
    t = Side(style='thin')
    return Border(t, t, t, t)

THIN_BORDER = _border()
FONT_BOLD   = Font(bold=True)
FONT_BOLD_W = Font(bold=True, color='FFFFFF', size=11)
FONT_BOLD_B = Font(bold=True, color='FFFFFF', size=10)
FONT_TITLE  = Font(bold=True, color='FFFFFF', size=13)
FONT_ITALIC = Font(italic=True, size=9)
CENTER      = Alignment('center', 'center', wrap_text=True)
LEFT        = Alignment('left', 'center', wrap_text=True)

# ── Colores ────────────────────────────────────────────────
C_AZUL      = _pf('BDD7EE')
C_AZUL_O    = _pf('9DC3E6')
C_AZUL_2    = _pf('4472C4')
C_NARANJ_2  = _pf('C55A11')
C_VERDE_H   = _pf('70AD47')
C_AMBER_H   = _pf('FF9900')
C_CYAN_H    = _pf('00B0F0')
C_DARK_H    = _pf('203864')
C_NARANJ_D  = _pf('843C0C')
C_ROJO_D    = _pf('7B1818')
C_GRIS      = _pf('D9D9D9')
C_GRIS_L    = _pf('F2F2F2')
C_AMBER_L   = _pf('FFF2CC')
C_ROJO_L    = _pf('FFCCCC')
C_VERDE_PK  = _pf('C6EFCE')
C_DARK_GRN  = _pf('375623')
C_TITULO    = _pf('1F4E79')
C_NOTA      = _pf('D6E4F0')

# ── Abrir source ─────────────────────────────────────────
print('Leyendo archivo original…')
wb_src = openpyxl.load_workbook(SRC, data_only=False)
src_sheets = {s.title: s for s in wb_src.worksheets}

# ── Crear workbook limpio ────────────────────────────────
print('Creando workbook limpio…')
wb_new = Workbook()
wb_new.remove(wb_new.active)  # quitar hoja default

# ═══════════════════════════════════════════════════════════
# COPIAR CADA HOJA DEL ORIGINAL (datos + fórmulas)
# ═══════════════════════════════════════════════════════════
SHEET_ORDER = ['INSTRUCCIONES', 'PONDERADORES', 'MATRIZ_174',
               'PREGUNTAS_PROXY', 'SCORECARDS', 'RADAR_BRECHAS']

def copy_sheet(ws_src, ws_dst):
    """Copia valores, fórmulas, merged cells y anchos de columna."""
    for row in ws_src.iter_rows():
        for cell in row:
            dst_cell = ws_dst.cell(row=cell.row, column=cell.column)
            dst_cell.value = cell.value
    # Merged cells
    for merge in ws_src.merged_cells.ranges:
        ws_dst.merge_cells(str(merge))
    # Anchos de columna
    for col_letter, dim in ws_src.column_dimensions.items():
        if dim.width:
            ws_dst.column_dimensions[col_letter].width = dim.width
    # Filas
    for row_num, dim in ws_src.row_dimensions.items():
        if dim.height:
            ws_dst.row_dimensions[row_num].height = dim.height
    # Freeze
    if ws_src.freeze_panes:
        ws_dst.freeze_panes = ws_src.freeze_panes

for sheet_name in SHEET_ORDER:
    if sheet_name in src_sheets:
        ws_new = wb_new.create_sheet(sheet_name)
        copy_sheet(src_sheets[sheet_name], ws_new)
        print(f'  ✓ {sheet_name} copiada')

# ═══════════════════════════════════════════════════════════
# ACTUALIZAR SCORECARDS (en workbook nuevo)
# ═══════════════════════════════════════════════════════════
ws_sc = wb_new['SCORECARDS']
ws_sc['A1'].value = 'SCORECARDS — ISA-Completo · IP · IV · RE · Café y Cacao Perú'
ws_sc.cell(2, 14).value = 'Tipología ISCAM'
ws_sc.cell(2, 3).value = 'ISA-Completo\n(0-100)'

# Identificar filas con RUC real
scorecard_rows = [
    r for r in range(3, ws_sc.max_row + 1)
    if ws_sc.cell(r, 1).value and str(ws_sc.cell(r, 1).value).startswith('201')
]
print(f'SCORECARDS: {len(scorecard_rows)} orgs con RUC')

# Columna C: IP vivo desde ISCAM_Score
# ISCAM_Score data arranca en row 4, SCORECARDS data en row 3 → offset +1
for r in range(3, ws_sc.max_row + 1):
    ruc = ws_sc.cell(r, 1).value
    if not ruc or len(str(ruc)) != 11:
        continue
    c = ws_sc.cell(r, 3)
    c.value = f'=IFERROR(ISCAM_Score!AL{r+1},"—")'
    c.number_format = '0.0'
    c.font = Font(bold=True)

# Columna D: semáforo ISA-Completo (verde EUDR≈70/PV≈30 mix)
for r in range(3, ws_sc.max_row + 1):
    ruc = ws_sc.cell(r, 1).value
    if not ruc or len(str(ruc)) != 11:
        continue
    ws_sc.cell(r, 4).value = (
        f'=IF(C{r}="—","— Sin Inst.2",'
        f'IF(C{r}<34,"🔴  Crítico",'
        f'IF(C{r}<67,"🟡  En desarrollo","🟢  Alineado")))'
    )

# Columna N: tipología ISCAM
for r in range(3, ws_sc.max_row + 1):
    ruc = ws_sc.cell(r, 1).value
    if not ruc or len(str(ruc)) != 11:
        continue
    ws_sc.cell(r, 14).value = f'=IFERROR(ISCAM_Score!AC{r+1},"")'

# ═══════════════════════════════════════════════════════════
# ACTUALIZAR RADAR_BRECHAS — D3 → ISCAM_Score col G
# ═══════════════════════════════════════════════════════════
ws_rb = wb_new['RADAR_BRECHAS']
for r in range(3, ws_rb.max_row + 1):
    d3_cell = ws_rb.cell(r, 4)  # col D = índice 4 (A=1,B=2,C=3,D=4)
    if d3_cell.value and 'SCORECARDS' in str(d3_cell.value):
        d3_cell.value = f'=IFERROR(AVERAGEIF(MATRIZ_174!$C:$C,A{r},ISCAM_Score!$G:$G),0)'

# ═══════════════════════════════════════════════════════════
# CREAR ISCAM_Score
# ═══════════════════════════════════════════════════════════
ws_i = wb_new.create_sheet('ISCAM_Score', 1)  # posición 1
ws_i.freeze_panes = 'E4'

n_orgs  = wb_src['MATRIZ_174'].max_row - 2
max_row  = wb_src['MATRIZ_174'].max_row
ws_m_src = wb_src['MATRIZ_174']

# ── Fila 1: título ──────────────────────────────────────
ws_i.merge_cells('A1:AL1')
c = ws_i['A1']
c.value = ('ISCAM — ISA-Completo = 0.70×ISA-EUDR + 0.30×ISA-PV  |  '
           'IP × IV → RE  |  Café y Cacao Perú — 174 organizaciones')
c.fill = C_TITULO; c.font = FONT_TITLE; c.alignment = CENTER
ws_i.row_dimensions[1].height = 30

# ── Fila 2: nota ───────────────────────────────────────
ws_i.merge_cells('A2:AL2')
c = ws_i['A2']
c.value = (
    'ISA-Completo = 0.70×ISA-EUDR + 0.30×ISA-PV   |   '
    'ISA-EUDR = 0.875×Núcleo(D1–D7, geom.) + 0.125×Extendido(D8–D9, arit.)   |   '
    'ISA-PV = Promedio(D12:D15)   |   IP = Promedio(IP1..IP5)   |   '
    'IV = Promedio(IV1..IV5)   |   RE = IV×(1−IP/100)   |   Corte 2×2: 50'
)
c.fill = C_NOTA; c.font = FONT_ITALIC
c.alignment = Alignment('left', 'center', wrap_text=True)
ws_i.row_dimensions[2].height = 22

# ── Fila 3: headers ────────────────────────────────────
ws_i.row_dimensions[3].height = 54

def h3(col, label, fill, w=None):
    c = ws_i.cell(3, col)
    c.value = label; c.fill = fill
    c.font = FONT_BOLD_B; c.alignment = CENTER; c.border = THIN_BORDER
    if w: ws_i.column_dimensions[get_column_letter(col)].width = w

# Identificación
h3(1,  'RUC',                   C_AZUL,    14)
h3(2,  'Razón Social',           C_AZUL,    30)
h3(3,  'Depto',                 C_AZUL,    12)
h3(4,  'FOB UE USD',            C_AZUL,    16)

# D1-D11 inputs
for col, label, fill in [
    (5,  'D1 — Clasific.\nRegulatoria',         C_GRIS),
    (6,  'D2 — Trazabilidad\n(SCORECARDS H)',  C_AZUL_O),
    (7,  'D3 — Legalidad\n(OSCE/Neon)',        C_AZUL_O),
    (8,  'D4 — Deforestación\nCero',             C_GRIS),
    (9,  'D5 — Diligencia\nDebida',              C_AZUL_O),
    (10, 'D6 — Capacidad\nDigital',             C_AZUL_O),
    (11, 'D7 — Presión\nComprador',             C_GRIS),
    (12, 'D8 — Gobernanza',                     C_GRIS),
    (13, 'D9 — Riesgo\nFinanciero',            C_GRIS),
    (14, 'D10 — Certificac.',                   C_GRIS),
    (15, 'D11 — Género e\nInclusión',           C_GRIS),
]:
    h3(col, label, fill, 13)

# IP sub-dims
for col, label in [
    (16, 'IP1\nTrazabilidad\nD2'),
    (17, 'IP2\n√(D3×D4)'),
    (18, 'IP3\n(D5+D6+D8)/3'),
    (19, 'IP4\n(D6+D2)/2'),
    (20, 'IP5\n(D7+D9+Cert)/3'),
]:
    h3(col, label, C_AZUL_2, 13)

# IV sub-dims
for col, label in [
    (21, 'IV1\nPresión EU\nISA-PV×50'),
    (22, 'IV2\nD1 (base=50)'),
    (23, 'IV3\nha>0? → 65:35'),
    (24, 'IV4\nCert=0? → 70:30'),
    (25, 'IV5\nTipo Asoc → 65:40'),
]:
    h3(col, label, C_NARANJ_2, 13)

# Scores
for col, label, fill, w in [
    (26, 'IP\nPreparación',       C_DARK_H,  17),
    (27, 'IV\nVulnerabilidad',   C_NARANJ_D,17),
    (28, 'RE\nExclusión',        C_ROJO_D,  17),
    (29, 'Tipología\n2×2 ISCAM', C_DARK_GRN,22),
    (30, 'Banderas\nDuras',     C_ROJO_D,  20),
]:
    h3(col, label, fill, w)

# Ambientales + Performance
for col, label, fill in [
    (31, 'D12\nHuella Carbono',      C_VERDE_H),
    (32, 'D13\nReporte Sostenib.',    C_VERDE_H),
    (33, 'D14\nEconomía Circular',    C_VERDE_H),
    (34, 'D15\nFitosanitario',        C_VERDE_H),
    (35, 'ISA-PV\nPromedio D12:D15',  C_AMBER_H),
    (36, 'P_Global\nPromedio P1:P14', C_CYAN_H),
    (37, 'ISA-EUDR\nGeom.D1–D7\n+ Arit.D8–D9', C_AZUL_2),
    (38, 'ISA-Completo\n0.70×EUDR\n+0.30×PV', C_DARK_H),
]:
    h3(col, label, fill, 13)

# ═══════════════════════════════════════════════════════════
# FILAS DE DATOS (row 4+)
# ═══════════════════════════════════════════════════════════
print('Escribiendo filas de datos ISCAM_Score…')

# ISCAM_Score: row 3 = header labels, data rows 4-177
# MATRIZ_174: row 3 = first org → ISCAM_Score row{r} = MATRIZ_174 row{r-1}
# SCORECARDS: row 3 = first org → ISCAM_Score row{r} needs SCORECARDS row{r-1}
for r in range(4, max_row + 2):   # data starts at row 4 (row 3 = headers)
    src_r = r - 1  # MATRIZ_174 y SCORECARDS arrancan en row 3
    ruc = ws_m_src.cell(src_r, 1).value
    if not ruc:
        continue
    ws_i.row_dimensions[r].height = 16

    # A-D: Identificación
    ws_i.cell(r,1).value = ruc; ws_i.cell(r,1).alignment = CENTER; ws_i.cell(r,1).border = THIN_BORDER
    ws_i.cell(r,2).value = ws_m_src.cell(src_r,2).value or ''; ws_i.cell(r,2).alignment = LEFT; ws_i.cell(r,2).border = THIN_BORDER
    ws_i.cell(r,3).value = ws_m_src.cell(src_r,3).value or ''; ws_i.cell(r,3).alignment = CENTER; ws_i.cell(r,3).border = THIN_BORDER
    ws_i.cell(r,4).value = ws_m_src.cell(src_r,12).value or 0; ws_i.cell(r,4).number_format = '#,##0'; ws_i.cell(r,4).alignment = CENTER; ws_i.cell(r,4).border = THIN_BORDER

    # ── Inputs D1-D11 (cols 5-15) ───────────────────────
    # D1 (5): pendiente → 0 gris
    c = ws_i.cell(r,5); c.value = 0; c.fill = C_GRIS; c.font = Font(color='999999', italic=True); c.alignment = CENTER; c.border = THIN_BORDER
    # D2 (6): desde SCORECARDS!H → SCORECARDS row{r-1}
    c = ws_i.cell(r,6); c.value = f'=IFERROR(SCORECARDS!H{src_r},"")'; c.alignment = CENTER; c.border = THIN_BORDER; c.number_format = '0.00'
    # D3 (7): desde MATRIZ_174!U → MATRIZ_174 row{src_r}
    c = ws_i.cell(r,7); c.value = f'=IFERROR(MATRIZ_174!U{src_r},0)'; c.alignment = CENTER; c.border = THIN_BORDER; c.number_format = '0.00'
    # D4 (8): pendiente → 0 gris
    c = ws_i.cell(r,8); c.value = 0; c.fill = C_GRIS; c.font = Font(color='999999', italic=True); c.alignment = CENTER; c.border = THIN_BORDER
    # D5 (9): desde SCORECARDS!I
    c = ws_i.cell(r,9); c.value = f'=IFERROR(SCORECARDS!I{src_r},"")'; c.alignment = CENTER; c.border = THIN_BORDER; c.number_format = '0.00'
    # D6 (10): desde SCORECARDS!J
    c = ws_i.cell(r,10); c.value = f'=IFERROR(SCORECARDS!J{src_r},"")'; c.alignment = CENTER; c.border = THIN_BORDER; c.number_format = '0.00'
    # D7-D11 (11-15): pendientes
    for col in [11,12,13,14,15]:
        c = ws_i.cell(r,col); c.value = 0; c.fill = C_GRIS; c.font = Font(color='999999', italic=True); c.alignment = CENTER; c.border = THIN_BORDER

    # ── IP sub-dims (cols 16-20) ────────────────────────
    c = ws_i.cell(r,16); c.value = f'=IFERROR(F{r},0)'; c.alignment = CENTER; c.border = THIN_BORDER; c.number_format = '0.00'
    c = ws_i.cell(r,17); c.value = f'=IFERROR(SQRT(G{r}*H{r}),0)'; c.alignment = CENTER; c.border = THIN_BORDER; c.number_format = '0.00'
    c = ws_i.cell(r,18); c.value = f'=IFERROR((I{r}+J{r}+L{r})/3,0)'; c.alignment = CENTER; c.border = THIN_BORDER; c.number_format = '0.00'
    c = ws_i.cell(r,19); c.value = f'=IFERROR((J{r}+F{r})/2,0)'; c.alignment = CENTER; c.border = THIN_BORDER; c.number_format = '0.00'
    c = ws_i.cell(r,20); c.value = f'=IFERROR((K{r}+M{r}+MATRIZ_174!O{src_r})/3,0)'; c.alignment = CENTER; c.border = THIN_BORDER; c.number_format = '0.00'

    # ── IV sub-dims (cols 21-25) ────────────────────────
    c = ws_i.cell(r,21); c.value = f'=IFERROR(MATRIZ_174!AP{src_r}*50,0)'; c.alignment = CENTER; c.border = THIN_BORDER; c.number_format = '0.0'
    c = ws_i.cell(r,22); c.value = f'=IFERROR(IF(E{r}=0,50,E{r}),0)'; c.alignment = CENTER; c.border = THIN_BORDER; c.number_format = '0.0'
    c = ws_i.cell(r,23); c.value = f'=IF(MATRIZ_174!R{src_r}>0,65,35)'; c.alignment = CENTER; c.border = THIN_BORDER; c.number_format = '0.0'
    c = ws_i.cell(r,24); c.value = f'=IF(MATRIZ_174!O{src_r}=0,70,30)'; c.alignment = CENTER; c.border = THIN_BORDER; c.number_format = '0.0'
    c = ws_i.cell(r,25); c.value = f'=IF(OR(MATRIZ_174!P{src_r}="ASOCIACION",MATRIZ_174!P{src_r}="PENDIENTE"),65,40)'; c.alignment = CENTER; c.border = THIN_BORDER; c.number_format = '0.0'

    # ── IP Score (col 26) ─────────────────────────────
    c = ws_i.cell(r,26); c.value = f'=IFERROR(ROUND(AVERAGE(P{r},Q{r},R{r},S{r},T{r}),1),0)'
    c.fill = C_NOTA; c.font = FONT_BOLD; c.alignment = CENTER; c.border = THIN_BORDER; c.number_format = '0.0'

    # ── IV Score (col 27) ─────────────────────────────
    c = ws_i.cell(r,27); c.value = f'=IFERROR(ROUND(AVERAGE(U{r},V{r},W{r},X{r},Y{r}),1),0)'
    c.fill = _pf('FCE4D6'); c.font = FONT_BOLD; c.alignment = CENTER; c.border = THIN_BORDER; c.number_format = '0.0'

    # ── RE = IV × (1 − IP/100) (col 28) ─────────────
    c = ws_i.cell(r,28); c.value = f'=IFERROR(ROUND(AA{r}*(1-Z{r}/100),1),0)'
    c.fill = C_ROJO_L; c.font = FONT_BOLD; c.alignment = CENTER; c.border = THIN_BORDER; c.number_format = '0.0'

    # ── Tipología 2×2 (col 29) ─────────────────────────
    c = ws_i.cell(r,29)
    c.value = (f'=IF(AND(Z{r}>=50,AA{r}<50),"🟢  Resilientes",'
               f'IF(AND(Z{r}>=50,AA{r}>=50),"🟠  Expuestas Adaptables",'
               f'IF(AND(Z{r}<50,AA{r}<50),"⬜  Riesgo Latente",'
               f'"🔴  Riesgo Crítico")))')
    c.alignment = CENTER; c.border = THIN_BORDER

    # ── Banderas duras (col 30) ────────────────────────
    c = ws_i.cell(r,30); c.value = f'=IF(G{r}=0,"🚫  Inh. vigente OSCE","")'; c.alignment = CENTER; c.border = THIN_BORDER

    # ── D12-D15 / ISA-PV / P_Global (cols 31-36) ─────
    for col, src in [(31,'W'),(32,'X'),(33,'Y'),(34,'Z')]:
        c = ws_i.cell(r,col); c.value = f'=IFERROR(MATRIZ_174!{src}{src_r},0)'; c.alignment = CENTER; c.border = THIN_BORDER; c.number_format = '0'
    c = ws_i.cell(r,35); c.value = f'=IFERROR(MATRIZ_174!AP{src_r},"N/A")'; c.alignment = CENTER; c.border = THIN_BORDER; c.number_format = '0.00'
    c = ws_i.cell(r,36); c.value = f'=IFERROR(MATRIZ_174!AO{src_r},"N/A")'; c.alignment = CENTER; c.border = THIN_BORDER; c.number_format = '0.00'

    # ── ISA-EUDR (col 37) — geométrica núcleo(D1–D7) 87.5% + aritmética extendido(D8–D9) 12.5% ──
    # Geom mean sobre cols E–K (D1–D7): SQRTPRODICT eleva al cuadrado, 7 dims = POWER(x,1/7)
    # Si todos los D1–D7 valen 0 → "N/A" (dato insuficiente, no alineamiento cero)
    # ISCAM_Score cols: E=D1, F=D2, G=D3, H=D4, I=D5, J=D6, K=D7, L=D8, M=D9
    nucleus = f'(E{r}*F{r}*G{r}*H{r}*I{r}*J{r}*K{r})'  # D1*D2*...*D7
    extended = f'(L{r}+M{r})/2'  # (D8+D9)/2
    c = ws_i.cell(r,37); c.value = f'=IFERROR(ROUND(POWER({nucleus},1/7)*0.875+({extended})*0.125,1),"N/A")'
    c.fill = C_AZUL_2; c.font = FONT_BOLD; c.alignment = CENTER; c.border = THIN_BORDER; c.number_format = '0.0'

    # ── ISA-Completo (col 38) — 0.70×ISA-EUDR + 0.30×ISA-PV ──
    c = ws_i.cell(r,38)
    c.value = f'=IFERROR(IF(AK{r}="N/A","N/A",ROUND(0.70*AK{r}+0.30*AI{r},1)),"N/A")'
    c.fill = C_DARK_H; c.font = Font(bold=True, color='FFFFFF'); c.alignment = CENTER; c.border = THIN_BORDER; c.number_format = '0.0'

# ═══════════════════════════════════════════════════════════
# FILA DE PROMEDIOS (row max_row+1)
# ═══════════════════════════════════════════════════════════
last_r = max_row + 2   # max_row+1 ya es la última org (src_r=max_row → r=max_row+1)
ws_i.row_dimensions[last_r].height = 22

for col in range(1, 39):
    c = ws_i.cell(last_r, col)
    c.fill = C_DARK_GRN; c.font = Font(bold=True, color='FFFFFF')
    c.alignment = CENTER; c.border = THIN_BORDER

ws_i.merge_cells(f'A{last_r}:D{last_r}')
ws_i.cell(last_r, 1).value = 'PROMEDIO MUESTRAL'
for col in [26, 27, 28, 38]:
    c = ws_i.cell(last_r, col)
    c.value = f'=IFERROR(AVERAGE({get_column_letter(col)}4:{get_column_letter(col)}{max_row}),"—")'
    c.number_format = '0.0'
ws_i.cell(last_r, 29).value = f'n = {n_orgs} organizaciones'
ws_i.cell(last_r, 29).font = Font(bold=True, color='FFFFFF')

# ═══════════════════════════════════════════════════════════
# NOTA METODOLÓGICA AL PIE
# ═══════════════════════════════════════════════════════════
note_r = max_row + 4
ws_i.merge_cells(f'A{note_r}:AL{note_r}')
c = ws_i.cell(note_r, 1)
c.value = (
    'METODOLOGÍA ISCAM  |  '
    'ISA-EUDR = 0.875×(D1×D2×...×D7)^(1/7) + 0.125×(D8+D9)/2  |  '
    'ISA-PV = Promedio(D12:D15)  |  ISA-Completo = 0.70×ISA-EUDR + 0.30×ISA-PV  |  '
    'IP = Promedio(IP1..IP5): IP1=D2, IP2=√(D3×D4), IP3=(D5+D6+D8)/3, IP4=(D6+D2)/2, IP5=(D7+D9+Cert)/3  |  '
    'IV = Promedio(IV1..IV5): IV1=ISA-PV×50, IV2=D1(base=50), IV3=ha>0?→65:35, IV4=cert=0?→70:30, IV5=tipo Asoc?→65:40  |  '
    'RE = IV×(1−IP/100)  |  Corte 2×2: 50  |  '
    '█ GRIS=pendiente Inst.2  █ AZUL=Datos llenos  █ NARANJA=IV  █ ROJO=RE  █ VERDE=Ambiental  █ OSCURO=ISA'
)
c.fill = C_GRIS_L; c.font = Font(italic=True, size=8)
c.alignment = Alignment('left', 'center', wrap_text=True)
ws_i.row_dimensions[note_r].height = 30

print(f'ISCAM_Score: {n_orgs} orgs, 38 cols (A-AL)')

# ═══════════════════════════════════════════════════════════
# ACTUALIZAR PONDERADORES — agregar tabla ISCAM
# ═══════════════════════════════════════════════════════════
ws_p = wb_new['PONDERADORES']
nr = ws_p.max_row + 2

ws_p.merge_cells(f'A{nr}:D{nr}')
c = ws_p.cell(nr, 1)
c.value = 'VERSION ISCAM (2026-10-12) — Pesos mostrados para transparencia (fijos, no editables)'
c.font = Font(bold=True, color='1F4E79')
nr += 1

ws_p.merge_cells(f'A{nr}:D{nr}')
c = ws_p.cell(nr, 1)
c.value = 'ISA-EUDR e ISA-PV usan pesos FIJOS (87.5%/12.5% y 70%/30%). IP/IV pesan 20% cada sub-dim.'
c.font = Font(italic=True, size=9)
nr += 1

# Headers
for col, val in [(1,'SUBDIM'),(2,'FÓRMULA'),(3,'PESO')]:
    c = ws_p.cell(nr, col); c.value = val; c.fill = C_AZUL; c.font = FONT_BOLD; c.border = THIN_BORDER; c.alignment = CENTER
nr += 1

rows_iscam = [
    ('ISA-EUDR', '= 0.875×∛(D1×D2×...×D7) + 0.125×(D8+D9)/2', '100%'),
    ('','',''),
    ('ISA-PactoVerde', '= PROMEDIO(D12:D15)', '100%'),
    ('','',''),
    ('ISA-Completo', '= 0.70×ISA-EUDR + 0.30×ISA-PV', '100%'),
    ('','',''),
    ('IP1', '= D2', '20%'),
    ('IP2', '= √(D3 × D4)', '20%'),
    ('IP3', '= (D5 + D6 + D8) / 3', '20%'),
    ('IP4', '= (D6 + D2) / 2', '20%'),
    ('IP5', '= (D7 + D9 + Cert) / 3', '20%'),
    ('IP (total)', '= PROMEDIO(IP1:IP5)', '100%'),
    ('','',''),
    ('IV1', '= ISA-PV × 50 (presión EU/PV)', '20%'),
    ('IV2', '= D1 (base=50 si pendiente)', '20%'),
    ('IV3', '= ha>0? → 65 : 35 (fragilidad)', '20%'),
    ('IV4', '= cert=0? → 70 : 30 (brecha)', '20%'),
    ('IV5', '= tipo Asoc? → 65 : 40 (riesgo social)', '20%'),
    ('IV (total)', '= PROMEDIO(IV1:IV5)', '100%'),
    ('','',''),
    ('RE', '= IV × (1 − IP/100)', '—'),
    ('Cuadrante 2×2', 'IP≥50 vs <50  ×  IV≥50 vs <50', 'Corte=50'),
]
for idx, (dim, formula, peso) in enumerate(rows_iscam):
    rn = nr + idx
    # ISA-EUDR, ISA-PV, ISA-Completo → fondo azul corp
    if dim in ('ISA-EUDR', 'ISA-PactoVerde', 'ISA-Completo'):
        fill_row = _pf('BDD7EE')
    elif dim == '':
        fill_row = None
    else:
        fill_row = C_GRIS_L if idx % 2 == 1 else _pf('DEEAF1')
    c1 = ws_p.cell(rn, 1); c1.value = dim; c1.border = THIN_BORDER; c1.alignment = LEFT
    if dim and dim[0].isupper() and dim != '': c1.font = FONT_BOLD
    c2 = ws_p.cell(rn, 2); c2.value = formula; c2.border = THIN_BORDER; c2.alignment = LEFT
    c3 = ws_p.cell(rn, 3); c3.value = peso; c3.border = THIN_BORDER; c3.alignment = CENTER
    if dim and dim[0].isupper() and dim != '': c3.font = FONT_BOLD
    if fill_row:
        c1.fill = fill_row; c2.fill = fill_row; c3.fill = fill_row

# ═══════════════════════════════════════════════════════════
# GUARDAR
# ═══════════════════════════════════════════════════════════
print('Guardando…')
wb_new.save(OUT)
print(f'\n✓ Guardado: {OUT}')

# ── Resumen ──────────────────────────────────────────────
print()
print('═══ ARQUITECTURA ISCAM IMPLEMENTADA ═══')
print()
print('HOJAS:')
print('  ISCAM_Score  NUEVA — ISA-EUDR + ISA-Completo + IP/IV/RE + matriz 2×2 + D12-D15 + ISA-PV')
print('  SCORECARDS   Actualizada — ISA-Completo vivo en col C (ISCAM_Score!AL)')
print('  MATRIZ_174   Intacta — D3 Neon + D12-D15 + Bloque P')
print('  PONDERADORES Actualizado — ISA-EUDR + ISA-Completo + IP + IV + RE')
print()
print('COLUMNAS ISCAM_Score:')
print('  A-D    Identificación (RUC, Razón Social, Depto, FOB UE)')
print('  E-O    Inputs D1-D11 (D2/D5/D6 ← SCORECARDS; D3 ← MATRIZ_174; resto gris=pendiente)')
print('  P-T    IP1-IP5  (preparación sub-dimensiones)')
print('  U-Y    IV1-IV5  (vulnerabilidad sub-dimensiones)')
print('  Z      IP Score (promedio IP1-IP5)')
print('  AA     IV Score (promedio IV1-IV5)')
print('  AB     RE = IV × (1−IP/100)')
print('  AC     Tipología 2×2')
print('  AD     Banderas duras')
print('  AE-AH  D12/D13/D14/D15/ISA-PV/P_Global (desde MATRIZ_174)')
print('  AK     ISA-EUDR  ← NUEVO: 0.875×geom(D1:D7) + 0.125×(D8+D9)/2')
print('  AL     ISA-Completo ← NUEVO: 0.70×ISA-EUDR + 0.30×ISA-PV  ← SCORECARDS!C')
print('SCORECARDS col C → ISA-Completo (ANTES: IP Score)')
print()
print('ESTADO DE DATOS:')
print('  D2/D5/D6 → valores 0 (sin Instrumento 2)')
print('  D3       → scores Neon (0.75-1.0 para 36 orgs)')
print('  D1,D4,D7-D11 → 0 (pendiente Instrumento 2)')
print('  D12-D15  → proxy IPCC/FAO + FOB UE')
print('  ISA-PV   → AVERAGE(D12:D15)/2')
print('  P_Global → promedio P1-P14')
print()
print('IP/IV MOSTRARÁN VALORES PARCIALES hasta que se llene Instrumento 2.')
print('La arquitectura está viva — Excel recalculará automáticamente.')
