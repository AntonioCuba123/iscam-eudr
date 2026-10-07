import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter

wb = openpyxl.load_workbook('C:/Users/acuba/eudrperu/MATRIZ_IP_IV_v12_EUDRPERU.xlsx')
ws = wb['MATRIZ']

max_row = ws.max_row
print(f'Datos: {max_row - 5} orgs, cols existentes: {ws.max_column}')

# ISA_proxy (col BD=56): geométrica de D1-D7 todas = 0 => =0 siempre
# IP_proxy  (col BE=57): (T/30 + P/500) / 2   — años oper / 30  +  socios / 500
# IV_proxy  (col BF=58): (cert*1 + FOB/10000) ^ 0.5

header_fill = PatternFill('solid', fgColor='1F497D')
header_font = Font(name='Calibri', size=10, bold=True, color='FFFFFF')
fuente_fill = PatternFill('solid', fgColor='D9E1F2')
fuente_font = Font(name='Calibri', size=8, italic=True, color='333333')
formula_fill = PatternFill('solid', fgColor='E2EFDA')
formula_font = Font(name='Calibri', size=10)
align_center = Alignment(horizontal='center', vertical='center')
align_wrap   = Alignment(horizontal='center', vertical='center', wrap_text=True)

# Fórmulas — {r} se reemplaza por el número de fila
formulas = {
    'BD': {
        'nombre': 'ISA_proxy',
        'fuente_txt': 'ISA_proxy  |  PROXY: aprox. desde fuentes admin  |  NO es ISCAM real  |  2026',
        # D1-D7 todas sin dato => geométrica = 0
        'formula': '=0',
    },
    'BE': {
        'nombre': 'IP_proxy',
        'fuente_txt': 'IP_proxy  |  PROXY: aprox. desde fuentes admin  |  NO es ISCAM real  |  2026',
        # IP = (T/30 + P/500) / 2 — años oper y socios normalizados
        # T = años oper, P = n socios
        'formula': '=IFERROR((IF(ISNUMBER(T{r}),MIN(T{r}/30,1),0)+IF(ISNUMBER(P{r}),MIN(P{r}/500,1),0))/2,0)',
    },
    'BF': {
        'nombre': 'IV_proxy',
        'fuente_txt': 'IV_proxy  |  PROXY: aprox. desde fuentes admin  |  NO es ISCAM real  |  2026',
        # IV = (certificado*1 * FOB/10000)^0.5 — certificación y FOB
        # U = cert PAC, V = cert presente, L = FOB 2024
        'formula': '=IFERROR(IF(OR(U{r}<>"",V{r}="SÍ"),IF(ISNUMBER(L{r}),(1*MIN(L{r}/10000,1))^0.5,0),IF(ISNUMBER(L{r}),(0*MIN(L{r}/10000,1))^0.5,0)),0)',
    },
}

for col_letter, data in formulas.items():
    # Header fila 4
    h = ws[col_letter + '4']
    h.value = data['nombre']
    h.font = header_font
    h.fill = header_fill
    h.alignment = align_center

    # Fuente fila 5
    f5 = ws[col_letter + '5']
    f5.value = data['fuente_txt']
    f5.font = fuente_font
    f5.fill = fuente_fill
    f5.alignment = align_wrap

    # Fórmulas filas 6+
    for r in range(6, max_row + 1):
        cell = ws[col_letter + str(r)]
        formula = data['formula'].replace('{r}', str(r))
        cell.value = formula
        cell.font = formula_font
        cell.fill = formula_fill
        cell.alignment = align_center
        cell.number_format = '0.000'

ws.row_dimensions[4].height = 18
ws.row_dimensions[5].height = 40

wb.save('C:/Users/acuba/eudrperu/MATRIZ_IP_IV_v13_EUDRPERU.xlsx')
print(f'Guardado v13 OK — max col: {ws.max_column} ({get_column_letter(ws.max_column)})')

# Muestra fórmulas de fila 6
for col in ['BD', 'BE', 'BF']:
    print(f'  {col}4: {ws[col+"4"].value}')
    print(f'  {col}6: {ws[col+"6"].value}')
