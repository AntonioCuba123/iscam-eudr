# -*- coding: utf-8 -*-
"""
Normaliza el idioma de las celdas de texto de los libros del proyecto a
castellano, con las mismas reglas y lista blanca que fix_idioma.py
(conserva identificadores de hoja, nombres de archivo, código, URLs y
términos naturalizados).

Estrategia en dos pasos para no recorrer celda por celda vía COM (lento):
  1. openpyyl localiza las celdas cuyo texto cambia (lectura rápida);
  2. Excel vía COM reescribe solo esas celdas, preservando validaciones de
     datos, formatos y fórmulas.
"""
import os, shutil, datetime
import openpyxl, warnings
import win32com.client as wc

import fix_idioma as fi

warnings.filterwarnings('ignore')
ROOT = fi.ROOT
RESP = fi.RESP
ts = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")

LIBROS = [
    'PLANTILLA_INDICE_PVE_ISCAM.xlsx',
    os.path.join('ISCAM', 'Directorio - Pool de Expertos Panel AHP.xlsx'),
    # reports/informe_eudr_tablas.xlsx se corrigió a nivel de XML (tiene 7
    # gráficos que un round-trip perdería); Excel no logra abrirlo vía COM.
]


def candidatos(path):
    wb = openpyxl.load_workbook(path)
    out = []
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                v = c.value
                if isinstance(v, str) and not v.startswith('='):
                    nv = fi.normaliza(v)
                    if nv != v:
                        out.append((ws.title, c.coordinate, v, nv))
    wb.close()
    return out


app = wc.DispatchEx('Excel.Application')
app.Visible = False
app.DisplayAlerts = False

for rel in LIBROS:
    path = os.path.join(ROOT, rel)
    if not os.path.exists(path):
        print('  (no existe)', rel)
        continue
    cands = candidatos(path)
    if not cands:
        print(f'=== {rel}: sin cambios')
        continue
    bak = os.path.join(RESP, os.path.basename(path) + f'.backup_{ts}_pre-idioma.xlsx')
    shutil.copy2(path, bak)
    wb = app.Workbooks.Open(path)
    aplicados = 0
    for sheet, coord, viejo, nuevo in cands:
        cell = wb.Worksheets(sheet).Range(coord)
        if cell.Value == viejo:          # solo si nadie movió el texto
            cell.Value = nuevo
            aplicados += 1
    wb.Close(SaveChanges=True)
    print(f'=== {rel}: {aplicados}/{len(cands)} celdas normalizadas '
          f'(respaldo en ISCAM/respaldos)')
    for sheet, coord, viejo, nuevo in cands[:12]:
        print(f'   {sheet}!{coord}: {viejo[:58]!r} -> {nuevo[:58]!r}')
    if len(cands) > 12:
        print(f'   … y {len(cands) - 12} más')

app.Quit()
print('listo')
