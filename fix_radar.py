# -*- coding: utf-8 -*-
import win32com.client as wc, openpyxl
PATH = r"C:\Users\acuba\eudrperu\PLANTILLA_INDICE_PVE_ISCAM.xlsx"
wv = openpyxl.load_workbook(PATH, data_only=True)
rd = wv["RADAR_BRECHAS"]
for cell in ("A24", "A26", "A34", "A35", "A1", "A21", "A22", "A23"):
    print(cell, "=", repr(rd[cell].value))

app = wc.DispatchEx("Excel.Application"); app.Visible = False; app.DisplayAlerts = False
wb = app.Workbooks.Open(PATH)
r = wb.Worksheets("RADAR_BRECHAS")

# ── B..L (D1-D11): "—" cuando no hay dato en el departamento ──
src = {
    "B": ("ISCAM_Score", 5), "C": ("SCORECARDS", 8), "D": ("ISCAM_Score", 7),
    "E": ("ISCAM_Score", 8), "F": ("SCORECARDS", 9), "G": ("SCORECARDS", 10),
    "H": ("ISCAM_Score", 11), "I": ("ISCAM_Score", 12), "J": ("ISCAM_Score", 13),
    "K": ("ISCAM_Score", 14), "L": ("ISCAM_Score", 15),
}
for col, (sheet, sc) in src.items():
    if sheet == "ISCAM_Score":
        f = f'=IFERROR(AVERAGEIF(ISCAM_Score!R4C3:R177C3,RC1,ISCAM_Score!R4C{sc}:R177C{sc}),"\u2014")'
    else:
        f = f'=IFERROR(AVERAGEIF(SCORECARDS!R3C16:R176C16,RC1,SCORECARDS!R3C{sc}:R176C{sc}),"\u2014")'
    r.Range(f"{col}3:{col}17").FormulaR1C1 = f

# ── M: promedio solo si hay >=7 dimensiones con dato ──
r.Range("M3:M17").FormulaR1C1 = '=IF(COUNT(RC[-11]:RC[-1])<7,"\u2014",IFERROR(AVERAGE(RC[-11]:RC[-1]),"\u2014"))'

# ── Corte por producto: "—" cuando no hay dato ──
prod = {"C": 37, "D": 35, "E": 38, "F": 26, "G": 27, "H": 28}
for col, sc in prod.items():
    f = f'=IFERROR(AVERAGEIF(MATRIZ_174!R3C4:R176C4,RC1,ISCAM_Score!R4C{sc}:R177C{sc}),"\u2014")'
    r.Range(f"{col}30:{col}31").FormulaR1C1 = f
    r.Range(f"{col}32").FormulaR1C1 = f'=IFERROR(AVERAGEIF(MATRIZ_174!R3C4:R176C4,"",ISCAM_Score!R4C{sc}:R177C{sc}),"\u2014")'

r.Range("A24").Value = "\u2b1c Gris (\u2014) — Sin dato capturado"
app.CalculateFull(); wb.Save(); wb.Close(SaveChanges=False); app.Quit()
print("\nradar actualizado")
