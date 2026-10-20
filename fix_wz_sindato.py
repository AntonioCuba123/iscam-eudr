# -*- coding: utf-8 -*-
"""
MATRIZ_174!W:Z (D12–D15 Pacto Verde) traían 0 de relleno donde no hay dato:
  · W (D12.42) = `IF(NORMALIZADO!BV="",<literal>,BV)` con literal 0 en 129 filas
    (proxy 1 sólo en 45) → 0 no es una medición, es «sin dato».
  · X/Y/Z (D13.45, D14.51, D15.58) = `IF(NORMALIZADO!BW="",0,BW)` en las 174 filas
    → nunca hubo proxy: el 0 es íntegramente de relleno.

Efecto: al computar ISA-PV sólo sobre componentes con dato, ese 0 hacía que el
componente AMBIENTAL contara como presente y valiera 0, de modo que ISA-PV salía
0 (y la cobertura AQ contaba 1/7) en lugar de «—».

Se conserva el proxy FAO/IPCC documentado (W = 1 en las 45 organizaciones) y se
vacía todo lo demás. Escribe por COM.
"""
import os, shutil, datetime
import win32com.client as win32

ROOT = r"C:\Users\acuba\eudrperu"
PATH = os.path.join(ROOT, "PLANTILLA_INDICE_PVE_ISCAM.xlsx")
ts = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
bak = os.path.join(ROOT, "ISCAM", "respaldos", f"PLANTILLA_INDICE_PVE_ISCAM.backup_{ts}_pre-wz-sindato.xlsx")
shutil.copy2(PATH, bak); print("respaldo:", bak)

xl = win32.Dispatch("Excel.Application")
xl.Visible = False; xl.DisplayAlerts = False; xl.EnableEvents = False
wb = xl.Workbooks.Open(PATH)
m = wb.Worksheets("MATRIZ_174")

prox = 0
for r in range(3, 177):
    v = m.Cells(r, 23).Value                       # W computado (1 = proxy, 0 = relleno)
    if v == 1:
        prox += 1
        m.Cells(r, 23).Formula = f'=IF(NORMALIZADO!BV{r}="",1,NORMALIZADO!BV{r})'
    else:
        m.Cells(r, 23).Formula = f'=IF(NORMALIZADO!BV{r}="","",NORMALIZADO!BV{r})'
print("proxy D12 conservado (W=1):", prox, "filas → el resto de W vacío")

for col, ref in ((24, "BW"), (25, "BX"), (26, "BY")):
    m.Range(m.Cells(3, col), m.Cells(176, col)).Formula = f'=IF(NORMALIZADO!{ref}3="","",NORMALIZADO!{ref}3)'
print("X/Y/Z (D13/D14/D15) vaciados.")

m.Range("A180").Value = ("Un cero de relleno (falta de dato) se muestra como celda vacía, nunca como 0. Se vaciaron: "
                         "L (FOB UE), E (FOB total) y P1..P14; M (% UE/FOB) y O (score de certificación) devuelven «» "
                         "cuando falta el insumo; H/I venían truncadas a 3 caracteres y se recodificaron desde el texto "
                         "fuente; y W:Z (D12–D15 Pacto Verde) traían 0 de relleno —se conserva el proxy FAO/IPCC de D12 "
                         "(W=1 en las 45 organizaciones con hectáreas conocidas) y se vacía el resto—.")

xl.CalculateFull()
wb.Save(); wb.Close(SaveChanges=True); xl.Quit()
print("OK — W:Z limpios y guardado.")
