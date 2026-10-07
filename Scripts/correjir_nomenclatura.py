# -*- coding: utf-8 -*-
"""Corregir terminologia ISCAM en el Excel v5 y guardar como v5b."""
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter

AZUL = '1E3A5F'
AZUL_CLARO = '2563EB'
VERDE = '059669'
VERDE_CLARO = 'D1FAE5'
AMARILLO = 'D97706'
AMARILLO_CLARO = 'FEF3C7'
ROJO = 'DC2626'
BLANCO = 'FFFFFF'
GRIS_LIGHT = 'F3F4F6'

def hdr_fill(h): return PatternFill('solid', fgColor=h)
def thin_border():
    s = Side(style='thin', color='D1D5DB')
    return Border(left=s, right=s, top=s, bottom=s)

wb = openpyxl.load_workbook(r'C:/Users/acuba/eudrperu/MATRIZ_IP_IV_v5_EUDRPERU.xlsx')

# ── 1. MATRIZ: fila de titulo con terminologia correcta ──────────────────
ws = wb['MATRIZ']
ws['A1'] = 'EUDR PERU — Base de datos maestra de cooperativas cafetaleras y cacaoteras'
ws['A2'] = ('245 organizaciones | 6 fuentes | ISA/IP/IV/RE = Instrumento ISCAM '
             '| ISA=Indice Sintetico Alineamiento | IP=Indice Preparacion '
             '| IV=Indice Vulnerabilidad | RE=Riesgo Exclusion | sept 2026')

# ── 2. SCORECARD EUDR: terminologia completa ─────────────────────────────
ws6 = wb['SCORECARD EUDR']
# Fila 1 ya tiene headers D1-D11+ISA+IP+IV
# Cambiar titulo de la nota
ws6['A2'] = (
    'ISCAM: D1-D7 = Instrumento 2 (campo). D8-D9 = IP (Indice Preparacion). '
    'D10-D11 = IV (Indice Vulnerabilidad). ISA = Indice Sintetico Alineamiento. '
    'RE = Riesgo Exclusion (ponderacion AHP). '
    'ISA = geom(D1..D7), IP = media(D8,D9), IV = geom(D10,D11), RE = ponderacion AHP.'
)

# Agregar fila extra con descripcion de cada indice
# Buscar la siguiente fila libre
max_r = ws6.max_row
for r in range(2, max_r + 5):
    if ws6.cell(row=r, column=1).value is None:
        next_r = r
        break

# Headers de explicacion
indice_data = [
    ('ISA', 'Indice Sintetico de Alineamiento', 'geom(D1..D7)', '0.0-1.0', 'Sostenibilidad, due diligence, derechos humanos, traceabilidad, medio ambiente'),
    ('IP', 'Indice de Preparacion', 'media(D8,D9)', '0.0-1.0', 'Anos de operacion, n. socios, capacidad exportar, n. paises destino'),
    ('IV', 'Indice de Vulnerabilidad', 'geom(D10,D11)', '0.0-1.0', 'Certificaciones, volumen FOB, exposicion a EUDR'),
    ('RE', 'Riesgo de Exclusion', 'ponderacion AHP', '0.0-1.0', 'Probabilidad de exclusion del mercado EU por incumplimiento'),
]

# Fondo de titulo
ws6.merge_cells(f'A{next_r}:N{next_r}')
c = ws6.cell(row=next_r, column=1)
c.value = '--- Glosario de indices ISCAM ---'
c.font = Font(color=BLANCO, bold=True, size=9, name='Calibri')
c.fill = hdr_fill(AZUL_CLARO)
c.alignment = Alignment(horizontal='left', vertical='center')
ws6.row_dimensions[next_r].height = 14

next_r += 1
hdrs_ind = ['Indice', 'Nombre completo', 'Formula', 'Rango', 'Dimension']
hdrs_cols = [1, 4, 8, 12, 14]
for i, (h, col) in enumerate(zip(hdrs_ind, hdrs_cols)):
    c = ws6.cell(row=next_r, column=col)
    c.value = h
    c.font = Font(color=BLANCO, bold=True, size=9, name='Calibri')
    c.fill = hdr_fill('475569')
    c.alignment = Alignment(horizontal='center', vertical='center')
    c.border = thin_border()
# merge las celdas
ws6.merge_cells(f'A{next_r}:C{next_r}')
ws6.merge_cells(f'D{next_r}:G{next_r}')
ws6.merge_cells(f'H{next_r}:K{next_r}')
ws6.merge_cells(f'L{next_r}:M{next_r}')
ws6.merge_cells(f'N{next_r}:N{next_r}')
ws6.row_dimensions[next_r].height = 16

for i, (ind, nombre, formula, rango, dim) in enumerate(indice_data):
    r = next_r + 1 + i
    vals = [ind, nombre, formula, rango, dim]
    cols_merge = ['A:C', 'D:G', 'H:K', 'L:M', 'N:N']
    col_start = [1, 4, 8, 12, 14]
    bg_colors = ['0891B2', '7C3AED', 'B45309', 'DC2626', '059669']
    for j, (vw, merge_range, cs, bg) in enumerate(zip(vals, cols_merge, col_start, bg_colors)):
        try:
            parts = merge_range.split(':')
            ws6.merge_cells(f'{parts[0]}{r}:{parts[1]}{r}')
        except:
            pass
        c = ws6.cell(row=r, column=cs)
        c.value = vw
        c.font = Font(color='1F2937', bold=(j == 0), size=9, name='Calibri')
        c.fill = PatternFill('solid', fgColor='EFF6FF' if j == 0 else ('F9FAFB' if i % 2 == 0 else BLANCO))
        c.border = thin_border()
        c.alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
    ws6.row_dimensions[r].height = 18

# ── 3. COBERTURA IP IV: renombrar y corregir ────────────────────────────
ws3 = wb['COBERTURA IP IV']
# La columna A tiene las dimensiones — no cambiar, solo aclarar en la hoja
# Cambiar titulo de hoja si es necesario
ws3['A1'] = 'Dimension ISCAM'

# Agregar fila explicativa de ISA/IP/IV/RE
max_r3 = ws3.max_row
for r in range(max_r3 + 1, max_r3 + 5):
    if ws3.cell(row=r, column=1).value is None:
        note_r = r
        break

note_data = [
    'FORMULAS ISCAM:',
    '  ISA (Indice Sintetico de Alineamiento) = producto(D1 x D2 x ... x D7)^(1/7)  [geom. 0-1, mayor = mas alineado]',
    '  IP  (Indice de Preparacion)           = (D8 + D9) / 2                        [arit.  0-1, mayor = mas preparado]',
    '  IV  (Indice de Vulnerabilidad)         = (D10 x D11)^(1/2)                   [geom.  0-1, mayor = menos vulnerable]',
    '  RE  (Riesgo de Exclusion)             = ponderacion AHP con Pool Expertos        [0-1, mayor = mayor riesgo exclusion EUDR]',
]
ws3.merge_cells(f'A{note_r}:F{note_r}')
c = ws3.cell(row=note_r, column=1)
c.value = note_data[0]
c.font = Font(color=BLANCO, bold=True, size=9, name='Calibri')
c.fill = hdr_fill(AZUL)
c.alignment = Alignment(horizontal='left', vertical='center')
ws3.row_dimensions[note_r].height = 14

for i, txt in enumerate(note_data[1:], 1):
    r = note_r + i
    ws3.merge_cells(f'A{r}:F{r}')
    c = ws3.cell(row=r, column=1)
    c.value = txt
    c.font = Font(color='374151', size=8, name='Calibri', italic=True)
    c.fill = PatternFill('solid', fgColor='F9FAFB')
    c.alignment = Alignment(horizontal='left', vertical='center')
    ws3.row_dimensions[r].height = 13

# ── 4. DICCIONARIO: agregar ISA/IP/IV/RE ──────────────────────────────────
ws4 = wb['DICCIONARIO']
max_r4 = ws4.max_row

# Headers si no existen
if ws4.cell(row=max_r4, column=1).value not in (None, ''):
    max_r4 += 1

nuevos_dicc = [
    ('ISA',
     'Indice Sintetico de Alineamiento. Producto geometrico de D1 a D7 elevado a 1/7. Mide sostenibilidad, due diligence, derechos humanos, traceabilidad y medio ambiente.',
     'Instrumento 2 (ISCAM)',
     'geom(D1 x D2 x D3 x D4 x D5 x D6 x D7)^(1/7) — rango 0 a 1'),
    ('IP',
     'Indice de Preparacion. Media aritmetica de D8 (estructura) y D9 (mercado). Mide anos de operacion, n. de socios y capacidad de exportar.',
     'MIDAGRI + PRODUCE + SOPARSE',
     'media(D8 + D9) — rango 0 a 1'),
    ('IV',
     'Indice de Vulnerabilidad. Media geometrica de D10 (certificaciones) y D11 (volumen FOB). Mide exposicion al riesgo EUDR por falta de trazabilidad verificable.',
     'PAC + PRODUCE + SUNAT',
     'geom(D10 x D11)^(1/2) — rango 0 a 1'),
    ('RE',
     'Riesgo de Exclusion. Probabilidad de que la organizacion sea exclusion del mercado de la UE por incumplimiento del EUDR. Calculado con ponderacion AHP via Pool de Expertos.',
     'Pool Expertos AHP + Instrumento 2',
     'ponderacion AHP(ISA, IP, IV) con pesos del Pool — rango 0 a 1'),
    ('D1',
     'Trazabilidad de lotes y sistemas de monitoreo. Pregunta ISCAM P1-P3 (Instrumento 2).',
     'Instrumento 2 (campo)',
     'Escala 0-4 por pregunta; ISA = geom(D1..D7)'),
    ('D2',
     'Registro de productores y bases de datos. Pregunta ISCAM P4-P6.',
     'Instrumento 2 (campo)',
     'Escala 0-4'),
    ('D3',
     'Deforestacion y conversion de ecosistemas. Pregunta ISCAM P7-P9.',
     'Instrumento 2 (campo)',
     'Escala 0-4'),
    ('D4',
     'Manejo ambiental y buenas practicas. Pregunta ISCAM P10-P12.',
     'Instrumento 2 (campo)',
     'Escala 0-4'),
    ('D5',
     'Condiciones laborales y contratos. Pregunta ISCAM P13-P15.',
     'Instrumento 2 (campo)',
     'Escala 0-4'),
    ('D6',
     'No infancia, trabajo forzado ni discriminacion. Pregunta ISCAM P16-P18.',
     'Instrumento 2 (campo)',
     'Escala 0-4'),
    ('D7',
     'Seguridad y salud ocupacional. Pregunta ISCAM P19-P21.',
     'Instrumento 2 (campo)',
     'Escala 0-4'),
    ('D8',
     'Anos de operacion y numero de socios. Mide antiguedad y tamaño.',
     'MIDAGRI + SOPARSE CENCOOP + SUNAT',
     'D8 = min(anios/30, 1) si anios>0; sinon 0'),
    ('D9',
     'Capacidad de exportar: volumen, n. operaciones, n. paises destino.',
     'PRODUCE + MIDAGRI',
     'D9 = (n_ops>0) + (n_paises>1) + (fob>media)'),
    ('D10',
     'Certificaciones validas (EUDR): Rainforest, Fairtrade, Organic, etc.',
     'PAC directo',
     'D10 = 1 si certificacion valida, 0 sinon'),
    ('D11',
     'Volumen FOB 2024. Proxy de exposicion al mercado EU.',
     'PRODUCE + SUNAT',
     'D11 = min(FOB/max_FOB, 1)'),
]

for col, desc, fuente, nota in nuevos_dicc:
    max_r4 += 1
    for j, v in enumerate([col, desc, fuente, nota], 1):
        c = ws4.cell(row=max_r4, column=j)
        c.value = v
        c.font = Font(color='1F2937', size=9, name='Calibri', bold=(j == 1))
        c.fill = PatternFill('solid', fgColor='EFF6FF' if j == 1 else ('F9FAFB' if max_r4 % 2 == 0 else BLANCO))
        c.border = thin_border()
        c.alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
    ws4.column_dimensions['B'].width = 60
    ws4.column_dimensions['C'].width = 24
    ws4.column_dimensions['D'].width = 36
    ws4.row_dimensions[max_r4].height = 28

# ── 5. RESUMEN DE FUENTES: corregir ISA/IP/IV/RE ─────────────────────────
ws2 = wb['RESUMEN DE FUENTES']
ws2['A1'] = 'Fuente'
ws2['B1'] = 'Organizaciones'
ws2['C1'] = 'Campos clave'
ws2['D1'] = 'Dimension ISCAM'
ws2['E1'] = 'Notas'

# ── 6. Agregar nota de actualizacion ─────────────────────────────────────
ws_note = wb['MATRIZ']
# buscar fila libre al final
last_r = ws_note.max_row + 2
ws_note.merge_cells(f'A{last_r}:AY{last_r}')
c = ws_note.cell(row=last_r, column=1)
c.value = (
    'NOTA: ISA = Indice Sintetico de Alineamiento | IP = Indice de Preparacion '
    '| IV = Indice de Vulnerabilidad | RE = Riesgo de Exclusion. '
    'D1-D7 requieren Instrumento 2 (campo via Google Forms ISCAM). '
    'D8-D11 se calculan desde fuentes administrativas. '
    'Actualizacion: septiembre 2026.'
)
c.font = Font(color='6B7280', size=8, italic=True, name='Calibri')
c.fill = PatternFill('solid', fgColor='F3F4F6')
c.alignment = Alignment(horizontal='left', vertical='center')
ws_note.row_dimensions[last_r].height = 28

# ── guardar ──────────────────────────────────────────────────────────────────
out = r'C:/Users/acuba/eudrperu/MATRIZ_IP_IV_v5_EUDRPERU.xlsx'
wb.save(out)
print(f'Guardado: {out}')
print('Terminologia ISCAM corregida:')
for ind, nombre, formula, rango, dim in indice_data:
    print(f'  {ind} = {nombre}')
