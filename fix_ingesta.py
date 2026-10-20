# -*- coding: utf-8 -*-
"""Ajustes finos tras construir la capa de ingesta."""
import win32com.client as win32

PATH = r"C:\Users\acuba\eudrperu\PLANTILLA_INDICE_PVE_ISCAM.xlsx"
xl = win32.Dispatch("Excel.Application")
xl.Visible = False
xl.DisplayAlerts = False
xl.ScreenUpdating = False
xl.EnableEvents = False
wb = xl.Workbooks.Open(PATH)
xl.Calculation = -4135

# 1. Orden lógico de hojas (ancla explícita, tolerante a no-ops)
order = ["INSTRUCCIONES", "INSTRUMENTO_2_PREGUNTAS", "CODIFICACION", "CAPTURA",
         "NORMALIZADO", "ISCAM_Score", "PONDERADORES", "MATRIZ_174", "SCORECARDS",
         "RADAR_BRECHAS"]
anchor = None
for nm in order:
    try:
        ws = wb.Worksheets(nm)
        if anchor is None:
            ws.Move(Before=wb.Worksheets(1))
        else:
            ws.Move(After=wb.Worksheets(anchor))
        anchor = nm
    except Exception as e:
        print("order:", nm, e)
print("orden final:", [wb.Worksheets(i).Name for i in range(1, wb.Worksheets.Count + 1)])

# 2. IV2 (V): conservar la base 50 del bloque IV cuando D1 no es numérico
sco = wb.Worksheets("ISCAM_Score")
sco.Range("V4:V177").FormulaR1C1 = '=IF(OR(NOT(ISNUMBER(RC[-16])),RC[-16]=0),50,RC[-16])'
print("IV2 ajustado")

# 3. Panel D12-D15: contar la captura real (NORMALIZADO)
nz = wb.Worksheets("NORMALIZADO")
hdr = {}
for c in range(1, 100):
    v = nz.Cells(2, c).Value
    if v:
        hdr[str(v).strip()] = c
pairs = [("D12.42", 194), ("D13.45", 195), ("D14.51", 196), ("D15.58", 197)]
for qid, r in pairs:
    c = hdr.get(qid)
    if not c:
        print("   ! no encontrado", qid); continue
    L = chr(64 + c) if c <= 26 else "A" + chr(64 + c - 26)
    sco.Cells(r, 2).Formula = f"=COUNT(NORMALIZADO!{L}3:{L}176)"
    sco.Cells(r, 3).Formula = f'=IF(B{r}=174,"completo",IF(B{r}=0,"pendiente","parcial"))'
print("panel D12-D15 ajustado")

xl.Calculation = -4105
xl.CalculateFull()
wb.Save()
wb.Close(SaveChanges=True)
xl.Quit()
print("OK")
