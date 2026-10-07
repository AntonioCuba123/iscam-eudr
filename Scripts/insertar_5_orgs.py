"""Insertar 5 orgs validadas por API en la pestaña MATRIZ de la v8."""
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side

PATH_IN  = r'C:\Users\acuba\eudrperu\MATRIZ_IP_IV_v8_EUDRPERU.xlsx'
PATH_OUT = r'C:\Users\acuba\eudrperu\MATRIZ_IP_IV_v8b_EUDRPERU.xlsx'

wb = openpyxl.load_workbook(PATH_IN)
ws = wb['MATRIZ']

last_row = ws.max_row
print(f'Última fila MATRIZ: {last_row}')

# Los 5 RUCs validados por API SUNAT (18/sep/2026)
NUEVAS_ORGS = [
    {
        'ruc': '20132509876', 'nombre': 'COOPERATIVA AGRARIA CAFETALERA MARANURA LTDA. 129',
        'tipo': 'Cooperativa', 'dpto': 'Cusco', 'prov': 'La Convencion',
        'macro_zona': 'Cusco - La Convencion', 'producto': 'Cafe',
        'nota': 'Validado API SUNAT 18/sep/2026 | Ubigeo 080904 | La Convencion, Cusco',
    },
    {
        'ruc': '20568190450', 'nombre': 'COOPERATIVA AGRARIA KEMITO ENE LTDA.',
        'tipo': 'Cooperativa', 'dpto': 'Junin', 'prov': 'Satipo',
        'macro_zona': 'Junin - Satipo', 'producto': 'Cafe',
        'nota': 'Validado API SUNAT 18/sep/2026 | Ubigeo 120601 | Satipo, Junin',
    },
    {
        'ruc': '20603557825', 'nombre': 'COOPERATIVA AGRARIA KAFFEE SATIPO',
        'tipo': 'Cooperativa', 'dpto': 'Junin', 'prov': 'Satipo',
        'macro_zona': 'Junin - Satipo', 'producto': 'Cafe',
        'nota': 'Validado API SUNAT 18/sep/2026 | Ubigeo 120601 | Satipo, Junin',
    },
    {
        'ruc': '20603734255', 'nombre': 'COOPERATIVA AGRARIA AGROINDUSTRIAL MISHAGRO',
        'tipo': 'Cooperativa', 'dpto': 'Junin', 'prov': 'Chanchamayo',
        'macro_zona': 'Junin - Chanchamayo', 'producto': 'Cafe',
        'nota': 'Validado API SUNAT 18/sep/2026 | Ubigeo 120303 | Chanchamayo, Junin',
    },
    {
        'ruc': '20609098989', 'nombre': 'COOPERATIVA AGRARIA CAFETALERA AROMAS FINOS DEL PERU',
        'tipo': 'Cooperativa', 'dpto': 'San Martin', 'prov': 'San Martin',
        'macro_zona': 'San Martin', 'producto': 'Cafe',
        'nota': 'Validado API SUNAT 18/sep/2026 | Ubigeo 060801 | San Martin',
    },
]

YELLOW_FILL = PatternFill('solid', fgColor='FFF9C4')
THIN = Side(style='thin', color='BDBDBD')
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
LEFT   = Alignment(horizontal='left', vertical='center', wrap_text=True)
CENTER = Alignment(horizontal='center', vertical='center', wrap_text=True)

insertadas = 0
for org in NUEVAS_ORGS:
    next_row = last_row + 1 + insertadas
    row_vals = [
        org['ruc'],        # 0
        org['nombre'],     # 1
        org['tipo'],       # 2
        None,              # 3 CIIU
        org['dpto'],       # 4
        org['prov'],       # 5
        org['macro_zona'], # 6
        org['producto'],   # 7
        '—',               # 8 Exporta
        'NO',              # 9 FOB>0
        '—',               # 10 FOB 2024
        None,              # 11 FOB SUNAT
        None,              # 12 N ops
        None,              # 13 N paises
        None,              # 14 N socios
        None,              # 15 N trabaj.
        None,              # 16 Ventas prom
        None,              # 17 Ano inscrip.
        None,              # 18 Anios oper.
        None,              # 19 Cert PAC
        '—',               # 20 Cert presente
        None,              # 21 Repre
        org['nota'],       # 22 Cargo/nota
        None,              # 23 Tel
        None,              # 24 Correo
        False,             # 25 En CEPICAFE
        None,              # 26 En MIDAGRI
        None,              # 27 En CENCOOP
        None,              # 28 Flag CENCOOP
        None,              # 29 Razon CENCOOP
        None,              # 30 Dpto CENCOOP
        None,              # 31 Prov CENCOOP
        None,              # 32 Dist CENCOOP
        None,              # 33 CCPP
        None,              # 34 CIIU desc
        None,              # 35 Sector
        None,              # 36 Estado 2017
        None,              # 37 Rango
        None,              # 38 Anios CENCOOP
        None,              # 39 Presidente
        None,              # 40 Gerente prof
        None,              # 41 Gerente edad
        None,              # 42 Web
        None,              # 43 Correo CENCOOP
        None,              # 44 Tel movil
        None,              # 45 Lat
        None,              # 46 Lon
        None,              # 47 Ano constit.
        None,              # 48 Ano inicio oper.
        1,                 # 49 N fuentes
        'sept-2026',       # 50 Ano actualiz
        None,              # 51 Paises
        None,              # 52 Ano inicio exp.
        None,              # 53 Ano fin exp.
    ]
    for ci, val in enumerate(row_vals, start=1):
        c = ws.cell(row=next_row, column=ci, value=val)
        c.fill   = YELLOW_FILL
        c.border = BORDER
        c.font   = Font(bold=(ci == 1), size=9)
        c.alignment = LEFT if ci not in (1, 9, 10, 25, 26, 27, 28) else CENTER
    ws.row_dimensions[next_row].height = 32
    insertadas += 1
    print(f'  Insertada: {org["nombre"][:55]} | RUC {org["ruc"]}')

wb.save(PATH_OUT)
print()
print(f'Ok: {insertadas} orgs insertadas en MATRIZ (filas {last_row+1}-{last_row+insertadas})')
print(f'Archivo: {PATH_OUT}')
print()
print('Resumen validacion API:')
for org in NUEVAS_ORGS:
    print(f'  RUC {org["ruc"]} | {org["nombre"][:55]} | ACTIVO | Ubigeo segun API')
