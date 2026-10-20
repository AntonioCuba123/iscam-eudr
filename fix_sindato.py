# -*- coding: utf-8 -*-
"""Opcion A — 'sin dato' honesto: deja de escribir ceros donde no hay medicion."""
import win32com.client as wc
import shutil, os, time

PATH = r"C:\Users\acuba\eudrperu\PLANTILLA_INDICE_PVE_ISCAM.xlsx"
BK = r"C:\Users\acuba\eudrperu\ISCAM\respaldos\PLANTILLA_INDICE_PVE_ISCAM.backup_2026-10-15_pre-sindato.xlsx"
os.makedirs(os.path.dirname(BK), exist_ok=True)
shutil.copyfile(PATH, BK)
print("backup:", os.path.exists(BK), os.path.getsize(BK))

app = wc.DispatchEx("Excel.Application")
app.Visible = False; app.DisplayAlerts = False
wb = app.Workbooks.Open(PATH)

# ── 1. Quitar ceros-placeholder ──────────────────────────────────────────
s = wb.Worksheets("ISCAM_Score")
sc = wb.Worksheets("SCORECARDS")
# D1,D4,D7,D8,D9,D10,D11 (columnas E,H,K,L,M,N,O) en ISCAM_Score
for col in ("E", "H", "K", "L", "M", "N", "O"):
    s.Range(f"{col}4:{col}177").ClearContents()
# D2,D5,D6 y PPWR en SCORECARDS (columnas H,I,J,M)
for col in ("H", "I", "J", "M"):
    sc.Range(f"{col}3:{col}176").ClearContents()
print("placeholders limpiados")

# ── 2. D2/D5/D6 propaga vacio en lugar de 0 ──────────────────────────────
s.Range("F4:F177").FormulaR1C1 = '=IF(SCORECARDS!R[-1]C[2]="","",SCORECARDS!R[-1]C[2])'
s.Range("I4:I177").FormulaR1C1 = '=IF(SCORECARDS!R[-1]C="","",SCORECARDS!R[-1]C)'
s.Range("J4:J177").FormulaR1C1 = '=IF(SCORECARDS!R[-1]C="","",SCORECARDS!R[-1]C)'

# ── 3. ISA-EUDR: exige D1..D9 completos, si no "N/A" ─────────────────────
s.Range("AK4:AK177").FormulaR1C1 = (
    '=IF(COUNT(RC[-32]:RC[-24])=9,'
    'IFERROR(ROUND(POWER(PRODUCT(RC[-32]:RC[-26]),1/7)*0.875+((RC[-25]+RC[-24])/2)*0.125,1),"N/A"),"N/A")'
)
# ── 4. ISA-Completo: "—" si ISA-EUDR o ISA-PV no son numericos ───────────
s.Range("AL4:AL177").FormulaR1C1 = (
    '=IF(OR(NOT(ISNUMBER(RC[-1])),NOT(ISNUMBER(RC[-3]))),"\u2014",'
    'ROUND(0.7*RC[-1]+0.3*RC[-3]*100,1))'
)
# ── 5. IP: "—" si D2..D9 incompletos ─────────────────────────────────────
s.Range("Z4:Z177").FormulaR1C1 = (
    '=IF(COUNT(RC[-20]:RC[-13])<8,"\u2014",IFERROR(ROUND(AVERAGE(RC[-10]:RC[-6]),1),"\u2014"))'
)
# ── 6. RE: "—" si IP no es numerico ──────────────────────────────────────
s.Range("AB4:AB177").FormulaR1C1 = (
    '=IF(NOT(ISNUMBER(RC[-2])),"\u2014",IFERROR(ROUND(RC[-1]*(1-RC[-2]/100),1),"\u2014"))'
)
# ── 7. Tipologia: "Pendiente de instrumento" si IP no es numerico ────────
s.Range("AC4:AC177").FormulaR1C1 = (
    '=IF(OR(NOT(ISNUMBER(RC[-3])),NOT(ISNUMBER(RC[-2]))),"\u2b1c  Pendiente de instrumento",'
    'IF(AND(RC[-3]>=50,RC[-2]<50),"\U0001f7e2  Resilientes",'
    'IF(AND(RC[-3]>=50,RC[-2]>=50),"\U0001f7e0  Expuestas Adaptables",'
    'IF(AND(RC[-3]<50,RC[-2]<50),"\u2b1c  Riesgo Latente","\U0001f534  Riesgo Cr\u00edtico"))))'
)

# ── 8. MATRIZ_174: cobertura ISA-PV (AQ) y clasificacion parcial (T) ─────
m = wb.Worksheets("MATRIZ_174")
m.Range("AQ2").Value = "Cobertura ISA-PV (n de 8 componentes)"
m.Range("AQ3:AQ176").FormulaR1C1 = (
    '=COUNT(RC[-30])'
    '+IF(SCORECARDS!RC[-35]="",0,1)+IF(SCORECARDS!RC[-34]="",0,1)+IF(SCORECARDS!RC[-33]="",0,1)'
    '+IF(ISCAM_Score!R[1]C[-32]="",0,1)+IF(RC[-28]="",0,1)'
    '+IF(COUNT(RC[-20]:RC[-17])>0,1,0)'
)
m.Range("T3:T176").FormulaR1C1 = (
    '=IF(NOT(ISNUMBER(RC[-1])),"\u2014",IF(RC[23]<6,"\u2b1c  Parcial \u00b7 Inst. 2 pendiente",'
    'IF(RC[-1]<34,"\U0001f534 Cr\u00edtico",IF(RC[-1]<67,"\U0001f7e1 Vulnerable","\U0001f7e2 Preparado"))))'
)

# ── 9. SCORECARDS: resumen "Sin dato" cuenta "—" ─────────────────────────
sc.Range("A185").Value = "Sin dato (pendiente Inst. 2)"
sc.Range("B185").Value = '=COUNTIF(C3:C176,"\u2014")'

# ── 10. Nota metodologica + panel de cobertura ───────────────────────────
prev = s.Range("A180").Value
s.Range("A180").Value = prev + ("  |  Regla de dato faltante: mientras el Instrumento 2 no se levante, "
                                "ISA-EUDR, IP, RE e ISA-Completo se muestran como \u00ab\u2014\u00bb (sin dato), no como 0.")
rows = [
    ("COBERTURA DE CAPTURA POR DIMENSIÓN  (n de 174)", None, None),
    ("D1 — Clasificación regulatoria", "=COUNT(E4:E177)", None),
    ("D2 — Trazabilidad", "=COUNT(F4:F177)", None),
    ("D3 — Legalidad OSCE/OEFA", "=COUNT(G4:G177)", None),
    ("D4 — Deforestación cero", "=COUNT(H4:H177)", None),
    ("D5 — Diligencia debida", "=COUNT(I4:I177)", None),
    ("D6 — Capacidad digital", "=COUNT(J4:J177)", None),
    ("D7 — Presión comprador", "=COUNT(K4:K177)", None),
    ("D8 — Gobernanza", "=COUNT(L4:L177)", None),
    ("D9 — Riesgo financiero", "=COUNT(M4:M177)", None),
    ("D10 — Certificación", "=COUNT(N4:N177)", None),
    ("D11 — Ecosistema de apoyo", "=COUNT(O4:O177)", None),
    ("D12 — Huella de carbono", "=COUNT(MATRIZ_174!W3:W176)", None),
    ("D13 — Reporte sostenibilidad", "=COUNT(MATRIZ_174!X3:X176)", None),
    ("D14 — Economía circular", "=COUNT(MATRIZ_174!Y3:Y176)", None),
    ("D15 — Fitosanitario / LMR", "=COUNT(MATRIZ_174!Z3:Z176)", None),
    ("Certificación (Score Cert)", "=COUNT(MATRIZ_174!O3:O176)", None),
    ("Organizaciones con ISA-EUDR/IP computables", "=COUNT(Z4:Z177)", None),
]
r0 = 182
for i, (a, b, c) in enumerate(rows):
    r = r0 + i
    s.Cells(r, 1).Value = a
    if b:
        s.Cells(r, 2).Value = b
        s.Cells(r, 3).Value = f'=IF(B{r}=174,"completo",IF(B{r}=0,"pendiente","parcial"))'
s.Range(f"A{r0+len(rows)+1}").Value = (
    "ISA-EUDR requiere D1–D7 + D8–D9; IP requiere D2–D9. Ninguna se computa hasta levantar el Instrumento 2 "
    "(119 preguntas, hoja INSTRUMENTO_2_PREGUNTAS)."
)

app.CalculateFull()
wb.Save()
wb.Close(SaveChanges=False)
app.Quit()
time.sleep(1)
print("guardado OK")
