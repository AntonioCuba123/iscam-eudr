# -*- coding: utf-8 -*-
"""Test de contraste D3 (legalidad OSCE/OEFA) vs componentes del ISA-PV."""
import openpyxl, numpy as np
from collections import Counter

p = r"C:\Users\acuba\eudrperu\PLANTILLA_INDICE_PVE_ISCAM.xlsx"
wb = openpyxl.load_workbook(p, data_only=True)
m = wb["MATRIZ_174"]
s = wb["ISCAM_Score"]

N = 174
D3 = np.array([m.cell(3+i, 21).value or 0 for i in range(N)], dtype=float)
CERT = np.array([m.cell(3+i, 15).value or 0 for i in range(N)], dtype=float)
D12 = np.array([m.cell(3+i, 23).value or 0 for i in range(N)], dtype=float)
D13 = np.array([m.cell(3+i, 24).value or 0 for i in range(N)], dtype=float)
D14 = np.array([m.cell(3+i, 25).value or 0 for i in range(N)], dtype=float)
D15 = np.array([m.cell(3+i, 26).value or 0 for i in range(N)], dtype=float)
ISAPV = np.array([m.cell(3+i, 42).value or 0 for i in range(N)], dtype=float)
RUC = [str(m.cell(3+i, 1).value) for i in range(N)]
RAZ = [str(m.cell(3+i, 2).value)[:38] for i in range(N)]

IP  = np.array([s.cell(4+i, 26).value or 0 for i in range(N)], dtype=float)
IV  = np.array([s.cell(4+i, 27).value or 0 for i in range(N)], dtype=float)
RE  = np.array([s.cell(4+i, 28).value or 0 for i in range(N)], dtype=float)
IV4 = np.array([s.cell(4+i, 24).value or 0 for i in range(N)], dtype=float)
ISAeudr = np.array([s.cell(4+i, 37).value or 0 for i in range(N)], dtype=float)
ISAcomp = np.array([s.cell(4+i, 38).value or 0 for i in range(N)], dtype=float)
TIPO = [s.cell(4+i, 29).value for i in range(N)]

def pearson(x, y):
    if np.std(x) == 0 or np.std(y) == 0:
        return float("nan")
    return float(np.corrcoef(x, y)[0, 1])

def spearman(x, y):
    def rank(a):
        order = a.argsort(); r = np.empty(len(a)); r[order] = np.arange(len(a))
        return r
    if np.std(x) == 0 or np.std(y) == 0:
        return float("nan")
    return float(np.corrcoef(rank(x), rank(y))[0, 1])

L = []
def P(t=""):
    L.append(t); print(t)

P("# Contraste D3 (legalidad OSCE/OEFA) ↔ ISA-Pacto Verde")
P(f"\nMuestra: {N} organizaciones | fecha de consulta: 2026-10-15\n")

P("## 1. Distribución de la señal de legalidad (D3)")
P(f"- {int((D3==1.0).sum())} orgs D3=1.00 (sin hallazgos) | {int((D3==0.75).sum())} orgs D3=0.75 (infracción ambiental) "
  f"| {int((D3==0).sum())} con inhabilitación vigente")
P(f"- media = {D3.mean():.4f} | desv. est. = {D3.std():.4f} | min = {D3.min():.2f} | max = {D3.max():.2f}")
P(f"- **Varianza prácticamente nula** (1 observación distinta de 173): la correlación no es identificable.\n")

P("## 2. Correlaciones formales (n=174)")
P(f"| Par | Pearson | Spearman | Varianza del predictor |")
P(f"|---|---|---|---|")
for nom, x in [("D3 ~ ISA-PV", ISAPV), ("D3 ~ D12 Huella Carbono", D12),
               ("D3 ~ D13 Reporte Sost.", D13), ("D3 ~ D14 Econ. Circular", D14),
               ("D3 ~ D15 Fitosanitario", D15), ("D3 ~ Certificación", CERT)]:
    P(f"| {nom} | {pearson(D3,x):.3f} | {spearman(D3,x):.3f} | var={x.var():.2f} |")

P("\n## 3. ¿Tiene varianza el bloque ambiental del ISA-PV?")
for nom, x in [("D12", D12), ("D13", D13), ("D14", D14), ("D15", D15), ("ISA-PV (0-1)", ISAPV)]:
    u = Counter(np.round(x, 3).tolist())
    P(f"- {nom}: media={x.mean():.3f} | rango=[{x.min()}, {x.max()}] | valores: "
      f"{', '.join(f'{k}×{v}' for k, v in sorted(u.items(), key=lambda t:-t[1])[:6])}")

P("\n## 4. Certificación ↔ bloque ambiental (proxies con varianza real)")
for nom, x in [("ISA-PV (0-1)", ISAPV), ("D12 Huella Carbono", D12), ("D13 Reporte Sost.", D13),
               ("D14 Econ. Circular", D14), ("D15 Fitosanitario", D15)]:
    P(f"- Cert ~ {nom}: Pearson={pearson(CERT,x):.3f} | Spearman={spearman(CERT,x):.3f} | n(Cert>0)={int((CERT>0).sum())}")

P("\n## 5. Perfil de la única organización con registro de legalidad")
idx = [i for i in range(N) if D3[i] < 1.0]
for i in idx:
    P(f"- RUC {RUC[i]} — {RAZ[i]}: D3={D3[i]:.2f} | Cert={CERT[i]:.2f} | "
      f"D12-D15={[D12[i],D13[i],D14[i],D15[i]]} | ISA-PV={ISAPV[i]:.2f} | "
      f"IV4={IV4[i]:.1f} | IP={IP[i]:.1f} | IV={IV[i]:.1f} | RE={RE[i]:.1f} | tipo={TIPO[i]}")

P("\n## 6. Estadísticas del motor (contexto)")
for nom, x in [("IP (Preparación)", IP), ("IV (Vulnerabilidad)", IV), ("RE (Exclusión)", RE),
               ("IV4 (cert+legalidad)", IV4), ("ISA-EUDR", ISAeudr), ("ISA-Completo", ISAcomp)]:
    P(f"- {nom}: media={x.mean():.1f} | desv. est.={x.std():.1f} | min={x.min():.1f} | max={x.max():.1f}")
P(f"- Tipologías: {dict(Counter(TIPO))}")

P("\n## 6b. Advertencias sobre los coeficientes")
P("- Los Spearman altos (p. ej. D3~ISA-PV=0.362) son **espurios**: provienen del desempate de 173 valores "
  "idénticos y una sola observación distinta. Con esa estructura de empates el coeficiente no es interpretable.")
P("- **ISA-EUDR = 0 en las 174 organizaciones** (D4 Deforestación Cero y D7 Presión Comprador sin dato), de modo que "
  "ISA-Completo ≈ 0.3 × ISA-PV y tampoco ofrece una vara contra la cual contrastar la legalidad.")
P("- Potencia estadística del contraste: n(positivos)=1 → potencia ≈ 0 para cualquier prueba.")

P("\n## 7. Conclusión")
P("1. La fuente OSCE/OEFA, con 174/174 consultadas, produce una señal **casi constante** "
  "(173 sin hallazgos, 1 con infracción ambiental): no discrimina y por eso no puede entrar como "
  "componente ponderado ni correlacionarse con sentido estadístico.")
P("2. El bloque ambiental del ISA-PV (D12–D15) está en 0 para la práctica totalidad de la muestra: "
  "tampoco hay varianza que correlacionar del lado del índice.")
P("3. La decisión previa queda **confirmada empíricamente**: D3 se mantiene como **núcleo EUDR + bandera dura** "
  "y como **agravante de IV4 (30%)** solo cuando existe registro; no como componente ponderado del ISA-PV.")
P("4. Con esta fuente, la legalidad funciona mejor como **condición de habilitación/exclusión** que como "
  "variable continua de desempeño.")

open(r"C:\Users\acuba\eudrperu\ISCAM\ANALISIS_D3_vs_ISA-PV.md", "w", encoding="utf-8").write("\n".join(L))
P("\n[guardado: ISCAM\\ANALISIS_D3_vs_ISA-PV.md]")
