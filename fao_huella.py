# -*- coding: utf-8 -*-
"""Estimación de huella de carbono CO2e para las 36 orgs FOB UE.

Fuentes IPCC/SETAC/FAO para café y cacao:
  - Café convencional:   ~6,000 kg CO2e/ha/año (suelo + N2O + CH4)
  - Café orgánico:        ~2,500 kg CO2e/ha/año
  - Cacao convencional:   ~8,000 kg CO2e/ha/año
  - Cacao agroforesta:   ~4,500 kg CO2e/ha/año

Para D12 del Instrumento 2:
  0 = Sin medición (default para todas las orgs sin ha conocidas)
  1 = En curso (para orgs con ha > 0 pero sin cálculo formal)
  2 = Certificado (ninguna org lo tiene aún — score = 1)
"""

import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment

SRC = r'C:\Users\acuba\eudrperu\PLANTILLA_INDICE_PVE.xlsx'
OUT = r'C:\Users\acuba\eudrperu\PLANTILLA_INDICE_PVE.xlsx'

# Factores FAO/IPCC en kg CO2e/ha/año
FACTORES = {
    'cafe':  6000,   # convencional
    'café':  6000,
    'cacao': 8000,   # convencional
    'cacao': 8000,
}

GRIS     = PatternFill(start_color='D9D9D9', end_color='D9D9D9', fill_type='solid')
AMARILLO = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')
VERDE    = PatternFill(start_color='C6EFCE', end_color='C6EFCE', fill_type='solid')
BOLD     = Font(bold=True)
CENTER   = Alignment(horizontal='center')

wb = openpyxl.load_workbook(SRC, data_only=False)
ws = wb['MATRIZ_174']

# D12 está en col W = 23
COL_D12 = 23

print('RUC              | Prod     | Ha  | kgCO2e/año | D12 Score | Fuente')
print('-' * 90)

stats = {'0': 0, '1': 0, '2': 0, 'sin_ha': 0}

for r in range(3, ws.max_row + 1):
    ruc   = ws.cell(r, 1).value
    prod  = str(ws.cell(r, 4).value or '').lower().strip()
    ha    = ws.cell(r, 18).value or 0

    if ha <= 0:
        stats['sin_ha'] += 1
        d12 = 0
        fuente = 'Sin datos ha'
    else:
        factor = FACTORES.get(prod, 6000)
        co2e   = ha * factor
        # D12: si tiene ha, le damos 1 (en curso)
        d12 = 1
        fuente = f'{factor} kgCO2e/ha x {ha} ha'
        stats['1'] += 1

    cell = ws.cell(r, COL_D12)
    old_val = cell.value
    cell.value = d12

    # Solo remarcar las que no tenían valor (default=0 = gris ya puesto)
    if old_val is None or old_val == 0:
        cell.fill = GRIS if d12 == 0 else AMARILLO
    cell.alignment = CENTER

    print(f'{ruc} | {prod[:8]:8} | {ha:5} | {co2e if ha>0 else 0:>10.0f} |    {d12}     | {fuente}')

print(f'\nResumen: Sin ha={stats["sin_ha"]}, En curso (ha>0)={stats["1"]}, Certificado=0')

wb.save(OUT)
print(f'\nD12 poblado en {OUT}')
print('\nNOTA: Los valores 0=gris son estimaciones sin medición formal.')
print('      Las orgs con ha>0 reciben D12=1 (en curso).')
print('      Cuando respondan el Instrumento 2, sobrescribir manualmente.')
