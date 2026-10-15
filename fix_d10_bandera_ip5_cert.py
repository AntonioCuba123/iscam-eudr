# -*- coding: utf-8 -*-
"""
Dos correcciones metodológicas ratificadas contra las fuentes (2026-10-15):

1) D10 = BANDERA PURA (no promedia).
   Fuentes: §7.3 de la metodología ISA —«D10 · Certificación (bandera) | instrumento
   (D10.36, D10.37, D10.36a) | Bandera: no promedia»—; nota de puntaje del Instrumento 2
   («dimensión extendida — bandera de alerta, no promedio de madurez»); Tabla 4 del
   documento de trabajo (Q36 y Q37 son «Bandera»; la dimensión «bandera — no promedia»);
   Matriz de Cobertura Técnica (D10.36 «fuera de IP»). La hoja INSTRUMENTO_2_PREGUNTAS
   de este mismo libro ya declaraba los tres ítems como «bandera, no promedia».
   → NORMALIZADO!CK (D10) deja de promediar D10.36a y queda en «». El ítem sigue
     capturado (CAPTURA!CX) y normalizado (NORMALIZADO!BS), sólo se reporta aparte.

2) IP5 · componente certificación = CONTEO 0/33/66/100 (no el score ponderado 0,6/0,4).
   Fuente: Matriz de Cobertura Técnica —«IP5 recalculado (Certificaciones, conteo
   0/33/66/100)»—; §7.3 de la metodología ISA —«IP5 = (D7 + D9 + Certificación)/3»—.
   → MATRIZ_174!AU = n.º de certificaciones vigentes (B0.9 al cargar la encuesta;
     registro precensal H/I mientras tanto). MATRIZ_174!AV = 0/33/66/100.
     ISCAM_Score!T (IP5) usa AV y devuelve «» si falta cualquier componente.

Efectos colaterales corregidos (regla «sin dato = «», nunca 0»):
   · ISCAM_Score!T devolvía 0 cuando D7 o D9 estaban vacíos (el IFERROR los absorbía).
   · SCORECARDS!L («Cert 0-1») devolvía 0 de relleno con IFERROR(...,0).
"""
import os, shutil, datetime
import win32com.client as win32

ROOT = r"C:\Users\acuba\eudrperu"
PATH = os.path.join(ROOT, "PLANTILLA_INDICE_PVE_ISCAM.xlsx")
ts = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
bak = os.path.join(ROOT, "ISCAM", "respaldos", f"PLANTILLA_INDICE_PVE_ISCAM.backup_{ts}_pre-d10-bandera-ip5-cert.xlsx")
shutil.copy2(PATH, bak); print("respaldo:", bak)

xl = win32.Dispatch("Excel.Application")
xl.Visible = False; xl.DisplayAlerts = False; xl.EnableEvents = False
wb = xl.Workbooks.Open(PATH)

norm = wb.Worksheets("NORMALIZADO")
sc   = wb.Worksheets("ISCAM_Score")
m    = wb.Worksheets("MATRIZ_174")
card = wb.Worksheets("SCORECARDS")
rad  = wb.Worksheets("RADAR_BRECHAS")
preg = wb.Worksheets("INSTRUMENTO_2_PREGUNTAS")
pon  = wb.Worksheets("PONDERADORES")

# ── 1) D10 deja de promediar ────────────────────────────────────────────────
norm.Range("CK3:CK176").Formula = '=""'
sc.Range("N3").Value = "D10 \u2014 Certificaci\u00f3n\n(bandera; no promedia)"
sc.Range("A192").Value = "D10 \u2014 Certificaci\u00f3n (bandera, no promedia)"
sc.Range("A193").Value = "D11 \u2014 Ecosistema de apoyo (inventario, no promedia)"
rad.Range("K2").Value = "D10\nbandera"
rad.Range("L2").Value = "D11\ninventario"
print("D10: NORMALIZADO!CK vaciado (bandera pura).")

# ── 2) Conteo de certificaciones vigentes → 0/33/66/100 ─────────────────────
m.Range("AU2").Value = "Cert. vigentes (n)\nB0.9; si vac\u00edo, registro H/I"
m.Range("AV2").Value = "Score Cert IP5\n0/33/66/100 (conteo, no ponderado)"

for r in range(3, 177):
    m.Cells(r, 47).Formula = (
        '=IF(CAPTURA!N{r}<>"",'
        'ISNUMBER(SEARCH("Rainforest",CAPTURA!N{r}))+ISNUMBER(SEARCH("Fairtrade",CAPTURA!N{r}))'
        '+ISNUMBER(SEARCH("Org",CAPTURA!N{r}))+ISNUMBER(SEARCH("UTZ",CAPTURA!N{r}))'
        '+ISNUMBER(SEARCH("Otr",CAPTURA!N{r})),'
        'IF(AND(H{r}="",I{r}=""),"",IF(H{r}="SI",1,0)+IF(I{r}="SI",1,0)))'
    ).format(r=r)
    m.Cells(r, 48).Formula = '=IF(AU{r}="","",CHOOSE(MIN(3,AU{r})+1,0,33,66,100))'.format(r=r)
print("MATRIZ_174!AU/AV: conteo de certificaciones y score 0/33/66/100.")

# ── IP5 usa el conteo y exige los tres componentes ──────────────────────────
sc.Range("T4:T177").Formula = (
    '=IF(AND(ISNUMBER(K4),ISNUMBER(M4),ISNUMBER(MATRIZ_174!AV3)),'
    '(K4+M4+MATRIZ_174!AV3)/3,"")'
)
print("ISCAM_Score!T (IP5): usa el conteo y devuelve «\u00bb» si falta un componente.")

# ── 3) SCORECARDS!L: quitar el 0 de relleno ─────────────────────────────────
card.Range("L3:L176").Formula = '=IF(MATRIZ_174!O3="","",MATRIZ_174!O3)'
print("SCORECARDS!L: 0 de relleno → «\u00bb».")

# ── 4) Destino de B0.9 en la hoja de preguntas ──────────────────────────────
preg.Range("G14").Value = ("`MATRIZ_174!AU`/`AV` (conteo de certificaciones vigentes "
                           "\u2192 IP5, 0/33/66/100); `O` = score precensal ponderado "
                           "(0,6 org\u00e1nica / 0,4 Comercio Justo)")
for r in (100, 101, 102):
    preg.Cells(r, 7).Value = "`ISCAM_Score!N` (D10) \u2014 bandera, no promedia (se reporta aparte)"

# ── 5) Notas ────────────────────────────────────────────────────────────────
m.Range("A188").Value = "D10 ES BANDERA Y LA CERTIFICACI\u00d3N DE IP5 ES UN CONTEO (2026-10-15)"
m.Range("A189").Value = ("D10 (NORMALIZADO!CK) dej\u00f3 de promediar: sus tres \u00edtems \u2014D10.36 "
                         "(falsa seguridad), D10.37 (oferta de \u00abcertificaci\u00f3n EUDR\u00bb) y D10.36a "
                         "(asesor\u00eda)\u2014 son banderas y se reportan aparte (\u00a77.3 de la metodolog\u00eda ISA "
                         "y Tabla 4 del documento de trabajo). La certificaci\u00f3n s\u00ed entra al \u00edndice, pero "
                         "en IP5 y como conteo: AU = n.\u00ba de certificaciones vigentes (B0.9; registro "
                         "precensal H/I mientras no haya encuesta) y AV = 0/33/66/100 \u2014fuente: Matriz de "
                         "Cobertura T\u00e9cnica, \u00abIP5 recalculado (Certificaciones, conteo 0/33/66/100)\u00bb\u2014. "
                         "IP5 (ISCAM_Score!T) = (D7 + D9 + AV)/3 y devuelve \u00ab\u00bb si falta cualquier componente.")
pon.Range("A64").Value = "D10 ES BANDERA Y LA CERTIFICACI\u00d3N DE IP5 ES UN CONTEO (2026-10-15)"
pon.Range("A65").Value = ("D10 no promedia (bandera pura: D10.36, D10.37, D10.36a se reportan aparte). "
                          "Certificaci\u00f3n en IP5 = conteo de esquemas vigentes 0/33/66/100 "
                          "(MATRIZ_174!AU/AV), no el score ponderado 0,6/0,4. IP5 devuelve \u00ab\u00bb si falta "
                          "D7, D9 o la certificaci\u00f3n.")

xl.CalculateFull()
wb.Save(); wb.Close(SaveChanges=True); xl.Quit()
print("OK \u2014 D10 bandera + IP5 por conteo aplicados y guardados.")
