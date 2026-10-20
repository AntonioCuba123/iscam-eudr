# -*- coding: utf-8 -*-
"""Prueba sintética de IP5 y del conteo de certificaciones sobre una COPIA del libro."""
import os, shutil
import win32com.client as win32

ROOT = r"C:\Users\acuba\eudrperu"
TMP = r"C:\Users\acuba\AppData\Local\Temp\opencode"
os.makedirs(TMP, exist_ok=True)
copy = os.path.join(TMP, "_test_ip5.xlsx")
shutil.copy2(os.path.join(ROOT, "PLANTILLA_INDICE_PVE_ISCAM.xlsx"), copy)

xl = win32.Dispatch("Excel.Application")
xl.Visible = False; xl.DisplayAlerts = False; xl.EnableEvents = False
wb = xl.Workbooks.Open(copy)
try:
    cap = wb.Worksheets("CAPTURA"); m = wb.Worksheets("MATRIZ_174"); sc = wb.Worksheets("ISCAM_Score")

    print("--- Caso 1: sin B0.9, registro H=Fairtrade -> AU 1 -> AV 33")
    print("   AU3 =", m.Cells(3, 47).Value, " AV3 =", m.Cells(3, 48).Value)
    print("   IP5 (T4) =", repr(sc.Range('T4').Value), "(sin D7/D9 debe quedar vacío)")

    print("--- Caso 2: B0.9 = 'Rainforest Alliance, UTZ, Orgánico' -> AU 3 -> AV 100")
    cap.Range("N3").Value = "Rainforest Alliance, UTZ, Organico"
    xl.CalculateFull()
    print("   AU3 =", m.Cells(3, 47).Value, " AV3 =", m.Cells(3, 48).Value)

    print("--- Caso 3: D7=80, D9=50, cert AV=100 -> IP5 = (80+50+100)/3 = 76,67")
    sc.Range("K4").Value = 80; sc.Range("M4").Value = 50
    xl.CalculateFull()
    print("   IP5 (T4) =", sc.Range('T4').Value)

    print("--- Caso 4: D7=80, D9 vacío -> IP5 vacío (sin dato)")
    sc.Range("M4").ClearContents()
    xl.CalculateFull()
    print("   IP5 (T4) =", repr(sc.Range('T4').Value))

    print("--- Caso 5: B0.9 = 'Ninguna' -> AU 0 -> AV 0 -> IP5 = (80+50+0)/3 = 43,33")
    cap.Range("N3").Value = "Ninguna"
    sc.Range("M4").Value = 50
    xl.CalculateFull()
    print("   AU3 =", m.Cells(3, 47).Value, " AV3 =", m.Cells(3, 48).Value, " IP5 =", sc.Range('T4').Value)
finally:
    wb.Close(SaveChanges=False); xl.Quit()
print("prueba terminada (copia desechable:", copy, ")")
