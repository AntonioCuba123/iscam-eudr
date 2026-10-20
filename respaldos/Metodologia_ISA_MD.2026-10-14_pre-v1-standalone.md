# Metodología — Índice Sintético de Alineamiento (ISA) y Marco Muestral (café/cacao)

> **Nota de ubicación (2026-10-01):** el `Instrumento 7 - Evaluacion Critica y Elementos Adicionales.md` fue trasladado de `ISCAM\` a `Instrumentos\`, donde ahora-convive con el resto del paquete. Las referencias a "Instrumento 7" en este documento apuntan a `..\Instrumentos\Instrumento 7 - Evaluacion Critica y Elementos Adicionales.md`.

**Qué resuelve este documento:** operacionaliza, para el universo café/cacao (100–150 organizaciones), la metodología cuantitativa que el proyecto madre (`El impacto del Pacto Verde Europeo en la performance de las cooperativas peruanas.pdf`, ISCAM-Universidad del Pacífico) exige: encuesta tipo PRODUCE/CENACOOP adaptada, escala ordinal 0–4, **Índice Sintético de Alineamiento (ISA) completo del Pacto Verde** con cinco módulos — (i) huella de carbono, (ii) deforestación/trazabilidad, (iii) diligencia debida DD.HH./ambiente, (iv) reporte de sostenibilidad, (v) economía circular/envases — reglas de datos faltantes y validación de robustez, muestreo no probabilístico por cuotas, y ajustes ex-post de representatividad.

**Alcance actualizado (2026-10-09):** el toolkit EUDR (D1–D11) cubre en profundidad los módulos **(ii) deforestación/trazabilidad** y **(iii) diligencia debida** — y desde 2026-10-08 incluye los módulos (i), (iv) y (v) como dimensiones extendidas D12, D13, D14. **Desde 2026-10-09 se agrega el módulo (vi) Farm to Fork como dimensión D15 (Gestión fitosanitaria y LMR)**, cerrando el sesgo de cobertura hacia café en D12 (D15 aplica por igual a café y cacao) y capturando el pilar del Pacto Verde con mayor impacto operativo inmediato después del EUDR. El ISA completo del Pacto Verde se compone de:
- **ISA-EUDR (submódulos ii+iii)**: D1–D9 (núcleo D1–D7 geométrico 87.5% + extendido D8–D9 aritmético 12.5%) — índice de madurez regulatoria EUDR.
- **ISA-PactoVerde (módulos i+iv+v+vi)**: D12 (huella carbono), D13 (reporte sostenibilidad), D14 (economía circular), **D15 (fitosanitarios/LMR)** — media aritmética simple por dimensión, luego media aritmética entre las cuatro.
- **ISA-Completo**: 0.7 × ISA-EUDR + 0.3 × ISA-PactoVerde (pesos por validar en piloto; reflejan que el acceso al mercado UE lo decide el EUDR, pero la competitividad de largo plazo depende del Pacto Verde completo).

**Actualización 2026-09-16 — el módulo (i) huella de carbono ya no necesita construirse desde cero para café.** Se identificó **CalCafé v2.1** (`manual-uso-2021-calcafe-v2-1.pdf`, PromPerú / PUCP-PELCAN), una calculadora de Análisis de Ciclo de Vida ya validada (ISO 14040/44, metodología PEFCR de la Comisión Europea) que computa huella de carbono y huella hídrica del café peruano de exportación en 8 categorías de impacto, con comparación contra otros países productores. Es gratuita y pública. **Limitación real: solo cubre café, no cacao** — para el módulo de huella de carbono en cacao sí haría falta desarrollar o adaptar un instrumento aparte. **Actualización 2026-10-08:** el Instrumento 2 ya incluye D12 (5 preguntas) operacionalizando este módulo; para cacao se puntúa según producto principal y se anota la brecha.

**Actualización 2026-10-08 — módulos (iv) y (v) incorporados:** D13 (reporte de sostenibilidad, 6 preguntas, alineado CSRD/ESRS/taxonomía) y D14 (economía circular/envases, 5 preguntas, alineado Plan Acción Economía Circular UE, PPWR) ya están en el Instrumento 2. No existía instrumento previo identificado para estos módulos; el toolkit EUDR los cubre ahora como dimensiones extendidas del Pacto Verde.

**Actualización 2026-10-14 — Instrumento 2 v0.4 reforzado y su reflejo en la hoja de cálculo.** El Instrumento 2 pasó de 89 a **119 preguntas** (116 de instrumento + 3 metadata) cerrando los huecos de correspondencia con `PLANTILLA_INDICE_PVE_ISCAM.xlsx` detectados en el análisis inverso: 13 variables del proxy de verificación rápida que no tenían pregunta, 4 columnas D12–D15 en cero (30% de ISA-Completo), 10 indicadores PVE sin fuente y 3 campos de ficha (tipo de organización, departamento, RNCA). Detalle pregunta por pregunta con su celda destino en la nueva pestaña `INSTRUMENTO_2_PREGUNTAS` de la hoja de cálculo y en el Anexo v0.4 del documento del Form. Las preguntas **D12.42, D13.45, D14.51 y D15.58** son la versión mínima (escala 0/1/2) del módulo Pacto Verde cuyo rango `D12.40–D15.60` ya estaba reservado en la Google Sheet; las 17 preguntas restantes de ese módulo quedan pendientes de evaluación de comprensibilidad con el técnico de campo. Lo operativo del índice (IP, IV, RE, tipología 2×2, ISA-PV, P_Global, ponderaciones PVE) se documenta en la nueva §7 de este documento.

---

## 0. Fundamentos metodológicos (por qué este diseño, no otro)

Este ISA combina dos tradiciones metodológicas reales, no elecciones ad hoc:

- **Modelos de madurez por capacidades** — la escala ordinal 0–4 del Instrumento 2 replica la lógica del **Capability Maturity Model Integration (CMMI, SEI/Carnegie Mellon)**: los niveles no son intercambiables, cada uno presupone que el anterior ya está resuelto. Esto es lo que justifica tratar D1–D9 como una escalera, no como puntos acumulables libremente.
- **Construcción de indicadores compuestos** — el proceso de 8 pasos del ***OECD/JRC Handbook on Constructing Composite Indicators* (2008)** (marco teórico → datos → datos faltantes → análisis multivariado → normalización → ponderación/agregación → robustez → vinculación con otras variables) es la estructura que sigue este documento de punta a punta; es la referencia que usan Eurostat y el Banco Mundial para este mismo tipo de índice. **Actualización 2026-09-16:** Greco, Ishizaka, Tasiou & Torrisi (2019), *"On the Methodological Framework of Composite Indices: A Review of the Issues of Weighting, Aggregation, and Robustness"* (*Social Indicators Research*, 141), es la revisión que actualiza ese mismo Handbook con más de una década de crítica metodológica adicional sobre ponderación, agregación y robustez — se cita aquí como respaldo complementario, no como reemplazo, porque confirma que las tres decisiones más discutidas de este documento (agregación geométrica, raking, PCA como chequeo posterior) siguen siendo las prácticas recomendadas en la literatura más reciente, no solo en el Handbook de 2008.

Precedentes sectoriales reales con la misma arquitectura (escala ordinal + preguntas "bandera" no compensables + agregación que castiga el desbalance): el **SAI Platform Farm Sustainability Assessment (FSA)** — el instrumento de referencia mundial para evaluar sostenibilidad a nivel de finca/cooperativa, usado por compradores como Nestlé y Unilever, con niveles Bronce/Plata/Oro y preguntas obligatorias no compensables — y las **bandas de letra del CDP (Carbon Disclosure Project)**, construidas sobre puntajes ponderados con la misma filosofía. Este diseño no es una particularidad del toolkit EUDR; es el estándar de facto para este tipo de instrumento.

**Precedentes específicos de EUDR/café-cacao (2024-2025, más recientes que el diseño original de este documento):**
- Grabs, J., *"The Construction of Compliance with the European Union Deforestation Regulation in Global Coffee Value Chains"* (*Regulation & Governance*, Wiley, 2024/2025) — analiza directamente cómo se construye el cumplimiento del EUDR en cadenas de café; es el precedente más específico al caso de todos los citados en este documento.
- Team Europe Initiative on Deforestation-free Value Chains (2025), evaluación de preparación EUDR en café/caucho/madera en Vietnam, medida en trazabilidad, legalidad, capacidad técnica y capacidad financiera — un precedente aplicado casi idéntico en estructura a las 5 sub-dimensiones de IP definidas en el Remapeo D1-D9→IP.
- ScienceDirect (2025), *"Can cooperative membership foster compliance with New European Union regulations on deforestation-free production? Evidence from cocoa farmers in Western Côte d'Ivoire"* — estudio empírico que cruza pertenencia a cooperativa con cumplimiento EUDR real, directamente relevante para el objetivo (f) de performance del proyecto madre y para validar el Bloque P.

---

## 1. Marco muestral

**Este documento ya no es la fuente primaria del marco muestral.** Universo, unidad de análisis, tamaño de muestra, estratos de cuota y estado actual del marco viven en `Ficha Tecnica y Guia de Aplicacion - Instrumento 2.md` §1.2–§1.3 — consultar ahí. Lo que sigue en esta sección 1 es únicamente lo que **no** está en esa ficha: el detalle del piloto de comprensibilidad del instrumento (distinto del piloto de campo de la Fase 2 del plan a 75 días, que valida el despliegue completo, no solo la redacción de las preguntas).

### 1.1 Piloto de comprensibilidad del instrumento

Antes o durante el levantamiento de las 100–150 organizaciones, evaluar en una submuestra que cubra al menos 3 de las 4 celdas de mayor incidencia esperada: comprensibilidad de las preguntas, tiempo de aplicación, y tasa de no-respuesta por ítem. Ajustar el instrumento si algún ítem muestra no-respuesta >20%.

---

## 2. Construcción del Índice Sintético de Alineamiento (ISA)

### 2.1 Fuente de datos

El **ISA-EUDR** (submódulos ii+iii) se calcula exclusivamente sobre **D1–D9 del Instrumento 2** (escala 0–4 por pregunta, ya definida). D10 y D11 **no entran al ISA-EUDR** — se reportan aparte, como ya lo especifica el propio Instrumento 2 en su "Nota de puntaje" y el Instrumento 7: D10 es una bandera de falsa seguridad (un puntaje alto sería mala noticia) y D11 es un inventario de cobertura, no una medida de madurez. Meterlos al índice sintético invalidaría su interpretación.

El **ISA-PactoVerde** (módulos i+iv+v+vi) se calcula sobre **D12, D13, D14, D15 del Instrumento 2** (escala 0–4 por pregunta). D15 es nueva (2026-10-09) y cubre: (vi) gestión fitosanitaria y LMR (Farm to Fork). Aplica por igual a café y cacao, cerrando el sesgo de D12 que dependía de CalCafé v2.1 (solo disponible para café).

El **ISA-Completo** combina ambos:

```
ISA_Completo_i = 0.70 × ISA_EUDR_i + 0.30 × ISA_PactoVerde_i
```

Los pesos (70/30) reflejan que: (a) el acceso al mercado UE lo decide el cumplimiento EUDR (D1–D9), y (b) la competitividad de largo plazo y alineación con el Pacto Verde completo requieren los módulos i, iv, v. **Pesos a validar con el piloto (§4 — análisis de sensibilidad).**

### 2.2 Normalización por dimensión

Para cada dimensión *d* (D1…D9) de la organización *i*:

```
Dim_d,i = (promedio de respuestas 0–4 en las preguntas escala/porcentaje de esa dimensión, excluyendo texto libre y mapeo) / 4 × 100
```

Resultado: cada dimensión queda en escala 0–100, comparable entre sí antes de ponderar.

### 2.3 Ponderación y agregación

**ISA-EUDR (D1–D9) — Pesos (a validar con el piloto, ver §4 — análisis de sensibilidad):**

- **D1–D7 (dimensiones núcleo, derivadas directamente del texto del reglamento):** peso igual entre sí → 87.5% del ISA-EUDR.
- **D8–D9 (dimensiones extendidas — gobernanza y sostenibilidad económica):** peso igual entre sí → 12.5% del ISA-EUDR.

**Regla de agregación — corregida el 2026-09-16, de aritmética a geométrica híbrida.** La versión anterior de este documento promediaba D1–D9 con una media aritmética ponderada. Eso permite **sustitución perfecta** entre dimensiones: una cooperativa con D2 (trazabilidad) en 4 pero D5 (diligencia debida) en 0 saldría con un ISA "aceptable" a pesar de no tener ningún sistema de diligencia debida — exactamente el tipo de brecha crítica que el Instrumento 4 necesita ver, no esconder. El precedente que corrige esto es el propio **Índice de Desarrollo Humano del PNUD**: hasta 2009 usaba media aritmética; desde el *Informe de Desarrollo Humano 2010* usa **media geométrica**, documentando que penaliza el desbalance entre dimensiones porque estas no son sustitutos entre sí. Las dimensiones EUDR tampoco lo son: el reglamento no permite compensar la ausencia de diligencia debida con buena geolocalización.

Con la salvedad de que la media geométrica exige valores > 0 (un cero anula el producto completo — deseable en D1–D7, excesivo en D8–D9, que son moduladoras y no deberían anular el índice por sí solas), se agrega en dos niveles:

```
Núcleo_i     = ( Π (D1_i × D2_i × D3_i × D4_i × D5_i × D6_i × D7_i) )^(1/7)      [media geométrica, D1–D7, cada Dim_d,i en 0–100]
Extendido_i  = (D8_i + D9_i) / 2                                                [media aritmética, D8–D9]

ISA_EUDR_i = 0.875 × Núcleo_i + 0.125 × Extendido_i
```

**ISA-PactoVerde (D12–D15) — Agregación aritmética simple (módulos i, iv, v, vi son complementarios, no sustitutos estrictos):**

```
D12_i = promedio preguntas D12 (0–100)
D13_i = promedio preguntas D13 (0–100)
D14_i = promedio preguntas D14 (0–100)
D15_i = promedio preguntas D15 Q56–Q59 (0–100)  [Q60 es bandera independiente, no entra al promedio]

ISA_PactoVerde_i = (D12_i + D13_i + D14_i + D15_i) / 4
```

**ISA-Completo:**

```
ISA_Completo_i = 0.70 × ISA_EUDR_i + 0.30 × ISA_PactoVerde_i
```

**Justificación del esquema de pesos entre bloques:** las dimensiones núcleo EUDR determinan directamente el acceso al mercado (lo que el reglamento exige textualmente); las extendidas EUDR (D8–D9) son moduladoras de sostenibilidad del cumplimiento en el tiempo (Instrumento 7, §2). Los cuatro módulos PactoVerde (D12–D15) son complementarios entre sí (la huella de carbono informa el reporte, la circularidad reduce la huella, el control fitosanitario protege el acceso al mismo mercado que el EUDR) y no anulan el acceso al mercado por sí solos — por eso media aritmética entre ellos y peso 30% en el compuesto final. El esquema de pesos iguales *dentro* de cada bloque sigue siendo el default recomendado por el OECD/JRC Handbook en ausencia de un proceso de consenso de expertos (Delphi, o Analytic Hierarchy Process de Saaty) — no se recomienda un esquema de pesos "de experto" sin esa validación, que hoy no existe en el proyecto. Una vez haya datos reales del piloto, correr un **Análisis de Componentes Principales (PCA)** sobre D1–D15 como chequeo de robustez (§4): si el primer componente explica una fracción alta de la varianza, los pesos iguales son razonables; si dos dimensiones aparecen altamente correlacionadas, están sobre-representando un mismo fenómeno en el índice y el esquema debe ajustarse.

---

### 2.4 Reglas de datos faltantes

**Por qué no se imputa:** la tipología clásica de datos faltantes (**Rubin, 1976**; **Little & Rubin, 2002, *Statistical Analysis with Missing Data***) distingue MCAR (al azar), MAR (al azar condicional a otras variables observadas) y MNAR (no al azar — la ausencia depende del propio valor no observado). Una dimensión completa sin respuesta es, con alta probabilidad, **MNAR**: una cooperativa sin sistema de diligencia debida tiene más probabilidad de no poder responder D5 que una que sí lo tiene. Imputar con la media muestral en un caso MNAR sesga el índice hacia arriba exactamente donde debería mostrar el vacío — por eso la regla aquí es re-ponderar, nunca imputar.

- **Umbral mínimo para ISA-EUDR:** al menos 7 de las 9 dimensiones D1–D9 deben tener al menos el 70% de sus preguntas de escala respondidas. Si no se cumple, la organización **no recibe ISA-EUDR numérico** — se reporta como "diagnóstico EUDR incompleto".
- **Umbral mínimo para ISA-PactoVerde:** al menos 3 de las 4 dimensiones D12–D15 deben tener al menos el 70% de sus preguntas respondidas. Si no se cumple, **no recibe ISA-PactoVerde** — se reporta como "diagnóstico PactoVerde incompleto".
- **Para ISA-Completo:** se requiere que ambos sub-índices (ISA-EUDR e ISA-PactoVerde) sean calculables. Si uno falla, se reporta el que sí se pudo calcular y se anota la brecha.
- **Dimensión con respuesta parcial (≥70% pero <100%):** promediar sobre las preguntas efectivamente respondidas de esa dimensión (no imputar).
- **Dimensión totalmente ausente (0% respondida) en una organización que sí alcanza el umbral general:** excluir esa dimensión del cálculo y **re-ponderar proporcionalmente** las dimensiones restantes de su mismo bloque (núcleo o extendido) antes de aplicar la media geométrica/aritmética de ese bloque.
- **Distinguir "ausente" de "cero real":** una dimensión sin respuesta se excluye y re-pondera (arriba); una dimensión **respondida con puntaje 0 real** (la organización sí contestó y su nivel de madurez es 0) se mantiene en el cálculo y, en el bloque núcleo (geométrico), anula el producto — es la señal exacta que la media geométrica está diseñada para mostrar (§2.3). No confundir ambos casos en la base de datos: son semánticamente distintos.
- Reportar junto a cada ISA el **N° de dimensiones efectivamente usadas** (7, 8 o 9 para EUDR; 2, 3 o 4 para PactoVerde) para que la comparación entre organizaciones sea transparente.

### 2.5 Fórmula final por organización

**ISA-EUDR:**
```
Núcleo_i    = ( Π Dim_d,i para d en D1–D7 disponibles )^(1 / n_núcleo_disponibles)
Extendido_i = Σ Dim_d,i para d en D8–D9 disponibles / n_extendido_disponibles

ISA_EUDR_i = 0.875 × Núcleo_i + 0.125 × Extendido_i     (si D8–D9 ambas ausentes, ISA_EUDR_i = Núcleo_i)
```

**ISA-PactoVerde:**
```
D12_i = promedio preguntas D12 (0–100)
D13_i = promedio preguntas D13 — incluye Q44b + Q45–Q50 (0–100)
D14_i = promedio preguntas D14 (0–100)
D15_i = promedio preguntas D15 Q56–Q59 (0–100)  [Q60 es bandera independiente, no entra al promedio]

ISA_PactoVerde_i = (D12_i + D13_i + D14_i + D15_i) / 4     (si alguna dimensión ausente y no alcanza umbral mínimo, no se calcula)
```

**Umbral mínimo para ISA-PactoVerde (actualizado 2026-10-09):** al menos 3 de las 4 dimensiones D12–D15 deben tener al menos el 70% de sus preguntas respondidas.

**ISA-Completo:**
```
ISA_Completo_i = 0.70 × ISA_EUDR_i + 0.30 × ISA_PactoVerde_i
```

---

## 3. Ajuste por representatividad (ex-post)

Como la muestra es no probabilística por cuotas, reportar el ISA en dos versiones, siguiendo el mismo enfoque del proyecto madre (Deville & Särndal, 1992; calibración/ranking):

1. **ISA sin ajustar** — el calculado en §2.5 sobre la muestra lograda, tal cual.
2. **ISA calibrado por raking — corregido el 2026-09-16, de post-estratificación por celda a ajuste proporcional iterativo (raking).** La versión anterior proponía post-estratificación simple (reponderar cada celda Producto × Tamaño × Territorio al peso poblacional real). El problema: con 100–150 organizaciones repartidas en ~24 celdas posibles, muchas celdas tendrán 2–3 observaciones — ahí la post-estratificación por celda da pesos inestables (una sola organización puede terminar representando 30% de su celda). La solución estándar cuando solo se conocen los **totales marginales** (cuántas organizaciones hay por producto, por tamaño, por región — no necesariamente el cruce completo, que JNC/APPCACAO/MIDAGRI/CENAGRO probablemente no entreguen combinado) es **raking**, formalizado en **Deville & Särndal (1992, "Calibration Estimators in Survey Sampling")** — la misma referencia que el proyecto madre ya cita en su propia bibliografía — y recomendado explícitamente por **AAPOR (2013)** para muestras no probabilísticas por cuotas en esta situación exacta: se ajustan los pesos muestrales para que coincidan con cada margen por separado (Producto, Tamaño, Territorio), sin necesitar la celda cruzada completa.
3. Reportar la diferencia entre ISA sin ajustar y calibrado como **análisis de sensibilidad**, no como corrección definitiva — si la diferencia es grande, es señal de que la cuota lograda se alejó del universo real y debe documentarse como limitación, no ocultarse (**Bethlehem, 2010**, sobre sesgo de selección en encuestas no probabilísticas).

---

## 4. Validación de robustez

- **Consistencia interna por dimensión:** calcular alfa de Cronbach (**Cronbach, 1951**) para las preguntas de escala dentro de cada dimensión **D1–D15** con los datos del piloto (§1.1) y de la primera ronda completa. Un alfa <0.6 en alguna dimensión es señal de que sus preguntas no miden un mismo constructo — revisar redacción antes de escalar.
- **Estructura multivariada (PCA) como chequeo de los pesos:** correr un Análisis de Componentes Principales sobre **D1–D15** con los datos de la primera ronda completa (el piloto de 5–8 casos no alcanza para esto). Si el primer componente explica una fracción alta de la varianza total, el supuesto de pesos iguales es razonable; si dos dimensiones aparecen altamente correlacionadas, están capturando el mismo fenómeno y el esquema de pesos de §2.3 debe revisarse — este es el paso de "análisis multivariado" que el OECD/JRC Handbook ubica antes de fijar la ponderación definitiva (aquí se hace como validación posterior porque no hay datos reales todavía, ver §0).
- **Sensibilidad al esquema de agregación (ISA-EUDR):** recalcular el ISA-EUDR con (a) media aritmética simple en D1–D9 (el método original, ya descartado en §2.3) y (b) la media geométrica híbrida vigente, y reportar cuántas organizaciones cambian de cuartil entre ambos métodos. Se espera que el método aritmético "esconda" organizaciones con una dimensión núcleo en 0 que la geométrica expone — documentar cuántos casos son estos, es el hallazgo que justifica el cambio de método frente a cualquier revisor.
- **Sensibilidad al esquema de pesos entre bloques (ISA-EUDR):** recalcular el ISA-EUDR con pesos iguales entre las 9 dimensiones (11.1% cada una, ambas en aritmética simple para que la comparación sea limpia) vs. el esquema de §2.3, y reportar la correlación de rangos (Spearman) entre ambos. Si Spearman <0.85, el esquema de pesos importa y debe justificarse más allá del default de este documento.
- **Sensibilidad al peso ISA-Completo (70/30):** recalcular ISA-Completo con pesos alternativos (ej. 80/20, 60/40, 50/50) y reportar correlación de rangos (Spearman) vs. el esquema 70/30. Si Spearman <0.85 en cualquier comparación, el peso entre submódulos importa y debe justificarse.
- **Sensibilidad a la regla de datos faltantes:** recalcular excluyendo por completo a las organizaciones con alguna dimensión ausente (regla estricta) vs. la regla de re-ponderación proporcional (§2.4), y reportar cuántas organizaciones cambian de cuartil del ISA-EUDR e ISA-Completo entre ambos métodos.
- **Bootstrap — adoptado como estándar 2026-09-17.** Remuestreo con reemplazo (B=1000 iteraciones recomendadas) sobre la muestra piloto, para construir intervalos de confianza del ISA-EUDR, ISA-PactoVerde, ISA-Completo, IP, IV, RE por cooperativa y del ranking agregado. Es el estándar de robustez que ya exige el proyecto madre ISCAM (checklist de 6 pilares Q1/Q2, ver `Sistema de Indices ISCAM - ISA-IP-IV-RE-AHP.md` §8) y que el diseño original de este documento no tenía — se adopta explícitamente aquí para igualar esa exigencia. Ejecutar una vez exista la primera ronda completa de datos reales (no aplica al piloto de 5–8 casos de §1.1, la muestra es insuficiente para bootstrap).

---

## 5. Tipologías comparativas y conexión con el objetivo de performance

- Cruzar el ISA (ajustado) contra: producto (café/cacao/ambos), vía de exportación (directa/indirecta), tamaño, territorio — igual que pide el proyecto madre para sus "tipologías comparativas por sector, territorio y tamaño".
- **Territorio como nivel de agregación propio, no solo variable de estrato — decidido 2026-09-17.** Hasta ahora Territorio (Norte/Centro/Sur) solo se usaba como celda de cuota para el muestreo (§1). ISCAM lo trata como un nivel de agregación con score propio, dentro de la cadena parcela→productor→cooperativa→**territorio**→cadena de valor. Se adopta esa misma lógica: además del ISA/IP/IV/RE por cooperativa, reportar `RE_territorio = promedio(RE_c)` de las cooperativas de cada macro-región, una vez exista la primera ronda de datos reales. Esto habilita directamente la aplicación de "seguimiento territorial" (uno de los 5 usos de la matriz de tipología) — permite a un gobierno regional o a la cooperación internacional decidir dónde concentrar esfuerzo geográficamente, no solo por cooperativa individual.
- **Para el objetivo específico (f) del proyecto madre** ("medir el impacto de la adecuación al PVE en la performance") — el ISA de este documento es el **regresor/predictor**, no la performance en sí. **Actualización 2026-09-16:** la variable de performance ya tiene una versión preliminar — ver **Bloque P** del `Instrumento 2 - Encuesta Cuantitativa.md` (volumen exportado a la UE y su variación, N° de compradores europeos activos y su variación, precio pagado al socio y su variación, incidencia de rechazos/pérdida de contratos). Es v0.1, pendiente de validar con el equipo del proyecto madre (Checklist, Tarea D1) antes del piloto definitivo, pero ya permite ejecutar el piloto de la Tarea C sin bloquear por falta de instrumento.
- **Modelo de análisis propuesto una vez existan datos reales:** dado el diseño transversal, reportar (a) correlación simple ISA↔cada indicador de performance actual (P1, P3, P4, P6), (b) comparación de cuartiles de ISA vs. cuartiles de performance, y (c) para las variables retrospectivas (P2, P5, P7), la variación calculada como proxy de tendencia — dejando explícito en cualquier entregable que esto es asociación transversal con recall retrospectivo, no un panel real ni prueba de causalidad.

---

## 6. Vínculo con el resto del toolkit

- **Ficha técnica del instrumento (universo, muestra, quién responde):** `Ficha Tecnica y Guia de Aplicacion - Instrumento 2.md` §1 — fuente única desde 2026-09-17, ya no duplicada aquí.
- Fuente de datos: **Instrumento 2** (v3 actualizado 2026-10-09, **D1–D15**).
- Reglas de exclusión de D10/D11: ya definidas en **Instrumento 2** (Nota de puntaje) e **Instrumento 7** — D10/D11 no promedian en ISA-EUDR; D12/D13/D14/D15 no promedian en ISA-EUDR pero sí en ISA-PactoVerde.
- Muestra: cruza con el **Instrumento 5** (triaje) para decidir a qué organizaciones aplicar el diagnóstico integral (**D1–D15** + entrevista) vs. solo el núcleo (**D1–D9** para el ISA-EUDR).
- Informantes y aplicación: **Instrumento 6** y **Protocolo de Aplicacion - Tarea B**. D12: gerencia + responsable técnico/calidad; D13: gerencia + comunicación/transparencia; D14: gerencia + operaciones/beneficio; **D15: gerencia + responsable técnico de campo** (quien conoce los protocolos fitosanitarios y los resultados de análisis de residuos).
- Universo café/cacao ya parcialmente cubierto por la encuesta de campo (form v2) — ver **Puente**, que debe actualizarse para indicar qué organizaciones de la muestra ISA ya tienen datos D2–D4 de campo y solo faltan D1/D5–D9 de directiva; D12–D14 requieren aplicación completa del Instrumento 2 a la cooperativa.

**Pendiente para completar el ISA como entregable:** (a) ejecutar el piloto (§1.1), (b) obtener los totales poblacionales auxiliares de JNC/APPCACAO/MIDAGRI/CENAGRO para la calibración (§3), y (c) definir con el equipo del proyecto madre la variable de performance del objetivo (f), que este documento deja explícitamente fuera de su alcance.

---

## 7. Implementación del índice en la hoja de cálculo `PLANTILLA_INDICE_PVE_ISCAM.xlsx` (2026-10-14)

Esta sección documenta cómo se operacionaliza la metodología de las §§2–3 en la hoja de cálculo que clasifica a las 174 organizaciones del marco muestral. Es el puente entre el método descrito arriba y las celdas donde efectivamente se calcula.

### 7.1 Arquitectura de la hoja de cálculo

| Pestaña | Rol | Contenido |
|---|---|---|
| `INSTRUCCIONES` | Gobernanza del uso | Flujo de 5 pasos, definición del semáforo (Crítico 0–33 / Vulnerable 34–66 / Preparado 67–100) |
| `INSTRUMENTO_2_PREGUNTAS` **(nueva, v0.4)** | Puente Form → hoja | Las 119 preguntas del Instrumento 2 (sección, ID, bloque, pregunta, tipo, opciones, **celda destino en esta plantilla**, marca de nueva/modificada en v0.4) |
| `PONDERADORES` | Supuestos | Pesos del índice PVE en 7 componentes editables (EXP_UE 25, TRAZA 20, DILIG 15, CAPAC 10, PRESION 15, CERTIF 10, PPWR 5) y bloque ISCAM de pesos fijos (87.5/12.5 y 70/30) |
| `MATRIZ_174` | Marco muestral y datos duros | 174 organizaciones; 36 columnas de dato (SUNAT, DUAs/FOB, certificaciones, score OSCE, D12–D15, P1–P14) |
| `PREGUNTAS_PROXY` | Verificación rápida (back-up) | 36 preguntas proxy por dimensión con umbrales 0.67/0.34 |
| `SCORECARDS` | Scorecard por organización | ISA-Completo, semáforo, ranking y entradas manuales de D2/D5/D6 |
| `ISCAM_Score` | Cálculo del índice | D1–D11, IP1–IP5, IV1–IV5, IP, IV, RE, tipología 2×2, banderas, ISA-PV, P_Global, ISA-EUDR, ISA-Completo |
| `RADAR_BRECHAS` | Agregación territorial | Promedio por departamento y dimensión |

### 7.2 Índices calculados y fórmulas implementadas (`ISCAM_Score`, fila 4 = primera organización)

| Índice | Fórmula implementada | Columna |
|---|---|---|
| Dimensiones D1–D11 | valores por organización (0–100) | `E`–`O` |
| IP1 Trazabilidad | `= D2` | `P` |
| IP2 Legalidad×Deforestación | `= √(D3 × D4)` | `Q` |
| IP3 Sistema interno | `= (D5 + D6 + D8) / 3` | `R` |
| IP4 Capacidad × Trazabilidad | `= (D6 + D2) / 2` | `S` |
| IP5 Mercado y riesgo | `= (D7 + D9 + Cert) / 3` | `T` |
| IP — Preparación | `= promedio(IP1:IP5)` (20% cada subdimensión) | `Z` |
| IV1 Presión UE | `= ISA-PV × 50` (hoy proxy; definición de diseño = % FOB UE + riesgo comprador) | `U` |
| IV2 Rol regulatorio | `= D1` (hoy base 50 si D1=0; definición de diseño = RNCA) | `V` |
| IV3 Riesgo territorial | `= ha>0 ? 65 : 35` (hoy proxy; insumos de diseño ya capturados en B0.4/B0.10/B0.11/B0.13/B0.14) | `W` |
| IV4 Certificación/legalidad | `= Cert=0 ? 70 : 30` | `X` |
| IV5 Riesgo social | `= Tipo org Asociación/Pendiente ? 65 : 40` (hoy proxy; definición de diseño = % mujeres directiva, ya en B0.12) | `Y` |
| IV — Vulnerabilidad | `= promedio(IV1:IV5)` | `AA` |
| RE — Riesgo de exclusión | `= IV × (1 − IP/100)` | `AB` |
| Tipología 2×2 ISCAM | corte en IP=50 × IV=50 → Resilientes / Expuestas Adaptables / Riesgo Latente / Riesgo Crítico | `AC` |
| Banderas duras | hoy solo `= IF(D3=0,"🚫 Inh. vigente OSCE","")` | `AD` |
| ISA-PV (Pacto Verde) | `= AVG(D12:D15)/2` (`MATRIZ_174!AP`) | `AI` |
| P_Global (PVE) | `= promedio P1:P14` (`MATRIZ_174!AO`) — hoy no entra en ISA-Completo | `AJ` |
| ISA-EUDR | `= 0.875 × (D1·D2·…·D7)^(1/7) + 0.125 × ((D8+D9)/2)` | `AK` |
| ISA-Completo | `= 0.70 × ISA-EUDR + 0.30 × ISA-PV` | `AL` |

### 7.3 Fuente de datos por dimensión (estado al 2026-10-14)

| Dimensión | Fuente en la hoja | Estado |
|---|---|---|
| D1 Clasificación regulatoria | `ISCAM_Score!E` | Constante 0 — sin ruta de ingesta; el Form D1.1–D1.4 ya la cubre |
| D2 Trazabilidad | `F` vía `SCORECARDS!H` | Celda manual en 0 en las 183 filas; requiere regla de agregación 0-4→0-100 |
| D3 Legalidad | `G` vía `MATRIZ_174!U` (OSCE) | 138 de 174 vacías, escala no declarada; D3.14i (v0.4) permite actualizar el dato |
| D4 Deforestación | `H` | Constante 0 — Form D4.15–D4.17 + D4.15a (v0.4) |
| D5 Diligencia debida | `I` vía `SCORECARDS!I` | Manual 0 — Form D5.18–D5.21b |
| D6 Capacidad digital | `J` vía `SCORECARDS!J` | Manual 0 — Form D6.22–D6.25b + D6.22c (v0.4) |
| D7 Presión comprador | `K` | Constante 0 — Form D7.26–D7.28c + D7.26a/b (v0.4) |
| D8 Gobernanza | `L` | Constante 0 — Form D8.29–D8.32 |
| D9 Sostenibilidad económica | `M` | Constante 0 — Form D9.33–D9.35 |
| D10 Certificación (bandera) | `N` | Constante 0; no promedia por diseño |
| D11 Ecosistema de apoyo externo | `O` | Constante 0 — etiqueta corregida 2026-10-14: era "D11 — Género e Inclusión", pero en el toolkit y en el proyecto madre el género **no es una dimensión** — es insumo de IV5 vía B0.12 (`Propuesta ISCAM - Indices IP-IV-RE.docx`: "IV5 Riesgo social y comercial = D7 + fricción D8 + % mujeres en la directiva"). D11 sigue siendo el ecosistema de apoyo externo del Form (D11.38–D11.39a) |
| D12–D15 Pacto Verde | `AE`–`AH` vía `MATRIZ_174!W:Z` | Escala 0/1/2; hoy 45 orgs con 1 en D12 y 0 en el resto → preguntas mínimas v0.4 (D12.42, D13.45, D14.51, D15.58) |
| PVE P1–P14 | `MATRIZ_174!AA:AN` → `AO` | En 0; Bloque R (10 preguntas v0.4) + derivadas (P1, P2, P4) |
| PPWR | `SCORECARDS!M` | En 0; PP1/PP2 (v0.4) |
| Datos duros (FOB, DUAs, SUNAT, certificaciones, OSCE) | `MATRIZ_174` columnas `E`–`U` | Fuentes externas (SUNAT/ADUANET/OSEFA); el Form se usa como validación cruzada, nunca como reemplazo |

### 7.4 Nueva pestaña `INSTRUMENTO_2_PREGUNTAS`

Contiene una fila por cada una de las 119 preguntas del Instrumento 2 v0.4 con: sección, ID, bloque/dimensión, texto de la pregunta, tipo de campo, opciones, celda destino en la plantilla y marca de nueva (30, verde) o modificada (5, amarilla) en v0.4. Es el mapa de carga: cada respuesta del Google Form tiene una celda o una columna de destino identificada, y las preguntas que alimentan datos duros externos quedan marcadas como validación cruzada. El filtro automático permite trabajar por bloque o por pregunta nueva.

### 7.5 Reglas de escala y codificación (a implementar en la hoja de carga)

1. Escala 0–4 del Form → `×25` → 0–100 (mismo criterio que `Items_Normalizados!C2` del `Modelo de Calculo - ISA-IP-IV-RE-AHP.xlsx`, que es la hoja de cálculo de cálculo fino del proyecto).
2. Escala 0/1/2 de D12.42, D13.45, D14.51 y D15.58 → directo a las columnas `W:Z` de `MATRIZ_174` (`ISA-PV` las consume en 0–2 y las normaliza a 0–1 vía `/2`).
3. Preguntas de porcentaje (B0.7, D2.6, D3.11, D8.30, P11, B0.12, R1–R10) → 0–100 directo.
4. Banderas que **no** promedian (se reportan aparte): D2.10, D2.5b, D3.14i, D4.15a, D7.28, D10.36, D15.60.
5. Mapeo que **no** promedia: D5.19a, D7.28c, D11.38/D11.39.
6. Reglas de datos faltantes de §2.4 (re-ponderar, nunca imputar) aplican igual a la hoja de cálculo.

### 7.6 Correspondencia Form → hoja (resumen verificado)

| Bloque del Form | Preguntas | Destino principal |
|---|---|---|
| Metadata | 3 | Columnas D/E/F de la Google Sheet de respuestas |
| Bloque 0 | 17 | `MATRIZ_174` (B, A, D, Q, R, G, M, H/I, P, C) + insumos IV1–IV5 (`ISCAM_Score!U`–`Y`) |
| Bloque P | 15 | Insumos IV1 y validación (`MATRIZ_174!AK`); no puntúa dimensiones |
| D1–D11 | 68 | `ISCAM_Score!E`–`O` (D3 vía `MATRIZ_174!U`); banderas a `AD` |
| D12.42 / D13.45 / D14.51 / D15.58 | 4 | `MATRIZ_174!W:Z` → `AE:AH` → `AI` → 30% de `AL` |
| PP1–PP2 | 2 | `SCORECARDS!M` + `PONDERADORES!A18` |
| R1–R10 | 10 | `MATRIZ_174!AC, AE–AN` → `AO` (P_Global) |

---

## 8. Estado de implementación — correcciones aplicadas (2026-10-14)

Los 12 defectos detectados en la revisión de `PLANTILLA_INDICE_PVE_ISCAM.xlsx` se corrigieron el 2026-10-14, salvo los que dependen de la capa de ingesta o de una decisión de negocio, que quedan pendientes y explicitados.

| # | Defecto detectado | Estado | Corrección aplicada / pendiente |
|---|---|---|---|
| 1 | Fórmulas que no evaluaban en `PONDERADORES` (B26, B28, B30, B32–B37, B44: `PROMEDIO` español, `√`, nombres definidos inexistentes, referencias a celdas vacías) | ✅ Corregido | Celdas convertidas a texto documentado con referencia a la celda real del cálculo (columna B); `B26` (ISA-EUDR) ya no está vacía; se agregaron `B39–B43` con los proxies de IV1–IV5 |
| 2 | Desfase de filas en `MATRIZ_174!S/T` (`S3 = SCORECARDS!C1`) | ✅ Corregido | `S3:T176` referencian `SCORECARDS` de la misma fila; `T` usa el semáforo unificado |
| 3 | Promedios muestrales que excluían la organización 174 (`Z178`, `AL178`: rango 4:176) | ✅ Corregido | `Z178`, `AA178`, `AB178`, `AL178` promedian 4:177 |
| 4 | `RADAR_BRECHAS` columna H rotulada D7 promediaba `SCORECARDS!K` (D3); columna D cruzada con desfase de una fila | ✅ Corregido | H promedia `ISCAM_Score!K` (D7); D y H usan criterios del mismo sheet (`ISCAM_Score!C`), eliminando el desfase |
| 5 | Columnas B, E, I–L del radar en `=0` fijo (D1, D4, D8–D11 sin reporte) | ✅ Corregido | Conectadas a `ISCAM_Score!E/H/L/M/N/O` vía `AVERAGEIF` por departamento; fórmulas huérfanas D18/D19/D25 eliminadas |
| 6 | Error de escala en ISA-Completo: `AL = 0.7×AK + 0.3×AI` con AI en 0–1 (el PV aportaba máx 0.3 pts de 100) | ✅ Corregido | `AL = 0.7×AK + 0.3×AI×100` |
| 7 | IV1–IV5 placeholders incoherentes (IV1 = `ISA-PV×50` en escala 0–1; IV3 = `ha>0?→65:35` invertido y treatando "sin hectáreas" como bajo riesgo) | ✅ Corregido (proxy documentado) | IV1 = exposición UE real (`% FOB UE` de `MATRIZ_174!M`, tope 100); IV3 = hectáreas por socio (`R/Q`) con umbrales documentados y **sin dato → 65** (regla del proyecto: sin dato no significa sin riesgo); IV2/IV4/IV5 documentados como proxies en `PONDERADORES!B39–B43`. Pendiente: reescribir con las definiciones de diseño al ingestar el Form (B0.7/P1/P1b/P4/D7.26a → IV1; B0.4/B0.10/B0.11/B0.13/B0.14 → IV3; B0.12 + D3.14i → IV4/IV5) |
| 8 | Colisiones semánticas de nombres (D11 género vs ecosistema; prefijo P; D14/D8 en PONDERADORES; tres taxonomías de semáforo) | ✅ Corregido | `ISCAM_Score!O3` renombrado a "D11 — Ecosistema (inventario, no promedia)" — verificado contra el proyecto madre: el género es insumo de IV5 vía B0.12 (`Propuesta ISCAM - Indices IP-IV-RE.docx`, sub-dimensión 5 "Riesgo social y comercial"), no una dimensión propia. Etiquetas de `PONDERADORES!B17/B18` desambiguadas; semáforo de `SCORECARDS!D3:D176` unificado con `INSTRUCCIONES`. Pendiente menor: prefijo "P" (Bloque P performance vs columnas PVE P1–P14 de `MATRIZ_174`) — resuelto en el Form v0.4 con el Bloque R |
| 9 | Falta la capa de ingesta (hoja de codificación 0-4→0-100 y carga con join por RUC) | ⏳ Pendiente | D1/D4/D7–D11 siguen como constantes 0 hasta ingresar el Instrumento 2; la pestaña `INSTRUMENTO_2_PREGUNTAS` es el mapa de carga |
| 10 | Datos sucios (`H171='Si '`, `I171='En '`, fila 174 `'nan'`, 10 productos `'nan'`, 76 celdas de `SCORECARDS!F` escritas a mano) | ✅ Corregido | `H171='SI'` (recupera certificación orgánica), `I171` limpio, `B174` limpio y `C174='OTROS'`, 10 productos en blanco; las 76 celdas de F ahora son fórmula `=IFERROR(MATRIZ_174!L{r},0)` — valores previos idénticos a `MATRIZ_174!L`, verificados contra respaldo |
| 11 | `P_Global` huérfano (se calcula y muestra pero no entra en ISA-Completo) | ✅ Resuelto — decisión 2026-10-14 | **NO entra en ISA-Completo.** Tres razones del proyecto madre: (i) el índice es el **regresor/predictor** del objetivo (f) y la performance es la variable dependiente — incluirla sería circular (`Metodologia - Indice de Alineamiento (ISA)` §5); (ii) ISCAM usa los indicadores de performance como **validación externa** del índice (Fase 4, paso 12: certificaciones, % volumen trazable, continuidad exportadora, acceso a mercado UE — `Comparativa` §3.3), que es exactamente lo que P_Global mide; (iii) el impacto en performance/exclusión ya está operacionalizado en `RE = IV·(1−IP/100)`, no en el ISA. Documentado en `PONDERADORES!A49:B49` |
| 12 | Semáforo "— Sin Inst.2" en las 174 organizaciones | ℹ Esperado | Etiqueta correcta mientras no haya carga del Instrumento 2 |

---

## 9. Paridad café/cacao — sin sesgo (2026-10-14)

- **Marco muestral equilibrado:** 80 organizaciones CAFÉ, 83 CACAO, 1 PLÁTANO y 10 sin producto registrado (tras limpiar los valores `'nan'` de SUNAT). Relación 49% / 51% — el universo de la hoja de cálculo no está sesgado hacia un producto.
- **Instrumento sin sesgo de redacción:** ninguna pregunta del Instrumento 2 v0.4 asume café. Los ítems con riesgo de sesgo quedaron neutrales: **D12.42** (huella de carbono) pregunta si la organización "mide o ha calculado" su huella sin depender de CalCafé v2.1 (calculadora validada solo para café — limitación documentada al inicio de este documento); **D14.51** dice "pulpa o cáscara" (aplica a café y cacao, no "trilla"); **R5** dice "distintos del café o cacao"; **D15.58** (LMR/fitosanitario) aplica por igual a ambos. La identificación del producto es abierta en **B0.3**.
- **Cómputo producto-agnóstico:** ninguna fórmula del índice (ISA, IP, IV, RE, tipología 2×2, semáforos, radar) usa el producto como criterio de cálculo o de filtro.
- **Chequeo operativo de paridad:** nuevo bloque **"CORTE POR PRODUCTO"** en `RADAR_BRECHAS` (filas 28–35) con conteos y promedios de ISA-EUDR, ISA-PV, ISA-Completo, IP, IV y RE para CAFÉ, CACAO y "sin producto registrado", más un semáforo de paridad: brecha ≤ 5 puntos de ISA-Completo entre café y cacao → "✔ Sin brecha"; > 5 puntos → "⚠ revisar sesgo antes de publicar".
- **Muestreo:** si durante el levantamiento se detecta subrepresentación de cacao (o de café), se corrige la cuota del marco muestral (§1) antes de escalar, no se reprocesan los resultados después.
