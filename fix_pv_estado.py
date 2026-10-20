# -*- coding: utf-8 -*-
"""
Ajuste fino del estado ISA-PV: alinear «completo» con el umbral declarado en el
documento (§2.4: 3 de las 4 dimensiones Pacto Verde D12–D15 con dato) en vez de
exigir las 4, y mantener la exigencia de cobertura completa de componentes (7/7).

  completo  ⟺ COUNT(NORMALIZADO!BV:BY) >= 3  Y  AQ = 7
  parcial   ⟺ ISA-PV tiene valor pero no se cumple lo anterior  → «◐ Parcial · n/7»
  sin dato  ⟺ ningún componente con dato                        → «⬜ Sin dato PVE»
"""
import os, shutil, datetime
import win32com.client as win32

ROOT = r"C:\Users\acuba\eudrperu"
PATH = os.path.join(ROOT, "PLANTILLA_INDICE_PVE_ISCAM.xlsx")
ts = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
bak = os.path.join(ROOT, "ISCAM", "respaldos", f"PLANTILLA_INDICE_PVE_ISCAM.backup_{ts}_pre-pv-estado.xlsx")
shutil.copy2(PATH, bak); print("respaldo:", bak)

COMPLETO = "AND(COUNT(NORMALIZADO!BV3:BY3)>=3,AQ3=7)"
T3 = ('=IF(NOT(ISNUMBER(S3)),"⬜  Sin dato PVE",'
      'IF(' + COMPLETO + ',IF(S3<34,"🔴 Crítico",IF(S3<67,"🟡 Vulnerable","🟢 Preparado")),'
      '"◐  Parcial · "&AQ3&"/7"))')
AT3 = ('=IF(NOT(ISNUMBER(AP3)),"sin dato",'
       'IF(' + COMPLETO + ',"completo","parcial · "&AQ3&"/7"))')

xl = win32.Dispatch("Excel.Application")
xl.Visible = False; xl.DisplayAlerts = False; xl.EnableEvents = False
wb = xl.Workbooks.Open(PATH)
m = wb.Worksheets("MATRIZ_174")
m.Range("T3:T176").Formula = T3
m.Range("AT3:AT176").Formula = AT3
m.Range("AT2").Value = ("Estado ISA-PV\n"
                        "completo = 7/7 componentes y ≥3 de 4 dimensiones D12-D15 capturadas\n"
                        "parcial = valor provisional\n"
                        "sin dato = sin ningún componente")
xl.CalculateFull()
wb.Save(); wb.Close(SaveChanges=True); xl.Quit()
print("OK — estado ISA-PV alineado al umbral (§2.4: ≥3 de 4).")
