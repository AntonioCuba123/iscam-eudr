"""
Agregar columna FUENTE (col A) a la pestaña MATRIZ.
Detecta fuentes por cada org: PAC | MIDAGRI | CENCOOP 2017 | SOPARSE | SISPAC | SUNAT API
Concatenadas con punto y coma.
"""
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

PATH_V8B  = r'C:\Users\acuba\eudrperu\MATRIZ_IP_IV_v8b_EUDRPERU.xlsx'
PATH_OUT  = r'C:\Users\acuba\eudrperu\MATRIZ_IP_IV_v10_EUDRPERU.xlsx'
PATH_A1   = (
    r'C:\Users\acuba\.minimax\v2\assets\2026\09\18'
    r'\12-31-56-449-asset_20260918-123156-449_b797e5d1c8cd_bc2f6481'
    r'-cf948520-5739-4d82-8952-b9f7974eaf3c_06260002713402 (1).xlsx'
)
PATH_CENACOOP = r'C:\Users\acuba\eudrperu\data\CENACOOP_fusion_EUDR.csv'

# Los 5 RUCs validados por API (insertados en v8b)
SUNAT_API_RUCS = {
    '20132509876', '20568190450', '20603557825',
    '20603734255', '20609098989'
}

# ─────────────────────────────────────────────────────────────────────────────
# 1. Cargar RUCs de SISPAC (Archivo1)
# ─────────────────────────────────────────────────────────────────────────────
raw_a1 = pd.read_excel(PATH_A1, header=None)
rucs_sispac = set(
    raw_a1.iloc[3:, 112]
    .dropna()
    .astype(str)
    .str.strip()
    .where(raw_a1.iloc[3:, 112].astype(str).str.strip().str.match(r'^20\d{9}$'))
    .dropna()
)
# SIN SOPARSE: no hay archivo verificado para esa fuente

# ─────────────────────────────────────────────────────────────────────────────
# 3. Abrir workbook y modificar MATRIZ
# ─────────────────────────────────────────────────────────────────────────────
wb = openpyxl.load_workbook(PATH_V8B)
ws = wb['MATRIZ']

# Headers en fila 4 (0-indexed: row 4)
headers = {cell.column: cell.value for cell in ws[4] if cell.value}
col_ruc    = next((c for c, v in headers.items() if str(v).strip().upper() == 'RUC'), 1)
col_pac    = next((c for c, v in headers.items() if 'EN DIRECTORIO PAC' in str(v).upper()), None)
col_midagri= next((c for c, v in headers.items() if str(v).strip().upper() == 'EN MIDAGRI'), None)
col_cenacoop= next((c for c, v in headers.items() if str(v).strip().upper() == 'EN CENACOOP'), None)
col_cen    = next((c for c, v in headers.items() if 'FLAG CENCOOP' in str(v).upper()), None)

print(f'Columnas: RUC={col_ruc}, PAC={col_pac}, MIDAGRI={col_midagri}, CENCOOP={col_cen}')

# Leer todos los RUCs de la columna actual ANTES de insertar
rucs_por_fila = {}
for r in range(5, ws.max_row + 1):
    rucs_por_fila[r] = str(ws.cell(row=r, column=col_ruc).value).strip() \
        if ws.cell(row=r, column=col_ruc).value else ''

# Insertar columna nueva en posicion col_ruc (antes del RUC)
ws.insert_cols(col_ruc)
# Todos los indices de columnas a la derecha de col_ruc se incrementaron en 1
def shift(col_n, base):
    return col_n + 1 if col_n and col_n > base else col_n
col_pac     = shift(col_pac,     col_ruc)
col_midagri = shift(col_midagri,  col_ruc)
col_cenacoop= shift(col_cenacoop, col_ruc)
col_cen     = shift(col_cen,     col_ruc)
# col_ruc ahora apunta a la nueva columna FUENTE
# La original RUC está en col_ruc + 1
print(f'Despues de insertar: FUENTE={col_ruc}, RUC orig={col_ruc+1}, PAC={col_pac}, MIDAGRI={col_midagri}, CENACOOP={col_cenacoop}, CENCOOP2017={col_cen}')

# ─────────────────────────────────────────────────────────────────────────────
# 4. Determinar fuente para cada fila (datos desde fila 5)
# ─────────────────────────────────────────────────────────────────────────────
def detectar_fuentes(ruc_val):
    ruc = str(ruc_val).strip() if ruc_val else ''
    if not ruc or ruc in ('None', 'nan', ''):
        return []
    fuentes = []
    if ruc in rucs_sispac:
        fuentes.append('SISPAC')
    if ruc in SUNAT_API_RUCS:
        fuentes.append('SUNAT API')
    return fuentes

fuentes_stats = {}
total = 0

# min_row=6: fila 5 es header, datos arrancan en fila 6
# min_row=6: fila 5 es header, datos arrancan en fila 6
for excel_row_num in range(6, ws.max_row + 1):
    ruc_val = rucs_por_fila.get(excel_row_num, '')
    total += 1

    # Detectar fuentes basadas en flags de celda
    flags_fuentes = []
    pac_val       = ws.cell(excel_row_num, col_pac).value     if col_pac      else None
    mid_val       = ws.cell(excel_row_num, col_midagri).value  if col_midagri  else None
    cenacoop_val  = ws.cell(excel_row_num, col_cenacoop).value if col_cenacoop else None
    cen_val       = ws.cell(excel_row_num, col_cen).value      if col_cen      else None

    # PAC: booleano True
    if pac_val is True:
        flags_fuentes.append('PAC')
    # MIDAGRI: booleano True
    if mid_val is True:
        flags_fuentes.append('MIDAGRI')
    # CENACOOP (actual): booleano True
    if cenacoop_val is True:
        flags_fuentes.append('CENACOOP')
    # CENCOOP 2017: string SI
    if cen_val and str(cen_val).strip().upper() in ('SI', 'SÍ'):
        flags_fuentes.append('CENCOOP 2017')

    # Detectar por RUC en bases cruzadas
    ruc_fuentes = detectar_fuentes(ruc_val)

    # Detectar por RUC
    ruc_fuentes = detectar_fuentes(ruc_val)

    # Combinar sin duplicados
    todas = []
    for f in flags_fuentes + ruc_fuentes:
        if f not in todas:
            todas.append(f)

    fuente_txt = '; '.join(todas) if todas else '—'

    # Contar stats
    for f in todas:
        fuentes_stats[f] = fuentes_stats.get(f, 0) + 1
    if not todas:
        fuentes_stats['sin fuente'] = fuentes_stats.get('sin fuente', 0) + 1

    # Escribir en la nueva columna FUENTE (col_ruc = 1)
    ws.cell(excel_row_num, col_ruc).value = fuente_txt

# ─────────────────────────────────────────────────────────────────────────────
# 5. Header de la nueva columna
# ─────────────────────────────────────────────────────────────────────────────
header_cell = ws.cell(row=4, column=col_ruc)
header_cell.value = 'FUENTE'
print()
print('Estadísticas de fuentes:')
for k, v in sorted(fuentes_stats.items(), key=lambda x: -x[1]):
    pct = v / total * 100
    print(f'  {k}: {v} orgs ({pct:.0f}%)')
print(f'  Total filas procesadas: {total}')

# ─────────────────────────────────────────────────────────────────────────────
# 6. Estilar la columna FUENTE
# ─────────────────────────────────────────────────────────────────────────────
FUENTE_FILLS = {
    'PAC':          PatternFill('solid', fgColor='1565C0'),
    'MIDAGRI':      PatternFill('solid', fgColor='2E7D32'),
    'CENACOOP':     PatternFill('solid', fgColor='00695C'),
    'CENCOOP 2017': PatternFill('solid', fgColor='6A1B9A'),
    'SISPAC':       PatternFill('solid', fgColor='AD1457'),
    'SUNAT API':    PatternFill('solid', fgColor='AD1457'),
    '—':            PatternFill('solid', fgColor='F5F5F5'),
}
THIN = Side(style='thin', color='BDBDBD')
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
CENTER = Alignment(horizontal='center', vertical='center', wrap_text=True)

# Header
hcell = ws.cell(row=4, column=col_ruc)
hcell.fill      = PatternFill('solid', fgColor='37474F')
hcell.font      = Font(color='FFFFFF', bold=True, size=9)
hcell.border    = BORDER
hcell.alignment = CENTER

# Data rows
for row in ws.iter_rows(min_row=5, max_row=ws.max_row):
    c = row[col_ruc]
    c.border    = BORDER
    c.alignment = CENTER
    fuentes_str  = str(c.value or '—')
    primer_fuente = fuentes_str.split(';')[0].strip()
    fill = FUENTE_FILLS.get(primer_fuente, FUENTE_FILLS['—'])
    c.fill = fill
    c.font = Font(color='FFFFFF', size=8, bold=True) if primer_fuente != '—' \
             else Font(color='333333', size=8)

ws.column_dimensions[get_column_letter(col_ruc)].width = 30

# ─────────────────────────────────────────────────────────────────────────────
# 7. Guardar
# ─────────────────────────────────────────────────────────────────────────────
wb.save(PATH_OUT)
print()
print(f'Guardado: {PATH_OUT}')
print(f'Pestañas: {wb.sheetnames}')
