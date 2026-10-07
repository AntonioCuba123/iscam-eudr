"""
Genera el historico de cambios de DIM_ORGANIZACION para la pestana HIST_ATRIBUTO.

Compara dos versiones del libro BASE CONSOLIDADA.xlsx (un "antes" y un "despues" de
refrescar una o mas fuentes: SUNAT, OECE, RNP, PPA, FOB, contratacion) y detecta, por
RUC y por atributo de DIM_ORGANIZACION, los valores que cambiaron. No inventa datos:
si no hay una segunda consulta de las fuentes, no hay nada que comparar (backup ==
actual) y el script no genera filas.

Uso tipico (cuando se vuelva a consultar SUNAT/OECE/RNP/PPA/FOB/OCDS):
  1. Antes de tocar el libro, guardar una copia: "BASE CONSOLIDADA.backup_<fecha>.xlsx"
  2. Actualizar las pestanas de fuente (RUC_CONSULTAMASIVA, RUC_OECE, etc.) y las
     formulas derivadas (DIM_ORGANIZACION ya las recalcula solo).
  3. Correr en modo revision (no escribe nada):
       python hist_atributo_diff.py --before "BASE CONSOLIDADA.backup_2026-10-01.xlsx" --after "BASE CONSOLIDADA.xlsx"
     Esto imprime un resumen y guarda el detalle en hist_atributo_propuesto.csv
  4. Revisar el CSV. Si esta OK, aplicar (agrega las filas a HIST_ATRIBUTO y guarda el xlsx):
       python hist_atributo_diff.py --before "BASE CONSOLIDADA.backup_2026-10-01.xlsx" --after "BASE CONSOLIDADA.xlsx" --apply

Reglas aplicadas (ver README seccion 5.1):
  - Un valor vacio, "-" o 0 no "reemplaza" a uno informado, pero SI se registra como
    dato nuevo cuando antes estaba vacio (observacion = "dato nuevo") y como dato
    perdido cuando antes tenia valor y ahora esta vacio (observacion = "dato eliminado";
    esto casi siempre es sospechoso y merece revision manual, no se aplica solo).
  - No se comparan columnas derivadas/meta: fecha_ultima_actualizacion, score_completitud.
  - RUC nuevos (alta) o RUC que desaparecen (baja) se listan aparte, no como cambios
    de atributo.
"""
import argparse
import csv
import sys
from datetime import datetime

import openpyxl

SHEET = "DIM_ORGANIZACION"
KEY_COL = "ruc"
EXCLUDE_COLS = {"fecha_ultima_actualizacion", "score_completitud"}

# Atributo -> fuente 1 (directa y vigente), segun README seccion 5.3
ATRIBUTO_FUENTE = {
    "razon_social": "SUNAT Consulta RUC",
    "nombre_comercial": "SUNAT Consulta RUC",
    "tipo_contribuyente": "SUNAT Consulta RUC",
    "tipo_organizacion_programa": "Registro interno (b2)",
    "estado_contribuyente": "SUNAT Consulta RUC",
    "condicion_contribuyente": "SUNAT Consulta RUC",
    "fecha_inscripcion_ruc": "SUNAT Consulta RUC",
    "fecha_inicio_actividades": "SUNAT Consulta RUC",
    "ubigeo": "INEI (derivado SUNAT)",
    "departamento": "SUNAT domicilio fiscal",
    "provincia": "SUNAT domicilio fiscal",
    "distrito": "SUNAT domicilio fiscal",
    "direccion_fiscal": "SUNAT domicilio fiscal",
    "actividad_comercio_exterior": "SUNAT Consulta RUC",
    "ciiu_principal": "SUNAT Consulta RUC",
    "ciiu_secundario_1": "SUNAT Consulta RUC",
    "ciiu_secundario_2": "SUNAT Consulta RUC",
    "buen_contribuyente": "SUNAT Consulta RUC",
    "agente_retencion": "SUNAT Consulta RUC",
    "telefono_principal": "OECE ficha de proveedor",
    "email_principal": "OECE ficha de proveedor",
    "inscrito_rnp": "RNP (OECE)",
    "codigo_rnp": "RNP (OECE)",
    "inscrito_ppa": "MIDAGRI-PPA",
    "nombre_ppa": "MIDAGRI-PPA",
    "ventas_totales_2024": "Registro interno (b2, HECHO_PROGRAMA_ANUAL)",
    "ventas_totales_2025": "Registro interno (b2, HECHO_PROGRAMA_ANUAL)",
    "exporta": "SUNAT-Aduanas (HECHO_EXPORTACION)",
    "fob_total_usd": "SUNAT-Aduanas (HECHO_EXPORTACION)",
    "ultimo_periodo_exportacion": "SUNAT-Aduanas (HECHO_EXPORTACION)",
    "fob_ultimo_anio_usd": "SUNAT-Aduanas (HECHO_EXPORTACION)",
    "n_paises_destino": "SUNAT-Aduanas (HECHO_EXPORTACION)",
    "presidente_vigente": "OECE/RNP (REL_PERSONA_CARGO)",
    "representante_legal_vigente": "OECE/RNP (REL_PERSONA_CARGO)",
    "gerente_general": "OECE/RNP (REL_PERSONA_CARGO)",
    "n_directivos_vigentes": "OECE/RNP (REL_PERSONA_CARGO)",
    "producto_dominante": "Registro interno (b2)",
    "anios_intervencion": "Registro interno (b2)",
    "servicio_programa": "Registro interno (b2)",
    "n_socios_varones": "Registro interno (b3)",
    "n_socias_mujeres": "Registro interno (b3)",
    "hectareas_totales": "Registro interno (b3)",
    "certificacion_organica": "Organismo certificador / b3",
    "certificacion_comercio_justo": "Organismo certificador / b3",
    "avance_eudr": "Registro interno (b3)",
}


def norm(v):
    """Normaliza para comparar: None/''/'-' -> None (vacio); strings recortados."""
    if v is None:
        return None
    if isinstance(v, str):
        v = v.strip()
        if v in ("", "-"):
            return None
        return v
    return v


def sheet_dict_by_ruc(path, sheet=SHEET):
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb[sheet]
    headers = [c.value for c in ws[1]]
    if KEY_COL not in headers:
        raise SystemExit(f"La pestana {sheet} no tiene columna '{KEY_COL}' en {path}")
    out = {}
    for row in ws.iter_rows(min_row=2):
        vals = [c.value for c in row]
        ruc = vals[0]
        if ruc is None:
            continue
        out[str(ruc)] = dict(zip(headers, vals))
    return headers, out


def diff(before_path, after_path, fecha_valor=None, usuario_o_proceso="hist_atributo_diff.py"):
    fecha_valor = fecha_valor or datetime.now().strftime("%Y-%m-%d")

    headers_b, before = sheet_dict_by_ruc(before_path)
    headers_a, after = sheet_dict_by_ruc(after_path)

    cols = [h for h in headers_a if h != KEY_COL and h not in EXCLUDE_COLS]

    rucs_before = set(before)
    rucs_after = set(after)
    altas = sorted(rucs_after - rucs_before)
    bajas = sorted(rucs_before - rucs_after)
    comunes = sorted(rucs_before & rucs_after)

    rows = []
    for ruc in comunes:
        rb = before[ruc]
        ra = after[ruc]
        for col in cols:
            vb = norm(rb.get(col))
            va = norm(ra.get(col))
            if vb == va:
                continue
            if vb is None and va is not None:
                obs = "dato nuevo"
            elif vb is not None and va is None:
                obs = "dato eliminado (revisar)"
            else:
                obs = "cambio de valor"
            rows.append({
                "ruc": ruc,
                "atributo": col,
                "valor_anterior": "" if vb is None else vb,
                "valor_nuevo": "" if va is None else va,
                "fecha_valor": fecha_valor,
                "fuente": ATRIBUTO_FUENTE.get(col, ""),
                "usuario_o_proceso": usuario_o_proceso,
                "observacion": obs,
            })

    return rows, altas, bajas


def write_csv(rows, out_path):
    fieldnames = ["ruc", "atributo", "valor_anterior", "valor_nuevo", "fecha_valor",
                  "fuente", "usuario_o_proceso", "observacion"]
    with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def apply_to_workbook(rows, after_path):
    wb = openpyxl.load_workbook(after_path)
    ws = wb["HIST_ATRIBUTO"]
    next_row = ws.max_row + 1
    # si la hoja solo tiene el encabezado (fila 1) con datos vacios, empezar en fila 2
    if next_row == 2:
        first = [c.value for c in ws[1]]
        if all(v is None for v in first):
            next_row = 1  # no deberia pasar (fila 1 es encabezado real), salvaguarda
    fieldnames = ["ruc", "atributo", "valor_anterior", "valor_nuevo", "fecha_valor",
                  "fuente", "usuario_o_proceso", "observacion"]
    for r in rows:
        for i, key in enumerate(fieldnames, start=1):
            ws.cell(row=next_row, column=i, value=r[key])
        next_row += 1
    wb.save(after_path)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--before", required=True, help="xlsx de referencia (antes del refresco)")
    ap.add_argument("--after", required=True, help="xlsx actual (despues del refresco); tambien se actualiza si se usa --apply")
    ap.add_argument("--fecha", default=None, help="fecha_valor a registrar (aaaa-mm-dd); por defecto hoy")
    ap.add_argument("--out-csv", default="hist_atributo_propuesto.csv", help="CSV de revision (modo dry-run)")
    ap.add_argument("--apply", action="store_true", help="Escribe las filas directamente en HIST_ATRIBUTO del --after y guarda el xlsx")
    args = ap.parse_args()

    rows, altas, bajas = diff(args.before, args.after, fecha_valor=args.fecha)

    print(f"RUC nuevos (en 'after', no en 'before'): {len(altas)}")
    if altas:
        print("  ", ", ".join(altas[:20]), "..." if len(altas) > 20 else "")
    print(f"RUC que desaparecieron (en 'before', no en 'after'): {len(bajas)}")
    if bajas:
        print("  ", ", ".join(bajas[:20]), "..." if len(bajas) > 20 else "")
    print(f"Cambios de atributo detectados: {len(rows)}")

    if not rows:
        print("Nada que registrar en HIST_ATRIBUTO (las dos versiones son iguales en los atributos comparados).")
        return

    if args.apply:
        apply_to_workbook(rows, args.after)
        print(f"Se agregaron {len(rows)} filas a HIST_ATRIBUTO en {args.after} y se guardo el archivo.")
    else:
        write_csv(rows, args.out_csv)
        print(f"Modo revision: no se modifico el xlsx. Detalle en {args.out_csv}")
        print("Revisalo y corre de nuevo con --apply para escribirlo en HIST_ATRIBUTO.")


if __name__ == "__main__":
    sys.exit(main())
