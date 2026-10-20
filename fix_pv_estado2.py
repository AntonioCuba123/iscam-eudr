# -*- coding: utf-8 -*-
"""Hace autoexplicativo el estado ISA-PV cuando la cobertura de componentes está
completa pero el umbral Pacto Verde no: AT agrega el conteo D12-D15 capturado
(la condición del umbral), de modo que «parcial · 7/7» no quede sin explicación."""
import os, shutil, datetime
import win32com.client as win32

ROOT = r"C:\Users\acuba\eudrperu"
PATH = os.path.join(ROOT, "PLANTILLA_INDICE_PVE_ISCAM.xlsx")
ts = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
shutil.copy2(PATH, os.path.join(ROOT, "ISCAM", "respaldos",
             f"PLANTILLA_INDICE_PVE_ISCAM.backup_{ts}_pre-pv-estado2.xlsx"))

COMPLETO = "AND(COUNT(NORMALIZADO!BV3:BY3)>=3,AQ3=7)"
AT3 = ('=IF(NOT(ISNUMBER(AP3)),"sin dato",'
       'IF(' + COMPLETO + ',"completo",'
       '"parcial · "&AQ3&"/7 · D12-D15 "&COUNT(NORMALIZADO!BV3:BY3)&"/4"))')

xl = win32.Dispatch("Excel.Application")
xl.Visible = False; xl.DisplayAlerts = False; xl.EnableEvents = False
wb = xl.Workbooks.Open(PATH)
m = wb.Worksheets("MATRIZ_174")
m.Range("AT3:AT176").Formula = AT3
m.Columns("AT").ColumnWidth = 27
xl.CalculateFull()
wb.Save(); wb.Close(SaveChanges=True); xl.Quit()
print("OK — AT informa también D12-D15 capturado.")
