# -*- coding: utf-8 -*-
"""Uniforma el rótulo de ISCAM_Score!AM con el contenido real de MATRIZ_174!AT."""
import os, shutil, datetime
import win32com.client as win32

ROOT = r"C:\Users\acuba\eudrperu"
PATH = os.path.join(ROOT, "PLANTILLA_INDICE_PVE_ISCAM.xlsx")
ts = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
shutil.copy2(PATH, os.path.join(ROOT, "ISCAM", "respaldos",
             f"PLANTILLA_INDICE_PVE_ISCAM.backup_{ts}_pre-rotulo-am.xlsx"))

xl = win32.Dispatch("Excel.Application")
xl.Visible = False; xl.DisplayAlerts = False; xl.EnableEvents = False
wb = xl.Workbooks.Open(PATH)
wb.Worksheets("ISCAM_Score").Range("AM3").Value = (
    "Estado ISA-PV\n(completo / parcial · n/7 · D12-D15 k/4 / sin dato)")
wb.Save(); wb.Close(SaveChanges=True); xl.Quit()
print("OK — rótulo AM3 uniformado.")
