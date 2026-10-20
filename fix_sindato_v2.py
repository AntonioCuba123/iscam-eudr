# -*- coding: utf-8 -*-
"""Aplica el criterio «sin dato» a MATRIZ_174 y su cascada.

Regla: un cero de relleno (falta de dato) pasa a «» (celda vacía); un cero
medido se conserva.  Se corrigen además:

  * H/I  (Cert. Orgánica / Fairtrade): venían truncadas a 3 caracteres por
    build_pve_index.py (str(...)[:3]) -> se recodifican a SI/NO/«» desde el
    texto fuente de MATRIZ_ORGANIZACIONES_174_FINAL.csv.
  * M    (% UE/FOB): «» si no hay FOB total (no es «no exporta»).
  * O    (score de certificación): «» si no hay información de certificación.
  * L, E (FOB UE, FOB total): se vacían los ceros de relleno (orgs sin DUAs).
  * AA..AN (P1..P14): indicadores no levantados -> vacío.
  * ISCAM_Score U/X/T (IV1, IV4, IP5) y SCORECARDS F: propagan «».
"""
import os
import shutil
import datetime

import pandas as pd
import win32com.client as win32

ROOT = r"C:\Users\acuba\eudrperu"
XLS = os.path.join(ROOT, "PLANTILLA_INDICE_PVE_ISCAM.xlsx")
CSV = os.path.join(ROOT, "BASE CAFE CACAO 174", "MATRIZ_ORGANIZACIONES_174_FINAL.csv")

# ── respaldo ───────────────────────────────────────────────────────────────
ts = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
bk = os.path.join(ROOT, "ISCAM", "respaldos",
                  "PLANTILLA_INDICE_PVE_ISCAM.backup_%s_pre-sindato.xlsx" % ts)
shutil.copy2(XLS, bk)
print("respaldo:", os.path.basename(bk))


# ── recodificación de certificaciones ──────────────────────────────────────
def org_flag(t):
    """Certificación orgánica: cualquier texto hallado es una certificación."""
    if t is None or (isinstance(t, float)):
        return ""
    s = str(t).strip()
    if not s:
        return ""
    if s.lower().startswith("no"):
        return "NO"
    return "SI"


def ft_flag(t):
    """Fairtrade: «en proceso» = aún no vigente; «orgánica» mal ubicada = sin dato."""
    if t is None or (isinstance(t, float)):
        return ""
    s = str(t).strip().lower()
    if not s:
        return ""
    if "organica" in s or "orgánica" in s:
        return ""            # dato mal puesto en la columna [R]
    if s == "no" or "proceso" in s:
        return "NO"
    return "SI"


df = pd.read_csv(CSV, encoding="utf-8-sig")
C_ORG, C_FT = "Cert. Orgánica (interno)", "Cert. Comercio Justo (interno)"
cert = {}
for _, r in df.iterrows():
    ruc = str(r["RUC"]).strip()
    if str(r[C_ORG]) not in ("nan", "") or str(r[C_FT]) not in ("nan", ""):
        cert[ruc] = (org_flag(r[C_ORG]), ft_flag(r[C_FT]),
                     "" if str(r[C_ORG]) == "nan" else str(r[C_ORG]).strip(),
                     "" if str(r[C_FT]) == "nan" else str(r[C_FT]).strip())
print("certificaciones a recodificar:", len(cert))
ambi = [k for k, v in cert.items() if v[1] == ""]
print("  FT sin dato (ambiguo) [R]:", ambi)

# ── Excel ──────────────────────────────────────────────────────────────────
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

# comprobación de alineación SCORECARDS <-> MATRIZ_174
des = 0
for r in range(3, 177):
    if str(sc.Cells(r, 1).Value) != str(mz.Cells(r, 1).Value):
        des += 1
print("desalineación SCORECARDS vs MATRIZ_174:", des)
desk = 0
for r in range(4, 178):
    if str(sco.Cells(r, 1).Value) != str(mz.Cells(r - 1, 1).Value):
        desk += 1
print("desalineación ISCAM_Score vs MATRIZ_174:", desk)

# 1) H/I recodificadas + texto fuente en AR/AS
mz.Range("AR2").Value = "Cert. Orgánica — texto fuente (interno)"
mz.Range("AS2").Value = "Cert. Comercio Justo — texto fuente (interno)"
n = 0
for r in range(3, 177):
    ruc = str(mz.Cells(r, 1).Value).strip()
    if ruc in cert:
        h, i, txt_h, txt_i = cert[ruc]
        mz.Cells(r, 8).Value = h
        mz.Cells(r, 9).Value = i
        mz.Cells(r, 44).Value = txt_h
        mz.Cells(r, 45).Value = txt_i
        n += 1
print("H/I recodificadas:", n)

# 2) L y E: vaciar ceros de relleno (orgs sin DUAs)
cle = cll = 0
for r in range(3, 177):
    e = mz.Cells(r, 5).Value
    f = mz.Cells(r, 6).Value
    tiene_duas = isinstance(f, (int, float)) and f > 0
    if isinstance(e, (int, float)) and e == 0:
        mz.Cells(r, 5).ClearContents()
        cle += 1
    if not tiene_duas and isinstance(mz.Cells(r, 12).Value, (int, float)) and mz.Cells(r, 12).Value == 0:
        mz.Cells(r, 12).ClearContents()
        cll += 1
print("E vaciadas:", cle, "| L vaciadas:", cll)

# 3) P1..P14 (AA..AN): indicadores no levantados
mz.Range("AA3:AN176").ClearContents()
print("P1..P14 (AA:AN) vaciadas")

# 4) fórmulas M y O
mz.Range("M3").FormulaR1C1 = '=IF(RC[-8]>0,ROUND(RC[-1]/RC[-8]*100,1),"")'
mz.Range("M3:M176").FillDown()
mz.Range("O3").FormulaR1C1 = ('=IF(AND(RC[-7]="",RC[-6]=""),"",'
                              'IF(RC[-7]="SI",1,0)*0.6+IF(RC[-6]="SI",1,0)*0.4)')
mz.Range("O3:O176").FillDown()

# 5) cascada ISCAM_Score
sco.Range("U4").Formula = '=IF(ISNUMBER(MATRIZ_174!M3),MIN(100,ROUND(MATRIZ_174!M3,1)),"")'
sco.Range("U4:U177").FillDown()
sco.Range("X4").Formula = ('=IF(ISNUMBER(MATRIZ_174!O3),MIN(100,IF(MATRIZ_174!O3=0,70,30)'
                           '+IF(MATRIZ_174!U3="",0,0.3*(100-MATRIZ_174!U3*100))),"")')
sco.Range("X4:X177").FillDown()
sco.Range("T4").Formula = ('=IF(ISNUMBER(MATRIZ_174!O3),IFERROR((K4+M4+MATRIZ_174!O3)/3,0),"")')
sco.Range("T4:T177").FillDown()

# 6) SCORECARDS F (FOB UE) honesto
sc.Range("F3").Formula = '=IF(MATRIZ_174!L3="","",MATRIZ_174!L3)'
sc.Range("F3:F176").FillDown()

# 7) nota al pie de MATRIZ_174
r = 179
mz.Cells(r, 1).Value = "REGLA «SIN DATO» (2026-10-15)"
mz.Cells(r, 1).Font.Bold = True
mz.Cells(r + 1, 1).Value = ("Un cero de relleno (falta de dato) se muestra como celda vacía, nunca como 0. "
                            "Se vaciaron: L (FOB UE) y E (FOB total) de las organizaciones sin DUAs; "
                            "P1..P14 (indicadores no levantados). M (% UE/FOB) y O (score de certificación) "
                            "devuelven «» cuando falta el insumo. H/I venían truncadas a 3 caracteres y se "
                            "recodificaron a SI/NO/«» desde la fuente (texto original en AR/AS). "
                            "Un cero medido —por ejemplo, una organización que exporta pero no a la UE— se conserva.")
mz.Cells(r + 1, 1).WrapText = True

xl.Calculation = -4105
xl.CalculateFull()
wb.Save()

# ── reporte ────────────────────────────────────────────────────────────────
print()
print("fila   M(%UE)   O(cert)   IV1(U)   IV4(X)   IP5(T)   ISA-PV   PVE")
for fr in [3, 4, 5, 22, 30, 46, 100, 176]:
    ir = fr + 1          # MATRIZ fila 3 <-> ISCAM_Score fila 4
    print("  %3d   %-7s  %-8s  %-7s  %-7s  %-7s  %-7s  %s" % (
        fr,
        mz.Cells(fr, 13).Value, mz.Cells(fr, 15).Value,
        sco.Cells(ir, 21).Value, sco.Cells(ir, 24).Value, sco.Cells(ir, 20).Value,
        sco.Cells(ir, 35).Value, mz.Cells(fr, 19).Value))

wb.Close(SaveChanges=True)
xl.Quit()
print("OK")
