# -*- coding: utf-8 -*-
"""Da formato legible a las notas «sin dato» (fusiona A:D / A:H y fija alturas)."""
import win32com.client as win32

XLS = r"C:\Users\acuba\eudrperu\PLANTILLA_INDICE_PVE_ISCAM.xlsx"
xl = win32.Dispatch("Excel.Application")
xl.Visible = False
xl.DisplayAlerts = False
xl.ScreenUpdating = False
xl.EnableEvents = False
wb = xl.Workbooks.Open(XLS)
xl.Calculation = -4135

# ── INSTRUCCIONES: nota superior (A4:A5 ya fusionadas A:H) ──
ins = wb.Worksheets("INSTRUCCIONES")
ins.Range("A5").Value = (
    "La falta de dato no se convierte en 0 en ningún nivel: en la base precensal el % UE/FOB, el FOB, "
    "el score de certificación y los indicadores P1–P14 aparecen como «—». En el motor, ISA-PactoVerde, "
    "ISA-EUDR e IP se reportan «—» cuando no alcanzan su umbral de dimensiones con dato.")
ins.Range("A5").WrapText = True
ins.Rows(4).RowHeight = 18
ins.Rows(5).RowHeight = 48

# ── PONDERADORES: notas del bloque ISA-PV (A56:A59), fusionar A:D ──
pond = wb.Worksheets("PONDERADORES")
for r in (56, 57, 58, 59):
    rango = pond.Range("A%d:D%d" % (r, r))
    if not rango.MergeCells:
        rango.Merge()
    rango.WrapText = True
pond.Rows(56).RowHeight = 16
pond.Rows(57).RowHeight = 46
pond.Rows(58).RowHeight = 16
pond.Rows(59).RowHeight = 46

# ── MATRIZ_174: las notas al pie (A179/A180 y A182/A183) también en columna A ──
mz = wb.Worksheets("MATRIZ_174")
for r in (179, 180, 182, 183):
    rango = mz.Range("A%d:F%d" % (r, r))
    if not rango.MergeCells:
        rango.Merge()
    rango.WrapText = True
mz.Rows(179).RowHeight = 16
mz.Rows(180).RowHeight = 46
mz.Rows(182).RowHeight = 16
mz.Rows(183).RowHeight = 46

xl.Calculation = -4105
xl.CalculateFull()
wb.Save()
wb.Close(SaveChanges=True)
xl.Quit()
print("formato de notas ajustado")
