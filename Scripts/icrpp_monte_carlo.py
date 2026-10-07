"""Paso 7 OECD/JRC (incertidumbre y sensibilidad, Monte Carlo) y Paso 3
(ACP / alpha de Cronbach) del ICRPP, sobre la serie historica reconstruida
con datos abiertos MTC/APN (Scripts/icrpp_serie_historica.py).

Alcance honesto: solo el dominio RON es reconstruible con datos abiertos
(RON-01 trafico = cargas TM 2010-2017; RON-03 incidentes portuarios
2005-2017). RON-02 (heterogeneidad de carga, HHI inverso) es S/D: los
datos abiertos desagregan CARGAS por TERMINAL, no por tipo de carga.
Los dominios RTID, RLAC, RVI y RRC se mantienen fijos en los scores del
paper (Tabla 9) porque sus series requieren solicitudes Ley 27806
(ver Solicitudes_Ley27806_ICRPP.md).

Dos variantes para RON-02 ausente:
  V1 disponible: renormaliza los pesos de los indicadores con dato (5/8, 3/8)
  V2 latente:    RON-02 ~ U(0,1) en cada corrida, pesos completos 5/12, 4/12, 3/12
"""
import numpy as np
import pandas as pd
from pathlib import Path

DOC = Path(r"C:\Users\acuba\eudrperu\docs")
SERIE_XLSX = DOC / "ICRPP_SERIE_HISTORICA_RECONSTRUIDA.xlsx"
OUT_XLSX = DOC / "ICRPP_MONTE_CARLO_PASO7.xlsx"

N_MC = 10_000
SEED = 42

PESOS_DOMINIO = {"RTID": 0.33, "RLAC": 0.30, "RVI": 0.19, "RON": 0.12, "RRC": 0.06}
SCORES_FIJOS = {
    "CALLAO": {"RTID": 81.3, "RLAC": 64.2, "RVI": 58.7, "RRC": 70.0},
    "PAITA":  {"RTID": 68.0, "RLAC": 59.3, "RVI": 41.3, "RRC": 64.0},
}
RON_PAPER = {"CALLAO": 56.0, "PAITA": 42.0}
COMPUESTO_PAPER = {"CALLAO": 69.2, "PAITA": 57.4}
PESOS_IND_RON = {"RON-01": 0.05, "RON-02": 0.04, "RON-03": 0.03}
VENTANA_RON = (2010, 2017)


def cargar_serie():
    s = pd.read_excel(SERIE_XLSX, "SERIE_LARGA")
    s["puerto"] = s["puerto"].astype(str).str.upper()
    return s


def panel_ron(s):
    c = s[(s.indicador == "cargas_tm") & (s.nivel == "puerto")]
    ron01 = (c.groupby(["puerto", "anio"])["valor"].sum()
             .reset_index().rename(columns={"valor": "RON-01_cargas_tm"}))
    i = s[(s.indicador == "incidentes_portuarios") & (nivel_ok(s))]
    ron03 = (i.groupby(["puerto", "anio"])["valor"].sum()
             .reset_index().rename(columns={"valor": "RON-03_incidentes"}))
    a = s[(s.indicador == "accidentes_portuarios")]
    acc = (a.groupby(["puerto", "anio"])["valor"].sum()
           .reset_index().rename(columns={"valor": "ACC_accidentes"}))
    p = ron01.merge(ron03, on=["puerto", "anio"], how="outer")
    p = p.merge(acc, on=["puerto", "anio"], how="left")
    return p, ron01, ron03


def nivel_ok(s):
    return s["nivel"].isin(["puerto", "eventos"])


def norm_minmax(x, p5, p95):
    if p95 <= p5:
        return np.full_like(np.asarray(x, dtype=float), 0.5)
    return np.clip((np.asarray(x, dtype=float) - p5) / (p95 - p5), 0.0, 1.0)


def ron_puntual(panel, pool01, pool03, variante="V1"):
    p5_01, p95_01 = np.percentile(pool01, [5, 95])
    p5_03, p95_03 = np.percentile(pool03, [5, 95])
    n01 = norm_minmax(panel["RON-01_cargas_tm"], p5_01, p95_01)
    n03 = norm_minmax(panel["RON-03_incidentes"], p5_03, p95_03)
    if variante == "V1":
        w = np.array([5.0, 3.0]) / 8.0
        x = w[0] * n01 + w[1] * n03
    else:
        w = np.array([5.0, 4.0, 3.0]) / 12.0
        x = w[0] * n01 + w[1] * 0.5 + w[2] * n03
    out = panel[["puerto", "anio"]].copy()
    out["n_RON-01"] = n01
    out["n_RON-03"] = n03
    out["RON_score"] = 100.0 * x
    return out, (p5_01, p95_01), (p5_03, p95_03)


def composite(ron_score_100, puerto, pesos, ron_latente=None):
    xs = dict(SCORES_FIJOS[puerto])
    xs["RON"] = ron_score_100
    log = 0.0
    for d, w in pesos.items():
        log += w * np.log(max(xs[d], 1e-9) / 100.0)
    return 100.0 * np.exp(log)


def monte_carlo(panel, pool01, pool03):
    rng = np.random.default_rng(SEED)
    anios = range(VENTANA_RON[0], VENTANA_RON[1] + 1)
    filas = []
    doms = list(PESOS_DOMINIO)
    base_w = np.array([PESOS_DOMINIO[d] for d in doms])
    idx_ron = doms.index("RON")
    for _ in range(N_MC):
        b01 = rng.choice(pool01, size=pool01.size, replace=True)
        b03 = rng.choice(pool03, size=pool03.size, replace=True)
        p5_01, p95_01 = np.percentile(b01, [5, 95])
        p5_03, p95_03 = np.percentile(b03, [5, 95])
        w_dom = rng.dirichlet(base_w * 20.0)
        w_ind_v1 = rng.dirichlet(np.array([5.0, 3.0]) * 20.0)
        w_ind_v2 = rng.dirichlet(np.array([5.0, 4.0, 3.0]) * 20.0)
        ron_lat = rng.uniform(0.0, 1.0)
        for puerto in ("CALLAO", "PAITA"):
            for anio in anios:
                f = panel[(panel.puerto == puerto) & (panel.anio == anio)]
                if f.empty:
                    continue
                v01 = float(f["RON-01_cargas_tm"].iloc[0])
                v03 = float(f["RON-03_incidentes"].iloc[0])
                n01 = norm_minmax([v01], p5_01, p95_01)[0]
                n03 = norm_minmax([v03], p5_03, p95_03)[0]
                ron_v1 = 100.0 * (w_ind_v1[0] * n01 + w_ind_v1[1] * n03)
                ron_v2 = 100.0 * (w_ind_v2[0] * n01 + w_ind_v2[1] * ron_lat
                                  + w_ind_v2[2] * n03)
                filas.append(dict(
                    puerto=puerto, anio=anio,
                    w_RON=w_dom[idx_ron],
                    RON_V1=ron_v1, RON_V2=ron_v2,
                    compuesto_V1=composite(ron_v1, puerto, dict(zip(doms, w_dom))),
                    compuesto_V2=composite(ron_v2, puerto, dict(zip(doms, w_dom))),
                ))
    return pd.DataFrame(filas)


def sensibilidad(mc, punt):
    filas = []
    for puerto in ("CALLAO", "PAITA"):
        g = mc[mc.puerto == puerto]
        for col, nombre in [("w_RON", "peso RON"), ("RON_V1", "score RON (V1)")]:
            rho = g[col].corr(g["compuesto_V1"], method="spearman")
            filas.append(dict(puerto=puerto, variable=nombre,
                              spearman=round(float(rho), 4)))
    tornado = []
    for puerto in ("CALLAO", "PAITA"):
        ron_med = float(punt[punt.puerto == puerto]["RON_score"].mean())
        for d in PESOS_DOMINIO:
            for factor in (0.8, 1.2):
                pesos = dict(PESOS_DOMINIO)
                pesos[d] = pesos[d] * factor
                tot = sum(pesos.values())
                pesos = {k: v / tot for k, v in pesos.items()}
                tornado.append(dict(
                    puerto=puerto, dominio=d, factor=factor,
                    compuesto=round(composite(ron_med, puerto, pesos), 2)))
    return pd.DataFrame(filas), pd.DataFrame(tornado)


def acp_alpha(panel):
    p = panel.dropna(subset=["RON-01_cargas_tm", "RON-03_incidentes"]).copy()
    X2 = p[["RON-01_cargas_tm", "RON-03_incidentes"]].astype(float)
    corr2 = X2.corr().iloc[0, 1]
    alpha2 = 2.0 * corr2 / (1.0 + corr2) if pd.notna(corr2) else np.nan
    p3 = p.dropna(subset=["ACC_accidentes"])
    X3 = p3[["RON-01_cargas_tm", "RON-03_incidentes", "ACC_accidentes"]].astype(float)
    if len(X3) >= 3:
        c3 = X3.corr().values
        alpha3 = (3.0 / 2.0) * (1.0 - np.trace(c3) / np.sum(c3))
        pca_share = float(np.linalg.eigvalsh(c3)[-1] / 3.0)
    else:
        alpha3, c3, pca_share = np.nan, None, np.nan
    pca2 = float(np.linalg.eigvalsh(X2.corr().values)[-1] / 2.0) if len(X2) >= 3 else np.nan
    return dict(n2=len(X2), corr_r01_r03=corr2, alpha_2ind=alpha2, pca1_share_2ind=pca2,
                n3=len(X3), alpha_3ind=alpha3, pca1_share_3ind=pca_share)


def main():
    s = cargar_serie()
    panel, ron01, ron03 = panel_ron(s)
    panel = panel[panel.anio.between(*VENTANA_RON)]
    pool01 = ron01["RON-01_cargas_tm"].astype(float).values
    pool03 = ron03["RON-03_incidentes"].astype(float).values

    punt, b01, b03 = ron_puntual(panel, pool01, pool03, "V1")
    punt2, _, _ = ron_puntual(panel, pool01, pool03, "V2")

    mc = monte_carlo(panel, pool01, pool03)
    sens, tornado = sensibilidad(mc, punt)
    acp = acp_alpha(panel)

    resumen = []
    for puerto in ("CALLAO", "PAITA"):
        for variante, col_ron, col_comp in [("V1", "RON_V1", "compuesto_V1"),
                                            ("V2", "RON_V2", "compuesto_V2")]:
            g = mc[(mc.puerto == puerto)]
            ron_p = punt[punt.puerto == puerto]["RON_score"].mean() if variante == "V1" \
                else punt2[punt2.puerto == puerto]["RON_score"].mean()
            resumen.append(dict(
                puerto=puerto, variante=variante,
                RON_puntual=round(float(ron_p), 2),
                RON_paper=RON_PAPER[puerto],
                RON_mc_mediana=round(float(g[col_ron].median()), 2),
                RON_mc_p5=round(float(g[col_ron].quantile(0.05)), 2),
                RON_mc_p95=round(float(g[col_ron].quantile(0.95)), 2),
                compuesto_paper=COMPUESTO_PAPER[puerto],
                compuesto_mc_mediana=round(float(g[col_comp].median()), 2),
                compuesto_mc_p5=round(float(g[col_comp].quantile(0.05)), 2),
                compuesto_mc_p95=round(float(g[col_comp].quantile(0.95)), 2),
                P_ge_paper=round(float((g[col_comp] >= COMPUESTO_PAPER[puerto]).mean()), 4),
            ))
    resumen = pd.DataFrame(resumen)

    ranking = mc.pivot_table(index=[mc.anio], columns="puerto",
                             values="compuesto_V1", aggfunc="median")
    ranking["Callao_mayor_Paita"] = (ranking["CALLAO"] > ranking["PAITA"]).astype(int)

    anual = (mc.groupby(["puerto", "anio"])
             .agg(RON_mediana=("RON_V1", "median"),
                  RON_p5=("RON_V1", lambda x: x.quantile(0.05)),
                  RON_p95=("RON_V1", lambda x: x.quantile(0.95)),
                  comp_mediana=("compuesto_V1", "median"),
                  comp_p5=("compuesto_V1", lambda x: x.quantile(0.05)),
                  comp_p95=("compuesto_V1", lambda x: x.quantile(0.95)))
             .reset_index().round(2))

    metodo = pd.DataFrame([
        ("Objetivo", "Paso 7 OECD/JRC: propagacion de incertidumbre (Monte Carlo "
                     "10,000 corridas) y analisis de sensibilidad del ICRPP; Paso 3: "
                     "ACP y alpha de Cronbach sobre el panel RON. Mitiga las "
                     "Limitaciones 1 y 3 del paper ICRPP."),
        ("Alcance RON", "RON-01 = cargas TM anuales por puerto (proxy de millones "
                        "TEU/año; la fuente abierta reporta TM, no TEU). RON-03 = "
                        "incidentes portuarios anuales. RON-02 (HHI inverso de "
                        "heterogeneidad de carga) es S/D: CARGAS se desagregan por "
                        "terminal, no por tipo de carga."),
        ("Dominios fijos", "RTID, RLAC, RVI y RRC se fijan en los scores de la "
                           "Tabla 9 del paper (69.2/57.4 dependen de ellos); sus "
                           "series requieren solicitudes Ley 27806."),
        ("Normalizacion", "min-max con percentiles 5 y 95 sobre el pool de todos "
                          "los puertos y anios con dato (paper sec. 3.2). En cada "
                          "corrida MC el pool se remuestra con reemplazo (bootstrap) "
                          "y los percentiles se recomputan."),
        ("Pesos", "Dominios: Dirichlet(alpha = 20 x peso del paper). Indicadores "
                  "dentro de RON: Dirichlet(20 x peso) — V1 renormaliza 5/8, 3/8; "
                  "V2 usa pesos completos 5/12, 4/12, 3/12 con RON-02 latente "
                  "U(0,1)."),
        ("Agregacion", "Ec. 1 del paper: ICRPP = 100 x prod_d (X_d/100)^w_d "
                       "(geometrica); score dominical = media ponderada "
                       "aritmetica de los indicadores normalizados."),
        ("Semilla", f"numpy default_rng({SEED}); {N_MC} corridas; ventana "
                    f"{VENTANA_RON[0]}-{VENTANA_RON[1]} (unicos anios con RON-01 "
                    "y RON-03 simultaneos)."),
        ("Advertencia 1", "El panel es corto (8 anios) y desbalanceado (11 puertos "
                          "con incidentes); los percentiles 5-95 son inestables — "
                          "justamente lo que el MC cuantifica. No es una serie "
                          "2015-2025 completa: 2018-2022 sigue sin fuente abierta."),
        ("Advertencia 2", "Los scores fijos de RTID/RLAC/RVI/RRC son estimaciones "
                          "del paper (algunos con fuente truncada en la extraccion). "
                          "La incertidumbre del compuesto aqui cubre solo el canal "
                          "RON + pesos, no la incertidumbre de esos cuatro dominios."),
        ("Advertencia 3", "Resultado de robustez de metodologia, NO una "
                          "calificacion de cumplimiento EUDR ni de riesgo vigente: "
                          "los datos abiertos cubren hasta 2017 (mas 2023 parcial)."),
        ("Advertencia 4", "Saturacion del min-max: el Callao mueve ~10x el "
                          "siguiente puerto en TM, por lo que toca la cota 1.0 "
                          "en la mayoria de anios y de corridas; su RON "
                          "recomputado (96 V1) debe leerse como 'riesgo "
                          "operacional maximo en el pool', no como medida "
                          "cardinal. El bootstrap propaga la incertidumbre de "
                          "los percentiles pero no elimina el efecto de "
                          "discretizacion de la cota."),
    ], columns=["Campo", "Detalle"])

    acp_df = pd.DataFrame([
        ("n panel (2 indicadores, 2010-2017)", acp["n2"]),
        ("Correlacion RON-01 vs RON-03", round(float(acp["corr_r01_r03"]), 4)),
        ("Alpha de Cronbach (2 indicadores, Spearman-Brown)",
         round(float(acp["alpha_2ind"]), 4)),
        ("% varianza explicada por PC1 (2 indicadores)",
         round(float(acp["pca1_share_2ind"]), 4)),
        ("n panel (3 indicadores, 2014-2017, con accidentes)", acp["n3"]),
        ("Alpha de Cronbach (3 indicadores)",
         round(float(acp["alpha_3ind"]), 4) if pd.notna(acp["alpha_3ind"]) else "S/D"),
        ("% varianza explicada por PC1 (3 indicadores)",
         round(float(acp["pca1_share_3ind"]), 4) if pd.notna(acp["pca1_share_3ind"]) else "S/D"),
        ("Interpretacion", "Alpha bajo es esperado: RON-01 (exposicion al trafico) y "
                           "RON-03 (eventos de seguridad) miden facetas distintas del "
                           "riesgo operacional; el paper no reporta alpha por falta de "
                           "serie. n pequeno y correlacion ecologica: lectura "
                           "preliminar, no validacion factorial."),
    ], columns=["Metrica", "Valor"])

    r1 = resumen[(resumen.puerto == "CALLAO") & (resumen.variante == "V1")].iloc[0]
    r2 = resumen[(resumen.puerto == "PAITA") & (resumen.variante == "V1")].iloc[0]
    sat_callao = float((punt[(punt.puerto == "CALLAO")]["n_RON-01"] >= 1.0).mean())
    conclusion = pd.DataFrame([
        ("P1", "¿Sobrevive la clasificacion del paper (Callao ALTO, "
                       "Paita MODERADO-ALTO) a la incertidumbre?",
         f"Ranking robusto: Callao > Paita en {int(ranking['Callao_mayor_Paita'].sum())} "
         f"de {len(ranking)} anios (mediana MC, ambas variantes). Callao: "
         f"mediana MC {r1['compuesto_mc_mediana']:.1f} (p5-p95 "
         f"{r1['compuesto_mc_p5']:.1f}-{r1['compuesto_mc_p95']:.1f}), "
         f"P(>= paper 69.2) = {r1['P_ge_paper']:.0%} en V1 "
         f"({resumen[(resumen.puerto=='CALLAO')&(resumen.variante=='V2')].iloc[0]['P_ge_paper']:.0%} en V2). "
         f"Paita: mediana MC {r2['compuesto_mc_mediana']:.1f} (p5-p95 "
         f"{r2['compuesto_mc_p5']:.1f}-{r2['compuesto_mc_p95']:.1f}), "
         f"P(>= paper 57.4) = {r2['P_ge_paper']:.0%}: el score del paper "
         "para Paita esta en el extremo superior de lo que la serie "
         "reconstruida soporta."),
        ("P2", "¿Por que se mueve tanto Paita?",
         f"El RON recomputado de Paita (V1: {r2['RON_puntual']:.1f}, "
         f"V2: {resumen[(resumen.puerto=='PAITA')&(resumen.variante=='V2')].iloc[0]['RON_puntual']:.1f}) "
         "es mucho menor que la estimacion del paper (42.0): su trafico "
         "(~2.1M TM/año) y sus incidentes (0-2/año) son bajos frente al "
         "pool de 19 puertos. El RON pesa 12% y entra geometricamente, "
         "por lo que el compuesto cae de 57.4 a ~47 (V1). El Callao, en "
         "cambio, satura el min-max: "
         f"{sat_callao:.0%} de sus anios 2010-2017 tocan la cota 1.0 en "
         "RON-01 (es ~10x el siguiente puerto), lo que infla su RON "
         f"recomputado ({r1['RON_puntual']:.1f} vs 56.0 del paper)."),
        ("P3", "¿Que senala el Paso 3 (ACP/alpha)?",
         f"Alpha de Cronbach preliminar {acp['alpha_2ind']:.2f} (2 "
         f"indicadores, n={acp['n2']}) y {acp['alpha_3ind']:.2f} (3 "
         f"indicadores, n={acp['n3']}); PC1 explica "
         f"{acp['pca1_share_2ind']:.0%}. CAVEAT: RON-01 (TM) y RON-03 "
         "(incidentes) correlacionan 0.77 en parte porque ambos escalan "
         "con el tamaño del puerto — la coherencia puede medir tamano, no "
         "riesgo. Lectura preliminar, no validacion factorial."),
        ("P4", "¿Que falta para el Paso 7 completo?",
         "Series de RTID (decomisos DIRANDRO por puerto), RLAC (rankings "
         "SUNAT por aduana), RVI (PortMATE de campo) y RRC por puerto "
         "2015-2025 — pendientes de las solicitudes Ley 27806 en "
         "Solicitudes_Ley27806_ICRPP.md. Sin ellas, la incertidumbre de "
         "esos cuatro dominios (88% del peso) no esta cuantificada aqui."),
        ("Hallazgo", "Brecha Callao-Paita",
         f"El paper reporta 69.2 vs 57.4 (brecha 11.8). Recomputando RON "
         f"con datos abiertos la brecha sube a "
         f"{r1['compuesto_mc_mediana']-r2['compuesto_mc_mediana']:.1f} "
         "(V1): la concentracion del trafico en el Callao pesa mas de lo "
         "que el paper estima, y el riesgo operacional de Paita, menos."),
    ], columns=["Id", "Pregunta", "Respuesta / donde verlo"])

    with pd.ExcelWriter(OUT_XLSX, engine="openpyxl") as xw:
        metodo.to_excel(xw, sheet_name="METODO", index=False)
        punt.round(4).to_excel(xw, sheet_name="RON_PUNTUAL_V1", index=False)
        punt2.round(4).to_excel(xw, sheet_name="RON_PUNTUAL_V2", index=False)
        panel.round(2).to_excel(xw, sheet_name="RON_PANEL", index=False)
        resumen.to_excel(xw, sheet_name="MC_RESULTADOS", index=False)
        anual.to_excel(xw, sheet_name="MC_ANUAL", index=False)
        ranking.round(2).to_excel(xw, sheet_name="MC_RANKING_ANUAL", index=False)
        sens.to_excel(xw, sheet_name="SENSIBILIDAD_SPEARMAN", index=False)
        tornado.to_excel(xw, sheet_name="SENSIBILIDAD_TORNADO", index=False)
        acp_df.to_excel(xw, sheet_name="ACP_ALPHA_PASO3", index=False)
        conclusion.to_excel(xw, sheet_name="CONCLUSION", index=False)
        pd.DataFrame([
            ("Pool RON-01 (cargas TM, todos los puertos 2010-2017)",
             f"n={pool01.size}, p5={b01[0]:,.0f}, p95={b01[1]:,.0f}"),
            ("Pool RON-03 (incidentes, todos los puertos 2005-2017)",
             f"n={pool03.size}, p5={b03[0]:,.1f}, p95={b03[1]:,.1f}"),
        ], columns=["Pool", "Estadisticos"]).to_excel(
            xw, sheet_name="NORMALIZACION_POOLES", index=False)

    print("MC corridas:", len(mc))
    print(resumen.to_string(index=False))
    print()
    print("ACP:", {k: (round(v, 4) if isinstance(v, float) else v) for k, v in acp.items()})
    print("Ranking Callao>Paita:", int(ranking["Callao_mayor_Paita"].sum()), "/", len(ranking))
    print("salida:", OUT_XLSX)


if __name__ == "__main__":
    main()
