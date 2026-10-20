# -*- coding: utf-8 -*-
"""
Dos cambios sobre PLANTILLA_INDICE_PVE_ISCAM.xlsx (2026-10-15):

  A. ISA-PV PROVISIONAL CON ETIQUETA «parcial»
     Antes: por debajo del umbral (3 de 4 dimensiones D12–D15) ISA-PV se mostraba
     como «—». Ahora se muestra el valor re-ponderado sobre los componentes con
     dato, etiquetado como provisional:
        · MATRIZ_174!AP  = valor (numérico) siempre que haya ≥1 componente con dato
        · MATRIZ_174!AQ  = cobertura (n de 7 componentes con dato)   [sin cambio]
        · MATRIZ_174!AT  = NUEVO «Estado ISA-PV»: completo / parcial · n/7 / sin dato
        · MATRIZ_174!T   = clasificación PVE; sin veredicto de color mientras el
                           valor es provisional («◐ Parcial · n/7»), y el veredicto
                           (🔴/🟡/🟢) sólo cuando la medición está completa
     Notas y cabeceras actualizadas en MATRIZ_174, PONDERADORES e INSTRUCCIONES; y
     se agrega ISCAM_Score!AM con el mismo estado, para que el motor no muestre un
     número parcial sin bandera.

  B. IP5 — mezcla de escalas
     IP5 = (D7 + D9 + Cert)/3 sumaba dos dimensiones 0–100 (D7, D9) con el score de
     certificación 0–1 (MATRIZ_174!O). Corregido a Cert×100. Además, los subíndices
     IP1–IP5 devolvían 0 cuando faltaba un insumo (celda vacía → #VALUE! → 0); ahora
     devuelven vacío, coherente con «sin dato = «—», nunca 0».
"""
import os, shutil, datetime
import win32com.client as win32

ROOT = r"C:\Users\acuba\eudrperu"
PATH = os.path.join(ROOT, "PLANTILLA_INDICE_PVE_ISCAM.xlsx")
ts = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
bak = os.path.join(ROOT, "ISCAM", "respaldos", f"PLANTILLA_INDICE_PVE_ISCAM.backup_{ts}_pre-pv-parcial-ip5.xlsx")
shutil.copy2(PATH, bak); print("respaldo:", bak)

# ── Fórmulas (fila 3 de MATRIZ_174; Excel las propaga con referencias relativas) ──
AP3 = ('=IFERROR((IF(ISNUMBER(M3),M3/100*PONDERADORES!$D$12,0)'
       '+IF(ISNUMBER(SCORECARDS!H3),SCORECARDS!H3/100*PONDERADORES!$D$13,0)'
       '+IF(ISNUMBER(SCORECARDS!I3),SCORECARDS!I3/100*PONDERADORES!$D$14,0)'
       '+IF(ISNUMBER(SCORECARDS!J3),SCORECARDS!J3/100*PONDERADORES!$D$15,0)'
       '+IF(ISNUMBER(ISCAM_Score!K4),ISCAM_Score!K4/100*PONDERADORES!$D$16,0)'
       '+IF(ISNUMBER(O3),O3*PONDERADORES!$D$17,0)'
       '+IF(ISNUMBER(AVERAGE(W3:Z3)),AVERAGE(W3:Z3)/2*PONDERADORES!$D$19,0))'
       '/(IF(ISNUMBER(M3),PONDERADORES!$D$12,0)'
       '+IF(ISNUMBER(SCORECARDS!H3),PONDERADORES!$D$13,0)'
       '+IF(ISNUMBER(SCORECARDS!I3),PONDERADORES!$D$14,0)'
       '+IF(ISNUMBER(SCORECARDS!J3),PONDERADORES!$D$15,0)'
       '+IF(ISNUMBER(ISCAM_Score!K4),PONDERADORES!$D$16,0)'
       '+IF(ISNUMBER(O3),PONDERADORES!$D$17,0)'
       '+IF(ISNUMBER(AVERAGE(W3:Z3)),PONDERADORES!$D$19,0)),"—")')

COMPLETO = 'AND(AQ3=7,COUNT(NORMALIZADO!BV3:BY3)=4)'
T3 = ('=IF(NOT(ISNUMBER(S3)),"⬜  Sin dato PVE",'
      'IF(' + COMPLETO + ',IF(S3<34,"🔴 Crítico",IF(S3<67,"🟡 Vulnerable","🟢 Preparado")),'
      '"◐  Parcial · "&AQ3&"/7"))')
AT3 = ('=IF(NOT(ISNUMBER(AP3)),"sin dato",'
       'IF(' + COMPLETO + ',"completo","parcial · "&AQ3&"/7"))')

AP2 = ("ISA-PactoVerde (0-100) = EXP_UE 20% + TRAZA 16% + DILIG 12% + CAPAC 8% + PRESION 12% "
       "+ CERTIF 8% + AMBIENTAL(D12-D15) 20%. Se computa sólo sobre los componentes con dato, "
       "re-normalizando los pesos; «—» sólo si no hay ningún componente. Mientras no se cumpla "
       "el umbral (3 de 4 dimensiones D12-D15 capturadas) el valor es PROVISIONAL: ver AQ y AT.")
AQ2 = ("Cobertura ISA-PV: n de 7 componentes con dato (PPWR excluido hasta tener fuente). "
       "Gobierna el estado de AT: parcial mientras falte algún componente o D12-D15 no esté capturado.")
AT2 = "Estado ISA-PV\ncompleto = 7/7 componentes + D12-D15 capturado\nparcial = valor provisional\nsin dato = sin ningún componente"
T2 = "Clasificación PVE\n(veredicto de color sólo con medición completa; «◐ Parcial · n/7» mientras el valor es provisional)"

MAT_NOTE_T = "UMBRAL ISA-PACTOVERDE → VALOR PROVISIONAL (2026-10-15)"
MAT_NOTE_B = ("Por debajo del umbral del documento (§2.4) —3 de las 4 dimensiones Pacto Verde D12-D15 con dato— "
              "ISA-PV (AP) ya no se reporta como «—»: se muestra el valor re-ponderado sobre los componentes con dato "
              "y se etiqueta como PROVISIONAL en T («◐ Parcial · n/7») y en AT (estado). El veredicto de color "
              "(🔴/🟡/🟢) se reserva para cuando la medición está completa (7/7 componentes y D12-D15 capturado), "
              "porque un color sobre una base parcial sería una medición falsa. «—» queda sólo para las organizaciones "
              "sin ningún componente con dato. La cobertura por organización está en AQ.")

POND_T = "UMBRAL ISA-PACTOVERDE → VALOR PROVISIONAL (2026-10-15)"
POND_B = ("ISA-PV (MATRIZ_174!AP) se computa siempre sobre los componentes con dato, re-normalizando los pesos. "
          "Mientras no se cumplan 3 de 4 dimensiones D12-D15 (captura, NORMALIZADO) el valor es PROVISIONAL y así se "
          "etiqueta: MATRIZ_174!AT lo declara como «parcial · n/7» y la clasificación de MATRIZ_174!T se muestra como "
          "«◐ Parcial · n/7» sin veredicto de color. Con la medición completa, T vuelve a 🔴/🟡/🟢. «—» sólo cuando no "
          "hay ningún componente con dato. Cobertura por organización: MATRIZ_174!AQ.")

INS5 = ("La falta de dato no se convierte en 0 en ningún nivel: en la base precensal el % UE/FOB, el FOB, el score de "
        "certificación y los indicadores P1–P14 aparecen como «—». En el motor, ISA-EUDR e IP se reportan «—» cuando no "
        "alcanzan su umbral de dimensiones con dato. ISA-PactoVerde es la excepción declarada: sobre sus componentes con "
        "dato se computa igual, y mientras no cumpla su umbral (3 de 4 dimensiones D12–D15) el valor se muestra como "
        "PROVISIONAL, etiquetado «◐ Parcial · n/7» en MATRIZ_174 (columnas AT y T) —nunca como un color de clasificación "
        "ni como 0—.")

xl = win32.Dispatch("Excel.Application")
xl.Visible = False; xl.DisplayAlerts = False; xl.EnableEvents = False
wb = xl.Workbooks.Open(PATH)

# ── A. ISA-PV provisional ───────────────────────────────────────────────────
m = wb.Worksheets("MATRIZ_174")
m.Range("AP3:AP176").Formula = AP3
m.Range("T3:T176").Formula = T3
m.Range("AT3:AT176").Formula = AT3
m.Range("AP2").Value = AP2
m.Range("AQ2").Value = AQ2
m.Range("AT2").Value = AT2
m.Range("T2").Value = T2
m.Range("A182").Value = MAT_NOTE_T
m.Range("A183").Value = MAT_NOTE_B

s = wb.Worksheets("ISCAM_Score")
s.Range("AM3").Value = ("Estado ISA-PV\n(completo / parcial · n/7 / sin dato)")
s.Range("AM4:AM177").Formula = '=IFERROR(MATRIZ_174!AT3,"")'
s.Range("AI3").Value = "ISA-PV\n8 componentes ponderados\n(puede ser PROVISIONAL: ver AM)"

sc = wb.Worksheets("SCORECARDS")
sc.Range("A186").Value = "PVE promedio (ISA-PV, 0-100 · incluye parciales)"

wb.Worksheets("PONDERADORES").Range("A58").Value = POND_T
wb.Worksheets("PONDERADORES").Range("A59").Value = POND_B
wb.Worksheets("INSTRUCCIONES").Range("A5").Value = INS5

# ── B. IP5 y fallbacks de IP1–IP5 ───────────────────────────────────────────
s.Range("T4:T177").Formula = '=IF(ISNUMBER(MATRIZ_174!O3),IFERROR((K4+M4+MATRIZ_174!O3*100)/3,0),"")'
s.Range("Q4:Q177").Formula = '=IFERROR(SQRT(G4*H4),"")'
s.Range("R4:R177").Formula = '=IFERROR((I4+J4+L4)/3,"")'
s.Range("S4:S177").Formula = '=IFERROR((J4+F4)/2,"")'
s.Range("AA4:AA177").Formula = '=IFERROR(ROUND(AVERAGE(U4,V4,W4,X4,Y4),1),"—")'

xl.CalculateFull()
wb.Save(); wb.Close(SaveChanges=True); xl.Quit()
print("OK — AP/T/AT + IP5 (Cert×100) + notas aplicadas y guardadas.")
