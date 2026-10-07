#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reconstrucción de la serie histórica 2015-2025 del ICRPP con fuentes abiertas y locales.

Mitiga las Limitaciones 1 y 3 del paper ICRPP (vacío de serie histórica 2015-2025 para
ACP/Monte Carlo del Paso 7 OECD/JRC y percentiles 5-95 de la normalización min-max),
usando solo lo que es verificable hoy:

  - 7 datasets abiertos MTC/APN en datosabiertos.gob.pe (2005-2017), descargados con
    cabeceras de navegador (el portal devuelve 418 CloudWAF sin ellas).
  - Cuadros SUNAT de comercio exterior 2023-2024 (appsperu/data/sunat/cdro_*.xlsx).
  - DUA consolidado de café 2024-2026 (fichaduanas-cafe/DUA_CONSOLIDADO.xlsx).
  - Eventos materiales curados del paper ICRPP (decomisos SUNAT/Marina 2024-2025).

NO inventa dato: lo que no existe localmente ni en datos abiertos queda registrado
como GAP con la acción concreta para llenarlo (solicitud Ley 27806, evaluación de
campo PortMATE, re-descarga SEACE/INFOM). No hay documentos institucionales locales
para esas fuentes; por eso el script también genera las plantillas de solicitud.

Salida:
  docs/ICRPP_SERIE_HISTORICA_RECONSTRUIDA.xlsx
    LECTURA | SERIE_LARGA | COBERTURA_2015_2025 | BRECHAS_Y_ACCIONES |
    FUENTES | EVENTOS_MATERIALES | NORMALIZACION_DEMO
  docs/Solicitudes_Ley27806_ICRPP.md
"""

import csv
import hashlib
import re
import sys
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

import openpyxl
import pandas as pd
import requests

try:
    import xlrd
except ImportError:
    xlrd = None

ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = ROOT / "data" / "icrpp" / "apn"
OUT_XLSX = ROOT / "docs" / "ICRPP_SERIE_HISTORICA_RECONSTRUIDA.xlsx"
OUT_SOLICITUDES = ROOT / "docs" / "Solicitudes_Ley27806_ICRPP.md"
SUNAT_DIR = Path(r"C:\Users\acuba\appsperu\data\sunat")
DUA_XLSX = ROOT / "fichaduanas-cafe" / "DUA_CONSOLIDADO.xlsx"
YEARS = list(range(2015, 2026))

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
WAF_HEADERS = {
    "User-Agent": UA,
    "Referer": "https://www.datosabiertos.gob.pe/",
    "Accept": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,*/*",
}

# (archivo, dataset_id_portal, titulo, org)
APN_DATASETS = [
    ("CARGAS_2010_2017.xlsx", "ba073cf0-59c7-4cc4-a212-ef00627594c3",
     "MTC - APN - Movimiento de cargas en puertos a nivel nacional 2010-2017", "MTC/APN"),
    ("NAVES_RECIBIDAS.xlsx", None,
     "MTC - APN - Movimiento de naves recibidas a nivel nacional 2010-2017", "MTC/APN"),
    ("TIPOS_NAVES_2010_2017.xlsx", None,
     "MTC - APN - Movimiento por tipo de naves a nivel nacional 2010-2017", "MTC/APN"),
    ("ACCIDENTES_PUERTO_2014_2017.xlsx", None,
     "MTC - APN - Accidentes en puertos a nivel nacional 2014-2017", "MTC/APN"),
    ("INCIDENTES_PUERTOS_2015_2017.xlsx", None,
     "MTC - APN - Incidentes en puertos a nivel nacional (cubre 2005-2017)", "MTC/APN"),
    ("DERRAMES_PUERTOS_2008_2017.xlsx", None,
     "MTC - APN - Derrames en puertos a nivel nacional 2008-2017", "MTC/APN"),
    ("MERCANCIA_PELIGROSA_0.xlsx", None,
     "MTC - APN - Mercadería peligrosa en el puerto del Callao 2011-2017", "MTC/APN"),
]
APN_BASE = "https://www.datosabiertos.gob.pe/sites/default/files/"

# --- segunda ola: datasets abiertos en CSV/XLS que cubren parte del hueco 2018-2022
CSV_DIR = ROOT / "data" / "icrpp" / "open_csv"
CSV_DATASETS = [
    ("Licencias de prestación de servicios portuarios vigentes 2011-2022.csv",
     "MTC - Licencias de prestación de servicios portuarios vigentes, 2011-2022", "MTC"),
    ("Infraestructura_portuaria_terminales_embarcaderos_2022-2025.csv",
     "MTC - Infraestructura Portuaria – Terminales Portuarios y Embarcaderos 2022 a 2025", "MTC"),
    ("IQ No Fiscalizado - Decomiso.csv",
     "Volumen de Insumos Químicos No Fiscalizados decomisados según departamento (Kg), 2013-2018", "MININTER"),
]
# reportes mensuales de programación diaria de naves 2023 (solo Callao, prefijo DUE CLL)
NAVES_2023_XLS = ["reporte-Febrero2023.xls", "reporte-Marzo2023.xls",
                  "reporte-Abril2023.xls", "reporte-Mayo2023.xls",
                  "reporte-Junio2023.xls"]
# extractos de UN SOLO DIA (no son serie mensual); se registran con esa advertencia
NAVES_2023_CSV = ["DatasetSetiembre2023.csv", "Dataset-Octubre2023.csv",
                  "Dataset-Noviembre2023.csv", "Dataset-Diciembre2023.csv"]
MESES = {"Febrero": 2, "Marzo": 3, "Abril": 4, "Mayo": 5, "Junio": 6,
         "Setiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12}
UBIGEO_DEPTOS = {"01": "AMAZONAS", "02": "ÁNCASH", "03": "APURÍMAC", "04": "AREQUIPA",
                 "05": "AYACUCHO", "06": "CAJAMARCA", "07": "CALLAO", "08": "CUSCO",
                 "09": "HUANCAVELICA", "10": "HUÁNUCO", "11": "ICA", "12": "JUNÍN",
                 "13": "LA LIBERTAD", "14": "LAMBAYEQUE", "15": "LIMA", "16": "LORETO",
                 "17": "MADRE DE DIOS", "18": "MOQUEGUA", "19": "PASCO", "20": "PIURA",
                 "21": "PUNO", "22": "SAN MARTÍN", "23": "TACNA", "24": "TUMBES",
                 "25": "UCAYALI"}
ICRPP_PAPER_SCORES = {"CALLAO": (69.2, "ALTO"), "PAITA": (57.4, "MODERADO-ALTO")}

AGGLOMERADOS = {"TOTAL GENERAL", "TOTAL", "Maritimo", "Fluvial", "Lacustre",
                "Total IP Uso Público", "Total IP Uso Privado", "TOTAL GENERAL "}


# ---------------------------------------------------------------- utilidades
def to_num(v):
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip().replace(",", "")
    if s in ("", "-"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def is_formula(v):
    return isinstance(v, str) and v.startswith("=")


def year_map_from_row(values):
    """{col_idx: anio} para celdas con etiqueta tipo 'Año 2010' / 'AÑO 2014'."""
    out = {}
    for idx, v in enumerate(values):
        if v is None:
            continue
        m = re.match(r"^(?:Año|AÑO)\s*(?:de\s*)?((?:19|20)\d{2})$", str(v).strip())
        if m:
            out[idx] = int(m.group(1))
    return out


def find_header_row(ws, needed, max_row=40):
    """Primera fila con celdas tipo encabezado que cubren todos los tokens
    `needed`: la celda es igual al token o empieza por él (evita que filas
    de título con frases largas tipo '...puertos... Año 2008-2017' matcheen)."""
    for i, row in enumerate(ws.iter_rows(min_row=1, max_row=max_row, values_only=True), start=1):
        cells = [str(c).strip() for c in row if c is not None]
        if all(any(c.lower() == n.lower() or c.lower().startswith(n.lower())
                   for c in cells) for n in needed):
            return i
    return None


def rows_from(ws, first_row):
    for i, row in enumerate(ws.iter_rows(min_row=first_row, values_only=True), start=first_row):
        yield i, list(row)


# ------------------------------------------------------------ parseadores APN
def parse_cargas(path, registros, fuente):
    """Cargas TM por puerto/bahía y terminal, 2010-2017. Jerarquía de filas."""
    global _ctx_puerto
    _ctx_puerto = {}
    wb = openpyxl.load_workbook(path, read_only=True)
    ws = wb["Hoja1"]
    hdr = find_header_row(ws, ["Terminales Portuarios"])
    _, hrow = next(rows_from(ws, hdr))
    ymap = year_map_from_row(hrow)
    col_name = next(i for i, v in enumerate(hrow) if v and "Terminales Portuarios" in str(v))
    col_uso = col_name + 1
    for _, row in rows_from(ws, hdr + 1):
        name = row[col_name] if col_name < len(row) else None
        if name is None or not str(name).strip():
            continue
        name = str(name).strip()
        uso = str(row[col_uso]).strip() if (col_uso < len(row) and row[col_uso]) else ""
        vals = {anio: to_num(row[c]) for c, anio in ymap.items()}
        if not any(v is not None for v in vals.values()):
            continue
        if any(is_formula(row[c]) for c in ymap):
            continue  # agregados calculados; usamos valores publicados por puerto
        if uso in ("Público", "Privado"):
            nivel, puerto, detalle = "terminal", _ctx_puerto.get("actual", ""), name
        elif name in AGGLOMERADOS:
            _ctx_puerto["ambito"] = name
            continue
        else:
            nivel, puerto, detalle = "puerto", name, ""
            _ctx_puerto["actual"] = name
        for anio, valor in vals.items():
            if valor is None:
                continue
            registros.append(dict(dominio="RON", indicador="cargas_tm", ambito=_ctx_puerto.get("ambito", "MARITIMO"),
                                  puerto=puerto, detalle=detalle, nivel=nivel, anio=anio, valor=valor,
                                  unidad="TM", fuente=fuente, estado="ABIERTO"))
    wb.close()


_ctx_puerto = {}


def parse_naves(path, registros, fuente):
    global _ctx_puerto
    _ctx_puerto = {}
    wb = openpyxl.load_workbook(path, read_only=True)
    ws = wb["Hoja1"]
    hdr = find_header_row(ws, ["Ambito", "Año"])
    _, hrow = next(rows_from(ws, hdr))
    ymap = year_map_from_row(hrow)
    col_name = next(i for i, v in enumerate(hrow) if v and "Ambito" in str(v))
    for _, row in rows_from(ws, hdr + 1):
        name = row[col_name] if col_name < len(row) else None
        if name is None or not str(name).strip():
            continue
        name = str(name).strip()
        if any(is_formula(row[c]) for c in ymap):
            if name in ("Maritimo", "Fluvial", "Lacustre"):
                _ctx_puerto["ambito"] = name
            continue
        vals = {anio: to_num(row[c]) for c, anio in ymap.items()}
        if not any(v is not None for v in vals.values()):
            continue
        ambito = "NACIONAL" if name in AGGLOMERADOS else _ctx_puerto.get("ambito", "MARITIMO")
        for anio, valor in vals.items():
            if valor is None:
                continue
            registros.append(dict(dominio="RON", indicador="naves_recibidas", ambito=ambito,
                                  puerto=name, detalle="", nivel="puerto" if name not in AGGLOMERADOS else "total",
                                  anio=anio, valor=valor, unidad="naves", fuente=fuente, estado="ABIERTO"))
    wb.close()


def parse_tipos_naves(path, registros, fuente):
    wb = openpyxl.load_workbook(path, read_only=True)
    for sheet in wb.sheetnames:
        ws = wb[sheet]
        hdr = find_header_row(ws, ["Ambito", "Tipo", "Año"])
        if not hdr:
            continue
        _, hrow = next(rows_from(ws, hdr))
        ymap = year_map_from_row(hrow)
        col_ambito = next((i for i, v in enumerate(hrow) if v and "Ambito" in str(v)), 0)
        col_tipo = next((i for i, v in enumerate(hrow) if v and "Tipo" in str(v)), 1)
        for _, row in rows_from(ws, hdr + 1):
            ambito = str(row[col_ambito]).strip() if col_ambito < len(row) and row[col_ambito] else ""
            tipo = str(row[col_tipo]).strip() if col_tipo < len(row) and row[col_tipo] else ""
            if not tipo:
                continue
            vals = {anio: to_num(row[c]) for c, anio in ymap.items()}
            if not any(v is not None for v in vals.values()):
                continue
            for anio, valor in vals.items():
                if valor is None:
                    continue
                registros.append(dict(dominio="RON", indicador="naves_por_tipo",
                                      ambito=ambito or "NACIONAL", puerto="TODOS", detalle=tipo,
                                      nivel="tipo", anio=anio, valor=valor, unidad="naves",
                                      fuente=fuente, estado="ABIERTO"))
    wb.close()


def parse_seccion_puerto(path, registros, fuente, indicador, dominio, unidad,
                         cols_ctx, drug_filter=None):
    """Archivos con secciones por puerto (cabecera con fórmulas) y detalle con
    valores planos: ACCIDENTES, INCIDENTES. Agrega detalle a puerto por año."""
    wb = openpyxl.load_workbook(path, read_only=True)
    ws = wb["Hoja1"]
    hdr = find_header_row(ws, cols_ctx[:1] + ["AÑO"])
    _, hrow = next(rows_from(ws, hdr))
    ymap = year_map_from_row(hrow)
    col_ctx = [next((i for i, v in enumerate(hrow) if v and k.lower() in str(v).lower()), None) for k in cols_ctx]
    puerto_actual, agregado = None, {}
    for _, row in rows_from(ws, hdr + 1):
        ctx_vals = [str(row[c]).strip() if c is not None and c < len(row) and row[c] else "" for c in col_ctx]
        if any(is_formula(row[c]) for c in ymap if c < len(row)):
            if ctx_vals[0] and ctx_vals[0] not in AGGLOMERADOS:
                puerto_actual = ctx_vals[0]
                agregado.setdefault(puerto_actual, {a: 0.0 for a in ymap.values()})
            continue
        vals = {anio: to_num(row[c]) for c, anio in ymap.items()}
        if not any(v is not None for v in vals.values()):
            continue
        detalle = " | ".join(x for x in ctx_vals if x)
        if drug_filter and drug_filter.lower() not in detalle.lower():
            continue
        for anio, valor in vals.items():
            if valor is None:
                continue
            registros.append(dict(dominio=dominio, indicador=indicador + "_detalle",
                                  ambito="MARITIMO",
                                  puerto=puerto_actual or "SIN_SECCION", detalle=detalle,
                                  nivel="detalle", anio=anio, valor=valor, unidad=unidad,
                                  fuente=fuente, estado="ABIERTO"))
            if puerto_actual:
                agregado.setdefault(puerto_actual, {a: 0.0 for a in ymap.values()})
                agregado[puerto_actual][anio] = agregado[puerto_actual].get(anio, 0.0) + valor
    for puerto, por_anio in agregado.items():
        for anio, valor in por_anio.items():
            registros.append(dict(dominio=dominio, indicador=indicador, ambito="MARITIMO",
                                  puerto=puerto, detalle="", nivel="puerto", anio=anio,
                                  valor=valor, unidad=unidad, fuente=fuente, estado="ABIERTO"))
    wb.close()


def parse_derrames(path, registros, fuente):
    global _ctx_puerto
    _ctx_puerto = {}
    wb = openpyxl.load_workbook(path, read_only=True)
    ws = wb["Hoja1"]
    hdr = find_header_row(ws, ["Puerto", "Año"])
    _, hrow = next(rows_from(ws, hdr))
    ymap = year_map_from_row(hrow)
    col_name = next(i for i, v in enumerate(hrow) if v and "Puerto" in str(v))
    for _, row in rows_from(ws, hdr + 1):
        name = row[col_name] if col_name < len(row) else None
        if name is None or not str(name).strip():
            continue
        name = str(name).strip()
        if any(is_formula(row[c]) for c in ymap) or name in AGGLOMERADOS:
            if name in ("Maritimo", "Fluvial"):
                _ctx_puerto["ambito"] = name
            continue
        vals = {anio: to_num(row[c]) for c, anio in ymap.items()}
        if not any(v is not None for v in vals.values()):
            continue
        for anio, valor in vals.items():
            if valor is None:
                continue
            registros.append(dict(dominio="RON", indicador="derrames_portuarios",
                                  ambito=_ctx_puerto.get("ambito", "MARITIMO"), puerto=name,
                                  detalle="", nivel="puerto", anio=anio, valor=valor,
                                  unidad="eventos", fuente=fuente, estado="ABIERTO"))
    wb.close()


def parse_mercancia_peligrosa(path, registros, fuente):
    wb = openpyxl.load_workbook(path, read_only=True)
    ws = wb["Hoja1"]
    hdr = find_header_row(ws, ["CLASE", "TIPO DE OPERACIÓN", "AÑO"])
    _, hrow = next(rows_from(ws, hdr))
    ymap = year_map_from_row(hrow)
    for _, row in rows_from(ws, hdr + 1):
        clase = str(row[0]).strip() if row[0] else ""
        tipo_op = str(row[1]).strip() if len(row) > 1 and row[1] else ""
        if not clase and not tipo_op:
            continue
        if any(is_formula(row[c]) for c in ymap if c < len(row)):
            continue
        vals = {anio: to_num(row[c]) for c, anio in ymap.items()}
        if not any(v is not None for v in vals.values()):
            continue
        for anio, valor in vals.items():
            if valor is None:
                continue
            registros.append(dict(dominio="RTID", indicador="mercancia_peligrosa_callao",
                                  ambito="MARITIMO", puerto="Callao",
                                  detalle=f"{clase} | {tipo_op}" if clase and tipo_op else (clase or tipo_op),
                                  nivel="detalle", anio=anio, valor=valor, unidad="TM",
                                  fuente=fuente, estado="ABIERTO"))
    wb.close()


# ------------------------------------------------- segunda ola: CSV/XLS abiertos
def parse_licencias(path, registros, fuente):
    """Licencias de servicios portuarios vigentes 2011-2022 (cp1252, ';')."""
    with open(path, encoding="cp1252") as fh:
        rows = list(csv.reader(fh, delimiter=";"))
    tot = {}
    for r in rows[1:]:
        if len(r) < 3 or not r[0].strip():
            continue
        anio, servicio = r[0].strip(), r[1].strip()
        n = to_num(r[2])
        if n is None:
            continue
        registros.append(dict(dominio="RON", indicador="licencias_servicios_portuarios",
                              ambito="NACIONAL", puerto="TODOS", detalle=servicio,
                              nivel="servicio", anio=int(anio), valor=n,
                              unidad="licencias", fuente=fuente, estado="ABIERTO"))
        tot[anio] = tot.get(anio, 0) + n
    for anio, n in sorted(tot.items()):
        registros.append(dict(dominio="RON", indicador="licencias_servicios_portuarios",
                              ambito="NACIONAL", puerto="TODOS", detalle="TOTAL",
                              nivel="total", anio=int(anio), valor=n,
                              unidad="licencias", fuente=fuente, estado="ABIERTO"))


def parse_infraestructura(path, registros, fuente):
    """Inventario MTC de terminales/embarcaderos (cp1252, ';'), snapshot por
    FECHA_CORTE."""
    with open(path, encoding="cp1252") as fh:
        rows = list(csv.reader(fh, delimiter=";"))
    hdr = rows[0]
    ix = {n: i for i, n in enumerate(hdr)}
    cuts = sorted({r[ix["FECHA_CORTE"]] for r in rows[1:] if r and r[ix["FECHA_CORTE"]]})
    for cut in cuts:
        anio = int(cut[:4])
        sub = [r for r in rows[1:] if r and r[ix["FECHA_CORTE"]] == cut]
        grupos = {"total": len(sub), "concesionado": 0, "no concesionado": 0}
        by_ambito, by_dpto = {}, {}
        for r in sub:
            amb = r[ix["AMBITO"]].strip()
            dpto = UBIGEO_DEPTOS.get(r[ix["ID_DEPARTAMENTO"]].strip(),
                                     r[ix["ID_DEPARTAMENTO"]].strip())
            by_ambito[amb] = by_ambito.get(amb, 0) + 1
            by_dpto[dpto] = by_dpto.get(dpto, 0) + 1
            if r[ix["ES_CONCES"]].strip() in ("1", "true", "TRUE"):
                grupos["concesionado"] += 1
            else:
                grupos["no concesionado"] += 1
        for detalle, valor in grupos.items():
            registros.append(dict(dominio="RON", indicador="inventario_terminales_portuarios",
                                  ambito="NACIONAL", puerto="TODOS",
                                  detalle=f"snapshot {cut} | {detalle}", nivel="snapshot",
                                  anio=anio, valor=valor, unidad="instalaciones",
                                  fuente=fuente, estado="ABIERTO"))
        for amb, valor in by_ambito.items():
            registros.append(dict(dominio="RON", indicador="inventario_terminales_portuarios",
                                  ambito=amb.upper(), puerto="TODOS",
                                  detalle=f"snapshot {cut} | ámbito {amb}", nivel="snapshot",
                                  anio=anio, valor=valor, unidad="instalaciones",
                                  fuente=fuente, estado="ABIERTO"))
        for dpto, valor in by_dpto.items():
            registros.append(dict(dominio="RON", indicador="inventario_terminales_portuarios",
                                  ambito="NACIONAL", puerto=dpto,
                                  detalle=f"snapshot {cut}", nivel="snapshot",
                                  anio=anio, valor=valor, unidad="instalaciones",
                                  fuente=fuente, estado="ABIERTO"))


def parse_iq(path, registros, fuente):
    """Decomisos de insumos químicos no fiscalizados por departamento,
    2013-2018 (utf-8-sig, ';')."""
    with open(path, encoding="utf-8-sig") as fh:
        rows = list(csv.reader(fh, delimiter=";"))
    hdr = [h.lstrip("﻿") for h in rows[0]]
    years = [int(c) for c in hdr[1:] if re.match(r"^\d{4}$", c.strip())]
    for r in rows[1:]:
        if not r or not r[0].strip():
            continue
        dpto = r[0].strip()
        for y, c in zip(years, r[1:]):
            v = to_num(c)
            if v is None:
                continue
            registros.append(dict(dominio="RTID", indicador="decomisos_iq_no_fiscalizado",
                                  ambito="NACIONAL", puerto=dpto,
                                  detalle="insumos químicos no fiscalizados (precursores)",
                                  nivel="departamento", anio=y, valor=v, unidad="kg",
                                  fuente=fuente, estado="ABIERTO"))


def parse_naves_2023_xls(path, registros, fuente, mes):
    """Reporte mensual de programación diaria de naves 2023 (XLS, xlrd).
    SOLO Callao: todo DUE tiene prefijo CLL."""
    if xlrd is None:
        return
    wb = xlrd.open_workbook(str(path))
    sh = wb.sheet_by_index(0)
    n, tipos, banderas, conds, motivos = 0, {}, {}, {}, {}
    for i in range(7, sh.nrows):
        due = str(sh.cell_value(i, 2)).strip()
        if "-" not in due:
            continue
        n += 1
        tipo = str(sh.cell_value(i, 17)).strip() or "S/D"
        bandera = str(sh.cell_value(i, 9)).strip() or "S/D"
        cond = str(sh.cell_value(i, 14)).strip() or "S/D"
        motivo = str(sh.cell_value(i, 15)).strip() or "S/D"
        tipos[tipo] = tipos.get(tipo, 0) + 1
        banderas[bandera] = banderas.get(bandera, 0) + 1
        conds[cond] = conds.get(cond, 0) + 1
        motivos[motivo] = motivos.get(motivo, 0) + 1
    if not n:
        return
    registros.append(dict(dominio="RON", indicador="naves_programadas_callao",
                          ambito="MARITIMO", puerto="Callao",
                          detalle=f"{mes} 2023 (5 de 12 meses disponibles; solo Callao)",
                          nivel="mes", anio=2023, valor=float(n), unidad="naves",
                          fuente=fuente, estado="PARCIAL"))
    for tipo, k in tipos.items():
        registros.append(dict(dominio="RON", indicador="naves_programadas_callao",
                              ambito="MARITIMO", puerto="Callao",
                              detalle=f"{mes} 2023 | tipo {tipo}", nivel="detalle",
                              anio=2023, valor=float(k), unidad="naves",
                              fuente=fuente, estado="PARCIAL"))
    for bandera, k in banderas.items():
        registros.append(dict(dominio="RON", indicador="naves_programadas_callao",
                              ambito="MARITIMO", puerto="Callao",
                              detalle=f"{mes} 2023 | bandera {bandera}", nivel="detalle",
                              anio=2023, valor=float(k), unidad="naves",
                              fuente=fuente, estado="PARCIAL"))
    for cond, k in conds.items():
        registros.append(dict(dominio="RLAC", indicador="naves_programadas_callao",
                              ambito="MARITIMO", puerto="Callao",
                              detalle=f"{mes} 2023 | condicion {cond}", nivel="detalle",
                              anio=2023, valor=float(k), unidad="naves",
                              fuente=fuente, estado="PARCIAL"))
    for motivo, k in motivos.items():
        registros.append(dict(dominio="RON", indicador="naves_programadas_callao",
                              ambito="MARITIMO", puerto="Callao",
                              detalle=f"{mes} 2023 | motivo {motivo}", nivel="detalle",
                              anio=2023, valor=float(k), unidad="naves",
                              fuente=fuente, estado="PARCIAL"))


def parse_naves_2023_csv(path, registros, fuente, mes):
    """Extractos CSV de programación diaria 2023: UN SOLO DÍA, no serie."""
    with open(path, encoding="cp1252") as fh:
        rows = list(csv.reader(fh))
    hdr = rows[0]
    ix_fecha, ix_dpto = hdr.index("FECHA_CORTE"), hdr.index("DEPARTAMENTO")
    fechas = sorted({r[ix_fecha] for r in rows[1:] if r and r[ix_fecha]})
    deptos = {}
    for r in rows[1:]:
        if len(r) > ix_dpto:
            deptos[r[ix_dpto]] = deptos.get(r[ix_dpto], 0) + 1
    if not fechas:
        return
    fecha = fechas[0]
    for dpto, k in deptos.items():
        registros.append(dict(dominio="RON", indicador="naves_extracto_diario_2023",
                              ambito="MARITIMO", puerto=dpto.title(),
                              detalle=(f"extracto {fecha} ({mes} 2023); "
                                       "un solo día, NO es serie mensual"),
                              nivel="extracto", anio=2023, valor=float(k),
                              unidad="naves", fuente=fuente, estado="PARCIAL"))
def cdro_sheet(path):
    wb = openpyxl.load_workbook(path, read_only=True)
    return wb, wb[wb.sheetnames[0]]


def parse_sunat_cdro(registros):
    """Cuadros SUNAT 2023-2024: intercambio, importación por aduana, HHI."""
    # cdro_01 — intercambio comercial (totales ACUMULADO por régimen/sector)
    p = SUNAT_DIR / "cdro_01.xlsx"
    if p.exists():
        wb, ws = cdro_sheet(p)
        hdr = find_header_row(ws, ["Régimen"])
        _, grow = next(rows_from(ws, hdr))
        _, subrow = next(rows_from(ws, hdr + 1))
        # atribuye cada columna de año al grupo más cercano a su izquierda
        # (ACUMULADO / VARIACIÓN / ESTRUCTURA) y conserva solo ACUMULADO
        grupo_actual, ymap = None, {}
        grupos = [(i, str(v).strip()) for i, v in enumerate(grow) if v]
        for i, v in enumerate(subrow):
            for gi, gv in grupos:
                if gi <= i:
                    grupo_actual = gv
            if v is not None and re.match(r"^\d{4}$", str(v).strip()) \
                    and grupo_actual and "ACUMULADO" in grupo_actual:
                ymap[i] = int(str(v).strip())
        col_name = next(i for i, v in enumerate(grow) if v and "Régimen" in str(v))
        for _, row in rows_from(ws, hdr + 2):
            name = str(row[col_name]).strip() if col_name < len(row) and row[col_name] else ""
            if not name or name.startswith("CUADRO"):
                continue
            vals = {anio: to_num(row[c]) for c, anio in ymap.items()}
            if not any(v is not None for v in vals.values()):
                continue
            for anio, valor in vals.items():
                if valor is not None:
                    registros.append(dict(dominio="RLAC", indicador="comercio_exterior_nacional",
                                          ambito="NACIONAL", puerto="TODOS", detalle=name,
                                          nivel="regimen", anio=anio, valor=valor, unidad="USD",
                                          fuente="SUNAT/cdro_01", estado="LOCAL"))
        wb.close()

    # cdro_15 — importación CIF por aduana (totales anuales; fila de
    # etiquetas "I Trim..TOTAL" está UNA FILA DEBAJO del encabezado)
    p = SUNAT_DIR / "cdro_15.xlsx"
    if p.exists():
        wb, ws = cdro_sheet(p)
        hdr = find_header_row(ws, ["Aduana", "Periodo"])
        _, lrow = next(rows_from(ws, hdr + 1))
        cols_total = [c for c, v in enumerate(lrow)
                      if v is not None and "TOTAL" in str(v)]
        for _, row in rows_from(ws, hdr + 2):
            name = str(row[2]).strip() if len(row) > 2 and row[2] else ""
            if not name or name == "TOTAL":
                continue
            for c, anio in zip(cols_total, (2023, 2024)):
                valor = to_num(row[c]) if c < len(row) else None
                if valor is not None:
                    registros.append(dict(dominio="RLAC", indicador="importacion_cif_por_aduana",
                                          ambito="NACIONAL", puerto=name, detalle="",
                                          nivel="aduana", anio=anio, valor=valor, unidad="USD",
                                          fuente="SUNAT/cdro_15", estado="LOCAL"))
        wb.close()

    # cdro_08 / cdro_22 — concentración (HHI sobre ranking top-N: cota inferior)
    for fname, ind, col_name_idx, detail_idx in [
        ("cdro_08.xlsx", "concentracion_importadores_hhi", 2, 1),
        ("cdro_22.xlsx", "concentracion_exportadores_hhi", 3, 2),
    ]:
        p = SUNAT_DIR / fname
        if not p.exists():
            continue
        wb, ws = cdro_sheet(p)
        hdr = find_header_row(ws, ["Estructura"])
        _, hrow = next(rows_from(ws, hdr))
        col_share = next(c for c, v in enumerate(hrow) if v is not None and "Estructura" in str(v))
        shares = []
        for _, row in rows_from(ws, hdr + 1):
            name = str(row[col_name_idx]).strip() if len(row) > col_name_idx and row[col_name_idx] else ""
            if (not name or name == "TOTAL" or name.upper() == "RESTO"
                    or str(name).startswith(("Total ", "TOTAL"))):
                continue
            share = to_num(row[col_share]) if col_share < len(row) else None
            if share is not None and share > 0:
                shares.append((name, share))
        if shares:
            sv = [s for _, s in shares]
            if max(sv) <= 1.0:
                hhi = sum(s ** 2 for _, s in shares) * 10000.0
                escala = "fraccion"
            else:
                hhi = sum((s / 100.0) ** 2 for _, s in shares) * 10000.0
                escala = "porcentaje"
            registros.append(dict(dominio="RLAC", indicador=ind, ambito="NACIONAL", puerto="TODOS",
                                  detalle=f"top-{len(shares)} ranking SUNAT ({escala})",
                                  nivel="hhi", anio=2024, valor=round(hhi, 1),
                                  unidad="HHI_0_10000", fuente=f"SUNAT/{fname}",
                                  estado="LOCAL"))
        wb.close()

    # cdro_12 — ranking de despachadores de aduana (CIF + DAMs, 2023-2024)
    p = SUNAT_DIR / "cdro_12.xlsx"
    if p.exists():
        wb, ws = cdro_sheet(p)
        hdr = find_header_row(ws, ["Despachadores de Aduana", "VALOR CIF"])
        for _, row in rows_from(ws, hdr + 2):
            if len(row) < 8 or not row[3]:
                continue
            name = str(row[3]).strip()
            if (not name or name == "TOTAL" or name.upper() == "RESTO"
                    or str(row[1]).strip() in ("TOTAL",)):
                continue
            for c, anio, unidad in [(4, 2023, "USD"), (5, 2024, "USD")]:
                valor = to_num(row[c]) if c < len(row) else None
                if valor is not None:
                    registros.append(dict(dominio="RLAC", indicador="concentracion_despachadores_aduana",
                                          ambito="NACIONAL", puerto="TODOS",
                                          detalle=f"despachador {name}", nivel="empresa",
                                          anio=anio, valor=valor, unidad=unidad,
                                          fuente="SUNAT/cdro_12", estado="LOCAL"))
            for c, anio in [(6, 2023), (7, 2024)]:
                valor = to_num(row[c]) if c < len(row) else None
                if valor is not None:
                    registros.append(dict(dominio="RLAC", indicador="concentracion_despachadores_aduana_dams",
                                          ambito="NACIONAL", puerto="TODOS",
                                          detalle=f"despachador {name}", nivel="empresa",
                                          anio=anio, valor=valor, unidad="DAMs",
                                          fuente="SUNAT/cdro_12", estado="LOCAL"))
        wb.close()

    # cdro_13 — ranking de almacenes y depósitos aduaneros (CIF + DAMs)
    p = SUNAT_DIR / "cdro_13.xlsx"
    if p.exists():
        wb, ws = cdro_sheet(p)
        hdr = find_header_row(ws, ["Almacenes y depósitos", "Valor CIF"])
        for _, row in rows_from(ws, hdr + 2):
            if len(row) < 7 or not row[2]:
                continue
            name = str(row[2]).strip()
            if (not name or name == "TOTAL"
                    or name.upper() == "RESTO"):
                continue
            for c, anio, unidad in [(3, 2023, "USD"), (4, 2024, "USD")]:
                valor = to_num(row[c]) if c < len(row) else None
                if valor is not None:
                    registros.append(dict(dominio="RLAC", indicador="concentracion_almacenes_depositos",
                                          ambito="NACIONAL", puerto="TODOS",
                                          detalle=f"almacen {name}", nivel="empresa",
                                          anio=anio, valor=valor, unidad=unidad,
                                          fuente="SUNAT/cdro_13", estado="LOCAL"))
            for c, anio in [(5, 2023), (6, 2024)]:
                valor = to_num(row[c]) if c < len(row) else None
                if valor is not None:
                    registros.append(dict(dominio="RLAC", indicador="concentracion_almacenes_depositos_dams",
                                          ambito="NACIONAL", puerto="TODOS",
                                          detalle=f"almacen {name}", nivel="empresa",
                                          anio=anio, valor=valor, unidad="DAMs",
                                          fuente="SUNAT/cdro_13", estado="LOCAL"))
        wb.close()

    # cdro_16 — principales subpartidas por aduana (FOB y CIF por
    # subpartida; base para markup FOB->CIF, verificacion RLAC-01)
    p = SUNAT_DIR / "cdro_16.xlsx"
    if p.exists():
        wb, ws = cdro_sheet(p)
        hdr = find_header_row(ws, ["Aduana / Subpartidas", "Valor FOB"])
        aduana = ""
        for _, row in rows_from(ws, hdr + 2):
            if len(row) < 7:
                continue
            c1 = str(row[1]).strip() if row[1] else ""
            if c1.startswith("Total "):
                aduana = c1[6:].strip()
                continue
            if not c1 or c1 == "TOTAL":
                continue
            subpartida = str(row[3]).strip() if len(row) > 3 and row[3] else ""
            desc = str(row[4]).strip() if len(row) > 4 and row[4] else ""
            if not subpartida or not aduana:
                continue
            for c_fob, c_cif, anio in [(5, 7, 2023), (6, 8, 2024)]:
                fob = to_num(row[c_fob]) if c_fob < len(row) else None
                cif = to_num(row[c_cif]) if c_cif < len(row) else None
                if fob is None or cif is None:
                    continue
                registros.append(dict(dominio="RLAC", indicador="subpartida_aduana_fob_cif",
                                      ambito="NACIONAL", puerto=aduana,
                                      detalle=f"subpartida {subpartida} | {desc[:60]}",
                                      nivel="subpartida", anio=anio,
                                      valor=round(cif, 2), unidad="USD_CIF",
                                      fuente="SUNAT/cdro_16", estado="LOCAL"))
                registros.append(dict(dominio="RLAC", indicador="subpartida_aduana_fob_cif",
                                      ambito="NACIONAL", puerto=aduana,
                                      detalle=f"subpartida {subpartida} | {desc[:60]}",
                                      nivel="subpartida", anio=anio,
                                      valor=round(fob, 2), unidad="USD_FOB",
                                      fuente="SUNAT/cdro_16", estado="LOCAL"))
        wb.close()


# ------------------------------------------------------------- DUAs locales
def parse_duas(registros):
    if not DUA_XLSX.exists():
        return
    wb = openpyxl.load_workbook(DUA_XLSX, read_only=True)

    # mapeo aduana
    cat = {}
    ws = wb["CAT_ADUANAS"]
    rows = list(ws.iter_rows(values_only=True))
    for r in rows[1:]:
        if r and r[0]:
            cat[str(r[0]).strip()] = str(r[1]).strip() if r[1] else ""

    # DUAS: FOB/peso por año y aduana
    ws = wb["DUAS"]
    rows = ws.iter_rows(values_only=True)
    header = [str(c).strip() if c is not None else "" for c in next(rows)]
    ix = {n: header.index(n) for n in header if n}
    agg = {}
    for r in rows:
        if not r or r[ix.get("anio", -1)] is None:
            continue
        anio = str(r[ix["anio"]]).strip()
        aduana = cat.get(str(r[ix["aduana"]]).strip(), str(r[ix["aduana"]]).strip())
        fob = to_num(r[ix["valor_neto_fob"]]) if "valor_neto_fob" in ix else None
        peso = to_num(r[ix["total_peso_neto"]]) if "total_peso_neto" in ix else None
        if fob is None:
            continue
        key = (anio, aduana)
        a = agg.setdefault(key, dict(fob=0.0, peso=0.0, n=0))
        a["fob"] += fob
        a["peso"] += peso or 0.0
        a["n"] += 1
    for (anio, aduana), a in agg.items():
        registros.append(dict(dominio="RLAC", indicador="exportacion_fob_duas_cafe",
                              ambito="MARITIMO" if aduana != "AEREA Y POSTAL EX-IAAC" else "AEREO",
                              puerto=aduana, detalle="universo 25 cooperativas (café)",
                              nivel="aduana", anio=int(anio), valor=round(a["fob"], 2),
                              unidad="USD", fuente="DUA_CONSOLIDADO/DUAS", estado="LOCAL"))
        registros.append(dict(dominio="RLAC", indicador="peso_neto_duas_cafe",
                              ambito="MARITIMO" if aduana != "AEREA Y POSTAL EX-IAAC" else "AEREO",
                              puerto=aduana, detalle="universo 25 cooperativas (café)",
                              nivel="aduana", anio=int(anio), valor=round(a["peso"], 2),
                              unidad="kg", fuente="DUA_CONSOLIDADO/DUAS", estado="LOCAL"))
        registros.append(dict(dominio="RLAC", indicador="n_duas_cafe",
                              ambito="MARITIMO" if aduana != "AEREA Y POSTAL EX-IAAC" else "AEREO",
                              puerto=aduana, detalle="universo 25 cooperativas (café)",
                              nivel="aduana", anio=int(anio), valor=float(a["n"]),
                              unidad="DUAs", fuente="DUA_CONSOLIDADO/DUAS", estado="LOCAL"))

    # SERIES_ICO: cobertura de series ICO por año
    ws = wb["SERIES_ICO"]
    rows = ws.iter_rows(values_only=True)
    header = [str(c).strip() if c is not None else "" for c in next(rows)]
    ix_anios = header.index("anios") if "anios" in header else None
    conteo = {}
    if ix_anios is not None:
        for r in rows:
            if not r or len(r) <= ix_anios or not r[ix_anios]:
                continue
            for y in re.findall(r"20\d{2}", str(r[ix_anios])):
                conteo[y] = conteo.get(y, 0) + 1
        for anio, n in conteo.items():
            registros.append(dict(dominio="RLAC", indicador="n_series_ico",
                                  ambito="NACIONAL", puerto="TODOS",
                                  detalle="series ICO de operaciones/lotes", nivel="conteo",
                                  anio=int(anio), valor=float(n), unidad="series",
                                  fuente="DUA_CONSOLIDADO/SERIES_ICO", estado="LOCAL"))
    wb.close()


# ------------------------------------------------------- eventos materiales
EVENTOS_MATERIALES = [
    dict(fecha="2024-08-01", puerto="NACIONAL", kg=18000.0,
         descripcion="Operativo nacional (desglose no publicado por puerto)",
         fuente="ICRPP paper, Tabla decomisos (ago. 2024)"),
    dict(fecha="2024-09-01", puerto="Jorge Chávez + Callao + Paita", kg=3323.0,
         descripcion="Intercepción SUNAT 1-set-2024; valor estimado de mercado > US$104 M",
         fuente="ICRPP paper, Introducción (SUNAT 2024)"),
    dict(fecha="2025-07-03", puerto="Callao", kg=1453.0,
         descripcion="Operativo conjunto SUNAT/Marina; contenedores contaminados — arroz",
         fuente="ICRPP paper, Tabla decomisos (3 jul. 2025)"),
    dict(fecha="2025-12-01", puerto="Paita", kg=3407.0,
         descripcion="Operativo 'Perú Seguro'; contenedores de arroz",
         fuente="ICRPP paper, Tabla decomisos (dic. 2025)"),
    dict(fecha="2025-12-31", puerto="NACIONAL", kg=21222.0,
         descripcion="Total droga intervenida SUNAT 2025 (Memoria Anual 2025)",
         fuente="ICRPP paper, Tabla decomisos (total 2025)"),
]


# --------------------------------------------------------------- descarga APN
def descargar_apn(fuentes_meta):
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    for fname, dataset_id, titulo, org in APN_DATASETS:
        dest = CACHE_DIR / fname
        url = APN_BASE + fname
        meta = dict(archivo=fname, url=url, dataset_id=dataset_id or "", titulo=titulo,
                    organizacion=org, bytes=0, sha256="", descargado_en="", estado="")
        if dest.exists():
            meta["estado"] = "CACHE"
        else:
            try:
                r = requests.get(url, headers=WAF_HEADERS, timeout=90)
                r.raise_for_status()
                dest.write_bytes(r.content)
                meta["estado"] = "DESCARGADO"
            except Exception as e:
                meta["estado"] = f"ERROR: {type(e).__name__}: {e}"
                fuentes_meta.append(meta)
                continue
        meta["bytes"] = dest.stat().st_size
        meta["sha256"] = hashlib.sha256(dest.read_bytes()).hexdigest()
        meta["descargado_en"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        fuentes_meta.append(meta)


def descargar_open_csv(fuentes_meta):
    """Segunda ola: CSVs/XLS abiertos (licencias, infraestructura, IQ, naves 2023)."""
    if xlrd is None:
        print("ADVERTENCIA: xlrd no disponible; los reportes .xls de naves 2023 "
              "no se procesarán. Instalar con: pip install xlrd")
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    todo = ([(f, t, o) for f, t, o in CSV_DATASETS]
            + [(f, "APN - Programación diaria de naves 2023 (mensual, Callao)", "APN")
               for f in NAVES_2023_XLS]
            + [(f, "APN - Extracto de programación diaria de naves 2023 (un día)", "APN")
               for f in NAVES_2023_CSV])
    for fname, titulo, org in todo:
        dest = CSV_DIR / fname
        url = APN_BASE + urllib.parse.quote(fname)
        meta = dict(archivo=fname, url=url, dataset_id="", titulo=titulo,
                    organizacion=org, bytes=0, sha256="", descargado_en="", estado="")
        if dest.exists():
            meta["estado"] = "CACHE"
        else:
            try:
                r = requests.get(url, headers=WAF_HEADERS, timeout=90)
                r.raise_for_status()
                dest.write_bytes(r.content)
                meta["estado"] = "DESCARGADO"
            except Exception as e:
                meta["estado"] = f"ERROR: {type(e).__name__}: {e}"
                fuentes_meta.append(meta)
                continue
        meta["bytes"] = dest.stat().st_size
        meta["sha256"] = hashlib.sha256(dest.read_bytes()).hexdigest()
        meta["descargado_en"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        fuentes_meta.append(meta)


# ------------------------------------------------------------------ cobertur
def build_cobertura(registros):
    """Matriz indicador x año (2015-2025) con el mejor estado disponible."""
    rank = {"ABIERTO": 4, "PARCIAL": 3, "LOCAL": 2, "CURADO": 1}
    celdas = {}
    puertos = {}
    for r in registros:
        if r["anio"] not in YEARS:
            continue
        key = r["indicador"]
        celdas.setdefault(key, {})
        if rank.get(r["estado"], 0) >= rank.get(celdas[key].get(r["anio"], ""), 0):
            celdas[key][r["anio"]] = r["estado"]
        if r["puerto"] and r["puerto"] not in ("TODOS", ""):
            puertos.setdefault(key, set()).add(r["puerto"])
    orden = ["cargas_tm", "naves_recibidas", "naves_por_tipo", "accidentes_portuarios",
             "incidentes_portuarios", "incidentes_droga_portuarios", "derrames_portuarios",
              "mercancia_peligrosa_callao", "comercio_exterior_nacional",
             "importacion_cif_por_aduana", "concentracion_importadores_hhi",
             "concentracion_exportadores_hhi", "exportacion_fob_duas_cafe",
             "peso_neto_duas_cafe", "n_duas_cafe", "n_series_ico",
             "decomisos_eventos", "licencias_servicios_portuarios",
             "inventario_terminales_portuarios", "decomisos_iq_no_fiscalizado",
             "naves_programadas_callao", "naves_extracto_diario_2023"]
    filas = []
    for ind in orden:
        if ind not in celdas:
            continue
        fila = dict(indicador=ind, **{str(y): celdas[ind].get(y, "") for y in YEARS})
        ps = sorted(puertos.get(ind, set()))
        fila["puertos_cubiertos"] = ", ".join(ps[:8]) + ("…" if len(ps) > 8 else "")
        filas.append(fila)
    return pd.DataFrame(filas)


ACCIONES = {
    "cargas_tm": "Solicitar a APN (Ley 27806) el Anuario Estadístico Portuario 2018-2025. No hay documento institucional local; el portal datosabiertos solo publica 2010-2017. Verificar también apn.gob.pe por anuarios recientes.",
    "naves_recibidas": "Solicitar a APN (Ley 27806) movimiento de naves 2018-2025. Para 2023 existen reportes mensuales de programación diaria en datosabiertos (no agregados; requiere procesamiento aparte).",
    "naves_por_tipo": "Solicitar a APN (Ley 27806) movimiento por tipo de nave 2018-2025.",
    "accidentes_portuarios": "Solicitar a APN/MTC (Ley 27806) registro de accidentes portuarios 2018-2025.",
    "incidentes_portuarios": "Solicitar a APN/MTC (Ley 27806) registro de incidentes portuarios 2018-2025.",
    "incidentes_droga_portuarios": "Solicitar a APN/MTC (Ley 27806) incidentes tipo 'Droga' 2018-2025 y cruzar con DIRANDRO (ver decomisos).",
    "derrames_portuarios": "Solicitar a APN/MTC (Ley 27806) registro de derrames portuarios 2018-2025.",
    "mercancia_peligrosa_callao": "Solicitar a APN (Ley 27806) movimiento de mercancía peligrosa 2018-2025 (Callao y otros puertos).",
    "comercio_exterior_nacional": "Solicitar a SUNAT (Ley 27806) cuadros de comercio exterior 2015-2022; alternativa: recompilar de memorias anuales SUNAT o bases comerciales (TradeMap).",
    "importacion_cif_por_aduana": "Solicitar a SUNAT (Ley 27806) importación CIF por aduana 2015-2022.",
    "concentracion_importadores_hhi": "Solicitar a SUNAT (Ley 27806) ranking de importadores 2015-2022 para HHI histórico; el cdro actual solo cubre 2023-2024.",
    "concentracion_exportadores_hhi": "Solicitar a SUNAT (Ley 27806) ranking de exportadores tradicionales 2015-2022.",
    "exportacion_fob_duas_cafe": "Extender universo de DUAs más allá de las 25 cooperativas (SUNAT Aduanas, Ley 27806) para series 2015-2023 por aduana.",
    "peso_neto_duas_cafe": "Ídem exportacion_fob_duas_cafe.",
    "n_duas_cafe": "Ídem exportacion_fob_duas_cafe.",
    "n_series_ico": "Ídem exportacion_fob_duas_cafe.",
    "decomisos_eventos": "Solicitar a DIRANDRO/MININTER (Ley 27806) estadísticas de decomisos de drogas desagregadas por puerto y año 2015-2025. No hay documento institucional local; los eventos 2024-2025 son puntuales y no sustituyen una serie.",
    "licencias_servicios_portuarios": "Cubierto 2011-2022 por datos abiertos MTC. Para 2023-2025: solicitar a MTC (Ley 27806) o verificar reposición en el portal.",
    "inventario_terminales_portuarios": "Snapshot MTC al 2022-12-31 (título dice 2022-2025 pero solo hay un corte). Para cortes 2023-2025: solicitar a MTC (Ley 27806).",
    "decomisos_iq_no_fiscalizado": "Cubierto 2013-2018 (MININTER, datos abiertos). Para 2019-2025: solicitar a DIRANDRO/MININTER (Ley 27806).",
    "naves_programadas_callao": "Procesado en Scripts/icrpp_naves_2023_callao.py -> docs/NAVES_2023_CALLAO_ANALISIS.xlsx (solo Callao, Feb-Jun 2023; condicion TRAMPA/LINEA, motivo, procedencia, estadía, DUE). Para el resto de meses y puertos: solicitar a APN (Ley 27806); Enero/Julio/Agosto 2023 no existen en el portal (404).",
    "naves_extracto_diario_2023": "Los extractos CSV de Set-Dic 2023 son de UN SOLO DÍA cada uno; no sustituyen una serie mensual. Solicitar a APN (Ley 27806) los reportes mensuales completos.",
    "portmate": "Evaluación de campo PortMATE (PNUD/WCS) en Callao y Paita — dato primario no publicable; requiere trabajo de campo (Limitación 2 del paper).",
    "seace_infobras": "Re-descargar contratación pública portuaria de SEACE/OCSE y obras públicas de INFOM; el paper ICRPP lo calculó en vivo pero no hay dataset local en eudrperu.",
    "decomisos_serie": "Solicitar a DIRANDRO/MININTER (Ley 27806) estadísticas de decomisos de drogas desagregadas por puerto y año 2015-2025. No hay documento institucional local; los eventos 2024-2025 son puntuales y no sustituyen una serie.",
}


def build_brechas(cobertura):
    filas = []
    for _, fila in cobertura.iterrows():
        ind = fila["indicador"]
        for y in YEARS:
            if not fila[str(y)]:
                filas.append(dict(indicador=ind, anio=y,
                                  accion=ACCIONES.get(ind, "Identificar fuente.")))
    # gaps transversales que no son series de indicador
    filas.append(dict(indicador="portmate_rvi01", anio="2015-2025", accion=ACCIONES["portmate"]))
    filas.append(dict(indicador="seace_infobras_rrc", anio="2015-2025", accion=ACCIONES["seace_infobras"]))
    filas.append(dict(indicador="decomisos_droga_serie", anio="2015-2023", accion=ACCIONES["decomisos_serie"]))
    return pd.DataFrame(filas)


def build_normalizacion(registros):
    """Percentiles sobre la ventana histórica disponible (mitigación parcial de la
    Limitación 3 del paper). Solo puertos con >=3 años de dato."""
    df = pd.DataFrame([r for r in registros if r["nivel"] == "puerto"
                       and r["indicador"] in ("cargas_tm", "naves_recibidas",
                                              "accidentes_portuarios", "incidentes_portuarios",
                                              "derrames_portuarios")])
    filas = []
    if not df.empty:
        for (ind, puerto), g in df.groupby(["indicador", "puerto"]):
            if g["anio"].nunique() < 3:
                continue
            s = g.groupby("anio")["valor"].sum()
            filas.append(dict(indicador=ind, puerto=puerto, anios=int(s.size),
                              ventana=f"{int(s.index.min())}-{int(s.index.max())}",
                              min=round(s.min(), 2), p5=round(s.quantile(0.05), 2),
                              p50=round(s.quantile(0.50), 2), p95=round(s.quantile(0.95), 2),
                              max=round(s.max(), 2),
                              advertencia=("Serie corta (ventana %d-%d): percentiles 5-95 sesgados; "
                                           "Limitación 3 del paper se mitiga solo parcialmente."
                                           % (int(s.index.min()), int(s.index.max())))))
    return pd.DataFrame(filas)


# -------------------------------------------------------------- solicitudes
PLANTILLAS = [
    ("SUPERINTENDENCIA NACIONAL DE ADUANAS Y DE ADMINISTRACIÓN TRIBUTARIA (SUNAT)",
     "Cuadros de comercio exterior 2015-2022: importación CIF y exportación FOB por aduana "
     "(MARITIMA DEL CALLAO, PAITA y demás), por subpartida arancelaria y ranking de "
     "importadores/exportadores, en formato XLSX/CSV.",
     "Serie histórica de concentración (HHI) y markup FOB/CIF del dominio RLAC del ICRPP."),
    ("AUTORIDAD PORTUARIA NACIONAL (APN)",
     "Anuario Estadístico Portuario 2018-2025: movimiento de cargas (TM) por terminal y puerto, "
     "naves recibidas, accidentes, incidentes, derrames y mercancía peligrosa, con la misma "
     "estructura de los cuadros 2005-2017 publicados en datosabiertos.gob.pe, en XLSX.",
     "Serie histórica de tráfico y seguridad portuaria del dominio RON del ICRPP."),
    ("DIRECCIÓN GENERAL DE CAPITANÍAS Y GUARDACOSTAS (DIMAR) — MARINA DE GUERRA DEL PERÚ",
     "Registro de incidentes y siniestros náuticos en terminales portuarios 2015-2025 "
     "(tipo, fecha, puerto, consecuencias), en formato tabular.",
     "Componente de riesgo operacional-náutico (RON) del ICRPP."),
    ("DIRECCIÓN ANTIDROGAS (DIRANDRO) — MINISTERIO DEL INTERIOR",
     "Estadísticas de decomisos de drogas desagregadas por puerto y año 2015-2025 "
     "(kg por tipo de sustancia, puerto, operación), en formato tabular.",
     "Serie del dominio RTID del ICRPP; los eventos 2024-2025 son puntuales y no "
     "sustituyen una serie estadística."),
]


def generar_solicitudes(brechas):
    n_gaps = len(brechas)
    lines = [
        "# Solicitudes de acceso a información (Ley 27806) — serie histórica ICRPP",
        "",
        f"Generado por `Scripts/icrpp_serie_historica.py` el "
        f"{datetime.now(timezone.utc).isoformat(timespec='seconds')}.",
        "",
        f"Contexto: la reconstrucción con fuentes abiertas y locales cubrió "
        f"{len(brechas)} celdas de brecha en la matriz 2015-2025. **No existen documentos "
        "institucionales locales** para estas fuentes; las plantillas de abajo son el mitigante "
        "formal. La Ley 27806 no exige motivación del solicitante; plazo de respuesta: "
        "10 días hábiles (art. 19).",
        "",
    ]
    for i, (inst, datos, uso) in enumerate(PLANTILLAS, start=1):
        lines += [
            f"## {i}. {inst}",
            "",
            "**Fundamento:** Ley 27806, Ley de Transparencia y Acceso a la Información Pública "
            "(art. 2: toda persona tiene derecho a solicitar información pública).",
            "",
            "**Datos solicitados:**",
            "",
            datos,
            "",
            "**Uso:** investigación independiente — Índice Compuesto de Riesgo Portuario "
            f"Peruano (ICRPP). {uso}",
            "",
            "**Formato solicitado:** archivo electrónico (XLSX/CSV) con estructura de campos "
            "explícita, o indicación del portal de datos abiertos donde ya se publique.",
            "",
            "---",
            "",
        ]
    lines += [
        "## Registro de brechas por indicador/año",
        "",
        f"{n_gaps} celdas pendientes (ver `BRECHAS_Y_ACCIONES` en "
        "`docs/ICRPP_SERIE_HISTORICA_RECONSTRUIDA.xlsx`).",
        "",
        "| Indicador | Año(s) | Acción |",
        "|---|---|---|",
    ]
    for _, b in brechas.iterrows():
        lines.append(f"| {b['indicador']} | {b['anio']} | {b['accion']} |")
    OUT_SOLICITUDES.write_text("\n".join(lines), encoding="utf-8")


# ------------------------------------------------- exposicion cooperativas (opc. 7)
def build_exposicion_cooperativas(registros):
    """Cruza las organizaciones exportadoras del DUA consolidado (15 con
    DUAs) con el riesgo portuario de su aduana dominante por FOB.

    El ICRPP compuesto del paper solo existe para Callao (69.2, ALTO) y
    Paita (57.4, MODERADO-ALTO); para el resto de aduanas no hay score
    compuesto y se reporta 'S/D' en lugar de inventar un numero."""
    if not DUA_XLSX.exists():
        return pd.DataFrame(), pd.DataFrame()
    wb = openpyxl.load_workbook(DUA_XLSX, read_only=True)

    cat = {}
    for r in list(wb["CAT_ADUANAS"].iter_rows(values_only=True))[1:]:
        if r and r[0]:
            cat[str(r[0]).strip()] = str(r[1]).strip() if r[1] else ""

    ws = wb["DUAS"]
    rows = ws.iter_rows(values_only=True)
    header = [str(c).strip() if c is not None else "" for c in next(rows)]
    ix = {n: header.index(n) for n in header if n}
    agg = {}
    for r in rows:
        if not r or r[ix.get("anio", -1)] is None:
            continue
        ruc = str(r[ix["ruc"]]).strip()
        razon = str(r[ix["razon_social"]]).strip()
        aduana = cat.get(str(r[ix["aduana"]]).strip(), str(r[ix["aduana"]]).strip())
        fob = to_num(r[ix["valor_neto_fob"]]) if "valor_neto_fob" in ix else None
        if fob is None:
            continue
        a = agg.setdefault(ruc, dict(razon=razon, fob=0.0, n=0, por_aduana={}))
        a["fob"] += fob
        a["n"] += 1
        a["por_aduana"][aduana] = a["por_aduana"].get(aduana, 0.0) + fob

    # stats por puerto desde la serie reconstruida (nivel puerto)
    df = pd.DataFrame([r for r in registros if r["nivel"] == "puerto"])
    def stat(indicador, puerto, modo, anios=None):
        g = df[(df["indicador"] == indicador) & (df["puerto"].str.upper() == puerto)]
        if anios:
            g = g[g["anio"].between(anios[0], anios[1])]
        if g.empty:
            return None
        s = g.groupby("anio")["valor"].sum()
        if modo == "prom":
            return round(float(s.mean()), 2)
        return round(float(s.sum()), 2)

    filas, metodo = [], []
    for ruc, a in sorted(agg.items(), key=lambda kv: -kv[1]["fob"]):
        dominante = max(a["por_aduana"], key=a["por_aduana"].get)
        pct = round(100.0 * a["por_aduana"][dominante] / a["fob"], 1)
        score, nivel = ICRPP_PAPER_SCORES.get(dominante.upper(), (None, "S/D"))
        if dominante.upper() in ICRPP_PAPER_SCORES:
            cargas = stat("cargas_tm", dominante, "prom", (2015, 2017))
            naves = stat("naves_recibidas", dominante, "prom", (2015, 2017))
            incid = stat("incidentes_portuarios", dominante, "sum", (2005, 2017))
            derrames = stat("derrames_portuarios", dominante, "sum", (2008, 2017))
        else:
            cargas = naves = incid = derrames = None
        filas.append(dict(
            ruc=ruc, razon_social=a["razon"], fob_total_usd=round(a["fob"], 2),
            n_duas=a["n"], aduana_dominante=dominante,
            pct_fob_en_aduana_dominante=pct,
            icrpp_paper=score if score is not None else "S/D",
            nivel_riesgo_paper=nivel,
            cargas_tm_prom_2015_2017=cargas,
            naves_recibidas_prom_2015_2017=naves,
            incidentes_portuarios_2005_2017=incid,
            derrames_portuarios_2008_2017=derrames,
            cobertura_serie_puerto="2015-2017 ABIERTO (APN); 2018-2022 GAP; 2023+ PARCIAL/LIMITADO"))
    metodo = [
        ("Qué es", "Exposición al riesgo portuario de cada organización "
                      "exportadora del DUA consolidado (15 con DUAs; el universo "
                      "mayor del proyecto son 51 cooperativas), por su aduana "
                      "dominante en FOB."),
        ("Aduna dominante", "La aduana con mayor FOB acumulado de la cooperativa en el "
                              "DUA consolidado 2024-2026."),
        ("ICRPP paper", "Score compuesto publicado en el paper ICRPP (vigencia 2024-2025): "
                          "Callao 69.2 ALTO, Paita 57.4 MODERADO-ALTO. Solo existe para "
                          "esos dos puertos; el resto se marca S/D (no se inventa)."),
        ("Stats RON", "Promedios 2015-2017 (cargas TM, naves) y sumas "
                        "2005-2017 (incidentes) / 2008-2017 (derrames) de la "
                        "serie reconstruida con datos abiertos APN."),
        ("Advertencia", "El ICRPP compuesto de otros puertos (Matarani, Pisco, etc.) "
                          "aún no existe; el score del paper es de 2024-2025 y la serie "
                          "abierta cubre hasta 2017. La exposición es un insumo de "
                          "trazabilidad, no una calificación de cumplimiento EUDR."),
    ]
    return pd.DataFrame(filas), pd.DataFrame(metodo, columns=["item", "detalle"])


# --------------------------------------------------------------------- main
def main():
    registros, fuentes_meta = [], []
    descargar_apn(fuentes_meta)
    descargar_open_csv(fuentes_meta)

    for fname, _, titulo, _ in APN_DATASETS:
        path = CACHE_DIR / fname
        if not path.exists():
            continue
        fuente = f"MTC-APN/datosabiertos ({fname})"
        if fname == "CARGAS_2010_2017.xlsx":
            parse_cargas(path, registros, fuente)
        elif fname == "NAVES_RECIBIDAS.xlsx":
            parse_naves(path, registros, fuente)
        elif fname == "TIPOS_NAVES_2010_2017.xlsx":
            parse_tipos_naves(path, registros, fuente)
        elif fname == "ACCIDENTES_PUERTO_2014_2017.xlsx":
            parse_seccion_puerto(path, registros, fuente, "accidentes_portuarios",
                                 "RON", "eventos", ["PUERTO", "TIPO", "ESTADO"])
        elif fname == "INCIDENTES_PUERTOS_2015_2017.xlsx":
            parse_seccion_puerto(path, registros, fuente, "incidentes_portuarios",
                                 "RON", "eventos", ["PUERTO", "TIPO", "HALLAZGO"])
            parse_seccion_puerto(path, registros, fuente, "incidentes_droga_portuarios",
                                 "RTID", "eventos", ["PUERTO", "TIPO", "HALLAZGO"],
                                 drug_filter="Droga")
        elif fname == "DERRAMES_PUERTOS_2008_2017.xlsx":
            parse_derrames(path, registros, fuente)
        elif fname == "MERCANCIA_PELIGROSA_0.xlsx":
            parse_mercancia_peligrosa(path, registros, fuente)

    # segunda ola (CSV/XLS abiertos)
    for fname, _, _ in CSV_DATASETS:
        path = CSV_DIR / fname
        if not path.exists():
            continue
        fuente = f"MTC/datosabiertos ({fname})" if "Licencias" in fname or "Infraestructura" in fname else f"MININTER/datosabiertos ({fname})"
        if "Licencias" in fname:
            parse_licencias(path, registros, fuente)
        elif "Infraestructura" in fname:
            parse_infraestructura(path, registros, fuente)
        elif "IQ" in fname:
            parse_iq(path, registros, fuente)
    for fname in NAVES_2023_XLS:
        path = CSV_DIR / fname
        if not path.exists():
            continue
        mes = next((m for m in MESES if m in fname), "")
        parse_naves_2023_xls(path, registros, f"APN/datosabiertos ({fname})", mes)
    for fname in NAVES_2023_CSV:
        path = CSV_DIR / fname
        if not path.exists():
            continue
        mes = next((m for m in MESES if m in fname), "")
        parse_naves_2023_csv(path, registros, f"APN/datosabiertos ({fname})", mes)

    parse_sunat_cdro(registros)
    parse_duas(registros)

    for ev in EVENTOS_MATERIALES:
        registros.append(dict(dominio="RTID", indicador="decomisos_eventos",
                              ambito="MARITIMO", puerto=ev["puerto"],
                              detalle=ev["descripcion"], nivel="evento",
                              anio=int(ev["fecha"][:4]), valor=ev["kg"], unidad="kg",
                              fuente=ev["fuente"], estado="CURADO"))

    df_serie = pd.DataFrame(registros)
    cobertura = build_cobertura(registros)
    brechas = build_brechas(cobertura)
    normalizacion = build_normalizacion(registros)
    df_fuentes = pd.DataFrame(fuentes_meta)
    df_eventos = pd.DataFrame(EVENTOS_MATERIALES)
    df_exposicion, df_expo_metodo = build_exposicion_cooperativas(registros)

    # hoja de lectura
    resumen = df_serie.groupby("estado").size().to_dict()
    anios_cubiertos = sorted({int(a) for a in df_serie["anio"].unique() if pd.notna(a)})
    lectura = pd.DataFrame([
        ("Propósito", "Reconstrucción de la serie histórica 2015-2025 del ICRPP con fuentes "
                      "abiertas y locales; mitiga Limitaciones 1 y 3 del paper."),
        ("Método", "Descarga de 7 datasets MTC/APN 2005-2017 + segunda ola abierta "
                   "(licencias 2011-2022, inventario MTC 2022, IQ decomisos 2013-2018, "
                   "naves Callao 2023), con cabeceras de navegador contra CloudWAF; "
                   "parseo jerárquico (agregados con fórmulas se recalculan desde el "
                   "detalle cuando aplica), integración de cuadros SUNAT 2023-2024 y "
                   "DUAs de café 2024-2026, y eventos curados del paper."),
        ("Estados", "ABIERTO=descargado de datosabiertos.gob.pe; PARCIAL=abierto pero "
                    "incompleto (meses/días parciales o un solo puerto); "
                    "LOCAL=archivo del proyecto; CURADO=curado del paper ICRPP; "
                    "''=sin dato (GAP)."),
        ("Cobertura de años", f"{anios_cubiertos[0]}-{anios_cubiertos[-1]} (no contiguo); "
                              f"registros: {len(df_serie)}"),
        ("Estados (conteo)", str(resumen)),
        ("GAPS 2015-2025", f"{len(brechas)} celdas — ver BRECHAS_Y_ACCIONES y "
                           "Solicitudes_Ley27806_ICRPP.md"),
        ("Hueco 2018-2022", "Parcialmente cubierto por licencias portuarias (conteo "
                              "anual) e inventario MTC (snapshot 2022-12-31); el tráfico "
                              "portuario (cargas/naves) 2018-2022 sigue sin fuente "
                              "abierta: requiere solicitud a APN."),
        ("Advertencia 1", "Los rankings SUNAT son top-N: el HHI es una cota inferior."),
        ("Advertencia 2", "Las DUAs cubren solo las 15 organizaciones del DUA "
                          "consolidado (universo mayor del proyecto: 51 "
                          "cooperativas); no representan el tráfico total de las "
                          "aduanas."),
        ("Advertencia 3", "Los percentiles 5-95 de NORMALIZACION_DEMO usan ventanas cortas "
                          "(2005-2017); mitigan solo parcialmente la Limitación 3."),
        ("Advertencia 4", "Los eventos de decomiso son puntuales (2024-2025); no son serie "
                          "estadística. La serie 2015-2025 requiere la solicitud a DIRANDRO."),
        ("Advertencia 5", "Los reportes de naves 2023 son solo de Callao y 5 de 12 meses "
                          "(Feb-Jun); los extractos CSV de Set-Dic son de UN SOLO DÍA cada "
                          "uno. Enero/Julio/Agosto 2023 no existen en el portal (404)."),
        ("Advertencia 6", "El inventario MTC 2022-2025 tiene un solo corte real "
                          "(2022-12-31) pese al título; no es serie anual."),
    ], columns=["item", "detalle"])

    with pd.ExcelWriter(OUT_XLSX, engine="openpyxl") as xw:
        lectura.to_excel(xw, sheet_name="LECTURA", index=False)
        df_serie.to_excel(xw, sheet_name="SERIE_LARGA", index=False)
        cobertura.to_excel(xw, sheet_name="COBERTURA_2015_2025", index=False)
        brechas.to_excel(xw, sheet_name="BRECHAS_Y_ACCIONES", index=False)
        df_fuentes.to_excel(xw, sheet_name="FUENTES", index=False)
        df_eventos.to_excel(xw, sheet_name="EVENTOS_MATERIALES", index=False)
        normalizacion.to_excel(xw, sheet_name="NORMALIZACION_DEMO", index=False)

    OUT_EXPO = ROOT / "docs" / "COOPERATIVAS_EXPOSICION_PORTUARIA.xlsx"
    with pd.ExcelWriter(OUT_EXPO, engine="openpyxl") as xw:
        df_exposicion.to_excel(xw, sheet_name="EXPOSICION", index=False)
        df_expo_metodo.to_excel(xw, sheet_name="METODO", index=False)

    generar_solicitudes(brechas)

    print(f"registros: {len(df_serie)} | estados: {resumen}")
    print(f"anios con dato: {anios_cubiertos}")
    print(f"cobertura indicadores: {len(cobertura)} | brechas 2015-2025: {len(brechas)}")
    print(f"cooperativas en exposicion portuaria: {len(df_exposicion)}")
    print(f"salida: {OUT_XLSX}")
    print(f"salida: {OUT_EXPO}")
    print(f"salida: {OUT_SOLICITUDES}")
    print()
    print("COBERTURA_2015_2025:")
    print(cobertura[["indicador"] + [str(y) for y in YEARS]].to_string(index=False))


if __name__ == "__main__":
    main()
