# Metodología — Índice Sintético de Alineamiento (ISA) y Marco Muestral (café/cacao)

**Qué resuelve este documento:** operacionaliza, para el universo café/cacao (100–150 organizaciones), la metodología cuantitativa que el proyecto madre (**El impacto del Pacto Verde Europeo en el desempeño de las cooperativas peruanas**, ISCAM — Universidad del Pacífico) exige: encuesta tipo PRODUCE/CENACOOP adaptada, escala ordinal 0–4, **Índice Sintético de Alineamiento (ISA) completo del Pacto Verde** con cinco módulos — (i) huella de carbono, (ii) deforestación/trazabilidad, (iii) diligencia debida DD.HH./ambiente, (iv) reporte de sostenibilidad, (v) economía circular/envases — reglas de datos faltantes y validación de robustez, muestreo no probabilístico por cuotas, y ajustes ex-post de representatividad.

**Alcance actualizado (2026-10-09):** la caja de herramientas EUDR (D1–D11) cubre en profundidad los módulos **(ii) deforestación/trazabilidad** y **(iii) diligencia debida** — y desde 2026-10-08 incluye los módulos (i), (iv) y (v) como dimensiones extendidas D12, D13, D14. **Desde 2026-10-09 se agrega el módulo (vi) Farm to Fork como dimensión D15 (Gestión fitosanitaria y LMR)**, cerrando el sesgo de cobertura hacia café en D12 (D15 aplica por igual a café y cacao) y capturando el pilar del Pacto Verde con mayor impacto operativo inmediato después del EUDR. El ISA completo del Pacto Verde se compone de:
- **ISA-EUDR (submódulos ii+iii)**: D1–D9 (núcleo D1–D7 geométrico 87.5% + extendido D8–D9 aritmético 12.5%) — índice de madurez regulatoria EUDR.
- **ISA-PactoVerde (módulos i+iv+v+vi)**: D12 (huella carbono), D13 (reporte sostenibilidad), D14 (economía circular), **D15 (fitosanitarios/LMR)** — media aritmética simple por dimensión, luego media aritmética entre las cuatro.
- **ISA-Completo**: 0.7 × ISA-EUDR + 0.3 × ISA-PactoVerde (pesos por validar en piloto; reflejan que el acceso al mercado UE lo decide el EUDR, pero la competitividad de largo plazo depende del Pacto Verde completo).

**Actualización 2026-09-16 — el módulo (i) huella de carbono ya no necesita construirse desde cero para café.** Se identificó **CalCafé v2.1** (PromPerú / PUCP-PELCAN), una calculadora de Análisis de Ciclo de Vida ya validada (ISO 14040/44, metodología PEFCR de la Comisión Europea) que computa huella de carbono y huella hídrica del café peruano de exportación en 8 categorías de impacto, con comparación contra otros países productores. Es gratuita y pública. **Limitación real: solo cubre café, no cacao** — para el módulo de huella de carbono en cacao sí haría falta desarrollar o adaptar un instrumento aparte. **Actualización 2026-10-08:** el instrumento ya incluye una pregunta de medición de huella de carbono (D12.42, escala 0/1/2) que no depende de esa calculadora; para cacao se puntúa según producto principal y se anota la brecha.

**Actualización 2026-10-08 — módulos (iv) y (v) incorporados:** D13 (reporte de sostenibilidad, 6 preguntas, alineado CSRD/ESRS/taxonomía) y D14 (economía circular/envases, 5 preguntas, alineado Plan Acción Economía Circular UE, PPWR) ya están en el instrumento. No existía instrumento previo identificado para estos módulos; el instrumento los cubre ahora como dimensiones extendidas del Pacto Verde.

**Actualización 2026-10-14 — instrumento v0.4 (primera versión cerrada).** El instrumento pasó de 89 a **119 preguntas** (116 de instrumento + 3 metadata) cerrando huecos de cobertura: 13 variables del cuestionario de verificación rápida que no tenían pregunta, las 4 dimensiones Pacto Verde (**D12.42, D13.45, D14.51, D15.58**, escala 0/1/2) que activan el 30% de ISA-Completo, 10 indicadores del índice de Pacto Verde y 3 campos de ficha (tipo de organización, departamento, RNCA). Las 17 preguntas restantes del módulo Pacto Verde quedan pendientes de evaluación de comprensibilidad con el técnico de campo. Lo operativo del índice (IP, IV, RE, tipología 2x2, ponderaciones) se documenta en la §7 de este documento.

---

## 0. Fundamentos metodológicos (por qué este diseño, no otro)

Este ISA combina dos tradiciones metodológicas reales, no elecciones ad hoc:

- **Modelos de madurez por capacidades** — la escala ordinal 0–4 del instrumento replica la lógica del **Capability Maturity Model Integration (CMMI, SEI/Carnegie Mellon)**: los niveles no son intercambiables, cada uno presupone que el anterior ya está resuelto. Esto es lo que justifica tratar D1–D9 como una escalera, no como puntos acumulables libremente.
- **Construcción de indicadores compuestos** — el proceso de 8 pasos del ***OECD/JRC Handbook on Constructing Composite Indicators* (2008)** (marco teórico → datos → datos faltantes → análisis multivariado → normalización → ponderación/agregación → robustez → vinculación con otras variables) es la estructura que sigue este documento de punta a punta; es la referencia que usan Eurostat y el Banco Mundial para este mismo tipo de índice. **Actualización 2026-09-16:** Greco, Ishizaka, Tasiou & Torrisi (2019), *"On the Methodological Framework of Composite Indices: A Review of the Issues of Weighting, Aggregation, and Robustness"* (*Social Indicators Research*, 141), es la revisión que actualiza ese mismo Handbook con más de una década de crítica metodológica adicional sobre ponderación, agregación y robustez — se cita aquí como respaldo complementario, no como reemplazo, porque confirma que las tres decisiones más discutidas de este documento (agregación geométrica, calibración, verificación multivariada como control posterior) siguen siendo las prácticas recomendadas en la literatura más reciente, no solo en el Handbook de 2008.

Precedentes sectoriales reales con la misma arquitectura (escala ordinal + preguntas "bandera" no compensables + agregación que castiga el desbalance): el **SAI Platform Farm Sustainability Assessment (FSA)** — el instrumento de referencia mundial para evaluar sostenibilidad a nivel de finca/cooperativa, usado por compradores como Nestlé y Unilever, con niveles Bronce/Plata/Oro y preguntas obligatorias no compensables — y las **bandas de letra del CDP (Carbon Disclosure Project)**, construidas sobre puntajes ponderados con la misma filosofía. Este diseño no es una particularidad dla caja de herramientas EUDR; es el estándar de facto para este tipo de instrumento.

**Precedentes específicos de EUDR/café-cacao (2024-2025, más recientes que el diseño original de este documento):**
- Grabs, J., *"The Construction of Compliance with the European Union Deforestation Regulation in Global Coffee Value Chains"* (*Regulation & Governance*, Wiley, 2024/2025) — analiza directamente cómo se construye el cumplimiento del EUDR en cadenas de café; es el precedente más específico al caso de todos los citados en este documento.
- Team Europe Initiative on Deforestation-free Value Chains (2025), evaluación de preparación EUDR en café/caucho/madera en Vietnam, medida en trazabilidad, legalidad, capacidad técnica y capacidad financiera — un precedente aplicado casi idéntico en estructura a las 5 sub-dimensiones de IP.
- ScienceDirect (2025), *"Can cooperative membership foster compliance with New European Union regulations on deforestation-free production? Evidence from cocoa farmers in Western Côte d'Ivoire"* — estudio empírico que cruza pertenencia a cooperativa con cumplimiento EUDR real, directamente relevante para el objetivo (f) de desempeño del proyecto madre y para validar el Bloque P.

---

## 1. Marco muestral

**Universo y unidad de análisis:** organizaciones cooperativas y empresariales de café y cacao con actividad de exportación en el Perú. El directorio consolidado del que parte este trabajo identifica **174 organizaciones** —80 de café, 83 de cacao, 1 de plátano y 10 sin producto registrado—, estratificadas por producto, tamaño y territorio (Norte/Centro/Sur).

**Tamaño de muestra:** objetivo de 100–150 organizaciones para la primera ronda. **Muestreo:** no probabilístico por cuotas sobre los estratos producto x tamaño x territorio; la representatividad se corrige ex-post por calibración (§3).

**Estado del marco al 2026-10-14:** las 174 organizaciones están cargadas con sus datos duros (comercio exterior, fiscalización, certificaciones); la información de madurez (D1–D15) depende de la aplicación del instrumento.

Lo que sigue en esta sección es el detalle del piloto de comprensibilidad del instrumento (distinto del piloto de campo, que valida el despliegue completo, no solo la redacción de las preguntas).

### 1.1 Piloto de comprensibilidad del instrumento

Antes o durante el levantamiento de las 100–150 organizaciones, evaluar en una submuestra que cubra al menos 3 de las 4 celdas de mayor incidencia esperada: comprensibilidad de las preguntas, tiempo de aplicación, y tasa de no-respuesta por ítem. Ajustar el instrumento si algún ítem muestra no-respuesta >20%.

---

## 2. Construcción del Índice Sintético de Alineamiento (ISA)

### 2.1 Fuente de datos

El **ISA-EUDR** (submódulos ii+iii) se calcula exclusivamente sobre **D1–D9 del instrumento** (escala 0–4 por pregunta, ya definida). D10 y D11 **no entran al ISA-EUDR** — se reportan aparte: D10 es una bandera de falsa seguridad (un puntaje alto sería mala noticia) y D11 es un inventario de cobertura, no una medida de madurez. Meterlos al índice sintético invalidaría su interpretación.

El **ISA-PactoVerde** (módulos i+iv+v+vi) se calcula sobre **D12, D13, D14, D15 del instrumento** (escala 0–4 por pregunta; la versión de campo vigente usa 0/1/2). D15 es nueva (2026-10-09) y cubre: (vi) gestión fitosanitaria y LMR (Farm to Fork). Aplica por igual a café y cacao, cerrando el sesgo de D12 que dependía de CalCafé v2.1 (solo disponible para café).

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

**Regla de agregación — corregida el 2026-09-16, de aritmética a geométrica híbrida.** La versión anterior de este documento promediaba D1–D9 con una media aritmética ponderada. Eso permite **sustitución perfecta** entre dimensiones: una cooperativa con D2 (trazabilidad) en 4 pero D5 (diligencia debida) en 0 saldría con un ISA "aceptable" a pesar de no tener ningún sistema de diligencia debida — exactamente el tipo de brecha crítica que la matriz de brechas necesita ver, no esconder. El precedente que corrige esto es el propio **Índice de Desarrollo Humano del PNUD**: hasta 2009 usaba media aritmética; desde el *Informe de Desarrollo Humano 2010* usa **media geométrica**, documentando que penaliza el desbalance entre dimensiones porque estas no son sustitutos entre sí. Las dimensiones EUDR tampoco lo son: el reglamento no permite compensar la ausencia de diligencia debida con buena geolocalización.

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
D15_i = promedio de las preguntas de D15 (0–100)  [la pregunta de retención en frontera es bandera independiente, no entra al promedio]

ISA_PactoVerde_i = (D12_i + D13_i + D14_i + D15_i) / 4
```

**ISA-Completo:**

```
ISA_Completo_i = 0.70 × ISA_EUDR_i + 0.30 × ISA_PactoVerde_i
```

**Justificación del esquema de pesos entre bloques:** las dimensiones núcleo EUDR determinan directamente el acceso al mercado (lo que el reglamento exige textualmente); las extendidas EUDR (D8–D9) son moduladoras de sostenibilidad del cumplimiento en el tiempo. Los cuatro módulos PactoVerde (D12–D15) son complementarios entre sí (la huella de carbono informa el reporte, la circularidad reduce la huella, el control fitosanitario protege el acceso al mismo mercado que el EUDR) y no anulan el acceso al mercado por sí solos — por eso media aritmética entre ellos y peso 30% en el compuesto final. El esquema de pesos iguales *dentro* de cada bloque sigue siendo el valor predeterminado recomendado por el OECD/JRC Handbook en ausencia de un proceso de consenso de expertos (Delphi, o Analytic Hierarchy Process de Saaty) — no se recomienda un esquema de pesos "de experto" sin esa validación, que hoy no existe en el proyecto. Una vez haya datos reales del piloto, correr un **Análisis de Componentes Principales (PCA)** sobre D1–D15 como chequeo de robustez (§4): si el primer componente explica una fracción alta de la varianza, los pesos iguales son razonables; si dos dimensiones aparecen altamente correlacionadas, están sobre-representando un mismo fenómeno en el índice y el esquema debe ajustarse.

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
D13_i = promedio de las preguntas de D13 (0–100)
D14_i = promedio preguntas D14 (0–100)
D15_i = promedio de las preguntas de D15 (0–100)  [la pregunta de retención en frontera es bandera independiente, no entra al promedio]

ISA_PactoVerde_i = (D12_i + D13_i + D14_i + D15_i) / 4     (si alguna dimensión ausente y no alcanza umbral mínimo, no se calcula)
```

**Umbral mínimo para ISA-PactoVerde (actualizado 2026-10-09):** al menos 3 de las 4 dimensiones D12–D15 deben tener al menos el 70% de sus preguntas respondidas.

**ISA-Completo:**
```
ISA_Completo_i = 0.70 × ISA_EUDR_i + 0.30 × ISA_PactoVerde_i
```

---

## 3. Ajuste por representatividad (ex-post)

Como la muestra es no probabilística por cuotas, reportar el ISA en dos versiones, siguiendo el mismo enfoque del proyecto madre (Deville & Särndal, 1992; calibración por ajuste proporcional iterativo):

1. **ISA sin ajustar** — el calculado en §2.5 sobre la muestra lograda, tal cual.
2. **ISA calibrado — corregido el 2026-09-16, de posestratificación por celda a ajuste proporcional iterativo.** La versión anterior proponía posestratificación simple (reponderar cada celda Producto × Tamaño × Territorio al peso poblacional real). El problema: con 100–150 organizaciones repartidas en ~24 celdas posibles, muchas celdas tendrán 2–3 observaciones — ahí la post-estratificación por celda da pesos inestables (una sola organización puede terminar representando 30% de su celda). La solución estándar cuando solo se conocen los **totales marginales** (cuántas organizaciones hay por producto, por tamaño, por región — no necesariamente el cruce completo, que JNC/APPCACAO/MIDAGRI/CENAGRO probablemente no entreguen combinado) es el **ajuste proporcional iterativo**, formalizado en **Deville & Särndal (1992, "Calibration Estimators in Survey Sampling")** — la misma referencia que el proyecto madre ya cita en su propia bibliografía — y recomendado explícitamente por **AAPOR (2013)** para muestras no probabilísticas por cuotas en esta situación exacta: se ajustan los pesos muestrales para que coincidan con cada margen por separado (Producto, Tamaño, Territorio), sin necesitar la celda cruzada completa.
3. Reportar la diferencia entre ISA sin ajustar y calibrado como **análisis de sensibilidad**, no como corrección definitiva — si la diferencia es grande, es señal de que la cuota lograda se alejó del universo real y debe documentarse como limitación, no ocultarse (**Bethlehem, 2010**, sobre sesgo de selección en encuestas no probabilísticas).

---

## 4. Validación de robustez

- **Consistencia interna por dimensión:** calcular alfa de Cronbach (**Cronbach, 1951**) para las preguntas de escala dentro de cada dimensión **D1–D15** con los datos del piloto (§1.1) y de la primera ronda completa. Un alfa <0.6 en alguna dimensión es señal de que sus preguntas no miden un mismo constructo — revisar redacción antes de escalar.
- **Estructura multivariada (PCA) como chequeo de los pesos:** correr un Análisis de Componentes Principales sobre **D1–D15** con los datos de la primera ronda completa (el piloto de 5–8 casos no alcanza para esto). Si el primer componente explica una fracción alta de la varianza total, el supuesto de pesos iguales es razonable; si dos dimensiones aparecen altamente correlacionadas, están capturando el mismo fenómeno y el esquema de pesos de §2.3 debe revisarse — este es el paso de "análisis multivariado" que el OECD/JRC Handbook ubica antes de fijar la ponderación definitiva (aquí se hace como validación posterior porque no hay datos reales todavía, ver §0).
- **Sensibilidad al esquema de agregación (ISA-EUDR):** recalcular el ISA-EUDR con (a) media aritmética simple en D1–D9 (el método original, ya descartado en §2.3) y (b) la media geométrica híbrida vigente, y reportar cuántas organizaciones cambian de cuartil entre ambos métodos. Se espera que el método aritmético "esconda" organizaciones con una dimensión núcleo en 0 que la geométrica expone — documentar cuántos casos son estos, es el hallazgo que justifica el cambio de método frente a cualquier revisor.
- **Sensibilidad al esquema de pesos entre bloques (ISA-EUDR):** recalcular el ISA-EUDR con pesos iguales entre las 9 dimensiones (11.1% cada una, ambas en aritmética simple para que la comparación sea limpia) vs. el esquema de §2.3, y reportar la correlación de rangos (Spearman) entre ambos. Si Spearman <0.85, el esquema de pesos importa y debe justificarse más allá del valor predeterminado de este documento.
- **Sensibilidad al peso ISA-Completo (70/30):** recalcular ISA-Completo con pesos alternativos (ej. 80/20, 60/40, 50/50) y reportar correlación de rangos (Spearman) vs. el esquema 70/30. Si Spearman <0.85 en cualquier comparación, el peso entre submódulos importa y debe justificarse.
- **Sensibilidad a la regla de datos faltantes:** recalcular excluyendo por completo a las organizaciones con alguna dimensión ausente (regla estricta) vs. la regla de re-ponderación proporcional (§2.4), y reportar cuántas organizaciones cambian de cuartil del ISA-EUDR e ISA-Completo entre ambos métodos.
- **Remuestreo con reemplazo — adoptado como estándar 2026-09-17.** Remuestreo con reemplazo (B=1000 iteraciones recomendadas) sobre la muestra piloto, para construir intervalos de confianza del ISA-EUDR, ISA-PactoVerde, ISA-Completo, IP, IV, RE por cooperativa y de la clasificación agregada. Es el estándar de robustez que ya exige el proyecto madre ISCAM (requisito de robustez del proyecto madre ISCAM) y que el diseño original de este documento no tenía — se adopta explícitamente aquí para igualar esa exigencia. Ejecutar una vez exista la primera ronda completa de datos reales (no aplica al piloto de 5–8 casos de §1.1, la muestra es insuficiente para el remuestreo).

---

## 5. Tipologías comparativas y conexión con el objetivo de desempeño

- Cruzar el ISA (ajustado) contra: producto (café/cacao/ambos), vía de exportación (directa/indirecta), tamaño, territorio — igual que pide el proyecto madre para sus "tipologías comparativas por sector, territorio y tamaño".
- **Territorio como nivel de agregación propio, no solo variable de estrato — decidido 2026-09-17.** Hasta ahora Territorio (Norte/Centro/Sur) solo se usaba como celda de cuota para el muestreo (§1). ISCAM lo trata como un nivel de agregación con puntaje propio, dentro de la cadena parcela→productor→cooperativa→**territorio**→cadena de valor. Se adopta esa misma lógica: además del ISA/IP/IV/RE por cooperativa, reportar `RE_territorio = promedio(RE_c)` de las cooperativas de cada macro-región, una vez exista la primera ronda de datos reales. Esto habilita directamente la aplicación de "seguimiento territorial" (uno de los 5 usos de la matriz de tipología) — permite a un gobierno regional o a la cooperación internacional decidir dónde concentrar esfuerzo geográficamente, no solo por cooperativa individual.
- **Para el objetivo específico (f) del proyecto madre** ("medir el impacto de la adecuación al PVE en el desempeño") — el ISA de este documento es el **regresor/predictor**, no el desempeño en sí. **Actualización 2026-09-16:** la variable de desempeño ya tiene una versión preliminar — el **Bloque P** del instrumento (volumen exportado a la UE y su variación, N° de compradores europeos activos y su variación, precio pagado al socio y su variación, incidencia de rechazos/pérdida de contratos). Es v0.1, pendiente de validar con el equipo del proyecto madre (lista de verificación, Tarea D1) antes del piloto definitivo, pero ya permite ejecutar el piloto de la Tarea C sin bloquear por falta de instrumento.
- **Modelo de análisis propuesto una vez existan datos reales:** dado el diseño transversal, reportar (a) correlación simple ISA↔cada indicador de desempeño actual (P1, P3, P4, P6), (b) comparación de cuartiles de ISA vs. cuartiles de desempeño, y (c) para las variables retrospectivas (P2, P5, P7), la variación calculada como aproximación de tendencia — dejando explícito en cualquier entregable que esto es asociación transversal con recall retrospectivo, no un panel real ni prueba de causalidad.

---

## 6. Alcance de esta primera versión

- **Fuente de datos:** el instrumento (versión 0.4, 119 preguntas, D1–D15), aplicado una vez por organización.
- **Reglas de exclusión:** D10 y D11 no promedian en ISA-EUDR; D12–D15 no promedian en ISA-EUDR pero sí en ISA-PactoVerde.
- **Profundidad de aplicación:** diagnóstico integral (D1–D15 + entrevista) para las organizaciones de la muestra; núcleo (D1–D9) cuando solo se requiere el ISA-EUDR.
- **Informantes por dimensión:** D12: gerencia + responsable técnico/calidad; D13: gerencia + comunicación/transparencia; D14: gerencia + operaciones/beneficio; D15: gerencia + responsable técnico de campo (quien conoce los protocolos fitosanitarios y los resultados de análisis de residuos); el resto de las dimensiones: gerencia general.
- **Composición de esta primera versión:** este documento de metodología, el instrumento de 119 preguntas y la hoja de cálculo de las 174 organizaciones. El fundamento, las fases de validación y los requisitos de robustez provienen del proyecto madre (ISCAM — Universidad del Pacífico, *El impacto del Pacto Verde Europeo en el desempeño de las cooperativas peruanas*).

---

**Pendiente para completar el ISA como entregable:** (a) ejecutar el piloto (§1.1), (b) obtener los totales poblacionales auxiliares de JNC/APPCACAO/MIDAGRI/CENAGRO para la calibración (§3), y (c) definir con el equipo del proyecto madre la variable de desempeño del objetivo (f), que este documento deja explícitamente fuera de su alcance.

---

## 7. El índice en la hoja de cálculo

### 7.1 Arquitectura

La hoja de cálculo que acompaña esta primera versión tiene ocho áreas funcionales:

1. **Instrucciones de uso** con la definición del semáforo (Crítico 0–33 / Vulnerable 34–66 / Preparado 67–100).
2. **Mapa de correspondencia pregunta–celda:** las 119 preguntas del instrumento con su destino, marcadas como nuevas (30) o modificadas (5) en la versión 0.4.
3. **Ponderadores:** índice PVE editable en 7 componentes (exposición UE 25, trazabilidad 20, diligencia 15, capacidad 10, presión del comprador 15, certificación 10, envases PPWR 5) y las fórmulas del bloque ISCAM documentadas como texto con su equivalencia.
4. **Marco muestral:** 174 organizaciones con 36 variables de dato (comercio exterior, fiscalización, certificaciones, puntaje de legalidad, dimensiones Pacto Verde e indicadores PVE).
5. **Verificación rápida:** 36 preguntas de verificación rápida por dimensión con umbrales 0.67/0.34, usadas como respaldo y validación.
6. **Tarjetas de puntaje por organización:** ISA-Completo, semáforo, clasificación y entradas manuales de D2, D5 y D6.
7. **Motor de cálculo:** dimensiones D1–D11, subíndices IP1–IP5 y IV1–IV5, IP, IV, RE, tipología 2x2, banderas, ISA-PV, indicador PVE, ISA-EUDR e ISA-Completo por organización.
8. **Radar departamental:** promedio por departamento y por dimensión, más el corte por producto.

### 7.2 Índices calculados

| Índice | Fórmula |
|---|---|
| Dimensiones D1–D11 | valor 0–100 por organización (fuente: el instrumento) |
| IP1 · Trazabilidad y origen | = D2 |
| IP2 · Legalidad x Deforestación | = RAIZ(D3 x D4) |
| IP3 · Capacidades organizacionales | = (D5 + D6 + D8) / 3 |
| IP4 · Información y documentación | = (D6 + D2) / 2 |
| IP5 · Mercado y riesgo | = (D7 + D9 + Certificación) / 3 · Certificación = conteo de esquemas vigentes llevado a 0/33/66/100 (ratificado 2026-10-15) |
| **IP — Preparación** | = promedio(IP1:IP5), 20% cada sub-dimensión |
| IV1 · Exposición UE | = % del FOB exportado a la UE (tope 100) |
| IV2 · Rol regulatorio | = D1 (base 50 si D1 = 0) |
| IV3 · Fragilidad territorial | = hectáreas por socio: 2 o más a 35; 0.5–2 a 50; menos de 0.5 a 65; **sin dato a 65** |
| IV4 · Certificación/legalidad | = sin certificado a 70; con certificado a 30 |
| IV5 · Riesgo social | = tipo de organización: asociación o pendiente a 65; resto a 40 |
| **IV — Vulnerabilidad** | = promedio(IV1:IV5) |
| **RE — Riesgo de Exclusión** | = IV x (1 − IP/100) |
| Tipología ISCAM 2x2 | corte IP = 50 x IV = 50 → Resilientes / Expuestas Adaptables / Riesgo Latente / Riesgo Crítico |
| Banderas duras | hoy: inh. vigente de legalidad (D3 = 0); las banderas del instrumento (D2.5b, D3.14i, D4.15a, D7.28, D10.36, D15.60) se reportan aparte |
| ISA-PV (Pacto Verde) | = promedio(D12:D15) / 2, escala 0–1 |
| Indicador PVE | = promedio de los 14 indicadores PVE — **no compone ISA-Completo** (decisión §8) |
| **ISA-EUDR** | = 0.875 x (D1·D2·D3·D4·D5·D6·D7)^(1/7) + 0.125 x ((D8+D9)/2) |
| **ISA-Completo** | = 0.70 x ISA-EUDR + 0.30 x ISA-PV x 100 |

### 7.3 Fuente de datos por dimensión (estado al 2026-10-14)

| Dimensión | Fuente | Estado |
|---|---|---|
| D1 · Clasificación regulatoria | instrumento (D1.1–D1.4) | Requiere carga; hoy sin valor |
| D2 · Trazabilidad | instrumento (D2.5–D2.10, D2.5a/b) | Entrada manual sin escala declarada; falta regla 0-4 a 0-100 |
| D3 · Legalidad | puntaje externo de legalidad (corte histórico) + pregunta de sanciones vigentes | 138 de 174 sin dato; la pregunta v0.4 permite actualizarlo |
| D4 · Deforestación | instrumento (D4.15–D4.17, D4.15a) | Requiere carga |
| D5 · Diligencia debida | instrumento (D5.18–D5.21b) | Entrada manual |
| D6 · Capacidad digital | instrumento (D6.22–D6.25b, D6.22c) | Entrada manual |
| D7 · Presión del comprador | instrumento (D7.26–D7.28c, D7.26a/b) | Requiere carga |
| D8 · Gobernanza | instrumento (D8.29–D8.32) | Requiere carga |
| D9 · Sostenibilidad económica | instrumento (D9.33–D9.35) | Requiere carga |
| D10 · Certificación (bandera) | instrumento (D10.36, D10.37, D10.36a) | Bandera: no promedia |
| D11 · Ecosistema | instrumento (D11.38–D11.39a) | Inventario: no promedia |
| D12–D15 · Pacto Verde | instrumento (D12.42, D13.45, D14.51, D15.58) | Escala 0/1/2; sin dato a 0 |
| Indicadores PVE | bloque R + derivadas | Sin dato a 0 |
| PPWR | preguntas PP1/PP2 | Sin dato a 0 |
| Datos duros (comercio, fiscalización, certificaciones) | fuentes externas | El instrumento se usa como validación cruzada, nunca como reemplazo |

### 7.4 Mapa de correspondencia pregunta a destino

| Bloque | Preguntas | Destino principal |
|---|---|---|
| Metadata | 3 | Columnas de auditoría de la hoja de respuestas |
| Bloque 0 | 17 | Marco muestral + insumos de IV1–IV5 |
| Bloque P | 15 | Insumos de IV1 y validación externa; no puntúa dimensiones |
| D1–D11 | 68 | Dimensiones del índice; banderas reportadas aparte |
| Pacto Verde | 4 | ISA-PV (30% de ISA-Completo) |
| PPWR | 2 | Ponderador de envases |
| Bloque R | 10 | Indicadores PVE (validación externa) |

### 7.5 Reglas de escala y codificación

1. Escala 0–4 del instrumento → x25 → 0–100.
2. Escala 0/1/2 de las dimensiones Pacto Verde → directo; /2 → 0–1; x100 al componer el 30% de ISA-Completo.
3. Preguntas de porcentaje → 0–100 directo.
4. Banderas que **no** promedian: D2.10, D2.5b, D3.14i, D4.15a, D7.28, D10.36, D15.60.
5. Mapeos que **no** promedian: D5.19a, D7.28c, D11.38/D11.39.
6. Datos faltantes: re-ponderar, nunca imputar (§2.4).

---

## 8. Estado de implementación — correcciones aplicadas (2026-10-14)

La revisión célula por célula de la hoja de cálculo detectó 12 defectos. Al 2026-10-14, 10 están cerrados (corregidos o resueltos por decisión documentada) y queda uno pendiente, que depende de que existan respuestas reales que cargar.

| # | Defecto detectado | Estado | Corrección aplicada / pendiente |
|---|---|---|---|
| 1 | Fórmulas del bloque de ponderadores que no evaluaban (función en español, símbolo de raíz, nombres definidos inexistentes, referencias a celdas vacías) | Corregido | Celdas convertidas a texto documentado con su equivalencia; la fila del ISA-EUDR se completó; se agregaron los proxies de IV1–IV5 |
| 2 | La clasificación PVE del marco muestral se mostraba desplazada dos filas | Corregido | Referencia a la misma fila de la scorecard |
| 3 | Los promedios muestrales excluían la última organización | Corregido | Los promedios cubren las 174 organizaciones |
| 4 | El radar reportaba dos veces la dimensión de legalidad y ninguna la de presión del comprador; una columna cruzaba hojas con desfase de fila | Corregido | Cada dimensión se promedia con criterios de la misma hoja |
| 5 | Cuatro dimensiones del radar estaban fijas en cero (sin reporte por departamento) | Corregido | Conectadas al motor de cálculo |
| 6 | Error de escala en ISA-Completo: el componente Pacto Verde (0–1) se sumaba contra elEUDR (0–100) y aportaba como máximo 0.3 puntos de 100 | Corregido | ISA-Completo = 0.70 x ISA-EUDR + 0.30 x ISA-PV x 100 |
| 7 | IV1–IV5 placeholders incoherentes (IV1 multiplicaba por 50 una escala 0–1; IV3 trataba "sin hectáreas" como bajo riesgo) | Corregido | IV1 = exposición UE real; IV3 = hectáreas por socio con umbrales y sin dato a 65 (regla del proyecto: sin dato no significa sin riesgo); IV2/IV4/IV5 documentados como proxies |
| 8 | Colisiones semánticas de nombres (una dimensión etiquetada como tema de género, prefijos repetidos, tres taxonomías de semáforo) | Corregido | La dimensión 11 se rotuló como ecosistema de apoyo externo: el género es insumo de IV5 vía la pregunta de mujeres en la directiva, no una dimensión propia — verificado contra el diseño del proyecto madre. Etiquetas de ponderadores desambiguadas; semáforo unificado; prefijo resuelto con el bloque R |
| 9 | Falta la capa de ingesta (codificación 0-4 a 0-100 y carga con unión por RUC) | **Pendiente** | Las dimensiones sin fuente externa siguen en 0 hasta ingresar el instrumento; el mapa de correspondencia es la guía de carga |
| 10 | Datos sucios (certificación con espacio final, valor fuera de dominio, registros sin nombre ni departamento, valores escritos a mano en lugar de fórmula) | Corregido | Limpieza verificada contra respaldo: los valores manuales coincidían con la fuente antes de reemplazarlos por fórmula |
| 11 | Indicador PVE calculado pero sin uso | Resuelto (decisión) | **No entra en ISA-Completo:** el índice es el regresor/predictor del objetivo (f) y el desempeño es la variable dependiente —incluirla sería circular—; el proyecto madre usa los indicadores de desempeño como validación externa del índice (Fase 4, paso 12: certificaciones, % volumen trazable, continuidad exportadora, acceso a mercado UE); el impacto en desempeño ya está operacionalizado en RE = IV x (1 − IP/100) |
| 12 | Semáforo "sin instrumento" en las 174 organizaciones | Esperado | Etiqueta correcta mientras no haya carga del instrumento |

---

## 9. Paridad café/cacao — sin sesgo (2026-10-14)

- **Marco muestral equilibrado:** 80 organizaciones de café, 83 de cacao, 1 de plátano y 10 sin producto registrado. Relación 49% / 51% — el universo no está sesgado hacia un producto.
- **Instrumento sin sesgo de redacción:** ninguna pregunta asume café. La dimensión de huella de carbono (D12.42) pregunta si la organización "mide o ha calculado" su huella, sin depender de una calculadora validada solo para café; la dimensión fitosanitaria (D15.58) aplica a ambos productos; la pregunta de economía circular dice "pulpa o cáscara" (aplica a café y cacao, no "trilla"); el indicador de diversificación dice "distintos del café o cacao"; la identificación del producto es abierta.
- **Cómputo producto-agnóstico:** ninguna fórmula del índice usa el producto como criterio de cálculo o de filtro.
- **Chequeo operativo de paridad:** el corte por producto de la hoja de cálculo reporta conteos y promedios de ISA-EUDR, ISA-PV, ISA-Completo, IP, IV y RE para café, cacao y "sin producto registrado", con un semáforo: brecha de 5 puntos o menos en ISA-Completo entre café y cacao → sin brecha; más de 5 puntos → revisar sesgo antes de publicar.
- **Muestreo:** si el levantamiento introduce subrepresentación de un producto, se corrige la cuota muestral (§1) antes de escalar, no se reprocesan los resultados después.
