import pandas as pd

SRC = r"C:/Users/acuba/eudrperu/ficharucsunat/ruc-oece-personas.txt"
DIR = r"C:/Users/acuba/eudrperu/ficharucsunat"
DST_CSV = f"{DIR}/gerencia_gobernanza.csv"
DST_XLSX = f"{DIR}/gerencia_gobernanza.xlsx"

df = pd.read_csv(SRC, sep="\t", dtype=str).apply(lambda s: s.str.strip())
df["fecha_ingreso"] = pd.to_datetime(df["fecha_ingreso"], errors="coerce")
df["fecha_consulta"] = pd.to_datetime(df["fecha_consulta"], errors="coerce")

rows = []
for ruc, g in df.groupby("ruc", sort=False):
    socios = g[g["rol"] == "SOCIO"]
    org = g[g["rol"] == "ORGANO_ADMINISTRACION"]
    rep = g[g["rol"] == "REPRESENTANTE"]

    def ult(cargo_patron, sub=None):
        m = org if sub is None else org[org["tipo_organo"].str.contains(sub, case=False, na=False)]
        m = m[m["cargo"].str.contains(cargo_patron, case=False, na=False)]
        if m.empty:
            return "", ""
        m = m.sort_values("fecha_ingreso", na_position="first").iloc[-1]
        return str(m["nombre"]), str(m["dni"])

    pres_n, pres_d = ult(r"^Presidente$")
    vice_n, vice_d = ult(r"^Vice Presidente$")
    # gerente general: cargo exacto 'Gerente General'
    ger_n, ger_d = "", ""
    gg = org[org["cargo"].str.strip() == "Gerente General"]
    if not gg.empty:
        gg = gg.sort_values("fecha_ingreso", na_position="first").iloc[-1]
        ger_n, ger_d = str(gg["nombre"]), str(gg["dni"])

    # representante legal (rol REPRESENTANTE), último
    rep_n, rep_d = "", ""
    if not rep.empty:
        rep = rep.sort_values("fecha_ingreso", na_position="first").iloc[-1]
        rep_n, rep_d = str(rep["nombre"]), str(rep["dni"])

    rows.append(
        {
            "ruc": ruc,
            "n_socios": int((socios["source_id"].nunique())),
            "n_directivos": int(len(org)),
            "presidente_nombre": pres_n,
            "presidente_dni": pres_d,
            "vice_presidente_nombre": vice_n,
            "vice_presidente_dni": vice_d,
            "gerente_general_nombre": ger_n,
            "gerente_general_dni": ger_d,
            "representante_legal_nombre": rep_n,
            "representante_legal_dni": rep_d,
            "fecha_consulta": str(g["fecha_consulta"].max().date()) if pd.notna(g["fecha_consulta"].max()) else "",
        }
    )

out = pd.DataFrame(rows)
out.to_csv(DST_CSV, index=False, encoding="utf-8-sig")
out.to_excel(DST_XLSX, index=False, engine="openpyxl", sheet_name="Gobernanza")

print("rucs con datos de gobernanza:", len(out))
print("con socios:", int((out["n_socios"] > 0).sum()))
print("con presidente:", int(out["presidente_nombre"].astype(bool).sum()))
print("con gerente_general:", int(out["gerente_general_nombre"].astype(bool).sum()))
print("con representante_legal:", int(out["representante_legal_nombre"].astype(bool).sum()))
print("cols:", list(out.columns))
