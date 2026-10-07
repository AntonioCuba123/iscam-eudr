#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Descarga los archivos OCDS anuales publicados por Open Contracting Partnership
(mirror de contratacionesabiertas.oece.gob.pe/OSCE-OECE) y extrae, para el
universo de RUC de rucs.txt/RUC_ID, los procesos, adjudicaciones y contratos
del Estado peruano en los que cada RUC aparece como proveedor/postor.

Por qué este camino y no la API de OECE:
  - https://contratacionesabiertas.oece.gob.pe/api/v1/search?supplier=PE-RUC-{ruc}
    responde 200 con JSON valido, pero el parametro `supplier` se ignora en
    el servidor: devuelve el corpus completo (2.75M+ resultados) sin filtrar,
    verificado en vivo el 2026-09-23 comparando 3 llamadas con RUC distinto,
    RUC inventado y sin parametro -> mismo total_results en las tres.
  - El unico camino verificado que SI funciona es la descarga masiva (bulk)
    republicada en https://data.open-contracting.org/en/publication/135 :
    archivos .jsonl.gz por anio (2003-actual), cada linea es un release OCDS
    "compiled" completo con buyer/tender/parties/awards/contracts. Confirmado
    con curl -I (redirige a un CDN real) y con una descarga completa del
    archivo 2026 (141 MB, estructura verificada linea por linea).

Salida: un .txt tab-delimited (mismo formato que las demas fuentes del
proyecto: columnas + fecha_consulta), listo para cargar en la pestana
HECHO_CONTRATACION_ESTATAL de BASE CONSOLIDADA.xlsx.

Uso tipico:
    python oece_contrataciones_por_ruc.py
    python oece_contrataciones_por_ruc.py --years 2015-2026
    python oece_contrataciones_por_ruc.py --years all
    python oece_contrataciones_por_ruc.py --ruc-file rucs.txt

Requisitos: solo la libreria estandar de Python + openpyxl (ya presente en
este entorno) para leer el universo de RUC desde BASE CONSOLIDADA.xlsx.
"""

from __future__ import annotations

import argparse
import gzip
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_XLSX = BASE_DIR / "BASE CONSOLIDADA.xlsx"
DEFAULT_CACHE_DIR = BASE_DIR / "cache_ocds"
DEFAULT_OUT = BASE_DIR / "ruc-contratacion-estatal.txt"
DEFAULT_CTL_LOG = BASE_DIR / "ruc-contratacion-estatal.ctl_fuente_consulta.txt"

BULK_URL_TMPL = "https://data.open-contracting.org/en/publication/135/download?name={name}"

# RUC conocido que falta en RUC_ID pero SI esta en el universo de consulta
# (ver README de BASE CONSOLIDADA.xlsx, seccion "Tratamiento", paso 1).
KNOWN_MISSING_RUC = {"20404057805": "COOPERATIVA AGRARIA ACOPAGRO LTDA"}

FIELDNAMES = [
    "ruc",
    "razon_social_ruc",
    "ocid",
    "nivel_registro",
    "entidad_ruc",
    "entidad_nombre",
    "objeto",
    "monto",
    "moneda",
    "fecha",
    "estado",
    "metodo_contratacion",
    "rol_en_proceso",
    "fuente",
    "fecha_consulta",
]


def utcnow_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def load_ruc_universe(xlsx_path: Path, ruc_file: Path | None) -> dict[str, str]:
    """Devuelve {ruc: razon_social}. Prioriza --ruc-file si se pasa; si no,
    lee la hoja RUC_ID de BASE CONSOLIDADA.xlsx y agrega el RUC conocido que
    falta ahi (ver README del libro)."""
    universe: dict[str, str] = {}

    if ruc_file is not None:
        for line in ruc_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t") if "\t" in line else [line]
            ruc = parts[0].strip()
            razon = parts[1].strip() if len(parts) > 1 else ""
            if ruc:
                universe[ruc] = razon
        return universe

    import openpyxl

    wb = openpyxl.load_workbook(xlsx_path, read_only=True, data_only=True)
    ws = wb["RUC_ID"]
    rows = ws.iter_rows(min_row=2, values_only=True)
    for row in rows:
        if not row or not row[0]:
            continue
        ruc = str(row[0]).strip()
        razon = str(row[1]).strip() if len(row) > 1 and row[1] else ""
        universe[ruc] = razon

    for ruc, razon in KNOWN_MISSING_RUC.items():
        universe.setdefault(ruc, razon)

    return universe


def resolve_years(years_arg: str) -> list[int]:
    current_year = datetime.now().year
    if years_arg == "all":
        return list(range(2003, current_year + 1))
    if "-" in years_arg:
        start, end = years_arg.split("-", 1)
        return list(range(int(start), int(end) + 1))
    if "," in years_arg:
        return sorted(int(y.strip()) for y in years_arg.split(",") if y.strip())
    return [int(years_arg)]


def download_year(year: int, cache_dir: Path) -> Path:
    cache_dir.mkdir(parents=True, exist_ok=True)
    dest = cache_dir / f"{year}.jsonl.gz"
    if dest.exists() and dest.stat().st_size > 0:
        print(f"  [{year}] ya en cache ({dest.stat().st_size / 1_048_576:.1f} MB), omito descarga")
        return dest

    url = BULK_URL_TMPL.format(name=f"{year}.jsonl.gz")
    print(f"  [{year}] descargando {url} ...")
    tmp = dest.with_suffix(dest.suffix + ".part")
    result = subprocess.run(
        ["curl", "-sL", "--fail", "--max-time", "1800", "-o", str(tmp), url],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 or not tmp.exists() or tmp.stat().st_size == 0:
        if tmp.exists():
            tmp.unlink()
        print(f"  [{year}] SIN DATOS o falla de descarga (rc={result.returncode}): {result.stderr.strip()}")
        return None
    tmp.rename(dest)
    print(f"  [{year}] descargado ({dest.stat().st_size / 1_048_576:.1f} MB)")
    return dest


def iter_releases(gz_path: Path):
    with gzip.open(gz_path, "rt", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                print(f"    linea {line_no} de {gz_path.name}: JSON invalido, se omite", file=sys.stderr)
                continue


def party_ruc_matches(party: dict, ruc_universe: dict[str, str]) -> list[str]:
    """Devuelve los RUC de nuestro universo que calzan con este party,
    revisando tanto identifier como additionalIdentifiers (algunos
    proveedores, sobre todo consorcios, traen el RUC solo ahi)."""
    matches: set[str] = set()
    identifiers = [party.get("identifier")] + list(party.get("additionalIdentifiers") or [])
    for ident in identifiers:
        if not ident:
            continue
        if ident.get("scheme") == "PE-RUC":
            ruc_id = str(ident.get("id") or "").strip()
            if ruc_id in ruc_universe:
                matches.add(ruc_id)
    return sorted(matches)


def extract_rows_for_release(release: dict, ruc_universe: dict[str, str]) -> list[dict]:
    parties = release.get("parties") or []
    ocid = release.get("ocid", "")
    buyer = release.get("buyer") or {}
    tender = release.get("tender") or {}
    awards = release.get("awards") or []
    contracts = release.get("contracts") or []
    awards_by_id = {a.get("id"): a for a in awards if a.get("id")}

    # party.id -> party, para resolver awards/contracts por id de proveedor
    parties_by_id = {p.get("id"): p for p in parties if p.get("id")}

    # El RUC del comprador vive en su registro completo dentro de parties[],
    # no en el objeto `buyer` de primer nivel (que solo trae id/name).
    buyer_party = parties_by_id.get(buyer.get("id")) or {}
    entidad_ruc = next(
        (
            ai.get("id")
            for ai in (buyer_party.get("additionalIdentifiers") or [])
            if ai.get("scheme") == "PE-RUC"
        ),
        "",
    )
    if not entidad_ruc and (buyer_party.get("identifier") or {}).get("scheme") == "PE-RUC":
        entidad_ruc = buyer_party["identifier"].get("id", "")

    rows: list[dict] = []
    seen_ruc_in_release: set[str] = set()

    for party in parties:
        matched_rucs = party_ruc_matches(party, ruc_universe)
        if not matched_rucs:
            continue
        roles = party.get("roles") or []
        party_id = party.get("id")

        for ruc in matched_rucs:
            if ruc in seen_ruc_in_release:
                continue  # 1 fila por RUC por release (evita duplicar por rol repetido)

            # 1) Buscar contrato firmado que enlace a un award donde este RUC es proveedor
            contract_row = None
            for c in contracts:
                award = awards_by_id.get(c.get("awardID"))
                if not award:
                    continue
                supplier_ids = [s.get("id") for s in (award.get("suppliers") or [])]
                if party_id in supplier_ids:
                    contract_row = {
                        "nivel_registro": "contrato",
                        "monto": (c.get("value") or {}).get("amount"),
                        "moneda": (c.get("value") or {}).get("currency"),
                        "fecha": c.get("dateSigned") or award.get("date"),
                        "estado": c.get("status"),
                        "objeto": c.get("title") or award.get("title") or tender.get("title"),
                    }
                    break

            # 2) Si no hay contrato, buscar adjudicacion (award) donde este RUC es proveedor
            award_row = None
            if contract_row is None:
                for a in awards:
                    supplier_ids = [s.get("id") for s in (a.get("suppliers") or [])]
                    if party_id in supplier_ids:
                        award_row = {
                            "nivel_registro": "adjudicacion",
                            "monto": (a.get("value") or {}).get("amount"),
                            "moneda": (a.get("value") or {}).get("currency"),
                            "fecha": a.get("date"),
                            "estado": a.get("status") or a.get("statusDetails"),
                            "objeto": a.get("title") or tender.get("title"),
                        }
                        break

            # 3) Si tampoco hay award, dejar registro a nivel de proceso/postor
            base = contract_row or award_row or {
                "nivel_registro": "proceso",
                "monto": (tender.get("value") or {}).get("amount"),
                "moneda": (tender.get("value") or {}).get("currency"),
                "fecha": tender.get("datePublished") or release.get("date"),
                "estado": tender.get("statusDetails") or tender.get("status"),
                "objeto": tender.get("title"),
            }

            rows.append(
                {
                    "ruc": ruc,
                    "razon_social_ruc": ruc_universe.get(ruc, ""),
                    "ocid": ocid,
                    "nivel_registro": base["nivel_registro"],
                    "entidad_ruc": entidad_ruc,
                    "entidad_nombre": buyer.get("name", ""),
                    "objeto": base.get("objeto") or "",
                    "monto": base.get("monto"),
                    "moneda": base.get("moneda") or "",
                    "fecha": base.get("fecha") or "",
                    "estado": base.get("estado") or "",
                    "metodo_contratacion": tender.get("procurementMethodDetails")
                    or tender.get("procurementMethod")
                    or "",
                    "rol_en_proceso": ",".join(roles),
                    "fuente": "OCDS bulk (data.open-contracting.org/en/publication/135)",
                }
            )
            seen_ruc_in_release.add(ruc)

    return rows


def write_output(rows_by_key: dict[tuple[str, str], dict], out_path: Path, fecha_consulta: str) -> None:
    with out_path.open("w", encoding="utf-8", newline="\n") as f:
        f.write("\t".join(FIELDNAMES) + "\n")
        for row in rows_by_key.values():
            row["fecha_consulta"] = fecha_consulta
            values = [str(row.get(col, "")) for col in FIELDNAMES]
            f.write("\t".join(values) + "\n")


def write_ctl_log(ctl_path: Path, years: list[int], n_rucs_consultados: int, n_rucs_devueltos: int, fecha_consulta: str) -> None:
    header = [
        "id_consulta",
        "fuente",
        "tipo_fuente",
        "pestaña_destino",
        "endpoint_metodo",
        "archivo_origen",
        "fecha_consulta",
        "rucs_consultados",
        "rucs_devueltos",
        "notas",
    ]
    row = [
        "7",
        "OECE / Open Contracting Partnership (mirror OCDS)",
        "Directo (bulk, republicado por OCP)",
        "HECHO_CONTRATACION_ESTATAL",
        f"GET data.open-contracting.org/en/publication/135/download?name={{año}}.jsonl.gz — años {years[0]}-{years[-1]}",
        f"oece_contrataciones_por_ruc.py -> {DEFAULT_OUT.name}",
        fecha_consulta,
        str(n_rucs_consultados),
        str(n_rucs_devueltos),
        "El endpoint search?supplier= de contratacionesabiertas.oece.gob.pe ignora el filtro (devuelve 2.75M+ resultados sin filtrar); se uso el bulk anual como via verificada.",
    ]
    is_new = not ctl_path.exists()
    with ctl_path.open("a", encoding="utf-8", newline="\n") as f:
        if is_new:
            f.write("\t".join(header) + "\n")
        f.write("\t".join(row) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--years",
        default="2015-2026",
        help="Año único, rango 'YYYY-YYYY', lista 'YYYY,YYYY' o 'all' (2003-actual). Default: 2015-2026.",
    )
    parser.add_argument("--xlsx", type=Path, default=DEFAULT_XLSX, help="Ruta a BASE CONSOLIDADA.xlsx (para RUC_ID).")
    parser.add_argument("--ruc-file", type=Path, default=None, help="Alternativa: .txt con RUC (y opcionalmente razón social) por línea.")
    parser.add_argument("--cache-dir", type=Path, default=DEFAULT_CACHE_DIR, help="Directorio para los .jsonl.gz descargados.")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="Archivo .txt de salida.")
    parser.add_argument("--ctl-log", type=Path, default=DEFAULT_CTL_LOG, help="Archivo donde anexar la fila para CTL_FUENTE_CONSULTA.")
    parser.add_argument("--keep-cache", action="store_true", default=True, help="No borrar los .jsonl.gz descargados (default: se conservan siempre).")
    args = parser.parse_args()

    years = resolve_years(args.years)
    print(f"Años a procesar: {years[0]}-{years[-1]} ({len(years)} archivo(s))")

    ruc_universe = load_ruc_universe(args.xlsx, args.ruc_file)
    print(f"Universo de RUC a buscar: {len(ruc_universe)}")

    rows_by_key: dict[tuple[str, str], dict] = {}
    rucs_con_match: set[str] = set()

    for year in years:
        gz_path = download_year(year, args.cache_dir)
        if gz_path is None:
            continue

        n_releases = 0
        n_matches_year = 0
        for release in iter_releases(gz_path):
            n_releases += 1
            rows = extract_rows_for_release(release, ruc_universe)
            for row in rows:
                key = (row["ruc"], row["ocid"])
                existing = rows_by_key.get(key)
                if existing is None or (row["fecha"] or "") > (existing["fecha"] or ""):
                    rows_by_key[key] = row
                rucs_con_match.add(row["ruc"])
                n_matches_year += 1
            if n_releases % 200_000 == 0:
                print(f"    [{year}] {n_releases:,} releases procesados, {n_matches_year} coincidencias hasta ahora")

        print(f"  [{year}] listo: {n_releases:,} releases, {n_matches_year} coincidencias")

    fecha_consulta = utcnow_iso()
    write_output(rows_by_key, args.out, fecha_consulta)
    write_ctl_log(args.ctl_log, years, len(ruc_universe), len(rucs_con_match), fecha_consulta)

    print()
    print(f"Filas escritas: {len(rows_by_key)}")
    print(f"RUC con al menos 1 coincidencia: {len(rucs_con_match)} / {len(ruc_universe)}")
    print(f"Salida: {args.out}")
    print(f"Log CTL_FUENTE_CONSULTA (para pegar en la pestaña homónima): {args.ctl_log}")


if __name__ == "__main__":
    main()
