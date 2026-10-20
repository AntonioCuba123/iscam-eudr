# -*- coding: utf-8 -*-
"""Implementa el umbral de ISA-PactoVerde del documento (§2.4) y unifica el centinela.

  * El documento exige «3 de 4 dimensiones Pacto Verde (D12–D15) con dato» para
    reportar ISA-PactoVerde.  Se operacionaliza como: al menos 3 de las 4 celdas
    D12–D15 de NORMALIZADO (BV:BY) no vacías para esa organización.
  * Por debajo del umbral, ISA-PV se reporta como «—» (sin dato), nunca como 0.
  * Centinelas del bloque PVE unificados a «—».
"""
import os
import shutil
import datetime

import win32com.client as win32

ROOT = r"C:\Users\acuba\eudrperu"
XLS = os.path.join(ROOT, "PLANTILLA_INDICE_PVE_ISCAM.xlsx")

ts = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
bk = os.path.join(ROOT, "ISCAM", "respaldos",
                  "PLANTILLA_INDICE_PVE_ISCAM.backup_%s_pre-umbral-pv.xlsx" % ts)
shutil.copy2(XLS, bk)
print("respaldo:", os.path.basename(bk))

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

xl = win32.Dispatch("Excel.Application")
xl.Visible = False
xl.DisplayAlerts = False
xl.ScreenUpdating = False
xl.EnableEvents = False
wb = xl.Workbooks.Open(XLS)
xl.Calculation = -4135

mz = wb.Worksheets("MATRIZ_174")
sco = wb.Worksheets("ISCAM_Score")
sc = wb.Worksheets("SCORECARDS")

# 1) ISA-PV con umbral (D12..D15 = NORMALIZADO BV:BY, +32..+35 respecto de AP)
mz.Range("AP3:AP176").FormulaR1C1 = (
    '=IF(COUNT(NORMALIZADO!RC[32]:RC[35])>=3,IFERROR((%s)/(%s),"—"),"—")' % (NUM, DEN))

# 2) sentinelas del bloque PVE
mz.Range("S3:S176").Formula = '=IFERROR(ROUND(AP3*100,1),"—")'
mz.Range("T3:T176").Formula = ('=IF(AQ3<6,"⬜  Parcial · Inst. 2 pendiente",IF(NOT(ISNUMBER(S3)),"—",'
                               'IF(S3<34,"🔴 Crítico",IF(S3<67,"🟡 Vulnerable","🟢 Preparado"))))')
mz.Range("AQ2").Value = ("Cobertura ISA-PV (n de 7 componentes con dato; PPWR pendiente). "
                         "ISA-PV se reporta como «—» mientras no se cumpla el umbral "
                         "(3 de 4 dimensiones D12–D15).")
sco.Range("AI4:AI177").Formula = '=IFERROR(MATRIZ_174!AP3,"—")'
sc.Range("B186").Formula = '=IFERROR(ROUND(AVERAGE(MATRIZ_174!S3:S176),1),"—")'

# nota en MATRIZ_174
mz.Cells(182, 1).Value = "UMBRAL ISA-PACTOVERDE (2026-10-15)"
mz.Cells(182, 1).Font.Bold = True
mz.Cells(183, 1).Value = ("ISA-PactoVerde se reporta como «—» (sin dato) mientras la organización no alcance "
                          "el umbral del documento (§2.4): 3 de las 4 dimensiones Pacto Verde D12–D15 con dato. "
                          "Bajo el umbral un valor de 0 sería una medición falsa. La cobertura por organización "
                          "está en AQ.")
mz.Cells(183, 1).WrapText = True

xl.Calculation = -4105
xl.CalculateFull()
wb.Save()

print("\nfila   AQ   ISA-PV(AI)   S(PVE)   T(clasif)")
for fr in [3, 4, 22, 46]:
    ir = fr + 1
    print("  %3d   %-4s %-11s %-8s %s" % (fr, mz.Cells(fr, 43).Value, sco.Cells(ir, 35).Value,
                                          mz.Cells(fr, 19).Value, str(mz.Cells(fr, 20).Value)[:32]))
print("\nPVE promedio (SCORECARDS!B186):", sc.Cells(186, 2).Value)
print("ISA-EUDR (AK4):", sco.Cells(4, 37).Value, "| ISA-Completo (AL4):", sco.Cells(4, 38).Value)

wb.Close(SaveChanges=True)
xl.Quit()
print("OK")
