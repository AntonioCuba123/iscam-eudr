"""
Análisis de overlap entre Archivo1 (PA SISPAC 20) y MATRIZ_IP_IV_v7_EUDRPERU
"""
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

PATH_A1 = (
    r'C:\Users\acuba\.minimax\v2\assets\2026\09\18'
    r'\12-31-56-449-asset_20260918-123156-449_b797e5d1c8cd_bc2f6481'
    r'-cf948520-5739-4d82-8952-b9f7974eaf3c_06260002713402 (1).xlsx'
)
PATH_V7 = r'C:\Users\acuba\eudrperu\MATRIZ_IP_IV_v7_EUDRPERU.xlsx'

# ── Cargar A1 (header en row 3, 0-indexed → skiprows=3) ──
raw = pd.read_excel(PATH_A1, header=None)
data = raw.iloc[3:].copy()
data.columns = [f'col_{i}' for i in range(data.shape[1])]

# Identidad
data = data.rename(columns={
    'col_0': 'NOMBRE',
    'col_1': 'PRODUCTO_DOM',
    'col_4': 'UBIGEO',
    'col_5': 'DEPARTAMENTO',
    'col_112': 'RUC'
})

# RUC limpio (11 dígitos)
data['RUC'] = data['RUC'].astype(str).str.strip()
data['RUC_11'] = data['RUC'].where(data['RUC'].str.len() == 11, None)

# Café / cacao
data['ES_CAFE_CACAO'] = data['PRODUCTO_DOM'].astype(str).str.upper().str.strip().isin(['CAFÉ', 'CACAO'])

# ── Cargar v7 ──
v7_raw = pd.read_excel(PATH_V7, sheet_name='MATRIZ', header=None)
v7 = v7_raw.iloc[4:].copy()
v7.columns = [f'v7_col_{i}' for i in range(v7.shape[1])]
v7 = v7.rename(columns={
    'v7_col_0': 'RUC',
    'v7_col_1': 'NOMBRE_V7',
    'v7_col_2': 'TIPO_PROD',
    'v7_col_4': 'DPTO_V7'
})
v7['RUC'] = v7['RUC'].astype(str).str.strip()

# ── Resumen universo ──
total_a1 = data['NOMBRE'].notna().sum()
cafe_a1 = data[data['ES_CAFE_CACAO']]['NOMBRE'].notna().sum()
rucs_a1 = data['RUC_11'].notna().sum()
total_v7 = v7['NOMBRE_V7'].notna().sum()
rucs_v7 = v7['RUC'].notna().sum()

print('=== UNIVERSOS ===')
print(f'A1 total filas: {total_a1} | Café/Cacao: {cafe_a1} | Con RUC 11d: {rucs_a1}')
print(f'v7 total filas: {total_v7} | Con RUC: {rucs_v7}')

# ── Cruce por RUC ──
a1_rucs = set(data['RUC_11'].dropna())
v7_rucs  = set(v7['RUC'].dropna())
overlap_rucs = a1_rucs & v7_rucs

print()
print('=== CRUCE POR RUC ===')
print(f'A1 RUCs únicos: {len(a1_rucs)}')
print(f'v7 RUCs únicos: {len(v7_rucs)}')
print(f'Overlap (en ambos): {len(overlap_rucs)}')
print(f'Solo en A1: {len(a1_rucs - v7_rucs)}')
print(f'Solo en v7: {len(v7_rucs - a1_rucs)}')

# ── Muestra overlap ──
print()
print('=== MUESTRA OVERLAP (primeros 10) ===')
overlap_list = sorted(list(overlap_rucs))[:10]
for r in overlap_list:
    a1_row = data[data['RUC'] == r].iloc[0]
    v7_row = v7[v7['RUC'] == r].iloc[0]
    print(f'  RUC {r}:')
    print(f'    A1: {a1_row["NOMBRE"][:70]}')
    print(f'    v7: {v7_row["NOMBRE_V7"][:70]}')
    print(f'    A1 producto: {a1_row["PRODUCTO_DOM"]} | v7 tipo: {v7_row["TIPO_PROD"]}')

# ── Variables de venta disponibles en A1 ──
print()
print('=== VARIABLES DE VENTA EN A1 ===')
# Las columnas de venta están en la zona cols ~58-114
# Identificar por grupo de años
for col_i in range(58, 115):
    header_grp = raw.iloc[1, col_i]
    header_yr  = raw.iloc[2, col_i]
    non_null   = raw.iloc[3:, col_i].notna().sum()
    if non_null > 50 and str(header_yr) != 'nan':
        print(f'  col[{col_i}]: grupo={str(header_grp)[:40]} | año={header_yr} | datos={non_null}')
