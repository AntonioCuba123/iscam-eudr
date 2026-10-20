# -*- coding: utf-8 -*-
"""Prueba del motor con un caso sintético, sobre una COPIA temporal (el entregable
no se toca). Verifica la corrección de escala de IP5 y la cadena del estado ISA-PV
(parcial → completo)."""
import os, shutil, tempfile
import win32com.client as win32

SRC = r"C:\Users\acuba\eudrperu\PLANTILLA_INDICE_PVE_ISCAM.xlsx"
TMP = os.path.join(r"C:\Users\acuba\AppData\Local\Temp\opencode", "test_pv_sintetico.xlsx")
os.makedirs(os.path.dirname(TMP), exist_ok=True)
shutil.copy2(SRC, TMP)

xl = win32.Dispatch("Excel.Application")
xl.Visible = False; xl.DisplayAlerts = False; xl.EnableEvents = False
wb = xl.Workbooks.Open(TMP)
try:
    iss, mtz, sc, nz = (wb.Worksheets("ISCAM_Score"), wb.Worksheets("MATRIZ_174"),
                        wb.Worksheets("SCORECARDS"), wb.Worksheets("NORMALIZADO"))
    print("--- estado inicial (captura vacía) ---")
    print("  MATRIZ T3:", mtz.Range("T3").Value, "| AT3:", mtz.Range("AT3").Value,
          "| AP3:", mtz.Range("AP3").Value)

    print("\n--- A) IP5 (ISCAM_Score!T4) con D7=100, D9=50 y conteo AV ---")
    for cert, esp in ((100, (100 + 50 + 100) / 3), (66, (100 + 50 + 66) / 3)):
        iss.Range("K4").Value = 100        # D7
        iss.Range("M4").Value = 50         # D9
        mtz.Range("AV3").Value = cert      # conteo 0/33/66/100, no el score 0-1 de O
        xl.CalculateFull()
        got = iss.Range("T4").Value
        print(f"  AV={cert} → IP5 = {got}   (esperado {esp:.1f})",
              "OK" if got is not None and abs(got - esp) < 0.05 else "REVISAR")

    print("\n--- B) ISA-PV: 7/7 componentes + D12-D15 en 0-100 → completo ---")
    mtz.Range("M3").Value = 80             # EXP_UE
    sc.Range("H3").Value = 50              # TRAZA (D2)
    sc.Range("I3").Value = 60              # DILIG (D5)
    sc.Range("J3").Value = 70              # CAPAC (D6)
    iss.Range("K4").Value = 100            # PRESION (D7)
    mtz.Range("O3").Value = 1              # CERTIF (0-1)
    for c in ("BW3", "BZ3", "CB3", "CC3"):
        nz.Range(c).Value = 100            # ancla de D12, D13, D14 y D15
    xl.CalculateFull()
    anclas = sum(1 for c in ("BW3", "BZ3", "CB3", "CC3") if nz.Range(c).Value not in (None, ""))
    print("  AQ3 (cobertura):", mtz.Range("AQ3").Value, "| anclas D12-D15:", anclas)
    print("  AP3:", mtz.Range("AP3").Value, "| S3:", mtz.Range("S3").Value)
    print("  T3 :", mtz.Range("T3").Value, "| AT3:", mtz.Range("AT3").Value)
    print("  ISCAM AM4:", iss.Range("AM4").Value)

    print("\n--- C) mismos datos, pero sin D12-D15 → vuelve a parcial ---")
    for c in ("BW3", "BZ3", "CB3", "CC3"):
        nz.Range(c).ClearContents()
    xl.CalculateFull()
    print("  AP3:", mtz.Range("AP3").Value, "| T3:", mtz.Range("T3").Value,
          "| AT3:", mtz.Range("AT3").Value)
    print("  parcial:", "OK" if "Parcial" in str(mtz.Range("T3").Value) else "REVISAR")

    print("\n--- D) sin ningún componente → sin dato ---")
    for addr, ws in (("M3", mtz), ("O3", mtz), ("H3", sc), ("I3", sc), ("J3", sc), ("K4", iss)):
        ws.Range(addr).ClearContents()
    xl.CalculateFull()
    print("  AP3:", mtz.Range("AP3").Value, "| S3:", mtz.Range("S3").Value,
          "| T3:", mtz.Range("T3").Value, "| AT3:", mtz.Range("AT3").Value)
    print("  sin dato:", "OK" if mtz.Range("AP3").Value == "—" else "REVISAR")
finally:
    wb.Close(SaveChanges=False)
    xl.Quit()
os.remove(TMP)
print("\ncopia temporal eliminada:", not os.path.exists(TMP))
