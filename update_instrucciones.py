# -*- coding: utf-8 -*-
"""Actualiza INSTRUCCIONES (flujo de carga) y PONDERADORES (nota de ingesta)."""
import win32com.client as win32

PATH = r"C:\Users\acuba\eudrperu\PLANTILLA_INDICE_PVE_ISCAM.xlsx"
xl = win32.Dispatch("Excel.Application")
xl.Visible = False
xl.DisplayAlerts = False
xl.ScreenUpdating = False
xl.EnableEvents = False
wb = xl.Workbooks.Open(PATH)
xl.Calculation = -4135

# ── PONDERADORES: ver vecindad de notas ───────────────────────────────────
pond = wb.Worksheets("PONDERADORES")
print("--- PONDERADORES filas 44-56 ---")
for r in range(44, 57):
    for c in range(1, 5):
        v = pond.Cells(r, c).Value
        if v is not None:
            print(f"  {chr(64+c)}{r}: {str(v)[:190]}")

# ── INSTRUCCIONES: flujo de carga ─────────────────────────────────────────
ins = wb.Worksheets("INSTRUCCIONES")
ins.Range("B13").Value = (
    "Cargar las respuestas del Instrumento 2 en la hoja CAPTURA: una fila por cooperativa (RUC y razón "
    "social ya precargados) y una columna por pregunta, con lista desplegable en las preguntas de opción. "
    "Es la única hoja donde se escribe: NORMALIZADO calcula los 0-100 por pregunta y las dimensiones "
    "D1-D11, y el motor (ISCAM_Score), los semáforos y el radar se recalculan solos.")

ins.Range("A27").Value = (
    "Cómo funciona la carga del instrumento: la hoja CODIFICACION es la tabla de codificación (cada opción "
    "de respuesta vale 0-100, o «sin dato» si la opción expresa desconocimiento o no aplicación); la hoja "
    "CAPTURA es la entrada de datos; y la hoja NORMALIZADO convierte y agrega. Si una respuesta no está en "
    "la tabla, se marca «⚠» para revisarla. Las preguntas de casillas múltiples se separan con «;». La "
    "tabla de codificación marca con «[R]» los ítems a ratificar antes del levantamiento de campo.")
ins.Range("A27").WrapText = True
ins.Rows(27).RowHeight = 78

# ── PONDERADORES: nota de ingesta ─────────────────────────────────────────
last = 53
while pond.Cells(last, 1).Value is not None and last < 70:
    last += 1
pond.Cells(last, 1).Value = "CAPA DE INGESTA (2026-10-15)"
pond.Cells(last, 1).Font.Bold = True
pond.Cells(last + 1, 1).Value = (
    "El Instrumento 2 se carga en CAPTURA; CODIFICACION traduce cada opción a 0-100 (o «sin dato») y "
    "NORMALIZADO entrega el 0-100 por pregunta y el agregado de D1-D11, que alimenta ISCAM_Score. D3 "
    "conserva el valor de la consulta OSCE/OEFA cuando no hay respuesta de encuesta.")
pond.Cells(last + 1, 1).WrapText = True
print(f"\nnotas PONDERADORES escritas en A{last}:A{last+1}")

xl.Calculation = -4105
xl.CalculateFull()
wb.Save()
wb.Close(SaveChanges=True)
xl.Quit()
print("OK")
