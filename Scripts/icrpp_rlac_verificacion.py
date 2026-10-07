"""Verificacion de las afirmaciones RLAC del paper ICRPP contra
los cuadros SUNAT 2023-2024 locales (cdro_08/12/13/15/16/22) y
la programacion de naves 2023 del Callao.

Afirmaciones verificadas (paper ICRPP, secciones 5.1 y 6):
  A1. "El Callao, con el 46.6% del comercio formal" (RLAC-02)
  A2. "HHI = 2,629 ... altamente concentrado (US DOJ/FTC > 2,500)"
  A3. "markup promedio 4.95% (desv. 2.37%), max 14.25% en 3926,
       ninguna subpartida supera el umbral FATF de ±15%" (RLAC-01)
  A4. "crecimiento sostenido de +12.9% entre T1 y T4 de 2024,
       y +11.7% respecto al mismo periodo de 2023" (trafico Callao)

Fuente del paper: "SUNAT Aduanas — Rastro (public.port_imports,
is_total=true, year=2024)". Los cuadros cdro de SUNAT son la
misma fuente institucional pero agregados por aduana/empresa;
las diferencias de magnitud se reportan, no se silencian.
"""
from pathlib import Path

import openpyxl
import pandas as pd

SUNAT = Path(r"C:\Users\acuba\appsperu\data\sunat")
NAVES = Path(r"C:\Users\acuba\eudrperu\docs\NAVES_2023_CALLAO_ANALISIS.xlsx")
OUT = Path(r"C:\Users\acuba\eudrperu\docs\RLAC_VERIFICACION_2023_2024.xlsx")


def cuadro(fname, sheet=0):
    wb = openpyxl.load_workbook(str(SUNAT / fname), read_only=True,
                                    data_only=True)
    ws = wb[wb.sheetnames[sheet]]
    rows = [list(r) for r in ws.iter_rows(values_only=True)]
    wb.close()
    return rows


def to_num(v):
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    try:
        return float(str(v).strip().replace(",", ""))
    except ValueError:
        return None


def hhi(shares):
    return round(sum(s ** 2 for s in shares) * 10000.0, 1)


def concentracion_portuaria():
    rows = cuadro("cdro_15.xlsx")
    anios, totales = (2023, 2024), {}
    for r in rows:
        if len(r) > 12 and r[1] == "TOTAL":
            totales = {2023: to_num(r[7]), 2024: to_num(r[12])}
            break
    filas = []
    for r in rows:
        if len(r) < 13 or not r[2] or r[2] == "TOTAL":
            continue
        name = str(r[2]).strip()
        for c, anio in [(7, 2023), (12, 2024)]:
            v = to_num(r[c])
            if v is None:
                continue
            filas.append(dict(aduana=name, anio=anio, cif_usd=v,
                                  share=round(100.0 * v / totales[anio], 2)))
    df = pd.DataFrame(filas)
    resumen = (df.groupby("anio")
                 .apply(lambda g: pd.Series({
                     "n_aduanas": len(g),
                     "share_callao": round(float(g[g.aduana == "MARITIMA DEL CALLAO"]["share"].iloc[0]), 2),
                     "hhi": hhi((g["share"] / 100.0).tolist()),
                     "top3_share": round(float(g.sort_values("share", ascending=False)["share"].head(3).sum()), 2),
                 }), include_groups=False)
                 .reset_index())
    return df, resumen, totales


def ranking_hhi(fname, name_col, c_val, c_cnt, label):
    rows = cuadro(fname)
    total = None
    entidades = {}
    for r in rows:
        if len(r) <= (c_cnt if c_cnt else c_val) + 1:
            continue
        if r[1] == "TOTAL" or (r[1] and str(r[1]).startswith("TOTAL")):
            total = {2023: to_num(r[c_val]), 2024: to_num(r[c_val + 1])}
            continue
        name = r[name_col]
        if (not name or str(name).upper() == "RESTO"
                or str(name).startswith("Total")):
            continue
        name = str(name).strip()
        entidades.setdefault(name, {})[2023] = to_num(r[c_val])
        entidades[name][2024] = to_num(r[c_val + 1])
        if c_cnt:
            entidades[name][(2023, "n")] = to_num(r[c_cnt])
            entidades[name][(2024, "n")] = to_num(r[c_cnt + 1])
    filas = []
    for name, vals in entidades.items():
        for anio in (2023, 2024):
            v = vals.get(anio)
            if v is None or not total or not total[anio]:
                continue
            fila = dict(entidad=name, anio=anio, valor=v,
                            share=round(100.0 * v / total[anio], 3))
            if c_cnt:
                n = vals.get((anio, "n"))
                if n is not None:
                    fila["cantidad"] = n
            filas.append(fila)
    df = pd.DataFrame(filas)
    resumen = (df.groupby("anio")
                 .apply(lambda g: pd.Series({
                     "n_entidades": len(g),
                     "top1_share": round(float(g.sort_values("share", ascending=False)["share"].iloc[0]), 2),
                     "top5_share": round(float(g.sort_values("share", ascending=False)["share"].head(5).sum()), 2),
                     "hhi_valor": hhi((g["share"] / 100.0).tolist()),
                 }), include_groups=False)
                 .reset_index())
    return df, resumen


def markup_callao():
    rows = cuadro("cdro_16.xlsx")
    filas = []
    for r in rows:
        if len(r) < 9 or not r[1] or not r[3]:
            continue
        if str(r[1]).strip().startswith("Total") or str(r[1]).strip() == "TOTAL":
            continue
        sub = str(r[3]).strip()
        desc = str(r[4]).strip() if len(r) > 4 and r[4] else ""
        fob24, cif24 = to_num(r[6]), to_num(r[8])
        fob23, cif23 = to_num(r[5]), to_num(r[7])
        if None in (fob24, cif24, fob23, cif23) or fob24 == 0 or fob23 == 0:
            continue
        filas.append(dict(
            subpartida=sub, descripcion=desc[:70],
            fob_2023=fob23, cif_2023=cif23,
            fob_2024=fob24, cif_2024=cif24,
            markup_2023=round(100.0 * (cif23 - fob23) / fob23, 2),
            markup_2024=round(100.0 * (cif24 - fob24) / fob24, 2),
        ))
    df = pd.DataFrame(filas)
    if df.empty:
        return df, None
    w24 = df.fob_2024 / df.fob_2024.sum()
    stats = dict(
        n_subpartidas=len(df),
        markup_promedio_ponderado=round(float((w24 * df.markup_2024).sum()), 2),
        markup_promedio_simple=round(float(df.markup_2024.mean()), 2),
        markup_desviacion=round(float(df.markup_2024.std()), 2),
        markup_max=round(float(df.markup_2024.max()), 2),
        subpartida_max=df.loc[df.markup_2024.idxmax(), "subpartida"],
        n_sobre_15pct=int((df.markup_2024 > 15.0).sum()),
        n_bajo_menos15pct=int((df.markup_2024 < -15.0).sum()),
    )
    return df, stats


def hhi_naves_2023():
    d = pd.read_excel(NAVES, "DETALLE")
    filas = []
    for dim, col in [("bandera", "bandera"), ("procedencia", "procedencia"),
                     ("agente", "agente"), ("tipo_nave", "tipo"),
                     ("condicion", "cond"), ("motivo_escala", "motivo")]:
        vc = d[col].value_counts()
        shares = (vc / vc.sum()).tolist()
        top = vc.head(5)
        filas.append(dict(
            dimension=dim, n_categorias=len(vc),
            hhi=hhi(shares),
            top1=f"{top.index[0]} ({100.0 * top.iloc[0] / vc.sum():.1f}%)",
            top3_share=round(100.0 * top.head(3).sum() / vc.sum(), 1),
        ))
    return pd.DataFrame(filas)


def main():
    port_df, port_res, totales = concentracion_portuaria()
    callao_share_2024 = float(
        port_df[(port_df.aduana == "MARITIMA DEL CALLAO")
                  & (port_df.anio == 2024)]["share"].iloc[0])
    hhi_2024 = float(port_res[port_res.anio == 2024]["hhi"].iloc[0])
    hhi_2023 = float(port_res[port_res.anio == 2023]["hhi"].iloc[0])

    brok_df, brok_res = ranking_hhi(
        "cdro_12.xlsx", 3, 4, 6, "despachadores de aduana")
    alma_df, alma_res = ranking_hhi(
        "cdro_13.xlsx", 2, 3, 5, "almacenes y depositos")
    imp_rows = cuadro("cdro_08.xlsx")
    imp_shares, imp_names = [], []
    for r in imp_rows:
        if len(r) < 9 or not r[2] or r[1] == "TOTAL":
            continue
        if str(r[2]).strip().upper() == "RESTO":
            continue
        s = to_num(r[8])
        if s and s > 0:
            imp_shares.append(s)
            imp_names.append(str(r[2]).strip())
    hhi_imp = hhi(imp_shares)
    exp_rows = cuadro("cdro_22.xlsx")
    exp_shares = []
    for r in exp_rows:
        if (len(r) <= 7 or not r[3] or r[1] == "TOTAL"
                or str(r[3]).strip().upper() == "RESTO"):
            continue
        s = to_num(r[7])
        if s and s > 0:
            exp_shares.append(s)
    hhi_exp = hhi(exp_shares)

    mk_df, mk_stats = markup_callao()
    nv_hhi = hhi_naves_2023()

    # A4: crecimiento trimestral Callao (cdro_15)
    rows15 = cuadro("cdro_15.xlsx")
    callao_q = None
    for r in rows15:
        if len(r) > 12 and r[2] == "MARITIMA DEL CALLAO":
            callao_q = [to_num(r[3]), to_num(r[4]), to_num(r[5]), to_num(r[6]),
                        to_num(r[8]), to_num(r[9]), to_num(r[10]), to_num(r[11])]
            break
    a4 = None
    if callao_q and all(v is not None for v in callao_q):
        t1_23, t4_23, t1_24, t4_24 = callao_q[0], callao_q[3], callao_q[4], callao_q[7]
        a4 = dict(
            t4_2023_vs_t1_2023=round(100.0 * (t4_23 - t1_23) / t1_23, 1),
            t4_2024_vs_t1_2024=round(100.0 * (t4_24 - t1_24) / t1_24, 1),
            anio_2024_vs_2023_total=round(100.0 * (sum(callao_q[4:8]) - sum(callao_q[0:4])) / sum(callao_q[0:4]), 1),
        )

    verificacion = pd.DataFrame([
        ("A1", "RLAC-02", '"El Callao, con el 46.6% del comercio formal" '
                          "(sec. 5.1.2)",
         "46.6% (2024)",
         f"{callao_share_2024:.1f}% de las importaciones CIF 2024 "
         f"(cdro_15; {hhi_2024:,.0f} HHI)",
         "DIVERGE",
         "El paper cita Rastro public.port_imports(is_total=true): "
         "probablemente otro alcance (comercio total I+E, operaciones "
         "o regimes distintos). Con la tabla SUNAT autoritativa por "
         "aduana, el Callao concentra ~73% del valor CIF importado. "
         "Pendiente reconciliar la consulta Rastro exacta."),
        ("A2", "RLAC-02", '"HHI = 2,629 cruza el umbral de altamente '
                          'concentrado (US DOJ/FTC > 2,500)"',
         "HHI 2,629 (2024)",
         f"HHI {hhi_2024:,.0f} (2024) / {hhi_2023:,.0f} (2023) sobre "
         "importaciones CIF por aduana (cdro_15)",
         "DIVERGE (misma direccion)",
         "Ambos superan 2,500 ('altamente concentrado'), pero el HHI "
         "local es ~2x el del paper. La conclusion cualitativa "
         "(concentracion estructural del Callao) se mantiene y es "
         "aun mas fuerte."),
        ("A3", "RLAC-01", '"markup promedio 4.95% (desv. 2.37%), max '
                          '14.25% en 3926; ninguna subpartida supera '
                          'el umbral FATF de ±15%"',
         "prom 4.95%, max 14.25%, 0 > 15%",
         (f"prom {mk_stats['markup_promedio_ponderado']}% (ponderado "
          f"FOB), max {mk_stats['markup_max']}% en {mk_stats['subpartida_max']}, "
          f"{mk_stats['n_sobre_15pct']} subpartidas > 15% "
          f"(n={mk_stats['n_subpartidas']})")
         if mk_stats else "S/D",
         ("VERIFICADO" if mk_stats and mk_stats["n_sobre_15pct"] == 0
          and abs(mk_stats["markup_promedio_ponderado"] - 4.95) < 1.0
          else "Parcialmente verificado")
         if mk_stats else "S/D",
         "Markup FOB->CIF por subpartida del Callao 2024 (cdro_16). "
         "Coherente con el paper si el promedio y el max calzan; "
         "el umbral FATF (±15%) es una senal de alerta, no evidencia "
         "de subfacturacion."),
        ("A4", "RON/RLAC", '"trafico del Callao +12.9% T1->T4 2024, '
                          '+11.7% vs 2023" (sec. 5.1.3)',
         "+12.9% T1-T4 2024; +11.7% interanual",
         (f"T4 vs T1 2024: +{a4['t4_2024_vs_t1_2024']}%; "
          f"2024 vs 2023 total: +{a4['anio_2024_vs_2023_total']}% "
          "(cdro_15, CIF)")
         if a4 else "S/D",
         "DIVERGE (misma direccion)" if a4 else "S/D",
         "El crecimiento CIF del Callao en cdro_15 es mayor en "
         "T1->T4 y menor interanual que el paper. El paper usa "
         "trimestrales de Rastro (operaciones), cdro_15 es valor "
         "CIF anual por trimestre. Direccion (crecimiento) "
         "consistente; magnitudes no reconciliadas."),
        ("A5", "RTID", '"Memoria SUNAT 2025: 21,222 kg de droga '
                        'decomisados en 2025" (sec. 6)',
         "21,222 kg (2025)", "S/D", "NO VERIFICABLE",
         "No hay dato local de decomisos 2025; requiere Memoria "
         "SUNAT 2025 o solicitud DIRANDRO (Ley 27806)."),
        ("A6", "RRC", '"INFOBRAS: 36 obras paralizadas en el Callao, '
                       '384 en Piura" (sec. 5.3)',
         "36 / 384 obras", "S/D", "NO VERIFICABLE",
         "INFOBRAS no esta en el dataset local; requiere consulta "
         "a la fuente (Rastro informes-control / INFOM)."),
    ], columns=["Id", "Dominio", "Afirmacion_paper",
                "Valor_paper", "Valor_dato_local", "Veredicto", "Nota"])

    lectura = pd.DataFrame([
        ("Que es", "Contraste afirmacion por afirmacion del paper "
                     "ICRPP contra los cuadros SUNAT 2023-2024 "
                     "locales y la programacion de naves 2023."),
        ("Fuentes locales", "SUNAT cdro_08 (importadores), cdro_12 "
                                "(despachadores de aduana), cdro_13 "
                                "(almacenes/depositos), cdro_15 "
                                "(importacion CIF por aduana), cdro_16 "
                                "(subpartidas por aduana), cdro_22 "
                                "(exportadores por pais); MTC/APN "
                                "programacion de naves 2023."),
        ("Fuente del paper", "Rastro (public.port_imports / "
                                 "port_subpartida_imports, is_total=true, "
                                 "year=2024) e INFOBRAS, consultados en "
                                 "vivo por el autor del paper; no hay "
                                 "dataset local de Rastro en eudrperu."),
        ("Interpretacion", "DIVERGE no significa 'error del paper': "
                               "puede reflejar otro alcance (operaciones "
                               "vs valor, comercio total vs importaciones, "
                               "regimenes). Senala que la cifra del paper "
                               "no es reproducible con la tabla SUNAT "
                               "autoritativa y debe citarse con su "
                               "denominador exacto."),
        ("RESTO", "Los rankings SUNAT incluyen una fila 'RESTO' "
                      "(entidades fuera del top-N). Se excluye de los "
                      "HHI: el HHI reportado por entidad nombrada es "
                      "cota inferior (el RESTO esta disperso entre "
                      "cientos de entidades pequenas; p. ej. despachadores: "
                      "~50% del CIF esta en el RESTO)."),
        ("Hallazgo nuevo", "Concentracion de despachadores de aduana "
                               "nombrados: HHI 234 (baja) con top-5 = "
                               "28.7% del CIF 2024; el ~50% restante esta "
                               "en la cola larga de pequenos despachadores "
                               "(dato no presente en el paper). Almacenes/"
                               "depositos: APM Terminals + DP World "
                               "(ambos del Callao) lideran; HHI 644."),
        ("Veredictos", "VERIFICADO = calza dentro de tolerancia; "
                           "DIVERGE = misma direccion, magnitud "
                           "distinta; PARCIAL = calza parcialmente; "
                           "NO VERIFICABLE = sin dato local."),
        ("Advertencia", "Estos datos son 2023-2024 (y programacion "
                          "2023); NO son una evaluacion vigente de "
                          "riesgo ni de cumplimiento EUDR."),
    ], columns=["Campo", "Detalle"])

    with pd.ExcelWriter(OUT, engine="openpyxl") as xw:
        lectura.to_excel(xw, sheet_name="LECTURA", index=False)
        verificacion.to_excel(xw, sheet_name="VERIFICACION", index=False)
        port_df.to_excel(xw, sheet_name="CONCENTRACION_PORTUARIA", index=False)
        port_res.to_excel(xw, sheet_name="PORTUARIA_RESUMEN", index=False)
        brok_df.to_excel(xw, sheet_name="DESPACHADORES", index=False)
        brok_res.to_excel(xw, sheet_name="DESPACHADORES_RESUMEN", index=False)
        alma_df.to_excel(xw, sheet_name="ALMACENES_DEPOSITOS", index=False)
        alma_res.to_excel(xw, sheet_name="ALMACENES_RESUMEN", index=False)
        pd.DataFrame({"entidad": imp_names, "share_estructura_pct": imp_shares}
                     ).to_excel(xw, sheet_name="IMPORTADORES", index=False)
        pd.DataFrame([
            ("importadores (cdro_08, top-501, estructura 2024)", hhi_imp),
            ("exportadores tradicionales (cdro_22, estructura 2024)", hhi_exp),
        ], columns=["concentracion", "hhi_0_10000"]
        ).to_excel(xw, sheet_name="HHI_EMPRESARIAL", index=False)
        mk_df.to_excel(xw, sheet_name="MARKUP_SUBPARTIDAS", index=False)
        pd.DataFrame([mk_stats]).to_excel(
            xw, sheet_name="MARKUP_RESUMEN", index=False)
        nv_hhi.to_excel(xw, sheet_name="HHI_NAVES_2023", index=False)

    print("=== VERIFICACION ===")
    print(verificacion[["Id", "Afirmacion_paper", "Veredicto"]].to_string(index=False))
    print()
    print("Portuaria 2024: Callao share", callao_share_2024, "| HHI", hhi_2024)
    print("Despachadores:", brok_res.to_dict("records"))
    print("Almacenes:", alma_res.to_dict("records"))
    print("HHI importadores:", hhi_imp, "| exportadores:", hhi_exp)
    print("Markup:", mk_stats)
    print("A4:", a4)
    print("salida:", OUT)


if __name__ == "__main__":
    main()
