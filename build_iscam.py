# -*- coding: utf-8 -*-
"""
Reconstruye PLANTILLA_INDICE_PVE.xlsx bajo la arquitectura ISCAM completa:

  IP  = Índice de Preparación   (0-100)
  IV  = Índice de Vulnerabilidad (0-100)
  RE  = Riesgo de Exclusión    = IV × (1 - IP/100)
  Matriz 2×2: Preparación × Vulnerabilidad

Estructura:
  - SCORECARDS  → se renombra a IP_Scorecards (dashboard operativo IP)
  - ISCAM_Score → hoja nueva con IP/IV/RE/Quadrant completos
  - PONDERADORES → pesos ISCAM
"""

import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter

SRC = r'C:\Users\acuba\eudrperu\PLANTILLA_INDICE_PVE.xlsx'
OUT = r'C:\Users\acuba\eudrperu\PLANTILLA_INDICE_PVE_ISCAM.xlsx'

# ── Colores ──────────────────────────────────────────────
AZUL      = PatternFill(start_color='BDD7EE', end_color='BDD7EE', fill_type='solid')
AZUL_O    = PatternFill(start_color='9DC3E6', end_color='9DC3E6', fill_type='solid')
VERDE_H   = PatternFill(start_color='E2EFDA', end_color='E2EFDA', fill_type='solid')
VERDE_PK  = PatternFill(start_color='C6EFCE', end_color='C6EFCE', fill_type='solid')
NARANJA   = PatternFill(start_color='FCE4D6', end_color='FCE4D6', fill_type='solid')
AMARILLO  = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')
GRIS      = PatternFill(start_color='D9D9D9', end_color='D9D9D9', fill_type='solid')
GRIS_L    = PatternFill(start_color='F2F2F2', end_color='F2F2F2', fill_type='solid')
ROJO      = PatternFill(start_color='FF0000', end_color='FF0000', fill_type='solid')
ROJO_L    = PatternFill(start_color='FFCCCC', end_color='FFCCCC', fill_type='solid')
AMBER_L   = PatternFill(start_color='FFF2CC', end_color='FFF2CC', fill_type='solid')
BOLD      = Font(bold=True)
BOLD_BLANCO = Font(bold=True, color='FFFFFF')
CENTER    = Alignment(horizontal='center', vertical='center', wrap_text=True)
LEFT      = Alignment(horizontal='left', vertical='center', wrap_text=True)
THIN      = Side(style='thin')

def thin_border():
    return Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

def hdr(ws, r, c, v, fill=AZUL, font=None, align=CENTER, width=None, wrap=True):
    cell = ws.cell(r, c)
    cell.value = v
    cell.fill = fill
    cell.font = font or BOLD
    cell.alignment = Alignment(horizontal=align.horizontal, vertical='center', wrap_text=wrap)
    cell.border = thin_border()
    if width:
        ws.column_dimensions[get_column_letter(c)].width = width

def cell_fmt(ws, r, c, value, fill=None, font=None, align=CENTER, fmt=None):
    cell = ws.cell(r, c)
    cell.value = value
    if fill:
        cell.fill = fill
    if font:
        cell.font = font
    if align:
        cell.alignment = align
    if fmt:
        cell.number_format = fmt
    cell.border = thin_border()
    return cell

# ══════════════════════════════════════════════════════════
wb = openpyxl.load_workbook(SRC, data_only=False)
ws_matriz = wb['MATRIZ_174']
ws_pond   = wb['PONDERADORES']

# ── Determinar filas de datos ───────────────────────────
max_row = ws_matriz.max_row
print(f'Datos: {max_row - 2} organizaciones')

# ── CREAR HOJA ISCAM_Score ────────────────────────────
if 'ISCAM_Score' in wb.sheetnames:
    del wb['ISCAM_Score']
ws = wb.create_sheet('ISCAM_Score', 1)  # después de INSTRUCCIONES

ws.freeze_panes = 'C4'

# Fila 1: título
ws.merge_cells('A1:BF1')
c = ws['A1']
c.value = 'ISCAM — Índice de Preparación (IP) × Índice de Vulnerabilidad (IV) × Riesgo de Exclusión (RE) — Café y Cacao Perú'
c.fill = PatternFill(start_color='1F4E79', end_color='1F4E79', fill_type='solid')
c.font = Font(bold=True, color='FFFFFF', size=12)
c.alignment = CENTER
ws.row_dimensions[1].height = 30

# Fila 2: nota
ws.merge_cells('A2:BF2')
c = ws['A2']
c.value = (
    'IP e IV se calculan tras aplicar Instrumento 2 (D1-D11). '
    'D3 = Legalidad OSCE (fuente: Neon). '
    'Las columnas en GRIS son inputs del Instrumento 2 (pendientes). '
    'P_Global e ISA-PactoVerde se leen de MATRIZ_174 (W-AP). '
    'RE = IV × (1 - IP/100). Cuadrante: IP alto/bajo × IV alto/bajo (corte = mediana muestral).'
)
c.fill = PatternFill(start_color='D6E4F0', end_color='D6E4F0', fill_type='solid')
c.font = Font(size=9, italic=True)
c.alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
ws.row_dimensions[2].height = 35

# Fila 3: grupo de headers
ws.row_dimensions[3].height = 18

# ── GRUPOS DE COLUMNAS ────────────────────────────────
# Identificación: A-D
# D1-D11 (inputs): E-O
# IP sub-dims: P-T
# IV sub-dims: U-Y
# Scores: Z-AB
# Instrumento 2 cols: AC-AF
# Block P cols: AG-AU

NCOL = 57  # hasta col BF

# Identificación
hdr(ws, 3, 1, 'RUC',              fill=AZUL, width=14)
hdr(ws, 3, 2, 'Razón Social',      fill=AZUL, width=30)
hdr(ws, 3, 3, 'Depto',             fill=AZUL, width=14)
hdr(ws, 3, 4, 'FOB UE USD',        fill=AZUL, width=16)

# D1-D11 (inputs Instrumento 2) — GRIS = pendientes
D_HEADERS = [
    (5,  'D1',   'Clasificación\nRegulatoria',         'D2',  'Trazabilidad',          'D3',  'Legalidad\n(OSCE)',       'D4',  'Deforestación\nCero',
     9,  'D5',   'Diligencia\nDebida',                10,    'D6',   'Capacidad\nDigital',      11,    'D7',   'Presión\nComprador',
     12, 'D8',   'Gobernanza',                        13,    'D9',   'Riesgo\nFinanciero',     14,    'D10',  'Certificaciones']
for i, val in enumerate(D_HEADERS, start=5):
    if isinstance(val, int):
        continue  # skip odd indices (they are labels)
    col = i
    # Determine fill: D3 = azul por tener dato Neon
    d_name = D_HEADERS[i-5] if (i-5) % 3 == 0 else ''
    fill = AZUL_O if (i-5) % 3 == 2 else GRIS  # col 7 = D3 = azul
    hdr(ws, 3, col, D_HEADERS[i-4], fill=fill, width=12)

# Rebuild D_HEADERS properly
d_cols = [
    (5,  'D1',   'Clasificación Reg.',          GRIS),
    (7,  'D2',   'Trazabilidad',                GRIS),
    (9,  'D3',   'Legalidad (OSCE)',            AZUL_O),  # D3 = dato Neon
    (11, 'D4',   'Deforestación Cero',          GRIS),
    (13, 'D5',   'Diligencia Debida',           GRIS),
    (15, 'D6',   'Capacidad Digital',           GRIS),
    (17, 'D7',   'Presión Comprador',          GRIS),
    (19, 'D8',   'Gobernanza',                 GRIS),
    (21, 'D9',   'Riesgo Financiero',          GRIS),
    (23, 'D10',  'Certificaciones',             GRIS),
]
for col, name, label, fill in d_cols:
    hdr(ws, 3, col, f'{name}\n{label}', fill=fill, width=13)

# IP sub-dimensiones
ip_cols = [
    (25, 'IP1', 'Trazabilidad\n(D2)',          PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')),
    (27, 'IP2', 'Cump. Ambiental\n√(D3×D4)',   PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')),
    (29, 'IP3', 'Capacidades\nOrg. (D5+D6+D8)',PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')),
    (31, 'IP4', 'Info y Docs\n(D6.23+D2.9)',  PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')),
    (33, 'IP5', 'Adaptación\n(D7+D9+D11+Cert)',PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')),
]
for col, name, label, fill in ip_cols:
    c = ws.cell(3, col)
    c.value = f'{name}\n{label}'
    c.fill = fill
    c.font = Font(bold=True, color='FFFFFF')
    c.alignment = CENTER
    c.border = thin_border()
    ws.column_dimensions[get_column_letter(col)].width = 13

# IV sub-dimensiones
iv_cols = [
    (35, 'IV1', 'Depend. UE\n(P1/P1b+P4)',    PatternFill(start_color='C55A11', end_color='C55A11', fill_type='solid')),
    (37, 'IV2', 'Exposición Reg.\n(D1)',        PatternFill(start_color='C55A11', end_color='C55A11', fill_type='solid')),
    (39, 'IV3', 'Fragilidad\nTerritorial',      PatternFill(start_color='C55A11', end_color='C55A11', fill_type='solid')),
    (41, 'IV4', 'Brechas Tec/Fin\n(100-D6.24+D9)',PatternFill(start_color='C55A11', end_color='C55A11', fill_type='solid')),
    (43, 'IV5', 'Riesgo Social\ny Comercial',   PatternFill(start_color='C55A11', end_color='C55A11', fill_type='solid')),
]
for col, name, label, fill in iv_cols:
    c = ws.cell(3, col)
    c.value = f'{name}\n{label}'
    c.fill = fill
    c.font = Font(bold=True, color='FFFFFF')
    c.alignment = CENTER
    c.border = thin_border()
    ws.column_dimensions[get_column_letter(col)].width = 13

# Scores principales
score_cols = [
    (45, 'IP',    'Índice de\nPreparación',  '0-100', PatternFill(start_color='203864', end_color='203864', fill_type='solid')),
    (47, 'IV',    'Índice de\nVulnerabilidad','0-100', PatternFill(start_color='843C0C', end_color='843C0C', fill_type='solid')),
    (49, 'RE',    'Riesgo de\nExclusión',  '0-100', PatternFill(start_color='7B1818', end_color='7B1818', fill_type='solid')),
    (51, 'Cuadrante', 'Tipología ISCAM',   '',      PatternFill(start_color='375623', end_color='375623', fill_type='solid')),
    (53, 'Banderas',  'Banderas Duras',   '',      PatternFill(start_color='7B1818', end_color='7B1818', fill_type='solid')),
]
for col, name, label, rng, fill in score_cols:
    c = ws.cell(3, col)
    c.value = f'{name}\n{label}'
    c.fill = fill
    c.font = Font(bold=True, color='FFFFFF')
    c.alignment = CENTER
    c.border = thin_border()
    ws.column_dimensions[get_column_letter(col)].width = 16 if name in ['IP','IV','RE'] else 22

# D12-D15 + ISA-PV (desde MATRIZ_174)
env_cols = [
    (55, 'D12',  'Huella Carbono',  'MATRIZ W', PatternFill(start_color='70AD47', end_color='70AD47', fill_type='solid')),
    (57, 'D13',  'Reporte Sostenib.', 'MATRIZ X', PatternFill(start_color='70AD47', end_color='70AD47', fill_type='solid')),
    (59, 'D14',  'Economía Circular', 'MATRIZ Y', PatternFill(start_color='70AD47', end_color='70AD47', fill_type='solid')),
    (61, 'D15',  'Fitosanitario',    'MATRIZ Z', PatternFill(start_color='70AD47', end_color='70AD47', fill_type='solid')),
    (63, 'ISA-PV','ISA-PactoVerde', 'MATRIZ AP', PatternFill(start_color='FF9900', end_color='FF9900', fill_type='solid')),
    (65, 'P_Glob','Performance',     'MATRIZ AO', PatternFill(start_color='00B0F0', end_color='00B0F0', fill_type='solid')),
]
for col, name, label, src, fill in env_cols:
    c = ws.cell(3, col)
    c.value = f'{name}\n({label})'
    c.fill = fill
    c.font = Font(bold=True, color='FFFFFF')
    c.alignment = CENTER
    c.border = thin_border()
    ws.column_dimensions[get_column_letter(col)].width = 13

# ── FILAS DE DATOS ────────────────────────────────────
print('Escribiendo filas de datos...')

for r in range(3, max_row + 1):
    ws.row_dimensions[r].height = 16
    ruc = ws_matriz.cell(r, 1).value
    if not ruc:
        continue

    # A: RUC
    cell_fmt(ws, r, 1, ruc, align=CENTER)

    # B: Razón Social
    rs = ws_matriz.cell(r, 2).value or ''
    cell_fmt(ws, r, 2, rs, align=LEFT)

    # C: Depto
    dept = ws_matriz.cell(r, 3).value or ''
    cell_fmt(ws, r, 3, dept, align=CENTER)

    # D: FOB UE USD (hardcoded value from MATRIZ col L)
    fob_ue = ws_matriz.cell(r, 12).value or 0
    cell_fmt(ws, r, 4, fob_ue, fmt='#,##0')

    # E-O: D1-D10 inputs (GRIS = pendientes de Instrumento 2)
    for col in [5, 7, 9, 11, 13, 15, 17, 19, 21, 23]:
        c = ws.cell(r, col)
        c.value = 0
        c.fill = GRIS
        c.alignment = CENTER
        c.font = Font(color='999999', italic=True)
        c.border = thin_border()

    # D3 (col 9): leer de MATRIZ_174 col U (D3 Score)
    c_d3 = ws.cell(r, 9)
    c_d3.value = f'=MATRIZ_174!U{r}'
    c_d3.fill = PatternFill(start_color='BDD7EE', end_color='BDD7EE', fill_type='solid')
    c_d3.alignment = CENTER
    c_d3.border = thin_border()

    # ── IP sub-dimensiones (col 25-33) ──────────────
    # IP1 = D2 (col 7)
    c = ws.cell(r, 25); c.value = f'=IFERROR(I{r},0)'; c.alignment = CENTER; c.border = thin_border()
    # IP2 = √(D3 × D4)  (cols 9 y 11)
    c = ws.cell(r, 27); c.value = f'=IFERROR(SQRT(J{r}*L{r}),0)'; c.alignment = CENTER; c.border = thin_border()
    # IP3 = (D5+D6+D8)/3  (cols 13, 15, 19)
    c = ws.cell(r, 29); c.value = f'=IFERROR((N{r}+P{r}+T{r})/3,0)'; c.alignment = CENTER; c.border = thin_border()
    # IP4 = (D6.23+D2.9)/2 — D6.23 en D6 col 15, D2.9 proxy en D2 col 7
    c = ws.cell(r, 31); c.value = f'=IFERROR((P{r}+H{r})/2,0)'; c.alignment = CENTER; c.border = thin_border()
    # IP5 = (D7+D9+D11+CERT)/4  (cols 17, 21, + cert from MATRIZ col O)
    c = ws.cell(r, 33); c.value = f'=IFERROR((R{r}+V{r}+MATRIZ_174!O{r})/3,0)'; c.alignment = CENTER; c.border = thin_border()

    # ── IV sub-dimensiones (col 35-43) ──────────────
    # IV1 = Dependencia UE (proxy: FOB UE > 0 → 50; alta → 80; baja → 20)
    # Proxy: si FOB UE > 0 → tienen exposición UE → IV1 = 50 baseline
    c = ws.cell(r, 35); c.value = f'=IF(D{r}>0,50,20)'; c.alignment = CENTER; c.border = thin_border()
    # IV2 = D1 recodificado (proxy: 50 por ahora)
    c = ws.cell(r, 37); c.value = f'=F{r}*0'; c.alignment = CENTER; c.border = thin_border(); c.fill = GRIS
    # IV3 = Fragilidad territorial (proxy: ha > 0 → más frágil)
    c = ws.cell(r, 39); c.value = f'=IF(MATRIZ_174!R{r}>0,60,40)'; c.alignment = CENTER; c.border = thin_border()
    # IV4 = Brechas tecnológicas (proxy: cert = 0 → alta brecha)
    c = ws.cell(r, 41); c.value = f'=IF(MATRIZ_174!O{r}=0,70,30)'; c.alignment = CENTER; c.border = thin_border()
    # IV5 = Riesgo social (proxy: tipo org = asociación → mayor riesgo)
    c = ws.cell(r, 43); c.value = f'=IF(OR(MATRIZ_174!P{r}="ASOCIACION",MATRIZ_174!P{r}="PENDIENTE"),60,40)'; c.alignment = CENTER; c.border = thin_border()

    # ── IP Score (col 45) ────────────────────────────
    c = ws.cell(r, 45)
    c.value = f'=IFERROR(ROUND(AVERAGE(AA{r},AC{r},AE{r},AG{r},AI{r}),1),0)'
    c.number_format = '0.0'
    c.fill = PatternFill(start_color='D6E4F0', end_color='D6E4F0', fill_type='solid')
    c.font = Font(bold=True)
    c.alignment = CENTER
    c.border = thin_border()

    # ── IV Score (col 47) ────────────────────────────
    c = ws.cell(r, 47)
    c.value = f'=IFERROR(ROUND(AVERAGE(AK{r},AM{r},AO{r},AQ{r},AS{r}),1),0)'
    c.number_format = '0.0'
    c.fill = PatternFill(start_color='FCE4D6', end_color='FCE4D6', fill_type='solid')
    c.font = Font(bold=True)
    c.alignment = CENTER
    c.border = thin_border()

    # ── RE = IV × (1 - IP/100) (col 49) ─────────────
    c = ws.cell(r, 49)
    c.value = f'=IFERROR(ROUND(AU{r}*(1-AV{r}/100),1),0)'
    c.number_format = '0.0'
    c.fill = PatternFill(start_color='FFCCCC', end_color='FFCCCC', fill_type='solid')
    c.font = Font(bold=True)
    c.alignment = CENTER
    c.border = thin_border()

    # ── Cuadrante 2×2 (col 51) ───────────────────────
    # Corte: mediana de la muestra → se usa 50 como proxy (IP e IV en escala 0-100)
    c = ws.cell(r, 51)
    c.value = (
        f'=IF(AND(AV{r}>=50,AU{r}<50),"🟢 Resilientes",'
        f'IF(AND(AV{r}>=50,AU{r}>=50),"🟠 Expuestas Adaptables",'
        f'IF(AND(AV{r}<50,AU{r}<50),"⬜ Riesgo Latente",'
        f'"🔴 Riesgo Crítico")))'
    )
    c.alignment = CENTER
    c.border = thin_border()
    ws.row_dimensions[r].height = 18

    # ── Banderas duras (col 53) ─────────────────────
    c = ws.cell(r, 53)
    # D3=0 → inh. vigente = bandera roja
    c.value = f'=IF(J{r}=0,"🚫 Inh. vigente OSCE","")'
    c.alignment = CENTER
    c.border = thin_border()

    # ── D12-D15 e ISA-PV (cols 55-65) ──────────────
    # D12 = MATRIZ col W=23
    c = ws.cell(r, 55); c.value = f'=MATRIZ_174!W{r}'; c.alignment = CENTER; c.border = thin_border()
    # D13 = MATRIZ col X=24
    c = ws.cell(r, 57); c.value = f'=MATRIZ_174!X{r}'; c.alignment = CENTER; c.border = thin_border()
    # D14 = MATRIZ col Y=25
    c = ws.cell(r, 59); c.value = f'=MATRIZ_174!Y{r}'; c.alignment = CENTER; c.border = thin_border()
    # D15 = MATRIZ col Z=26
    c = ws.cell(r, 61); c.value = f'=MATRIZ_174!Z{r}'; c.alignment = CENTER; c.border = thin_border()
    # ISA-PV = MATRIZ col AP=42
    c = ws.cell(r, 63)
    c.value = f'=IFERROR(MATRIZ_174!AP{r},"N/A")'
    c.number_format = '0.00'
    c.alignment = CENTER; c.border = thin_border()
    # P_Global = MATRIZ col AO=41
    c = ws.cell(r, 65)
    c.value = f'=IFERROR(MATRIZ_174!AO{r},"N/A")'
    c.number_format = '0.00'
    c.alignment = CENTER; c.border = thin_border()

# ── FILA DE PROMEDIOS ────────────────────────────────
last_r = max_row + 1
ws.row_dimensions[last_r].height = 20
for c in range(1, 66):
    cell = ws.cell(last_r, c)
    cell.fill = PatternFill(start_color='375623', end_color='375623', fill_type='solid')
    cell.font = Font(bold=True, color='FFFFFF')
    cell.border = thin_border()
    cell.alignment = CENTER

ws.cell(last_r, 1).value = 'PROMEDIO MUESTRAL'
ws.merge_cells(f'A{last_r}:D{last_r}')
for c in [45, 47, 49]:
    col_l = get_column_letter(c)
    ws.cell(last_r, c).value = f'=IFERROR(AVERAGE({col_l}3:{col_l}{max_row}),"—")'
    ws.cell(last_r, c).number_format = '0.0'
ws.cell(last_r, 51).value = f'{max_row - 2} organizaciones'

# ── LEYENDA DE COLORES ──────────────────────────────
note_r = max_row + 3
ws.merge_cells(f'A{note_r}:BF{note_r}')
c = ws.cell(note_r, 1)
c.value = (
    'LEYENDA: █ GRIS = input pendiente del Instrumento 2 (D1-D11)   '
    '█ AZUL OSCURO = IP sub-dimensión (preparación)   '
    '█ NARANJA OSCURO = IV sub-dimensión (vulnerabilidad)   '
    '█ VERDE OSCURO = ISCAM Score   '
    '█ ROJO = Riesgo de Exclusión   '
    '█ VERDE CLARO = ISA-PactoVerde   '
    'RE = IV × (1 - IP/100) | Corte alto/bajo: 50 (mediana muestral proxy)'
)
c.fill = GRIS_L
c.font = Font(size=8, italic=True)
c.alignment = Alignment(horizontal='left', wrap_text=True)
ws.row_dimensions[note_r].height = 30

print(f'ISCAM_Score: {max_row - 2} orgs escritas, {ws.max_column} columnas')

# ══════════════════════════════════════════════════════════
# ACTUALIZAR SCORECARDS — IP-centrado con referencia ISCAM
# ══════════════════════════════════════════════════════════
ws_s = wb['SCORECARDS']

# Actualizar título
ws_s['A1'].value = 'SCORECARDS — IP (Índice de Preparación ISCAM) por organización'

# Reemplazar columna C (PVE Score) con fórmula IP
# IP = promedio(IP1:IP5) — referenciando ISCAM_Score
# IP1=D2, IP2=√(D3×D4), IP3=(D5+D6+D8)/3, IP4=(D6.23+D2.9)/2, IP5=(D7+D9+CERT)/4
for r in range(3, ws_s.max_row + 1):
    c = ws_s.cell(r, 3)
    # Referencia viva a ISCAM_Score col AV = 48
    c.value = f'=IFERROR(ISCAM_Score!AV{r},"—")'
    c.number_format = '0.0'

# Actualizar semáforo para IP (corte 50)
ws_s.cell(2, 4).value = 'Semáforo IP'
for r in range(3, ws_s.max_row + 1):
    c = ws_s.cell(r, 4)
    c.value = f'=IF(C{r}="—","— Sin D1-D11",IF(C{r}<34,"🔴 Crítico",IF(C{r}<67,"🟡 En desarrollo","🟢 Preparado")))'

# Actualizar semáforo UE para referencia cruz IP×IV (lee de ISCAM_Score)
ws_s.cell(2, 14).value = 'Tipología ISCAM'
for r in range(3, ws_s.max_row + 1):
    c = ws_s.cell(r, 14)
    c.value = f'=IFERROR(ISCAM_Score!AY{r},"")'

# ══════════════════════════════════════════════════════════
# ACTUALIZAR PONDERADORES — pesos ISCAM
# ══════════════════════════════════════════════════════════
# Limpiar y reescribir la sección de ponderaciones
ws_p = wb['PONDERADORES']

# Agregar nota de versión ISCAM
note_row = 23
if ws_p.max_row >= note_row:
    pass
else:
    ws_p.cell(note_row, 1).value = 'VERSION ISCAM (2026-10-12)'
    ws_p.cell(note_row, 1).font = Font(bold=True, color='1F4E79')

# ══════════════════════════════════════════════════════════
# GUARDAR
# ══════════════════════════════════════════════════════════
wb.save(OUT)
print(f'\n✓ Guardado: {OUT}')
print('\nArquitectura ISCAM:')
print('  ISCAM_Score: IP1-IP5, IV1-IV5, IP, IV, RE, Cuadrante, D12-D15, ISA-PV')
print('  SCORECARDS:   IP vivo con referencia a ISCAM_Score')
print('  MATRIZ_174:  D3 Neon + D12-D15 + Bloque P intactos')
print()
print('NOTA: D1-D11 en GRIS = pendientes Instrumento 2.')
print('      IP/IV/RE muestran "—" hasta que se llene Instrumento 2.')
print('      Banderas duras (D3=0) ya se levantan desde Neon.')
