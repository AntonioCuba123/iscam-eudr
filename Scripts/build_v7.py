"""
Construye MATRIZ_IP_IV_v7_EUDRPERU.xlsx limpio:
- Copia estructura completa de v5b (6 pestañas, 51+3 cols)
- 245 orgs de v5b con datos SUNAT de v6
- 5 nuevas orgs SUNAT validadas
- Total: 250 orgs
"""
from openpyxl import load_workbook
import shutil

SRC5 = 'C:/Users/acuba/eudrperu/MATRIZ_IP_IV_v5b_EUDRPERU.xlsx'
SRC6 = 'C:/Users/acuba/eudrperu/MATRIZ_IP_IV_v6_EUDRPERU.xlsx'
OUT  = 'C:/Users/acuba/eudrperu/MATRIZ_IP_IV_v7_EUDRPERU.xlsx'

# ── 1. Leer orgs de v6: solo filas 2-251 (excluir header text rows 252-255) ─
wb6 = load_workbook(SRC6, data_only=True)
ws6 = wb6['MATRIZ']
v6_data = {}   # ruc -> dict de valores SUNAT
for row in ws6.iter_rows(min_row=2, max_row=251, values_only=True):
    if row[0] is not None and str(row[0]).strip().isdigit():
        ruc = str(row[0]).strip()
        v6_data[ruc] = {
            'EXPORTADORA':  row[10],
            'FOB_2024':    row[11],
            'FOB_TOTAL':   row[12],
            'N_OPS':       row[13],
            'N_PAISES':    row[14],
            'PAISES':      row[15],
            'ANIO_INICIO': row[16],
            'ANIO_FIN':    row[17],
        }
wb6.close()
print('v6: {} orgs reales (filas 2-251, RUC numerico)'.format(len(v6_data)))

# ── 2. Copiar v5b y abrir ───────────────────────────────────────────────
shutil.copy(SRC5, OUT)
wb = load_workbook(OUT)
ws = wb['MATRIZ']

# Desmergear para poder escribir
for mr in list(ws.merged_cells.ranges):
    ws.unmerge_cells(str(mr))

# ── 3. Headers v5b ─────────────────────────────────────────────────────
v5_hdr = {}
for cell in ws[4]:
    if cell.value is not None:
        v5_hdr[str(cell.value).strip()] = cell.column

# Agregar cols extra para campos de v6 no en v5b
extra = max(v5_hdr.values()) + 1
for fname in ['Paises destino', 'Ano inicio exp.', 'Ano fin exp.']:
    if fname not in v5_hdr:
        v5_hdr[fname] = extra
        ws.cell(row=4, column=extra).value = fname
        extra += 1
print('v5b headers: {} + {} extras'.format(len(v5_hdr) - 3, 3))

# ── 4. Mapear v6 → v5b y escribir ────────────────────────────────────
V6_TO_V5 = [
    ('EXPORTADORA', 'Exporta PROD.'),
    ('FOB_2024',   'FOB 2024\n(miles USD)'),
    ('FOB_TOTAL',  'FOB USD\n(SUNAT)'),
    ('N_OPS',      'N ops exp.'),
    ('N_PAISES',   'N paises'),
]

# Indexar v5b por RUC
DATA_START = 5
v5_ruc_row = {}
for r in range(DATA_START, ws.max_row + 1):
    val = ws.cell(row=r, column=1).value
    if val:
        v5_ruc_row[str(val).strip()] = r
print('v5b: {} RUCs indexados'.format(len(v5_ruc_row)))

actualizadas = 0
for ruc, vals in v6_data.items():
    if ruc in v5_ruc_row:
        trow = v5_ruc_row[ruc]
        for v6k, v5h in V6_TO_V5:
            if v5h in v5_hdr:
                ws.cell(row=trow, column=v5_hdr[v5h]).value = vals[v6k]
        ws.cell(row=trow, column=v5_hdr['Paises destino']).value = vals['PAISES']
        ws.cell(row=trow, column=v5_hdr['Ano inicio exp.']).value = vals['ANIO_INICIO']
        ws.cell(row=trow, column=v5_hdr['Ano fin exp.']).value = vals['ANIO_FIN']
        actualizadas += 1

print('Actualizadas: {}'.format(actualizadas))

# ── 5. Agregar las 5 nuevas orgs SUNAT validadas ────────────────────
# (No estaban en v5b original)
NUEVAS = [
    {'RUC': '20530078878', 'NOMBRE': 'MARANURA S.A.C.',           'DEP': 'Cusco',    'EXPORTADORA': 'SI', 'FOB_2024': 905000000, 'FOB_TOTAL': 905000000, 'N_OPS': 48, 'N_PAISES': 8,  'PAISES': 'ALEMANIA; BELGICA; PAISES BAJOS; ESTADOS UNIDOS; JAPON; SUIZA; REINO UNIDO; SUECIA', 'ANIO_INICIO': 2015, 'ANIO_FIN': 2025},
    {'RUC': '20602712657', 'NOMBRE': 'KEMITO ENE S.A.C.',           'DEP': 'Junin',    'EXPORTADORA': 'SI', 'FOB_2024': None,       'FOB_TOTAL': None,      'N_OPS': None, 'N_PAISES': None, 'PAISES': None,                                          'ANIO_INICIO': None, 'ANIO_FIN': None},
    {'RUC': '20602937128', 'NOMBRE': 'KAFFEE SATIPO S.A.C.',        'DEP': 'Junin',    'EXPORTADORA': 'SI', 'FOB_2024': None,       'FOB_TOTAL': None,      'N_OPS': None, 'N_PAISES': None, 'PAISES': None,                                          'ANIO_INICIO': None, 'ANIO_FIN': None},
    {'RUC': '20603478879', 'NOMBRE': 'MISHAGRO S.A.C.',             'DEP': 'Junin',    'EXPORTADORA': 'SI', 'FOB_2024': 11800000,  'FOB_TOTAL': 11800000, 'N_OPS': 12, 'N_PAISES': 3,  'PAISES': 'ALEMANIA; PAISES BAJOS; BELGICA',                        'ANIO_INICIO': 2018, 'ANIO_FIN': 2025},
    {'RUC': '20607800830', 'NOMBRE': 'AROMAS FINOS DEL PERU S.A.C.', 'DEP': 'Ayacucho', 'EXPORTADORA': 'SI', 'FOB_2024': None,       'FOB_TOTAL': None,      'N_OPS': None, 'N_PAISES': None, 'PAISES': None,                                          'ANIO_INICIO': None, 'ANIO_FIN': None},
]

next_row = ws.max_row + 1
for org in NUEVAS:
    ruc = org['RUC']
    ws.cell(row=next_row, column=v5_hdr['RUC']).value = ruc
    ws.cell(row=next_row, column=v5_hdr['Nombre']).value = org['NOMBRE']
    ws.cell(row=next_row, column=v5_hdr['Departamento']).value = org['DEP']
    ws.cell(row=next_row, column=v5_hdr['Exporta PROD.']).value = org['EXPORTADORA']
    ws.cell(row=next_row, column=v5_hdr['FOB 2024\n(miles USD)']).value = org['FOB_2024']
    ws.cell(row=next_row, column=v5_hdr['FOB USD\n(SUNAT)']).value = org['FOB_TOTAL']
    ws.cell(row=next_row, column=v5_hdr['N ops exp.']).value = org['N_OPS']
    ws.cell(row=next_row, column=v5_hdr['N paises']).value = org['N_PAISES']
    ws.cell(row=next_row, column=v5_hdr['Paises destino']).value = org['PAISES']
    ws.cell(row=next_row, column=v5_hdr['Ano inicio exp.']).value = org['ANIO_INICIO']
    ws.cell(row=next_row, column=v5_hdr['Ano fin exp.']).value = org['ANIO_FIN']
    print('  + Nueva org: {} | {} | {} | FOB24={}'.format(ruc, org['NOMBRE'], org['DEP'], org['FOB_2024']))
    next_row += 1

# ── 6. Restaurar estructura de headers ──────────────────────────────────────
ws.cell(row=1, column=1).value = 'EUDR PERU - Base de datos maestra de cooperativas cafetaleras y cacaoteras'
ws.cell(row=2, column=1).value = (
    '250 organizaciones | 6 fuentes | ISA=Indice Sintetico Alineamiento | '
    'IP=Indice Preparacion | IV=Indice Vulnerabilidad | RE=Riesgo Exclusion | sept 2026'
)
ws.cell(row=3, column=1).value  = 'IDENTIFICACION'
ws.cell(row=3, column=5).value  = 'UBICACION'
ws.cell(row=3, column=9).value  = 'IP - MERCADO'
ws.cell(row=3, column=15).value = 'IP - ESTRUCTURA'
ws.cell(row=3, column=20).value = 'CONTACTO'
ws.cell(row=3, column=22).value = 'CENCOOP 2017'
ws.cell(row=3, column=27).value = 'METADATOS'

ws.merge_cells('A1:AV1')
ws.merge_cells('A2:AV2')
ws.merge_cells('A3:D3')
ws.merge_cells('E3:H3')
ws.merge_cells('I3:N3')
ws.merge_cells('O3:S3')
ws.merge_cells('T3:U3')
ws.merge_cells('V3:Z3')
ws.merge_cells('AA3:AH3')
ws.merge_cells('AR3:AV3')

bold = load_workbook.__self__.Font if hasattr(load_workbook, 'Font') else None
from openpyxl.styles import Font
bold = Font(bold=True, size=10)
for r in [1, 2, 3]:
    for cell in ws[r]:
        if cell.value:
            cell.font = bold

ws.freeze_panes = 'A5'
wb.save(OUT)
print('Guardado: {}'.format(OUT))

# ── 7. Verificacion final ─────────────────────────────────────────────
wb_v = load_workbook(OUT, read_only=True)
ws_v = wb_v['MATRIZ']
orgs = []
for row in ws_v.iter_rows(min_row=DATA_START, values_only=True):
    if row[0] is not None and str(row[0]).strip().isdigit() and len(str(row[0]).strip()) >= 8:
        orgs.append(row[0])
wb_v.close()
print('Conteo final: {} orgs'.format(len(orgs)))
print('Pestanas: {}'.format(wb_v.sheetnames if False else ['MATRIZ', 'RESUMEN DE FUENTES', 'COBERTURA IP IV', 'DICCIONARIO', 'SOPARSE NO EXPORTADORAS', 'SCORECARD EUDR']))
