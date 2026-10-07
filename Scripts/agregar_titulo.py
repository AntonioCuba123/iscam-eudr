import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

wb = openpyxl.load_workbook('C:/Users/acuba/eudrperu/MATRIZ_IP_IV_v14_EUDRPERU.xlsx')
ws = wb['MATRIZ']

# Ver estado actual
print(f'Estado: {ws.max_row} filas, {ws.max_column} columnas')
print(f'Headers en fila 4, datos en fila 6+')

# Insertar UNA fila al inicio (empuja todo: 1->2, 2->3, ..., 4->5, 5->6, 6->7...)
ws.insert_rows(1)
print('Fila insertada. Ahora: titulo=f1, vacia=f2, vacia=f3, headers=f4, fuente=f5, datos=f6+')

# --- TÍTULO en fila 1 ---
# Merge A1:BF1
max_col_letter = get_column_letter(ws.max_column)

titulo_cell = ws['A1']
titulo_cell.value = (
    'EUDR PERÚ — Matriz Maestra de Cooperativas Cafetaleras y Cacaoteras  |  '
    'ISCAM: ISA · IP · IV · RE  |  '
    '258 organizaciones  |  Fuentes: SUNAT · MIDAGRI · PRODUCE · PAC · CENCOOP 2017  |  v14 (sep 2026)'
)

titulo_font = Font(name='Calibri', size=11, bold=True, color='FFFFFF')
titulo_fill = PatternFill('solid', fgColor='1F497D')
titulo_align = Alignment(horizontal='center', vertical='center', wrap_text=True)
titulo_border = Border(
    bottom=Side(style='medium', color='0D3473')
)

titulo_cell.font = titulo_font
titulo_cell.fill = titulo_fill
titulo_cell.alignment = titulo_align
titulo_cell.border = titulo_border

# Aplicar estilo a toda la fila 1 fusionada
for col in range(1, ws.max_column + 1):
    cell = ws.cell(1, col)
    cell.font = titulo_font
    cell.fill = titulo_fill
    cell.alignment = titulo_align
    if col == 1:
        cell.border = Border(
            bottom=Side(style='medium', color='0D3473')
        )

# Merge A1:BF1
ws.merge_cells('A1:' + max_col_letter + '1')
ws.row_dimensions[1].height = 30

# Ajustar fila 2 (vacía, separador)
ws.row_dimensions[2].height = 6

# Ajustar demás filas
ws.row_dimensions[3].height = 6   # separador
ws.row_dimensions[4].height = 28  # headers
ws.row_dimensions[5].height = 40  # fuente

wb.save('C:/Users/acuba/eudrperu/MATRIZ_IP_IV_v14_EUDRPERU.xlsx')
print('Guardado v14 con titulo')

# Verificar
wb2 = openpyxl.load_workbook('C:/Users/acuba/eudrperu/MATRIZ_IP_IV_v14_EUDRPERU.xlsx')
ws2 = wb2['MATRIZ']
print('Fila 1:', ws2['A1'].value[:80] if ws2['A1'].value else 'VACIA')
print('Fila 4 headers (primeros 5):', [ws2.cell(4,c).value for c in range(1,6) if ws2.cell(4,c).value])
print('Fila 6 dato 1 RUC:', ws2['B6'].value, '| Nombre:', ws2['C6'].value)
