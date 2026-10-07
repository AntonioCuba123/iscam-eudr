import openpyxl
from openpyxl import load_workbook

wb6 = load_workbook('C:/Users/acuba/eudrperu/MATRIZ_IP_IV_v6_EUDRPERU.xlsx', data_only=True)
ws6 = wb6['MATRIZ']

print('=== Headers (row 1) ===')
for cell in ws6[1]:
    if cell.value is not None:
        print(f'  col {cell.column_letter}({cell.column}): {repr(str(cell.value)[:60])}')

print()
print('=== Data rows 2-5 ===')
for r in range(2, 6):
    print(f'--- Row {r} ---')
    for cell in ws6[r]:
        v = str(cell.value)[:70] if cell.value is not None else 'EMPTY'
        print(f'  col {cell.column_letter}({cell.column}): {v}')

wb6.close()
