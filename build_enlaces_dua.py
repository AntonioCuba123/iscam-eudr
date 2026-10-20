# -*- coding: utf-8 -*-
"""Excel de enlaces ADUANET para buscar DUAs (2024 -> a la fecha). Sin consultas en vivo:
el patron de URL esta validado contra aduanet.gob.pe y contra jsDetalleDUA de la pagina
resumen (documentado en el propio HTML del sitio).
"""
import pandas as pd

ANIOS = [2024, 2025, 2026]
OFFSET = 1992


def url_resumen(ruc, anio):
    """Nivel 1: resumen de exportaciones por RUC y año (todas las aduanas y meses).
    Patron validado en vivo (devuelve filas) y coincide con el conector del proyecto
    exportaciones-fob-connector.ts de apps/identidad-fiscal."""
    return ("http://www.aduanet.gob.pe/cl-ad-itconsultadwh/ieITS01Alias"
            "?accion=buscarListadoImpoExpo&CG_consulta=1&indOCE=false&vig001278=F"
            "&strMenu=-&CG_tipo=4&CG_Codigo=" + ruc + "&CG_DNombre="
            "&CG_Aduana=999&CG_Ano=" + str(anio - OFFSET) + "&CG_Mes=00&CG_regimen=40")


def url_duas(ruc, anio, mes, adu, agente, pais):
    """Nivel 2: listado de DUAs de una combinacion. Copia literal de la funcion
    jsDetalleDUA que sirve la propia pagina resumen de ADUANET:
        ...&CG_ruc=" + tipNroDoc + "&CG_aduana=" + codAduana + "&CG_agente=" + codAgente
        + "&CG_mes=" + codMes + "&CG_anio=" + codAnio + "&CG_pais=" + codPais
    La aduana va con 3 digitos: ADUANET muestra 046 (Paita), no 46."""
    return ("http://www.aduanet.gob.pe/cl-ad-itconsultadwh/ieITS01Alias"
            "?accion=buscarListadoDuas&CG_consulta=1&CG_regimen=40&CG_ruc=4" + ruc +
            "&CG_aduana=" + str(adu).zfill(3) + "&CG_agente=" + str(agente) +
            "&CG_mes=" + str(int(mes)) + "&CG_anio=" + str(anio) + "&CG_pais=" + str(pais))


def url_detalle(adu, anio, num):
    return ("http://www.aduanet.gob.pe/servlet/SgCDUI2?option=una&n=40"
            "&codaduana=" + str(adu) + "&anoprese=" + str(anio) +
            "&numecorre=" + str(num).zfill(6))


# ---------------------------------------------------------------- datos
ex = pd.read_csv(r"C:\Users\acuba\AppData\Local\Temp\kilo\_exp76.csv", dtype=str)
rucs174 = pd.read_excel(
    r"C:\Users\acuba\eudrperu\BASE CAFE CACAO 174\CONSULTA MASIVA RUC 10.10.26\ruces_lotes_174.xlsx")
rucs174["RUC"] = rucs174["RUC"].astype(str).str.zfill(11)
S174 = set(rucs174["RUC"])

ex = ex[ex["ruc"].isin(S174)].copy()
ex["act"] = ex["actividad"].str.strip()
ex = ex.sort_values(["act", "ruc"]).reset_index(drop=True)
RAZON = dict(zip(ex["ruc"], ex["razon_social"].astype(str)))
N = len(ex)
print("RUC a cubrir:", N)

fob = pd.read_csv(r"C:\Users\acuba\eudrperu\ficharucsunat\ruc-exportaciones-fob.txt",
                  sep="\t", dtype={"ruc": str})
fob = fob[fob["anio"] >= 2024]
dua = pd.read_csv(r"C:\Users\acuba\eudrperu\ficharucsunat\dua_canal_final.csv", dtype={"ruc": str})
dua = dua[dua["anio"] >= 2024]
duas_por_ruc = dua.groupby("ruc").size().to_dict()
fob_rucs, dua_rucs = set(fob["ruc"]), set(dua["ruc"])

# ---------------------------------------------------------------- hoja 1
r1 = []
for _, r in ex.iterrows():
    ruc = r["ruc"]
    ncombo = len(fob[fob["ruc"] == ruc])
    for a in ANIOS:
        previo = len(fob[(fob["ruc"] == ruc) & (fob["anio"] == a)])
        nota = []
        if ruc in fob_rucs:
            nota.append("FOB previo: %d combos (ver hoja 2)" % ncombo)
        else:
            nota.append("SIN datos previos: arrancar aqui para descubrir adu/agente/mes/país")
        if ruc in dua_rucs:
            nota.append("%d DUAs ya capturadas" % duas_por_ruc.get(ruc, 0))
        if a == 2026:
            nota.append("año en curso (hasta octubre)")
        if a == 2024:
            nota.append("año de partida EUDR")
        r1.append({
            "RUC": ruc, "Razón social": RAZON[ruc], "Clasificación SUNAT": r["act"],
            "Año": a, "CG_Ano (= año − 1992)": a - OFFSET,
            "ENLACE ADUANET — resumen del año": url_resumen(ruc, a),
            "Estado del enlace": "PATRÓN VALIDADO (respondió en prueba en vivo)",
            "Filas FOB previas ese año": previo,
            "Combos conocidos": ncombo if ruc in fob_rucs else 0,
            "Estado búsqueda": "PENDIENTE",
            "N° operaciones FOB": "", "N° DUAs": "", "FOB USD del año": "",
            "Países destino": "", "Observaciones": " | ".join(nota),
        })
df1 = pd.DataFrame(r1)

# ---------------------------------------------------------------- hoja 2
r2 = []
for _, c in fob.iterrows():
    ruc = c["ruc"]
    if ruc not in RAZON:
        continue
    r2.append({
        "RUC": ruc, "Razón social": RAZON[ruc], "Año": int(c["anio"]), "Mes": int(c["mes"]),
        "Aduana (3 dígitos)": str(c["aduana_codigo"]).zfill(3),
        "Agente": c["agente_codigo"], "País": c["pais_codigo"],
        "ENLACE ADUANET — listado de DUAs": url_duas(ruc, c["anio"], c["mes"],
                                                    c["aduana_codigo"], c["agente_codigo"],
                                                    c["pais_codigo"]),
        "Estado del enlace": "CANDIDATO — confirmar contra el resumen del año",
        "FOB USD previo del combo": c["fob_usd"],
        "Estado búsqueda": "PENDIENTE", "N° DUAs": "", "Canal(es)": "", "Observaciones": "",
    })
df2 = pd.DataFrame(r2).sort_values(["RUC", "Año", "Mes", "País"]).reset_index(drop=True)

# ---------------------------------------------------------------- hoja 3
r3 = []
for _, d in dua.iterrows():
    if d["ruc"] not in RAZON:
        continue
    r3.append({"RUC": d["ruc"], "Razón social": RAZON[d["ruc"]], "Año DUA": int(d["anio"]),
               "N° DUA": str(d["dua_numero"]), "Fecha embarque": d["fecha_embarque"],
               "Canal": d["canal"], "Aduana": d["aduana_codigo"], "Agente": d["agente_codigo"],
               "País": d["pais_codigo"],
               "ENLACE detalle (SgCDUI2 — pide captcha)": d["url_detalle"]})
df3 = pd.DataFrame(r3).sort_values(["RUC", "Año DUA", "N° DUA"]).reset_index(drop=True)

# ---------------------------------------------------------------- hoja 4
r4 = []
for _, r in ex.iterrows():
    ruc = r["ruc"]
    tiene_fob = ruc in fob_rucs
    r4.append({
        "RUC": ruc, "Razón social": RAZON[ruc], "Clasificación SUNAT": r["act"],
        "¿FOB previo?": "SI" if tiene_fob else "NO",
        "¿DUAs previas?": "SI" if ruc in dua_rucs else "NO",
        "Combos conocidos": len(fob[fob["ruc"] == ruc]) if tiene_fob else 0,
        "DUAs en base": duas_por_ruc.get(ruc, 0),
        "Ruta de búsqueda": ("Nivel 1 y nivel 2 (combos ya conocidos)" if tiene_fob
                             else "Nivel 1 primero: descubrir adu/agente/mes/país"),
        "Enlaces nivel 1": len(ANIOS),
        "Enlaces nivel 2": len(df2[df2["RUC"] == ruc]),
        "Enlaces nivel 3": len(df3[df3["RUC"] == ruc]),
    })
df4 = pd.DataFrame(r4).sort_values(["Ruta de búsqueda", "RUC"]).reset_index(drop=True)

# ---------------------------------------------------------------- hoja 0
guia = [
    ("GUÍA DE BÚSQUEDA DE DUAs — ADUANET SUNAT", ""),
    ("", ""),
    ("Objetivo", "Cubrir los movimientos de exportación (DUAs) desde 2024 hasta la fecha de los "
                 "%d RUC clasificados como EXPORTADOR / IMPORTADOR-EXPORTADOR dentro de la base "
                 "de 174 organizaciones cafetaleras y cacaoteras." % N),
    ("Armado", "11 de octubre de 2026"),
    ("Fuente", "http://www.aduanet.gob.pe/cl-ad-itconsultadwh/ieITS01Alias — Consulta por "
               "Importador/Exportador, régimen 40 = exportación definitiva"),
    ("Total de enlaces a cubrir", "%d (nivel 1: %d · nivel 2: %d · nivel 3: %d)"
     % (len(df1) + len(df2) + len(df3), len(df1), len(df2), len(df3))),
    ("", ""),
    ("NIVEL 1 — Resumen por RUC y año (sin captcha)", ""),
    ("Qué da", "Todas las operaciones de exportación del RUC en el año: mes, aduana, agente, "
               "país destino y FOB en dólares. Es el punto de entrada y el que responde "
               "directamente a 'movimientos de exportación'."),
    ("Parámetro clave", "CG_Ano = año real − 1992  →  2024 = 32 · 2025 = 33 · 2026 = 34"),
    ("Otros parámetros", "CG_Aduana=999 (todas las aduanas) · CG_Mes=00 (todo el año) · "
                         "CG_regimen=40 (exportación definitiva) · CG_tipo=4 (RUC)"),
    ("Validación", "Probado en vivo: devuelve filas y enlaces jsDetalleDUA. Coincide con el "
                   "conector del proyecto apps/identidad-fiscal/api/src/ingest/"
                   "exportaciones-fob-connector.ts"),
    ("Hoja", "1. Resumen por año  —  %d enlaces (%d RUC × %d años)" % (len(df1), N, len(ANIOS))),
    ("", ""),
    ("NIVEL 2 — Listado de DUAs (sin captcha)", ""),
    ("Qué da", "Las DUAs de una combinación RUC + año + mes + aduana + agente + país, con fecha "
               "de embarque y canal (verde / rojo / naranja). El enlace al detalle sale del "
               "onclick de jsDetalleDUA en la página resumen."),
    ("Corrección aplicada", "ADUANET usa la aduana con 3 dígitos: 046 (Paita), no 46. "
                            "Los enlaces de esta hoja ya van corregidos."),
    ("Cuidado con el año", "El año del combo sale del resumen (año de embarque). La DUA puede "
                           "tener anoprese del año anterior: en la base capturada, 1662 de 1704 "
                           "coinciden y 42 tienen un año de diferencia."),
    ("Cuidado con el mes", "El mes del FOB (embarque) puede no coincidir con el mes que lista "
                           "ADUANET: confirmar contra el resumen antes de dar el combo por bueno."),
    ("Hoja", "2. Listado DUAs  —  %d enlaces candidatos" % len(df2)),
    ("", ""),
    ("HUECO DE COBERTURA 2024", "La Hoja 2 solo trae 2025 y 2026 porque el archivo de FOB "
                                "previo (ficharucsunat/ruc-exportaciones-fob.txt) arranca en "
                                "2025. Las DUAs de 2024 ya capturadas están en la Hoja 3 "
                                "(%d enlaces), y el resumen de 2024 se cubre con la Hoja 1. "
                                "Si se requiere el listado de DUAs de 2024 combo por combo, "
                                "hay que construir esos candidatos leyendo el resumen de 2024."
                                % len(df3)),
    ("", ""),
    ("NIVEL 3 — Detalle de la DUA (sí pide captcha)", ""),
    ("Qué da", "Ficha completa: partida arancelaria, bultos, peso neto/bruto, FOB, valor cláusula."),
    ("Limitación", "SgCDUI2 exige captcha: no se puede automatizar (nota del 23/09/2026)."),
    ("Hoja", "3. DUAs ya capturadas  —  %d enlaces ya resueltos en el proyecto" % len(df3)),
    ("", ""),
    ("ORDEN DE TRABAJO", ""),
    ("Paso 1", "Hoja 1: abrir el resumen del año de cada RUC. Anotar N° operaciones FOB y FOB USD."),
    ("Paso 2", "Leer en ese resumen los combos aduana/agente/mes/país reales y usarlos en la "
               "Hoja 2. Los candidatos pre-armados son un atajo, no una verdad."),
    ("Paso 3", "Solo si hace falta la ficha completa, Hoja 3 (resolver el captcha a mano)."),
    ("", ""),
    ("RUC SIN DATOS PREVIOS", "%d de %d RUC no tienen FOB ni DUAs previas: arrancan obligados "
                              "en el Nivel 1." % (int((df4['¿FOB previo?'] == 'NO').sum()), N)),
    ("RUC CON DATOS PREVIOS", "%d de %d tienen combos ya conocidos: pueden ir directo al Nivel 2."
     % (int((df4['¿FOB previo?'] == 'SI').sum()), N)),
    ("2026 parcial", "El año en curso llega hasta octubre de 2026."),
    ("Aduanas", "118 = Marítima del Callao · 046 = Paita · 235 = Aérea"),
    ("Columnas a llenar", "Estado búsqueda · N° operaciones FOB · N° DUAs · FOB USD · "
                          "Países destino · Observaciones"),
    ("", ""),
    ("FUERA DE LA BASE 174", "20140181405 CAC La Florida (exportador, no integra las 174) · "
                             "20600920597 Yuraq Yaku (homónimo de Ayacucho, entidad distinta)"),
]
dfg = pd.DataFrame(guia, columns=["Campo", "Detalle"])

# ---------------------------------------------------------------- escritura
out = r"C:\Users\acuba\eudrperu\BASE CAFE CACAO 174\CONSULTA MASIVA RUC 10.10.26\ENLACES_BUSQUEDA_DUA_2024-2026.xlsx"
hojas = [("GUÍA", dfg), ("1. Resumen por año", df1), ("2. Listado DUAs", df2),
         ("3. DUAs ya capturadas", df3), ("4. Estado por RUC", df4)]

from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

with pd.ExcelWriter(out, engine="openpyxl") as w:
    for nombre, d in hojas:
        d.to_excel(w, sheet_name=nombre, index=False)
        ws = w.sheets[nombre]
        hf = PatternFill("solid", fgColor="1F4E78")
        azul = PatternFill("solid", fgColor="DDEBF7")
        thin = Side(style="thin", color="BFBFBF")
        for c in ws[1]:
            c.font = Font(bold=True, color="FFFFFF", size=10)
            c.fill = hf
            c.alignment = Alignment(vertical="center", horizontal="center", wrap_text=True)
        ws.row_dimensions[1].height = 36
        for i, col in enumerate(d.columns, start=1):
            L = get_column_letter(i)
            s = str(col)
            if "ENLACE" in s:
                ancho = 64
            elif "Razón" in s or "Detalle" in s or "Ruta" in s or "Observ" in s:
                ancho = 46
            elif "Estado" in s or "Clasific" in s:
                ancho = 28
            else:
                ancho = 16
            ws.column_dimensions[L].width = ancho
        cols_link = [i for i, c in enumerate(d.columns, start=1) if "ENLACE" in str(c)]
        cols_est = [i for i, c in enumerate(d.columns, start=1)
                    if str(c) in ("Estado del enlace", "Estado búsqueda")]
        for row in ws.iter_rows(min_row=2):
            for i in cols_link:
                cell = row[i - 1]
                if cell.value and str(cell.value).startswith("http"):
                    cell.hyperlink = str(cell.value)
                    cell.font = Font(color="0563C1", underline="single", size=9)
            for i in cols_est:
                cell = row[i - 1]
                v = str(cell.value or "")
                if v.startswith("PATRÓN VALIDADO"):
                    cell.fill = azul
                    cell.font = Font(bold=True, color="1F4E78", size=9)
        for row in ws.iter_rows(min_row=2):
            for c in row:
                c.alignment = Alignment(vertical="top", wrap_text=True)
                c.border = Border(left=thin, right=thin, top=thin, bottom=thin)
        ws.freeze_panes = None if nombre == "GUÍA" else "C2"
        ws.auto_filter.ref = None if nombre == "GUÍA" else ws.dimensions
        if nombre == "GUÍA":
            ws.column_dimensions["A"].width = 40
            ws.column_dimensions["B"].width = 100
            for row in ws.iter_rows(min_row=1):
                v = row[0].value
                if v and str(v).isupper() and len(str(v)) > 5:
                    row[0].font = Font(bold=True, color="1F4E78", size=11)

print("OK ->", out)
for nombre, d in hojas:
    print("  %-22s %5d filas x %2d cols" % ("'" + nombre + "'", len(d), len(d.columns)))
print()
print("Nivel 1 (resumen año) :", len(df1), "enlaces")
print("Nivel 2 (listado DUA) :", len(df2), "enlaces")
print("Nivel 3 (detalle)     :", len(df3), "enlaces")
print("TOTAL                 :", len(df1) + len(df2) + len(df3))
print("RUC con FOB previo    :", int((df4['¿FOB previo?'] == 'SI').sum()), "/", N)
print("RUC sin FOB previo    :", int((df4['¿FOB previo?'] == 'NO').sum()), "/", N)
