"""
Reconstruye, en un solo script Python, las dos fuentes externas de
DIM_ORGANIZACION que hoy no tienen ningun conector local (solo existen como
.ts en el repo Rastro/appsperu, apps/identidad-fiscal/api/src/ingest/):

  Nivel 1 -- OECE, ficha de proveedor (alimenta RUC_OECE, RUC_OECE_PERSONAS
             y RNP -- las tres salen de la MISMA llamada, RNP es solo el
             subconjunto con codigo_registro no vacio, no hace falta pedirla
             aparte):
    GET https://eap.oece.gob.pe/ficha-proveedor-cns/1.0/ficha/{ruc}/resumen
    GET https://eap.oece.gob.pe/perfilprov-bus/1.0/ficha/{ruc}  (telefono/email)

  Nivel 2 -- MIDAGRI, Padron de Productores Agrarios (alimenta RUC_PPA):
    GET https://gateway.midagri.gob.pe/sisppa/api/services/app/Consulta/GetNombreConsulta
        ?codDocumento=6&Documento={ruc}

Ambos son JSON, sin captcha ni sesion -- confirmado en vivo el 24/09/2026
contra el RUC 20404057805 (ACOPAGRO), mismo caso que uso el conector
original del 20/09/2026 en Rastro. El parseo replica exactamente
oece-ficha-normalize.ts y padron-ppa-normalize.ts de ese repo (ver
apps/identidad-fiscal/api/src/ingest/ en Treevu-ai/appsperu).

NO cubre b1/b2/b3 (hojas preexistentes del programa, no son fuentes
externas reconstruibles) ni RUC_CONSULTAMASIVA (bloqueado: *.sunat.gob.pe
no admite fetch directo, requiere el formulario web de e.sunat.gob.pe) ni
RUC_FOB/RUC_FOB_DUA (ya tienen su propio conector, dua_canal_full.py).

Uso:
  python identidad_fiscal_oece_ppa.py [--limit N] [--resume-from N]
Lee el universo de RUC desde RUC_CONSULTAMASIVA (597 RUC) y escribe 3 CSV
(oece_ficha.csv, oece_personas.csv, padron_ppa.csv) -- no toca el xlsx, eso
es un paso aparte (mismo patron que dua_canal_full.py + load_dua_canal.py).
"""
import argparse
import csv
import json
import re
import sys
import time
from datetime import datetime, timezone
from urllib.request import urlopen, Request

import openpyxl

XLSX_PATH = "BASE CONSOLIDADA.xlsx"
OECE_RESUMEN_URL = "https://eap.oece.gob.pe/ficha-proveedor-cns/1.0/ficha/{ruc}/resumen"
OECE_CONTACTO_URL = "https://eap.oece.gob.pe/perfilprov-bus/1.0/ficha/{ruc}"
PPA_URL = "https://gateway.midagri.gob.pe/sisppa/api/services/app/Consulta/GetNombreConsulta?codDocumento=6&Documento={ruc}"
DELAY_S = 0.3


def read_universo():
    wb = openpyxl.load_workbook(XLSX_PATH, data_only=True)
    ws = wb["RUC_CONSULTAMASIVA"]
    rucs = [str(row[0].value) for row in ws.iter_rows(min_row=2, max_row=ws.max_row) if row[0].value]
    return rucs


def fetch_json(url, timeout=20):
    req = Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
    with urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def empty_to_none(v):
    t = (v or "").strip() if isinstance(v, str) else v
    return None if t in ("", "null", None) else t


def parse_fecha_ddmmyyyy(v):
    if not v:
        return None
    m = re.match(r"^(\d{2})/(\d{2})/(\d{4})$", v.strip())
    if not m:
        return None
    dd, mm, yyyy = m.groups()
    return f"{yyyy}-{mm}-{dd}"


def parse_oece_ficha(ruc, raw, telefono, email):
    s = raw.get("datosSunat") or {}
    conf = raw.get("conformacion") or {}
    proveedor = conf.get("proveedor") or {}
    return {
        "ruc": ruc,
        "razon_social": empty_to_none(s.get("razon")),
        "tipo_empresa": empty_to_none(s.get("tipoEmpresa")),
        "estado_sunat": empty_to_none(s.get("estado")),
        "condicion_sunat": empty_to_none(s.get("condicion")),
        "departamento": empty_to_none(s.get("departamento")),
        "provincia": empty_to_none(s.get("provincia")),
        "distrito": empty_to_none(s.get("distrito")),
        "telefono": telefono,
        "email": email,
        "codigo_registro": empty_to_none(proveedor.get("codigoRegistro")),
    }


def map_persona(rol, raw):
    source_id = raw.get("idRepresentante") or raw.get("idOrgano") or raw.get("idSocio")
    if source_id is None:
        return None
    nombre = empty_to_none(raw.get("razonSocial") or raw.get("apellidosNomb"))
    if nombre is None:
        return None
    return {
        "rol": rol,
        "source_id": source_id,
        "dni": empty_to_none(raw.get("nroDocumento")),
        "nombre": nombre,
        "tipo_organo": empty_to_none(raw.get("descTipoOrgano")),
        "cargo": empty_to_none(raw.get("descCargo")),
        "fecha_ingreso": parse_fecha_ddmmyyyy(raw.get("fechaIngreso")),
    }


def parse_oece_personas(raw):
    conf = raw.get("conformacion") or {}
    personas = []
    for r in conf.get("representantes") or []:
        p = map_persona("REPRESENTANTE", r)
        if p:
            personas.append(p)
    for r in conf.get("organosAdm") or []:
        p = map_persona("ORGANO_ADMINISTRACION", r)
        if p:
            personas.append(p)
    for r in conf.get("socios") or []:
        p = map_persona("SOCIO", r)
        if p:
            personas.append(p)
    return personas


def parse_ppa(raw):
    nombre = (raw.get("result") or "").strip()
    registrado = nombre not in ("", "-")
    return {"registrado": registrado, "nombre_ppa": nombre if registrado else None}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--resume-from", type=int, default=0)
    args = ap.parse_args()

    rucs = read_universo()
    print(f"universo: {len(rucs)} RUC")
    if args.limit:
        rucs = rucs[args.resume_from: args.resume_from + args.limit]
    else:
        rucs = rucs[args.resume_from:]

    ficha_fields = ["ruc", "razon_social", "tipo_empresa", "estado_sunat", "condicion_sunat",
                     "departamento", "provincia", "distrito", "telefono", "email",
                     "codigo_registro", "fecha_consulta"]
    persona_fields = ["ruc", "rol", "source_id", "dni", "nombre", "tipo_organo", "cargo",
                       "fecha_ingreso", "fecha_consulta"]
    ppa_fields = ["ruc", "registrado", "nombre_ppa", "fecha_consulta"]

    mode = "a" if args.resume_from else "w"
    write_header = not (args.resume_from and mode == "a")

    n_ok, n_err = 0, 0
    t0 = time.time()

    with open("oece_ficha.csv", mode, newline="", encoding="utf-8-sig") as f_ficha, \
         open("oece_personas.csv", mode, newline="", encoding="utf-8-sig") as f_personas, \
         open("padron_ppa.csv", mode, newline="", encoding="utf-8-sig") as f_ppa:

        w_ficha = csv.DictWriter(f_ficha, fieldnames=ficha_fields)
        w_personas = csv.DictWriter(f_personas, fieldnames=persona_fields)
        w_ppa = csv.DictWriter(f_ppa, fieldnames=ppa_fields)
        if write_header:
            w_ficha.writeheader()
            w_personas.writeheader()
            w_ppa.writeheader()

        for i, ruc in enumerate(rucs, start=1):
            fecha_consulta = datetime.now(timezone.utc).isoformat()
            try:
                # Nivel 1: OECE
                resumen = fetch_json(OECE_RESUMEN_URL.format(ruc=ruc))
                telefono, email = None, None
                try:
                    contacto = fetch_json(OECE_CONTACTO_URL.format(ruc=ruc))
                    prov = contacto.get("proveedorT01") or {}
                    telefonos = prov.get("telefonos") or []
                    emails = prov.get("emails") or []
                    telefono = telefonos[0] if telefonos else None
                    email = emails[0] if emails else None
                except Exception:
                    pass  # sin telefono/email no es fatal, la ficha SUNAT igual se guarda

                ficha = parse_oece_ficha(ruc, resumen, telefono, email)
                ficha["fecha_consulta"] = fecha_consulta
                w_ficha.writerow(ficha)

                for p in parse_oece_personas(resumen):
                    p["ruc"] = ruc
                    p["fecha_consulta"] = fecha_consulta
                    w_personas.writerow(p)

                # Nivel 2: MIDAGRI-PPA
                ppa_raw = fetch_json(PPA_URL.format(ruc=ruc))
                ppa = parse_ppa(ppa_raw)
                ppa["ruc"] = ruc
                ppa["fecha_consulta"] = fecha_consulta
                w_ppa.writerow(ppa)

                n_ok += 1
            except Exception as e:
                n_err += 1
                print(f"[{i}/{len(rucs)}] ERROR ruc={ruc}: {e}", flush=True)

            if i % 50 == 0 or i == len(rucs):
                elapsed = time.time() - t0
                print(f"[{i}/{len(rucs)}] ok={n_ok} err={n_err} ({elapsed:.0f}s, {elapsed/i:.2f}s/fila)", flush=True)

            time.sleep(DELAY_S)

    print(f"Listo. ok={n_ok} err={n_err}. CSV: oece_ficha.csv, oece_personas.csv, padron_ppa.csv")


if __name__ == "__main__":
    sys.exit(main())
