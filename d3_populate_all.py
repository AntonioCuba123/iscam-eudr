# -*- coding: utf-8 -*-
"""Pobla MATRIZ_174!U (D3) y V (observación) para las 174 organizaciones, vía Excel COM."""
import win32com.client as wc
import json

PATH = r"C:\Users\acuba\eudrperu\PLANTILLA_INDICE_PVE_ISCAM.xlsx"
JSON = r"C:\Users\acuba\eudrperu\d3_batch_results.json"

data = json.load(open(JSON, encoding="utf-8"))["results"]

def score_d3(r):
    if r["tiene_inhabilitacion_vigente"]:
        return 0.0, 0xFF0000
    if r["inhabilitaciones"] > 0 or r["multas"] > 0:
        return 0.5, 0xFFC000
    if r.get("infracciones_ambientales", 0) > 0:
        return 0.75, 0x92D050
    return 1.0, 0x00B050

def obs_d3(r):
    if r["tiene_inhabilitacion_vigente"]:
        d = (r["inhabilitaciones_detalle"] or [{}])[0]
        return f"REVISAR - Inh. vigente: {d.get('resolucion','?')}"
    if r["inhabilitaciones"] > 0:
        return f"{r['inhabilitaciones']} inh. OSCE históricas"
    if r["multas"] > 0:
        return f"{r['multas']} multa(s) OSCE"
    if r.get("infracciones_ambientales", 0) > 0:
        return f"\u26a0 {r['infracciones_ambientales']} infracc. ambiental (OEFA)"
    return "Sin hallazgos OSCE / OEFA"

app = wc.DispatchEx("Excel.Application")
app.Visible = False; app.DisplayAlerts = False
wb = app.Workbooks.Open(PATH)
ws = wb.Worksheets("MATRIZ_174")

faltan = []
U = []; V = []; C = []
n = 0
for r in range(3, 177):
    ruc = str(ws.Cells(r, 1).Value).strip() if ws.Cells(r, 1).Value is not None else ""
    if ruc not in data:
        faltan.append((r, ruc)); U.append([None]); V.append([None]); C.append([None]); continue
    s, col = score_d3(data[ruc])
    U.append([s]); V.append([obs_d3(data[ruc])]); C.append([col]); n += 1

ws.Range("U3:U176").Value = U
ws.Range("V3:V176").Value = V
# colores del score
for i, cval in enumerate(C):
    if cval[0] is not None:
        ws.Cells(3 + i, 21).Interior.Color = cval[0]

print("filas pobladas:", n, "| sin dato en JSON:", faltan)
app.CalculateFull()
wb.Save(); wb.Close(SaveChanges=False); app.Quit()

from collections import Counter
print("U:", dict(Counter(x[0] for x in U)))
