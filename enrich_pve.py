# -*- coding: utf-8 -*-
"""Enriquece PLANTILLA_INDICE_PVE_d3.xlsx con D12-D15, Bloque P, D3 vivo en SCORECARDS."""

import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.utils import get_column_letter
from openpyxl.cell.cell import MergedCell

SRC = r'C:\Users\acuba\eudrperu\PLANTILLA_INDICE_PVE_d3.xlsx'
OUT = r'C:\Users\acuba\eudrperu\PLANTILLA_INDICE_PVE_enriquecida.xlsx'

wb = openpyxl.load_workbook(SRC, data_only=False)

# ── Colores ──────────────────────────────────────────────
AMARILLO = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')
GRIS     = PatternFill(start_color='D9D9D9', end_color='D9D9D9', fill_type='solid')
AZUL     = PatternFill(start_color='BDD7EE', end_color='BDD7EE', fill_type='solid')
VERDE_PK = PatternFill(start_color='E2EFDA', end_color='E2EFDA', fill_type='solid')
NARANJA  = PatternFill(start_color='FF9900', end_color='FF9900', fill_type='solid')
AMARIL_F = PatternFill(start_color='FFE699', end_color='FFE699', fill_type='solid')
BOLD     = Font(bold=True)

def set_header(ws, row, col, value, fill=AZUL, font=None):
    c = ws.cell(row, col)
    c.value = value
    c.fill = fill
    c.font = font or BOLD
    c.alignment = Alignment(horizontal='center', wrap_text=True)

# ══════════════════════════════════════════════════════════
# 1. MATRIZ_174 — agregar D12-D15 + Bloque P (P1-P14) + P_Global + ISA-PactoVerde
# ══════════════════════════════════════════════════════════
ws_m = wb['MATRIZ_174']
start_col = ws_m.max_column + 1  # = 23

# D12-D15 (variables填-able, default gris=pendiente)
D12_D15 = [
    ('D12', 'Huella Carbono (D12)\n0=No, 1=En curso, 2=Certificado'),
    ('D13', 'Reporte Sostenibilidad (D13)\n0=No, 1=En curso, 2=Publicado'),
    ('D14', 'Economía Circular (D14)\n0=No, 1=En transición, 2=Avanzado'),
    ('D15', 'Fitosanitario/LMR (D15)\n0=No verificado, 1=En monitoreo, 2=Cumple UE'),
]

for i, (col_name, col_label) in enumerate(D12_D15):
    col_idx = start_col + i
    set_header(ws_m, 1, col_idx, col_name, fill=AZUL)
    set_header(ws_m, 2, col_idx, col_label, fill=AZUL)
    ws_m.column_dimensions[get_column_letter(col_idx)].width = 22
    for r in range(3, ws_m.max_row + 1):
        cell = ws_m.cell(r, col_idx)
        if cell.value is None:
            cell.value = 0
            cell.fill = GRIS
            cell.alignment = Alignment(horizontal='center')

# Bloque P — 14 indicadores de performance
BLOQUE_P = [
    ('P1',  'P1 — Productividad (USD/ha/año)'),
    ('P2',  'P2 — Ingreso neto (USD/ha)'),
    ('P3',  'P3 — % socios con acceso crédito'),
    ('P4',  'P4 — Gender score (% muj. en org.)'),
    ('P5',  'P5 — Formalización laboral (%)'),
    ('P6',  'P6 — Capacitación/año/persona'),
    ('P7',  'P7 — Tasa retención socios (%)'),
    ('P8',  'P8 — Diversificación ingresos (%)'),
    ('P9',  'P9 — Acceso mercados premium (%)'),
    ('P10', 'P10 — Inversión EUDR (USD/año)'),
    ('P11', 'P11 — Score trazabilidad (%)'),
    ('P12', 'P12 — Quejas resueltas (%)'),
    ('P13', 'P13 — Energía renovable (%)'),
    ('P14', 'P14 — Residuos gestionados (%)'),
]

p_start = start_col + len(D12_D15)  # = 27
for i, (col_name, col_label) in enumerate(BLOQUE_P):
    col_idx = p_start + i
    set_header(ws_m, 1, col_idx, col_name, fill=VERDE_PK)
    set_header(ws_m, 2, col_idx, col_label, fill=VERDE_PK)
    ws_m.column_dimensions[get_column_letter(col_idx)].width = 20
    for r in range(3, ws_m.max_row + 1):
        cell = ws_m.cell(r, col_idx)
        if cell.value is None:
            cell.value = 0
            cell.fill = GRIS
            cell.alignment = Alignment(horizontal='center')

# P_Global — promedio P1:P14
p_global_col = p_start + len(BLOQUE_P)  # = 41
set_header(ws_m, 1, p_global_col, 'Bloque P\nScore (0-1)', fill=VERDE_PK)
set_header(ws_m, 2, p_global_col, 'P_Global — Promedio P1:P14\n(0=None, 1=满分)', fill=VERDE_PK)
ws_m.column_dimensions[get_column_letter(p_global_col)].width = 16
for r in range(3, ws_m.max_row + 1):
    p_cols = ','.join([f'{get_column_letter(p_start+i)}{r}' for i in range(14)])
    c = ws_m.cell(r, p_global_col)
    c.value = f'=IFERROR(AVERAGE({p_cols}),"N/A")'
    c.fill = PatternFill(start_color='C6EFCE', end_color='C6EFCE', fill_type='solid')
    c.alignment = Alignment(horizontal='center')

# ISA-PactoVerde — promedio D12:D15 / 2 (cada dimensión escala 0-2)
pv_col = p_global_col + 1  # = 42
set_header(ws_m, 1, pv_col, 'ISA-PactoVerde\n(0-1)', fill=NARANJA)
set_header(ws_m, 2, pv_col, 'ISA-PactoVerde = AVG(D12:D15)/2\n0=Nada, 2=Certificado', fill=NARANJA)
ws_m.column_dimensions[get_column_letter(pv_col)].width = 16
for r in range(3, ws_m.max_row + 1):
    d_cols = ','.join([f'{get_column_letter(start_col+i)}{r}' for i in range(4)])
    c = ws_m.cell(r, pv_col)
    c.value = f'=IFERROR(AVERAGE({d_cols})/2,"N/A")'
    c.fill = AMARIL_F
    c.alignment = Alignment(horizontal='center')

print('MATRIZ_174 extendida:')
print(f'  D12-D15  → cols {get_column_letter(start_col)}-{get_column_letter(start_col+3)} (nuevas)')
print(f'  P1-P14   → cols {get_column_letter(p_start)}-{get_column_letter(p_start+13)} (nuevas)')
print(f'  P_Global → col  {get_column_letter(p_global_col)} (fórmula AVG P1:P14)')
print(f'  ISA-PV   → col  {get_column_letter(pv_col)} (fórmula AVG D12:D15 / 2)')

# ══════════════════════════════════════════════════════════
# 2. SCORECARDS — col K = D3 Legalidad (INDEX/MATCH desde MATRIZ_174!U)
# ══════════════════════════════════════════════════════════
ws_s = wb['SCORECARDS']
set_header(ws_s, 2, 11, 'Legalidad\nD3 (OSCE)', fill=AZUL)
ws_s.column_dimensions['K'].width = 14

for r in range(3, ws_s.max_row + 1):
    cell = ws_s.cell(r, 11)
    if isinstance(cell, MergedCell):
        continue
    cell.value = f'=IFERROR(INDEX(MATRIZ_174!$U:$U,MATCH(A{r},MATRIZ_174!$A:$A,0)),"")'
    cell.alignment = Alignment(horizontal='center')

print('\nSCORECARDS: col K = D3 Legalidad (INDEX/MATCH MATRIZ_174!U)')

# ══════════════════════════════════════════════════════════
# 3. RADAR_BRECHAS — col D (D3 Legalidad) = AVERAGEIF desde SCORECARDS!K
# ══════════════════════════════════════════════════════════
ws_r = wb['RADAR_BRECHAS']
for r in range(3, ws_r.max_row + 1):
    cell = ws_r.cell(r, 4)
    # Skip merged cells (only write to top-left of range)
    from openpyxl.cell.cell import MergedCell
    if isinstance(cell, MergedCell):
        continue
    cell.value = f'=IFERROR(AVERAGEIF(MATRIZ_174!$C:$C,A{r},SCORECARDS!$K:$K),0)'

print('RADAR_BRECHAS: col D = D3 Legalidad (AVERAGEIF → SCORECARDS!K)')

# ── Guardar ──────────────────────────────────────────────
wb.save(OUT)
print(f'\n✓ Guardado: {OUT}')
