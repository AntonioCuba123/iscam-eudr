"""
Build v8: integra datos SISPAC 20 (Archivo1) en MATRIZ_IP_IV_v7_EUDRPERU.xlsx
Nueva pestaña SISPAC VENTAS — 76 orgs con dato, resto vacío.
"""
import pandas as pd
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import warnings
warnings.filterwarnings('ignore')

PATH_A1 = (
    r'C:\Users\acuba\.minimax\v2\assets\2026\09\18'
    r'\12-31-56-449-asset_20260918-123156-449_b797e5d1c8cd_bc2f6481'
    r'-cf948520-5739-4d82-8952-b9f7974eaf3c_06260002713402 (1).xlsx'
)
PATH_IN  = r'C:\Users\acuba\eudrperu\MATRIZ_IP_IV_v7_EUDRPERU.xlsx'
PATH_OUT = r'C:\Users\acuba\eudrperu\MATRIZ_IP_IV_v8_EUDRPERU.xlsx'

# ─────────────────────────────────────────────────────────────────────────────
# 1. Cargar A1 y extraer RUCs
# ─────────────────────────────────────────────────────────────────────────────
raw = pd.read_excel(PATH_A1, header=None)
data = raw.iloc[3:].copy()
data.columns = [f'C{i}' for i in range(data.shape[1])]
años_row   = raw.iloc[2]
grupos_row = raw.iloc[1]

# Limpiar RUC
data['RUC'] = data['C112'].astype(str).str.strip()
data = data[data['RUC'].str.match(r'^20\d{9}$', na=False)].copy()
data['RUC'] = data['RUC'].str[:11]

# ─────────────────────────────────────────────────────────────────────────────
# 2. Columnas de venta — especificadas manualmente tras análisis
# ─────────────────────────────────────────────────────────────────────────────
# Estructura: col 56 = totales 2018, luego series 2019-2025 con sub-cols
# Primer valor de cada col = nombre de variable
VENTAS_COLS = {
    # VENTAS TOTALES
    'Ventas Totales 2018':      56,
    'Ventas Totales 2019':      59,
    'Ventas Totales 2020':      64,
    'Ventas Totales 2021':      69,
    'Ventas Totales 2022':      74,
    'Ventas Totales 2023':      79,
    'Ventas Totales 2024':      84,
    'Ventas Totales 2025':      90,
    # V. EJEC (ventas ejecutadas) — solo 2020-2025
    'V. Nac. 2020':            62,
    'V. Exp. 2020':            63,
    'V. Nac. 2021':            67,
    'V. Exp. 2021':            68,
    'V. Nac. 2022':            72,
    'V. Exp. 2022':            73,
    'V. Nac. 2023':            77,
    'V. Exp. 2023':            78,
    'V. Nac. 2024':            82,
    'V. Exp. 2024':            83,
    'V. Nac. 2025':            88,
    'V. Exp. 2025':            89,
    # Comprobantes 2023
    'Boleta 2023':             93,
    'Declaración Jurada 2023':  94,
    'Factura 2023':            96,
    'Guía Remisión 2023':      97,
    'Liq. Compra 2023':        98,
    'Total Comp. 2023':         99,
    # Comprobantes 2024
    'Boleta 2024':             100,
    'Declaración Jurada 2024': 101,
    'Factura 2024':            102,
    'Guía Remisión 2024':      103,
    'Liq. Compra 2024':        104,
    'Total Comp. 2024':         105,
    # Comprobantes 2025
    'Boleta 2025':             106,
    'Declaración Jurada 2025': 107,
    'Factura 2025':            108,
    'Guía Remisión 2025':      109,
    'Liq. Compra 2025':        110,
    'Total Comp. 2025':         111,
}

# Verificar que todas existan
ok = all(0 <= v < data.shape[1] for v in VENTAS_COLS.values())
print(f'Columnas SISPAC verificadas: {ok} ({len(VENTAS_COLS)} vars)')

# ─────────────────────────────────────────────────────────────────────────────
# 3. Leer RUCs de v7 (MATRIZ, headers en row 4, datos desde row 5)
# ─────────────────────────────────────────────────────────────────────────────
wb_in  = openpyxl.load_workbook(PATH_IN)
wb_out = openpyxl.load_workbook(PATH_IN)

matriz_ws = wb_in['MATRIZ']
headers_r4 = [cell.value for cell in matriz_ws[4]]
col_ruc    = next((i for i, h in enumerate(headers_r4) if h and str(h).strip().upper() == 'RUC'), 0)
col_nombre = next((i for i, h in enumerate(headers_r4) if 'NOMBRE' in str(h).upper()), 1)
print(f'MATRIZ: RUC col[{col_ruc}], Nombre col[{col_nombre}]')

v7_rucs = {}
for row in matriz_ws.iter_rows(min_row=5, values_only=True):
    ruc = str(row[col_ruc]).strip() if row[col_ruc] else ''
    nom = str(row[col_nombre]).strip() if row[col_nombre] else ''
    if ruc and ruc not in ('None', 'nan', ''):
        v7_rucs[ruc] = nom

print(f'Org en v7: {len(v7_rucs)}')

# ─────────────────────────────────────────────────────────────────────────────
# 4. Construir DataFrame SISPAC
# ─────────────────────────────────────────────────────────────────────────────
sispac_rows = []
for ruc, nombre in v7_rucs.items():
    match = data[data['RUC'] == ruc]
    row_dict = {'RUC': ruc, 'NOMBRE': nombre}
    if match.shape[0] > 0:
        m = match.iloc[0]
        row_dict['PRODUCTO_DOM']  = m['C1']
        row_dict['DEPARTAMENTO']  = m['C5']
        row_dict['PROVINCIA']      = m['C6']
        row_dict['DISTRITO']       = m['C7']
        for var_name, col_i in VENTAS_COLS.items():
            val = m.iloc[col_i]
            # Filtrar #REF! y errores
            if isinstance(val, str) and val.startswith('#'):
                val = None
            row_dict[var_name] = val if pd.notna(val) and val != '' else None
    sispac_rows.append(row_dict)

df = pd.DataFrame(sispac_rows)
print(f'Filas: {len(df)}')
print(f'Con Ventas Totales 2025: {df["Ventas Totales 2025"].notna().sum()}')

# ─────────────────────────────────────────────────────────────────────────────
# 5. Escribir pestaña SISPAC VENTAS
# ─────────────────────────────────────────────────────────────────────────────
if 'SISPAC VENTAS' in wb_out.sheetnames:
    del wb_out['SISPAC VENTAS']
ws = wb_out.create_sheet('SISPAC VENTAS')

# ── Estilos ──
GREEN_DARK  = PatternFill('solid', fgColor='1F5C2E')
GREEN_MED   = PatternFill('solid', fgColor='2E7D32')
GREEN_LIGHT = PatternFill('solid', fgColor='C8E6C9')
WHITE       = PatternFill('solid', fgColor='FFFFFF')
BLUE_GROUP  = PatternFill('solid', fgColor='1565C0')
BLUE_LIGHT  = PatternFill('solid', fgColor='E3F2FD')
GRAY_LIGHT  = PatternFill('solid', fgColor='F5F5F5')

HFONT = Font(color='FFFFFF', bold=True, size=9)
BFONT = Font(size=9)
BFONT_BOLD = Font(bold=True, size=9)

THIN = Side(style='thin', color='BDBDBD')
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
CENTER = Alignment(horizontal='center', vertical='center', wrap_text=True)
LEFT   = Alignment(horizontal='left',   vertical='center', wrap_text=True)
RIGHT  = Alignment(horizontal='right',  vertical='center')

# ── Row 1: título ──
ncols = len(df.columns)
ws.merge_cells(f'A1:{get_column_letter(ncols)}1')
c = ws['A1']
c.value = 'EUDR PERÚ — Datos de Venta SISPAC 20 (PA) | Cobertura: 76 orgs con dato SISPAC | Resto vacío → completar con Instrumento 2'
c.fill = GREEN_DARK
c.font = Font(color='FFFFFF', bold=True, size=10)
c.alignment = CENTER
ws.row_dimensions[1].height = 24

# ── Row 2: grupos de columnas (secciones) ──
ws.row_dimensions[2].height = 20
SECTION_COLS = {
    'RUC | NOMBRE | PRODUCTO': range(1, 5),          # cols 1-4
    'VENTAS TOTALES (S/)':    range(5, 13),           # cols 5-12
    'V. EJEC. NACIONALES (S/)': range(13, 21),        # cols 13-20
    'V. EJEC. EXPORTACIÓN (S/)': range(21, 29),       # cols 21-28
    'COMPROBANTES 2023':       range(29, 35),          # cols 29-34
    'COMPROBANTES 2024':       range(35, 41),         # cols 35-40
    'COMPROBANTES 2025':       range(41, 47),         # cols 41-46
}
SEC_COLORS = ['1565C0','1F5C2E','2E7D32','00695C','E65100','6A1B9A','AD1457']
sec_idx = 0
for sec_name, col_range in SECTION_COLS.items():
    if col_range.start < ncols:
        end_col = min(col_range.stop - 1, ncols)
        ws.merge_cells(
            start_row=2, start_column=col_range.start,
            end_row=2,   end_column=end_col
        )
        c = ws.cell(row=2, column=col_range.start)
        c.value = sec_name
        c.fill = PatternFill('solid', fgColor=SEC_COLORS[sec_idx % len(SEC_COLORS)])
        c.font = Font(color='FFFFFF', bold=True, size=9)
        c.alignment = CENTER
    sec_idx += 1

# ── Row 3: headers ──
ws.row_dimensions[3].height = 36
IDENT_COLS  = {'RUC','NOMBRE','PRODUCTO_DOM','DEPARTAMENTO','PROVINCIA','DISTRITO'}
NUM_COLS    = set(df.columns) - IDENT_COLS
for ci, col_name in enumerate(df.columns, start=1):
    c = ws.cell(row=3, column=ci, value=col_name)
    c.fill   = GREEN_MED
    c.font   = HFONT
    c.border = BORDER
    c.alignment = CENTER

# ── Data rows ──
for ri, (_, row_data) in enumerate(df.iterrows(), start=4):
    fill = GREEN_LIGHT if ri % 2 == 0 else WHITE
    ws.row_dimensions[ri].height = 16
    for ci, col_name in enumerate(df.columns, start=1):
        val = row_data[col_name]
        c = ws.cell(row=ri, column=ci, value=val if pd.notna(val) else None)
        c.fill   = fill
        c.border = BORDER
        if col_name in IDENT_COLS:
            c.alignment = LEFT
            c.font = BFONT_BOLD if col_name == 'NOMBRE' else BFONT
        else:
            c.alignment = RIGHT
            c.font = BFONT
        if isinstance(val, (int, float)) and pd.notna(val):
            c.number_format = '#,##0'

# ── Anchos de columna ──
for ci, col_name in enumerate(df.columns, start=1):
    w = {'RUC': 15, 'NOMBRE': 46, 'PRODUCTO_DOM': 14,
         'DEPARTAMENTO': 16, 'PROVINCIA': 18, 'DISTRITO': 20}.get(col_name, 14)
    ws.column_dimensions[get_column_letter(ci)].width = w

ws.freeze_panes = 'A4'

# ─────────────────────────────────────────────────────────────────────────────
# 6. Guardar
# ─────────────────────────────────────────────────────────────────────────────
wb_out.save(PATH_OUT)

# ── Resumen ──
con_dato = (df['Ventas Totales 2025'].notna()).sum()
print()
print(f'✅ Guardado: {PATH_OUT}')
print(f'   Pestañas: {wb_out.sheetnames}')
print(f'   Org con dato Ventas Totales 2025: {con_dato} / {len(df)}')
print()
print('Distribución de ventas 2025:')
s = df['Ventas Totales 2025'].dropna().astype(float).describe()
print(s.to_string())
