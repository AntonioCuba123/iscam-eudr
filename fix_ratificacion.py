# -*- coding: utf-8 -*-
"""
Aplica en vivo la ratificación [R] (2026-10-15) contra las fuentes originales del
Instrumento 2, sobre PLANTILLA_INDICE_PVE_ISCAM.xlsx:

  1. CODIFICACION — reemplaza la marca «[R] revisar» por el resultado ratificado
     (motivo de no promediar, o dirección confirmada).
  2. NORMALIZADO — reescribe el promedio de cada dimensión D1–D11 usando solo las
     preguntas que el instrumento dice que promedian (cod.DIMS). Bandera, mapeo,
     Bloque 0 y Bloque P quedan fuera del promedio (se siguen capturando y
     reportando por separado). D11 queda sin promedio (inventario).
  3. MATRIZ_174 — Fairtrade de 20132505455 (AGUILAYOC): «sin dato» → «SI», con
     fuente web/JNC («Orgánica y Comercio Justo»).

No reconstruye CAPTURA ni las validaciones: solo toca notas y fórmulas.
"""
import os, importlib.util, datetime, shutil
import win32com.client as win32

ROOT = r"C:\Users\acuba\eudrperu"
PATH = os.path.join(ROOT, "PLANTILLA_INDICE_PVE_ISCAM.xlsx")

sp = importlib.util.spec_from_file_location("cod", os.path.join(ROOT, "codificacion_instrumento2.py"))
cod = importlib.util.module_from_spec(sp); sp.loader.exec_module(cod)

ts = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
bak = os.path.join(ROOT, "ISCAM", "respaldos", f"PLANTILLA_INDICE_PVE_ISCAM.backup_{ts}_pre-ratificacion-aplicada.xlsx")
shutil.copy2(PATH, bak); print("respaldo:", bak)

NOTE = {
 # ── no promedian (bandera / mapeo / Bloque 0 / Bloque P) ───────────────────
 "B0.8":   "Bloque 0 (identificación) — no puntúa. Se captura y se reporta como variable de verificación de destinos (no entra a D7).",
 "P8":     "Bloque P (desempeño) — no puntúa; variable de resultado. Se reporta por separado.",
 "P10":    "Bloque P (desempeño) — no puntúa; variable de resultado. Se reporta por separado.",
 "P13":    "Bloque P (desempeño) — no puntúa; variable de resultado. Se reporta por separado.",
 "P14":    "Bloque P (desempeño) — no puntúa; variable de resultado. Se reporta por separado.",
 "D2.10":  "Bandera roja de mezcla de lotes — se reporta aparte; no promedia en D2.",
 "D2.5b":  "Bandera de trazabilidad de proveedores externos — se reporta aparte; no promedia en D2.",
 "D3.14g": "Verificación CLPI — no promedia en D3.",
 "D3.14i": "Bandera de saneamiento OEFA/SINEFA — se reporta aparte; no promedia en D3.",
 "D4.15a": "Bandera de alertas de deforestación — se reporta aparte; no promedia en D4.",
 "D5.19a": "Mapeo de componentes del plan de gestión — insumo del Instrumento 4; no promedia en D5.",
 "D7.28":  "Indicador de urgencia (riesgo percibido) — se reporta aparte; no promedia en D7.",
 "D7.28c": "Mapeo tipo/alcance de la documentación del comprador — insumo del Instrumento 4; no promedia en D7.",
 "D10.36": "Bandera de falsa seguridad (certificación ≠ EUDR) — se reporta aparte; no entra al puntaje de D10.",
 "D10.37": "Bandera (oferta de «certificación EUDR») — se reporta aparte; no entra al puntaje de D10.",
 "D11.38": "Mapeo/inventario de actores — insumo del Instrumento 4; no promedia.",
 "D11.39a":"D11 es inventario (no promedia) — se reporta por pregunta.",
 # ── sí promedian: dirección ratificada ─────────────────────────────────────
 "D1.1":   "Ratificado 2026-10-15: 100 = introduce bajo su propio nombre (operador directo); 50 = vende a través de un tercero.",
 "D1.4":   "Ratificado 2026-10-15: 100 = cumple los umbrales de micro/pequeña empresa (Directiva 2013/34/UE), que definen su régimen simplificado.",
 "D3.12":  "Ratificado 2026-10-15: severidad de la superposición — ninguna 100 · puntual 50 · extensa 0 · ANP/zona de amortiguamiento 0.",
 "D4.15":  "Ratificado 2026-10-15: eje de verificación del cambio de uso post-31-dic-2020; «casos detectados sin resolver» = 0.",
 "D6.25b": "Ratificado 2026-10-15: manda la última prueba (nunca 0 · >12 meses 50 · últimos 12 meses 100); el origen del protocolo es contexto (50).",
 "D9.34":  "Ratificado 2026-10-15: carga financiera — recursos propios 100 · fuente identificada 67 · crédito 33 · no ha sido necesario 100.",
 "PP1":    "Ratificado 2026-10-15: escala de reutilización (yute reutilizable > yute nuevo > papel > plástico); alimenta PPWR, no el ISA-EUDR.",
}
L_EUDR = {"B0.8", "P8", "P10", "P13", "P14", "D2.10", "D2.5b", "D3.14g", "D3.14i",
          "D4.15a", "D5.19a", "D7.28", "D7.28c", "D10.36", "D10.37", "D11.38", "D11.39a"}

xl = win32.Dispatch("Excel.Application")
xl.Visible = False; xl.DisplayAlerts = False; xl.ScreenUpdating = False
xl.EnableEvents = False
wb = xl.Workbooks.Open(PATH)
try:
    xl.Calculation = -4135            # xlCalculationManual
except Exception as e:
    print("  (no se pudo fijar cálculo manual, sigo igual):", e)
try:
    wb.Unprotect()
except Exception:
    pass

# ── 1. CODIFICACION — notas ratificadas ────────────────────────────────────
codws = wb.Worksheets("CODIFICACION")
codws.Range("A1").Value = ("CODIFICACIÓN — Instrumento 2 · opción de respuesta → puntaje 0-100.  "
                           "100 = mejor alineamiento con el EUDR.  «sin dato» = no se promedia.  "
                           "Banderas, mapeos y bloques 0/P se capturan y se reportan por separado: "
                           "no entran a ningún promedio (Instrumento 2, Tabla 5 y reglas de integridad).")
n = 0
last_cod = codws.Cells(codws.Rows.Count, 1).End(-4162).Row
for r in range(3, last_cod + 1):
    qid = codws.Cells(r, 1).Value
    if qid in NOTE:
        sd = str(codws.Cells(r, 5).Value).strip().lower().startswith("sin dato")
        txt = NOTE[qid] + ("  · «sin dato» no promedia" if sd else "")
        codws.Cells(r, 7).Value = txt
        n += 1
print("CODIFICACION — filas anotadas:", n)

# ── 2. NORMALIZADO — promedios de dimensión ratificados ────────────────────
nws = wb.Worksheets("NORMALIZADO")
last = nws.Cells(nws.Rows.Count, 1).End(-4162).Row      # xlUp
hdr = {}
for c in range(3, nws.Cells(2, nws.Columns.Count).End(-4159).Column + 1):   # xlToLeft
    v = nws.Cells(2, c).Value
    if v:
        hdr[v] = c
dim_col = {d: hdr[d] for d, _ in cod.DIMS}
for d, qs in cod.DIMS:
    dc = dim_col[d]
    if not qs:
        f = '=""'
    else:
        refs = []
        for q in qs:
            off = hdr[q] - dc
            refs.append("RC" if off == 0 else f"RC[{off}]")
        f = f'=IFERROR(AVERAGE({",".join(refs)}),"")'
    nws.Range(nws.Cells(3, dc), nws.Cells(last, dc)).FormulaR1C1 = f
print("NORMALIZADO — dimensiones reescritas:", len(cod.DIMS), " filas:", last - 2)

# ── 3. MATRIZ_174 — Fairtrade 20132505455 ─────────────────────────────────
mws = wb.Worksheets("MATRIZ_174")
done = []
for r in range(3, 177):
    if str(mws.Cells(r, 1).Value).strip() == "20132505455":
        mws.Cells(r, 9).Value = "SI"
        done.append(r)
print("MATRIZ_174 — Fairtrade 20132505455 (fila I):", done)

# ── 4. Encabezado ISCAM_Score (D10 = bandera + asesoría) ───────────────────
wb.Worksheets("ISCAM_Score").Cells(3, 14).Value = "D10 — Certificación\n(bandera; solo asesoría puntúa)"

xl.Calculation = -4105
xl.CalculateFull()
wb.Save(); wb.Close(SaveChanges=True); xl.Quit()
print("OK — guardado.")
