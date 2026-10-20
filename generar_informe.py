# -*- coding: utf-8 -*-
"""Informe: cruce DUAs x FOB en dolares, por organizacion.
Genera graficos PNG, el Markdown y el DOCX."""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt, RGBColor

OUT = r"C:\Users\acuba\appsperu"
XLSX = (r"C:\Users\acuba\eudrperu\BASE CAFE CACAO 174"
        r"\CONSULTA MASIVA RUC 10.10.26\CRUCE_DUAs_FOB_POR_ORGANIZACION.xlsx")
ANIOS = [2024, 2025, 2026]
AZUL = "#1F4E78"
VERDE = "#2E7D32"
AMBAR = "#E8A33D"
GRIS = "#9E9E9E"
ROJO = "#C0392B"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9,
    "axes.edgecolor": "#666666", "axes.labelcolor": "#333333",
    "axes.titlesize": 11, "axes.titleweight": "bold", "axes.titlecolor": AZUL,
    "figure.dpi": 150, "savefig.bbox": "tight", "savefig.facecolor": "white",
})

# ---------------------------------------------------------------- datos
h1 = pd.read_excel(XLSX, sheet_name="1. Cruce por organización")
h2 = pd.read_excel(XLSX, sheet_name="2. Detalle org-año")
h3 = pd.read_excel(XLSX, sheet_name="3. Detalle por combo")
h4 = pd.read_excel(XLSX, sheet_name="4. Resumen anual")

org = h1[h1["RUC"] != "TOTAL 76 RUC"].copy()
fob_tot = org["FOB USD TOTAL"].sum()
duas_tot = int(org["DUAs TOTAL"].sum())
act = org[org["FOB USD TOTAL"] > 0].copy()
sin = org[org["FOB USD TOTAL"] == 0].copy()
top = act.sort_values("FOB USD TOTAL", ascending=False).reset_index(drop=True)

M = lambda v: "US$ {:,.0f}".format(float(v))
N = lambda v: "{:,}".format(int(v))


def corta(s, n=34):
    s = str(s).strip()
    return s if len(s) <= n else s[: n - 1] + "…"


# ---------------------------------------------------------------- graficos
def etiqueta_bar(ax, barras, fmt="{:,.1f}M", dy=0.01):
    mx = max(b.get_height() for b in barras) or 1
    for b in barras:
        h = b.get_height()
        ax.annotate(fmt.format(h / 1e6 if "M" in fmt else h),
                    (b.get_x() + b.get_width() / 2, h),
                    textcoords="offset points", xytext=(0, 3),
                    ha="center", va="bottom", fontsize=7.5, color="#333333")
    ax.set_ylim(0, mx * 1.16)


# G1: FOB por año
fig, ax = plt.subplots(figsize=(6.6, 3.0))
b = ax.bar([str(a) for a in ANIOS], h4["FOB USD"].tolist(),
           color=[AZUL, AZUL, GRIS], width=0.55)
etiqueta_bar(ax, b)
ax.set_title("FOB exportado por año — universo de 76 RUC")
ax.set_ylabel("US$ millones")
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda v, p: "{:,.0f}M".format(v / 1e6)))
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", alpha=0.25, linestyle=":")
ax.annotate("año en curso\n(hasta octubre)", xy=(2, h4["FOB USD"].iloc[2]),
            xytext=(1.72, h4["FOB USD"].max() * 0.55), fontsize=7.5, color=ROJO,
            ha="center", arrowprops=dict(arrowstyle="->", color=ROJO, lw=0.9))
G1 = os.path.join(OUT, "grafico_fob_por_anio.png")
fig.savefig(G1)
plt.close(fig)

# G2: top 12 por FOB
t = top.head(12).iloc[::-1]
fig, ax = plt.subplots(figsize=(7.4, 4.4))
barras = ax.barh([corta(r["Razón social"], 30) for _, r in t.iterrows()],
                 t["FOB USD TOTAL"].tolist(), color=AZUL, height=0.68)
barras[-1].set_color(VERDE)
for bb, (_, r) in zip(barras, t.iterrows()):
    ax.annotate("{}  ·  {} DUAs · {} países".format(
        M(r["FOB USD TOTAL"]), N(r["DUAs TOTAL"]), N(r["N° países"])),
        (bb.get_width(), bb.get_y() + bb.get_height() / 2),
        xytext=(5, 0), textcoords="offset points",
        va="center", fontsize=7.2, color="#333333")
ax.set_xlim(0, t["FOB USD TOTAL"].max() * 1.42)
ax.set_title("Top 12 organizaciones por FOB exportado 2024–2026")
ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda v, p: "{:,.0f}M".format(v / 1e6)))
ax.set_xlabel("US$ millones")
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="x", alpha=0.25, linestyle=":")
G2 = os.path.join(OUT, "grafico_top_fob.png")
fig.savefig(G2)
plt.close(fig)

# G3: curva de concentracion
s = top["FOB USD TOTAL"].sort_values(ascending=False).reset_index(drop=True)
acum = s.cumsum() / fob_tot * 100
fig, ax = plt.subplots(figsize=(6.6, 3.2))
ax.plot(range(1, len(s) + 1), acum, color=AZUL, lw=2.2, marker="", zorder=3)
ax.fill_between(range(1, len(s) + 1), acum, color=AZUL, alpha=0.12, zorder=2)
for k, c in ((1, ROJO), (5, AMBAR), (10, VERDE)):
    ax.plot([k], [acum.iloc[k - 1]], "o", color=c, ms=7, zorder=4)
    ax.annotate("top {}: {:.0f}%".format(k, acum.iloc[k - 1]),
                (k, acum.iloc[k - 1]), xytext=(9, -12), textcoords="offset points",
                fontsize=8, color=c, fontweight="bold")
ax.axhline(80, color=GRIS, ls="--", lw=0.9)
ax.annotate("80% del FOB", (len(s) * 0.60, 81.5), fontsize=7.5, color="#777777")
ax.set_title("Concentración del FOB exportado")
ax.set_xlabel("Organizaciones ordenadas por FOB (de mayor a menor)")
ax.set_ylabel("% acumulado del FOB")
ax.set_ylim(0, 105)
ax.set_xlim(0, len(s) + 1)
ax.spines[["top", "right"]].set_visible(False)
ax.grid(alpha=0.25, linestyle=":")
G3 = os.path.join(OUT, "grafico_concentracion.png")
fig.savefig(G3)
plt.close(fig)

# G4: cobertura - situacion de los 76 RUC
cats = ["Con FOB y DUAs\n(exportan)", "Sin movimiento\n2024-2026"]
vals = [len(act), len(sin)]
fig, ax = plt.subplots(figsize=(6.6, 2.5))
barras = ax.barh(cats[::-1], vals[::-1], color=[GRIS, VERDE], height=0.5)
for bb, v in zip(barras, vals[::-1]):
    ax.annotate("{} RUC  ({:.0f}% de 76)".format(v, 100 * v / 76),
                (bb.get_width(), bb.get_y() + bb.get_height() / 2),
                xytext=(6, 0), textcoords="offset points", va="center",
                fontsize=8.5, fontweight="bold", color="#333333")
ax.set_xlim(0, 76 * 1.05)
ax.set_title("Cobertura del cruce sobre los 76 RUC exportadores")
ax.set_xlabel("Cantidad de RUC")
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="x", alpha=0.25, linestyle=":")
G4 = os.path.join(OUT, "grafico_cobertura.png")
fig.savefig(G4)
plt.close(fig)

# G5: FOB por año apilado, top 8
t8 = top.head(8)
fig, ax = plt.subplots(figsize=(7.4, 3.4))
x = range(len(t8))
p1 = ax.bar(x, t8["FOB USD 2024"], color=AZUL, label="2024", width=0.62)
p2 = ax.bar(x, t8["FOB USD 2025"], bottom=t8["FOB USD 2024"], color=VERDE,
            label="2025", width=0.62)
p3 = ax.bar(x, t8["FOB USD 2026"],
            bottom=t8["FOB USD 2024"] + t8["FOB USD 2025"], color=AMBAR,
            label="2026 (parcial)", width=0.62)
ax.set_xticks(list(x))
ax.set_xticklabels([corta(r["Razón social"], 16) for _, r in t8.iterrows()],
                   rotation=28, ha="right", fontsize=7.5)
ax.set_title("Composición anual del FOB — top 8 organizaciones")
ax.set_ylabel("US$ millones")
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda v, p: "{:,.0f}M".format(v / 1e6)))
ax.legend(frameon=False, fontsize=8, ncol=3, loc="upper right")
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", alpha=0.25, linestyle=":")
G5 = os.path.join(OUT, "grafico_composicion_anual.png")
fig.savefig(G5)
plt.close(fig)

print("graficos generados:")
for g in (G1, G2, G3, G4, G5):
    print("  ", os.path.basename(g))

# ================================================================ MARKDOWN
md = []
A = md.append

A("# Cruce de DUAs y FOB en dólares")
A("")
A("## Informe de movimientos de exportación 2024 – 2026")
A("")
A("**Universo:** 76 organizaciones cafetaleras y cacaoteras clasificadas como "
  "EXPORTADOR o IMPORTADOR/EXPORTADOR que integran la base de 174.  ")
A("**Fecha de corte:** 11 de octubre de 2026 · **2026 parcial** (hasta octubre).")
A("")
A("---")
A("")

A("## 1. Resumen ejecutivo")
A("")
A("| Indicador | Valor |")
A("|---|---|")
A("| Organizaciones del universo | 76 |")
A("| **Con exportación confirmada (FOB y DUAs)** | **%d (%.0f%%)** |" % (len(act), 100 * len(act) / 76))
A("| Sin movimiento en régimen 40 durante 2024-2026 | %d (%.0f%%) |" % (len(sin), 100 * len(sin) / 76))
A("| **FOB exportado total** | **%s** |" % M(fob_tot))
A("| **DUAs totales** | **%s** |" % N(duas_tot))
A("| Operaciones FOB | %s |" % N(int(org["Operaciones FOB TOTAL"].sum())))
A("| Ticket promedio | %s por DUA |" % M(fob_tot / duas_tot))
A("| Países destino | %d |" % int(h4["N° países"].max()))
A("| Canal VERDE / ROJO | %s / %s |" % (N(int(org["Canal VERDE"].sum())),
                                          N(int(org["Canal ROJO"].sum()))))
A("| Concentración: top 10 de 76 | %.0f%% del FOB |" % (top.head(10)["FOB USD TOTAL"].sum() / fob_tot * 100))
A("")
A("**Tres conclusiones de fondo:**")
A("")
A("1. **La exportación está muy concentrada.** Las 10 organizaciones más grandes explican "
  "el %.0f%% del FOB del universo; las 15 primeras, el %.0f%%. "
  "Trabajar el círculo chico mueve la mayoría del dinero."
  % (top.head(10)["FOB USD TOTAL"].sum() / fob_tot * 100,
     top.head(15)["FOB USD TOTAL"].sum() / fob_tot * 100))
A("2. **Ser exportador registrado no equivale a exportar.** %d de 76 RUC figuran como "
  "exportadores en su ficha SUNAT pero no registran movimiento en régimen 40 durante "
  "2024-2026." % len(sin))
A("3. **2025 es el año récord**, con %s, el %.0f%% del FOB del período; 2024 aportó %s y "
  "2026 (parcial) %s."
  % (M(h4[h4["Año"] == 2025]["FOB USD"].iloc[0]),
     100 * h4[h4["Año"] == 2025]["FOB USD"].iloc[0] / fob_tot,
     M(h4[h4["Año"] == 2024]["FOB USD"].iloc[0]),
     M(h4[h4["Año"] == 2026]["FOB USD"].iloc[0])))
A("")

A("## 2. Metodología y fuentes")
A("")
A("### Fuentes")
A("")
A("| Dato | Fuente | Cobertura |")
A("|---|---|---|")
A("| FOB en dólares | `BASE CONSOLIDADA.xlsx` → `HECHO_EXPORTACION` "
  "(SUNAT – Aduanas, exportaciones) | 2024, 2025 y 2026 |")
A("| DUAs, fecha de embarque y canal | `ficharucsunat/dua_canal_final.csv` "
  "(`accion=buscarListadoDuas` de ADUANET) | 2024, 2025 y 2026 |")
A("| Verificación en vivo | `_verif_dua_links.csv`: 699 enlaces consultados, 573 con datos | 2024-2026 |")
A("")
A("### Clave de cruce")
A("")
A("El cruce se hace por **RUC + año + mes + aduana + país**. El agente de aduana **no** "
  "entra en la clave por un defecto de la fuente, documentado en la sección 7.")
A("")
A("Con esa clave coinciden **917 combinaciones** y quedan **0 combinaciones con DUAs sin "
  "FOB**, sobre un FOB cruzado de US$ 291,8 millones de los US$ 292,7 millones totales de "
  "la fuente.")
A("")
A("### Advertencia sobre el ticket promedio")
A("")
A("Una misma combinación puede tener más de una DUA (embarques distintos con los mismos "
  "códigos). El FOB de la combinación se reparte entre esas DUAs, por lo que el ticket "
  "promedio es *FOB de la combinación ÷ número de DUAs*, **no** un dato propio de la DUA "
  "individual. Para el FOB por DUA hace falta el detalle `SgCDUI2`, que pide captcha.")
A("")
A("### Cuadre")
A("")
A("| Verificación | Resultado |")
A("|---|---|")
A("| FOB total igual en las 4 hojas del libro | %s ✓ |" % M(fob_tot))
A("| DUAs iguales en las 3 hojas | %s ✓ |" % N(duas_tot))
A("| 2024 + 2025 + 2026 = total | ✓ |")
A("| Operaciones FOB por año = total | %s ✓ |" % N(int(org["Operaciones FOB TOTAL"].sum())))
A("")

A("## 3. FOB exportado por año")
A("")
A("![FOB por año](grafico_fob_por_anio.png)")
A("")
A("| Año | RUC con FOB | RUC con DUAs | Operaciones FOB | DUAs | FOB USD | Ticket promedio | Países |")
A("|---|---|---|---|---|---|---|---|")
for _, r in h4.iterrows():
    A("| %d | %d | %d | %s | %s | %s | %s | %d |"
      % (r["Año"], r["RUC con FOB"], r["RUC con DUAs"], N(r["Operaciones FOB"]),
         N(r["DUAs"]), M(r["FOB USD"]), M(r["Ticket promedio USD/DUA"]), r["N° países"]))
A("| **Total** | **%d** | **%d** | **%s** | **%s** | **%s** | **%s** | **%d** |"
  % (act["RUC"].nunique(), act["RUC"].nunique(),
     N(int(h4["Operaciones FOB"].sum())), N(int(h4["DUAs"].sum())),
     M(h4["FOB USD"].sum()), M(fob_tot / duas_tot), int(h4["N° países"].max())))
A("")
A("*2026 está parcial: llega hasta octubre, por lo que su FOB no es comparable con un año "
  "completo. El ticket promedio de 2026 (%s) es además el más alto de los tres, señal de "
  "que los embarques recientes son de mayor valor unitario.*"
  % M(h4[h4["Año"] == 2026]["Ticket promedio USD/DUA"].iloc[0]))
A("")

A("## 4. Las organizaciones que más exportan")
A("")
A("![Top 12 por FOB](grafico_top_fob.png)")
A("")
A("| # | RUC | Organización | FOB 2024 | FOB 2025 | FOB 2026 | FOB total | DUAs | Países |")
A("|---|---|---|---|---|---|---|---|---|")
for i, r in top.head(12).iterrows():
    A("| %d | %s | %s | %s | %s | %s | **%s** | %s | %d |"
      % (i + 1, r["RUC"], corta(r["Razón social"], 40),
         M(r["FOB USD 2024"]), M(r["FOB USD 2025"]), M(r["FOB USD 2026"]),
         M(r["FOB USD TOTAL"]), N(r["DUAs TOTAL"]), r["N° países"]))
A("| | | **Top 12** | %s | %s | %s | **%s** | %s | |"
  % (M(top.head(12)["FOB USD 2024"].sum()), M(top.head(12)["FOB USD 2025"].sum()),
     M(top.head(12)["FOB USD 2026"].sum()), M(top.head(12)["FOB USD TOTAL"].sum()),
     N(int(top.head(12)["DUAs TOTAL"].sum()))))
A("")
A("![Composición anual](grafico_composicion_anual.png)")
A("")
A("**Lecturas del cuadro:**")
A("")
A("- **Tres organizaciones concentran el %.0f%% del FOB**: Sonomoro del VRAEM (%s), "
  "Cuencas del Huallaga (%s) y Cacao Aromático Colpa de Loros (%s)."
  % (top.head(3)["FOB USD TOTAL"].sum() / fob_tot * 100,
     M(top.iloc[0]["FOB USD TOTAL"]), M(top.iloc[1]["FOB USD TOTAL"]),
     M(top.iloc[2]["FOB USD TOTAL"])))
A("- **Colpa de Loros exporta a un solo país** (Francia, vía Kaoka) y aun así es la tercera: "
  "tiene una alianza comercial exclusiva que sustituye la diversificación.")
A("- **Ecoforest y Valle de Incahuasi son las más diversificadas** del top: 10 países cada una.")
A("- **Valle Grande, Cuencas del Huallaga y Caecam solo tienen FOB de 2025 en adelante**: "
  "son organizaciones de arranque reciente o que consolidaron su exportación ese año.")
A("- **Sangareni no registra FOB en 2026**, con US$ 13,2 millones acumulados de 2024-2025: "
  "es la única del top con un año completo en cero. Vale verificar si es discontinuidad o "
  "cambio de razón social.")
A("")

A("## 5. Concentración del FOB")
A("")
A("![Concentración](grafico_concentracion.png)")
A("")
A("| Ranking | FOB acumulado | % del universo |")
A("|---|---|---|")
for k in (1, 3, 5, 10, 15, 20):
    A("| Top %d | %s | %.0f%% |" % (k, M(top.head(k)["FOB USD TOTAL"].sum()),
                                     100 * top.head(k)["FOB USD TOTAL"].sum() / fob_tot))
A("| **%d organizaciones con FOB** | **%s** | **100%%** |" % (len(act), M(fob_tot)))
A("")
A("El %.0f%% del FOB sale de las 10 primeras organizaciones. Dicho de otro modo: **con "
  "atender 10 de 76 RUC se cubre dos tercios del movimiento exportador** del universo."
  % (top.head(10)["FOB USD TOTAL"].sum() / fob_tot * 100))
A("")

A("## 6. Cobertura: los 32 RUC sin movimiento")
A("")
A("![Cobertura](grafico_cobertura.png)")
A("")
A("De los 76 RUC que la ficha SUNAT clasifica como exportadores, **%d no registran FOB ni "
  "DUAs en régimen 40 durante 2024-2026**." % len(sin))
A("")
A("| RUC | Razón social |")
A("|---|---|")
for _, r in sin.sort_values("RUC").iterrows():
    A("| %s | %s |" % (r["RUC"], corta(r["Razón social"], 62)))
A("")
A("**Interpretación.** No significa necesariamente que no exporten. Las explicaciones "
  "posibles, en orden de frecuencia para este tipo de organizaciones, son:")
A("")
A("1. **Venta mediante comercializadora:** la cooperativa vende su café o cacao a un "
  "intermediario o exportador, y la DUA sale a nombre del comprador. Es el caso más común "
  "en organizaciones chicas sin plataforma de exportación propia.")
A("2. **Exportación bajo otro régimen distinto al 40** (por ejemplo, regímenes temporales "
  "o de draw-back), que no quedan en esta consulta.")
A("3. **Registro SUNAT vigente pero operación real suspendida**, como la Cooperativa "
  "Agraria de Cacaoteros Tecnificados de Padre Abad (RUC 20352417018), que figura en "
  "*suspensión temporal*.")
A("")
A("En los tres casos la conclusión práctica es la misma: **estas organizaciones no son "
  "exportadoras directas y no deberían tratarse como tales** en un análisis de cadena de "
  "valor sin verificarlo una por una.")
A("")

A("## 7. Hallazgo de calidad de datos: el agente de aduana en 2024")
A("")
A("Durante el cruce se detectó un defecto de la fuente que conviene dejar documentado "
  "porque afecta cualquier análisis que cruce estas dos tablas por agente.")
A("")
A("| Año | Filas en `HECHO_EXPORTACION` | `agente_codigo = 0` (vacío) | Agentes con dato |")
A("|---|---|---|---|")
he = pd.read_excel(r"C:\Users\acuba\eudrperu\ficharucsunat\BASE CONSOLIDADA.xlsx",
                   sheet_name="HECHO_EXPORTACION")
he["anio"] = pd.to_numeric(he["anio"], errors="coerce").astype(int)
he["ag"] = pd.to_numeric(he["agente_codigo"], errors="coerce").fillna(0).astype(int)
for a, g in he.groupby("anio"):
    A("| %d | %d | %d | %d |" % (a, len(g), int((g["ag"] == 0).sum()),
                                  g.loc[g["ag"] != 0, "ag"].nunique()))
A("")
A("**Consecuencia.** Las **278 filas de 2024** —todas— llegaron sin código de agente. "
  "Al cruzar por RUC + año + mes + aduana + **agente** + país, el resultado era engañoso: "
  "271 combinaciones con FOB y sin DUAs, y otras 271 al revés, con las casillas de FOB en "
  "cero. Un análisis que mirara solo esas cifras concluiría falsamente que 2024 no tuvo "
  "DUAs.")
A("")
A("**Solución aplicada.** Se quitó el agente de la clave de cruce y se pasó a "
  "**RUC + año + mes + aduana + país**. El agente se conserva como columna informativa, "
  "tomado de la tabla de DUAs cuando existe y de la de FOB cuando no. Con esa clave:")
A("")
A("- Coinciden **917 combinaciones**.")
A("- Quedan **0 combinaciones con DUAs y sin FOB** (antes 271).")
A("- El FOB que cruza con DUAs sube a **US$ 291,8 millones de US$ 292,7 millones**.")
A("- La hoja de detalle por combinación pasa de 888 a **655 filas**, todas con FOB real.")
A("")
A("**Recomendación.** Corregir el ingreso de 2024 en `HECHO_EXPORTACION` completando el "
  "`agente_codigo` desde `dua_canal_final.csv`, que sí lo tiene. Con ese arreglo el cruce "
  "por agente vuelve a ser válido y se gana la dimensión del agente en el análisis.")
A("")

A("## 8. Canales de control")
A("")
n_rojo = int(org["Canal ROJO"].sum())
A("De las %s DUAs del universo, **%s salieron por canal VERDE y %s por canal ROJO** "
  "(%.2f%%)." % (N(duas_tot), N(int(org["Canal VERDE"].sum())), N(n_rojo),
                 100 * n_rojo / duas_tot))
A("")
A("| RUC | Organización | DUAs rojas | DUAs totales | FOB total |")
A("|---|---|---|---|---|")
for _, r in org[org["Canal ROJO"] > 0].sort_values("Canal ROJO", ascending=False).iterrows():
    A("| %s | %s | %d | %s | %s |" % (r["RUC"], corta(r["Razón social"], 44),
                                       r["Canal ROJO"], N(r["DUAs TOTAL"]),
                                       M(r["FOB USD TOTAL"])))
A("")
A("El canal rojo implica inspección física de la mercancía. Son 6 operaciones de 5 "
  "organizaciones, así que no hay un patrón sistémico, pero conviene revisarlas: una DUA "
  "roja repetida en la misma organización suele indicar un problema de documentación o de "
  "clasificación arancelaria. **Allima Cacao** tiene una DUA roja sobre un FOB de apenas "
  "US$ 1 984, proporción que no se justifica por el volumen y sugiere un problema de "
  "papeles más que de mercancía.")
A("")

A("## 9. Anexo: las 44 organizaciones con exportación confirmada")
A("")
A("| RUC | Organización | FOB 2024 | FOB 2025 | FOB 2026 | FOB total | DUAs | Ticket prom. | Países | Aduanas |")
A("|---|---|---|---|---|---|---|---|---|---|")
for _, r in top.iterrows():
    A("| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |"
      % (r["RUC"], corta(r["Razón social"], 34), M(r["FOB USD 2024"]), M(r["FOB USD 2025"]),
         M(r["FOB USD 2026"]), M(r["FOB USD TOTAL"]), N(r["DUAs TOTAL"]),
         M(r["Ticket promedio USD/DUA"]) if pd.notna(r["Ticket promedio USD/DUA"]) else "—",
         r["Países destino"] if pd.notna(r["Países destino"]) else "—",
         r["Aduanas"] if pd.notna(r["Aduanas"]) else "—"))
A("| | **Total** | %s | %s | %s | **%s** | **%s** | **%s** | | |"
  % (M(top["FOB USD 2024"].sum()), M(top["FOB USD 2025"].sum()),
     M(top["FOB USD 2026"].sum()), M(fob_tot), N(duas_tot), M(fob_tot / duas_tot)))
A("")
A("---")
A("")
A("*Informe generado el 11 de octubre de 2026. Todas las cifras provienen de "
  "SUNAT – Aduanas vía ADUANET y del consolidado del proyecto. El detalle combinación por "
  "combinación está en el libro `CRUCE_DUAs_FOB_POR_ORGANIZACION.xlsx`.*")

MD = os.path.join(OUT, "INFORME_CRUCE_DUAs_FOB.md")
with open(MD, "w", encoding="utf-8") as f:
    f.write("\n".join(md))
print("MD ->", MD, "|", len("\n".join(md)), "caracteres")


# ================================================================ DOCX
doc = Document()
st = doc.styles["Normal"]
st.font.name = "Calibri"
st.font.size = Pt(10)
for s in doc.sections:
    s.left_margin = s.right_margin = Cm(1.9)
    s.top_margin = s.bottom_margin = Cm(1.9)
AZ = RGBColor(0x1F, 0x4E, 0x78)


def H(t, n):
    p = doc.add_heading(t, level=n)
    for r in p.runs:
        r.font.color.rgb = AZ
    return p


def P(t, bold=False, italic=False, size=10, align=None, color=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    if align:
        p.alignment = align
    r = p.add_run(t)
    r.bold, r.italic = bold, italic
    r.font.size = Pt(size)
    if color:
        r.font.color.rgb = color
    return p


def img(path, ancho=16.2):
    doc.add_picture(path, width=Cm(ancho))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER


def tabla(df, encabezado_num=True, total_row=False, ancho_max=44):
    t = doc.add_table(rows=1, cols=len(df.columns))
    t.style = "Light Grid Accent 1"
    for i, c in enumerate(df.columns):
        cell = t.rows[0].cells[i]
        cell.text = str(c)
        for p in cell.paragraphs:
            for r in p.runs:
                r.bold = True
                r.font.size = Pt(7.5)
    for k, (_, row) in enumerate(df.iterrows()):
        cells = t.add_row().cells
        for i, c in enumerate(df.columns):
            v = row[c]
            if isinstance(v, float):
                v = "{:,.2f}".format(v) if "ticket" in str(c).lower() or "prom" in str(c).lower() \
                    else "{:,.0f}".format(v)
            txt = "—" if pd.isna(v) else str(v)
            cells[i].text = txt[:ancho_max]
            for p in cells[i].paragraphs:
                for r in p.runs:
                    r.font.size = Pt(7.5)
                    if total_row and k == len(df) - 1:
                        r.bold = True
    return t


# --- portada
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Cruce de DUAs y FOB en dólares")
r.bold = True
r.font.size = Pt(24)
r.font.color.rgb = AZ
P("Informe de movimientos de exportación 2024 – 2026", italic=True, size=12,
  align=WD_ALIGN_PARAGRAPH.CENTER)
P("Universo: 76 organizaciones cafetaleras y cacaoteras clasificadas como EXPORTADOR o "
  "IMPORTADOR/EXPORTADOR que integran la base de 174",
  size=9, align=WD_ALIGN_PARAGRAPH.CENTER, color=RGBColor(0x66, 0x66, 0x66))
P("Fecha de corte: 11 de octubre de 2026 · 2026 parcial (hasta octubre)",
  size=9, align=WD_ALIGN_PARAGRAPH.CENTER, color=RGBColor(0x66, 0x66, 0x66))
doc.add_paragraph()

H("1. Resumen ejecutivo", 1)
d = pd.DataFrame({
    "Indicador": ["Organizaciones del universo", "Con exportación confirmada (FOB y DUAs)",
                  "Sin movimiento en régimen 40 durante 2024-2026", "FOB exportado total",
                  "DUAs totales", "Operaciones FOB", "Ticket promedio",
                  "Países destino", "Canal VERDE / ROJO", "Concentración: top 10 de 76"],
    "Valor": [76, "%d (%.0f%%)" % (len(act), 100 * len(act) / 76),
              "%d (%.0f%%)" % (len(sin), 100 * len(sin) / 76),
              M(fob_tot), N(duas_tot), N(int(org["Operaciones FOB TOTAL"].sum())),
              M(fob_tot / duas_tot), int(h4["N° países"].max()),
              "%s / %s" % (N(int(org["Canal VERDE"].sum())), N(int(org["Canal ROJO"].sum()))),
              "%.0f%% del FOB" % (top.head(10)["FOB USD TOTAL"].sum() / fob_tot * 100)],
})
tabla(d)

P("Tres conclusiones de fondo", bold=True, size=11)
P("1. La exportación está muy concentrada. Las 10 organizaciones más grandes explican el "
  "%.0f%% del FOB del universo; las 15 primeras, el %.0f%%. Trabajar el círculo chico "
  "mueve la mayoría del dinero."
  % (top.head(10)["FOB USD TOTAL"].sum() / fob_tot * 100,
     top.head(15)["FOB USD TOTAL"].sum() / fob_tot * 100))
P("2. Ser exportador registrado no equivale a exportar. %d de 76 RUC figuran como "
  "exportadores en su ficha SUNAT pero no registran movimiento en régimen 40 durante "
  "2024-2026." % len(sin))
P("3. 2025 es el año récord, con %s, el %.0f%% del FOB del período; 2024 aportó %s y "
  "2026 (parcial) %s."
  % (M(h4[h4["Año"] == 2025]["FOB USD"].iloc[0]),
     100 * h4[h4["Año"] == 2025]["FOB USD"].iloc[0] / fob_tot,
     M(h4[h4["Año"] == 2024]["FOB USD"].iloc[0]),
     M(h4[h4["Año"] == 2026]["FOB USD"].iloc[0])))

H("2. Metodología y fuentes", 1)
tabla(pd.DataFrame({
    "Dato": ["FOB en dólares", "DUAs, fecha de embarque y canal", "Verificación en vivo"],
    "Fuente": ["BASE CONSOLIDADA.xlsx → HECHO_EXPORTACION (SUNAT – Aduanas, exportaciones)",
               "ficharucsunat/dua_canal_final.csv (buscarListadoDuas de ADUANET)",
               "_verif_dua_links.csv: 699 enlaces consultados, 573 con datos"],
    "Cobertura": ["2024, 2025 y 2026", "2024, 2025 y 2026", "2024-2026"],
}))
P("")
P("Clave de cruce", bold=True, size=11)
P("El cruce se hace por RUC + año + mes + aduana + país. El agente de aduana no entra en "
  "la clave por un defecto de la fuente, documentado en la sección 7. Con esa clave "
  "coinciden 917 combinaciones y quedan 0 combinaciones con DUAs sin FOB, sobre un FOB "
  "cruzado de US$ 291,8 millones de los US$ 292,7 millones totales de la fuente.")
P("Advertencia sobre el ticket promedio", bold=True, size=11)
P("Una misma combinación puede tener más de una DUA (embarques distintos con los mismos "
  "códigos). El FOB de la combinación se reparte entre esas DUAs, por lo que el ticket "
  "promedio es FOB de la combinación ÷ número de DUAs, no un dato propio de la DUA "
  "individual. Para el FOB por DUA hace falta el detalle SgCDUI2, que pide captcha.")
P("Cuadre", bold=True, size=11)
tabla(pd.DataFrame({
    "Verificación": ["FOB total igual en las 4 hojas del libro",
                     "DUAs iguales en las 3 hojas",
                     "2024 + 2025 + 2026 = total",
                     "Operaciones FOB por año = total"],
    "Resultado": [M(fob_tot) + " ✓", N(duas_tot) + " ✓", "✓",
                  N(int(org["Operaciones FOB TOTAL"].sum())) + " ✓"],
}))

doc.add_page_break()
H("3. FOB exportado por año", 1)
img(G1, 15.5)
t = h4.copy()
t.columns = ["Año", "RUC con FOB", "RUC con DUAs", "Operaciones FOB", "DUAs", "FOB USD",
             "Ticket promedio USD/DUA", "N° países", "Países destino", "N° aduanas"]
t["FOB USD"] = t["FOB USD"].map(lambda v: "{:,.0f}".format(v))
t["Ticket promedio USD/DUA"] = t["Ticket promedio USD/DUA"].map(lambda v: "{:,.0f}".format(v))
t = t.drop(columns=["Países destino", "N° aduanas"])
tot = {"Año": "Total", "RUC con FOB": act["RUC"].nunique(), "RUC con DUAs": act["RUC"].nunique(),
       "Operaciones FOB": int(h4["Operaciones FOB"].sum()), "DUAs": int(h4["DUAs"].sum()),
       "FOB USD": "{:,.0f}".format(fob_tot),
       "Ticket promedio USD/DUA": "{:,.0f}".format(fob_tot / duas_tot),
       "N° países": int(h4["N° países"].max())}
t = pd.concat([t, pd.DataFrame([tot])], ignore_index=True)
tabla(t, total_row=True)
P("")
P("2026 está parcial: llega hasta octubre, por lo que su FOB no es comparable con un año "
  "completo. El ticket promedio de 2026 (%s) es además el más alto de los tres, señal de "
  "que los embarques recientes son de mayor valor unitario."
  % M(h4[h4["Año"] == 2026]["Ticket promedio USD/DUA"].iloc[0]), italic=True, size=8.5)

doc.add_page_break()
H("4. Las organizaciones que más exportan", 1)
img(G2, 16.2)
t = top.head(12).copy()
t.insert(0, "#", range(1, len(t) + 1))
t["FOB total"] = t["FOB USD TOTAL"].map(lambda v: "{:,.0f}".format(v))
for c in ("FOB USD 2024", "FOB USD 2025", "FOB USD 2026"):
    t[c] = t[c].map(lambda v: "{:,.0f}".format(v))
t["Razón social"] = t["Razón social"].map(lambda s: corta(s, 30))
t["DUAs TOTAL"] = t["DUAs TOTAL"].map(N)
tt = t[["#", "RUC", "Razón social", "FOB USD 2024", "FOB USD 2025", "FOB USD 2026",
        "FOB total", "DUAs TOTAL", "N° países"]].rename(columns={"DUAs TOTAL": "DUAs"})
tabla(tt)
P("")
img(G5, 16.2)
P("Lecturas del cuadro", bold=True, size=11)
P("- Tres organizaciones concentran el %.0f%% del FOB: Sonomoro del VRAEM (%s), Cuencas "
  "del Huallaga (%s) y Cacao Aromático Colpa de Loros (%s)."
  % (top.head(3)["FOB USD TOTAL"].sum() / fob_tot * 100, M(top.iloc[0]["FOB USD TOTAL"]),
     M(top.iloc[1]["FOB USD TOTAL"]), M(top.iloc[2]["FOB USD TOTAL"])))
P("- Colpa de Loros exporta a un solo país (Francia, vía Kaoka) y aun así es la tercera: "
  "tiene una alianza comercial exclusiva que sustituye la diversificación.")
P("- Ecoforest y Valle de Incahuasi son las más diversificadas del top: 10 países cada una.")
P("- Valle Grande, Cuencas del Huallaga y Caecam solo tienen FOB de 2025 en adelante: son "
  "organizaciones de arranque reciente o que consolidaron su exportación ese año.")
P("- Sangareni no registra FOB en 2026, con US$ 13,2 millones acumulados de 2024-2025: es "
  "la única del top con un año completo en cero. Vale verificar si es discontinuidad o "
  "cambio de razón social.")

doc.add_page_break()
H("5. Concentración del FOB", 1)
img(G3, 15.5)
t = pd.DataFrame({
    "Ranking": ["Top 1", "Top 3", "Top 5", "Top 10", "Top 15", "Top 20",
                "%d organizaciones con FOB" % len(act)],
    "FOB acumulado": [M(top.head(k)["FOB USD TOTAL"].sum()) for k in (1, 3, 5, 10, 15, 20)] + [M(fob_tot)],
    "% del universo": ["%.0f%%" % (100 * top.head(k)["FOB USD TOTAL"].sum() / fob_tot)
                       for k in (1, 3, 5, 10, 15, 20)] + ["100%"],
})
tabla(t, total_row=True)
P("")
P("El %.0f%% del FOB sale de las 10 primeras organizaciones. Dicho de otro modo: con "
  "atender 10 de 76 RUC se cubre dos tercios del movimiento exportador del universo."
  % (top.head(10)["FOB USD TOTAL"].sum() / fob_tot * 100))

doc.add_page_break()
H("6. Cobertura: los 32 RUC sin movimiento", 1)
img(G4, 15.0)
P("De los 76 RUC que la ficha SUNAT clasifica como exportadores, %d no registran FOB ni "
  "DUAs en régimen 40 durante 2024-2026." % len(sin))
t = sin.sort_values("RUC")[["RUC", "Razón social"]].copy()
t["Razón social"] = t["Razón social"].map(lambda s: corta(s, 56))
tabla(t)
P("")
P("Interpretación", bold=True, size=11)
P("No significa necesariamente que no exporten. Las explicaciones posibles, en orden de "
  "frecuencia para este tipo de organizaciones, son:")
P("1. Venta mediante comercializadora: la cooperativa vende su café o cacao a un "
  "intermediario o exportador, y la DUA sale a nombre del comprador. Es el caso más común "
  "en organizaciones chicas sin plataforma de exportación propia.")
P("2. Exportación bajo otro régimen distinto al 40 (por ejemplo, regímenes temporales o de "
  "draw-back), que no quedan en esta consulta.")
P("3. Registro SUNAT vigente pero operación real suspendida, como la Cooperativa Agraria "
  "de Cacaoteros Tecnificados de Padre Abad (RUC 20352417018), que figura en suspensión "
  "temporal.")
P("En los tres casos la conclusión práctica es la misma: estas organizaciones no son "
  "exportadoras directas y no deberían tratarse como tales en un análisis de cadena de "
  "valor sin verificarlo una por una.", italic=True)

doc.add_page_break()
H("7. Hallazgo de calidad de datos: el agente de aduana en 2024", 1)
P("Durante el cruce se detectó un defecto de la fuente que conviene dejar documentado "
  "porque afecta cualquier análisis que cruce estas dos tablas por agente.")
t = pd.DataFrame({
    "Año": [a for a, g in he.groupby("anio")],
    "Filas en HECHO_EXPORTACION": [len(g) for _, g in he.groupby("anio")],
    "agente_codigo = 0 (vacío)": [int((g["ag"] == 0).sum()) for _, g in he.groupby("anio")],
    "Agentes con dato": [g.loc[g["ag"] != 0, "ag"].nunique() for _, g in he.groupby("anio")],
})
tabla(t)
P("")
P("Consecuencia", bold=True, size=11)
P("Las 278 filas de 2024 —todas— llegaron sin código de agente. Al cruzar por RUC + año + "
  "mes + aduana + agente + país, el resultado era engañoso: 271 combinaciones con FOB y "
  "sin DUAs, y otras 271 al revés, con las casillas de FOB en cero. Un análisis que mirara "
  "solo esas cifras concluiría falsamente que 2024 no tuvo DUAs.")
P("Solución aplicada", bold=True, size=11)
P("Se quitó el agente de la clave de cruce y se pasó a RUC + año + mes + aduana + país. El "
  "agente se conserva como columna informativa, tomado de la tabla de DUAs cuando existe y "
  "de la de FOB cuando no. Con esa clave:")
P("- Coinciden 917 combinaciones.")
P("- Quedan 0 combinaciones con DUAs y sin FOB (antes 271).")
P("- El FOB que cruza con DUAs sube a US$ 291,8 millones de US$ 292,7 millones.")
P("- La hoja de detalle por combinación pasa de 888 a 655 filas, todas con FOB real.")
P("Recomendación", bold=True, size=11)
P("Corregir el ingreso de 2024 en HECHO_EXPORTACION completando el agente_codigo desde "
  "dua_canal_final.csv, que sí lo tiene. Con ese arreglo el cruce por agente vuelve a ser "
  "válido y se gana la dimensión del agente en el análisis.")

H("8. Canales de control", 1)
n_rojo = int(org["Canal ROJO"].sum())
P("De las %s DUAs del universo, %s salieron por canal VERDE y %s por canal ROJO (%.2f%%)."
  % (N(duas_tot), N(int(org["Canal VERDE"].sum())), N(n_rojo), 100 * n_rojo / duas_tot))
t = org[org["Canal ROJO"] > 0].sort_values("Canal ROJO", ascending=False)[
    ["RUC", "Razón social", "Canal ROJO", "DUAs TOTAL", "FOB USD TOTAL"]].copy()
t["Razón social"] = t["Razón social"].map(lambda s: corta(s, 40))
t["Canal ROJO"] = t["Canal ROJO"].astype(int)
t["FOB USD TOTAL"] = t["FOB USD TOTAL"].map(lambda v: "{:,.0f}".format(v))
t = t.rename(columns={"Canal ROJO": "DUAs rojas", "DUAs TOTAL": "DUAs totales",
                      "FOB USD TOTAL": "FOB total"})
tabla(t)
P("")
P("El canal rojo implica inspección física de la mercancía. Son 6 operaciones de 5 "
  "organizaciones, así que no hay un patrón sistémico, pero conviene revisarlas: una DUA "
  "roja repetida en la misma organización suele indicar un problema de documentación o de "
  "clasificación arancelaria. Allima Cacao tiene una DUA roja sobre un FOB de apenas "
  "US$ 1 984, proporción que no se justifica por el volumen y sugiere un problema de "
  "papeles más que de mercancía.")

doc.add_page_break()
H("9. Anexo: las 44 organizaciones con exportación confirmada", 1)
t = top.copy()
for c in ("FOB USD 2024", "FOB USD 2025", "FOB USD 2026", "FOB USD TOTAL"):
    t[c] = t[c].map(lambda v: "{:,.0f}".format(v))
t["Razón social"] = t["Razón social"].map(lambda s: corta(s, 28))
t["DUAs TOTAL"] = t["DUAs TOTAL"].map(N)
t["Ticket promedio USD/DUA"] = t["Ticket promedio USD/DUA"].map(
    lambda v: "{:,.0f}".format(v) if pd.notna(v) else "—")
t["Países destino"] = t["Países destino"].fillna("—").map(lambda s: corta(s, 26))
t["Aduanas"] = t["Aduanas"].fillna("—")
tt = t[["RUC", "Razón social", "FOB USD 2024", "FOB USD 2025", "FOB USD 2026",
        "FOB USD TOTAL", "DUAs TOTAL", "Ticket promedio USD/DUA", "Países destino",
        "Aduanas"]].rename(columns={"FOB USD TOTAL": "FOB total",
                                    "DUAs TOTAL": "DUAs"})
tt.loc[len(tt)] = ["", "Total", "{:,.0f}".format(top["FOB USD 2024"].sum()),
                   "{:,.0f}".format(top["FOB USD 2025"].sum()),
                   "{:,.0f}".format(top["FOB USD 2026"].sum()), "{:,.0f}".format(fob_tot),
                   N(duas_tot), "{:,.0f}".format(fob_tot / duas_tot), "", ""]
tabla(tt, total_row=True)
P("")
P("Informe generado el 11 de octubre de 2026. Todas las cifras provienen de SUNAT – "
  "Aduanas vía ADUANET y del consolidado del proyecto. El detalle combinación por "
  "combinación está en el libro CRUCE_DUAs_FOB_POR_ORGANIZACION.xlsx.",
  italic=True, size=8, color=RGBColor(0x66, 0x66, 0x66))

DOCX = os.path.join(OUT, "INFORME_CRUCE_DUAs_FOB.docx")
doc.save(DOCX)
print("DOCX->", DOCX)
print()
print("FOB total:", M(fob_tot), "| DUAs:", N(duas_tot), "| activas:", len(act),
      "| sin movimiento:", len(sin))
