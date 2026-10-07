"""Análisis de la programación diaria de naves 2023 del Callao
(unico bloque de dato de trafico portuario posterior a 2017
disponible en datos abiertos, sin Ley 27806).

Fuente: reportes mensuales "Programación diaria de movimiento de
naves — NAVES ARRIBADAS/RECEPCIONADAS" del MTC/APN, Feb-Jun 2023
(5 de 12 meses; Enero, Julio y Agosto no existen en el portal,
HTTP 404; Setiembre-Diciembre solo existen como extractos de UN
SOLO DIA, registrados aparte como naves_extracto_diario_2023).

Dimensiones extraidas por fila: N°, DUE (CLL-2023-XXXXX), NAVE,
H.ARR, H.LP, estadía (h), BANDERA, RECEPCIONADO, PTO PROCEDENCIA,
AGENTE, ETD, COND (LINEA/TRAMPA), MOTIVO ESCALA, TIPO NAVE, OBS.

Lectura RLAC/TBML: FATF/GAFILAT asocian mayor riesgo al tráfico
tramp (irregular) y a banderas de conveniencia; se reportan los
shares por mes, no una calificación.
"""
import re
from collections import Counter
from pathlib import Path

import pandas as pd
import xlrd

CACHE = Path(r"C:\Users\acuba\eudrperu\data\icrpp\open_csv")
SERIE_XLSX = Path(r"C:\Users\acuba\eudrperu\docs\ICRPP_SERIE_HISTORICA_RECONSTRUIDA.xlsx")
OUT_XLSX = Path(r"C:\Users\acuba\eudrperu\docs\NAVES_2023_CALLAO_ANALISIS.xlsx")

MESES = ["Febrero", "Marzo", "Abril", "Mayo", "Junio"]
MES_NUM = {"Febrero": 2, "Marzo": 3, "Abril": 4, "Mayo": 5, "Junio": 6}
DUE_RE = re.compile(r"^CLL-2023-(\d{5})$")

PUERTOS_PERU = {
    "CALLAO", "CHANCAY", "SUPE", "HUACHO", "HUARMEY", "CHIMBOTE",
    "SALAVERRY", "CHICAMA", "TALARA", "PAITA", "BAYOVAR", "ETEN",
    "PISCO", "SAN NICOLAS", "MATARANI", "ILO", "PUNTA LOBITOS",
    "MOLLENDO", "PUNTA PATACHE", "CABO NEGRO", "PATILLOS",
    "CALETA COLOSO", "PUNTA CHUNGO", "SAN JUAN DE MARCONA",
}
AGUAS_INTERNACIONALES = {
    "INTERNATIONAL WATERS", "NATIONAL WATERS", "CRUCE CANAL DE PANAMA",
}
BANDERAS_CONVENIENCIA = {
    "LIBERIA", "PANAMA", "ISLAS MARSHALL", "MALTA", "BAHAMAS",
    "HONDURAS", "CYPRUS", "CURACAO",
}


def clasificar_procedencia(p):
    if p in PUERTOS_PERU:
        return "PERU"
    if p in AGUAS_INTERNACIONALES:
        return "AGUAS INTERNACIONALES"
    return "EXTRANJERO"


def parsear_horas(s):
    m = re.match(r"^(\d+):(\d{2})$", s.strip())
    if not m:
        return None
    return int(m.group(1)) + int(m.group(2)) / 60.0


def parsear_mes(mes):
    path = CACHE / f"reporte-{mes}2023.xls"
    wb = xlrd.open_workbook(str(path))
    sh = wb.sheet_by_index(0)
    filas = []
    for i in range(7, sh.nrows):
        due = str(sh.cell_value(i, 2)).strip()
        m = DUE_RE.match(due)
        if not m:
            continue
        filas.append(dict(
            mes=mes, n_mes=int(float(str(sh.cell_value(i, 1)).strip() or 0)),
            due=due, due_num=int(m.group(1)),
            nave=str(sh.cell_value(i, 3)).strip(),
            bandera=str(sh.cell_value(i, 9)).strip() or "S/D",
            recepcionado=str(sh.cell_value(i, 10)).strip() or "S/D",
            procedencia=str(sh.cell_value(i, 11)).strip() or "S/D",
            agente=str(sh.cell_value(i, 12)).strip() or "S/D",
            cond=str(sh.cell_value(i, 14)).strip() or "S/D",
            motivo=str(sh.cell_value(i, 15)).strip() or "S/D",
            tipo=str(sh.cell_value(i, 17)).strip() or "S/D",
            estadia_h=parsear_horas(str(sh.cell_value(i, 8)).strip()),
            obs=str(sh.cell_value(i, 19)).strip(),
        ))
    return filas


def main():
    detalle = []
    for mes in MESES:
        detalle.extend(parsear_mes(mes))
    df = pd.DataFrame(detalle)

    mensual = []
    for mes in MESES:
        g = df[df.mes == mes]
        trampa = int((g.cond == "TRAMPA").sum())
        linea = int((g.cond == "LINEA").sum())
        proc_clas = g.procedencia.map(clasificar_procedencia)
        n_peru = int((proc_clas == "PERU").sum())
        n_extranj = int((proc_clas == "EXTRANJERO").sum())
        n_aguas = int((proc_clas == "AGUAS INTERNACIONALES").sum())
        n_conveniencia = int(g.bandera.isin(BANDERAS_CONVENIENCIA).sum())
        no_paga = int(g.obs.str.contains("NO PAGA", case=False, na=False).sum())
        mensual.append(dict(
            mes=mes, mes_num=MES_NUM[mes],
            n_naves=len(g),
            naves_unicas=g.nave.nunique(),
            tipos_distintos=g.tipo.nunique(),
            banderas_distintas=g.bandera.nunique(),
            procedencias_distintas=g.procedencia.nunique(),
            agentes_distintos=g.agente.nunique(),
            share_trampa=round(trampa / len(g), 4) if len(g) else None,
            n_trampa=trampa, n_linea=linea,
            share_procedencia_peru=round(n_peru / len(g), 4) if len(g) else None,
            share_procedencia_extranjera=round(n_extranj / len(g), 4) if len(g) else None,
            share_aguas_internacionales=round(n_aguas / len(g), 4) if len(g) else None,
            n_procedencia_peru=n_peru, n_procedencia_extranjera=n_extranj,
            n_aguas_internacionales=n_aguas,
            banderas_conveniencia=n_conveniencia,
            share_banderas_conveniencia=round(n_conveniencia / len(g), 4) if len(g) else None,
            obs_no_paga=no_paga,
            share_no_paga=round(no_paga / len(g), 4) if len(g) else None,
            estadia_media_h=round(float(g.estadia_h.mean()), 2) if g.estadia_h.notna().any() else None,
            estadia_mediana_h=round(float(g.estadia_h.median()), 2) if g.estadia_h.notna().any() else None,
            estadia_max_h=round(float(g.estadia_h.max()), 2) if g.estadia_h.notna().any() else None,
            due_min=g.due_num.min(), due_max=g.due_num.max(),
        ))
    mensual = pd.DataFrame(mensual)

    tipo_mes = df.pivot_table(index="tipo", columns="mes", values="due",
                                  aggfunc="count", fill_value=0)
    tipo_mes["TOTAL"] = tipo_mes.sum(axis=1)
    tipo_mes["%"] = (tipo_mes["TOTAL"] / tipo_mes["TOTAL"].sum()).round(4)
    tipo_mes = tipo_mes.sort_values("TOTAL", ascending=False)

    cond_mes = df.pivot_table(index="cond", columns="mes", values="due",
                                  aggfunc="count", fill_value=0)
    cond_mes["TOTAL"] = cond_mes.sum(axis=1)
    cond_mes["%"] = (cond_mes["TOTAL"] / cond_mes["TOTAL"].sum()).round(4)

    motivo_mes = df.pivot_table(index="motivo", columns="mes", values="due",
                                     aggfunc="count", fill_value=0)
    motivo_mes["TOTAL"] = motivo_mes.sum(axis=1)
    motivo_mes["%"] = (motivo_mes["TOTAL"] / motivo_mes["TOTAL"].sum()).round(4)

    proc = (df.groupby("procedencia")
              .agg(n_naves=("due", "count"),
                   n_meses=("mes", "nunique"),
                   n_naves_distintas=("nave", "nunique"))
              .sort_values("n_naves", ascending=False))
    proc["share"] = (proc["n_naves"] / proc["n_naves"].sum()).round(4)
    proc["extranjera"] = proc.index != "PERU"

    bandera = (df.groupby("bandera")
                 .agg(n_naves=("due", "count"),
                      n_naves_distintas=("nave", "nunique"))
                 .sort_values("n_naves", ascending=False))
    bandera["share"] = (bandera["n_naves"] / bandera["n_naves"].sum()).round(4)

    due_seq = []
    max_prev = None
    for mes in MESES:
        g = df[df.mes == mes].sort_values("due_num")
        nums = g.due_num.values
        nuevos = (int(nums.max()) - max_prev) if max_prev is not None else None
        due_seq.append(dict(
            mes=mes, due_min=int(nums.min()), due_max=int(nums.max()),
            n_reportadas=len(g),
            due_nuevos_mes=nuevos,
            cobertura_vs_nuevos=(round(len(g) / nuevos, 4)
                                  if nuevos else None),
            nota=("numeracion CLL-2023 acumulada en el anio; "
                  "cobertura = reportadas / (max DUE mes - max DUE mes "
                  "anterior). Febrero: sin baseline de Enero (reporte "
                  "Enero 2023 no existe, 404) -> S/D."),
        ))
        max_prev = int(nums.max())
    due_seq = pd.DataFrame(due_seq)

    naves_hist = pd.read_excel(SERIE_XLSX, "SERIE_LARGA")
    ch = naves_hist[(naves_hist.indicador == "naves_recibidas")
                    & (naves_hist.puerto == "Callao")]
    hist = (ch.groupby("anio")["valor"].sum() / 12.0).round(1)
    tendencia = pd.DataFrame({
        "anio": list(hist.index) + [2023],
        "naves_mes_promedio": list(hist.values)
        + [round(float(mensual.set_index("mes").loc[MESES, "n_naves"].mean()), 1)],
    })
    tendencia["fuente"] = ["APN datos abiertos (movimiento anual/12)"] * len(hist) + \
        ["APN programación diaria Feb-Jun 2023 (5 meses)"]
    tendencia["estado"] = ["ABIERTO"] * len(hist) + ["PARCIAL"]

    lectura = pd.DataFrame([
        ("Qué es", "Analisis de la programación diaria de naves "
                     "arribadas/recepcionadas en el Callao, Feb-Jun 2023: "
                     "único dato de tráfico portuario posterior a 2017 "
                     "disponible en datos abiertos sin Ley 27806."),
        ("Fuente", "MTC/APN — datosabiertos.gob.pe, reportes mensuales "
                     "'Programación diaria de movimiento de naves' "
                     "(reporte-Febrero..Junio2023.xls), cache en "
                     "data/icrpp/open_csv/."),
        ("Cobertura", "5 de 12 meses (Feb-Jun 2023). Enero, Julio y "
                        "Agosto 2023 NO existen en el portal (HTTP 404). "
                        "Set-Dic 2023 existen solo como extractos de UN "
                        "SOLO DÍA (registrados en la serie histórica como "
                        "naves_extracto_diario_2023); no son serie mensual."),
        ("Programación ≠ recepción", "El reporte es la PROGRAMACIÓN "
                                       "diaria (DUE asignados), no la "
                                       "recepción efectiva; puede diferir "
                                       "del movimiento real (naves "
                                       "reprogramadas, canceladas o no "
                                       "contadas en naves_recibidas 2010-2017)."),
        ("DUE", "Numeración CLL-2023-XXXXX acumulada en el año "
                  "(no se reinicia por mes). 'cobertura_vs_nuevos' = "
                  "naves reportadas / (max DUE del mes - max DUE del "
                  "mes anterior): 86-97% en Mar-Jun. Febrero es S/D "
                  "por falta del reporte de Enero. Una cobertura <100% "
                  "puede indicar DUEs asignados a movimientos no "
                  "incluidos en este reporte (p. ej. partidas) u "
                  "omisiones; verificar con APN."),
        ("Procedencia", "Clasificada contra lista de puertos peruanos "
                          "conocidos. 'LA LIBERTAD' y 'VENTANAS' se "
                          "clasifican como EXTRANJERO (puertos de "
                          "Ecuador; en Perú los puertos homónimos de "
                          "región no existen como tal). 'INTERNATIONAL/"
                          "NATIONAL WATERS' = aguas internacionales."),
        ("Lectura RLAC", "Share TRAMPA vs LINEA y banderas de "
                           "conveniencia se reportan como señales de "
                           "riesgo TBML (FATF/GAFILAT: envío tramp e "
                           "irregular asociado a mayor riesgo). Son "
                           "señales de exposición, NO evidencia de "
                           "ilícito ni calificación de cumplimiento."),
        ("Estadía", "H.LP - H.ARR en horas, parseada del formato 'h:mm' "
                      "del reporte. Estadía corta puede indicar "
                      "operación eficiente o menor ventana de control; "
                      "contexto requerido antes de interpretar."),
        ("NO PAGA", "Filas con OBS 'NO PAGA. PUERTO INTERMEDIO PERUANO' "
                      "(y similares): naves en tránsito que no operan "
                      "comercialmente en el Callao; se cuentan aparte."),
        ("Tendencia", "naves_recibidas 2010-2017 (anual/12) vs "
                        "promedio mensual Feb-Jun 2023. Comparación "
                        "indicativa: bases conceptualmente distintas "
                        "(recepción efectiva vs programación)."),
        ("Advertencia", "Solo Callao; no hay equivalente para Paita u "
                          "otros puertos en 2023. No extrapolar al "
                          "total nacional."),
    ], columns=["Campo", "Detalle"])

    with pd.ExcelWriter(OUT_XLSX, engine="openpyxl") as xw:
        lectura.to_excel(xw, sheet_name="LECTURA", index=False)
        mensual.to_excel(xw, sheet_name="MENSUAL", index=False)
        tipo_mes.to_excel(xw, sheet_name="TIPO_NAVE")
        cond_mes.to_excel(xw, sheet_name="CONDICION_TRAMPA_LINEA")
        motivo_mes.to_excel(xw, sheet_name="MOTIVO_ESCALA")
        proc.to_excel(xw, sheet_name="PROCEDENCIA")
        bandera.to_excel(xw, sheet_name="BANDERA")
        due_seq.to_excel(xw, sheet_name="DUE_SECUENCIA", index=False)
        tendencia.to_excel(xw, sheet_name="TENDENCIA", index=False)
        df.to_excel(xw, sheet_name="DETALLE", index=False)

    print("filas detalle:", len(df))
    print(mensual[["mes", "n_naves", "share_trampa",
                     "share_procedencia_peru",
                     "share_procedencia_extranjera",
                     "share_banderas_conveniencia",
                     "estadia_media_h"]].to_string(index=False))
    print()
    print("DUE (cobertura vs numeracion acumulada):")
    print(due_seq[["mes", "due_max", "n_reportadas",
                     "due_nuevos_mes", "cobertura_vs_nuevos"]]
          .to_string(index=False))
    print()
    print("TENDENCIA naves/mes:")
    print(tendencia.to_string(index=False))
    print()
    print("CONDICION:")
    print(cond_mes.to_string())
    print("salida:", OUT_XLSX)


if __name__ == "__main__":
    main()
