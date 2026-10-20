# -*- coding: utf-8 -*-
"""Agrega la nota de codificación ratificada (2026-10-15) a PONDERADORES y MATRIZ_174.
Escribe por COM para no perder validaciones ni comentarios."""
import os, shutil, datetime
import win32com.client as win32

ROOT = r"C:\Users\acuba\eudrperu"
PATH = os.path.join(ROOT, "PLANTILLA_INDICE_PVE_ISCAM.xlsx")
ts = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
bak = os.path.join(ROOT, "ISCAM", "respaldos", f"PLANTILLA_INDICE_PVE_ISCAM.backup_{ts}_pre-nota-ratificacion.xlsx")
shutil.copy2(PATH, bak); print("respaldo:", bak)

TITULO = "CODIFICACIÓN RATIFICADA CONTRA LAS FUENTES DEL INSTRUMENTO (2026-10-15)"
CUERPO = (
    "Los quince ítems [R] se resolvieron con las fuentes del propio instrumento "
    "(Nota de puntaje del Instrumento 2, Tabla 5 del DOC_TRABAJO y reglas de integridad de la "
    "estructura de la hoja de respuestas), no por criterio propio. Ocho quedan FUERA de todo "
    "promedio —banderas, mapeos, Bloque 0 y Bloque P— y se reportan por separado: B0.8, P8, P10, "
    "P13, P14, D2.10, D2.5b, D3.14g, D3.14i, D4.15a, D5.19a, D7.28, D7.28c, D10.36, D10.37, "
    "D11.38, D11.39a. Los otros siete SÍ promedian (dirección confirmada): D1.1, D1.4, D3.12, "
    "D4.15, D6.25b, D9.34 y PP1. NORMALIZADO computa el promedio de cada dimensión solo sobre las "
    "preguntas promediables; D11 es inventario (sin promedio) y D10 puntúa solo por la asesoría EUDR. "
    "Detalle ítem por ítem en la hoja CODIFICACION."
)

xl = win32.Dispatch("Excel.Application")
xl.Visible = False; xl.DisplayAlerts = False; xl.EnableEvents = False
wb = xl.Workbooks.Open(PATH)


def bloque(ws, r):
    ws.Range(f"A{r}:D{r}").Merge()
    ws.Cells(r, 1).Value = TITULO
    ws.Cells(r, 1).Font.Bold = True
    ws.Cells(r + 1, 1).Value = CUERPO
    ws.Range(f"A{r+1}:D{r+1}").Merge()
    ws.Range(f"A{r}:D{r+1}").WrapText = True
    ws.Range(f"A{r}:D{r+1}").VerticalAlignment = -4160     # xlTop
    ws.Rows(r).RowHeight = 16.05
    ws.Rows(r + 1).RowHeight = 78


bloque(wb.Worksheets("PONDERADORES"), 61)
bloque(wb.Worksheets("MATRIZ_174"), 185)

xl.CalculateFull()
wb.Save(); wb.Close(SaveChanges=True); xl.Quit()
print("OK — notas agregadas en PONDERADORES!A61 y MATRIZ_174!A185.")
