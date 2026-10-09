"""
Replica las tablas y hallazgos del informe "MIDAGRI vs. Aduanas: Verificacion EUDR Cafe".

Cruza dos fuentes:
  1. 3 directorio - base de datos de los excels de midagri 06.10.26.xlsx
     -> hoja 'base 25 detallada (cafe)'  (autorreporte MIDAGRI, 25 organizaciones)
  2. DUA_CONSOLIDADO_con_atributos_20261002 (2).xlsx
     -> hoja 'por RUC'  (registro real de Aduanas, scrapeado de aduanet.gob.pe)

Uso:
    python generar_tablas_informe_eudr.py

Requiere: pandas, openpyxl (pip install pandas openpyxl)

Salida:
    informe_eudr_tablas.xlsx  -- un libro con una hoja por tabla del informe
    Resumen de hallazgos clave impreso por consola.
"""

import re
from pathlib import Path

import pandas as pd
from openpyxl.chart import BarChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.worksheet.worksheet import Worksheet

# ---------------------------------------------------------------------------
# Configuracion
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
MIDAGRI_FILE = BASE_DIR / "3 directorio - base de datos de los excels de midagri 06.10.26.xlsx"
DUA_FILE = BASE_DIR / "DUA_CONSOLIDADO_con_atributos_20261002 (2).xlsx"
OECE_FILE = BASE_DIR.parent / "ficharucsunat" / "ruc oece rnp ppa.xlsx"
OUTPUT_FILE = BASE_DIR / "informe_eudr_tablas.xlsx"

MIDAGRI_SHEET = "base 25 detallada (cafe)"
DUA_SHEET = "por RUC"


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

def _clean_col(col) -> str:
    """Colapsa saltos de linea y espacios multiples en un encabezado de columna."""
    return re.sub(r"\s+", " ", str(col)).strip()


def _money(x) -> float:
    try:
        return float(x) if pd.notna(x) else 0.0
    except (TypeError, ValueError):
        return 0.0


def _ruc_int(x):
    try:
        return int(x)
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------------------
# Carga de datos
# ---------------------------------------------------------------------------

def load_midagri() -> pd.DataFrame:
    """Carga y limpia la hoja 'base 25 detallada (cafe)' de MIDAGRI."""
    df = pd.read_excel(MIDAGRI_FILE, sheet_name=MIDAGRI_SHEET)
    df.columns = [_clean_col(c) for c in df.columns]
    df = df[df["RUC"].notna()].copy()
    df["RUC"] = df["RUC"].apply(_ruc_int)
    return df


def load_oece() -> dict[str, pd.DataFrame]:
    """Carga el libro complementario de PPA / OECE / RNP (597 RUC a nivel nacional)."""
    sheets = {}
    for name in ("RUC_PPA", "RUC_OECE", "RUC_OECE_PERSONAS", "RNP"):
        df = pd.read_excel(OECE_FILE, sheet_name=name)
        df.columns = [_clean_col(c) for c in df.columns]
        key_col = "ruc"
        df = df[df[key_col].notna()].copy()
        df[key_col] = df[key_col].apply(lambda v: str(_ruc_int(v)))
        sheets[name] = df
    return sheets


def load_dua() -> pd.DataFrame:
    """Carga la hoja 'por RUC' del cruce real de Aduanas (DUA_CONSOLIDADO)."""
    df = pd.read_excel(DUA_FILE, sheet_name=DUA_SHEET)
    df.columns = [_clean_col(c) for c in df.columns]
    df = df[df["ruc"].notna()].copy()
    df["ruc"] = df["ruc"].apply(_ruc_int)
    return df


# ---------------------------------------------------------------------------
# Seccion 2-3: universo y reconciliacion FOB autorreporte vs. real
# ---------------------------------------------------------------------------

FOB_COL = "EXPORTACIONES 2025 FOB DOLARES"  # tras limpiar espacios/saltos


def build_reconciliation(midagri: pd.DataFrame, dua: pd.DataFrame) -> pd.DataFrame:
    """Tabla de la Seccion 3: FOB 2025 autorreportado vs. FOB 2025 real (DUA)."""
    m = midagri[["RUC", "Organizacion" if "Organizacion" in midagri.columns else "Organización",
                 "Exporta SI/NO" if "Exporta SI/NO" in midagri.columns else "Exporta SÍ/NO",
                 FOB_COL]].copy()
    m.columns = ["ruc", "organizacion", "exporta_self", "fob25_self"]
    m["fob25_self"] = m["fob25_self"].apply(_money)

    d = dua[["ruc", "razon_social", "2025_fob", "2024_fob", "2026_fob", "total_fob", "paises"]].copy()
    d = d.rename(columns={"2025_fob": "fob25_real", "2024_fob": "fob24_real",
                           "2026_fob": "fob26_real", "total_fob": "fob_total_real"})

    out = m.merge(d, on="ruc", how="left")
    out["delta_usd"] = out["fob25_real"] - out["fob25_self"]
    out["delta_pct"] = out.apply(
        lambda r: (r["delta_usd"] / r["fob25_self"] * 100) if r["fob25_self"] else None, axis=1
    )
    return out.sort_values("fob25_self", ascending=False).reset_index(drop=True)


def summarize_reconciliation(recon: pd.DataFrame) -> None:
    declared = recon[recon["exporta_self"].astype(str).str.upper() == "SI"]
    total_self = declared["fob25_self"].sum()
    total_real = declared["fob25_real"].sum()
    n_match = (declared["delta_usd"].abs() < 1).sum()
    n_mismatch = declared["fob25_real"].notna().sum() - n_match

    print("--- Seccion 3: reconciliacion FOB 2025 ---")
    print(f"  Organizaciones que autorreportan 'Exporta: SI': {len(declared)}")
    print(f"  Total FOB autorreportado:  US$ {total_self:,.2f}")
    print(f"  Total FOB real (DUA):      US$ {total_real:,.2f}")
    if total_self:
        print(f"  Diferencia agregada:       {((total_real - total_self) / total_self) * 100:+.1f}%")
    print(f"  Coinciden al centavo:      {n_match}")
    print(f"  Difieren (ruido real):     {n_mismatch}")
    print()


# ---------------------------------------------------------------------------
# Seccion 4: caso OCUMAL / exportadores "invisibles"
# ---------------------------------------------------------------------------

def find_invisible_exporters(midagri: pd.DataFrame, dua: pd.DataFrame) -> pd.DataFrame:
    """Organizaciones que se autorreportan 'Exporta: NO' pero tienen registro DUA real."""
    exporta_col = "Exporta SI/NO" if "Exporta SI/NO" in midagri.columns else "Exporta SÍ/NO"
    org_col = "Organizacion" if "Organizacion" in midagri.columns else "Organización"
    no_exporta = midagri.loc[midagri[exporta_col].astype(str).str.upper() == "NO", ["RUC", org_col]]
    no_exporta = no_exporta.rename(columns={"RUC": "ruc", org_col: "organizacion"})

    d = dua[["ruc", "razon_social", "2024_fob", "2025_fob", "2026_fob", "total_fob", "paises"]]
    out = no_exporta.merge(d, on="ruc", how="inner")
    return out


# ---------------------------------------------------------------------------
# Seccion 5: certificaciones declaradas vs. huella documental en aduanas
# ---------------------------------------------------------------------------

def certification_gap(midagri: pd.DataFrame, dua: pd.DataFrame) -> pd.DataFrame:
    org_col = "Organizacion" if "Organizacion" in midagri.columns else "Organización"
    ct_col = next(c for c in midagri.columns if c.startswith("Certificaci"))  # Comercio Justo col (2nd match ok)
    cert_cols = [c for c in midagri.columns if c.startswith("Certificaci")]
    org_cert_col = cert_cols[0]
    ct_cert_col = cert_cols[1] if len(cert_cols) > 1 else cert_cols[0]

    m = midagri[["RUC", org_col, org_cert_col, ct_cert_col]].copy()
    m.columns = ["ruc", "organizacion", "organica_declarada", "comercio_justo_declarado"]

    d = dua[["ruc", "items_con_descripcion", "n_items_organico", "n_items_fairtrade"]]
    out = m.merge(d, on="ruc", how="inner")
    out["organica_declarada"] = out["organica_declarada"].notna() & (
        out["organica_declarada"].astype(str).str.upper() != "NO"
    )
    out["fairtrade_declarado"] = out["comercio_justo_declarado"].notna() & (
        out["comercio_justo_declarado"].astype(str).str.upper().str.strip() != "NO"
    )
    return out[["organizacion", "fairtrade_declarado", "n_items_fairtrade", "items_con_descripcion",
                "organica_declarada", "n_items_organico"]]


# ---------------------------------------------------------------------------
# Seccion 6: concentracion de puertos y agentes de aduana
# ---------------------------------------------------------------------------

def port_and_broker_concentration(dua: pd.DataFrame) -> dict:
    aduanas_count: dict[str, int] = {}
    agentes_count: dict[str, int] = {}
    for _, row in dua.iterrows():
        for a in str(row.get("aduanas_nombre") or "").split(","):
            a = a.strip()
            if a:
                aduanas_count[a] = aduanas_count.get(a, 0) + 1
        for a in str(row.get("agentes_nombre") or "").split(","):
            a = a.strip()
            if a:
                agentes_count[a] = agentes_count.get(a, 0) + 1
    return {
        "aduanas": pd.DataFrame(sorted(aduanas_count.items(), key=lambda x: -x[1]),
                                 columns=["aduana", "n_organizaciones"]),
        "agentes": pd.DataFrame(sorted(agentes_count.items(), key=lambda x: -x[1]),
                                 columns=["agente_aduana", "n_organizaciones"]),
    }


# ---------------------------------------------------------------------------
# Seccion 7: evolucion 2024-2026 (con cautela metodologica)
# ---------------------------------------------------------------------------

def year_evolution(dua: pd.DataFrame) -> pd.DataFrame:
    totals = {
        "2024": dua["2024_fob"].apply(_money).sum(),
        "2025": dua["2025_fob"].apply(_money).sum(),
        "2026 (corte parcial)": dua["2026_fob"].apply(_money).sum(),
    }
    return pd.DataFrame(list(totals.items()), columns=["anio", "fob_total_usd"])


# ---------------------------------------------------------------------------
# Seccion 9: FOB autorreportado vs. "Ventas ejecutadas de exportacion"
# ---------------------------------------------------------------------------

def fob_vs_ventas_ejecutadas(midagri: pd.DataFrame) -> pd.DataFrame:
    org_col = "Organizacion" if "Organizacion" in midagri.columns else "Organización"
    exporta_col = "Exporta SI/NO" if "Exporta SI/NO" in midagri.columns else "Exporta SÍ/NO"
    ventas_col = "Ventas_Ejec_Exp_2025"
    total_col = "Total general 2025"

    cols = ["RUC", org_col, exporta_col, FOB_COL, ventas_col, total_col]
    out = midagri[cols].copy()
    out.columns = ["ruc", "organizacion", "exporta_self", "fob25_self", "ventas_ejec_exp25", "total_general25"]
    for c in ["fob25_self", "ventas_ejec_exp25", "total_general25"]:
        out[c] = out[c].apply(_money)
    out["ratio_ventas_sobre_fob"] = out.apply(
        lambda r: (r["ventas_ejec_exp25"] / r["fob25_self"]) if r["fob25_self"] else None, axis=1
    )
    return out[(out["fob25_self"] > 0) | (out["ventas_ejec_exp25"] > 0)].sort_values(
        "ventas_ejec_exp25", ascending=False
    ).reset_index(drop=True)


# ---------------------------------------------------------------------------
# Seccion 10: socios declarados vs. "beneficiarios" PAC
# ---------------------------------------------------------------------------

def socios_vs_beneficiarios(midagri: pd.DataFrame) -> pd.DataFrame:
    org_col = "Organizacion" if "Organizacion" in midagri.columns else "Organización"
    v_col = "Numero de socios (varones)" if "Numero de socios (varones)" in midagri.columns else \
        "Número de socios (varones)"
    m_col = "Numero de socias (Mujeres)"
    benef_col = "Beneficiarios total 2025"

    out = midagri[["RUC", org_col, v_col, m_col, benef_col]].copy()
    out.columns = ["ruc", "organizacion", "socios_v", "socias_m", "beneficiarios_2025"]
    out["socios_v"] = out["socios_v"].fillna(0)
    out["socias_m"] = out["socias_m"].fillna(0)
    out["socios_total"] = out["socios_v"] + out["socias_m"]
    out = out[out["beneficiarios_2025"].notna() & (out["socios_total"] > 0)].copy()
    out["cobertura_pct"] = (out["beneficiarios_2025"] / out["socios_total"] * 100).round(0)
    return out[["organizacion", "socios_total", "beneficiarios_2025", "cobertura_pct"]].sort_values(
        "cobertura_pct"
    ).reset_index(drop=True)


# ---------------------------------------------------------------------------
# Seccion 4.8: registro en el PPA y vigencia de la representacion legal (OECE)
# ---------------------------------------------------------------------------

def ppa_and_governance(midagri: pd.DataFrame, oece_sheets: dict[str, pd.DataFrame]) -> dict:
    """PPA: confirma inscripcion organizacional (Art. 9). OECE: antiguedad del mandato
    directivo vigente, como senal de riesgo de representacion legal no capturada por el indice."""
    org_col = "Organizacion" if "Organizacion" in midagri.columns else "Organización"
    rucs = {str(_ruc_int(r)) for r in midagri["RUC"] if pd.notna(r)}

    ppa = oece_sheets["RUC_PPA"]
    ppa_match = ppa[ppa["ruc"].isin(rucs)]
    pct_en_ppa = (ppa_match["registrado"].astype(str).str.lower() == "true").mean() * 100

    personas = oece_sheets["RUC_OECE_PERSONAS"]
    personas_match = personas[personas["ruc"].isin(rucs)].copy()
    personas_match["fecha_ingreso"] = pd.to_datetime(personas_match["fecha_ingreso"], errors="coerce")
    hoy = pd.Timestamp.now()
    personas_match["antiguedad_anios"] = (hoy - personas_match["fecha_ingreso"]).dt.days / 365.25

    presidentes = personas_match[
        personas_match["cargo"].astype(str).str.contains("Presidente", case=False, na=False)
    ].copy()
    org_by_ruc = dict(zip(midagri["RUC"].apply(_ruc_int).astype(str), midagri[org_col]))
    presidentes["organizacion"] = presidentes["ruc"].map(org_by_ruc)
    presidentes = presidentes.sort_values("antiguedad_anios", ascending=False)

    rnp = oece_sheets["RNP"]
    n_en_rnp = rnp["ruc"].isin(rucs).sum()

    return {
        "pct_en_ppa": pct_en_ppa,
        "n_orgs_con_directivos": personas_match["ruc"].nunique(),
        "mandatos_presidente": presidentes[["organizacion", "ruc", "nombre", "fecha_ingreso", "antiguedad_anios"]],
        "n_en_rnp": int(n_en_rnp),
    }


# ---------------------------------------------------------------------------
# Indice de preparacion EUDR por organizacion (tiers 1/2/3)
# ---------------------------------------------------------------------------

def _parse_avance(v) -> float | None:
    """Normaliza el campo 'avance EUDR declarado' a una fraccion [0, 1] cuando es posible."""
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return None
    s = str(v).strip()
    try:
        f = float(s)
        return f / 100 if f > 1 else f
    except (TypeError, ValueError):
        pass
    m = re.search(r"(\d+(\.\d+)?)\s*%", s)
    return float(m.group(1)) / 100 if m else None


def readiness_index(midagri: pd.DataFrame, dua: pd.DataFrame) -> pd.DataFrame:
    """Construye el indice de preparacion EUDR (seccion 3.2 del documento) y clasifica
    cada organizacion en Tier 1 (alta), Tier 2 (riesgo de bloqueo) o Tier 3 (incipiente)."""
    org_col = "Organizacion" if "Organizacion" in midagri.columns else "Organización"
    exporta_col = "Exporta SI/NO" if "Exporta SI/NO" in midagri.columns else "Exporta SÍ/NO"
    cert_cols = [c for c in midagri.columns if c.startswith("Certificaci")][:2]
    dua_idx = {int(r["ruc"]): r for _, r in dua.iterrows() if pd.notna(r["ruc"])}

    rows = []
    for _, r in midagri.iterrows():
        ruc = _ruc_int(r["RUC"])
        if ruc is None:
            continue
        exporta = str(r.get(exporta_col) or "").upper()
        avance_raw = r.get("Indicar el avance con el reglamento de la EUDR")
        avance = _parse_avance(avance_raw)
        n_cert = sum(
            1 for c in cert_cols
            if pd.notna(r.get(c)) and str(r.get(c)).strip().upper() not in ("NO", "NO CUENTA", "")
        )
        sunat_formal = (r.get("Estado del Contribuyente (SUNAT)") == "ACTIVO" and
                         r.get("Condición del Contribuyente (SUNAT)") == "HABIDO")
        fob_self = _money(r.get(FOB_COL))

        d_row = dua_idx.get(ruc)
        fiabilidad, delta_pct = "Sin verificación externa (sin registro DUA)", None
        if d_row is not None:
            fob_real_25 = _money(d_row.get("2025_fob"))
            fob_real_total = _money(d_row.get("total_fob"))
            if exporta == "SI" and fob_self:
                delta_pct = (fob_real_25 - fob_self) / fob_self * 100
                fiabilidad = "Coincide con Aduanas" if abs(delta_pct) < 1 else f"Diverge {delta_pct:+.0f}%"
            elif exporta == "NO" and fob_real_total:
                fiabilidad = f'Actividad exportadora detectada en Aduanas (US$ {fob_real_total:,.0f})'

        if exporta != "SI":
            tier = "Tier 3 — preparación incipiente"
        else:
            riesgo = (avance is None or avance < 0.75) or (not sunat_formal) or \
                     (delta_pct is not None and abs(delta_pct) >= 10)
            tier = "Tier 2 — riesgo de bloqueo" if riesgo else "Tier 1 — preparación alta"

        rows.append(dict(ruc=ruc, organizacion=r.get(org_col), exporta=exporta,
                          avance_eudr_declarado=avance_raw, avance_eudr_pct=avance,
                          n_certificaciones=n_cert, formal_sunat=sunat_formal,
                          fob25_self=fob_self, fiabilidad_autorreporte=fiabilidad,
                          delta_fob_pct=delta_pct, tier=tier))

    return pd.DataFrame(rows).sort_values(["tier", "fob25_self"], ascending=[True, False]).reset_index(drop=True)


# ---------------------------------------------------------------------------
# Seccion 11: reconciliacion de peso fisico (kg) vs. Aduanas
# ---------------------------------------------------------------------------

def weight_reconciliation(midagri: pd.DataFrame, dua: pd.DataFrame) -> pd.DataFrame:
    """FOB y kg autorreportados (col. 'Q EN KILOS') vs. peso neto real (DUA), con precio implicito US$/kg."""
    org_col = "Organizacion" if "Organizacion" in midagri.columns else "Organización"
    exporta_col = "Exporta SI/NO" if "Exporta SI/NO" in midagri.columns else "Exporta SÍ/NO"

    m = midagri[["RUC", org_col, exporta_col, FOB_COL, "Q EN KILOS"]].copy()
    m.columns = ["ruc", "organizacion", "exporta_self", "fob25_self", "kg25_self"]
    m = m[m["exporta_self"].astype(str).str.upper() == "SI"].copy()
    for c in ["fob25_self", "kg25_self"]:
        m[c] = m[c].apply(_money)

    d = dua[["ruc", "2025_fob", "2025_peso_neto"]].rename(
        columns={"2025_fob": "fob25_real", "2025_peso_neto": "kg25_real"}
    )

    out = m.merge(d, on="ruc", how="left")
    out["delta_kg_pct"] = out.apply(
        lambda r: (r["kg25_real"] - r["kg25_self"]) / r["kg25_self"] * 100
        if r["kg25_self"] and pd.notna(r["kg25_real"]) else None, axis=1
    )
    out["usd_kg_self"] = out.apply(
        lambda r: r["fob25_self"] / r["kg25_self"] if r["kg25_self"] else None, axis=1
    )
    out["usd_kg_real"] = out.apply(
        lambda r: r["fob25_real"] / r["kg25_real"] if r["kg25_real"] else None, axis=1
    )
    return out.sort_values("delta_kg_pct").reset_index(drop=True)


# ---------------------------------------------------------------------------
# Seccion 12: otras inconsistencias de dato (_ORIGEN, fechas invertidas)
# ---------------------------------------------------------------------------

def other_data_issues(midagri: pd.DataFrame) -> dict:
    org_col = "Organizacion" if "Organizacion" in midagri.columns else "Organización"

    origen_check = midagri[[org_col, "Región", "_ORIGEN"]].copy()
    origen_check.columns = ["organizacion", "region_real", "origen_declarado"]
    origen_check["coherente"] = origen_check.apply(
        lambda r: str(r["origen_declarado"]).strip().lower().find(
            str(r["region_real"]).strip().lower()) >= 0
        if pd.notna(r["origen_declarado"]) and pd.notna(r["region_real"]) else None, axis=1
    )

    dates = midagri[[org_col, "Fecha de inicio de actividades", "Fecha de Inscripción SUNAT"]].copy()
    dates.columns = ["organizacion", "inicio_actividades", "inscripcion_sunat"]
    dates["fecha_invertida"] = pd.to_datetime(dates["inicio_actividades"], errors="coerce") > \
        pd.to_datetime(dates["inscripcion_sunat"], errors="coerce")
    dates_invertidas = dates[dates["fecha_invertida"] == True]  # noqa: E712

    return {"origen": origen_check, "fechas_invertidas": dates_invertidas}


# ---------------------------------------------------------------------------
# Pestana "Atributos completos": 9 tablas tematicas (todas las columnas)
# ---------------------------------------------------------------------------

def attribute_tables(midagri: pd.DataFrame) -> dict:
    org_col = "Organizacion" if "Organizacion" in midagri.columns else "Organización"

    def pick(cols):
        return midagri[[c for c in cols if c in midagri.columns]].copy()

    tables = {}

    tables["01_identificacion"] = pick([
        "RUC", org_col, "Región", "Provincia", "Tipo de Contribuyente (SUNAT)", "CIIU Principal",
    ])

    tables["02_perfil_agronomico"] = pick([
        org_col, "Altitud de las unidades productivas: (rango - m.s.n.m)",
        "Número de socios (varones)", "Numero de socias (Mujeres)",
        "Numero de hectareas totales de la organización", "Producto Dom",
    ])

    cert_cols = [c for c in midagri.columns if c.startswith("Certificaci")] + \
        [c for c in midagri.columns if c.startswith("Con que otras certificaciones")]
    tables["03_certificaciones"] = pick([org_col] + cert_cols)

    tables["04_intervencion_pac"] = pick([
        org_col, "Año de intervención",
        "Colocar la Etapa en la que se encuentra el PAC: Formulación Ejecución Finalizado",
        "Intervención 2020-2026", "Indicar el avance con el reglamento de la EUDR",
    ])

    benef_cols = [c for c in midagri.columns if c.startswith("Beneficiarios total")]
    tables["05_beneficiarios_historico"] = pick([org_col] + benef_cols)

    at_cols = [c for c in midagri.columns if "Asistencias" in c or "Talleres" in c]
    tables["06_asistencia_tecnica"] = pick([org_col] + at_cols)

    ventas_cols = [c for c in midagri.columns if c.startswith("Ventas totales")]
    tables["07_ventas_historicas"] = pick([org_col] + ventas_cols)

    comprobante_cols = [c for c in midagri.columns if "2025" in c and (
        "Boleta" in c or "Declaración Jurada" in c or c == "Factura 2025" or
        "Guía de Remisión" in c or "Liquidación de Compra" in c or "Total general" in c
    )]
    tables["08_comprobantes_2025"] = pick([org_col] + comprobante_cols)

    tables["09_estado_sunat"] = pick([
        org_col, "Estado del Contribuyente (SUNAT)", "Condición del Contribuyente (SUNAT)",
        "Actividad de Comercio Exterior", "Afecto Nuevo RUS",
    ])

    return tables


# ---------------------------------------------------------------------------
# Graficos nativos de Excel (un grafico por hallazgo visual del informe)
# ---------------------------------------------------------------------------

def _add_bar_chart(
    ws: Worksheet,
    *,
    title: str,
    y_title: str,
    cat_col: int,
    val_cols: list[int],
    n_rows: int,
    anchor: str,
    series_titles: list[str] | None = None,
    height_cm: float = 9.0,
    width_cm: float = 20.0,
) -> None:
    """Agrega un BarChart de columnas a `ws`, leyendo datos de las columnas
    1-indexadas `val_cols` (serie(s)) y `cat_col` (categorias), filas 2..n_rows+1
    (fila 1 = encabezado)."""
    chart = BarChart()
    chart.type = "col"
    chart.title = title
    chart.y_axis.title = y_title
    chart.x_axis.title = None
    chart.height = height_cm
    chart.width = width_cm
    chart.gapWidth = 60

    cats = Reference(ws, min_col=cat_col, min_row=2, max_row=n_rows + 1)
    for i, col in enumerate(val_cols):
        data = Reference(ws, min_col=col, min_row=1, max_row=n_rows + 1)
        chart.add_data(data, titles_from_data=True)
        if series_titles:
            chart.series[i].tx = None  # deja el titulo tomado de to_data; nombre visible via leyenda
    chart.set_categories(cats)
    chart.dataLabels = DataLabelList()
    chart.dataLabels.showVal = False
    ws.add_chart(chart, anchor)


def add_report_charts(sheets: dict[str, Worksheet], recon_chart_df: pd.DataFrame,
                       ports: dict, years: pd.DataFrame, fob_vs_ventas: pd.DataFrame,
                       socios_benef: pd.DataFrame, peso_recon: pd.DataFrame,
                       readiness: pd.DataFrame) -> None:
    """Inserta en el libro los graficos equivalentes a los del informe."""

    # Indice de preparacion -- FOB por organizacion exportadora, separado en dos series
    # (Tier 1 / Tier 2) para que cada una tome un color distinto automaticamente.
    exporters = readiness[readiness["tier"] != "Tier 3 — preparación incipiente"].copy()
    exporters["fob_tier1"] = exporters["fob25_self"].where(
        exporters["tier"].str.startswith("Tier 1"), 0.0)
    exporters["fob_tier2"] = exporters["fob25_self"].where(
        exporters["tier"].str.startswith("Tier 2"), 0.0)
    exporters = exporters.sort_values("fob25_self", ascending=False)
    ws_readiness = sheets["00_indice_preparacion_EUDR"]
    start_col = 12  # columna L en adelante, para no pisar la tabla principal
    ws_readiness.cell(row=1, column=start_col, value="organizacion")
    ws_readiness.cell(row=1, column=start_col + 1, value="FOB Tier 1")
    ws_readiness.cell(row=1, column=start_col + 2, value="FOB Tier 2")
    for i, (_, r) in enumerate(exporters.iterrows(), start=2):
        ws_readiness.cell(row=i, column=start_col, value=r["organizacion"])
        ws_readiness.cell(row=i, column=start_col + 1, value=r["fob_tier1"])
        ws_readiness.cell(row=i, column=start_col + 2, value=r["fob_tier2"])
    _add_bar_chart(
        ws_readiness, title="FOB 2025 por organizacion, coloreado por tier de preparacion EUDR",
        y_title="US$", cat_col=start_col, val_cols=[start_col + 1, start_col + 2],
        n_rows=len(exporters), anchor="A30",
        series_titles=["Tier 1 — preparación alta", "Tier 2 — riesgo de bloqueo"],
    )

    # Seccion 3 -- delta FOB real vs. autorreportado (grafico de barras con signo)
    ws = sheets["03b_grafico_delta_FOB"]
    _add_bar_chart(
        ws, title="FOB real (DUA) menos FOB autorreportado, por organizacion",
        y_title="Diferencia, US$", cat_col=1, val_cols=[2], n_rows=len(recon_chart_df),
        anchor="D2",
    )

    # Seccion 6 -- concentracion por agente de aduana
    ws = sheets["06_concentracion_agentes"]
    _add_bar_chart(
        ws, title="Organizaciones por agente de aduana",
        y_title="N de organizaciones", cat_col=1, val_cols=[2],
        n_rows=len(ports["agentes"]), anchor="D2",
    )

    # Seccion 7 -- evolucion anual del FOB real
    ws = sheets["07_evolucion_anual"]
    _add_bar_chart(
        ws, title="FOB real por año (2026 es corte parcial)",
        y_title="FOB, US$", cat_col=1, val_cols=[2], n_rows=len(years), anchor="D2",
    )

    # Seccion 9 -- FOB autorreportado vs. Ventas ejecutadas de exportacion
    ws = sheets["09_FOB_vs_ventas_ejec"]
    _add_bar_chart(
        ws, title="FOB autorreportado vs. Ventas ejec. de exportacion (misma ficha MIDAGRI)",
        y_title="US$", cat_col=2, val_cols=[4, 5], n_rows=len(fob_vs_ventas), anchor="H2",
        series_titles=["FOB autorreportado", "Ventas ejec. exportacion"],
    )

    # Seccion 10 -- socios totales vs. beneficiarios PAC 2025
    ws = sheets["10_socios_vs_beneficiarios"]
    _add_bar_chart(
        ws, title="Socios totales vs. 'beneficiarios' PAC 2025",
        y_title="Personas", cat_col=1, val_cols=[2, 3], n_rows=len(socios_benef), anchor="F2",
        series_titles=["Socios totales", "Beneficiarios PAC 2025"],
    )

    # Seccion 11 -- diferencia de peso (kg) real vs. autorreportado
    # columnas (1-indexadas): 1 ruc, 2 organizacion, 3 exporta_self, 4 fob25_self,
    # 5 kg25_self, 6 fob25_real, 7 kg25_real, 8 delta_kg_pct, 9 usd_kg_self, 10 usd_kg_real
    ws = sheets["11_reconciliacion_peso"]
    _add_bar_chart(
        ws, title="Diferencia de peso exportado 2025: real (DUA) menos autorreportado, %",
        y_title="%", cat_col=2, val_cols=[8], n_rows=len(peso_recon), anchor="L2",
    )


# ---------------------------------------------------------------------------
# Orquestacion
# ---------------------------------------------------------------------------

def main() -> None:
    if not MIDAGRI_FILE.exists() or not DUA_FILE.exists():
        raise FileNotFoundError(
            "Coloca este script en la misma carpeta que los dos archivos .xlsx fuente, "
            "o ajusta MIDAGRI_FILE / DUA_FILE al inicio del script."
        )

    midagri = load_midagri()
    dua = load_dua()
    oece_sheets = load_oece() if OECE_FILE.exists() else None
    governance = ppa_and_governance(midagri, oece_sheets) if oece_sheets else None

    recon = build_reconciliation(midagri, dua)
    invisibles = find_invisible_exporters(midagri, dua)
    cert_gap = certification_gap(midagri, dua)
    ports = port_and_broker_concentration(dua)
    years = year_evolution(dua)
    fob_vs_ventas = fob_vs_ventas_ejecutadas(midagri)
    socios_benef = socios_vs_beneficiarios(midagri)
    peso_recon = weight_reconciliation(midagri, dua)
    data_issues = other_data_issues(midagri)
    readiness = readiness_index(midagri, dua)
    attrs = attribute_tables(midagri)

    # --- resumen por consola, para verificar contra el informe ---
    summarize_reconciliation(recon)

    print("--- Seccion 4: exportadores 'invisibles' (autorreporte NO, DUA real SI) ---")
    if invisibles.empty:
        print("  Ninguno encontrado.")
    else:
        for _, r in invisibles.iterrows():
            print(f"  {r['organizacion']}: FOB24=US${_money(r['2024_fob']):,.2f}  "
                  f"FOB25=US${_money(r['2025_fob']):,.2f}  paises={r['paises']}")
    print()

    print("--- Seccion 6: agente de aduana mas usado ---")
    top_agent = ports["agentes"].iloc[0]
    total_orgs = ports["agentes"]["n_organizaciones"].sum()
    print(f"  {top_agent['agente_aduana']}: {top_agent['n_organizaciones']} organizaciones "
          f"(de un total de referencias = {total_orgs})")
    print()

    print("--- Seccion 7: FOB real por anio (ojo: 2026 es corte parcial) ---")
    print(years.to_string(index=False))
    print()

    print("--- Seccion 9: FOB autorreportado vs. 'Ventas ejec. exportacion' (mismo archivo) ---")
    sample = fob_vs_ventas[fob_vs_ventas["fob25_self"] > 0].head(8)
    print(sample[["organizacion", "fob25_self", "ventas_ejec_exp25", "ratio_ventas_sobre_fob"]]
          .to_string(index=False))
    print()

    print("--- Seccion 10: organizaciones con menor cobertura 'beneficiarios'/socios ---")
    print(socios_benef.head(5).to_string(index=False))
    print()

    print("--- Seccion 11: reconciliacion de peso fisico (kg), implicit USD/kg ---")
    print(peso_recon[["organizacion", "kg25_self", "kg25_real", "delta_kg_pct",
                       "usd_kg_self", "usd_kg_real"]].to_string(index=False))
    print()

    print("--- Indice de preparacion EUDR (tiers) ---")
    print(readiness["tier"].value_counts().to_string())
    print()
    print(readiness[["organizacion", "tier", "avance_eudr_declarado", "n_certificaciones",
                      "formal_sunat", "fiabilidad_autorreporte"]].to_string(index=False))
    print()

    if governance:
        print("--- Seccion 4.8: registro PPA y vigencia de mandatos (OECE) ---")
        print(f"  Organizaciones registradas en el PPA: {governance['pct_en_ppa']:.0f}%")
        print(f"  Organizaciones con directivos en OECE: {governance['n_orgs_con_directivos']} de 25")
        print(f"  Organizaciones con registro en RNP: {governance['n_en_rnp']}")
        print("  Mandatos de Presidente, por antiguedad:")
        print(governance["mandatos_presidente"].to_string(index=False))
        print()

    print("--- Seccion 12: otras inconsistencias de dato ---")
    n_incoherentes = (data_issues["origen"]["coherente"] == False).sum()  # noqa: E712
    print(f"  Campo '_ORIGEN' incoherente con la region real en {n_incoherentes} de "
          f"{data_issues['origen']['coherente'].notna().sum()} filas evaluadas.")
    if not data_issues["fechas_invertidas"].empty:
        print("  Organizaciones con 'inicio de actividades' posterior a 'inscripcion SUNAT':")
        for _, r in data_issues["fechas_invertidas"].iterrows():
            print(f"    {r['organizacion']}: inicio={r['inicio_actividades']}  "
                  f"inscripcion={r['inscripcion_sunat']}")
    print()

    # tabla compacta para el grafico de la Seccion 3 (delta FOB, solo exportadores con dato real)
    recon_chart_df = (
        recon[(recon["exporta_self"].astype(str).str.upper() == "SI") & recon["delta_usd"].notna()]
        [["organizacion", "delta_usd"]]
        .sort_values("delta_usd")
        .reset_index(drop=True)
    )

    # --- exportar todo a un unico libro Excel, una hoja por tabla ---
    with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
        recon.to_excel(writer, sheet_name="03_reconciliacion_FOB", index=False)
        recon_chart_df.to_excel(writer, sheet_name="03b_grafico_delta_FOB", index=False)
        invisibles.to_excel(writer, sheet_name="04_exportadores_invisibles", index=False)
        cert_gap.to_excel(writer, sheet_name="05_certificaciones_vs_aduana", index=False)
        ports["aduanas"].to_excel(writer, sheet_name="06_concentracion_puertos", index=False)
        ports["agentes"].to_excel(writer, sheet_name="06_concentracion_agentes", index=False)
        years.to_excel(writer, sheet_name="07_evolucion_anual", index=False)
        fob_vs_ventas.to_excel(writer, sheet_name="09_FOB_vs_ventas_ejec", index=False)
        socios_benef.to_excel(writer, sheet_name="10_socios_vs_beneficiarios", index=False)
        readiness.to_excel(writer, sheet_name="00_indice_preparacion_EUDR", index=False)
        if governance:
            governance["mandatos_presidente"].to_excel(
                writer, sheet_name="04_8_vigencia_mandatos", index=False)
        peso_recon.to_excel(writer, sheet_name="11_reconciliacion_peso", index=False)
        data_issues["origen"].to_excel(writer, sheet_name="12_origen_incoherente", index=False)
        data_issues["fechas_invertidas"].to_excel(writer, sheet_name="12_fechas_invertidas", index=False)
        for name, table in attrs.items():
            table.to_excel(writer, sheet_name=f"anexo_{name}"[:31], index=False)

        add_report_charts(writer.sheets, recon_chart_df, ports, years, fob_vs_ventas,
                           socios_benef, peso_recon, readiness)

    print(f"Libro generado (con tablas y graficos): {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
