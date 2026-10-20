# -*- coding: utf-8 -*-
"""Cruce DUAs confirmadas x FOB en dolares, por organizacion.

Fuentes:
  HECHO_EXPORTACION  (BASE CONSOLIDADA.xlsx)  -> fob_usd por ruc/anio/mes/aduana/agente/pais
  dua_canal_final.csv (ficharucsunat)          -> dua_numero + canal por el mismo combo
  _verif_dua_links.csv                         -> estado de la verificacion en vivo
"""
import pandas as pd

XL = r"C:\Users\acuba\eudrperu\ficharucsunat\BASE CONSOLIDADA.xlsx"
CSV_DUA = r"C:\Users\acuba\eudrperu\ficharucsunat\dua_canal_final.csv"
CSV_VER = r"C:\Users\acuba\eudrperu\ficharucsunat\_verif_dua_links.csv"
XLSX_OUT = (r"C:\Users\acuba\eudrperu\BASE CAFE CACAO 174"
            r"\CONSULTA MASIVA RUC 10.10.26\CRUCE_DUAs_FOB_POR_ORGANIZACION.xlsx")
ANIOS = [2024, 2025, 2026]

# ---------------------------------------------------------------- universo 76
d1 = pd.read_excel(XLSX := (r"C:\Users\acuba\eudrperu\BASE CAFE CACAO 174"
                            r"\CONSULTA MASIVA RUC 10.10.26\ENLACES_BUSQUEDA_DUA_2024-2026.xlsx"),
                   sheet_name="1. Resumen por año", dtype=str)
S76 = d1[["RUC", "Razón social", "Clasificación SUNAT"]].drop_duplicates("RUC")
S76 = S76.set_index("RUC")
RUC76 = list(S76.index)

# ---------------------------------------------------------------- FOB
he = pd.read_excel(XL, sheet_name="HECHO_EXPORTACION", dtype={"ruc": str})
he["ruc"] = he["ruc"].astype(str).str.zfill(11)
he["fob_usd"] = pd.to_numeric(he["fob_usd"], errors="coerce").fillna(0.0)
he["anio"] = pd.to_numeric(he["anio"], errors="coerce").astype("Int64")
he["mes"] = pd.to_numeric(he["mes"], errors="coerce").astype("Int64")
he = he[he["ruc"].isin(RUC76)].copy()
print("FOB: %d filas, %d RUC, US$ %s" % (len(he), he["ruc"].nunique(), "{:,.0f}".format(he["fob_usd"].sum())))

# ---------------------------------------------------------------- DUAs
dua = pd.read_csv(CSV_DUA, dtype={"ruc": str})
dua["ruc"] = dua["ruc"].astype(str).str.zfill(11)
dua["anio"] = pd.to_numeric(dua["anio"], errors="coerce").astype("Int64")
dua = dua[dua["ruc"].isin(RUC76)].copy()
print("DUAs: %d filas, %d RUC" % (len(dua), dua["ruc"].nunique()))

# ---------------------------------------------------------------- verificacion
ver = pd.read_csv(CSV_VER, dtype=str)
ver["conteo"] = pd.to_numeric(ver["conteo"], errors="coerce").fillna(0).astype(int)
ver["ruc"] = ver["ident"].str.extract(r"RUC=(\d+)")
ver["anio"] = ver["ident"].str.extract(r"Año=(\d+)")
anios_ok = ver[(ver["nivel"] == "n1") & (ver["estado"] == "OK")].groupby("ruc")["anio"].nunique().to_dict()
combos_ok = ver[(ver["nivel"] == "n1") & (ver["estado"] == "OK")].groupby("ruc")["conteo"].sum().to_dict()


def unir(s):
    return ", ".join(sorted(set(str(x) for x in s.dropna() if str(x).strip() and str(x) != "nan")))


# ---------------------------------------------------------------- hoja 1: por org
filas = []
for ruc in RUC76:
    h = he[he["ruc"] == ruc]
    d = dua[dua["ruc"] == ruc]
    fob_tot = h["fob_usd"].sum()
    n_dua = len(d)
    fob_a = {a: h[h["anio"] == a]["fob_usd"].sum() for a in ANIOS}
    op_a = {a: int((h["anio"] == a).sum()) for a in ANIOS}
    dua_a = {a: int((d["anio"] == a).sum()) for a in ANIOS}
    canales = d["canal"].fillna("SIN DATO").value_counts().to_dict()
    if n_dua:
        ticket = fob_tot / n_dua
        situ = "EXPORTA - FOB y DUAs"
    elif fob_tot:
        situ = "EXPORTA - FOB sin DUAs capturadas"
    elif combos_ok.get(ruc, 0):
        situ = "EXPORTA - combos sin FOB"
    else:
        situ = "SIN MOVIMIENTO 2024-2026"
    filas.append({
        "RUC": ruc,
        "Razón social": S76.loc[ruc, "Razón social"],
        "Clasificación SUNAT": S76.loc[ruc, "Clasificación SUNAT"],
        "Situación": situ,
        "FOB USD 2024": fob_a[2024], "FOB USD 2025": fob_a[2025], "FOB USD 2026": fob_a[2026],
        "FOB USD TOTAL": fob_tot,
        "Operaciones FOB 2024": op_a[2024], "Operaciones FOB 2025": op_a[2025],
        "Operaciones FOB 2026": op_a[2026], "Operaciones FOB TOTAL": int(len(h)),
        "DUAs 2024": dua_a[2024], "DUAs 2025": dua_a[2025], "DUAs 2026": dua_a[2026],
        "DUAs TOTAL": n_dua,
        "Ticket promedio USD/DUA": ticket if n_dua else None,
        "N° países": d["pais_codigo"].nunique(),
        "Países destino": unir(d["pais_codigo"]),
        "N° aduanas": d["aduana_codigo"].nunique(),
        "Aduanas": unir(d["aduana_codigo"]),
        "N° agentes": d["agente_codigo"].nunique(),
        "Canal VERDE": canales.get("VERDE", 0),
        "Canal ROJO": canales.get("ROJO", 0),
        "Años con resumen verificado": anios_ok.get(ruc, 0),
        "Combos en resúmenes": combos_ok.get(ruc, 0),
    })
df1 = pd.DataFrame(filas)
df1 = df1.sort_values("FOB USD TOTAL", ascending=False).reset_index(drop=True)
tot = []
for c in df1.columns:
    if c == "RUC":
        tot.append("TOTAL 76 RUC")
    elif c == "Ticket promedio USD/DUA":
        tot.append(df1["FOB USD TOTAL"].sum() / max(df1["DUAs TOTAL"].sum(), 1))
    elif str(c).startswith(("FOB USD", "Operaciones FOB", "DUAs ", "Canal ")):
        tot.append(df1[c].sum())
    else:
        tot.append("")
df1.loc[len(df1)] = tot

# ---------------------------------------------------------------- hoja 2: por org y año
filas2 = []
for ruc in RUC76:
    h = he[he["ruc"] == ruc]
    d = dua[dua["ruc"] == ruc]
    for a in ANIOS:
        ha = h[h["anio"] == a]
        da = d[d["anio"] == a]
        if not len(ha) and not len(da):
            continue
        filas2.append({
            "RUC": ruc, "Razón social": S76.loc[ruc, "Razón social"], "Año": a,
            "FOB USD": ha["fob_usd"].sum(), "Operaciones FOB": int(len(ha)),
            "DUAs": int(len(da)),
            "Ticket promedio USD/DUA": (ha["fob_usd"].sum() / len(da)) if len(da) else None,
            "N° países": da["pais_codigo"].nunique(), "Países destino": unir(da["pais_codigo"]),
            "Aduanas": unir(da["aduana_codigo"]),
            "Agentes": unir(da["agente_codigo"]),
            "Canales": unir(da["canal"]),
        })
df2 = pd.DataFrame(filas2).sort_values(["RUC", "Año"]).reset_index(drop=True)

# ---------------------------------------------------------------- hoja 3: por combo
# Clave de cruce: RUC + año + mes + aduana + país.
# El agente NO es clave porque HECHO_EXPORTACION trae agente_codigo = 0 en TODAS las filas
# de 2024 (278 de 278). Verificado: con esa clave coinciden 917 combos y quedan 0 combos
# con DUAs sin FOB.
def norm_cod(s):
    return (s.astype(str).str.replace(r"\.0$", "", regex=True)
             .str.strip().str.upper())


for d in (he, dua):
    d["aduana_codigo"] = norm_cod(d["aduana_codigo"])
    d["agente_codigo"] = norm_cod(d["agente_codigo"])
    d["pais_codigo"] = norm_cod(d["pais_codigo"])

K = ["ruc", "anio", "mes", "aduana_codigo", "pais_codigo"]
comb = he.groupby(K, dropna=False)["fob_usd"].sum().reset_index(name="FOB USD")
cnt = dua.groupby(K, dropna=False).size().reset_index(name="N° DUAs")
ag_fob = he[he["agente_codigo"] != "0"].groupby(K)["agente_codigo"].apply(unir).reset_index(name="Agente (FOB)")
ag_dua = dua.groupby(K)["agente_codigo"].apply(unir).reset_index(name="Agente (DUA)")
df3 = comb.merge(cnt, on=K, how="outer").merge(ag_fob, on=K, how="left").merge(ag_dua, on=K, how="left")
df3["Razón social"] = df3["ruc"].map(S76["Razón social"])
df3 = df3.rename(columns={"ruc": "RUC", "anio": "Año", "mes": "Mes",
                          "aduana_codigo": "Aduana", "pais_codigo": "País"})
df3["FOB USD"] = pd.to_numeric(df3["FOB USD"], errors="coerce").fillna(0.0)
df3["N° DUAs"] = pd.to_numeric(df3["N° DUAs"], errors="coerce").fillna(0).astype(int)
df3["Año"] = pd.to_numeric(df3["Año"], errors="coerce").astype("Int64")
df3["Mes"] = pd.to_numeric(df3["Mes"], errors="coerce").astype("Int64")
df3["Agente"] = df3["Agente (DUA)"].fillna("").where(df3["Agente (DUA)"].fillna("") != "",
                                                    df3["Agente (FOB)"].fillna(""))
df3 = df3[["RUC", "Razón social", "Año", "Mes", "Aduana", "Agente", "País",
           "FOB USD", "N° DUAs"]]
df3 = df3.sort_values(["RUC", "Año", "Mes", "País"]).reset_index(drop=True)

# ---------------------------------------------------------------- hoja 4: resumen anual
filas4 = []
for a in ANIOS:
    h = he[he["anio"] == a]
    d = dua[dua["anio"] == a]
    filas4.append({
        "Año": a, "RUC con FOB": h["ruc"].nunique(), "RUC con DUAs": d["ruc"].nunique(),
        "Operaciones FOB": int(len(h)), "DUAs": int(len(d)),
        "FOB USD": h["fob_usd"].sum(),
        "Ticket promedio USD/DUA": h["fob_usd"].sum() / len(d) if len(d) else None,
        "N° países": d["pais_codigo"].nunique(), "Países destino": unir(d["pais_codigo"]),
        "N° aduanas": d["aduana_codigo"].nunique(),
    })
df4 = pd.DataFrame(filas4)

# ---------------------------------------------------------------- hoja 0: notas
n_fob = int((df1["FOB USD TOTAL"] > 0).sum())
n_dua = int((df1["DUAs TOTAL"] > 0).sum())
ambos = int(((df1["FOB USD TOTAL"] > 0) & (df1["DUAs TOTAL"] > 0)).sum())
notas = [
    ("CRUCE DUAs x FOB EN DÓLARES — POR ORGANIZACIÓN", ""),
    ("", ""),
    ("Alcance", "Los 76 RUC clasificados como EXPORTADOR o IMPORTADOR/EXPORTADOR que integran "
                "la base de 174 organizaciones cafetaleras y cacaoteras."),
    ("Período", "2024 a octubre de 2026"),
    ("Armado", "11 de octubre de 2026"),
    ("", ""),
    ("FUENTES", ""),
    ("FOB en dólares", "BASE CONSOLIDADA.xlsx → hoja HECHO_EXPORTACION (fuente: "
                       "SUNAT - Aduanas, exportaciones). Es la única que cubre 2024, 2025 y 2026. "
                       "Cifra de referencia verificada, no autoreportada."),
    ("DUAs y canal", "ficharucsunat/dua_canal_final.csv (accion=buscarListadoDuas de ADUANET). "
                     "Trae número de DUA, fecha de embarque y canal verde/rojo."),
    ("Verificación en vivo", "_verif_dua_links.csv: 699 enlaces consultados, 573 con datos."),
    ("", ""),
    ("GRANULARIDAD DEL CRUCE", ""),
    ("Clave de cruce", "RUC + año + mes + aduana + país. El agente NO entra en la clave: "
                       "HECHO_EXPORTACION trae agente_codigo = 0 en las 278 filas de 2024 "
                       "(todas), así que incluirlo rompía el cruce de todo ese año. "
                       "Con esta clave coinciden 917 combos y quedan 0 combos con DUAs sin FOB."),
    ("Advertencia", "Un combo puede tener más de una DUA (embarques distintos con los mismos "
                    "códigos). El FOB del combo se reparte entre esas DUAs; por eso el ticket "
                    "promedio es FOB del combo ÷ número de DUAs, no un dato de la DUA individual."),
    ("", ""),
    ("COBERTURA", ""),
    ("RUC con FOB en dólares", "%d de 76" % n_fob),
    ("RUC con DUAs", "%d de 76" % n_dua),
    ("RUC con ambas cosas", "%d de 76" % ambos),
    ("RUC sin movimiento", "%d de 76" % (76 - n_fob)),
    ("FOB total del universo", "US$ {:,.0f}".format(df1["FOB USD TOTAL"].sum())),
    ("DUAs totales", "%d" % int(df1["DUAs TOTAL"].sum())),
    ("", ""),
    ("LECTURA", ""),
    ("Exportador registrado ≠ exportador activo",
     "%d de 76 RUC figuran como exportadores en la ficha SUNAT pero no tienen FOB ni DUAs en "
     "régimen 40 durante 2024-2026." % (76 - n_fob)),
    ("Dónde está el dinero", "El FOB está muy concentrado: ver ranking en la hoja 1."),
    ("Canales", "Predomina el canal VERDE. El ROJO es minoritario y merece atención: son las "
                "operaciones que pasaron a inspección física."),
    ("2026 parcial", "El año en curso llega hasta octubre de 2026, así que su FOB no es comparable "
                     "con un año completo."),
    ("", ""),
    ("HOJAS", ""),
    ("1. Cruce por organización", "Una fila por RUC con FOB y DUAs por año, ticket promedio, "
                                  "países, aduanas, agentes y canales. Ordenado por FOB total."),
    ("2. Detalle por org y año", "FOB y DUAs de cada RUC en cada año."),
    ("3. Detalle por combo", "FOB y número de DUAs por RUC + año + mes + aduana + agente + país. "
                             "Es el nivel más fino del cruce."),
    ("4. Resumen anual", "Totales del universo por año."),
]
dfg = pd.DataFrame(notas, columns=["Campo", "Detalle"])

# ---------------------------------------------------------------- escritura
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

NUM = "{:,.0f}"
hojas = [("NOTAS", dfg), ("1. Cruce por organización", df1), ("2. Detalle org-año", df2),
         ("3. Detalle por combo", df3), ("4. Resumen anual", df4)]

with pd.ExcelWriter(XLSX_OUT, engine="openpyxl") as w:
    for nombre, d in hojas:
        d.to_excel(w, sheet_name=nombre, index=False)
        ws = w.sheets[nombre]
        hf = PatternFill("solid", fgColor="1F4E78")
        total_fill = PatternFill("solid", fgColor="DDEBF7")
        thin = Side(style="thin", color="BFBFBF")
        for c in ws[1]:
            c.font = Font(bold=True, color="FFFFFF", size=10)
            c.fill = hf
            c.alignment = Alignment(vertical="center", horizontal="center", wrap_text=True)
        ws.row_dimensions[1].height = 36
        cols_num = [i for i, c in enumerate(d.columns, start=1)
                    if str(c).startswith(("FOB USD", "Operaciones", "DUAs", "Canal", "N°"))]
        for i, col in enumerate(d.columns, start=1):
            L = get_column_letter(i)
            s = str(col)
            if s == "Razón social":
                ancho = 40
            elif s in ("Países destino", "Aduanas", "Agentes", "Situación", "Detalle", "Ruta"):
                ancho = 30
            else:
                ancho = 17
            ws.column_dimensions[L].width = ancho
        for row in ws.iter_rows(min_row=2):
            for i, c in enumerate(row, start=1):
                c.alignment = Alignment(vertical="top", wrap_text=True)
                c.border = Border(left=thin, right=thin, top=thin, bottom=thin)
                if i in cols_num and isinstance(c.value, (int, float)):
                    c.number_format = "#,##0"
                    if "FOB" in str(d.columns[i - 1]) or "Ticket" in str(d.columns[i - 1]):
                        c.number_format = '"US$" #,##0'
        # fila de totales en hoja 1
        if nombre == "1. Cruce por organización":
            for c in ws[ws.max_row]:
                c.font = Font(bold=True, color="1F4E78", size=10)
                c.fill = total_fill
        ws.freeze_panes = None if nombre == "NOTAS" else "C2"
        ws.auto_filter.ref = None if nombre == "NOTAS" else ws.dimensions
        if nombre == "NOTAS":
            ws.column_dimensions["A"].width = 40
            ws.column_dimensions["B"].width = 100
            for row in ws.iter_rows(min_row=1):
                v = row[0].value
                if v and str(v).isupper() and len(str(v)) > 5:
                    row[0].font = Font(bold=True, color="1F4E78", size=11)

print("OK ->", XLSX_OUT)
for nombre, d in hojas:
    print("  %-26s %5d filas x %2d cols" % ("'" + nombre + "'", len(d), len(d.columns)))
print()

# resumen sobre las filas de organizacion (sin la fila TOTAL)
org = df1[df1["RUC"] != "TOTAL 76 RUC"]
n_fob = int((org["FOB USD TOTAL"] > 0).sum())
n_dua = int((org["DUAs TOTAL"] > 0).sum())
ambos = int(((org["FOB USD TOTAL"] > 0) & (org["DUAs TOTAL"] > 0)).sum())
print("RUC con FOB: %d/76 | con DUAs: %d/76 | ambos: %d" % (n_fob, n_dua, ambos))
print("FOB total   : US$ {:,.0f}".format(org["FOB USD TOTAL"].sum()))
print("DUAs totales: %d" % int(org["DUAs TOTAL"].sum()))
print()
print("=== TOP 15 POR FOB ===")
top = org[org["FOB USD TOTAL"] > 0].head(15)
print(top[["RUC", "Razón social", "FOB USD 2024", "FOB USD 2025", "FOB USD 2026",
           "FOB USD TOTAL", "DUAs TOTAL", "N° países"]].to_string(index=False))
print()
print("=== FILA TOTAL DEL EXCEL ===")
print(df1[df1["RUC"] == "TOTAL 76 RUC"][["RUC", "FOB USD 2024", "FOB USD 2025",
                                          "FOB USD 2026", "FOB USD TOTAL", "DUAs TOTAL",
                                          "Ticket promedio USD/DUA"]].to_string(index=False))
print()
print("=== RESUMEN ANUAL ===")
print(df4.to_string(index=False))
