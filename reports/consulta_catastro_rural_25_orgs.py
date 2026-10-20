"""
Consulta en vivo el geoservicio publico del Catastro Rural de MIDAGRI
(georural.midagri.gob.pe) para los 16 distritos donde se ubican las 25
organizaciones cafetaleras de 'base 25 detallada (cafe)', y genera la
tabla comparativa que sustenta
'Nota Tecnica - Cobertura del Catastro Rural MIDAGRI en los 25 casos.md'.

Fuente: ArcGIS REST Server publico, sin autenticacion.
  Capa 0  "Predio Rural": geometria + area_ha + id_dist (ubigeo INEI de 6
          digitos) + observacion (vinculo a personas en el Sistema SSET).
          NO tiene campo de titular, DNI, RUC, ni fecha de actualizacion,
          ni estado de titulacion -- son limitaciones reales de la fuente,
          no supuestos.
  Capa 8  "Proyectos Catastrales": nombre y codigo de cada proyecto
          catastral vigente, a nivel de departamento.

Uso:
    python consulta_catastro_rural_25_orgs.py

Requiere: pandas, requests, openpyxl.
Salida: catastro_rural_25_orgs.xlsx (tablas) + impresion de hallazgos.
"""

import ssl
from pathlib import Path

import pandas as pd
import requests
import truststore

# georural.midagri.gob.pe no envia la cadena de certificados completa en el
# handshake TLS; el almacen "certifi" que usa requests por defecto no la
# completa, pero el almacen de certificados del sistema (Windows/schannel) si
# la tiene -- lo mismo que usan curl y git en este equipo. truststore hace que
# requests use ese almacen del sistema en vez de certifi.
truststore.inject_into_ssl()

BASE_DIR = Path(__file__).resolve().parent
MIDAGRI_FILE = BASE_DIR / "3 directorio - base de datos de los excels de midagri 06.10.26.xlsx"
OUTPUT_FILE = BASE_DIR / "catastro_rural_25_orgs.xlsx"

REST_BASE = "https://georural.midagri.gob.pe/geoservicios/rest/services/public/Catastro_Rural/MapServer"
TIMEOUT = 30

# Departamentos (codigo INEI de 2 digitos) que cubren las 25 organizaciones
DEPARTAMENTOS = {"01": "Amazonas", "05": "Ayacucho", "06": "Cajamarca",
                  "08": "Cusco", "12": "Junín", "19": "Pasco", "22": "San Martín"}


def _get(path: str, params: dict) -> dict:
    params = {**params, "f": "json"}
    r = requests.get(f"{REST_BASE}{path}", params=params, timeout=TIMEOUT)
    r.raise_for_status()
    data = r.json()
    if "error" in data:
        raise RuntimeError(f"Error del geoservicio en {path}: {data['error']}")
    return data


def load_midagri_ubigeos() -> pd.DataFrame:
    """Un registro por distrito unico de las 25 organizaciones, con la lista de
    organizaciones, socios y hectareas que cada una declara en ese distrito."""
    df = pd.read_excel(MIDAGRI_FILE, sheet_name="base 25 detallada (cafe)")
    df.columns = [str(c).replace("\n", " ").strip() for c in df.columns]
    import re
    df.columns = [re.sub(r"\s+", " ", c) for c in df.columns]

    org_col = "Organización"
    ha_col = "Numero de hectareas totales de la organización"
    v_col = "Número de socios (varones)"
    m_col = "Numero de socias (Mujeres)"

    df["ubigeo"] = df["Ubigeo"].apply(lambda x: f"{int(x):06d}")
    df["socios_total"] = df[v_col].fillna(0) + df[m_col].fillna(0)

    rows = []
    for ubigeo, g in df.groupby("ubigeo"):
        rows.append(dict(
            ubigeo=ubigeo,
            region=g["Región"].iloc[0],
            provincia=g["Provincia"].iloc[0],
            distrito=g["Distrito"].iloc[0],
            organizaciones=" | ".join(g[org_col].tolist()),
            n_organizaciones=len(g),
            socios_declarados=int(g["socios_total"].sum()),
            ha_declaradas=float(g[ha_col].sum()),
        ))
    return pd.DataFrame(rows).sort_values("ubigeo").reset_index(drop=True)


def query_catastro_por_distrito(ubigeos: list[str]) -> pd.DataFrame:
    """Capa 0 'Predio Rural': conteo y area catastrada (ha) por distrito,
    agrupado server-side (groupByFieldsForStatistics)."""
    where = "id_dist IN (" + ",".join(f"'{u}'" for u in ubigeos) + ")"
    data = _get("/0/query", {
        "where": where,
        "outStatistics": (
            '[{"statisticType":"count","onStatisticField":"objectid","outStatisticFieldName":"n_predios"},'
            '{"statisticType":"sum","onStatisticField":"area_ha","outStatisticFieldName":"area_catastrada_ha"}]'
        ),
        "groupByFieldsForStatistics": "id_dist",
        "orderByFields": "id_dist",
        "returnGeometry": "false",
    })
    rows = [f["attributes"] for f in data.get("features", [])]
    out = pd.DataFrame(rows).rename(columns={"id_dist": "ubigeo"})
    if out.empty:
        out = pd.DataFrame(columns=["ubigeo", "n_predios", "area_catastrada_ha"])
    return out


def query_total_nacional() -> int:
    """Capa 0, sin filtro: total de predios en toda la capa (contexto nacional)."""
    data = _get("/0/query", {
        "where": "1=1",
        "outStatistics": '[{"statisticType":"count","onStatisticField":"objectid","outStatisticFieldName":"n_total"}]',
    })
    return int(data["features"][0]["attributes"]["n_total"])


def query_proyectos_catastrales(dept_codes: list[str]) -> pd.DataFrame:
    """Capa 8 'Proyectos Catastrales': nombre y codigo de cada proyecto vigente
    en los departamentos de interes (sin filtro distrital -- la capa no lo trae)."""
    where = "id_dpto IN (" + ",".join(f"'{d}'" for d in dept_codes) + ")"
    data = _get("/8/query", {
        "where": where,
        "outFields": "id_dpto,nomdpto,cod_proy,nombre_proy",
        "returnGeometry": "false",
    })
    rows = [f["attributes"] for f in data.get("features", [])]
    return pd.DataFrame(rows).sort_values(["id_dpto", "nombre_proy"]).reset_index(drop=True)


def main() -> None:
    midagri = load_midagri_ubigeos()
    ubigeos = midagri["ubigeo"].tolist()

    catastro = query_catastro_por_distrito(ubigeos)
    comparativo = midagri.merge(catastro, on="ubigeo", how="left")
    comparativo["n_predios"] = comparativo["n_predios"].fillna(0).astype(int)
    comparativo["area_catastrada_ha"] = comparativo["area_catastrada_ha"].fillna(0.0)
    comparativo["ratio_area_catastrada_vs_declarada"] = (
        comparativo["area_catastrada_ha"] / comparativo["ha_declaradas"]
    ).round(2)

    total_nacional = query_total_nacional()
    proyectos = query_proyectos_catastrales(list(DEPARTAMENTOS.keys()))

    print("--- Comparativo por distrito (capa 'Predio Rural') ---")
    print(comparativo.to_string(index=False))
    print()
    print(f"--- Contexto nacional: {total_nacional:,} predios en toda la capa a nivel Peru ---")
    print()
    print(f"--- Proyectos catastrales nombrados en los {len(DEPARTAMENTOS)} departamentos de interes ---")
    print(f"  Total encontrados: {len(proyectos)}")
    print(proyectos.to_string(index=False))

    sin_dato = comparativo[comparativo["n_predios"] == 0]
    if not sin_dato.empty:
        print()
        print("--- Distritos SIN predios en la capa publica (no implica ausencia real, ver limitaciones) ---")
        print(sin_dato[["ubigeo", "region", "provincia", "distrito", "organizaciones"]].to_string(index=False))

    with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
        comparativo.to_excel(writer, sheet_name="comparativo_distrito", index=False)
        proyectos.to_excel(writer, sheet_name="proyectos_catastrales", index=False)
        pd.DataFrame([{"n_total_predios_nacional": total_nacional}]).to_excel(
            writer, sheet_name="contexto_nacional", index=False)

    print(f"\nLibro generado: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
