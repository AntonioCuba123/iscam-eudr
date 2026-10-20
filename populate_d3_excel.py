# -*- coding: utf-8 -*-
"""Popula D3 Score en PLANTILLA_INDICE_PVE.xlsx desde d3_batch_results.json."""

import openpyxl
import json

RESULTS_FILE = r'C:\Users\acuba\eudrperu\d3_batch_results.json'
TEMPLATE_FILE = r'C:\Users\acuba\eudrperu\PLANTILLA_INDICE_PVE.xlsx'
OUTPUT_FILE   = r'C:\Users\acuba\eudrperu\PLANTILLA_INDICE_PVE_d3.xlsx'

def score_d3(result):
    """Convierte señal OSCE+OEFA a score D3 (0-1)."""
    if result['tiene_inhabilitacion_vigente']:
        return 0.0       # Crítico: inh. vigente OSCE
    elif result['inhabilitaciones'] > 0 or result['multas'] > 0:
        return 0.5       # Vulnerable: historia OSCE
    elif result.get('infracciones_ambientales', 0) > 0:
        return 0.75     # Precaución: infracción ambiental OEFA (no es inh. vigente)
    else:
        return 1.0       # Sin hallazgos

def color_d3(result):
    if result['tiene_inhabilitacion_vigente']:
        return 'FF0000'  # Rojo
    elif result['inhabilitaciones'] > 0 or result['multas'] > 0:
        return 'FFC000'  # Ámbar OSCE
    elif result.get('infracciones_ambientales', 0) > 0:
        return '92D050'  # Verde claro - precaución ambiental
    else:
        return '00B050'  # Verde

print("=== Leyendo resultados D3 ===")
with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

results = data['results']
print(f"  Base OSCE: {data.get('base_osce','?')}")
print(f"  Base OEA:  {data.get('base_oea','?')}")
print(f"  Timestamp: {data.get('timestamp','?')}")
print(f"  Total orgs consultadas: {data.get('total_rucs','?')}")

print("\n=== Abriendo plantilla ===")
wb = openpyxl.load_workbook(TEMPLATE_FILE)
ws_matriz = wb['MATRIZ_174']
ws_score = wb['SCORECARDS']

# Determinar columnas en MATRIZ_174
headers_m = [c.value for c in ws_matriz[2]]  # Fila 2 = headers
print(f"  Headers MATRIZ_174: {[h for h in headers_m if h]}")

# Buscar columnas
col_ruc = next((i+1 for i, h in enumerate(headers_m) if h == 'RUC'), None)
col_d3 = next((i+1 for i, h in enumerate(headers_m) if h and 'D3' in str(h)), None)
col_observ = next((i+1 for i, h in enumerate(headers_m) if h and 'Observ' in str(h)), None)

print(f"  Col RUC: {col_ruc}, Col D3: {col_d3}, Col Observ: {col_observ}")

# Si no existe columna D3, agregarla
if not col_d3:
    # Agregar columna T (índice 20 = columna T)
    new_col = ws_matriz.max_column + 1
    from openpyxl.utils import get_column_letter
    col_letter = get_column_letter(new_col)
    ws_matriz.cell(2, new_col).value = 'D3 Score (OSCE)'
    ws_matriz.cell(2, new_col).font = openpyxl.styles.Font(bold=True)
    col_d3 = new_col
    print(f"  Nueva columna D3 agregada en col {col_letter}")

# Si no existe columna de observación, agregarla
if not col_observ:
    new_col2 = ws_matriz.max_column + 1
    from openpyxl.utils import get_column_letter
    col_letter2 = get_column_letter(new_col2)
    ws_matriz.cell(2, new_col2).value = 'D3 Observación'
    ws_matriz.cell(2, new_col2).font = openpyxl.styles.Font(bold=True)
    col_observ = new_col2
    print(f"  Nueva columna Observación agregada en col {col_letter2}")

# Escribir resultados
actualizados = 0
for row_idx in range(3, ws_matriz.max_row + 1):
    ruc_cell = ws_matriz.cell(row_idx, col_ruc)
    ruc = str(ruc_cell.value) if ruc_cell.value else ''
    if not ruc or ruc == 'None':
        continue

    if ruc in results:
        result = results[ruc]
        score = score_d3(result)
        color = color_d3(result)

        # Score
        score_cell = ws_matriz.cell(row_idx, col_d3)
        score_cell.value = score
        score_cell.fill = openpyxl.styles.PatternFill(start_color=color, end_color=color, fill_type='solid')
        score_cell.alignment = openpyxl.styles.Alignment(horizontal='center')

        # Observación
        obs_cell = ws_matriz.cell(row_idx, col_observ)
        if result['tiene_inhabilitacion_vigente']:
            detalle = result['inhabilitaciones_detalle'][0] if result['inhabilitaciones_detalle'] else {}
            obs_cell.value = f"REVISAR - Inh. vigente: {detalle.get('resolucion','?')}"
        elif result['inhabilitaciones'] > 0:
            obs_cell.value = f"{result['inhabilitaciones']} inh. OSCE históricas"
        elif result['multas'] > 0:
            obs_cell.value = f"{result['multas']} multa(s) OSCE"
        elif result.get('infracciones_ambientales', 0) > 0:
            detalle_amb = result.get('infracciones_ambientales_detalle', [{}])[0]
            obs_cell.value = f"⚠ {result['infracciones_ambientales']} infracc. ambiental (OEFA)"
        else:
            obs_cell.value = "Sin hallazgos OSCE / OEFA"

        actualizados += 1

print(f"\n  Org actualizadas en plantilla: {actualizados}/{len(results)}")

# Guardar
wb.save(OUTPUT_FILE)
print(f"\n✓ Plantilla actualizada: {OUTPUT_FILE}")
