# -*- coding: utf-8 -*-
import win32com.client as win32

XLS = r"C:\Users\acuba\eudrperu\PLANTILLA_INDICE_PVE_ISCAM.xlsx"
xl = win32.Dispatch("Excel.Application")
xl.Visible = False
xl.DisplayAlerts = False
xl.ScreenUpdating = False
xl.EnableEvents = False
wb = xl.Workbooks.Open(XLS)
xl.Calculation = -4135

pond = wb.Worksheets("PONDERADORES")
last = 57
while pond.Cells(last, 1).Value is not None and last < 80:
    last += 1
pond.Cells(last, 1).Value = "UMBRAL ISA-PACTOVERDE (2026-10-15)"
pond.Cells(last, 1).Font.Bold = True
pond.Cells(last + 1, 1).Value = ("ISA-PV se reporta como «—» (sin dato) mientras la organización no alcance "
                                 "3 de las 4 dimensiones Pacto Verde D12–D15 con dato (medido sobre la "
                                 "captura, NORMALIZADO). Por encima del umbral se repondera sobre los "
                                 "componentes con dato. La cobertura por organización está en MATRIZ_174!AQ.")
pond.Cells(last + 1, 1).WrapText = True

ins = wb.Worksheets("INSTRUCCIONES")
last = 1
while ins.Cells(last, 1).Value is not None and last < 120:
    last += 1
last += 1
ins.Cells(last, 1).Value = "SIN DATO = «—», NUNCA 0 (regla vigente desde 2026-10-15)"
ins.Cells(last, 1).Font.Bold = True
ins.Cells(last + 1, 1).Value = ("Aplica a toda la plantilla: la falta de dato no se convierte en 0 en ningún "
                                "nivel. En la base precensal (MATRIZ_174) el % UE/FOB, el FOB, el score de "
                                "certificación y los indicadores P1–P14 aparecen como «—» cuando falta la fuente; "
                                "la certificación se recodificó a SI/NO desde el texto fuente. En el motor, "
                                "ISA-PactoVerde exige el umbral de 3 de las 4 dimensiones D12–D15, ISA-EUDR 7 de "
                                "9 dimensiones D1–D9 e IP las 8 dimensiones D2–D9; por debajo se reporta «—».")
ins.Cells(last + 1, 1).WrapText = True

xl.Calculation = -4105
xl.CalculateFull()
wb.Save()
wb.Close(SaveChanges=True)
xl.Quit()
print("notas escritas: PONDERADORES A%d y INSTRUCCIONES A%d" % (last, last))
