import pandas as pd

SRC = r"C:\Users\acuba\eudrperu\ficharucsunat\rucconsultamultiple\RM20261005105736349.xlsx"
DST = r"C:\Users\acuba\eudrperu\ficharucsunat\rucconsultamultiple\exportadores_only.txt"

d = pd.read_excel(SRC, dtype=str)
d["Actividad de Comercio Exterior"] = d["Actividad de Comercio Exterior"].fillna("").astype(str).str.strip()
exp = d[d["Actividad de Comercio Exterior"] == "EXPORTADOR"]

with open(DST, "w", encoding="utf-8") as f:
    for r in exp["NumeroRuc"].tolist():
        f.write(f"{r}|\n")

print("exportadores:", len(exp))
print(f.writelines if False else None)
