# -*- coding: utf-8 -*-
"""
Reconstruye PLANTILLA_INDICE_PVE.xlsx bajo arquitectura ISCAM completa.

Arquitectura:
  MATRIZ_174  → datos base + D3 Neon + D12-D15 + Bloque P
  SCORECARDS  → scores D2/D5/D6 (referencia MATRIZ_174 + formulas)
  ISCAM_Score → IP/IV/RE agregados + matriz 2×2

Fórmulas ISCAM:
  IP  = promedio(IP1..IP5)          [0-100, mayor = más preparado]
  IV  = promedio(IV1..IV5)          [0-100, mayor = más vulnerable]
  RE  = IV × (1 − IP/100)           [0-100, mayor = más excluido]
  Tipología 2×2: IP≥50 / IV<50 → Resilientes | IP≥50 / IV≥50 → Expuestas Adaptables
                  IP<50  / IV<50 → Riesgo Latente | IP<50 / IV≥50 → Riesgo Crítico

Fuentes de D-dimensiones:
  D2/D5/D6   → SCORECARDS cols H, I, J
  D3         → MATRIZ_174!U  (Neon)
  D4/D7/D8/D9/D10/D11 → 0 (pendiente Instrumento 2)
  Cert (D8)  → MATRIZ_174!O  (score certificaciones)
"""

import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter

SRC = r'C:\Users\acuba\eudrperu\PLANTILLA_INDICE_PVE.xlsx'
OUT = r'C:\Users\acuba\eudrperu\PLANTILLA_INDICE_PVE_ISCAM.xlsx'

# ── Estilos ────────────────────────────────────────────────
def _pf(fg):
    return PatternFill(patternType='solid', fgColor=fg)
AZUL      = _pf('BDD7EE')
AZUL_O    = _pf('9DC3E6')
AZUL_2    = _pf('4472C4')
NARANJ_2  = _pf('C55A11')
VERDE_H   = _pf('70AD47')
AMBER_H   = _pf('FF9900')
CYAN_H    = _pf('00B0F0')
DARK_H    = _pf('203864')
NARANJ_D  = _pf('843C0C')
ROJO_D    = _pf('7B1818')
GRIS      = _pf('D9D9D9')
GRIS_L    = _pf('F2F2F2')
AMBER_L   = _pf('FFF2CC')
ROJO_L    = _pf('FFCCCC')
VERDE_PK  = _pf('C6EFCE')
DARK_GRN  = _pf('375623')

BOLD      = Font(bold=True)
BOLD_B    = Font(bold=True, color='FFFFFF')
FONT_9    = Font(size=9)
FONT_9_I  = Font(size=9, italic=True)
FONT_12   = Font(bold=True, size=12, color='FFFFFF')
CENTER    = Alignment('center', 'center', wrap_text=True)
LEFT      = Alignment('left', 'center', wrap_text=True)
LEFT_W    = Alignment('left', 'center', wrap_text=False)
THIN      = Side('thin')
TB        = Border(THIN, THIN, THIN, THIN)

def hdr(ws, r, c, v, fill=AZUL, font=None, align=CENTER, w=None):
    cell = ws.cell(r, c)
    cell.value = v; cell.fill = fill
    cell.font = font or BOLD
    cell.alignment = align; cell.border = TB
    if w: ws.column_dimensions[get_column_letter(c)].width = w

def cfmt(ws, r, c, v, fill=None, font=None, align=CENTER, fmt=None):
    cell = ws.cell(r, c)
    cell.value = v
    if fill:  cell.fill  = fill
    if font:  cell.font  = font
    if fmt:   cell.number_format = fmt
    cell.alignment = align; cell.border = TB
    return cell

# ── Cargar workbook ────────────────────────────────────────
print('Cargando…')
wb  = openpyxl.load_workbook(SRC, data_only=False)
ws_m = wb['MATRIZ_174']
ws_s = wb['SCORECARDS']

max_row = ws_m.max_row
n_orgs  = max_row - 2
print(f'Org: {n_orgs}')

# ═══════════════════════════════════════════════════════════
# CREAR ISCAM_Score
# ═══════════════════════════════════════════════════════════
if 'ISCAM_Score' in wb.sheetnames:
    del wb['ISCAM_Score']
# Insertar como hoja 1 (tras INSTRUCCIONES si existe, si no posición 1)
ws_i = wb.create_sheet('ISCAM_Score', 1)
ws_i.freeze_panes = 'E4'

# ── Fila 1: título ──────────────────────────────────────
ws_i.merge_cells('A1:AH1')
c = ws_i['A1']
c.value = ('ISCAM — Índice de Preparación (IP) × Índice de Vulnerabilidad (IV) × '
           'Riesgo de Exclusión (RE)  |  Café y Cacao Perú — 174 organizaciones')
c.fill = _pf('1F4E79')
c.font = FONT_12; c.alignment = CENTER
ws_i.row_dimensions[1].height = 28

# ── Fila 2: nota metodológica ──────────────────────────
ws_i.merge_cells('A2:AH2')
c = ws_i['A2']
c.value = (
    'IP = Promedio(IP1..IP5)   IV = Promedio(IV1..IV5)   '
    'RE = IV × (1 − IP/100)   |   Corte alto/bajo: 50 (mediana muestral proxy)   |   '
    'D2/D5/D6 → SCORECARDS  |  D3 → Neon/MATRIZ_174  |  D1,D4,D7-D11 → Pendiente Instrumento 2'
)
c.fill = _pf('D6E4F0')
c.font = FONT_9_I; c.alignment = Alignment('left', 'center', wrap_text=True)
ws_i.row_dimensions[2].height = 22

# ── Fila 3: headers (UNA SOLA FILA — datos en row 4+) ──
ws_i.row_dimensions[3].height = 52

def h3(ws, col, label, fill, w=None):
    """Header compacto en fila 3, UNA sola fila."""
    c = ws.cell(3, col)
    c.value = label; c.fill = fill
    c.font = Font(bold=True, color='FFFFFF', size=9)
    c.alignment = Alignment('center', 'center', wrap_text=True)
    c.border = TB
    if w: ws.column_dimensions[get_column_letter(col)].width = w

# Identificación
h3(ws_i, 1, 'RUC',           AZUL, w=14)
h3(ws_i, 2, 'Razón Social',   AZUL, w=30)
h3(ws_i, 3, 'Depto',         AZUL, w=12)
h3(ws_i, 4, 'FOB UE USD',    AZUL, w=16)

# Inputs D1-D11
for col, name, label, fill in [
    (5,  'D1',  'D1 — Clasific.\nRegulatoria',    GRIS),
    (6,  'D2',  'D2 — Trazabilidad\n(SCORECARDS)', AZUL_O),
    (7,  'D3',  'D3 — Legalidad\n(OSCE/Neon)',    AZUL_O),
    (8,  'D4',  'D4 — Deforestación\nCero',         GRIS),
    (9,  'D5',  'D5 — Diligencia\nDebida',           AZUL_O),
    (10, 'D6',  'D6 — Capacidad\nDigital',          AZUL_O),
    (11, 'D7',  'D7 — Presión\nComprador',           GRIS),
    (12, 'D8',  'D8 — Gobernanza',                   GRIS),
    (13, 'D9',  'D9 — Riesgo\nFinanciero',          GRIS),
    (14, 'D10', 'D10 — Certificac.',                 GRIS),
    (15, 'D11', 'D11 — Género e\nInclusión',         GRIS),
]:
    h3(ws_i, col, label, fill, w=13)

# IP sub-dims
for col, name, label in [
    (16, 'IP1', 'IP1\nTrazabilidad\nD2'),
    (17, 'IP2', 'IP2\n√(D3×D4)'),
    (18, 'IP3', 'IP3\n(D5+D6+D8)/3'),
    (19, 'IP4', 'IP4\n(D6+D2)/2'),
    (20, 'IP5', 'IP5\n(D7+D9+C)/3'),
]:
    h3(ws_i, col, label, AZUL_2, w=13)

# IV sub-dims
for col, name, label in [
    (21, 'IV1', 'IV1\nPresión EU\nISA-PV×50'),
    (22, 'IV2', 'IV2\nD1 (base=50)'),
    (23, 'IV3', 'IV3\nha>0? 65:35'),
    (24, 'IV4', 'IV4\nCert=0? 70:30'),
    (25, 'IV5', 'IV5\nAsoc? 65:40'),
]:
    h3(ws_i, col, label, NARANJ_2, w=13)

# Scores
for col, name, label, fill in [
    (26, 'IP',  'IP\nPreparación',       DARK_H),
    (27, 'IV',  'IV\nVulnerabilidad',    NARANJ_D),
    (28, 'RE',  'RE\nExclusión',         ROJO_D),
    (29, 'Tipo','Tipología\n2×2 ISCAM',  DARK_GRN),
    (30, 'Band','Banderas\nDuras',       ROJO_D),
]:
    h3(ws_i, col, label, fill, w=17 if name in ('IP','IV','RE') else 20)

# Ambientales + Performance
for col, name, label in [
    (31, 'D12', 'D12\nHuella Carbono'),
    (32, 'D13', 'D13\nReporte Sostenib.'),
    (33, 'D14', 'D14\nEconomía Circular'),
    (34, 'D15', 'D15\nFitosanitario'),
    (35, 'ISA-PV','ISA-PV\nAVERAGE/2'),
    (36, 'P_Glb','P_Global\nPerformance'),
]:
    fill_map = {35: AMBER_H, 36: CYAN_H}
    h3(ws_i, col, label, VERDE_H if col <= 34 else fill_map.get(col, VERDE_H), w=13)

# ════════════════════════════════════════════════════════
# FILAS DE DATOS
# ════════════════════════════════════════════════════════
print('Escribiendo filas de datos…')

for r in range(4, max_row + 1):   # row 3=header, data desde row 4
    ws_i.row_dimensions[r].height = 16
    ruc = ws_m.cell(r, 1).value
    if not ruc:
        continue

    # A: RUC
    cfmt(ws_i, r, 1, ruc, align=CENTER)
    # B: Razón Social
    rs = ws_m.cell(r, 2).value or ''
    cfmt(ws_i, r, 2, rs, align=LEFT)
    # C: Depto
    cfmt(ws_i, r, 3, ws_m.cell(r, 3).value or '', align=CENTER)
    # D: FOB UE USD
    cfmt(ws_i, r, 4, ws_m.cell(r, 12).value or 0, fmt='#,##0')

    # ── Inputs D1-D11 ────────────────────────────────
    # D1 (col 5): pendiente → 0 gris
    cfmt(ws_i, r, 5, 0, GRIS, Font(color='999999', italic=True), CENTER)
    # D2 (col 6): desde SCORECARDS!H
    cfmt(ws_i, r, 6, f'=IFERROR(SCORECARDS!H{r},"")', CENTER, fmt='0.00')
    # D3 (col 7): desde MATRIZ_174!U (Neon)
    cfmt(ws_i, r, 7, f'=IFERROR(MATRIZ_174!U{r},0)', CENTER, fmt='0.00')
    # D4 (col 8): pendiente → 0 gris
    cfmt(ws_i, r, 8, 0, GRIS, Font(color='999999', italic=True), CENTER)
    # D5 (col 9): desde SCORECARDS!I
    cfmt(ws_i, r, 9, f'=IFERROR(SCORECARDS!I{r},"")', CENTER, fmt='0.00')
    # D6 (col 10): desde SCORECARDS!J
    cfmt(ws_i, r, 10, f'=IFERROR(SCORECARDS!J{r},"")', CENTER, fmt='0.00')
    # D7-D11 (cols 11-15): pendientes
    for col in [11, 12, 13, 14, 15]:
        cfmt(ws_i, r, col, 0, GRIS, Font(color='999999', italic=True), CENTER)

    # ── IP sub-dimensiones (cols 16-20) ──────────────
    # IP1 = D2 (col 6)
    cfmt(ws_i, r, 16, f'=IFERROR(F{r},0)', CENTER, fmt='0.00')
    # IP2 = SQRT(D3 × D4)  (cols 7 × 8)
    cfmt(ws_i, r, 17, f'=IFERROR(SQRT(G{r}*H{r}),0)', CENTER, fmt='0.00')
    # IP3 = (D5+D6+D8)/3  (cols 9, 10, 12)
    cfmt(ws_i, r, 18, f'=IFERROR((I{r}+J{r}+L{r})/3,0)', CENTER, fmt='0.00')
    # IP4 = (D6+D2)/2  (cols 10, 6)
    cfmt(ws_i, r, 19, f'=IFERROR((J{r}+F{r})/2,0)', CENTER, fmt='0.00')
    # IP5 = (D7+D9+CERT)/3  (cols 11, 13, MATRIZ_174!O)
    cfmt(ws_i, r, 20, f'=IFERROR((K{r}+M{r}+MATRIZ_174!O{r})/3,0)', CENTER, fmt='0.00')

    # ── IV sub-dimensiones (cols 21-25) ──────────────
    # IV1 = ISA-PV = (D12+D13+D14+D15)/4  (MATRIZ_174!AP = col 42)
    # Proxy presión ambiental / Pacto Verde: 0-2 → escalado a 0-100
    cfmt(ws_i, r, 21, f'=IFERROR(MATRIZ_174!AP{r}*50,0)', CENTER, fmt='0.0')
    # IV2 = D1 recodificado (si D1=0 pendiente → 50 baseline)
    cfmt(ws_i, r, 22, f'=IFERROR(IF(E{r}=0,50,E{r}),0)', CENTER, fmt='0.0')
    # IV3 = Fragilidad territorial: ha > 0 → más frágil
    cfmt(ws_i, r, 23, f'=IF(MATRIZ_174!R{r}>0,65,35)', CENTER, fmt='0.0')
    # IV4 = Brecha: cert = 0 → alta brecha
    cfmt(ws_i, r, 24, f'=IF(MATRIZ_174!O{r}=0,70,30)', CENTER, fmt='0.0')
    # IV5 = Tipo asoc. → mayor riesgo social
    cfmt(ws_i, r, 25, f'=IF(OR(MATRIZ_174!P{r}="ASOCIACION",MATRIZ_174!P{r}="PENDIENTE"),65,40)', CENTER, fmt='0.0')

    # ── IP Score (col 26) ────────────────────────────
    c = cfmt(ws_i, r, 26, f'=IFERROR(ROUND(AVERAGE(P{r},Q{r},R{r},S{r},T{r}),1),0)',
             _pf('D6E4F0'), Font(bold=True), CENTER, '0.0')

    # ── IV Score (col 27) ────────────────────────────
    cfmt(ws_i, r, 27, f'=IFERROR(ROUND(AVERAGE(U{r},V{r},W{r},X{r},Y{r}),1),0)',
         _pf('FCE4D6'), Font(bold=True), CENTER, '0.0')

    # ── RE = IV × (1 − IP/100) (col 28) ────────────
    # RE = IV × (1 − IP/100)  → col 28 (AB), IP=Z(26), IV=AA(27)
    cfmt(ws_i, r, 28, f'=IFERROR(ROUND(AA{r}*(1-Z{r}/100),1),0)',
         ROJO_L, Font(bold=True), CENTER, '0.0')

    # ── Tipología 2×2 (col 29) ───────────────────────
    # Corte: 50 | IP=Z(26) ≥50  vs <50 | IV=AA(27) ≥50 vs <50
    c = ws_i.cell(r, 29)
    c.value = (
        f'=IF(AND(Z{r}>=50,AA{r}<50),"🟢  Resilientes",'
        f'IF(AND(Z{r}>=50,AA{r}>=50),"🟠  Expuestas Adaptables",'
        f'IF(AND(Z{r}<50,AA{r}<50),"⬜  Riesgo Latente",'
        f'"🔴  Riesgo Crítico")))'
    )
    c.alignment = CENTER; c.border = TB

    # ── Banderas duras (col 30) ─────────────────────
    c = ws_i.cell(r, 30)
    c.value = f'=IF(G{r}=0,"🚫  Inh. vigente OSCE","")'
    c.alignment = CENTER; c.border = TB

    # ── D12-D15 + ISA-PV + P_Global (cols 31-36) ────
    cfmt(ws_i, r, 31, f'=IFERROR(MATRIZ_174!W{r},0)', CENTER, fmt='0')
    cfmt(ws_i, r, 32, f'=IFERROR(MATRIZ_174!X{r},0)', CENTER, fmt='0')
    cfmt(ws_i, r, 33, f'=IFERROR(MATRIZ_174!Y{r},0)', CENTER, fmt='0')
    cfmt(ws_i, r, 34, f'=IFERROR(MATRIZ_174!Z{r},0)', CENTER, fmt='0')
    cfmt(ws_i, r, 35, f'=IFERROR(MATRIZ_174!AP{r},"N/A")', CENTER, fmt='0.00')
    cfmt(ws_i, r, 36, f'=IFERROR(MATRIZ_174!AO{r},"N/A")', CENTER, fmt='0.00')

# ═══════════════════════════════════════════════════════════
# FILA DE PROMEDIOS (última fila)
# ═══════════════════════════════════════════════════════════
last_r = max_row + 1
ws_i.row_dimensions[last_r].height = 20

for c in range(1, 37):
    cell = ws_i.cell(last_r, c)
    cell.fill = DARK_GRN; cell.font = Font(bold=True, color='FFFFFF')
    cell.alignment = CENTER; cell.border = TB

ws_i.merge_cells(f'A{last_r}:D{last_r}')
ws_i.cell(last_r, 1).value = 'PROMEDIO MUESTRAL'
for col, lbl in [(26,'IP'), (27,'IV'), (28,'RE')]:
    c = ws_i.cell(last_r, col)
    c.value = f'=IFERROR(AVERAGE({get_column_letter(col)}4:{get_column_letter(col)}{max_row}),"—")'
    c.number_format = '0.0'
ws_i.cell(last_r, 29).value = f'n = {n_orgs} orgs'
ws_i.cell(last_r, 29).font = Font(bold=True, color='FFFFFF')

# ═══════════════════════════════════════════════════════════
# NOTA METODOLÓGICA AL PIE
# ═══════════════════════════════════════════════════════════
note_r = max_row + 3
ws_i.merge_cells(f'A{note_r}:AH{note_r}')
c = ws_i.cell(note_r, 1)
c.value = (
    'METODOLOGÍA ISCAM  |  '
    'IP = Promedio(IP1..IP5): IP1=D2, IP2=√(D3×D4), IP3=(D5+D6+D8)/3, IP4=(D6+D2)/2, IP5=(D7+D9+CERT)/3  |  '
    'IV = Promedio(IV1..IV5): IV1=ISA-PV×50, IV2=D1(baseline=50), IV3=ha>0?65:35, IV4=cert=0?70:30, IV5=tipo Asoc?65:40  |  '
    'RE = IV×(1−IP/100)  |  Corte 2×2: 50  |  '
    'Colores: █ GRIS=pendiente Instrumento 2  █ AZUL=Datos llenos  █ VERDE=Ambiental  █ NARANJA=IV  █ ROJO=RE'
)
c.fill = GRIS_L; c.font = Font(size=8, italic=True)
c.alignment = Alignment('left', 'center', wrap_text=True)
ws_i.row_dimensions[note_r].height = 30

print(f'ISCAM_Score: {n_orgs} orgs, 36 cols (A-AJ)')

# ═══════════════════════════════════════════════════════════
# ACTUALIZAR SCORECARDS
# ═══════════════════════════════════════════════════════════
ws_s['A1'].value = 'SCORECARDS — IP (Îndice de Preparación ISCAM) por organización'
# Header col N (fuera del loop de datos)
ws_s.cell(2, 14).value = 'Tipología ISCAM'

# Iterar SOLO sobre filas con RUC real (descarta merged cells)
scorecard_data_rows = [r for r in range(3, ws_s.max_row + 1)
                       if ws_s.cell(r, 1).value and str(ws_s.cell(r, 1).value).startswith('201')]
print(f'SCORECARDS: {len(scorecard_data_rows)} orgs con RUC')

for r in scorecard_data_rows:
    c = ws_s.cell(r, 3)
    # ISCAM_Score data starts at row 4, SCORECARDS data starts at row 3 → +1 offset
    c.value = f'=IFERROR(ISCAM_Score!Z{r+1},"—")'
    c.number_format = '0.0'

for r in scorecard_data_rows:
    c = ws_s.cell(r, 4)
    c.value = f'=IF(C{r}="—","— Sin D1-D11",IF(C{r}<34,"🔴  Crítico",IF(C{r}<67,"🟡  En desarrollo","🟢  Preparado")))'

for r in scorecard_data_rows:
    c = ws_s.cell(r, 14)
    c.value = f'=IFERROR(ISCAM_Score!AC{r+1},"")'

# ═══════════════════════════════════════════════════════════
# ACTUALIZAR RADAR_BRECHAS: D3 referencia correcta
# ═══════════════════════════════════════════════════════════
ws_r = wb['RADAR_BRECHAS']
# D3 ya usa AVERAGEIF hacia SCORECARDS!K — verificar que esté bien
for row in ws_r.iter_rows(min_row=3, max_row=ws_r.max_row, values_only=False):
    cell_d3 = row[2]  # col D = índice 2
    if cell_d3.value and 'SCORECARDS' in str(cell_d3.value):
        cell_d3.value = '=IFERROR(AVERAGEIF(MATRIZ_174!$C:$C,A{r},ISCAM_Score!$G:$G),0)'.replace('{r}', str(cell_d3.row))

# ═══════════════════════════════════════════════════════════
# ACTUALIZAR PONDERADORES — agregar sección ISCAM
# ═══════════════════════════════════════════════════════════
ws_p = wb['PONDERADORES']
next_row = ws_p.max_row + 2

# Título sección
ws_p.merge_cells(f'A{next_row}:D{next_row}')
c = ws_p.cell(next_row, 1)
c.value = 'VERSION ISCAM (2026-10-12) — Pesos fijos, no editables'
c.font = Font(bold=True, color='1F4E79')
next_row += 1

# Nota
ws_p.merge_cells(f'A{next_row}:D{next_row}')
c = ws_p.cell(next_row, 1)
c.value = 'IP e IV se calculan con pesos IGUALES (20% cada sub-dim). Los pesos se muestran para transparencia, no son editables.'
c.font = Font(size=9, italic=True)
next_row += 1

# Tabla de pesos ISCAM
iscam_weights = [
    ('SUBDIM ISCAM',    'FÓRMULA',                               'PESO'),
    ('IP1',             '= D2',                                  '20%'),
    ('IP2',             '= √(D3 × D4)',                          '20%'),
    ('IP3',             '= (D5 + D6 + D8) / 3',                  '20%'),
    ('IP4',             '= (D6 + D2) / 2',                       '20%'),
    ('IP5',             '= (D7 + D9 + Cert) / 3',               '20%'),
    ('IP (total)',       '= PROMEDIO(IP1:IP5)',                   '100%'),
    ('','',''),
    ('IV1',             '= ISA-PV × 50 (presión EU/PV)',         '20%'),
    ('IV2',             '= D1 (baseline=50 si pendiente)',        '20%'),
    ('IV3',             '= ha>0? 65 : 35 (fragilidad)',          '20%'),
    ('IV4',             '= cert=0? 70 : 30 (brecha)',            '20%'),
    ('IV5',             '= tipo Asoc? 65 : 40 (riesgo social)',  '20%'),
    ('IV (total)',       '= PROMEDIO(IV1:IV5)',                   '100%'),
    ('','',''),
    ('RE',              '= IV × (1 − IP/100)',                   '—'),
    ('Cuadrante 2×2',   'IP≥50 vs IP<50  ×  IV≥50 vs IV<50',    'Corte=50'),
]
fills_w = [AZUL, GRIS_L]*20
for i, (dim, formula, peso) in enumerate(iscam_weights):
    rn = next_row + i
    c1 = ws_p.cell(rn, 1); c1.value = dim; c1.fill = GRIS_L if i%2==1 else _pf('DEEAF1')
    c2 = ws_p.cell(rn, 2); c2.value = formula
    c3 = ws_p.cell(rn, 3); c3.value = peso
    if dim and dim[0].isupper() and dim != '':
        c1.font = BOLD; c3.font = BOLD
    for cc in [c1,c2,c3]:
        cc.alignment = LEFT; cc.border = TB

# ═══════════════════════════════════════════════════════════
# SANITIZAR ESTILOS ANTES DE GUARDAR
# Convierte StyleProxy fills del archivo original → PatternFill real
# ═══════════════════════════════════════════════════════════
from openpyxl.styles.fills import PatternFill as _PF
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for cell in row:
            f = cell.fill
            # StyleProxy aparece cuando openpyxl carga el archivo original
            if f is not None and not isinstance(f, _PF):
                # Reemplazar con fill transparente inerte (no afecta estilo original)
                cell.fill = _PF(patternType=None, fgColor='00000000')

# ═══════════════════════════════════════════════════════════
# GUARDAR
# ═══════════════════════════════════════════════════════════
wb.save(OUT)
print(f'\n✓ Guardado: {OUT}')

# ── Resumen ────────────────────────────────────────────────
print()
print('═══ ARQUITECTURA ISCAM IMPLEMENTADA ═══')
print()
print('HOJAS:')
print('  ISCAM_Score  Nueva — IP/IV/RE + matriz 2×2 + D12-D15 + ISA-PV + P_Global')
print('  SCORECARDS   Actualizada — IP vivo referencing ISCAM_Score!Z')
print('  MATRIZ_174   Intacta — D3 Neon + D12-D15 + Bloque P')
print('  PONDERADORES Actualizado — tabla de pesos ISCAM agregada')
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
print()
print('ESTADO DE DATOS:')
print('  D2/D5/D6 → valores 0 (sin Instrumento 2)')
print('  D3       → scores Neon (0.75-1.0 para 36 orgs)')
print('  D1,D4,D7-D11 → 0 (pendiente Instrumento 2)')
print('  D12-D15  → proxy IPCC/FAO + FOB UE')
print('  ISA-PV   → AVERAGE(D12:D15)/2')
print('  P_Global → promedio P1-P14')
print()
print('IP E IV MOSTRARÁN VALORES PARCIALES hasta que se llene Instrumento 2.')
print('La arquitectura está viva y recalculará automáticamente.')
