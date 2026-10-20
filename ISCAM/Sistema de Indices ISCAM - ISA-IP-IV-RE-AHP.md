# Sistema de Índices ISCAM — ISA, IP, IV, RE y AHP

**Qué es este documento:** síntesis única de 5 documentos que antes contaban la misma historia en piezas separadas — `Metodologia - Indice de Alineamiento (ISA) y Marco Muestral.md`, `Remapeo D1-D9 a Indice de Preparacion (IP-ISCAM).md`, `Diseno - Indice de Vulnerabilidad (IV-ISCAM).md`, `Comparativa - ISA D1-D11 vs IP-IV-RE ISCAM.md` y `Panel AHP - Diseno de Validacion de Pesos (IP-IV).md`. Esos 5 documentos **no se eliminan** — siguen siendo la fuente de detalle matemático/bibliográfico completo; este documento es el punto de entrada narrativo para quien necesita entender el sistema completo sin leer los 5 por separado.

**El relato en una frase:** el toolkit EUDR (D1–D11) ya es un instrumento de recolección con datos y banderas duras; el proyecto madre ISCAM necesita, además, dos índices (Preparación e Vulnerabilidad) que se combinan en un Riesgo de Exclusión — este documento explica cómo las mismas 73 preguntas de Instrumento 2 alimentan ambos sistemas sin duplicar ni una sola pregunta.

---

## 0. Fundamentos (por qué este diseño, no otro)

- **Modelo de madurez por capacidades** (CMMI) — la escala ordinal 0–4 trata D1–D9 como una escalera, no como puntos acumulables libremente.
- **OECD/JRC Handbook on Constructing Composite Indicators (2008)**, actualizado por Greco, Ishizaka, Tasiou & Torrisi (2019) — estructura de 8 pasos que este sistema sigue de punta a punta.
- **Precedentes sectoriales con la misma arquitectura** (escala + banderas no compensables + agregación que castiga desbalance): SAI Platform FSA, bandas del CDP.
- **Precedentes EUDR/café-cacao específicos (2024–2025):** Grabs (2024/25) sobre construcción de cumplimiento EUDR en café; Team Europe Initiative (2025, Vietnam) con estructura casi idéntica a las 5 sub-dimensiones de IP; estudio Côte d'Ivoire (2025) sobre membresía cooperativa y cumplimiento real, relevante para el objetivo (f).

---

## 1. Por qué dos índices, no uno

El toolkit propio (ISA sobre D1–D11) y el diseño del proyecto madre (IP/IV/RE) **no compiten — resuelven preguntas distintas**:

| | ISA (D1–D11) | IP / IV / RE (ISCAM) |
|---|---|---|
| Fuerte en | Trazabilidad legal artículo por artículo, banderas no compensables (D2.10, D10, trabajo forzoso), 76 preguntas ya redactadas y aplicables | Vulnerabilidad estructural (IV) — ausente en el ISA; operacionalización fina de "impacto en exclusión" vía RE = IV·(1−IP/100); matriz 2×2 de priorización |
| Débil en | No mide vulnerabilidad estructural (dependencia de mercado, fragilidad territorial) | Sin instrumento propio de recolección hasta este remapeo; sin panel de validación de pesos hasta el diseño AHP (§6) |
| Veredicto | **Motor de cumplimiento regulatorio** — de dónde salen los datos y qué hacer cuando algo está mal | **Superestructura analítica** que el proyecto madre necesita para publicar y priorizar |

**Decisión ya ejecutada:** IP se calcula remapeando D1–D9 (§3); IV se diseñó reutilizando la mayoría de las mismas preguntas, invertidas, más 3 preguntas nuevas (§4); las banderas duras del ISA (D2.10, D10, trabajo forzoso) **se mantienen siempre fuera** de IP/IV/RE, reportadas aparte — es la salvaguarda que el diseño ISCAM original no contemplaba.

---

## 2. ISA — Índice Sintético de Alineamiento (D1–D9)

```
Núcleo_i    = ( Π Dim_d,i para d en D1–D7 disponibles )^(1 / n_núcleo_disponibles)     [geométrica]
Extendido_i = Σ Dim_d,i para d en D8–D9 disponibles / n_extendido_disponibles           [aritmética]
ISA_i = 0.875 × Núcleo_i + 0.125 × Extendido_i
```

- **Geométrica en D1–D7:** las dimensiones núcleo no son sustitutas entre sí — un cero en diligencia debida (D5) no se compensa con buena geolocalización (D2). Mismo precedente que el cambio del IDH-PNUD de aritmética a geométrica (2010).
- **Datos faltantes — nunca imputar, re-ponderar** (lógica MNAR, Rubin/Little & Rubin): una dimensión sin respuesta se excluye y las restantes del bloque se re-ponderan proporcionalmente. Umbral mínimo: 7 de 9 dimensiones con ≥70% de sus preguntas de escala respondidas, o la organización no recibe ISA numérico.
- **D10 y D11 nunca se promedian** — D10 es bandera de falsa seguridad, D11 es inventario.
- Detalle matemático completo, ajuste por raking (Deville & Särndal, 1992) y bibliografía: `Metodologia - Indice de Alineamiento (ISA) y Marco Muestral.md` §2–§4.

---

## 3. Remapeo D1–D9 → Índice de Preparación (IP)

Reagrupación pura — ninguna pregunta nueva, ninguna reescrita.

| Sub-dimensión IP | Fuente en D1–D11 | Agregación |
|---|---|---|
| **IP1 · Trazabilidad y origen** | D2 completo | Directa |
| **IP2 · Cumplimiento ambiental** | D3 + D4 | Geométrica √(D3×D4) — requisitos núcleo, no sustituibles |
| **IP3 · Capacidades organizacionales** | D8 + D5 + D6 (parcial) | Aritmética |
| **IP4 · Información y documentación** | D6.23 + D2.9 | Aritmética — sub-dimensión más delgada del remapeo (solo 2 ítems fuente, limitación documentada) |
| **IP5 · Capacidad de adaptación y recursos** | D7 + D9 + D11(recalc.) + Certificaciones(recalc.) | Aritmética |

D1 (clasificación regulatoria) y D10 (bandera) quedan fuera de IP, igual que fuera del ISA. `IP = 0.20 × cada sub-dimensión` (pesos iguales, pendiente AHP §6). Detalle completo: `Remapeo D1-D9 a Indice de Preparacion (IP-ISCAM).md`.

---

## 4. Diseño del Índice de Vulnerabilidad (IV)

A diferencia de IP, IV **sí era un vacío real** — 3 de 5 sub-dimensiones se resolvieron por reúso invertido de preguntas existentes; solo 2 sub-dimensiones necesitaron preguntas nuevas.

| Sub-dimensión IV | Fuente | Tipo |
|---|---|---|
| **IV1 · Dependencia del mercado europeo** | Bloque P (P1/P1b, P4) | Reúso + 1 pregunta nueva (P1b, ya redactada) |
| **IV2 · Exposición regulatoria** | D1 completo | Reúso total, invertido — resuelve el "huérfano" de D1 |
| **IV3 · Fragilidad productiva y territorial** | D3.14 + Bloque 0 (dispersión, distancia, tamaño de parcela derivado) | Reúso + 2 preguntas nuevas (ya redactadas) |
| **IV4 · Brechas tecnológicas y financieras** | D6.24 + D9, invertidos | Reúso total — el mejor caso de reúso identificado |
| **IV5 · Riesgo social y comercial** | D7 (invertido) + fricción D8 + % mujeres en directiva | Reúso parcial + 1 pregunta nueva |

`IV = 0.20 × cada sub-dimensión` (pesos iguales, pendiente AHP §6). Las 5 sub-dimensiones son calculables desde el primer piloto — no queda ninguna huérfana de dato. Detalle completo: `Diseno - Indice de Vulnerabilidad (IV-ISCAM).md`.

---

## 5. Riesgo de Exclusión (RE) y matriz de tipología

```
RE_c = IV_c · (1 − IP_c/100)
```

Una cooperativa muy vulnerable (IV alto) pero muy preparada (IP alto) tiene RE bajo — la preparación *modera* la vulnerabilidad (Hipótesis 3 del proyecto madre). RE ubica a cada cooperativa en una matriz 2×2 (IP alto/bajo × IV alto/bajo) con 4 cuadrantes de priorización, el más crítico siendo IP bajo + IV alto ("riesgo crítico de exclusión"). El corte alto/bajo se fija con la mediana muestral del primer piloto real, no arbitrariamente.

**Diagrama completo del flujo (10 sub-dimensiones → IP/IV → RE → matriz de tipología):** https://claude.ai/code/artifact/5ef7f6b8-fb82-4d18-a356-be5580871d5b

---

## 6. Panel AHP — validación de pesos

El 20% parejo por sub-dimensión (§3, §4) es un valor predeterminado, no una decisión final. El panel AHP (Saaty 1980) lo reemplaza con pesos derivados de comparaciones pareadas de 8–10 expertos (5 grupos: EUDR/legal, gremios/cooperativas, certificación, cooperación técnica, académico ISCAM), en dos matrices 5×5 independientes (IP y IV — nunca un peso relativo IP-vs-IV, porque esa relación ya está fija en RE).

**El punto donde más se falla:** agregar las matrices de los expertos por **media geométrica elemento-por-elemento (método AIJ)**, nunca promediando los pesos ya calculados de cada experto por separado (método AIP) — Forman & Peniwati (1998). Sensibilidad obligatoria: correlación de Spearman entre ordenamiento con pesos AHP y ordenamiento con pesos iguales.

**Diagrama completo del proceso (6 pasos, con el contraste AIJ vs. AIP):** https://claude.ai/code/artifact/fdf332b1-897d-43ad-b182-0bda5465067a
**Instrumento de captura ya construido:** https://claude.ai/code/artifact/323b416c-1678-4fd0-a5c9-b02b7d874f1e

Panel real **aún no convocado** — depende del equipo del proyecto madre (Fase 0 del plan a 75 días). Detalle completo: `Panel AHP - Diseno de Validacion de Pesos (IP-IV).md`.

---

## 7. Validación de robustez

- **Consistencia interna:** alfa de Cronbach por dimensión D1–D9 (umbral 0.6).
- **Estructura multivariada:** PCA sobre D1–D9 una vez exista la primera ronda completa de datos — si el primer componente explica una fracción alta de la varianza, los pesos iguales son razonables.
- **Sensibilidad a la agregación:** aritmética simple vs. geométrica híbrida — cuántas organizaciones cambian de cuartil.
- **Sensibilidad a los pesos:** pesos iguales vs. pesos AHP — correlación de Spearman.
- **Sensibilidad a datos faltantes:** exclusión estricta vs. re-ponderación proporcional.
- **Bootstrap** (estándar ISCAM, ausente en el diseño original del ISA) — pendiente de adoptar para robustez adicional exigible en publicación Q1/Q2.

---

## 8. Lista de verificación de 6 pilares para publicación Q1/Q2 (auto-evaluación, criterio propio de ISCAM)

| Pilar | Estado |
|---|---|
| Validez conceptual | Parcial — Instrumento 1/7 justifican cada dimensión; falta panel Delphi/CVI formal |
| Triangulación de datos | **Cubierto** — fuentes de verificación oficiales ya en Instrumento 3 (GEOSERFOR, SINIA, OEFA, SENASA, BDPI, fajas marginales, SUNAT/VUCE) |
| Ponderación explícita | Parcial — pesos iguales justificados (OECD/JRC); falta ejecutar el panel AHP (§6) |
| Robustez empírica | Parcial — Cronbach y Spearman definidos; falta bootstrap |
| Validación externa | Parcial — los 4 criterios ISCAM (certificaciones, % volumen trazable, continuidad exportadora, acceso a mercado UE) ya tienen pregunta en Bloque P; falta la correlación empírica real contra IP/RE, que requiere datos del piloto |
| Aplicación para política pública | Débil — no articulado explícitamente qué decisión de terceros (gremio, cooperante, gobierno regional) alimenta cada pieza |

---

## 9. Pendientes reales (consolidado de los 5 documentos fuente)

- [ ] Convocar el panel AHP real — bloqueado en el equipo del proyecto madre (Fase 0 del plan a 75 días).
- [x] **Pregunta de "% volumen trazable" — cerrado 2026-09-17.** P11 en Bloque P.
- [x] **Pregunta de "continuidad exportadora" — cerrado 2026-09-17.** P12 en Bloque P.
- [x] **Fracción de D8 que cuenta como "fricción" para IV5 — cerrado 2026-09-17.** D8.30 invertida (100 − D8.30); ver `Diseno - Indice de Vulnerabilidad (IV-ISCAM).md`.
- [x] **Bootstrap adoptado como estándar de robustez — cerrado 2026-09-17** (regla documentada en Metodología ISA §4; ejecución espera datos reales del piloto).
- [ ] Fijar el corte alto/bajo de la matriz de tipología 2×2 — depende de datos reales del piloto (Fase 2/3 del plan a 75 días). Único ítem que sigue bloqueado por falta de datos, no por decisión pendiente.
- [x] **Territorio como nivel de agregación con puntaje propio — cerrado 2026-09-17.** Regla `RE_territorio = promedio(RE_c)` documentada en Metodología ISA §5; ejecución espera datos reales.

---

## 10. Mapa de navegación — dónde está cada pieza

| Necesitas... | Ve a |
|---|---|
| El detalle matemático completo y la bibliografía del ISA | `Metodologia - Indice de Alineamiento (ISA) y Marco Muestral.md` |
| El detalle completo del remapeo a IP | `Remapeo D1-D9 a Indice de Preparacion (IP-ISCAM).md` |
| El detalle completo del diseño de IV | `Diseno - Indice de Vulnerabilidad (IV-ISCAM).md` |
| La comparación exhaustiva ISA vs. IP/IV/RE, criterio por criterio | `Comparativa - ISA D1-D11 vs IP-IV-RE ISCAM.md` |
| El diseño completo del panel AHP (composición, procedimiento) | `Panel AHP - Diseno de Validacion de Pesos (IP-IV).md` |
| Qué pregunta exacta de Instrumento 2 alimenta qué sub-dimensión, pregunta por pregunta | Matriz de Cobertura Técnica — [por dimensión](https://claude.ai/code/artifact/ab244f2a-176d-454e-94b4-3f97d691fe9b) / [por pregunta](https://claude.ai/code/artifact/c832a3c4-8a7c-46ef-9ce2-d569c076d60b) |
| Ficha técnica, guía metodológica y guía de llenado del instrumento | `Ficha Tecnica y Guia de Aplicacion - Instrumento 2.md` |

---

**Estado:** documento de trabajo, 2026-09-17. Reemplaza a los 5 documentos fuente como punto de entrada — esos 5 siguen existiendo y no se editaron en esta síntesis (a diferencia de la consolidación de la Ficha Técnica, aquí no hubo contenido duplicado que recortar: cada documento fuente ya cubría un tramo distinto de la misma cadena, este documento solo los enhebra).
