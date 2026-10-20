# Contraste D3 (legalidad OSCE/OEFA) ↔ ISA-Pacto Verde

Muestra: 174 organizaciones | fecha de consulta: 2026-10-15

## 1. Distribución de la señal de legalidad (D3)
- 173 orgs D3=1.00 (sin hallazgos) | 1 orgs D3=0.75 (infracción ambiental) | 0 con inhabilitación vigente
- media = 0.9986 | desv. est. = 0.0189 | min = 0.75 | max = 1.00
- **Varianza prácticamente nula** (1 observación distinta de 173): la correlación no es identificable.

## 2. Correlaciones formales (n=174)
| Par | Pearson | Spearman | Varianza del predictor |
|---|---|---|---|
| D3 ~ ISA-PV | -0.052 | 0.362 | var=0.00 |
| D3 ~ D12 Huella Carbono | -0.129 | 0.384 | var=0.19 |
| D3 ~ D13 Reporte Sost. | nan | nan | var=0.00 |
| D3 ~ D14 Econ. Circular | nan | nan | var=0.00 |
| D3 ~ D15 Fitosanitario | nan | nan | var=0.00 |
| D3 ~ Certificación | 0.010 | 0.973 | var=0.01 |

## 3. ¿Tiene varianza el bloque ambiental del ISA-PV?
- D12: media=0.259 | rango=[0.0, 1.0] | valores: 0.0×129, 1.0×45
- D13: media=0.000 | rango=[0.0, 0.0] | valores: 0.0×174
- D14: media=0.000 | rango=[0.0, 0.0] | valores: 0.0×174
- D15: media=0.000 | rango=[0.0, 0.0] | valores: 0.0×174
- ISA-PV (0-1): media=0.029 | rango=[0.0, 0.225] | valores: 0.0×125, 0.125×23, 0.025×11, 0.1×4, 0.225×2, 0.065×1

## 4. Certificación ↔ bloque ambiental (proxies con varianza real)
- Cert ~ ISA-PV (0-1): Pearson=0.206 | Spearman=0.393 | n(Cert>0)=3
- Cert ~ D12 Huella Carbono: Pearson=0.219 | Spearman=0.411 | n(Cert>0)=3
- Cert ~ D13 Reporte Sost.: Pearson=nan | Spearman=nan | n(Cert>0)=3
- Cert ~ D14 Econ. Circular: Pearson=nan | Spearman=nan | n(Cert>0)=3
- Cert ~ D15 Fitosanitario: Pearson=nan | Spearman=nan | n(Cert>0)=3

## 5. Perfil de la única organización con registro de legalidad
- RUC 20136201213 — CENTRAL DE COOPERATIVAS AGRARIAS CAFET: D3=0.75 | Cert=0.00 | D12-D15=[np.float64(1.0), np.float64(0.0), np.float64(0.0), np.float64(0.0)] | ISA-PV=0.07 | IV4=77.5 | IP=0.0 | IV=49.5 | RE=49.5 | tipo=⬜  Riesgo Latente

## 6. Estadísticas del motor (contexto)
- IP (Preparación): media=0.0 | desv. est.=0.0 | min=0.0 | max=0.1
- IV (Vulnerabilidad): media=51.3 | desv. est.=4.6 | min=36.0 | max=64.0
- RE (Exclusión): media=51.3 | desv. est.=4.6 | min=36.0 | max=64.0
- IV4 (cert+legalidad): media=69.4 | desv. est.=5.2 | min=30.0 | max=77.5
- ISA-EUDR: media=0.0 | desv. est.=0.0 | min=0.0 | max=0.0
- ISA-Completo: media=0.9 | desv. est.=1.6 | min=0.0 | max=6.8
- Tipologías: {'🔴  Riesgo Crítico': 158, '⬜  Riesgo Latente': 16}

## 6b. Advertencias sobre los coeficientes
- Los Spearman altos (p. ej. D3~ISA-PV=0.362) son **espurios**: provienen del desempate de 173 valores idénticos y una sola observación distinta. Con esa estructura de empates el coeficiente no es interpretable.
- **ISA-EUDR = 0 en las 174 organizaciones** (D4 Deforestación Cero y D7 Presión Comprador sin dato), de modo que ISA-Completo ≈ 0.3 × ISA-PV y tampoco ofrece una vara contra la cual contrastar la legalidad.
- Potencia estadística del contraste: n(positivos)=1 → potencia ≈ 0 para cualquier prueba.

## 7. Conclusión
1. La fuente OSCE/OEFA, con 174/174 consultadas, produce una señal **casi constante** (173 sin hallazgos, 1 con infracción ambiental): no discrimina y por eso no puede entrar como componente ponderado ni correlacionarse con sentido estadístico.
2. El bloque ambiental del ISA-PV (D12–D15) está en 0 para la práctica totalidad de la muestra: tampoco hay varianza que correlacionar del lado del índice.
3. La decisión previa queda **confirmada empíricamente**: D3 se mantiene como **núcleo EUDR + bandera dura** y como **agravante de IV4 (30%)** solo cuando existe registro; no como componente ponderado del ISA-PV.
4. Con esta fuente, la legalidad funciona mejor como **condición de habilitación/exclusión** que como variable continua de desempeño.