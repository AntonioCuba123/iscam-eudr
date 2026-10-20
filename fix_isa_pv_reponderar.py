# -*- coding: utf-8 -*-
"""ISA-PV: reponderar sobre los componentes presentes (misma regla que ISA-EUDR).

Antes:  ISA-PV = Σ(wᵢ·vᵢ) / 100      -> un componente sin dato contaba como 0
Ahora:  ISA-PV = Σ(wᵢ·vᵢ) / Σwᵢ      -> wᵢ solo de los componentes presentes
PPWR (w=4) queda excluido mientras no tenga fuente (nota AQ2: «PPWR pendiente»).
"""
import win32com.client as win32

PATH = r"C:\Users\acuba\eudrperu\PLANTILLA_INDICE_PVE_ISCAM.xlsx"
xl = win32.Dispatch("Excel.Application")
xl.Visible = False
xl.DisplayAlerts = False
xl.ScreenUpdating = False
xl.EnableEvents = False
wb = xl.Workbooks.Open(PATH)
xl.Calculation = -4135
mz = wb.Worksheets("MATRIZ_174")

# ── AP = ISA-PV (42) ; offsets sobre AP: M=-29, O=-27, W:Z=-19:-16 ────────
#   SCORECARDS H/I/J = -34/-33/-32 ; ISCAM_Score K fila+1 = R[1]C[-31]
NUM = (
    'IF(ISNUMBER(RC[-29]),RC[-29]/100*PONDERADORES!R12C4,0)'
    '+IF(ISNUMBER(SCORECARDS!RC[-34]),SCORECARDS!RC[-34]/100*PONDERADORES!R13C4,0)'
    '+IF(ISNUMBER(SCORECARDS!RC[-33]),SCORECARDS!RC[-33]/100*PONDERADORES!R14C4,0)'
    '+IF(ISNUMBER(SCORECARDS!RC[-32]),SCORECARDS!RC[-32]/100*PONDERADORES!R15C4,0)'
    '+IF(ISNUMBER(ISCAM_Score!R[1]C[-31]),ISCAM_Score!R[1]C[-31]/100*PONDERADORES!R16C4,0)'
    '+IF(ISNUMBER(RC[-27]),RC[-27]*PONDERADORES!R17C4,0)'
    '+IF(ISNUMBER(AVERAGE(RC[-19]:RC[-16])),AVERAGE(RC[-19]:RC[-16])/2*PONDERADORES!R19C4,0)'
)
DEN = (
    'IF(ISNUMBER(RC[-29]),PONDERADORES!R12C4,0)'
    '+IF(ISNUMBER(SCORECARDS!RC[-34]),PONDERADORES!R13C4,0)'
    '+IF(ISNUMBER(SCORECARDS!RC[-33]),PONDERADORES!R14C4,0)'
    '+IF(ISNUMBER(SCORECARDS!RC[-32]),PONDERADORES!R15C4,0)'
    '+IF(ISNUMBER(ISCAM_Score!R[1]C[-31]),PONDERADORES!R16C4,0)'
    '+IF(ISNUMBER(RC[-27]),PONDERADORES!R17C4,0)'
    '+IF(ISNUMBER(AVERAGE(RC[-19]:RC[-16])),PONDERADORES!R19C4,0)'
)
mz.Range("AP3:AP176").FormulaR1C1 = f'=IFERROR(({NUM})/({DEN}),"N/A")'

# ── AQ = cobertura (43): mismo criterio de presencia, en sintonía ──────────
mz.Range("AQ3:AQ176").FormulaR1C1 = (
    '=IF(ISNUMBER(RC[-30]),1,0)'
    '+IF(ISNUMBER(SCORECARDS!RC[-35]),1,0)'
    '+IF(ISNUMBER(SCORECARDS!RC[-34]),1,0)'
    '+IF(ISNUMBER(SCORECARDS!RC[-33]),1,0)'
    '+IF(ISNUMBER(ISCAM_Score!R[1]C[-32]),1,0)'
    '+IF(ISNUMBER(RC[-28]),1,0)'
    '+IF(COUNT(RC[-20]:RC[-17])>0,1,0)'
)
mz.Range("AQ2").Value = ("Cobertura ISA-PV (n de 7 componentes presentes; PPWR pendiente). "
                         "ISA-PV se repondera sobre los componentes presentes.")

xl.Calculation = -4105
xl.CalculateFull()
wb.Save()

# ── muestreo antes/después ────────────────────────────────────────────────
print("org (fila)   cobertura   ISA-PV")
for f in [3, 4, 5, 46, 100, 176]:
    print(f"   {f:3}         {mz.Cells(f, 43).Value}         {mz.Cells(f, 42).Value}")
print("  S2 (PVE score x100):", mz.Cells(3, 19).Value)
wb.Close(SaveChanges=True)
xl.Quit()
print("OK")
