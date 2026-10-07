# Marco y Justificación — Fundamentos del Diagnóstico EUDR

**Fusiona:** `Instrumento 1 - Marco de Dimensiones de Diagnostico.md` + `Instrumento 7 - Evaluacion Critica y Elementos Adicionales.md`. Esos dos archivos se mantienen intactos (no se editaron); este es el punto de entrada.

**Base normativa:** Reglamento (UE) 2023/1115, modificado por Reglamento (UE) 2025/2650, interpretado por la 3ª edición del Documento de Orientación (C/2026/3896). Ver `Fe de Erratas - Actualizacion Reglamento 2025-2650.md`.

---

## 1. Las 11 dimensiones

### Núcleo (D1–D7) — mínimo indispensable

| # | Dimensión | Qué mide | Por qué es núcleo |
|---|---|---|---|
| D1 | Clasificación regulatoria | Rol de la cooperativa (operador, operador posterior, comerciante, micro/pequeño operador primario) | Determina qué obligaciones aplican |
| D2 | Trazabilidad y geolocalización | Vínculo lote↔parcela | Requisito técnico más citado y más costoso del EUDR |
| D3 | Legalidad de la producción | Tenencia, permisos, laboral/ambiental | El EUDR exige "legal **y** libre de deforestación" (Art. 3) |
| D4 | Riesgo de deforestación | Uso de suelo vs. corte 31-dic-2020 | Criterio sustantivo que decide acceso al mercado |
| D5 | Sistema interno de diligencia debida | Proceso propio de recolección/evaluación/mitigación/declaración | Convierte los datos de D2–D4 en declaración válida |
| D6 | Capacidad organizacional y digital | Personal, presupuesto, sistemas | Sin esto, nada de lo anterior es sostenible |
| D7 | Posición en la cadena de valor | Exigencias/apoyo del comprador | La presión real viene del comprador, no solo del Estado |

### Extendidas (D8–D11) — diagnóstico integral

| # | Dimensión | Qué mide | Por qué se agregó |
|---|---|---|---|
| D8 | Gobernanza interna y apropiación de los socios | Si los socios entienden/participan, no solo la directiva | D2–D5 dependen de la cooperación del socio individual — datos levantados por un proyecto externo con fecha de cierre puntúan verde hoy y rojo en 18 meses |
| D9 | Sostenibilidad económica del cumplimiento | Costo de adecuación vs. presupuesto real; riesgo de traslado al precio del socio | "Cumplir" financiando con deuda o bajando el precio al socio no es sostenible, es una bomba de tiempo |
| D10 | Confusión certificación voluntaria / EUDR | Si la cooperativa cree (erróneamente) estar ya cubierta | Bandera de percepción más peligrosa: genera falsa seguridad. Art. 30 — la certificación puede informar la evaluación de riesgo pero no sustituye geolocalización ni declaración |
| D11 | Ecosistema de apoyo externo | Qué apoyo estatal/cooperación ya conoce o usa | Sin esto el diagnóstico es solo una lista de carencias sin rutas de solución |

**Refuerzo dentro de D2, no D12 aparte:** segregación física de lotes / prohibición de balance de masas — pertenece a la misma cadena de custodia que D2 ya cubre.

**Refuerzo dentro de D3, no D12 aparte:** contexto de zona de desarrollo alternativo/conflicto — no es criterio del reglamento en sí, pero cambia la interpretación de una brecha de legalidad (falta de gestión vs. problema estructural que excede a la cooperativa).

---

## 2. Elementos evaluados y descartados — con argumento, no por omisión

| Elemento | Por qué se descartó |
|---|---|
| Blockchain / plataformas de trazabilidad de terceros | El reglamento exige geolocalización + declaración en TRACES-sucesor, no una tecnología específica. Riesgo de sobreventa comercial |
| Dimensión de género | Relevante para CSDDD/ESG, no determina acceso al mercado bajo EUDR específicamente. Se mantiene como variable de contexto en Bloque 0, sin peso en el semáforo |
| Búsqueda de una "certificación EUDR" | No existe. Se convirtió en pregunta de alerta dentro de D10 |
| Trazabilidad del empaque del producto terminado | El reglamento regula la materia prima, no el diseño del empaque |
| Monitoreo satelital propio (por cooperativa individual) | Herramientas gratuitas (GFW, PNCB-MINAM) cubren la escala de una cooperativa; capacidad propia tiene sentido a nivel gremial, no individual — documentado en D11 como recurso a conectar |
| Huella de carbono, GEI, batería ambiental operativa (pesticidas, agua, residuos) | ~25 preguntas del form de campo no encajan en D1–D11: no deciden acceso al mercado bajo EUDR. Excepción: autorización de agua y tratamiento de aguas residuales (14a/14b) sí son legalidad ambiental real y sí entran a D3 |

---

## 3. Validación externa (2026) — Documento orientador ADEX/MIDAGRI/MINCETUR/GIZ/EFI

Resultado de un Grupo de Trabajo Multisectorial (R.M. N.° 0128-2025-MIDAGRI), metodología del European Forest Institute (*Legality Due Diligence Navigator*). No es una guía de terceros — es la posición oficial peruana sobre legislación pertinente EUDR en café/cacao.

- **Confirma una decisión de alcance ya tomada:** evalúa las mismas 7 categorías del Art. 2(40) que estructuran D3, y concluye que **no hay requisito legal pertinente para CLPI** en café/cacao peruano — valida con autoridad oficial la exclusión de CLPI como dimensión separada (D3.14g quedó como verificación de bajo costo, no como criterio de puntaje — ver `Ficha Tecnica y Guia de Aplicacion - Instrumento 2.md`).
- **Aporta fuentes de verificación oficiales:** GEOSERFOR, SINIA, registro de infractores OEFA, SIGIA-SENASA, BDPI, DAM en SUNAT/VUCE, mapa de fajas marginales — ya incorporadas en `Instrumento 3`.
- **Dos estadísticas de línea base que calibran D3/D4:** 40–60% de productores sin título inscrito (Cavassa, 2022); 45% de cafetales nuevos en bosque primario, 25% en purmas (Vargas & Willems, 2017/PNUD-MIDAGRI). Un "No" en D3.11 o un "No verificado" en D4.15 no es una anomalía de una cooperativa específica — es la norma nacional.

---

## 4. Cómo se usa este marco

- **Diagnóstico rápido / gran número de cooperativas:** D1–D7 vía Instrumento 2 (núcleo) + panel digital.
- **Diagnóstico integral (prioritarias, con financiamiento, alto riesgo):** D1–D11 completas, encuesta + entrevista (Instrumento 3) + FGD.
- Las extendidas (D8–D11) se añaden sin romper comparabilidad de D1–D7 entre cooperativas evaluadas solo con el núcleo.

---

**Estado:** documento de trabajo, 2026-09-17.
