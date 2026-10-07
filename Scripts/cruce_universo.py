"""
Cruce unificado EUDRPERU — universo completo cafe/cacao
Fuentes: PAC directory + MIDAGRI 2026 + CENACOOP 2017 + SUNAT vivo
"""
import openpyxl, pandas as pd, os

OUT = r"C:\Users\acuba\eudrperu\data\EUDRPERU_universo_consolidado.csv"

# ─── 1. PAC base ────────────────────────────────────────────────────────────
f_pac = r"C:\Users\acuba\eudrperu\Directorio Cooperativas Cafe-Cacao Peru.xlsx"
wb = openpyxl.load_workbook(f_pac, data_only=True)
ws = wb["Cooperativas y asociaciones"]
rows = list(ws.iter_rows(values_only=True))
pac = pd.DataFrame(rows[1:], columns=[str(c).strip() if c else f"c{i}" for i, c in enumerate(rows[0])])
for c in pac.columns:
    pac[c] = pac[c].astype(str).str.strip().str.replace("\n", " ")
pac_cc = pac[pac["Producto"].str.contains("Café|CACAO", na=False, case=False, regex=True)].copy()
pac_cc = pac_cc.rename(columns={"Organización": "nombre_pac", "Región / macro-zona": "region_pac",
    "Producto": "producto_pac", "Certificación conocida": "cert_pac",
    "Correo": "correo_pac", "Teléfono": "tel_pac", "Representante conocido": "rep_pac"})
pac_cc = pac_cc[["nombre_pac", "producto_pac", "region_pac", "rep_pac", "cert_pac", "correo_pac", "tel_pac"]]
wb.close()
print(f"PAC cafe+cacao: {len(pac_cc)} orgs")

# ─── 2. PAC v3 RUCs ────────────────────────────────────────────────────────
f_v3 = r"C:\Users\acuba\eudrperu\Directorio Cooperativas Cafe-Cacao Peru (v3 - Cepicafe-Norandino).xlsx"
wb3 = openpyxl.load_workbook(f_v3, data_only=True)
ws3 = wb3.active
rows3 = list(ws3.iter_rows(values_only=True))
h3 = [str(c).replace("\n", " ").strip() if c else f"c{i}" for i, c in enumerate(rows3[0])]
v3 = pd.DataFrame(rows3[1:], columns=h3)
v3["ruc"] = v3["RUC"].apply(lambda x: str(x).strip() if str(x).strip().isdigit() and len(str(x).strip()) == 11 else "")
v3 = v3[v3["ruc"] != ""][["Organización (nombre usual)", "ruc"]].copy()
v3.columns = ["nombre_v3", "ruc"]
v3["nombre_norm"] = v3["nombre_v3"].str.upper().str.replace(r"[^A-Z0-9 ]", "", regex=True).str.replace(r"\s+", " ", regex=True)
wb3.close()
v3_dict = dict(zip(v3["nombre_norm"], v3["ruc"]))
print(f"PAC v3 RUCs: {len(v3)} orgs")

# Asignar RUCs a PAC
pac_cc["nombre_norm"] = pac_cc["nombre_pac"].str.upper().str.replace(r"[^A-Z0-9 ]", "", regex=True).str.replace(r"\s+", " ", regex=True)
pac_cc["ruc"] = ""
for idx, row in pac_cc.iterrows():
    pac_cc.loc[idx, "ruc"] = v3_dict.get(row["nombre_norm"], "")

# Si no hay RUC, buscar en MIDAGRI luego
pac_cc["fuente"] = "PAC"
print(f"PAC con RUC (v3): {(pac_cc['ruc'] != '').sum()}")

# ─── 3. MIDAGRI ────────────────────────────────────────────────────────────
mid = pd.read_csv(r"C:\Users\acuba\eudrperu\data\MIDAGRI_cooperativas_agrarias_2026.csv", sep="|", dtype=str)
mid["ruc"] = mid["ruc"].str.strip()
mid["nombre_norm"] = mid["cooperativa"].str.upper().str.replace(r"[^A-Z0-9 ]", "", regex=True).str.replace(r"\s+", " ", regex=True)
mid_cc = mid[mid["actividad_principal"].str.contains("Caf|Cac", na=False, case=False, regex=True)].drop_duplicates(subset="ruc").copy()
print(f"MIDAGRI cafe+cacao: {len(mid_cc)} orgs")
mid_ruc_dict = dict(zip(mid_cc["nombre_norm"], mid_cc["ruc"]))
# Asignar RUCs faltantes desde MIDAGRI
for idx, row in pac_cc.iterrows():
    if pac_cc.loc[idx, "ruc"] == "":
        pac_cc.loc[idx, "ruc"] = mid_ruc_dict.get(row["nombre_norm"], "")
print(f"PAC con RUC (v3+MIDAGRI): {(pac_cc['ruc'] != '').sum()}")

# ─── 4. CENACOOP fusion ──────────────────────────────────────────────────
cen = pd.read_csv(r"C:\Users\acuba\eudrperu\data\CENACOOP_fusion_EUDR.csv", sep="|", dtype=str)
cen["ruc"] = cen["ruc_llave"].str.strip()
for c in ["sunat_exp_fob_usd_total", "sunat_exp_n_operaciones", "sunat_exp_n_paises",
           "sunat_imp_fob_usd_total", "sunat_imp_n_operaciones",
           "data2024_fob_miles_dolar", "data2024_trabajadores", "data2024_ventas_prom_soles"]:
    cen[c] = pd.to_numeric(cen[c], errors="coerce")
print(f"CENACOOP fusion: {len(cen)} orgs")

# ─── 5. SUNAT vivo ──────────────────────────────────────────────────────
sun = pd.read_csv(r"C:\Users\acuba\eudrperu\data\SUNAT_validacion_ruc.csv", sep="|", dtype=str)
sun["ruc"] = sun["ruc"].str.strip()
sun_dict = {}
for _, row in sun.iterrows():
    r = str(row["ruc"])
    if r and len(r) == 11:
        sun_dict[r] = {"estado": row["estado_sunat"], "domicilio": row["domicilio_sunat"],
                       "razon": row["razon_social_sunat"], "ubigeo": row["ubigeo_sunat"]}
print(f"SUNAT vivo: {len(sun_dict)} orgs")

# ─── 6. Maestro por RUC ──────────────────────────────────────────────────
maestro = {}

# Agregar PAC
for _, row in pac_cc.iterrows():
    r = str(row["ruc"]).strip()
    if r and len(r) == 11:
        if r not in maestro:
            maestro[r] = {"nombre": row["nombre_pac"], "ruc": r, "fuentes": set(),
                          "region_pac": str(row["region_pac"]) if row["region_pac"] else "",
                          "cert_pac": str(row["cert_pac"]) if row["cert_pac"] else "",
                          "rep_pac": str(row["rep_pac"]) if row["rep_pac"] else "",
                          "correo_pac": str(row["correo_pac"]) if row["correo_pac"] else "",
                          "tel_pac": str(row["tel_pac"]) if row["tel_pac"] else ""}
        maestro[r]["fuentes"].add("PAC")

# Agregar MIDAGRI
for _, row in mid_cc.iterrows():
    r = str(row["ruc"]).strip()
    if r and len(r) == 11:
        if r not in maestro:
            maestro[r] = {"ruc": r, "fuentes": set(), "nombre": row["cooperativa"]}
        maestro[r]["fuentes"].add("MIDAGRI")
        for col, key in [("departamento", "departamento"), ("provincia", "provincia"),
                          ("distrito", "distrito"), ("actividad_midagri", "actividad_principal"),
                          ("producto_midagri", "producto_principal"),
                          ("socios_total", "total_socios"),
                          ("socios_h", "socios_hombres"), ("socios_m", "socios_mujeres"),
                          ("anio_inscripcion", "anio_inscripcion")]:
            v = row.get(key, "")
            if pd.notna(v) and str(v).strip():
                maestro[r][col] = str(v).strip()

# Agregar CENACOOP
for _, row in cen.iterrows():
    r = str(row["ruc"]).strip()
    if r and len(r) == 11:
        if r not in maestro:
            maestro[r] = {"ruc": r, "fuentes": set()}
            maestro[r]["nombre"] = str(row.get("cooperativa_midagri", ""))
        maestro[r]["fuentes"].add("CENACOOP")
        # SUNAT
        exp_n = row.get("sunat_exp_n_operaciones", 0) or 0
        if exp_n > 0:
            maestro[r]["sunat_exporta"] = True
            maestro[r]["exp_n_ops"] = exp_n
            maestro[r]["exp_fob"] = row.get("sunat_exp_fob_usd_total", 0) or 0
            maestro[r]["exp_n_paises"] = row.get("sunat_exp_n_paises", 0) or 0
            maestro[r]["exp_paises"] = str(row.get("sunat_exp_paises", ""))[:120]
            maestro[r]["exp_anio_min"] = int(row["sunat_exp_anio_min"]) if pd.notna(row.get("sunat_exp_anio_min")) else None
            maestro[r]["exp_anio_max"] = int(row["sunat_exp_anio_max"]) if pd.notna(row.get("sunat_exp_anio_max")) else None
            maestro[r]["imp_fob"] = row.get("sunat_imp_fob_usd_total", 0) or 0
        maestro[r]["cen_email"] = str(row.get("cen2017_CORREO", ""))[:100]
        maestro[r]["cen_tel_fijo"] = str(row.get("cen2017_TELEFONO_FIJO", ""))[:30]
        maestro[r]["cen_tel_movil"] = str(row.get("cen2017_TELEFONO_MOVIL", ""))[:30]
        maestro[r]["cen_web"] = str(row.get("cen2017_PAG_WEB", ""))[:100]
        maestro[r]["d2024_exporta"] = str(row.get("data2024_exporta", ""))
        maestro[r]["d2024_fob"] = row.get("data2024_fob_miles_dolar", 0) or 0
        maestro[r]["d2024_exp"] = str(row.get("data2024_experiencia", ""))[:80]
        maestro[r]["d2024_trab"] = row.get("data2024_trabajadores", 0) or 0
        maestro[r]["d2024_ventas"] = row.get("data2024_ventas_prom_soles", 0) or 0

# Agregar SUNAT vivo (override si es más reciente)
for r, datos in sun_dict.items():
    if r in maestro:
        maestro[r]["sunat_estado"] = datos["estado"]
        maestro[r]["sunat_domicilio"] = datos["domicilio"]
        maestro[r]["sunat_razon"] = datos["razon"]
        maestro[r]["sunat_ubigeo"] = datos["ubigeo"]

# ─── 7. Armar DataFrame ─────────────────────────────────────────────────
rows_out = []
for ruc, d in maestro.items():
    fuentes = sorted(d.get("fuentes", set()))
    rows_out.append({
        "ruc": ruc,
        "nombre": d.get("nombre", ""),
        "fuentes": "|".join(fuentes),
        "en_pac": "PAC" in fuentes,
        "en_midagri": "MIDAGRI" in fuentes,
        "en_cenacoop": "CENACOOP" in fuentes,
        "departamento": d.get("departamento", ""),
        "provincia": d.get("provincia", ""),
        "actividad_midagri": d.get("actividad_midagri", ""),
        "producto_midagri": d.get("producto_midagri", ""),
        "sunat_estado": d.get("sunat_estado", ""),
        "sunat_domicilio": d.get("sunat_domicilio", ""),
        "sunat_exporta": bool(d.get("sunat_exporta", False)),
        "exp_n_ops": d.get("exp_n_ops"),
        "exp_fob_usd": d.get("exp_fob"),
        "exp_n_paises": d.get("exp_n_paises"),
        "exp_paises": d.get("exp_paises", ""),
        "exp_anio_min": d.get("exp_anio_min"),
        "exp_anio_max": d.get("exp_anio_max"),
        "imp_fob_usd": d.get("imp_fob"),
        "d2024_exporta": d.get("d2024_exporta", ""),
        "d2024_fob": d.get("d2024_fob"),
        "d2024_experiencia": d.get("d2024_exp", ""),
        "d2024_trabajadores": d.get("d2024_trab"),
        "d2024_ventas": d.get("d2024_ventas"),
        "socios_total": d.get("socios_total", ""),
        "socios_h": d.get("socios_h", ""),
        "socios_m": d.get("socios_m", ""),
        "anio_inscripcion": d.get("anio_inscripcion", ""),
        "region_pac": d.get("region_pac", ""),
        "cert_pac": d.get("cert_pac", ""),
        "rep_pac": d.get("rep_pac", ""),
        "correo_pac": d.get("correo_pac", ""),
        "tel_pac": d.get("tel_pac", ""),
        "cen_email": d.get("cen_email", ""),
        "cen_tel_movil": d.get("cen_tel_movil", ""),
        "cen_web": d.get("cen_web", ""),
    })

df = pd.DataFrame(rows_out)
# Normalizar departamento
def norm_depto(v):
    if pd.isna(v) or str(v).strip() in ("", "—", "nan", "None"):
        return ""
    return str(v).strip().title()
df["departamento"] = df["departamento"].apply(norm_depto)
df.sort_values(["departamento", "nombre"], inplace=True)
df.reset_index(drop=True, inplace=True)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
df.to_csv(OUT, sep="|", index=False, encoding="utf-8")
print(f"\nGuardado: {OUT}  ({len(df)} orgs)")

# ─── 8. Estadisticas ─────────────────────────────────────────────────────
print("\n=== RESULTADOS ===")
print(f"Total universo: {len(df)}")
print(f"En PAC: {df['en_pac'].sum()}")
print(f"En MIDAGRI: {df['en_midagri'].sum()}")
print(f"En CENACOOP: {df['en_cenacoop'].sum()}")
print(f"Overlap PAC∩MIDAGRI: {((df['en_pac']==True)&(df['en_midagri']==True)).sum()}")
print(f"SUNAT ACTIVO: {(df['sunat_estado']=='ACTIVO').sum()}")
print(f"SUNAT HABIDO: {(df['sunat_domicilio']=='HABIDO').sum()}")
print(f"Exporta en SUNAT: {df['sunat_exporta'].sum()}")
brecha = ((df['sunat_exporta']==False) & (df['d2024_exporta']=='SI')).sum()
print(f"Brecha exporta (SUNAT=no, D2024=SI): {brecha}")
sin_exp = ((df['sunat_exporta']==False) & (~df['d2024_exporta'].isin(['SI']))).sum()
print(f"Sin evidencia de exportacion: {sin_exp}")
print()
print("Departamentos:")
print(df["departamento"].value_counts().head(12))
print()
print("Por fuente:")
for src, col in [("PAC","en_pac"),("MIDAGRI","en_midagri"),("CENACOOP","en_cenacoop")]:
    n = df[col].sum()
    exp = ((df[col]==True) & df["sunat_exporta"]).sum()
    print(f"  {src}: {n} orgs | {exp} exportan en SUNAT")
print()
print("Top 10 exportadoras:")
top = df[df["exp_fob_usd"] > 0].nlargest(10, "exp_fob_usd")[["nombre","departamento","exp_fob_usd","exp_n_paises","sunat_estado"]]
for _, r in top.iterrows():
    print(f"  {str(r['nombre'])[:55]} | {r['departamento']} | FOB: ${r['exp_fob_usd']:,.0f} | {r['exp_n_paises']} paises | {r['sunat_estado']}")
print()
print("Actividades (exportadoras):")
print(df[df["sunat_exporta"]==True]["actividad_midagri"].value_counts().head(6))
print()
n_email = ((df["correo_pac"].str.contains("@", na=False)) | (df["cen_email"].str.contains("@", na=False))).sum()
n_tel = ((df["tel_pac"]!="") | (df["cen_tel_movil"]!="")).sum()
print(f"Contactos: {n_email} con email | {n_tel} con telefono")
