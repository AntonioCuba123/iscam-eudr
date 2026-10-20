# -*- coding: utf-8 -*-
"""Validacion de cuadre del Excel de cruce."""
import pandas as pd

P = (r"C:\Users\acuba\eudrperu\BASE CAFE CACAO 174"
     r"\CONSULTA MASIVA RUC 10.10.26\CRUCE_DUAs_FOB_POR_ORGANIZACION.xlsx")

h1 = pd.read_excel(P, sheet_name="1. Cruce por organización")
h2 = pd.read_excel(P, sheet_name="2. Detalle org-año")
h3 = pd.read_excel(P, sheet_name="3. Detalle por combo")
h4 = pd.read_excel(P, sheet_name="4. Resumen anual")

org = h1[h1["RUC"] != "TOTAL 76 RUC"]
tot = h1[h1["RUC"] == "TOTAL 76 RUC"].iloc[0]

print("=== CUADRE ===")
print("FOB total hoja 1 (orgs) : {:>16,.2f}".format(org["FOB USD TOTAL"].sum()))
print("FOB total fila TOTAL    : {:>16,.2f}".format(tot["FOB USD TOTAL"]))
print("FOB total hoja 2        : {:>16,.2f}".format(h2["FOB USD"].sum()))
print("FOB total hoja 3        : {:>16,.2f}".format(h3["FOB USD"].sum()))
print("FOB total hoja 4        : {:>16,.2f}".format(h4["FOB USD"].sum()))
print()
print("DUAs hoja 1 (orgs)      : {:>16,d}".format(int(org["DUAs TOTAL"].sum())))
print("DUAs fila TOTAL         : {:>16,d}".format(int(tot["DUAs TOTAL"])))
print("DUAs hoja 3             : {:>16,d}".format(int(h3["N° DUAs"].sum())))
print()
print("FOB 2024+2025+2026 = TOTAL ?",
      round(org["FOB USD 2024"].sum() + org["FOB USD 2025"].sum() + org["FOB USD 2026"].sum(), 2),
      "vs", round(org["FOB USD TOTAL"].sum(), 2))
print("Operaciones FOB 2024+2025+2026 = TOTAL ?",
      int(org["Operaciones FOB 2024"].sum() + org["Operaciones FOB 2025"].sum()
          + org["Operaciones FOB 2026"].sum()),
      "vs", int(org["Operaciones FOB TOTAL"].sum()))
print("DUAs 2024+2025+2026 = TOTAL ?",
      int(org["DUAs 2024"].sum() + org["DUAs 2025"].sum() + org["DUAs 2026"].sum()),
      "vs", int(org["DUAs TOTAL"].sum()))
print()
print("=== concentracion ===")
s = org.sort_values("FOB USD TOTAL", ascending=False)
fob = org["FOB USD TOTAL"].sum()
for k in (1, 3, 5, 10, 15):
    parte = s.head(k)["FOB USD TOTAL"].sum()
    print("  top %2d RUC -> US$ %14s  (%5.1f%% del FOB del universo)" % (k, "{:,.0f}".format(parte), 100 * parte / fob))
print()
print("=== canales ===")
print("  VERDE: %d | ROJO: %d" % (int(org["Canal VERDE"].sum()), int(org["Canal ROJO"].sum())))
rojo = org[org["Canal ROJO"] > 0][["RUC", "Razón social", "Canal ROJO", "FOB USD TOTAL"]]
if len(rojo):
    print()
    print("  RUC con canal ROJO (inspeccion fisica):")
    print(rojo.to_string(index=False))
print()
print("=== RUC sin movimiento (32) ===")
sin = org[org["FOB USD TOTAL"] == 0]
print("  cantidad:", len(sin))
print("  " + ", ".join(sin["RUC"].tolist()))
print()
print("=== muestra hoja 3 (combo) ===")
print(h3[h3["N° DUAs"] > 0].head(6).to_string(index=False, max_colwidth=34))
