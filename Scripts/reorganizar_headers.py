import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter
import shutil, copy

shutil.copy('C:/Users/acuba/eudrperu/MATRIZ_IP_IV_v16_EUDRPERU.xlsx',
            'C:/Users/acuba/eudrperu/MATRIZ_IP_IV_v17_EUDRPERU.xlsx')

wb = openpyxl.load_workbook('C:/Users/acuba/eudrperu/MATRIZ_IP_IV_v17_EUDRPERU.xlsx')
ws = wb['MATRIZ']

# Estado actual tras insert_rows(1):
# Fila 1: Titulo
# Fila 2: vacia (separador)
# Fila 3: vacia (separador)
# Fila 4: VACIA (deberia tener headers)
# Fila 5: headers (RUC, Nombre...)  <- AL REVES
# Fila 6: fuente (SUNAT_API..., MIDAGRI...)  <- AL REVES
# Fila 7: vacia
# Fila 8+: DATOS (formulas correctas)

# Solucion: swap filas 4 y 5
# - Copiar headers de fila 5 a fila 4
# - Poner fuente en fila 5
# - Dejar fila 6 vacia
# - Fila 7+ = datos

# Paso 1: Copiar headers de fila 5 a fila 4
header_font = Font(name='Calibri', size=10, bold=True)
for col_num in range(1, ws.max_column + 1):
    src = ws.cell(5, col_num)
    dst = ws.cell(4, col_num)
    if src.value is not None:
        # Copiar valor (string de header)
        dst.value = src.value
        dst.font = header_font
    else:
        dst.value = None

# Paso 2: Rellenar fuente en fila 5 con el mapeo completo
fuentes_map = {
    'A': '—', 'B': 'SUNAT_API_identidad-fiscal (validacion RUC)  |  2026',
    'C': 'SUNAT_API_identidad-fiscal  |  2026',
    'D': 'PRODUCE_2_Matriz_informacion_Estudios_economicos_29.05.2023  |  2023',
    'E': 'SUNAT_API_identidad-fiscal  |  2026',
    'F': 'SUNAT_API_identidad-fiscal  |  2026',
    'G': 'MIDAGRI_reg-nacional-cooperativas-agrarias-260226  |  2026',
    'H': 'Directorio_PAC_Cepicafe-Norandino  |  2024',
    'I': 'Directorio_PAC_Cepicafe-Norandino  |  2024',
    'J': 'PRODUCE_2_Matriz_informacion_Estudios_economicos_29.05.2023  |  2023',
    'K': 'PRODUCE_2_Matriz_informacion_Estudios_economicos_29.05.2023  |  2023',
    'L': 'PRODUCE_2_Matriz_informacion_Estudios_economicos_29.05.2023  |  2023',
    'M': 'SUNAT_exportaciones_2010_2025  |  2010-2025',
    'N': 'PRODUCE_2_Matriz_informacion_Estudios_economicos_29.05.2023  |  2023',
    'O': 'PRODUCE_2_Matriz_informacion_Estudios_economicos_29.05.2023  |  2023',
    'P': 'MIDAGRI_reg-nacional-cooperativas-agrarias-260226  |  2026',
    'Q': 'MIDAGRI_reg-nacional-cooperativas-agrarias-260226  |  2026',
    'R': 'CENACOOP_fusion_EUDR (data2024_ventas_prom_soles)  |  2024',
    'S': 'MIDAGRI_reg-nacional-cooperativas-agrarias-260226  |  2026',
    'T': 'MIDAGRI_reg-nacional-cooperativas-agrarias-260226 / CENCOOP_2017  |  2026',
    'U': 'Directorio_PAC_Cepicafe-Norandino  |  2024',
    'V': 'Validacion_propia (cruce PAC+PRODUCE)  |  2026',
    'W': 'MIDAGRI_reg-nacional-cooperativas-agrarias-260226  |  2026',
    'X': 'MIDAGRI_reg-nacional-cooperativas-agrarias-260226  |  2026',
    'Y': 'MIDAGRI_reg-nacional-cooperativas-agrarias-260226 / SUNAT_API  |  2026',
    'Z': 'MIDAGRI_reg-nacional-cooperativas-agrarias-260226 / SUNAT_API  |  2026',
    'AA': 'Directorio_PAC_Cepicafe-Norandino  |  2024',
    'AB': 'MIDAGRI_reg-nacional-cooperativas-agrarias-260226  |  2026',
    'AC': 'CENACOOP_fusion_EUDR  |  2026',
}
# Completar CENCOOP 2017 para AD-BC
for col_letter in ['AD','AE','AF','AG','AH','AI','AJ','AK','AL','AM','AN','AO','AP','AQ','AR','AS','AT','AU','AV','AW','AX']:
    fuentes_map[col_letter] = 'CENCOOP_2017  |  2017'
fuentes_map['AY'] = '—concat_propio  |  —'
fuentes_map['AZ'] = '—concat_propio  |  —'
for col_letter in ['BA','BB','BC']:
    fuentes_map[col_letter] = 'PRODUCE_2_Matriz_informacion_Estudios_economicos_29.05.2023 / SUNAT_exportaciones  |  2023'
fuentes_map['BD'] = 'ISA_proxy: D1-D7=0 sin fuente admin  |  PROXY  |  2026'
fuentes_map['BE'] = 'IP_proxy: (T/30+P/500)/2  |  PROXY: aprox desde fuentes admin — NO es ISCAM real  |  2026'
fuentes_map['BF'] = 'IV_proxy: cert*FOB normalizado  |  PROXY: aprox desde fuentes admin — NO es ISCAM real  |  2026'

def get_fill(archivo):
    if 'CENCOOP_2017' in archivo: return PatternFill('solid', fgColor='FFF2CC')
    elif 'Directorio_PAC' in archivo: return PatternFill('solid', fgColor='DDEEFF')
    elif 'PRODUCE' in archivo: return PatternFill('solid', fgColor='FFE0CC')
    elif 'MIDAGRI' in archivo: return PatternFill('solid', fgColor='E2EFDA')
    elif 'SUNAT' in archivo: return PatternFill('solid', fgColor='FCE4D6')
    elif 'CENACOOP_fusion' in archivo: return PatternFill('solid', fgColor='F4B8C1')
    elif 'Validacion' in archivo: return PatternFill('solid', fgColor='EDEDED')
    elif 'ISA_proxy' in archivo or 'IP_proxy' in archivo or 'IV_proxy' in archivo:
        return PatternFill('solid', fgColor='D9E1F2')
    else: return PatternFill('solid', fgColor='F2F2F2')

fuente_font = Font(name='Calibri', size=8, italic=True, color='444444')
fuente_align = Alignment(horizontal='center', vertical='center', wrap_text=True)

for col_letter, txt in fuentes_map.items():
    cell = ws[col_letter + '5']
    cell.value = txt
    cell.font = fuente_font
    cell.fill = get_fill(txt)
    cell.alignment = fuente_align

# Limpiar fila 6 (quedó vacia tras el swap de originales)
for col_num in range(1, ws.max_column + 1):
    ws.cell(6, col_num).value = None

# Verificar
print('Estructura final:')
for r in range(1, 9):
    vals = [(ws.cell(r, c).column_letter, ws.cell(r, c).value) 
            for c in range(1, 5) if ws.cell(r, c).value]
    print('  Fila ' + str(r) + ': ' + str(vals))
print('Datos:')
print('  Fila 8 - B:', ws['B8'].value, '| C:', ws['C8'].value)
print('  BE8 formula:', ws['BE8'].value)

# Corregir formulas: ahora los datos estan en fila 8, no 7
# Las formulas corrige_formulas_proxy puso refs en fila 7
import re
count = 0
for r in range(8, ws.max_row + 1):
    for col in ['BD', 'BE', 'BF']:
        cell = ws[col + str(r)]
        if cell.value and isinstance(cell.value, str) and cell.value.startswith('='):
            old = cell.value
            def replace_row(m):
                return m.group(1) + str(int(m.group(2)) + 1) + m.group(3)
            new = re.sub(r'(\b[A-Z]+)(\d+)(\b)', replace_row, old)
            if old != new:
                cell.value = new
                count += 1

print('Formulas actualizadas de fila 7 a fila 8: ' + str(count))
print('Datos en fila 8 - B:', ws['B8'].value, '| C:', ws['C8'].value)
print('BE8 formula:', ws['BE8'].value)

wb.save('C:/Users/acuba/eudrperu/MATRIZ_IP_IV_v17_EUDRPERU.xlsx')
print('Guardado v17')
