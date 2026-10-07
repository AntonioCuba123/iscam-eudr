import os
import pandas as pd

TXT = r"C:/Users/acuba/eudrperu/ficharucsunat/ruc-oece-personas.txt"
MASTER = r"C:/Users/acuba/eudrperu/ficharucsunat/ppaconsultamultiple/rucs_a_consultar.txt"
DIR = r"C:/Users/acuba/eudrperu/ficharucsunat"

raw = pd.read_csv(TXT, sep="\t", dtype=str).apply(lambda s: s.str.strip())
master = set(l.strip().rstrip("|").strip() for l in open(MASTER, encoding="utf-8") if l.strip())

raw["fecha_ingreso"] = pd.to_datetime(raw["fecha_ingreso"], errors="coerce", format="mixed")
raw["fecha_consulta"] = pd.to_datetime(raw["fecha_consulta"], errors="coerce", format="mixed")

print("=== 1. VISTA GENERAL DEL ARCHIVO LOCAL ===")
print("total filas:", len(raw))
print("columnas:", list(raw.columns))
print("rucs distintos:", raw["ruc"].nunique())
print("rucs con datos en master (179):", len(set(raw["ruc"]) & master), "-> lista:", sorted(set(raw["ruc"]) & master))
print()

print("=== 2. DISTRIBUCIÓN POR ROL / CARGO / ÓRGANO ===")
print("rol:")
print(raw["rol"].value_counts())
print("tipo_organo:")
print(raw["tipo_organo"].value_counts())
print("cargo:")
print(raw["cargo"].value_counts())
print()

print("=== 3. VALIDEZ DE DATOS / SUCiedad ===")
print("filas con dni vacío:", raw["dni"].eq("-").sum() + raw["dni"].isna().sum())
print("filas con nombre vacío:", raw["nombre"].isna().sum() + (raw["nombre"].eq("-")).sum())
print("dni no numéricos (excluye '-'):", raw[~raw["dni"].eq("-")]["dni"].apply(lambda x: not str(x).isdigit()).sum())
print("fechas_ingreso nulas:", raw["fecha_ingreso"].isna().sum())
# DNI con ceros a la izquierda verificados
print("ejemplo dni (string):", raw["dni"].dropna().unique()[:5])
print()

print("=== 4. COBERTURA POR RUC (master ∩ OECE): campos clave ===")
m = raw[raw["ruc"].isin(master)]
resumen = []
for ruc, g in m.groupby("ruc"):
    resumen.append({
        "ruc": ruc,
        "n_fila": len(g),
        "n_org_admin": int((g["rol"] == "ORGANO_ADMINISTRACION").sum()),
        "n_representante": int((g["rol"] == "REPRESENTANTE").sum()),
        "n_socio": int((g["rol"] == "SOCIO").sum()),
        "presidente": bool(((g["cargo"].fillna("") == "Presidente")).any()),
        "gerente_general": bool((g["cargo"].fillna("") == "Gerente General").any()),
        "fecha_consulta": str(g["fecha_consulta"].max().date()) if pd.notna(g["fecha_consulta"].max()) else "",
    })
cov = pd.DataFrame(resumen)
print("rucs master con datos OECE:", len(cov))
print("cuyo tiene presidente:", int(cov["presidente"].sum()))
print("cuyo tiene gerente_general:", int(cov["gerente_general"].sum()))
print("cuyo tiene representante:", int(cov["n_representante"].gt(0).sum()))
print("cuyo tiene socios:", int(cov["n_socio"].gt(0).sum()))
print()

print("=== 5. RUCs FALTANTES en OECE (master de 179 sin datos) ===")
faltan = sorted(master - set(raw["ruc"]))
print("faltan:", len(faltan), faltan)
print()

cov.to_csv(os.path.join(DIR, "revision_oece_vs_master.csv"), index=False, encoding="utf-8-sig")
print("exportado: revision_oece_vs_master.csv (cobertura de los", len(cov), "rucs master con datos OECE)")
