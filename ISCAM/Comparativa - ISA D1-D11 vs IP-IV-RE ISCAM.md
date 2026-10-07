# Comparativa — Enfoque EUDR (D1–D11 / ISA) vs. Enfoque ISCAM (IP / IV / RE)

**Qué resuelve este documento:** compara la aproximación construida en este toolkit (Instrumentos 1–7, D1–D11, ISA geométrico) contra la metodología real del equipo del proyecto madre revelada en `Projet ISCAM - Methodologie.png` y `Projet ISCAM - INDICE de Vulnerabilite et de preparation.png` (Índice de Preparación IP, Índice de Vulnerabilidad IV, Riesgo de Exclusión RE), y determina dónde aporta más valor cada una — para decidir cómo combinarlas, no para elegir una y descartar la otra.

**Respaldo bibliográfico añadido (2026-09-16), más reciente y más específico al caso que las referencias metodológicas generales ya citadas en la Metodología del ISA:**
- Grabs, J., *"The Construction of Compliance with the European Union Deforestation Regulation in Global Coffee Value Chains"* (*Regulation & Governance*, Wiley, 2024/2025) — el precedente más específico encontrado: analiza directamente cómo se construye el cumplimiento del EUDR en cadenas de valor de café.
- Team Europe Initiative on Deforestation-free Value Chains (2025) — evaluación de preparación EUDR en café/caucho/madera en Vietnam (trazabilidad, legalidad, capacidad técnica, capacidad financiera) — un precedente aplicado casi idéntico en estructura a las 5 sub-dimensiones de IP.
- ScienceDirect (2025), *"Can cooperative membership foster compliance with New European Union regulations on deforestation-free production? Evidence from cocoa farmers in Western Côte d'Ivoire"* — estudio empírico que cruza pertenencia a cooperativa con cumplimiento EUDR real, relevante para el objetivo (f) de performance y para validar Bloque P.
- Greco, Ishizaka, Tasiou & Torrisi (2019), *"On the Methodological Framework of Composite Indices"* (*Social Indicators Research*, 141) — actualiza el OECD/JRC Handbook (2008) con una década más de crítica metodológica sobre ponderación, agregación y robustez; usado aquí como respaldo adicional de las decisiones de agregación geométrica y raking ya tomadas.

---

## 1. Matriz comparativa

| Criterio | Enfoque EUDR (D1–D11 / ISA) | Enfoque ISCAM (IP / IV / RE) | Quién aporta más valor |
|---|---|---|---|
| **Base normativa directa** | Estructurado literalmente sobre las 7 categorías del Art. 2(40) del EUDR, con citas de artículos, decretos supremos y reglamentos específicos por cada sub-requisito (Documento orientador ADEX/MIDAGRI/EFI ya incorporado) | "Cumplimiento ambiental" agrupa deforestación/uso de suelo/manejo ambiental en una sola sub-dimensión, sin desagregación legal explícita visible en la infografía | **EUDR (D1–D11)** — la trazabilidad legal pregunta-por-pregunta es lo que hace defendible el instrumento ante un auditor real, no solo ante un revisor de paper |
| **Medición de vulnerabilidad estructural** | Prácticamente ausente — no hay nada equivalente a "fragilidad territorial" (dispersión geográfica, presión sobre el suelo) ni a "dependencia del mercado europeo" como índice propio | Dimensión completa (IV) con 5 sub-dimensiones: dependencia de mercado, exposición regulatoria, fragilidad productiva/territorial, brechas tecnológicas/financieras, riesgo social y comercial | **ISCAM (IV)** — esto es un vacío real de nuestro diseño, no una diferencia de preferencia |
| **Operacionalización de "impacto en performance/exclusión"** (objetivo f del proyecto madre) | Bloque P + correlación simple ISA↔performance (asociación transversal, sin causalidad) | Fórmula `RE_c = IV_c · (1 − IP_c/100)` — modela explícitamente que la preparación *modera* el efecto de la vulnerabilidad; opera directamente la Hipótesis 3 del equipo | **ISCAM (RE)** — es una operacionalización más fina que una simple correlación, y es la que el equipo ya diseñó para publicar |
| **Regla de agregación** | Geométrica híbrida en D1–D7 (penaliza desbalance, precedente IDH-PNUD 2010) + aritmética en D8–D9 | Suma ponderada (aritmética) en IP e IV — permite compensación entre dimensiones | **Depende del objetivo:** para decidir "¿esta cooperativa cumple o no?" (regulatorio), la geométrica es más defendible porque el EUDR no admite compensar ausencia de diligencia debida con buena trazabilidad. Para un índice académico de "preparación general" (IP), la aritmética es una elección legítima y más simple de comunicar — **ninguna gana claramente aquí, son para preguntas distintas** |
| **Validación de contenido antes de fijar pesos** | No existe — pesos iguales por defecto, justificados solo por el OECD/JRC Handbook | Panel Delphi/expertos con Índice de Validez de Contenido (CVI) explícito en Fase 1 | **ISCAM** — es un paso de rigor metodológico que falta por completo en nuestro diseño y que un revisor de Q1/Q2 pediría |
| **Preguntas ya redactadas y listas para aplicar** | 41+ preguntas D1–D11 con opciones cerradas, banderas, ayudas de llenado, encuesta online funcional (con `db` para piloto) | Ninguna pregunta concreta visible — la infografía define dimensiones e indicadores conceptuales ("registro de productores", "geolocalización de parcelas"), no ítems de encuesta operativos | **EUDR (D1–D11)** — en términos de ejecución inmediata (piloto de 5-10 cooperativas, que ambos documentos piden), este toolkit ya tiene el instrumento, ISCAM todavía no |
| **Banderas no compensables (falsas seguridades, riesgos duros)** | D2.10 (mezcla de lotes/balance de masas), D10 (falsa seguridad de certificación), D3 trabajo forzoso — todas explícitamente no promediables | No visible en la infografía — el diseño de "suma ponderada" per se no contempla banderas que anulen el resultado | **EUDR (D1–D11)** — sin este mecanismo, una cooperativa con un solo incumplimiento grave (ej. trabajo forzoso) podría verse "bien" en el índice si el resto de indicadores compensa |
| **Robustez y sensibilidad** | Alfa de Cronbach, sensibilidad de pesos (Spearman), sensibilidad a regla de datos faltantes | Todo lo anterior + **bootstrap** explícito, más PCA/análisis factorial como parte formal de la Fase 4 | **ISCAM** — el bootstrap es un estándar más alto para el tipo de robustez que exige una publicación Q1/Q2; deberíamos adoptarlo |
| **Unidad de análisis** | Organización (cooperativa) únicamente, con el productor cubierto solo por la encuesta de campo (form v2) como fuente de datos, no como nivel de índice propio | Multinivel explícito: parcela → productor → cooperativa → territorio → cadena de valor | **ISCAM** — reconoce niveles que nuestro diseño trata como "insumo de datos" en vez de como niveles propios de análisis |
| **Tipología de priorización para acción** | Instrumento 4 (Matriz de Brechas), semáforo D1–D9 por dimensión | Matriz Preparación × Vulnerabilidad (2×2): Riesgo crítico / Expuestas pero adaptables / Riesgo latente / Resilientes y mejor posicionadas | **ISCAM** — la matriz 2×2 es más simple de comunicar a un tomador de decisiones (gremio, cooperación) que un semáforo de 9 dimensiones; complementa, no reemplaza, al Instrumento 4 |
| **Trazabilidad del marco muestral (quiénes son las 100-150 organizaciones)** | Avance real 2026-09-16: JNC/APPCACAO/Central Café y Cacao mapeados, 20 RUC verificados, directorio Excel | No referenciado en la infografía (asume "levantamiento de datos" como paso 7, sin detalle de fuente) | **EUDR (este toolkit)** — trabajo ya adelantado que ISCAM todavía no muestra tener resuelto |
| **Costo de implementación restante** | Bajo para D1–D9 (ya existe); alto para llenar el vacío de IV desde cero | Alto en general — ningún ítem de encuesta está redactado todavía, falta el panel Delphi, falta el piloto | **EUDR (D1–D11)** tiene menor costo marginal para arrancar el piloto ya |

---

## 2. Veredicto: ninguno gana solo — la combinación correcta

**Ninguna de las dos aproximaciones debería descartarse.** Resuelven preguntas distintas y se necesitan mutuamente:

- **D1–D11 es el instrumento de recolección y el motor de cumplimiento regulatorio** — ya redactado, ya con banderas duras, ya con trazabilidad legal artículo por artículo, ya con un piloto listo para correr. Es el "de dónde salen los datos" y "qué hacer cuando algo está mal".
- **IP/IV/RE es la superestructura analítica que el proyecto madre necesita para su objetivo de investigación** (medir riesgo de exclusión, publicar en Q1/Q2, construir la matriz de tipología) — que hoy no tiene instrumento propio, solo el diseño conceptual.

**Propuesta concreta de combinación** (no implementada aún, pendiente de tu confirmación):

1. **IP_c se calcula a partir de D1–D9**, remapeando nuestras 9 dimensiones a las 5 sub-dimensiones de IP del proyecto madre:
   - Trazabilidad y origen ← D2
   - Cumplimiento ambiental ← D3 + D4 (fusionados, como lo tiene ISCAM)
   - Capacidades organizacionales ← D6 + D8
   - Información y documentación ← D5
   - Capacidad de adaptación y acceso a recursos ← D7 + D9 + D11 (aunque D11 sigue sin promediarse, como inventario)
   - D1 (clasificación regulatoria) y D10 (bandera de certificación) quedan fuera de IP igual que quedan fuera del ISA — no encajan como "capacidad", son estatus jurídico y percepción, respectivamente.
2. **IV_c es un índice nuevo por diseñar** — la brecha real. Requiere: (a) preguntas nuevas para fragilidad territorial y brechas tecnológicas/financieras que hoy no existen en ningún instrumento, (b) reutilizar Bloque 0 (% exportado a UE, concentración de compradores) para "dependencia del mercado", (c) reutilizar D7 para "exposición regulatoria".
3. **RE_c = IV_c · (1 − IP_c/100)** se calcula una vez existan ambos índices — sustituye o complementa la correlación simple que había propuesto para el objetivo (f).
4. **Las banderas duras (D2.10, D10, trabajo forzoso) se mantienen aparte de IP/IV/RE**, reportadas siempre, nunca absorbidas en la suma ponderada — es la salvaguarda que el diseño de ISCAM no contempla y que debemos preservar al integrar.
5. **Agregar el panel Delphi/CVI y el bootstrap** de la Fase 1 y Fase 4 de ISCAM al plan de validación, hoy ausentes de nuestra Metodología.

Esto no es una elección — es literalmente construir el índice **IV** que falta y conectar el instrumento que ya existe (**D1–D11**) al índice que el proyecto necesita para publicar (**IP/RE**), preservando lo que D1–D11 hace mejor (banderas, trazabilidad legal, ejecución inmediata).

---

## 3. Elementos adicionales de ISCAM que refuerzan la combinación (no eran "punto de comparación", son piezas a incorporar)

Revisando de nuevo ambas infografías con la pregunta "¿qué más hay aquí que no capturé en la matriz", aparecen 7 elementos concretos:

### 3.1 El "checklist de 6 pilares para Q1/Q2" (pie de la infografía de metodología)
ISCAM lista explícitamente qué hace publicable a un índice de este tipo: **validez conceptual · triangulación de datos · ponderación explícita · robustez empírica · validación externa · aplicación para política pública y cadenas sostenibles**. Es una vara de medir concreta. Auditando nuestro estado actual contra estos 6 pilares:

| Pilar | Estado en el toolkit actual |
|---|---|
| Validez conceptual | Parcial — Instrumento 1/7 justifican cada dimensión, pero sin panel Delphi/CVI formal |
| Triangulación de datos | **Ya cubierto y más fuerte de lo que creía** — ver §3.2 |
| Ponderación explícita | Parcial — pesos iguales justificados (OECD/JRC), falta AHP |
| Robustez empírica | Parcial — Cronbach y Spearman ya definidos, falta bootstrap |
| Validación externa | Débil — Bloque P existe pero no está formalmente atado a esto (ver §3.3) |
| Aplicación para política pública | Débil — no articulado explícitamente (ver §3.4) |

### 3.2 "Triangulación de información" (Fase 2, paso 5) — ya lo estamos cumpliendo sin haberlo llamado así
ISCAM pide: Encuesta • Evidencia documental • Bases de datos • Geolocalización • Trazabilidad • Auditoría de consistencia. Las fuentes de verificación oficiales que agregamos al Instrumento 3 esta sesión (GEOSERFOR, SINIA, OEFA, SENASA, BDPI, mapa de fajas marginales, DAM/VUCE de SUNAT) **son exactamente esto** — evidencia documental + bases de datos + geolocalización, verificando lo que dice la encuesta. Vale la pena reencuadrar esa sección del Instrumento 3 explícitamente como "cumplimiento del paso de triangulación de ISCAM", porque ya lo resolvimos sin saber que era un requisito formal de ellos.

### 3.3 "Validación externa" (Fase 4, paso 12) — da una lista *cerrada* de qué debe validar el índice, y hay que atar el Bloque P a ella
ISCAM especifica 4 criterios de validación externa: **Certificaciones · % volumen trazable · Continuidad exportadora · Acceso a mercado UE**. Esto es más preciso que "alguna variable de performance": nos dice exactamente qué correlacionar contra IP/RE para demostrar que el índice mide algo real. Cruce con lo que ya tenemos:
- Certificaciones → ya está en Bloque 0.
- Acceso a mercado UE → cubierto por P1/P4 (volumen y N.º de compradores activos).
- Continuidad exportadora → **cerrado 2026-09-17** — P12 (años consecutivos exportando a la UE), ya no parcial.
- % volumen trazable → **cerrado 2026-09-17** — P11 en Bloque P de `Instrumento 2 - Encuesta Cuantitativa.md`. Continuidad exportadora → **cerrado el mismo día** — P12 (años consecutivos exportando a la UE). Ambas no promedian dentro de ninguna dimensión; son criterios de validación externa, se correlacionan contra IP/RE una vez calculados.

### 3.4 "Aplicaciones: herramienta para la acción" — le da destino a la Matriz IP×IV que hoy no tenemos explícito en el Instrumento 4
ISCAM ata la matriz 2×2 a 5 usos concretos: priorización de asistencia técnica, focalización de financiamiento, diseño de políticas, seguimiento territorial, acceso sostenible al mercado UE. El Instrumento 4 (Matriz de Brechas) da recomendaciones por cooperativa, pero no está explícitamente diseñado para alimentar decisiones de terceros (un gremio decidiendo dónde poner asistencia técnica, un cooperante decidiendo dónde financiar). Vale la pena que el Instrumento 4 declare estos 5 usos como su "para qué", una vez exista la matriz combinada.

### 3.5 AHP (Analytic Hierarchy Process) como método de ponderación nombrado explícitamente
No es solo "Delphi u opinión de expertos" — ISCAM nombra **AHP** puntualmente, que implica matrices de comparación pareada entre dimensiones y un ratio de consistencia (Saaty). Es más estructurado que un panel Delphi genérico y da un número de consistencia verificable. Si se hace panel de expertos para validar pesos (§3.1), debería ejecutarse como AHP, no como consulta abierta, para producir el ratio de consistencia que un revisor Q1/Q2 esperaría ver.

### 3.6 Nivel "Territorio" como unidad de análisis propia, no solo como variable de estrato
Nuestra Metodología usa Territorio (Norte/Centro/Sur) como celda de cuota para el muestreo, nada más. ISCAM lo trata como un **nivel de agregación con score propio** — "Territorio" tiene su propio lugar en la cadena parcela→productor→cooperativa→**territorio**→cadena de valor. Esto habilita directamente la aplicación "seguimiento territorial" del punto 3.4: reportar un RE promedio por macro-región, no solo por cooperativa individual, es lo que le permite a un gobierno regional o a la cooperación internacional decidir dónde concentrar esfuerzo geográficamente.

### 3.7 Hipótesis 1 y 2 son afirmaciones testeables con datos que ya vamos a tener
- H1: "Mayor dependencia del mercado europeo → mayor vulnerabilidad" — testeable cruzando Bloque 0 (% exportado a UE) contra el IV una vez construido.
- H2: "Mayor trazabilidad y capacidad organizacional → mayor preparación" — cuidado: es casi circular si D2/D6/D8 ya son insumo directo de IP (estaría probando que IP correlaciona con sus propios componentes). Para que sea una hipótesis real y no tautológica, habría que testearla contra el criterio de validación externa (§3.3: continuidad exportadora), no contra el propio IP.

---

**Actualización 2026-09-16:** ambos pasos ejecutados en orden — remapeo D1–D9 → IP en `Remapeo D1-D9 a Indice de Preparacion (IP-ISCAM).md`, diseño de IV en `Diseno - Indice de Vulnerabilidad (IV-ISCAM).md` (incluye la fórmula de RE_c y la matriz 2×2 de tipología). Pendiente: redactar 3-4 preguntas nuevas que IV necesita (documentadas en ese archivo, §2 y §6), panel AHP para validar pesos, y trasladar a la Metodología del ISA la aclaración de que las banderas duras (D2.10, D10, trabajo forzoso) se mantienen siempre fuera de IP/IV/RE.
