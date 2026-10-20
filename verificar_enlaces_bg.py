# -*- coding: utf-8 -*-
"""Verifica en vivo los enlaces ADUANET del Excel (concurrente, reanudable).

Nivel 1 (resumen por año): cuenta los combos jsDetalleDUA que devuelve la pagina.
Nivel 2 (listado de DUAs): cuenta las filas de DUA (tr.bg) que devuelve.

Guarda el avance en un CSV incremental. Si se corta, reanuda donde quedó.
Al terminar escribe el resultado de vuelta en el Excel.

Uso: python verificar_enlaces_bg.py [--workers N]
"""
import argparse
import csv
import os
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.request import urlopen, Request

import pandas as pd

XLSX = (r"C:\Users\acuba\eudrperu\BASE CAFE CACAO 174"
        r"\CONSULTA MASIVA RUC 10.10.26\ENLACES_BUSQUEDA_DUA_2024-2026.xlsx")
SALIDA = r"C:\Users\acuba\eudrperu\ficharucsunat\_verif_dua_links.csv"

HOJAS = [("1. Resumen por año", "ENLACE ADUANET — resumen del año", "n1"),
         ("2. Listado DUAs", "ENLACE ADUANET — listado de DUAs", "n2")]
CLAVES = ("RUC", "Año", "Mes", "País", "Aduana (3 dígitos)")

UA = {"User-Agent": "Mozilla/5.0"}
TIMEOUT = 25
REINTENTOS = 3
ESPERA = 1.0

_PAT = re.compile(
    r'jsDetalleDUA\(\s*"?(\d+)"?\s*,\s*"?(\d+)"?\s*,\s*"?(\d+)"?\s*,\s*"?(\d+)"?\s*,'
    r'\s*"?(\d+)"?\s*,\s*"?(\d+)"?\s*,\s*"?([A-Za-z]{2})"?\s*\)')


def get(u):
    return urlopen(Request(u, headers=UA), timeout=TIMEOUT).read().decode("latin1", "replace")


def analizar(url, nivel):
    """(estado, conteo, detalle). estado: OK, VACIO, ERROR."""
    for intento in range(REINTENTOS):
        try:
            html = get(url)
            if nivel == "n1":
                n = len(_PAT.findall(html))
                return ("OK" if n else "VACIO"), n, \
                       ("%d combos adu/agente/mes/país en el resumen" % n if n
                        else "resumen sin combos")
            filas = []
            for tr in re.findall(r'<tr class="bg"[^>]*>(.*?)</tr>', html, re.S):
                tds = [re.sub(r"<[^>]+>", "", x).strip()
                       for x in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)]
                if not tds:
                    continue
                if tds[0].lower().startswith("no se encontr"):
                    return "VACIO", 0, "sin DUAs en ese combo"
                filas.append(tds)
            if filas:
                det = "; ".join("%s %s %s %s" % (f[0], f[2], f[3], f[4]) for f in filas[:6])
                return "OK", len(filas), det
            return "VACIO", 0, "respuesta sin filas"
        except Exception as e:
            if intento == REINTENTOS - 1:
                return "ERROR", 0, "%s: %s" % (type(e).__name__, str(e)[:70])
            time.sleep(ESPERA * (intento + 1) * 2)
    return "ERROR", 0, "sin respuesta"


# ---------------------------------------------------------------- lista de tareas
tareas = []
for hoja, col, nivel in HOJAS:
    d = pd.read_excel(XLSX, sheet_name=hoja, dtype=str)
    for idx, row in d.iterrows():
        u = row.get(col)
        if u and str(u).startswith("http"):
            ident = " | ".join("%s=%s" % (k, row.get(k)) for k in CLAVES if k in d.columns)
            tareas.append({"nivel": nivel, "hoja": hoja, "fila": int(idx) + 2,
                           "url": str(u), "ident": ident})

hechos = {}
if os.path.exists(SALIDA):
    with open(SALIDA, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            hechos[(r["nivel"], r["fila"])] = r
pend = [t for t in tareas if (t["nivel"], t["fila"]) not in hechos]

print("Total: %d | ya verificados: %d | pendientes: %d" % (len(tareas), len(hechos), len(pend)),
      flush=True)

ap = argparse.ArgumentParser()
ap.add_argument("--workers", type=int, default=4)
args = ap.parse_args()

lock = threading.Lock()
cont = {"ok": 0, "vacio": 0, "err": 0, "n": 0}
t0 = time.time()
modo = "a" if os.path.exists(SALIDA) else "w"

with open(SALIDA, modo, newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=["nivel", "hoja", "fila", "ident", "url",
                                      "estado", "conteo", "detalle"])
    if modo == "w":
        w.writeheader()
        f.flush()

    def trabajo(t):
        est, n, det = analizar(t["url"], t["nivel"])
        return t, est, n, det

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futuros = {ex.submit(trabajo, t): t for t in pend}
        for fut in as_completed(futuros):
            t, est, n, det = fut.result()
            with lock:
                w.writerow({"nivel": t["nivel"], "hoja": t["hoja"], "fila": t["fila"],
                            "ident": t["ident"], "url": t["url"], "estado": est,
                            "conteo": n, "detalle": det})
                f.flush()
                cont["n"] += 1
                cont[{"OK": "ok", "VACIO": "vacio", "ERROR": "err"}[est]] += 1
                i, tot = cont["n"], len(pend)
                if i % 25 == 0 or i == tot:
                    el = time.time() - t0
                    print("  %d/%d ok=%d vacio=%d err=%d (%.0fs, %.1fs/enlace, %d workers)"
                          % (i, tot, cont["ok"], cont["vacio"], cont["err"], el, el / i,
                             args.workers), flush=True)
            time.sleep(0.05)

print("Terminado: ok=%d vacio=%d err=%d" % (cont["ok"], cont["vacio"], cont["err"]), flush=True)

# ---------------------------------------------------------------- volcar al Excel
res = {}
with open(SALIDA, encoding="utf-8-sig") as f:
    for r in csv.DictReader(f):
        res[(r["nivel"], int(r["fila"]))] = r

from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment

wb = load_workbook(XLSX)
COLOR = {"OK": ("C6EFCE", "1F6F3D", True), "VACIO": ("F2F2F2", "808080", False),
         "ERROR": ("FFC7CE", "9C0006", False)}
TXT = {"OK": "VERIFICADO en vivo", "VACIO": "VACIO - sin resultados",
       "ERROR": "REVISAR - error de red"}

for hoja, col, nivel in HOJAS:
    ws = wb[hoja]
    enc = [c.value for c in ws[1]]
    if col not in enc:
        continue
    nombre_conteo = "N° combos (resumen)" if nivel == "n1" else "N° DUAs"
    for nombre in ("Estado del enlace", nombre_conteo, "Detalle de la verificación"):
        if nombre not in enc:
            ws.cell(row=1, column=len(enc) + 1, value=nombre)
            enc.append(nombre)
    ce = enc.index("Estado del enlace") + 1
    cn = enc.index(nombre_conteo) + 1
    cd = enc.index("Detalle de la verificación") + 1
    for fila in range(2, ws.max_row + 1):
        r = res.get((nivel, fila))
        if not r:
            continue
        est = r["estado"]
        bg, fg, bold = COLOR[est]
        c = ws.cell(row=fila, column=ce, value=TXT[est])
        c.fill = PatternFill("solid", fgColor=bg)
        c.font = Font(bold=bold, size=9, color=fg)
        c.alignment = Alignment(vertical="top", wrap_text=True)
        try:
            if int(r.get("conteo") or 0) > 0:
                ws.cell(row=fila, column=cn, value=int(r["conteo"]))
        except (TypeError, ValueError):
            pass
        ws.cell(row=fila, column=cd, value=r.get("detalle", "")[:250]).alignment = \
            Alignment(vertical="top", wrap_text=True)

wb.save(XLSX)
print("Excel actualizado ->", XLSX, flush=True)
