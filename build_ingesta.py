# -*- coding: utf-8 -*-
"""
Construye la capa de ingesta del Instrumento 2 en la plantilla ISCAM:
  · CODIFICACION  — tabla opción de respuesta → puntaje 0-100 (manual de codificación)
  · CAPTURA       — una fila por organización, una columna por pregunta (entrada de datos)
  · NORMALIZADO   — 0-100 por pregunta + agregados D1-D11

Y cablea el motor: ISCAM_Score!E:O y SCORECARDS!H/I/J y MATRIZ_174!W:Z.
Usa Excel COM (no openpyxl) para preservar valores en caché, comentarios y VML.

⚠ Este script NO es un «rebuild» completo: no incluye las correcciones posteriores
aplicadas sobre el libro por `fix_sindato_v2.py` (recodificación de certificaciones,
ceros de relleno → «sin dato», cascada IV1/IV4/IP5), `fix_umbral_pv.py` (umbral
ISA-PV) ni `fix_ratificacion.py` (ratificación [R] aplicada en vivo). Volver a
ejecutarlo sobre el libro actual revertiría esos arreglos.
"""
import importlib.util, shutil, datetime, os
import openpyxl
from openpyxl.utils import get_column_letter
import win32com.client as win32

ROOT = r"C:\Users\acuba\eudrperu"
PATH = os.path.join(ROOT, "PLANTILLA_INDICE_PVE_ISCAM.xlsx")

# ── 0. Respaldo ─────────────────────────────────────────────────────────────
ts = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
os.makedirs(os.path.join(ROOT, "ISCAM", "respaldos"), exist_ok=True)
bak = os.path.join(ROOT, "ISCAM", "respaldos", f"PLANTILLA_INDICE_PVE_ISCAM.backup_{ts}_pre-ingesta.xlsx")
shutil.copy2(PATH, bak)
print("respaldo:", bak)

# ── 1. Especificación de codificación ──────────────────────────────────────
sp = importlib.util.spec_from_file_location("cod", os.path.join(ROOT, "codificacion_instrumento2.py"))
cod = importlib.util.module_from_spec(sp); sp.loader.exec_module(cod)

# Ratificación [R] (2026-10-15): los ítems que no promedian traen su motivo y los
# que sí promedian traen su dirección ratificada. Ambos viven en el archivo de
# codificación, que es la fuente única de estas decisiones.
NO_PROMEDIA = cod.NO_PROMEDIA
RULING = cod.RULING


def nota_de(qid):
    """Nota de la fila en CODIFICACION (motivo de no promediar o dirección ratificada)."""
    if qid in NO_PROMEDIA:
        return "  · " + NO_PROMEDIA[qid]
    if qid in RULING:
        return "  · " + RULING[qid]
    return ""

# ── 2. Leer el instrumento (orden canónico) ────────────────────────────────
wbx = openpyxl.load_workbook(PATH, data_only=True)
wsi = wbx["INSTRUMENTO_2_PREGUNTAS"]
QS = []
for r in range(3, wsi.max_row + 1):
    sid = wsi.cell(r, 2).value
    if not sid:
        continue
    QS.append(dict(id=sid, sec=wsi.cell(r, 1).value, bloque=wsi.cell(r, 3).value,
                   texto=wsi.cell(r, 4).value, tipo=wsi.cell(r, 5).value,
                   op=wsi.cell(r, 6).value, dest=wsi.cell(r, 7).value))
QIDX = {q["id"]: q for q in QS}
print("preguntas:", len(QS))


def spec_of(qid):
    v = cod.TABLA.get(qid)
    if v is None:
        return ("NP", "no_puntua")
    return v


def ops_of(qid):
    t = QIDX[qid]["op"]
    if not t or t == "—":
        return []
    return [o.strip() for o in str(t).split(" / ")]


SCORING = [q["id"] for q in QS if spec_of(q["id"])[0] in ("O", "E", "N", "C", "Cn", "X")]
print("preguntas que puntúan:", len(SCORING))

DIMS = cod.DIMS
for d, qs in DIMS:
    for q in qs:
        assert q in SCORING, f"{q} no puntúa pero está en {d}"

# RUC y razón social en orden MATRIZ_174 (filas 3..176)
wsm = wbx["MATRIZ_174"]
ORGS = [(wsm.cell(r, 1).value, wsm.cell(r, 2).value) for r in range(3, 177)]
print("organizaciones:", len(ORGS))
OLD_WZ = [[wsm.cell(r, c).value for c in range(23, 27)] for r in range(3, 177)]  # W,X,Y,Z literales

# ── 3. Layout de columnas ──────────────────────────────────────────────────
CAP = {}   # qid -> columna en CAPTURA
c = 3
for q in QS:
    CAP[q["id"]] = c; c += 1
NOR = {}   # qid -> columna en NORMALIZADO
c = 3
for qid in SCORING:
    NOR[qid] = c; c += 1
DIMCOL = {}
for d, _ in DIMS:
    DIMCOL[d] = c; c += 1
LAST_NORM_COL = c - 1
print(f"CAPTURA cols C:{2+len(QS)}  |  NORMALIZADO cols C:{LAST_NORM_COL}")

# ── 4. Filas de CODIFICACION ───────────────────────────────────────────────
cod_rows, opt_rng = [], {}
r = 3
for q in QS:
    qid = q["id"]; t, val = spec_of(qid)
    nota = nota_de(qid)
    if t == "O":
        start = r
        for op, sc in val:
            cod_rows.append([qid, q["bloque"], q["tipo"], op,
                             ("sin dato" if sc is None else sc),
                             f"{qid}|{op}",
                             ("«sin dato» no promedia" if sc is None else "") + nota])
            r += 1
        opt_rng[qid] = (start, r - 1)
    elif t == "E":
        cod_rows.append([qid, q["bloque"], q["tipo"], "(todas las opciones 0–4)", "", "", "Escala 0-4 ×25 → 0-100" + nota]); r += 1
    elif t == "N":
        cod_rows.append([qid, q["bloque"], q["tipo"], "(valor numérico)", "", "", "Valor nativo 0-100" + nota]); r += 1
    elif t == "C":
        cod_rows.append([qid, q["bloque"], q["tipo"], "(casillas múltiples, separar con «;»)", "", "",
                         f"Puntaje = (n.º marcados ÷ {val}) × 100" + nota]); r += 1
    elif t == "Cn":
        cod_rows.append([qid, q["bloque"], q["tipo"], "(casillas múltiples, separar con «;»)", "", "",
                         f"Puntaje = (n.º marcados ÷ {val}) × 100; «Ninguno» = 0" + nota]); r += 1
    elif t == "X":
        cod_rows.append([qid, q["bloque"], q["tipo"], "(casillas múltiples, separar con «;»)", "", "",
                         "Puntaje = (% de destinos de la UE sobre el total marcado) × 100" + nota]); r += 1
    else:
        cod_rows.append([qid, q["bloque"], q["tipo"], q["op"] if q["op"] != "—" else "—", "", "",
                         cod.REGLAS.get(val, str(val)) + nota]); r += 1
print("filas CODIFICACION:", len(cod_rows))

# ── 5. Abrir Excel y construir ─────────────────────────────────────────────
xl = win32.Dispatch("Excel.Application")
xl.Visible = False
xl.DisplayAlerts = False
xl.ScreenUpdating = False
xl.EnableEvents = False
wb = xl.Workbooks.Open(PATH)
xl.Calculation = -4135  # xlCalculationManual
try:
    wb.Unprotect()
except Exception:
    pass

for nm in ("CODIFICACION", "CAPTURA", "NORMALIZADO"):
    try:
        wb.Worksheets(nm).Delete()
    except Exception:
        pass

ANCHOR = wb.Worksheets("ISCAM_Score")
_N0 = wb.Worksheets.Count
_ORDEN = ["INSTRUCCIONES", "INSTRUMENTO_2_PREGUNTAS", "CODIFICACION", "CAPTURA",
          "NORMALIZADO", "ISCAM_Score", "PONDERADORES", "MATRIZ_174", "SCORECARDS",
          "RADAR_BRECHAS"]


def add_before(name, k):
    """Inserta una hoja justo antes de ISCAM_Score (nunca usar Move: borra hojas)."""
    h = wb.Worksheets.Add(Before=ANCHOR)
    h.Name = name
    if wb.Worksheets.Count != _N0 + k:
        raise RuntimeError(f"n.º de hojas inesperado tras crear {name}: {wb.Worksheets.Count}")
    return h


# ---------- 5.1 CODIFICACION ----------
ws = add_before("CODIFICACION", 1)
ws.Range("A1:G1").Merge()
ws.Range("A1").Value = ("CODIFICACIÓN — Instrumento 2 · opción de respuesta → puntaje 0-100.  "
                        "100 = mejor alineamiento con el EUDR.  «sin dato» = no se promedia.  "
                        "Banderas, mapeos y bloques 0/P se capturan y reportan por separado: no entran a ningún promedio.")
ws.Range("A2:G2").Value = [["ID", "Sección / Bloque", "Tipo de campo", "Opción de respuesta",
                            "Puntaje (0-100)", "Clave (ID|Opción)", "Nota"]]
if cod_rows:
    ws.Range(ws.Cells(3, 1), ws.Cells(2 + len(cod_rows), 7)).Value = cod_rows
ws.Range("A2:G2").Font.Bold = True
ws.Range("A1:G1").Font.Bold = True
ws.Range("A1").WrapText = True
ws.Rows(1).RowHeight = 42
for col, w in zip("ABCDEFG", (11, 30, 22, 62, 13, 34, 46)):
    ws.Columns(col).ColumnWidth = w
ws.Columns("D").WrapText = True
ws.Columns("G").WrapText = True
ws.Range("A2:G2").Interior.Color = 0xD9D9D9
ws.Range("E3:E" + str(2 + len(cod_rows))).HorizontalAlignment = -4108

# ---------- 5.2 CAPTURA ----------
ws = add_before("CAPTURA", 2)
last_col = 2 + len(QS)
hdr = ["RUC", "Razón Social"] + [q["id"] for q in QS]
short = ["", ""] + [(str(q["texto"])[:60] if q["texto"] else "") for q in QS]
ws.Range(ws.Cells(1, 1), ws.Cells(1, last_col)).Merge()
ws.Range("A1").Value = ("CAPTURA — Instrumento 2 (119 preguntas · 1 respuesta por cooperativa).  "
                        "Pegue aquí las respuestas del formulario; el motor calcula solo.  "
                        "Casillas múltiples: separe con «;».  El enunciado completo está en INSTRUMENTO_2_PREGUNTAS.")
ws.Range("A1").WrapText = True
ws.Rows(1).RowHeight = 34
ws.Range(ws.Cells(2, 1), ws.Cells(2, last_col)).Value = [hdr]
ws.Range(ws.Cells(3, 1), ws.Cells(2 + len(ORGS), 2)).Value = [list(o) for o in ORGS]
ws.Range("A2").Value = "RUC (clave de unión)"
ws.Range(ws.Cells(2, 1), ws.Cells(2, last_col)).Font.Bold = True
ws.Range(ws.Cells(2, 1), ws.Cells(2, last_col)).Orientation = 90
ws.Rows(2).RowHeight = 150
ws.Columns(1).ColumnWidth = 15
ws.Columns(2).ColumnWidth = 42
ws.Range(ws.Cells(2, 3), ws.Cells(2, last_col)).ColumnWidth = 8.5
ws.Range(ws.Cells(2, 1), ws.Cells(2, last_col)).Interior.Color = 0xC6EFCE
ws.Rows(2).HorizontalAlignment = -4108
ws.Rows(2).VerticalAlignment = -4108
ws.Activate()
xl.ActiveWindow.FreezePanes = False
ws.Range("C3").Select()
xl.ActiveWindow.FreezePanes = True
print("CAPTURA base escrita")

# validaciones y comentarios
nval = 0
for q in QS:
    qid = q["id"]; col = CAP[qid]; t, val = spec_of(qid)
    rng = ws.Range(ws.Cells(3, col), ws.Cells(2 + len(ORGS), col))
    try:
        rng.Validation.Delete()
    except Exception:
        pass
    if t == "O" and qid in opt_rng:
        a, b = opt_rng[qid]
        try:
            rng.Validation.Add(3, 1, 1, f"=CODIFICACION!$D${a}:$D${b}")
            rng.Validation.IgnoreBlank = True
            rng.Validation.InCellDropdown = True
            nval += 1
        except Exception as e:
            print("   ! validación", qid, e)
    elif t == "E":
        rng.Validation.Add(1, 1, 1, "0", "4")
        rng.Validation.ErrorMessage = "Escala 0 a 4"
    elif t == "N":
        rng.Validation.Add(1, 1, 1, "0", "100")
        rng.Validation.ErrorMessage = "Valor 0 a 100"
print("validaciones tipo lista:", nval)
ws.Range("A1").Font.Bold = True

# ---------- 5.3 NORMALIZADO ----------
ws = add_before("NORMALIZADO", 3)
nc = LAST_NORM_COL
ws.Range(ws.Cells(1, 1), ws.Cells(1, nc)).Merge()
ws.Range("A1").Value = ("NORMALIZADO — 0-100 automático (hoja de cálculo, no editar).  "
                        "Lee CAPTURA y aplica CODIFICACION; los vacíos se propagan como «sin dato».")
ws.Range("A1").Font.Bold = True
hd = [["RUC", "Razón Social"] + SCORING + [d for d, _ in DIMS]]
ws.Range(ws.Cells(2, 1), ws.Cells(2, nc)).Value = hd
ws.Range(ws.Cells(2, 1), ws.Cells(2, nc)).Font.Bold = True
ws.Rows(2).RowHeight = 60
ws.Range(ws.Cells(2, 3), ws.Cells(2, nc)).Orientation = 90
ws.Range(ws.Cells(2, 1), ws.Cells(2, nc)).Interior.Color = 0xDDEBF7
ws.Columns(1).ColumnWidth = 15
ws.Columns(2).ColumnWidth = 30
ws.Range(ws.Cells(2, 3), ws.Cells(2, nc)).ColumnWidth = 8.5

last_norm_row = 2 + len(ORGS)


def ref(qid):
    d = CAP[qid] - NOR[qid]
    return "RC" if d == 0 else f"RC[{d}]"


ws.Range(ws.Cells(3, 1), ws.Cells(last_norm_row, 1)).FormulaR1C1 = "=CAPTURA!RC"
ws.Range(ws.Cells(3, 2), ws.Cells(last_norm_row, 2)).FormulaR1C1 = "=CAPTURA!RC[1]"

LOOK = "INDEX(CODIFICACION!R2C5:R500C5,MATCH({k}&{r},CODIFICACION!R2C6:R500C6,0))"
for q in QS:
    qid = q["id"]
    if qid not in NOR:
        continue
    t, val = spec_of(qid)
    r = "CAPTURA!" + ref(qid)
    if t == "O":
        key = '"' + qid + '|"'
        f = (f'=IF({r}="","",IFERROR(IF({LOOK.format(k=key, r=r)}="sin dato","",'
             f'{LOOK.format(k=key, r=r)}),"⚠"))')
    elif t == "E":
        f = f'=IF({r}="","",IF(AND(ISNUMBER({r}),{r}>=0,{r}<=4),{r}*25,"⚠"))'
    elif t == "N":
        f = f'=IF({r}="","",IF(ISNUMBER({r}),MAX(0,MIN(100,{r})),"⚠"))'
    elif t == "C":
        n = val
        f = (f'=IF({r}="","",MIN(100,ROUND((LEN({r})-LEN(SUBSTITUTE({r},";",""))+1)/{n}*100,1)))')
    elif t == "Cn":
        n = val
        f = (f'=IF({r}="","",IF(ISNUMBER(SEARCH("Ninguno",{r})),0,'
             f'MIN(100,ROUND((LEN({r})-LEN(SUBSTITUTE({r},";",""))+1)/{n-1}*100,1))))')
    else:  # X — B0.8 destinos UE
        eu = ["Alemania", "Bélgica", "Países Bajos", "Francia", "Italia", "España", "Suecia", "Dinamarca"]
        cnt = "+".join([f'ISNUMBER(SEARCH("{e}",{r}))' for e in eu])
        f = (f'=IF({r}="","",ROUND(({cnt})/((LEN({r})-LEN(SUBSTITUTE({r},";","")))+1)*100,1))')
    c = NOR[qid]
    ws.Range(ws.Cells(3, c), ws.Cells(last_norm_row, c)).FormulaR1C1 = f

for d, qs in DIMS:
    parts = []
    for q in qs:
        off = NOR[q] - DIMCOL[d]
        parts.append("RC" if off == 0 else f"RC[{off}]")
    f = f'=IFERROR(AVERAGE({",".join(parts)}),"")'
    ws.Range(ws.Cells(3, DIMCOL[d]), ws.Cells(last_norm_row, DIMCOL[d])).FormulaR1C1 = f
ws.Range(ws.Cells(2, 3), ws.Cells(2, nc)).Font.Size = 9
print("NORMALIZADO escrito")

# ---------- 5.4 Cableado del motor ----------
sco = wb.Worksheets("ISCAM_Score")
# E=D1, F=D2, G=D3, H=D4, I=D5, J=D6, K=D7, L=D8, M=D9, N=D10, O=D11
for dim, c in [("D1", 5), ("D2", 6), ("D3", 7), ("D4", 8), ("D5", 9), ("D6", 10),
               ("D7", 11), ("D8", 12), ("D9", 13), ("D10", 14), ("D11", 15)]:
    nd = DIMCOL[dim]
    rr = f"NORMALIZADO!R[-1]C[{nd-c}]"
    if dim == "D3":
        f = (f'=IF({rr}="",IFERROR(MATRIZ_174!R[-1]C[14]*100,""),{rr})')
    else:
        f = f'=IF({rr}="","",{rr})'
    sco.Range(sco.Cells(4, c), sco.Cells(177, c)).FormulaR1C1 = f
print("ISCAM_Score E:O cableado")

sc = wb.Worksheets("SCORECARDS")
for dim, c in [("D2", 8), ("D5", 9), ("D6", 10)]:
    nd = DIMCOL[dim]
    f = f'=IF(NORMALIZADO!RC[{nd-c}]="","",NORMALIZADO!RC[{nd-c}])'
    sc.Range(sc.Cells(3, c), sc.Cells(176, c)).FormulaR1C1 = f
print("SCORECARDS H:J cableado")

mz = wb.Worksheets("MATRIZ_174")
for dim, c in [("D12.42", 23), ("D13.45", 24), ("D14.51", 25), ("D15.58", 26)]:
    nd = NOR[dim]
    for i in range(len(ORGS)):
        old = OLD_WZ[i][c - 23]
        old = "" if old is None else old
        f = f'=IF(NORMALIZADO!RC[{nd-c}]="",{old!r},NORMALIZADO!RC[{nd-c}])'
        mz.Cells(3 + i, c).FormulaR1C1 = f
print("MATRIZ_174 W:Z cableado")

# ISA-PV (AP): tolerar componentes vacíos sin romper ("" ÷ 100 daba #VALUE!)
AP_F = ('=IFERROR(((RC[-29]/100)*PONDERADORES!R12C4'
        '+IFERROR(SCORECARDS!RC[-34]/100,0)*PONDERADORES!R13C4'
        '+IFERROR(SCORECARDS!RC[-33]/100,0)*PONDERADORES!R14C4'
        '+IFERROR(SCORECARDS!RC[-32]/100,0)*PONDERADORES!R15C4'
        '+IFERROR(ISCAM_Score!R[1]C[-31]/100,0)*PONDERADORES!R16C4'
        '+IFERROR(RC[-27],0)*PONDERADORES!R17C4'
        '+0*PONDERADORES!R18C4'
        '+(AVERAGE(RC[-19]:RC[-16])/2)*PONDERADORES!R19C4)/PONDERADORES!R20C4,"N/A")')
mz.Range("AP3:AP176").FormulaR1C1 = AP_F
print("ISA-PV (MATRIZ_174!AP) blindado")

# IV2 (V): conservar la base 50 del bloque IV cuando D1 no es numérico
sco.Range("V4:V177").FormulaR1C1 = '=IF(OR(NOT(ISNUMBER(RC[-16])),RC[-16]=0),50,RC[-16])'
print("IV2 ajustado")

# ---------- 5.5 Panel de cobertura ----------
panel = [("D1 — Clasificación regulatoria", "E"), ("D2 — Trazabilidad", "F"),
         ("D3 — Legalidad OSCE/OEFA + encuesta", "G"), ("D4 — Deforestación cero", "H"),
         ("D5 — Diligencia debida", "I"), ("D6 — Capacidad digital", "J"),
         ("D7 — Presión comprador", "K"), ("D8 — Gobernanza", "L"),
         ("D9 — Riesgo financiero", "M"), ("D10 — Certificación", "N"),
         ("D11 — Ecosistema de apoyo", "O")]
sco.Range("A182").Value = "COBERTURA DE CAPTURA POR DIMENSIÓN  (n de 174)  — calculada sobre NORMALIZADO"
sco.Range("A182").Font.Bold = True
for i, (lbl, col) in enumerate(panel):
    rr = 183 + i
    sco.Cells(rr, 1).Value = lbl
    sco.Cells(rr, 2).Formula = f"=COUNT({col}$4:{col}$177)"
    sco.Cells(rr, 3).Formula = f'=IF(B{rr}=174,"completo",IF(B{rr}=0,"pendiente","parcial"))'
r2 = 183 + len(panel)
for lbl, qid in [("D12 — Huella de carbono (=1 «en curso»)", "D12.42"),
                 ("D13 — Reporte sostenibilidad", "D13.45"),
                 ("D14 — Economía circular", "D14.51"),
                 ("D15 — Fitosanitario / LMR", "D15.58")]:
    L = get_column_letter(NOR[qid])
    sco.Cells(r2, 1).Value = lbl
    sco.Cells(r2, 2).Formula = f"=COUNT(NORMALIZADO!{L}3:{L}176)"
    sco.Cells(r2, 3).Formula = f'=IF(B{r2}=174,"completo",IF(B{r2}=0,"pendiente","parcial"))'
    r2 += 1
sco.Cells(r2, 1).Value = "Organizaciones con ISA-EUDR computable (≥7 de D1–D9)"
sco.Cells(r2, 2).Formula = "=COUNT(AK4:AK177)"
sco.Cells(r2, 3).Formula = f'=IF(B{r2}=0,"pendiente",IF(B{r2}=174,"completo","parcial"))'
r2 += 1
sco.Cells(r2, 1).Value = "Organizaciones con IP computable (8 de D2–D9)"
sco.Cells(r2, 2).Formula = "=COUNT(Z4:Z177)"
sco.Cells(r2, 3).Formula = f'=IF(B{r2}=0,"pendiente",IF(B{r2}=174,"completo","parcial"))'
print("panel de cobertura actualizado")

fin = [wb.Worksheets(i).Name for i in range(1, wb.Worksheets.Count + 1)]
print("orden final:", fin)
assert fin == _ORDEN, f"orden inesperado: {fin}"

# ── 6. Recalcular y guardar ────────────────────────────────────────────────
xl.Calculation = -4105  # xlCalculationAutomatic
xl.CalculateFull()
wb.Save()
wb.Close(SaveChanges=True)
xl.Quit()
print("OK — guardado.")
