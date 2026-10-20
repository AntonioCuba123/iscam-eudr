# Memoria Diaria EUDR — Situación Institucional y Estado de Preparación

**Alcance:** cooperativas de café y cacao del Perú frente al Reglamento (UE) 2023/1115 (EUDR).
**Corte inicial:** 2026-10-01 · **Modo:** *append-only* por fecha. La línea base (§2–§4) no se reescribe; las novedades van a §5.

---

## 0. Cómo usar y actualizar este documento

Este archivo es la memoria viva del proyecto. Se actualiza **agregando una entrada diaria en §5**, nunca reescribiendo §2–§4. Cuando un dato de la línea base queda desmentido por una novedad, la corrección se anota en §5 y se marca el ítem original con `⚠ SUSTITUIDO (fecha)`.

**Convención de estado de evidencia** — se usa en cada afirmación:

| Marca | Significado |
|---|---|
| `[V]` | **Verificado** en fuente primaria (regulamento, acto oficial, portal del Estado) |
| `[M]` | **Medido** con dato propio reproducible (consulta a base de datos o cálculo sobre datos locales) |
| `[I]` | **Inferido** — razonamiento sólido sin medición directa; no citar como dato |

**Regla de citación:** toda cifra lleva fecha de corte y fuente. Si una cifra tiene dos versiones en circulación, se anotan ambas con su origen y se marca el conflicto.

### Lista de verificación de actualización diaria

1. Verificar si cambió el calendario de aplicación (§2.1) — es el ítem de mayor impacto.
2. Verificar si cambió la clasificación de riesgo del Perú (§2.3) — si pasa a *low risk*, se activa el Art. 4a y §2.2 se cae.
3. Rastrear novedades de georreferenciación MIDAGRI (PPA / Identidad Digital / AgroDigital).
4. Rastrear reuniones de arranque MINCETUR / PROMPERÚ / SAFE-GIZ y nuevas organizaciones asistidas.
5. Rastrear el estado del Reglamento de Gestión Ambiental del Sector Agrario (§2.5) — ¿se publicó el DS que modifica el 006-2024?
6. **Verificar la freshness de OEFA** (`infracciones_ambientales`) — el corte era 2024-04-30 (§8.10.1). Si sube, re-ejecutar el cruce negativo contra las 54 cooperativas y anotar el delta.
7. Revisar litigios, sanciones o retiradas de producto en la UE vinculados a origen peruano.
8. **Re-ejecutar los comandos de §6** si cambia la data de SENACE o del universo exportador, y anotar el delta en §5.
9. Revisar los hitos de §8.7 y las brechas de §8.8 contra las fuentes oficiales — son los puntos donde el Estado declara sus propios cuellos de botella.
10. Verificar el *Perfil de Riesgo País* de MINCETUR (§8.1.7) y el presupuesto MEF para el escalamiento de georreferenciación (§8.1.5) — ambos son bloqueantes declarados.
11. Resolver los conflictos abiertos de §8.12 (cifras de exportación) y §8.13 (numeración D1–D11) antes de publicar cualquier entregable.

---

## 1. Resumen ejecutivo (estado al 2026-10-01)

1. **Quedan 90 días.** La aplicación general es el **30-dic-2026**; micro y pequeñas no madereras, **30-jun-2027**. La Comisión ha declarado que **no habrá una tercera prórroga**. `[V]`
2. **La "simplificación" no aplica a Perú.** El régimen de declaración única del Art. 4a exige estar establecido en un país de *bajo riesgo*; el Perú está clasificado como **riesgo estándar**. Ninguna cooperativa peruana accede a él, sin importar su tamaño. `[V]`
3. **El Estado construyó el mapa, no el sistema.** 181.731 parcelas georreferenciadas (jul-2026) contra ~350.000 productores de café+cacao: cobertura parcial, y el registro es solo insumo, no cumplimiento. `[V]`
4. **El eslabón que el reglamento exige — DDS por lote, control de mezcla y declaración — no existe en ninguna cooperativa del universo**, y las 52 organizaciones con exposición UE y US$2.79 mil millones de FOB histórico no tienen **ningún** registro de certificación ambiental. `[M]`
5. **El hallazgo de fondo es institucional, no del productor:** para una parcela de café o cacao no existe fuente pública de legalidad ambiental verificable por un tercero. En 1.870 certificaciones SENACE, la única que menciona café o cacao es una **fábrica de tostado**. `[M]`

**Tesis de trabajo:** el costo del EUDR es principalmente de *información y gobernanza interna*, no de falta de datos geográficos. El Perú resolvió el problema fácil (georreferenciar) y no toca el caro (sistemas de diligencia debida por lote). La clasificación *standard risk* elimina la única vía de alivio por tamaño. Eso convierte el 30-dic-2026 en riesgo de exclusión real para la mitad larga de las cooperativas exportadoras.

---

## 2. LÍNEA BASE — marco regulatorio e institucional

> Congelada al 2026-10-01. No editar; superseded se anota en §5.

### 2.1 Calendario de aplicación `[V]`

| Hito | Fecha | Estado al corte |
|---|---|---|
| Reglamento (UE) 2023/1115 en vigor | 29-jun-2023 | — |
| 1ª prórroga (OT+1) | 30-dic-2025 / 30-jun-2026 | Superada |
| Revisión focalizada **(UE) 2025/2650** | Publicada 23-dic-2025, vigor 26-dic-2025 | En vigor |
| Revisión de simplificación **COM(2026)191** + Guía y FAQs en todas las lenguas | 04-may-2026 | Hecho |
| Sistema de Información EUDR (TRACES) cerrado por reconstrucción | 16-feb-2026 | Reabrió 30-jun-2026 |
| Reglas técnicas finales — **Reg. Impl. (UE) 2026/1565** | 13-jul-2026, vigor 17-jul-2026 | En vigor |
| **APLICACIÓN: medianas y grandes** | **30-dic-2026** | **90 días al corte** |
| Aplicación: micro y pequeñas (no ATH) | 30-jun-2027 | — |
| **Nuevo alcance: café soluble/instantáneo** (Acto Delegado Anexo I, 13-jul-2026) | **30-dic-2027** | Nuevo |
| Informe de revisión de simplificación con propuesta legislativa | 30-abr-2026 | Entregado; sin cambios legislativos adoptados |

**Consecuencias operativas del calendario:**
- La Comisión confirmó que **no habrá una tercera prórroga** y que no reabre el texto legal.
- El Sistema de Información está **operativo** (producción y *acceptance*), con API publicada en el acto de jul-2026. La vía técnica existe; el reloj corre.
- El café soluble entra en alcance con un año de margen: amplifica el problema en 2027 en lugar de resolverlo en 2026.

### 2.2 El hallazgo que cambia el marco: el Art. 4a no alcanza al Perú `[V]`

- Definición de *micro and small primary operator* (nuevo Art. 4a): requiere estar **"established in a country classified as low risk"**.
- El Perú está clasificado como **`standard risk`** (ver §2.3).
- ⇒ **Ninguna cooperativa peruana accede a la declaración simplificada de una sola vez**, por pequeña que sea. Quedan sujetas a DDS completo con evaluación y mitigación de riesgo.
- La Comisión lo escribió en COM(2026)191: los micro/pequeños operadores primarios *source, by definition, from low-risk countries* y por tanto nunca requieren evaluación de riesgo.
- En la práctica, un análisis de la negociación (presentación de ICE, oct-2025) fue explícito: el nuevo régimen **"no se espera aplicable a escala a las cadenas de cacao y café"**, porque los productores de terceros países nunca son "operadores".

**Lo que sí es alivio real y usable:** COM(2026)191 establece que **"the cooperative, rather than its members, can submit a single due diligence statement"**. Una cooperativa puede actuar como operador único y presentar **un solo DDS que cubra a todos sus socios**. Es la palanca operativa para una cooperativa de 600 socios, y corresponde a la variable que el marco D1 ya captura (rol regulatorio).

**Precedente para el paper:** Rainforest Foundation Norway recomendó en 2025 clasificar al Perú como **alto riesgo** (y al menos Ucayali, Loreto, San Martín, Huánuco y Junín). El resultado fue `standard`. Documenta la fuerza relativa del Perú en la clasificación de riesgo.

### 2.3 Clasificación de riesgo del Perú `[V]`

- **Reg. Impl. (UE) 2025/1093** (22-may-2025): *benchmarking* de países. El Perú = **`standard risk category`**.
- En `standard risk` **no** aplica la diligencia debida simplificada del Art. 13 (que sí está disponible para países `low risk`).
- Metodología: *Global Forest Resources Assessment* de la FAO, más criterios cualitativos del Art. 29.
- La lista es un acto de implementación → **es revisable**. Si el Perú pasara a `low risk`, se activaría el Art. 4a y §2.2 se cae. Vigilar (§0, punto 2).

### 2.4 Avances institucionales por actor

| Actor | Qué entregó | Escala real | Marca |
|---|---|---|---|
| **MIDAGRI — PPA / Identidad Digital** | Georreferenciación masiva vía AgroDigital | 2.031.000 productores empadronados, 38 variables, **86% de éxito de georreferencia** (2024) | `[V]` |
| **MIDAGRI — georreferenciación EUDR** | 140.000+ parcelas (nov-2025, 13 regiones) → **181.731 parcelas** café+cacao+palma (jul-2026) | Supera la meta nacional declarada. **Mezcla palma** → cobertura café/cacao real por debajo del 50% de los ~350.000 productores | `[V]` |
| **MINCETUR — debida diligencia** | Asistencia presencial 2026 | **19 organizaciones** (Amazonas, Cajamarca, San Martín, Junín) | `[V]` |
| **PROMPERÚ — SAFE / GIZ** | 4 talleres (Pucallpa, Pichanaqui, Quillabamba, Chachapoyas), may-jun-2026 | 80+ participantes, alcance indirecto ~13.000 productores | `[V]` |
| **MIDAGRI — normativa de legalidad** | DS 006-2024-MIDAGRI. **RM D000325-2026-MIDAGRI-DM** (19-ago-2026) publica el *proyecto* de DS que lo modifica | **Sigue en proyecto.** El marco de referencia del Anexo VII no está cerrado | `[V]` |
| **Rainforest Alliance** | Criterios EUDR opt-in en RACP desde 15-ene-2024 | **>3.000 productores de café + >4.000 de cacao en San Martín** | `[V]` |
| **Solidaridad Latam** | Guía de recomendaciones Ucayali (09-sep-2026) | Regional, no nacional | `[V]` |
| **AL-INVEST Verde** | Förder PPA + Identidad Digital, foco San Martín, desde nov-2024 | Regional, foco San Martín | `[V]` |

**Lectura de conjunto:** la institución peruana construyó el **insumo geográfico** a escala nacional y entrenó a ~80 organizaciones, pero no construyó el **sistema de diligencia debida** que el reglamento exige. La Cámara Peruana de Café y Cacao ya lo advirtió en 2024 sobre el PPA: *"no es suficiente para cumplir con la UE"*.

### 2.5 El vacío de la evidencia de legalidad ambiental `[M]`

**Medido sobre 1.870 certificaciones ambientales SENACE** (dataset `senace-cartera-proyectos`, ingesta 30-sep-2026):

| Consulta | Resultado |
|---|---|
| Exportadores café/cacao (SUNAT) | 126 |
| …con destino UE | 118 |
| **Cruzan con algún proyecto SENACE** | **0** |
| De los UE, con proyecto SENACE | **0** |
| De los café/cacao, con proyecto SENACE | **0** |
| Proyectos que mencionan café o cacao (búsqueda en todos los campos de texto) | **1** |

**Validación contra falso negativo de formato:** 126/126 RUC del universo exportador son de 11 dígitos; 1.863/1.870 filas de SENACE tienen RUC de 11 dígitos (7 nulos). El cruce es legítimo. **El 0 es medido, no artefacto.**

**El único registro con café/cacao:** `BRITT BRANDS PERU SAC` — *"PLANTA PRODUCTORA Y COMERCIALIZADORA DE CAFÉ TOSTADO EN GRANO Y MOLIDO Y ENVASADO DE CHOCOLATE, DISTRITO DE LURÍN – LIMA"*, `Clasificación`, Aprobado, RD N° 084-2017-SENACE-JEF/DEAR, RUC 20601645964. Es una **planta industrial**, no una finca ni una cooperativa.

**Qué contiene realmente el bucket `Agricultura` de SENACE — 182 proyectos (9.7% de la cartera):**

| Instrumento | n | Titular público | Lectura |
|---|---|---|---|
| Clasificación | 112 | 66 | **Escalón más bajo** — ni siquiera es EIA. 61.5% del bloque |
| IGAPRO | 56 | **55** | Obras de protección ribereña |
| Actualización / ITS / PPC / TdR / MTdR | 14 | 13 | Reformas de EIA existente |
| **Total** | **182** | **133 (73%)** | |

Los 49 privados del tramo "Clasificación" son, textualmente: fundo de palta/papaya/limón, planta empacadora de frutas, planta de incubación avícola, palma aceitera, planta de beneficio de cerdos, fundo de vid, planta de tratamiento contra mosca de la fruta, planta procesadora de semillas.

**Formulación citable del hallazgo:**

> En 1.870 certificaciones ambientales SENACE, la única que menciona café o cacao es una fábrica de tostado. **SENACE certificó la planta, nunca certificó el cultivo.**

**Implicancia estructural:** la autorización ambiental del sector agrario la emite **MIDAGRI** bajo su reglamento sectorial (DS 006-2024-MIDAGRI), no SENACE. No existe un registro nacional consolidado y público de evaluaciones ambientales del sector agrario. Por tanto:

- Para el Anexo VII, **no hay vía pública por la cual un operador europeo verifique de manera independiente la legalidad ambiental de una parcela de café o cacao**.
- El costo de verificación recae entero sobre el exportador, que debe producir la evidencia por confianza en su proveedor.
- El marco sectorial **ni siquiera está cerrado** (RM D000325-2026 en proyecto de DS): las cooperativas invierten en verificabilidad sobre una base normativa móvil.

### 2.6 Estado de preparación por dimensión D1–D11

| Dimensión | Estado | Evidencia |
|---|---|---|
| **D1 Clasificación regulatoria** | 🔴 Baja | Nadie ha definido si es operador, *downstream operator* o trader. El rol determina **quién** presenta el DDS. Sin diagnóstico de rol publicado. |
| **D2 Trazabilidad / geolocalización** | 🟡 Parcial | 181.731 parcelas a nivel país; a nivel de cooperativa, desconocido. Sin verificación de integración PPA↔parcelas propias. |
| **D3 Legalidad** | 🔴 Baja, severidad sistémica | 40–60% de productores sin título inscrito (Cavassa 2022). Marco sectorial en proyecto. Sin fuente pública para el Anexo VII (§2.5). |
| **D4 Riesgo de deforestación** | 🟠 Media-alta | Perú perdió 200 kha de bosque natural en 2024 (GFW); GeoBosques: 132 kha en 2023, epicentros Ucayali / San Martín / Loreto / Madre de Dios; MapBiomas: +1.062% palma, +193% arroz. La Origin Issue Assessment de Rainforest Alliance para café Perú señala la expansión de pequeña escala con tala y quema como driver principal. |
| **D5 Diligencia debida interna** | 🔴 Baja | Sin DDS, sin *reference number*, sin control de mezcla documentado. |
| **D6 Capacidad organizacional/digital** | 🟠 Dispersa | MIDAGRI ofrece Identidad Digital; ninguna cooperativa tiene sistema propio. |
| **D7 Posición en cadena** | 🔴 Vulnerable | Las 52 organizaciones con destino UE dependen de un comprador que traslada toda la exigencia. |
| **D8 Gobernanza / socios** | 🟡 | Centrales y federaciones activas (CENFROCAFE, Norandino, Cepicafe), pero gobernanza de datos de socios sin resolver. |
| **D9 Sostenibilidad económica** | 🟠 | El récord de precio (US$338/qq, 2025) financially da margen para invertir — **ventana histórica, posiblemente cerrándose**. |
| **D10 Falsa seguridad por certificación** | 🔴 Crítica | Orgánico (24/25 en San Martín) y Fairtrade (24/25) **no reemplazan** geolocalización ni DDS. RA tiene opt-in EUDR pero cubre ~7.000 productores en una región. |
| **D11 Ecosistema de apoyo** | 🟡 | Existe y funciona (SAFE, PROMPERÚ, MINCETUR, Solidaridad, RA), pero cubre una fracción del universo. |

### 2.7 Correcciones pendientes sobre el propio dataset `eudrperu`

1. **Falsos positivos por palabras clave.** `data/backup/sunat_todos_exportadores.csv` incluye cooperativas de **banano** y **mango**. El match por keyword de SUNAT no discrimina cultivo. Depurado: 126 → **54** café/cacao limpios (cota inferior; el filtro por nombre no captura razón social genérica).
2. **Placeholders de SUNAT.** Al menos 6 filas con nombre `"NUEVO EXPORTADOR"` — RUC sin razón social registrada.
3. **Deriva documental.** `docs/FUNDAMENTOS_UNIVERSO_ENCUESTABLE.md` dice 245 (correcto, coincide con el CSV); la Ficha Técnica del Instrumento 2 dice 258 con 76 datos SISPAC-PA. **El 258 no está respaldado por ningún archivo del repo.** Además conviven tres conteos de preguntas (39 / 73 / 75) y el índice "Herramientas de Diagnóstico" describe un Instrumento 2 de 39 preguntas que ya no existe.

---

## 3. Universo y exposición cuantificada

### 3.1 Denominador de productores — tres cifras oficiales incompatibles

| Cultivo | Productores | Fuente | Marca |
|---|---|---|---|
| Café + cacao | ~**350.000** | Cámara Peruana de Café y Cacao (2025) | `[V]` |
| Café | ~300.000 familias | Vira (2026) — coherente | `[V]` |
| Cacao | **83.000** | PRODUCE (2024) | `[V]` |
| Cacao | **>100.000** | El Peruano (2025) | `[V]` |
| Cacao | **>120.000** | PPA / MIDAGRI (2024) | `[V]` |

⚠ Usar con cautela: el rango de cacao es 83.000–120.000 según la fuente. Cualquier paper debe explicitar cuál usa.

### 3.2 Universo exportador (medido sobre `sunat_todos_exportadores.csv`) `[M]`

| Métrica | Valor |
|---|---|
| Exportadores café/cacao (SUNAT, 2010–2025) | 126 |
| …con ≥1 destino UE | **118 (93.7%)** |
| **Cooperativas café/cacao depuradas** | ⚠ SUSTITUIDO (2026-10-06): **51** (cota inferior) |
| **…de esas, con destino UE** | **52** |
| **FOB acumulado 2010–2025 de esas 52** | ⚠ SUSTITUIDO (2026-10-06): **US$ 2.740 millones** de las 51 vigentes |
| **Proyectos SENACE asociados a esas 52** | **0** |

**Contexto de magnitud:** US$2.79 mil millones en 16 años equivale a ~1.7 veces las exportaciones nacionales de café de un solo año (US$1.672M, 2025). La exposición económica del universo en riesgo es de la magnitud del sector nacional completo.

### 3.3 Universo de organizaciones

| Métrica | Valor | Fuente |
|---|---|---|
| Organizaciones con RUC validado (universo consolidado) | **245** | `EUDRPERU_universo_consolidado.csv` (245 filas) |
| De ellas, con destino UE | 28 | `[M]` |
| Con GPS y contacto directo (CENCOOP 2017) | 177 | `FUNDAMENTOS_UNIVERSO_ENCUESTABLE.md` |
| Con exportación confirmada (PRODUCE) | 56 | ídem |
| Candidatas adicionales (banco SOPARSE) | 83 | ídem |
| Universo extendido | 328 | ídem |
| Exportadores café+cacao según Cámara | ~450 | `[V]` |

**Contraste con nuestro propio universo:** el universo exportador real (52Organizations con destino UE) es **mucho más pequeño** que el "245". La métrica que importa para el riesgo EUDR no es el universo de organizaciones, sino el **subconjunto con exposición directa a la UE**.

**Segmentación de riesgo dentro de las 52:**
- **Baja exposición de incumplimiento** (tienen escala, capital y relación con certificadora): CENFROCAFE (US$358M FOB / 1.305 ops), NORANDINO (US$322M), COCLA (US$180M / 29 países), MARANURA (US$905M), ACOPAGRO (US$166M), APPBOSA (US$186M), ALTO MAYO (US$121M).
- **Alta exposición** (US$78k–3M FOB, 1–3 operaciones, un solo cliente europeo): QORIQAO, APAPG, Colpa de Loros, Sonomoro del VRAEM, Coopavre, Valle de Incahuasi. Para éstas, un solo embarque rechazado es el año entero.

### 3.4 Límites del denominador de cacao

⚠ Con tres cifras oficiales incompatibles (83k / 100k / 120k), la cobertura de georreferenciación solo puede expresarse como rango:
- **Techo optimista** (asumiendo que *ninguna* de las 181.731 parcelas es palma): ~52% de los 350.000 productores de café+cacao.
- **Realista**: la palma comparte zonas (Piura, Ucayali, San Martín, Loreto, Madre de Dios) → cobertura café+cacao **claramente por debajo de la mitad**.
- Y el **86% de éxito de georreferencia del PPA** significa que el número bruto no es el número válido.

---

## 4. Registro de verificación

### 4.1 Medido con dato propio `[M]`

| Hallazgo | Método | Fecha |
|---|---|---|
| 0 de 126 exportadores cruzan con SENACE | JOIN RUC entre `stage_eudr_exp` y `senace_cartera_proyectos` en Postgres | 2026-10-01 |
| 1 solo proyecto de 1.870 menciona café/cacao | Búsqueda ILIKE en titular+título+unidad+descripción+actividad | 2026-10-01 |
| 182 proyectos con `actividad = 'Agricultura'`; 73% de titular público; 61.5% son "Clasificación" | GROUP BY tipo sobre el bucket | 2026-10-01 |
| 118 de 126 exportadores con destino UE | Filtro por lista de países UE sobre el campo `paises` | 2026-10-01 |
| 54 cooperativas café/cacao depuradas, 52 con destino UE, US$2.786,5M FOB acumulado | Filtro por nombre excluyendo banano/mango/plátano/palta y placeholders | 2026-10-01 |
| 245 filas en `EUDRPERU_universo_consolidado.csv` | Conteo de líneas | 2026-10-01 |
| 1.863/1.870 filas SENACE con RUC de 11 dígitos (7 nulos) | Validación de formato → el 0 no es falso negativo | 2026-10-01 |

### 4.2 Verificado en fuente primaria `[V]`

Calendario de aplicación · Art. 4a y su requisito de país bajo riesgo · clasificación `standard risk` del Perú (Reg. Impl. 2025/1093) · Reg. (UE) 2025/2650 · Reg. Impl. (UE) 2026/1565 · COM(2026)191 y la cláusula regla "la cooperativa puede presentar un único DDS" · reaparición del Sistema de Información 30-jun-2026 · café soluble en Anexo I desde 30-dic-2027 · cifras MIDAGRI/PPA · workshops PROMPERÚ-SAFE · MINCETUR 19 organizaciones · RM D000325-2026-MIDAGRI-DM · alcance Rainforest Alliance Perú · deforestation GFW/GeoBosques/MapBiomas.

### 4.3 Inferido, no medido `[I]` — usar con cautela

- El desglose café+cacao de las 181.731 parcelas georreferenciadas (no hay fuente oficial que separe palma de café/cacao) → solo rango.
- La tasa de verificación de las autoridades de la UE para `standard risk` (la de `low risk` es 1%, confirmado; la de `standard` no se verificó en fuente primaria).
- La reducción de costo de cumplimiento "hasta 75%" atribuida al paquete de simplificación: **aparece solo en fuentes secundarias** (eudrready.eu). No usar sin confirmar.

### 4.4 Nota metodológica sobre las certificaciones voluntarias

- Rainforest Alliance: criterios EUDR opt-in en RACP desde 15-ene-2024; datos compartidos solo con consentimiento del productor.
- Fairtrade: estándar de café actualizado, vigente desde 2026 — el nivel de trazabilidad del sistema Fairtrade ya es compatible.
- Orgánico: trazabilidad de cadena completa ya existente, pero **no alineado con EUDR** por sí solo.
- ⇒ La pestaña D10 (confusión certificación/EUDR) **no es hipotética**: 24 de 25 cooperativas de la muestra de San Martín tienen orgánica y Fairtrade, y 17 de 25 declaran avance EUDR.

---

## 5. REGISTRO DIARIO

### 2026-10-15 — D10 ratificado como bandera pura e IP5 recalculado por conteo de certificaciones

**Decision ratificada contra las fuentes del propio instrumento** `[V]`: D10 (Confusión
certificación/EUDR) es bandera pura —no promedia— y sus tres ítems (D10.36 falsa seguridad,
D10.37 oferta de «certificación EUDR», D10.36a asesoría recibida) se capturan, se codifican y se
reportan aparte; ninguno entra a ISA-EUDR, IP ni IV. Fuentes: §7.3 de la metodología ISA —«D10 ·
Certificación (bandera) … Bandera: no promedia»—, la nota de puntaje del Instrumento 2 —«dimensión
extendida — bandera de alerta, no promedio de madurez»—, la Tabla 4 del documento de trabajo y la
hoja INSTRUMENTO_2_PREGUNTAS de la plantilla, que ya declaraba los tres ítems como bandera. Antes
de esta sesión el libro promediaba D10.36a en NORMALIZADO!CK, en contradicción con todas esas
fuentes: era un error de implementación, no una decisión de diseño.

**Segunda corrección de la misma sesión** `[V]`: la certificación entra al índice por IP5 y como
conteo 0/33/66/100 (0 · 1 · 2 · ≥3 esquemas vigentes), no como el puntaje ponderado precensal
0,6 orgánica / 0,4 Comercio Justo. Fuentes: Matriz de Cobertura Técnica —«IP5 recalculado
(Certificaciones, conteo 0/33/66/100)»— y §7.3 —«IP5 = (D7 + D9 + Certificación) / 3»—. El cálculo
viejo mezclaba escalas (D7 y D9 en 0–100 con la certificación en 0–1) y tomaba la certificación de
una fuente precensal.

**Aplicado en la plantilla** `PLANTILLA_INDICE_PVE_ISCAM.xlsx` (script
`fix_d10_bandera_ip5_cert.py`; respaldo `ISCAM\respaldos\PLANTILLA_INDICE_PVE_ISCAM.backup_
2026-10-15_*_pre-d10-bandera-ip5-cert.xlsx`):

- `NORMALIZADO!CK3:CK176` (promedio de D10) vaciado → `=""`: la dimensión queda en blanco, no en 0.
- `ISCAM_Score!N` (D10) solo hace eco de CK. Verificado: **0 fórmulas** en las 10 hojas consumen la
  columna N — D10 no alimenta ISA-EUDR, IP, IV ni RE.
- `MATRIZ_174!AU/AV` nuevas: AU = n.º de certificaciones vigentes (B0.9 al cargar la encuesta;
  registro precensal H/I mientras tanto) y AV = 0/33/66/100. Estado actual `[M]`: 22 de 174
  organizaciones con dato (15 con 2 esquemas → 66; 7 con 1 → 33); 152 sin dato → «».
- `ISCAM_Score!T` (IP5) = (D7 + D9 + AV)/3 y devuelve «» si falta cualquier componente; antes el
  IFERROR absorbía los vacíos y devolvía 0. `SCORECARDS!L` perdió su 0 de relleno.
- Notas dejadas en `MATRIZ_174!A188/A189` y `PONDERADORES!A64/A65`; destino de B0.9 documentado en
  `INSTRUMENTO_2_PREGUNTAS!G14` y los tres ítems de D10 marcados «bandera, no promedia» en G100:G102.
- Verificado con `verify_d10_ip5.py`: **0 errores de fórmula** en las 10 hojas y offsets de fila
  correctos (ISCAM_Score!T4 apunta a MATRIZ_174!AV3 porque el motor arranca en la fila 4 y la
  matriz en la 3).

**Aplicado en la documentación** (script `update_docx_d10_ip5.py`; respaldo
`ISCAM\respaldos\Metodologia - Instrumento 2 e Indice ISCAM.backup_*_pre-d10-bandera.docx`):

- `ISCAM\Metodologia - Instrumento 2 e Indice ISCAM.docx`: §2.6 ahora dice «promedian D1–D9; D10
  es bandera y D11 inventario»; fila IP5 de la Tabla 1 reescrita con el conteo 0–33–66–100; hito
  de §5 de IP5 corregido de escala y de fuente; hito nuevo «D10 ratificado como bandera pura
  (2026-10-15)». PDF regenerado con `make_pdf_sindato.py` (15 páginas).
- Propagación a los documentos que habían quedado con la fórmula vieja (script
  `update_docx_dtiscam_ip5.py`, con respaldos en `ISCAM\respaldos\`):
  - `DT-ISCAM-001_Indice_ISCAM_Trabajo.docx`: la Tabla 3 decía «D7 + D9 + D11 + Certificaciones» —
    incluía D11, que es inventario y no promedia —; ahora «D7 + D9 + Certificación (conteo
    0/33/66/100; sin D11, que es inventario)», con el detalle del conteo en la Tabla 8. La línea de
    hoja de ruta «Poblar D10 con certificaciones conocidas» se redirigió a B0.9 → MATRIZ_174!AU/AV
    → IP5.
  - `ISCAM\Metodologia_ISA_MarcoMuestral.docx`: misma corrección en su tabla de fórmulas.
  - `ISCAM\Metodologia - Indice de Alineamiento (ISA) y Marco Muestral.md` (motor de cálculo):
    IP5 documentado con el conteo 0/33/66/100.
  - `generar_doc_iscam.py` corregido en la fuente para que una regeneración no reintroduzca el
    texto viejo.
- `Instrumentos\Instrumento 2 - Encuesta Cuantitativa.md`: incorporada la pregunta **36a**
  (asesoría específica sobre EUDR), que existía en el texto del Google Form y en la plantilla pero
  faltaba en la encuesta; nota de puntaje de D10 actualizada a los tres ítems.
- `Instrumentos\DOC_TRABAJO_Instrumento2_ISCAM_v2.md`: Q36a incorporada a la Tabla 4 de D10; B0-9
  redirigido de «Insumo D10» a IP5 por conteo; Tabla 5 (D10 = 3 ítems) y totales ajustados
  (Tabla 2 → 94; D1–D15 → 80; total general → 104 ítems / 95 preguntas).

**Defectos ortográficos corregidos de paso** `[M]`: tres intrusiones de caracteres CJK heredadas
del portapapeles —«bibliografía» por «bibliografía» (DT-ISCAM-001, dos ocasiones, y su generador) y «满分»
por «un puntaje máximo» (ídem)— más «reportar» por «reportar» en DOC_TRABAJO_Instrumento2_ISCAM_v2.md.
Quedan pendientes instancias de la misma familia en `ficharucsunat\fuentes_urls.md`,
`reports\ANALISIS_TITULACION_EUDR_CAFE_PERU.md` y `reports\INFORME_TECNICO_EUDR_CAFE_PERU.md`,
fuera del alcance de esta sesión.

**Alcance de la ratificación** `[I]`: con D10 fuera de los promedios, sus ítems dejan de mover
ISA, IP, IV y RE; la certificación solo pesa vía IP5 (20% del IP) y como conteo. Efecto esperado
sobre índices ya publicados: nulo hasta cargar la encuesta, porque IP5 ya devolvía «» sin D7 y D9.

**Pendiente que deja esta sesión** `[M]`: (a) DOC_TRABAJO_Instrumento2_ISCAM_v2.md sigue sin
D11.39a ni los bloques PPWR/R que sí están en el Form v0.4 (119 ítems) y en la plantilla — sus
totales usan otra base de conteo y hay que reconciliarlos; (b) ese mismo documento cita
`ISCAM\Remapeo D1-D9 a Indice de Preparacion (IP-ISCAM).md`, que ya no existe en el working tree;
(c) `ISCAM_Score!P` (IP1) todavía devuelve 0 con `IFERROR(F4,0)` cuando D2 está vacío — el mismo
patrón «sin dato ≠ 0» que se corrigió en IP5; (d) el resto de la jornada 2026-10-15 (capa de
ingesta CAPTURA/NORMALIZADO, ratificación de los 15 ítems «[R]» de CODIFICACION, ISA-PactoVerde
provisional bajo el umbral Pacto Verde) quedó registrado en los hitos de §5 del docx de
metodología pero aún sin entrada propia en esta memoria.

### 2026-10-11 — Cierre de la base de 174 organizaciones: triaje, depuracion y modulo de trazabilidad EUDR

**Alcance de la jornada** `[M]`: se cerro la base de 174 organizaciones cafetaleras y cacaoteras
con cinco entregables y la apertura de la dimension de trazabilidad (D2), que era el vacio
estructural del proyecto. Todo queda en `BASE CAFE CACAO 174\CONSULTA MASIVA RUC 10.10.26\`
y en `appsperu\apps\identidad-fiscal\`.

**Entregable 1 — Matriz de hallazgos publicos (174/174)** `[M]`:
`MATRIZ_ORGANIZACIONES_174_FINAL.csv` y `.xlsx` (34 columnas), una ficha por RUC levantada desde
fuente web: nombre publico, socios, hectareas, certificaciones, exportaciones, hallazgo detallado
y URLs citadas. Informe legible en `HALLAZGOS_174_ORGANIZACIONES.md` y `.docx`.

**Entregable 2 — 1.840 enlaces ADUANET verificados en vivo** `[M]`:
`ENLACES_BUSQUEDA_DUA_2024-2026.xlsx`. 699 enlaces consultados contra aduanet.gob.pe: 573 con
datos (82%), 126 vacios, 0 errores. Tres niveles: resumen por RUC+anio (sin captcha), listado de
DUAs (sin captcha) y detalle de DUA (SgCDUI2, **si pide captcha**, no automatizable).

**Entregable 3 — Cruce DUAs x FOB en dolares** `[M]`:
`CRUCE_DUAs_FOB_POR_ORGANIZACION.xlsx`. 44 de 76 RUC exportadores con movimiento,
**US$ 243.192.124** y **1.141 DUAs** (2024-2026), cuadrado en las 4 hojas del libro.
Concentracion: el top 10 explica el **67%** del FOB. Informe con tablas y 5 graficos en
`appsperu\INFORME_CRUCE_DUAs_FOB.md` / `.docx`.

**Entregable 4 — Triaje y depuracion** `[M]`: `TRIAJE_Y_DEPURACION_174.xlsx` y
`ACCIONES_EJECUTADAS.xlsx` (15 hojas). Las 6 acciones ejecutadas: (1) universo activo **165** de
174, excluyendo 5 en suspension temporal y 4 en baja de oficio; (2) RUC 20611316616 recuperado con
5 contradicciones abiertas; (3) la ficha de 20393786044 **existia**, mi busqueda fallaba por
"COORDILLERA" con doble D; (4) identidad COAS reasignada a 20486973219; (5) via de venta de los 23
activos sin movimiento: 3 indirecta, 7 domestica, 13 sin operacion; (6) alcance del universo con
3 opciones documentadas, se recomienda la B.

**Hallazgo que reorganiza el analisis** `[M]`: el "42% sin movimiento" del universo exportador
**no era un hueco de datos**. El indicador `exporta` del proyecto cruza limpio con la realidad: los 44
con `exporta=SI` son todos ACTIVO y todos tienen FOB. Quien induce a error es la ficha SUNAT, que
clasifica como EXPORTADOR a organizaciones que no embarcan nada.

**Errores propios corregidos y documentados** `[M]`: (a) atribui a 20486668335, entidad
**suspendida** y con FOB cero, toda la identidad publica de COAS (566 socios, 1.700 ha,
Fairtrade, exportacion a Europa), que corresponde a 20486973219, la **mayor exportadora del
universo** con US$ 30,3 millones; (b) el segundo RUC de Kemito Ene que anote no existe;
(c) afirme que 20393786044 no tenia ficha interna cuando la tenia completa en 8 hojas.

**RUC 20611316616 — caso abierto** `[M]`: Asociacion de Productores Agropecuarios San Miguel.
SUNAT la ubica en **Ancash, Nuevo Chimbote** (costa), CIIU principal "cria de animales
domesticos", inscrita el **03/11/2025**. MIDAGRI la registra como beneficiaria PAC desde
**2019** con 22 beneficiados, sede **Piura, San Miguel de el Faique**, producto cacao. Una
organizacion no puede operar 6 anos antes de tener RUC. En la misma base existe la Organizacion
Zonal San Miguel del Faique (RUC 20604401187). Lectura: RUC mal asignado o cruzado al cargar.
**No tratar como organizacion cacaotera hasta aclararlo con MIDAGRI.**

---

### 2026-10-11b — Modulo de trazabilidad EUDR (D2): esquema, plantilla y validacion

**Entregable 5 — Migracion 013_eudr_trazabilidad.sql** `[M]`:
`apps\identidad-fiscal\api\src\db\migrations\013_eudr_trazabilidad.sql`. Abre la dimension
D2, que estaba en cero: **6 tablas** (`eudr_parcela`, `eudr_lote`, `eudr_lote_parcela`,
`eudr_lote_embarque`, `eudr_declaracion`, `eudr_declaracion_lote`) y **2 vistas**
(`v_eudr_cobertura_org`, `v_eudr_trazabilidad`). Cadena completa parcela -> lote -> embarque ->
DDS. Data contract en
`apps\identidad-fiscal\api\docs\data-contracts\eudr-trazabilidad.md`.

**Decision de diseno que sostiene el indicador** `[M]`: el cumplimiento del art. 9(1)(d) es una
**columna generada** (`cumple_geolocalizacion_eudr`) que compara el area contra el umbral de 4 ha
del reglamento. Se calcula, no se declara: quien carga no puede maquillar el indicador. La
geometria se guarda **tal como la reporta la organizacion**, con el sistema de referencia
anotado — forzar una conversion silenciosa de PSAD56 a WGS84 introduce un error de decenas de
metros, indistinguible de una falsificacion en una auditoria.

**Validado contra base real, no solo en papel** `[M]`: 9 reglas verificadas en el Postgres local
de Docker (`postgres://fiscal:fiscal@localhost:5438/identidad_fiscal`, 24 tablas con datos,
2.356.381 contribuyentes). Rechaza punto en parcela >4 ha, punto+poligono simultaneos, lat/lon
fuera de Peru, lat/lon invertidas, cultivo invalido, area negativa y codigo duplicado. Todo en
transaccion con ROLLBACK: la base queda intacta.

**Plantilla de recoleccion** `[M]`: `PLANTILLA_TRAZABILIDAD_EUDR.xlsx` +
`plantilla_trazabilidad_parcelas.csv`, con validaciones en Excel (lista CAFE/CACAO, rango de
lat/lon para Peru, error si se pone un punto en mas de 4 ha) y 3 filas de ejemplo.

**Inconsistencia encontrada en el propio proyecto** `[M]`: mi primer comentario citaba una tabla
`ruc_fob_dua` como destino del JOIN. **Esa tabla no existe en la base.** Las DUAs viven en
`BASE CONSOLIDADA.xlsx`, hoja `RUC_FOB_DUA`; la base solo tiene `ruc_exportaciones_fob`, que
trae FOB agregado por mes/aduana/agente/pais y **sin numero de DUA**. Comentario y data contract
corregidos. **Tarea derivada: ingerir RUC_FOB_DUA como tabla propia** para que la cadena
parcela -> lote -> DUA se resuelva dentro de la base.

**Error de objetivo que debe quedar registrado** `[M]`: aplique la migracion 013 al Neon de
produccion por confusion de `.env`. La raiz `.env.local` apunta a Neon; el `.env` de la app apunta
al Docker local del puerto 5438. Revisado despues: **Neon produccion estaba VACIA**, sin ninguna
de las 12 migraciones previas. No se revirtio nada: quedan 6 tablas `eudr_*` vacias y 1 fila en
`schema_migrations` que registra la 013 como aplicada, lo cual es enganoso si alguien corre
`migrate.ts` contra Neon luego. Pendiente de decision del responsable: revertir o completar alli.

### 2026-10-06j — Línea 3: verificación de las afirmaciones RLAC del paper contra cuadros SUNAT locales

**Entregable nuevo** `[M]`: `Scripts\icrpp_rlac_verificacion.py` → `docs\RLAC_VERIFICACION_2023_2024.xlsx` (9 hojas). Contrasta afirmación por afirmación del paper ICRPP contra cdro_08/12/13/15/16/22 de SUNAT y la programación de naves 2023. La serie histórica sube a 3,501 registros (se arreglaron 3 bugs de parse: cdro_15 buscaba "TOTAL" en la fila equivocada; HHI de cdro_08/22 dividía dos veces por 100 —pasó de 0.1 a 86.3—; se añaden cdro_12 despachadores, cdro_13 almacenes y cdro_16 subpartidas FOB/CIF).

**Veredictos** `[M]`:
- **A1 "Callao = 46.6% del comercio formal": DIVERGE.** La tabla autoritativa SUNAT cdro_15 (importación CIF por aduana) muestra **Callao = 73.0% de las importaciones CIF 2024** (72.7% en 2023). El paper cita Rastro `public.port_imports(is_total=true)`: otro alcance (¿operaciones? ¿comercio total I+E?). Pendiente reconciliar el denominador exacto.
- **A2 "HHI = 2,629 (altamente concentrado)": DIVERGE, misma dirección.** HHI local = **5,479** (2024) / 5,000+ (2023) sobre CIF por aduana — ~2× el del paper; ambos > 2,500 (umbral DOJ/FTC). La conclusión cualitativa (concentración estructural del Callao) se mantiene y es más fuerte.
- **A3 "markup prom 4.95%, max 14.25%, ninguna subpartida supera ±15% (FATF)": PARCIALMENTE VERIFICADO — y la parte del umbral se contradice.** Local (cdro_16, Callao 2024, 16 subpartidas): promedio ponderado **5.75%** (calza), pero máximo **19.36%** en subpartida 1005901100 (**maíz duro amarillo**) y **1 subpartida > 15%** (el paper dice 0). CAVEAT: cobertura distinta (16 subpartidas SUNAT vs 50 registros agregados del paper) y un markup >15% en granel agrícola puede ser flete/seguro legítimo — es señal de revisión, no evidencia de subfacturación.
- **A4 "tráfico Callao +12.9% T1→T4 2024, +11.7% vs 2023": DIVERGE, misma dirección.** Local (cdro_15 trimestral): **+20.3%** T1→T4 2024 y **+6.1%** interanual.
- **A5/A6 (decomisos 2025, INFOBRAS): NO VERIFICABLE** localmente (requieren Memoria SUNAT 2025 / consulta Rastro-INFOBRAS).

**Hallazgos nuevos** `[M]` (no en el paper): despachadores de aduana nombrados — HHI 234 (baja concentración), top-5 = 28.7% del CIF 2024, ~50% en la cola larga de pequeños despachadores (fila "RESTO" excluida de los HHI: son cotas inferiores); almacenes/depósitos — APM Terminals + DP World (ambos terminales del Callao) lideran, top-5 = 46%, HHI 644; importadores HHI 86 y exportadores HHI 165 (competitivos).

**No verificable** `[I]`: el denominador exacto de las cifras del paper (Rastro no está en dataset local); los datos son 2023-2024 y no son evaluación vigente de riesgo ni de cumplimiento EUDR.

### 2026-10-06i — Línea 2: análisis de la programación de naves 2023 del Callao (único tráfico portuario post-2017 abierto)

**Entregable nuevo** `[M]`: `Scripts\icrpp_naves_2023_callao.py` → `docs\NAVES_2023_CALLAO_ANALISIS.xlsx` (10 hojas, 1,296 filas de detalle auditables). Extiende la serie histórica: `ICRPP_SERIE_HISTORICA_RECONSTRUIDA.xlsx` pasa a 2,899 registros (añade desglose por condición TRAMPA/LINEA y motivo de escala al indicador `naves_programadas_callao`).

**Datos** `[V]`: reportes mensuales "Programación diaria de naves arribadas/recepcionadas" MTC/APN, **Feb-Jun 2023** (5 de 12 meses; Ene/Jul/Ago 2023 no existen en el portal, HTTP 404; Set-Dic son extractos de un solo día). **Programación (DUE asignados) ≠ recepción efectiva** — comparación con `naves_recibidas` 2010-2017 es indicativa, no equivalente.

**Hallazgos** `[M]`:
- **Volumen:** 245-283 naves/mes (media 259.2) vs 287.2/mes en 2017 y 306.0/mes en 2010 → ~10% below 2017, ~15% below 2010 (tendencia decreciente del tráfico portuario del Callao).
- **Señales RLAC/TBML:** **TRAMPA 52.4%** vs LINEA 46.6% (el envío tramp — irregular, sin línea fija — es el perfil que FATF/GAFILAT asocia a mayor riesgo de lavado vía comercio); **banderas de conveniencia 47-52%** (Liberia 236, Panamá 158, Islas Marshall 126, Malta 96, Bahamas 34).
- **Procedencia:** 71-73% extranjera (Buenaventura 129, Guayaquil 114, San Antonio 78, Pisco 76…), 22-26% puertos peruanos (cabotaje), ~5% aguas internacionales.
- **Estadía media:** 2.7-3.6 h (mediana ~2.5 h).
- **Calidad de dato:** cobertura del reporte vs numeración DUE acumulada anual: 86-97% (Mar-Jun); Feb sin línea base (Enero 404). 174 filas (13.4%) tienen OBS "NO PAGA — puerto intermedio peruano" (tránsito sin operación comercial).

**No verificable** `[I]`: son señales de **exposición**, no evidencia de ilícito ni calificación de cumplimiento; no hay equivalente para Paita u otros puertos en 2023; la serie 2018-2022 de cargas/naves sigue requiriendo solicitud Ley 27806.

### 2026-10-06h — Paso 7 OECD/JRC (Monte Carlo) y Paso 3 (ACP/α) del ICRPP sobre la serie reconstruida

**Entregable nuevo** `[M]`: `Scripts\icrpp_monte_carlo.py` → `docs\ICRPP_MONTE_CARLO_PASO7.xlsx` (12 hojas, 10,000 corridas, semilla 42, reproducible). Mitiga las Limitaciones 1 y 3 del paper ICRPP para el único dominio reconstruible con datos abiertos: RON.

**Alcance honesto:** RON-01 = cargas TM/año (proxy de TEU — la fuente abierta reporta TM) y RON-03 = incidentes portuarios/año, 2010-2017 (únicos años con ambos indicadores). **RON-02 (HHI inverso de heterogeneidad de carga) es S/D**: CARGAS se desagregan por terminal, no por tipo de carga. RTID/RLAC/RVI/RRC se fijan en los puntajes de la Tabla 9 del paper (sus series requieren las solicitudes Ley 27806 ya generadas). Dos variantes: V1 renormaliza pesos (5/8, 3/8); V2 trata RON-02 como latente U(0,1).

**Hallazgos** `[M]`:
- **Ordenamiento robusto:** Callao > Paita en 8/8 años (mediana MC, ambas variantes).
- **Callao:** compuesto MC mediana 71.7 (p5-p95: 67.8-76.5); P(≥69.2 del paper) = 84% (V1) / 66% (V2) — el puntaje del paper es ligeramente conservador. CAVEAT: el Callao satura el min-max (~10× el siguiente puerto en TM; toca la cota 1.0 en la mayoría de años), así que su RON recomputado (96.1) es "máximo del pool", no cardinal.
- **Paita:** compuesto MC mediana 47.3 (p5-p95: 32.7-56.2); P(≥57.4 del paper) = 2.5% — el puntaje del paper para Paita está en el extremo superior de lo que la serie reconstruida soporta, porque su RON real (8.3 V1 / 22.2 V2) es mucho menor que la estimación del paper (42.0).
- **Brecha Callao-Paita:** 11.8 (paper) → 24.4 (MC V1): la concentración del tráfico en el Callao pesa más de lo que el paper estima.
- **Paso 3 (ACP/α):** α = 0.87 (2 indicadores, n=80) y 0.88 (3 indicadores con accidentes, n=28); PC1 = 88%. CAVEAT: RON-01 y RON-03 correlacionan 0.77 en parte porque ambos escalan con el tamaño del puerto — la coherencia puede medir tamaño, no riesgo. Lectura preliminar, no validación factorial.

**No verificable** `[I]`: la incertidumbre de RTID/RLAC/RVI/RRC (88% del peso) no está cuantificada — falta la serie 2015-2025 por puerto (solicitudes Ley 27806 pendientes). Esto es robustez metodológica, no calificación de cumplimiento EUDR ni riesgo vigente (datos abiertos solo hasta 2017 + 2023 parcial).

### 2026-10-06g — Segunda ola de datos abiertos (hueco 2018-2022 parcial) y cruce cooperativa↔riesgo portuario

**Contexto:** la entrada 2026-10-06e dejó el hueco 2018-2022 y el 2023 sin cobertura. Esta entrada lo amplía con datos abiertos adicionales del mismo portal (sin Ley 27806) y conecta el ICRPP con el universo exportador del proyecto.

**Segunda ola (descarga con cabeceras de navegador, cache en `data\icrpp\open_csv\`)** `[V]`:
- **Licencias de servicios portuarios vigentes 2011-2022** (MTC, CSV `;`, cp1252): 145 filas año×servicio; totales anuales 694 (2011) → 1,022 (2022). **Cierra 2018-2022 en conteo de licencias.**
- **Infraestructura portuaria 2022-2025** (MTC, CSV): 507 terminales/embarcaderos, pero **un solo corte real (2022-12-31)** pese al título; no es serie anual.
- **IQ No Fiscalizado decomisados 2013-2018** (MININTER, CSV): kg por departamento; extiende RTID a 2013-2018 (Callao = 0 en todo el periodo).
- **Naves 2023**: reportes mensuales `.xls` **solo de Callao** (prefijo DUE `CLL`, 245-283 naves/mes) para **Feb-Jun**; los CSV de Set-Dic son **extractos de un solo día**; **Enero/Julio/Agosto 2023 no existen en el portal (HTTP 404)**. Estado PARCIAL, no ABIERTO.

**Cruce cooperativa↔riesgo portuario** `[M]`: `docs\COOPERATIVAS_EXPOSICION_PORTUARIA.xlsx` — 15 organizaciones exportadoras del DUA consolidado (el universo mayor del proyecto son 51 cooperativas; el DUA consolidado tiene 15 RUC con DUAs), con aduana dominante por FOB (PAITA o CALLAO), puntaje ICRPP del paper (Callao 69.2 ALTO / Paita 57.4 MODERADO-ALTO — solo existen para esos dos puertos; el resto se marca S/D, no se inventa), y stats RON de la serie reconstruida (cargas TM prom 2015-2017: Callao 49.90 M / Paita 2.16 M; naves prom: 3,497 / 572; incidentes 2005-2017: 128 / 5). Verificación aritmética contra la fuente APN pasada.

**Totales:** 2,817 registros (2,550 ABIERTO / 232 PARCIAL / 30 LOCAL / 5 CURADO); años con dato 2005-2022 **continuos** + 2023-2026; 21 indicadores; 179 brechas 2015-2025. Reproducir: `python Scripts\icrpp_serie_historica.py`.

**No verificable:** `[I]` el tráfico portuario (cargas/naves) 2018-2022 sigue sin fuente abierta — requiere solicitud a APN (plantilla ya generada); el ICRPP compuesto de puertos distintos de Callao/Paita no existe; la exposición portuaria es insumo de trazabilidad, **no** calificación de cumplimiento EUDR.

### 2026-10-06f — Verificación de URLs de las 25 cooperativas (corrige 5 errores de contenido) + 2 pendientes de Fase 1 resueltos (eran falsos pendientes) + 2 construidos

**Contexto:** tarea pendiente "perfiles de las 25 cooperativas a partir de fuentes públicas verificables" (`docs/cooperativas_fuentes_publicas.md`, creado 2026-10-06 temprano) tenía nombres de fuente sin URL ni fecha de acceso — no era verificable sin rehacer la búsqueda. Se pidió URL + fecha de acceso.

**Qué se hizo** `[V]`: 5 agentes en paralelo (uno por grupo de 5 cooperativas) re-verificaron cada fuente citada con WebSearch/WebFetch. Resultado: ~45 de ~65 citas con URL confirmada y fecha 2026-10-06; ~20 marcadas **NO VERIFICADA** (nunca se inventó un enlace) — sobre todo registros individuales MIDAGRI/RNCA, porque el portal gob.pe bloquea el fetch directo (HTTP 403/418) y no tiene buscador por nombre ni por N.º de registro.

**5 correcciones de contenido encontradas durante la verificación (no solo de URL)** — la tabla original tenía datos objetivamente incorrectos:
1. **CAFCER** (ítem 14) y **Tropical Products** (ítem 21): decían "sin hallazgo en fuentes públicas" — **falso**. CAFCER tiene web propia (cafcer.com) y nota oficial gob.pe (exportación de 820 t UE/EE.UU.). Tropical Products existe como **COOPTROPICALS** (cooptropicals.com, Pichanaki, Junín, 168 productores).
2. **Valle Grande** (ítem 10): decía "sin web propia" — tiene coopvallegrande.com. Su cifra FOB citada (US$ 939,006) no coincide con el PDF fuente real de JNC (US$ 355,574) — corregida.
3. **CASIL** (ítem 9): el reconocimiento alemán (café "Rosa Elvita"/Santos Acha Rivera, tostadurías Schramms-Kaffeerösterei y Die Rösterie) es de **2018** (fecha de publicación del artículo fuente confirmada: 6-abr-2018, agraria.pe), no 2023 como decía la fila. RUC público encontrado de paso: 20479595276.
4. **Yuraq Yacu** (ítem 15): confirmado **homónimo**, no error de transcripción. La única "Yuraq Yaku" con presencia pública (RUC 20600920597, marca "Café Colibrí", primera org. de Ayacucho con Marca Perú) está en Anchihuay, La Mar, **Ayacucho** — no en Pasco/Oxapampa/Villa Rica. No existe ninguna cooperativa con ese nombre en esa zona de Pasco en fuente pública alguna.

**Salidas:** `docs/cooperativas_fuentes_publicas.md` y `.xlsx` regenerados (26 filas verificadas con openpyxl), con sección nueva "Limitaciones de la verificación de URLs".

---

**Hallazgo separado, sobre el Plan de Trabajo 75 días (Fase 1):** al revisar las 4 tareas 🟢 internas pendientes, 2 resultaron ser **falsos pendientes** — ya estaban resueltos o superados, solo no estaba documentado:

- **Tarea C (marco muestral):** el objetivo del plan ("pasar de 46 a 100-150 orgs", escrito 2026-09-17) quedó obsoleto **el mismo día** en que se escribió — ese mismo 17-sep se cerró la consolidación a **245 organizaciones con RUC validado 100% por SUNAT** (`docs/FUNDAMENTOS_UNIVERSO_ENCUESTABLE.md`, universo extendido 328 con el banco de 83 no exportadoras). `[M]` La brecha real, antes no cuantificado: **95 de las 245 no tienen ningún contacto** (ni teléfono ni correo) — ese es el cuello de botella real, no el conteo total. Corregido en `Instrumentos/Ficha Tecnica y Guia de Aplicacion - Instrumento 2.md` (decía "46 orgs, 20 verificadas").
- **Fricción D8→IV5:** la definición **ya estaba cerrada desde el 2026-09-17** en `ISCAM/Diseno - Indice de Vulnerabilidad (IV-ISCAM).md` §6 (es **D8.30** invertido, `fricción_D8 = 100 − D8.30`; D8.29/31/32 quedan fuera porque miden esfuerzo institucional o continuidad, no resistencia del socio). El problema real era que `Scripts/matriz_data.py` (la fuente única de datos de la matriz de cobertura) nunca se sincronizó con esa decisión — seguía diciendo "pendiente" para D8.31/32 y "no entra a IV" para D8.30. Corregido.

**2 tareas 🟢 construidas de cero:**
- `Instrumentos/Estructura Google Sheet - Respuestas Instrumento 2.md` + `Plantilla ... .csv`: esquema de 82 columnas (6 metadata + 76 preguntas, mismo ID que `matriz_data.py`), listo para pegar en la fila 1 de la Sheet de respuestas.
- `Instrumentos/Texto para Google Form - Instrumento 2.md`: las 76 preguntas completas, verbatim, con tipo de campo (Google Forms) y opciones exactas — verificado por recuento automatizado que las 76 coinciden 1:1 con la Sheet.

**Corrección de bonus, de paso:** la Ficha Técnica decía "D1–D11: 50 ítems, total 75 preguntas" — recuento directo sobre `Instrumento 2 - Encuesta Cuantitativa.md` da **51 ítems, total 76** (D3 tiene 11 preguntas contando 14a-14g, no 10; el resto de dimensiones coincidía). Corregido en el mismo documento.

### 2026-10-06e — Serie histórica 2015-2025 del ICRPP reconstruida con datos abiertos (mitiga Limitaciones 1 y 3 del paper)

**Contexto:** el paper ICRPP (`ICRPP_Riesgo_Portuario_Peruano.pdf`, también en `appsperu/ICRPP_Paper_Journal.tex`) concluye que no se contó con la serie histórica completa 2015-2025 para el ACP/Monte Carlo del Paso 7 OECD/JRC y que los percentiles 5-95 del min-max están sesgados por series cortas. **No existen documentos institucionales locales** para APN 2018-2025, DIMAR ni DIRANDRO; la reconstrucción usa solo lo verificable hoy.

**Que se hizo:** `Scripts/icrpp_serie_historica.py` (idempotente, cache con SHA-256). Descarga 7 datasets MTC/APN de `https://www.datosabiertos.gob.pe/sites/default/files/` (CARGAS_2010_2017, NAVES_RECIBIDAS, TIPOS_NAVES_2010_2017, ACCIDENTES_PUERTO_2014_2017, INCIDENTES_PUERTOS_2015_2017 —cuyo contenido real cubre 2005-2017—, DERRAMES_PUERTOS_2008_2017, MERCANCIA_PELIGROSA_0) con cabeceras de navegador: sin `User-Agent`+`Referer` el portal devuelve **418 CloudWAF** `[V]`. Integra cuadros SUNAT 2023-2024 (`appsperu/data/sunat/cdro_*.xlsx`) y DUAs de café 2024-2026 (`fichaduanas-cafe/DUA_CONSOLIDADO.xlsx`).

**Resultados** `[M]`: 2,183 registros (2,148 ABIERTO / 30 LOCAL / 5 CURADO); años con dato 2005-2017 y 2023-2026; 16 indicadores; **142 celdas de brecha en 2015-2025**, el hueco estructural es **2018-2022** (sin fuente abierta identificada). Verificación de trazabilidad: Paita TM 2010-2017 coincide cifra por cifra con las filas agregadas de la fuente APN (ej. 2015 = 2,236,432 TM) y el agregado Callao 2015 (47.0 M TM) cuadra contra el total marítimo (88.5 M TM).

**Salidas:** `docs/ICRPP_SERIE_HISTORICA_RECONSTRUIDA.xlsx` (LECTURA, SERIE_LARGA, COBERTURA_2015_2025, BRECHAS_Y_ACCIONES, FUENTES, EVENTOS_MATERIALES, NORMALIZACION_DEMO con p5/p50/p95 por puerto) y `docs/Solicitudes_Ley27806_ICRPP.md` (plantillas SUNAT, APN, DIMAR, DIRANDRO — el mitigante formal para lo que no tiene documento local).

**No verificable / caveats:** `[I]` HHI SUNAT es cota inferior (rankings top-N); las DUAs cubren solo 25 cooperativas de café, no el tráfico total de aduana; los decomisos 2024-2025 son eventos puntuales curados del paper, **no serie estadística**; PortMATE (RVI-01) sigue sin evaluación de campo. Reproducir: `python Scripts/icrpp_serie_historica.py`.

### 2026-10-06 — CORRECCION DE FONDO: la serie ICO no identifica productores; el identificador de origen esta en la marca

**Contexto:** al preparar el post de LinkedIn se quiso verificar la afirmacion de la entrada del 2026-10-04 de que el ICO es "el codigo individual del PRODUCTOR". La verificacion la desmintio. Esta entrada corrige esa entrada y deja trazabilidad del error.

⚠ **SUSTITUIDO (2026-10-06), en su entirety por la entrada del 2026-10-04.** Los puntos 2, 3 (parrafo de la hoja `PRODUCTORES_ICO`), 4 (fila ICO) y 6 de aquella entrada quedan invalidos. Se conservan como registro del error.

**1. Que es realmente la serie ICO.** Segun la Camara Peruana del Cafe y Cacao, organismo certificante acreditado ante la Organizacion Internacional del Cafe (`camcafeperu.com.pe/ES/exportacion.php`), el tramite de exportacion de cafe tiene tres piezas distintas: [V]

| Pieza | Que identifica | Como se tramita |
|---|---|---|
| Codigo de exportador | La empresa exportadora registrada ante la OIC | Una vez por organizacion |
| Numero de marca | El saco: clave de pais, clave de exportador o caficultor, y numero de serie de la partida | Por operacion o lote |
| **Serie ICO** | **El numero de serie del certificado de origen** | **Por operacion o lote** |

El Registro A3 del Reglamento de la OIC (documento SC-100/20, articulo 3) confirma la estructura del codigo: clave del pais miembro, clave del caficultor o exportador, y numero de serie de la partida de cafe.

**La serie ICO identifica una operacion comercial, no a un productor ni a una parcela.** Por eso la conclusion de la entrada del 2026-10-04 — "el exportador 20136201213 declara 20 productores distintos" — era falsa: son 20 series de certificado de origen, todas de 2025.

**2. El DUA 001107 no es evidencia de ocho productores.** La entrada del 2026-10-04 lo citaba como "8 items, cada uno con un ICO diferente, es decir 8 productores distintos en una sola declaracion". Los ocho codigos son **consecutivos** (30/11/4039 a 30/11/4046), pesan 138 kg cada uno (uno 69), suman 1.035 kg, 1 bulto, US$ 9.676, y fueron declarados el 05/01/2025. Son ocho numeros de serie consecutivos de una misma operacion pequeña, no ocho productores.

**3. Error de extraccion: se perdian 4 de las 24 series ICO.** El patron de `desc_items.py` solo aceptaba el separador `/`. Valle Grande escribe `30-826-5005` y otro exportador `30-1234-4759`. Corregido a `[/\\-]` con espacios opcionales: se recuperan **24 series ICO, no 20**. [M]

**4. Hallazgo nuevo, mas fuerte que el anterior: el numero de marca aporta un identificador de origen estable.** 87 items traen un codigo con forma `NN-AAA-NNN`. El bloque central se mantiene constante dentro de un mismo exportador, y **cada exportador usa una sola clave**:

| Clave | Exportador | RUC | Items | FOB |
|---|---|---|---|---|
| 11 | Central de Cooperativas Agrarias Cafetaleras COCLA | 20136201213 | 33 | US$ 1.845.411 |
| 621 | Cooperativa Agraria Cafetalera Casil | 20479595276 | 5 | US$ 794.158 |
| 826 | Asociacion Valle Grande | 20542209951 | 12 | US$ 3.699.701 |
| 916 | Asociacion Agroexportadora de la Region San Martin | 20602650643 | 7 | US$ 1.242.142 |
| 968 | Asociacion de Productores Selva Nororiental | 20600263286 | 25 | US$ 4.154.568 |
| 1005 | Asociacion de Productores Cerro Blanco | 20606451122 | 1 | US$ 175.384 |
| 1023 | Coop. Agraria de Servicios Multiples Cordillera Azul | 20603820691 | 3 | US$ 441.834 |
| 1234 | No Registrado | 20605500430 | 1 | US$ 147.669 |

Total: 87 items, 66 DUAs, US$ 12.500.867, 1.632.615 kg, 9.756 bultos, 8 exportadores. [M]

Esto es lo mas cerca de un identificador de procedencia que existe hoy escrito en una DUA, y EUDR pide precisamente identificar el origen geografico de la parcela. **No es un productor individual**: identifica a la organizacion que exporta, que puede agregar cafe de socios de varios departamentos. Y esta escrito en el campo de marca comercial, no en un campo de trazabilidad.

**5. Hallazgo de calidad de dato.** La marca `39-968-2019` (DUA 35721, Selva Nororiental) declara pais 39, mientras las otras 24 marcas de ese exportador declaran 30. El 39 cae dentro de la serie secuencial `30-968-2017` a `30-968-2020`, asi que es error de tipeo. No se corrigio el dato; se registro en la seccion "CODIGOS DE MARCA CON PAIS INCONSISTENTE" de la hoja CONTROL.

**6. Lo aplicado al pipeline.** [M]
- `desc_items.py`: `RE_ICO` acepta los tres separadores; nueva funcion `_codigos_marcados` clasifica cada codigo `NN-AAA-NNN` por la etiqueta que lo precede (`ICO:` frente a `MARCA:` / `MARK:`), nunca por la forma. Los codigos cuya etiqueta quedo cortada por el limite de 100 caracteres se registran aparte en `codigo_sin_etiqueta` en vez de adivinarse.
- `generar_duas.py`: `H_ITEMS` pasa de 76 a 80 columnas (`ico` se sustituye por `serie_ico`, `numero_marca`, `clave_origen`, `pais_codigo` y `codigo_sin_etiqueta`). `por RUC` pasa de 46 a 48 columnas (`n_series_ico`, `series_ico`, `n_claves_origen`, `claves_origen`, `n_lotes`, `n_marcas`).
- Hoja `PRODUCTORES_ICO` renombrada a **`SERIES_ICO`** (una fila por serie, con `clave_origen` y `cobertura_serie_ico`). Hoja nueva **`CLAVES_ORIGEN`**: una fila por bloque central, con pais, RUC, items, DUAs, FOB, pesos, bultos y numero de series y marcas.
- `CONTROL` suma 6 metricas: items y series ICO, items con marca, items y claves de origen, items con codigo sin etiqueta.
- `CONTROL` suma la seccion de pais inconsistente.
- MINAGRI: bloque CA:DV (48 columnas) reescrito desde `por RUC`; las columnas 1-78 verificadas intactas.

**7. Codigos con etiqueta cortada.** 10 items tienen un codigo con la forma correcta pero cuya etiqueta quedo fuera del recorte de 100 caracteres: "HUMANO / 30-916-5421 / L..." con la palabra MARCA ausente, o "30/11/4773 - LOT NUMB ... KGICO:" con el numero de serie despues del corte. Se cuentan aparte para no contaminar los conteos de serie ni de marca.

**8. Verificacion.** Dos corridas consecutivas dan hojas identicas en las 8 hojas principales. 0 errores de parseo, 0 PDFs no reconocidos, 0 DUAs con items faltantes. Respaldos: `respaldos\duas\DUA_CONSOLIDADO_antes_series_ico_20261002.xlsx` y `MINAGRI_antes_series_ico_20261002.xlsx`.

**9. Post de LinkedIn reescrito.** `docs\post_linkedin_eudr_borrador.md`, 2.899 caracteres. Se retiraron tres afirmaciones: la de las "8.754 operaciones sin productor individual", la de los "ocho productores" de la DUA 1107 y la de los "20 productores distintos". Las notas de precision del archivo documentan cada retirada.

> *Append-only. Entrada más reciente primero.*


### 2026-10-06b — Segundo barrido: cobertura real de identificadores, rastro parcelario y vacios del formulario

**Contexto:** antes de dar por bueno el post se barro todo el corpus buscando indicadores adicionales. Salieron cinco hallazgos, tres de ellosITORs que corrigen afirmaciones previas.

**1. CORRECCION: el identificador de origen NO esta en todas las partidas.** La version de trabajo del post decia "esta escrito en todas las partidas". Es falso. Contando identificadores declarados (serie ICO, numero de marca, clave de origen, lote, codigo sin etiqueta):

| Identificadores en el item | Items | % | FOB |
|---|---|---|---|
| Ninguno | 224 | 71,8% | US$ 28.421.613 |
| Uno | 1 | 0,3% | |
| Dos | 82 | 26,3% | |
| Tres | 5 | 1,6% | |

**224 items sin ningun identificador = 71,8% de las partidas y 69,5% del FOB del corpus.** La redaccion correcta es "menos de un tercio de las partidas". [M]

**2. Organico declarado sin ningun identificador: 88 de 108 items.** US$ 9.614.019, 23,5% del corpus, 8 exportadores. El caso extremo es **La Florida** (RUC 20140181405): 39 items, 30 organicos, US$ 4.184.722, **cero identificadores en las 39 lineas**, y solo 8 descripciones distintas, la mas repetida 16 veces. [M]

**3. HALLAZGO FUERTE: el unico rastro hasta la finca.** Nueve items de la DUA 122024 (RUC 20602054480, Cooperativa Ecologica de Mujeres Cafetaleras Villa Rica), todos organicos, US$ 205.603,93, 18.975 kg:

| Item | FOB | Finca | Variedad | Contrato |
|---|---|---|---|---|
| 1 | 29.206,83 | La Requia | lavado | 13-49339 |
| 2 | 42.897,53 | La Esperanza | lavado | 13-49400 |
| 3 | 42.897,53 | La Aurora | lavado | 13-49401 |
| 4 | 21.448,77 | La Mariposa | lavado | 13-49402 |
| 5 | 16.474,48 | La Requia | Geisha | (inferido) |
| 6 | 17.645,79 | La Requia | Bourbon | 13-49404 |
| 7 | 6.069,54 | Santa Sofia | natural | 13-49405 |
| 8 | 8.670,78 | Santa Sofia | honey | 13-49406 |
| 9 | 20.292,68 | Cemcavir | lavado | 13-49407 |

**Seis fincas distintas en nueve lotes**: La Requia aparece tres veces, una por variedad (sin variedad, Geisha, Bourbon). Cada lote lleva su numero de contrato, escritos por la cooperativa en el campo libre de la descripcion de la mercancia. **Es lo mas cerca de la parcela que existe en todo el corpus, y aparece en una sola declaracion.** [M]

El patron que la cooperativa escribe siempre es `G1 <FINCA> [-<variedad>] CTR <numero>`. El PDF corta la descripcion a 100 caracteres y en tres items el contrato queda partido: 13-49400 y 13-49402 se reconstruyen porque el codigo completo aparece al principio de la linea siguiente; el del item 5 no se recupera del PDF en absoluto y 13-49403 es **inferencia** por la serie correlativa. La hoja `FINCAS` marca estos casos en la columna `contrato_truncado`.

Nota de control: "G1" tambien es un grado de exportacion, no solo una finca. El parser exige ademas la palabra `FINCA` o el bloque `CTR`, sin lo cual entra como finca "Coffee Organic" y "Coffee Big Bags Of", que no lo son.

Argumento que sostiene esto: la trazabilidad al origen no requiere un sistema nuevo, requiere que alguien escriba el nombre en el campo correcto.

**4. El cacao casi no esta.** 5 items de 312 (1,6%), **US$ 449.326 = 1,10% del FOB del corpus**, 74.901 kg, 3 exportadores, **cero identificadores de origen**. Todo el analisis de identificadores es cafe. El post menciona el cacao porque el universo exportador lo incluye, pero la evidencia de detalle es casi inexistente. [M]

**5. Hallazgo de calidad de dato: doce items con FOB en multiplo exacto de 50.000.** Nueve de US$ 50.000 y tres de US$ 100.000, **US$ 750.000 = 1,83% del corpus**. Todos son item 2 o 3, todos con bultos en cero, todos con peso exacto de 18.975 o 20.700 kg, y todos en DUAs `SIN_CABECERA`.

Tienen la misma firma que los 11 items fantasma ya excluidos (US$ 500.000). El filtro actual necesita el campo 6.5 de la cabecera para detectar el duplicado, y estos items estan en DUAs que no la tienen: **el filtro no los puede detectar por construccion, no por error**. Quedan para revision manual, no se excluyen. [M]

**6. Otros datos.** PESO INCOMPLETO: 32 items con "00 KG" donde deberia ir el peso del envase, US$ 4.628.732 = 11,3% del corpus (Casil 9, Valle Grande 8, Ocumal 7). ADUANAS: solo Paita (74,7% del FOB), Callao (25,3%) y una DUA aerea de US$ 410.

**7. Vacios estructurales del formulario.** La DUA no tiene campo para volumen de Robusta. Solo se mide por la palabra del texto libre: **0 items, 0 menciones de "CATIMOR" o "CATIMAO"**. Igual para Criollo, Trinitario, Forastero y Amazonico (0 cada uno) y para Rainforest, UTZ y "sostenible" (0 cada una). Solo se registran organico (108) y Fairtrade (10) porque son las unicas dos que los exportadores escriben. Es un vacio del formulario, no ausencia de produccion. [M]

**8. FAIRTRADE esta hiperconcentrado.** Los 10 items Fairtrade son todos de COCLA, US$ 1.276.458. Todos con clave de origen y serie ICO, ninguno con lote ni numero de marca. [M]

**9. Error mio de analisis, corregido.** Al comparar por exportador primero leí `organico == True` y obtuve ceros para todos. Las columnas se escriben en el libro como texto `SI` o vacio, no como booleanos. Recalculado con `SI` se obtiene 108 organicos y 10 Fairtrade, coherente con la entrada del 2026-10-04. Las cifras de esa entrada no cambian; el error fue solo del script de analisis.

**10. Cambios en los archivos.** Post reescrito a **2.888 caracteres** con la redaccion "menos de un tercio" y el bloque de fincas; sus notas de precision documentan las cuatro afirmaciones retiradas. Backup: `respaldos\duas\DUA_CONSOLIDADO_series_ico_20261002.xlsx`.

> *Append-only. Entrada más reciente primero.*


### 2026-10-06c — tercera depuracion del universo exportador: 54 → 52 → 51, y US$ 2.786,5 M → 2.740 M

**CORRECCION de la linea base.** El depurado del universo exportador se ha aplicado tres veces y la cifra sigue bajando. La version que circula en el post es la tercera:

| Version | Cooperativas cafe/cacao | Con destino UE | FOB acumulado | Que se elimino en esa pasada |
|---|---|---|---|---|
| 1 (2026-10-01) | 54 | 52 | US$ 2.786,5 M | depurado inicial: banano, mango, platano, palta y placeholders por nombre |
| 2 | 53 | 51 | — | una razon social que era un filing comercial, no un productor |
| 3 (**vigente**) | **51** | **51** | **US$ 2.740 M** | una razon social sin evidencia de cultivar cafe o cacao |

**Cifras vigentes para el post:** 51 exportadores de cafe/cacao con destino UE, US$ 2.740 millones de FOB acumulado 2010-2025. Ampliando a las organizaciones cuya razon social no menciona el cultivo, la cota sube a 99 organizaciones y US$ 4.290 millones. El post publica el rango, no el punto. `[M]`

**Por que no hay punto unico.** El filtro depende de si la razon social declara el cultivo: 48 organizaciones del universo tienen nombre generico ("Cooperativa Agricola", "Asociacion de Productores", "Central de Cooperativas") y pueden muy bien ser cafetaleras o cacaoteras. 51 es el piso defendible; 99 es el techo. Publicar un solo numero sin decir cual de los dos es seria falsear la medicion.

**Efecto practico:** la diferencia entre 52 y 51 es de US$ 46,5 millones (1,7%). No cambia ninguna conclusion del post, pero si se cita la cifra hay que citar la version vigente y no la de la entrada del 2026-10-01. Los conteos de OEFA, SENACE y las 245 filas del universo se rehacen con el filtro de 51 cuando se vuelvan a cruzar. [M]

> *Append-only. Entrada más reciente primero.*


### 2026-10-06d — CIERRE DE LA LETRA (d) DEL Art. 2(40): pregunta 14d, derechos de terceros

**Decisión tomada (2026-10-02):** crear la pregunta 14d para la letra **(d) derechos de terceros**, en lugar de dejar la brecha abierta. El hueco 14d que existía desde el 2026-10-01 queda **ocupado por una pregunta real**, sin renumerar 14e–14g, para no romper las referencias cruzadas de la matriz, el dossier y `Scripts\matriz_data.py`.

**Redacción de la pregunta 14d:** "¿existe algún derecho de terceros —carga, embargo, servidumbre, usufructo, arrendamiento o derecho de uso consuetudinario— que condicione o restrinja el uso de la tierra para cultivar café o cacao, o el derecho de la cooperativa a operar en esa finca?", escala de 6 opciones ordenadas 4→0, de "no existe ninguno" a "se han invocado derechos consuetudinarios sin proceso de acuerdo", más "No verificado".

**Fundamento de la redacción.** Se diseñó contra la definición del Art. 2(40)(d) —"derechos de uso y tenencia afectados por la producción, incluidos los derechos de uso tradicional de pueblos indígenas y comunidades locales"— y contra su desarrollo en la guía de la Comisión (C(2024) 7027, §6), que la desarrolla con **cargas, usufructo y acuerdos constructivos con el Estado**. **No por analogía con la Tabla 6**, porque la Tabla 6 no tiene fila para (d): por eso pueden estar sus 7 filas cubiertas y la letra (d) abierta al mismo tiempo. Ese era el nudo real del problema. [V]

**Tres decisiones de diseño que conviene defender:**

1. **"Acuerdo documentado sin título formal" puntúa 2, no 0.** La guía de la Comisión admite los acuerdos constructivos con el Estado: una tenencia legítima sin título formal puede ser válida si está documentada. No es una puerta permisiva, es el criterio del regulador.
2. **"No verificado" se computa como 0**, porque bajo el EUDR la carga de la prueba recae sobre el operador: lo no acreditado se trata como no acreditado. Pero **se reporta aparte el porcentaje de "No verificado"**, para que un cero por falta de información no se confunda con un cero por incumplimiento. Mismo tratamiento que la 15 de D4.
3. **Se distingue de 12 y de 14g**, que son otros failings: la 12 pregunta por superposición espacial, la 14g por el proceso de consentimiento, esta 14d por el título que pesa sobre la tierra. Una parcela sin superposición puede tener usufructo de un tercero; una con servidumbre registral puede no tener conflicto espacial. Un caso puede activar las tres y eso es correcto.

**Límite de verificabilidad, declarado.** La 14d **autodeclara**: el registro de cargas, usufructos y derechos consuetudinarios no es de acceso abierto en el Perú. No la degrada a la categoría de 14a/14b —aquellas no admiten ni contraste parcial— porque admite contraste documental limitado y el RUC del socio cruza con SUNAT y el Registro Catastral. Pero su puntaje se lee como percepción declarada, igual que el resto de D3.

**Efecto en el mapeo: las 8 letras tienen cobertura directa.** (a) 11 y 12 · (b) 14a/14b/14c · (c) no aplicable · (d) **14d** · (e) 13 · (f) 13 parcialmente · (g) 14g · (h) 14e y 14f. Ya no queda ninguna letra abierta por decisión de diseño.

**Recuento del instrumento: 75 → 76 preguntas.** Actualizado en el Dossier (4 lugares), el `Sistema de Indices ISCAM`, `docs\FUNDAMENTOS_UNIVERSO_ENCUESTABLE.md` y el `Plan de Trabajo`. La matriz queda en 76 filas, todas preguntas reales: 0 filas "SIN PREGUNTA". `.docx` regenerado con `Scripts\generar_matriz_docx.py`.

> *Append-only. Entrada más reciente primero.*


### 2026-10-05 — Atributos propagados al directorio de MINAGRI

**Contexto:** los atributos de item quedaron en `DETALLE_ITEMS` y en la hoja nueva `PRODUCTORES_ICO` del consolidado, pero el libro que usa el proyecto como fuente es el directorio de MINAGRI. Ese libro seguia sin verlos: su bloque de DUAs iba de CA a DE y solo traia agregados por anio (n_duas, fob, peso, bultos).

**Aplicado:**
- `por RUC` paso de 31 a 46 columnas. Se anexan 15 al final, para no desplazar las que MINAGRI ya tenia escritas desde CA: `items_con_descripcion`, `n_items_<atributo>` para los 10 atributos declarados (organico, fairtrade, rainforest, utz_jbs, sustentable_cert, arabica, washed, en_bolsa, a_granel, consumo_humano), y `n_ico_distintos`, `icos`, `n_lotes`, `n_marcas`.
- El bloque se propaga solo a MINAGRI por el mecanismo existente: ahora escribe **CA:DT (46 columnas)** en `base 25 detallada`. Verificado que las columnas 1 a 78 del directorio quedan **identicas** y que no se perdio ninguna fila ni columna previa.
- Cada `n_items_<atributo>` cuenta **DUAs en las que el exportador declara el atributo**, no items: un exportador que manda 6 items del mismo lote en una sola DUA cuenta 1. El 0 significa "no lo declara en ninguna DUA", no que el producto sea negativo.

**Lo que muestra el directorio (14 exportadores con DUAs, 11 sin).**

- **9 de 14 exportadores declaran organico** en alguna DUA. Dos destacan: `20140181405` (COOPERATIVA AGRA, 35 DUAs, US$ 4.18M) declara organico en 27 DUAs; `20136201213` (CENTRAL DE COOP, 33 DUAs, US$ 4.42M) en 26, y es el unico con Fairtrade (7 DUAs) y el unico con ICO (20 productores distintos).
- El mayor exportador del corpus, `20542209951` (ASOCIACION VALLE, 46 DUAs, US$ 11.72M), **no declara organico ni Fairtrade en ninguna DUA**, aunque si declara arábica en 42. Es el mayor volumen del conjunto y el que menos atributos de certificacion muestra.
- Solo `20136201213` trae ICO. La cobertura de ICO a nivel de directorio es de 1 exportador de 14.

**Advertencia de lectura.** Estos conteos dicen que el exportador **escribio** el atributo en la declaracion aduanal. No dicen que el producto este certificado, ni que la certificacion siga vigente, ni que el ICO corresponda a un productor con geolocalización. Para EUDR eso sigue siendo un dato declarado en aduana, no una verificación.


### 2026-10-04 — Atributos de los items de DUA: organico, certificacion y ICO de productor

**Contexto:** las descripciones de mercancia de cada item de DUA declaraban atributos que no se estaban extrayendo. Se investigaron los 495 PDF de `fichaduanas` (324 Serie + 171 Consulta) y se determino que el campo 7.35 ya se leia, pero el texto llegaba sucio y sin clasificar, y que escondia el ICO y el numero de marca.

> ⚠ **Los puntos 2, 3 (parrafo de la hoja), 4 (fila ICO) y 6 de esta entrada fueron SUSTITUIDOS el 2026-10-06.** La serie ICO no identifica productores: es el numero de serie del certificado de origen que emite la Camara Peruana del Cafe y Cacao, y se tramita por operacion o lote. Ademas el patron de extraccion perdia 4 de las 24 series. Ver la entrada del 2026-10-06. Se conserva el texto original para dejar traza del error.

**1. El campo 7.35 si se extraia, pero en formato inutil.** El extractor previo lo cortaba a 400 caracteres, lo que truncaba la repeticion y dejaba texto a medio cortar. Dos defectos: (a) **mojibake en el 37.5% de los items** — el PDF es latin-1 y se leia sin corregir, dejando "DescripciÃ³n" y "ORGÃ¡NICO", inservible para buscar; (b) el formulario reimpone la descripcion numerada por linea fisica, y el corte por numero de linea no coincidia con el corte del PDF. Resultado: 311 de 312 items con texto truncado o duplicado.

**2. Hallazgo con valor propio: el ICO del productor estaba en la descripcion y se perdia.** El ICO es el codigo individual del productor, que es la granularidad que el EUDR exige para trazar el origen del commodity. Se recuperaron **20 items con ICO que dan 20 productores distintos**, todos del RUC 20136201213. El caso mas claro es la DUA **001107**: 8 items, cada uno con un ICO diferente (30/11/4039 a 30/11/4046) — es decir, 8 productores distintos en una sola declaración. **Ninguna hoja del libro tenía esta información antes.** [V]

**3. Lo aplicado.**
- **`fichaduanas\desc_items.py`** (nuevo): repara el mojibake, quita la cabecera "Descripción Mercancías", reconstruye el texto repetido y clasifica los atributos declarados.
- **`parse_serie`** entrega la region cruda a ese modulo en vez de trocearla a mano.
- **27 columnas nuevas en `DETALLE_ITEMS`** (49 -> 76): organico, fairtrade, rainforest, utz_jbs, sustentable_cert, arabica, robusta, criollo, trinitario, forastero, amazonico, washed, honey, natural, sun_dried, en_grano, en_bolsa, a_granel, consumo_humano, ico, fda, lote, marca_txt, contrato, peso_declarado_kg, peso_texto_incompleto, atributos (indice compacto).
- **Hoja nueva `PRODUCTORES_ICO`**: una fila por ICO, con RUC del exportador, numero de items y DUAs, FOB, pesos, bultos, atributos y una descripcion de ejemplo. Incluye la columna `cobertura_ico` para que se lea que solo cubre 20 de 312 items.

**4. Medidas sobre el corpus (312 items, 307 de cafe y 5 de cacao).**

| Atributo declarado | Items | % |
|---|---|---|
| organico | 108 | 34.6% |
| arabica | 149 | 47.8% |
| washed | 67 | 21.5% |
| fairtrade | 10 | 3.2% |
| en bolsa | 200 | 64.1% |
| a granel | 74 | 23.7% |
| ICO (productor) | 20 | 6.4% |

**5. Correccion de semantica aplicada en el camino (importante).** La primera version escribia `NO` en 204 items para organico, porque la palabra no aparecia. Eso es un error grave en un atributo de certificacion: **que la DUA no mencione "organico" no significa que el producto no sea organico, significa que la DUA no lo declara.** Se corrigio a tres estados: `SI` si la palabra esta escrita, vacio si no se declara, y nunca `NO`. Se decidio esto deliberadamente pese a que una columna binaria seria mas comoda de filtrar.

**6. Advertencia sobre lo que el ICO NO es.** El ICO se lee de la descripcion de un item. **No es un registro de productores del Estado y no habilita trazar hacia la parcela.** Sirve para contar cuantos productores distintos declara cada exportador y que volumen se asocia a cada uno. El exportador 20136201213 declara 20 productores distintos en 20 items, todos organico+Fairtrade, con FOB entre 123 mil y 187 mil USD. Ese es un hallazgo de concentracion y de traza, no una prueba de cumplimiento.

**7. Verificacion.** Dos corridas consecutivas dan hojas identicas (idempotente). 0 errores de parseo, 0 PDFs no reconocidos, 0 DUAs con items faltantes. Ninguna hoja ni columna previa se perdio: `DUAS` sigue en 29 columnas, `por RUC` en 31 y `base 25 detallada` en 40. Copia previa del libro en la carpeta temporal antes de ejecutar.


> *Append-only. Entrada más reciente primero.*


### 2026-10-03 — Tabla 6 verificada en fuente primaria; 14d resuelta; Instrumento 7 movido

**Contexto:** el punto 11 de la lista de verificación (resolver 14d) llevaba dos dias abierto porque la Tabla 6 no estaba en el repo. Esta entrada lo cierra con fuente primaria, y de paso corrige dos conteos que estaban equivocados en tres documentos.

**1. Tabla 6 localizada y leida.** Descargado el PDF completo de 37 paginas del *Manual de debida diligencia en deforestacion. Pasos para su implementacion en cadenas exportadoras de cafe y cacao* (PROMPERU/BID, setiembre 2025). Copia publica verificada en `culturasostenible.pe`. La Tabla 6 esta en la **pag. 23**, titulada "Categorias de legalidad consideradas por el EUDR". [V] Contenido integro de la tabla:

| Fila | Categoria |
|---|---|
| 1 | Tenencia de la tierra y uso de suelo |
| 2 | Permisos ambientales y cumplimiento forestal |
| 3 | Normas laborales |
| 4 | Consentimiento libre, previo e informado (CLPI) |
| 5 | Cumplimiento de la normativa tributaria y aduanera |
| 6 | Cumplimiento de la normativa comercial |
| 7 | Medidas anticorrupcion |

**2. Hallazgo central: la Tabla 6 ya estaba cubierta al 100%.** Las 7 filas mapean a preguntas existentes — 11 y 12 (fila 1) · 14a/14b/14c (fila 2) · 13 (fila 3) · 14g (fila 4) · 14e (filas 5 y 6, una sola pregunta cubre tributario, aduanero y comercial) · 14f (fila 7). **No faltaba ninguna categoria legal.** Por tanto **14d no se redacta**: inventar una pregunta habria significado anclar una categoria legal inexistente. [V]

**3. Correccion de dos conteos que estaban mal.** El Instrumento 2 y el Dossier afirmaban "5 de las 7 categorias"; el Instrumento 2 afirmaba ademas que 14e y 14f eran "2 de las 7 que faltaban". El numero correcto es **7 de 7 filas de la Tabla 6**. Ambos documentos actualizados. [V]

**4. Correccion de fondo: son dos universos distintos y se estaban mezclando.** El Art. 2(40) del Reglamento (UE) 2023/1115 desglosa **8 categorias, letras (a)-(h)** —mas que 7—, y el manual las agrupa en 7 filas. Verificado contra la *Guidance on the application of the EUDR* de la Comision Europea, C(2024) 7027, parrafo 6 "Legality", que reproduce las ocho letras. [V] Consecuencias aplicadas:

- **Letra (c) — reglas forestales: no aplicable.** Solo es legislacion pertinente cuando se relaciona directamente con la **cosecha de madera**; cafe y cacao no son productos madereros. Se registra como **decision de alcance documentada**, reabrible si el proyecto incorpora productos madereros. No es una omision.
- **Letra (d) — derechos de terceros: la brecha real que queda abierta.** Ninguna pregunta la aborda directamente; la 12 la cubre solo parcialmente y oblicuamente. La definicion del reglamento alcanza derechos de uso y tenencia afectados por la produccion, incluidos los derechos de uso tradicional de pueblos indigenas y comunidades locales; la guia de la Comision la desarrolla con cargas, usufructo y acuerdos constructivos con el Estado. **Queda como decision pendiente del proyecto**, no se redacta sin aprobacion.
- **Letra (f) — derechos humanos protegidos por derecho internacional:** correccion de mapeo, la 14g (CLPI) estaba mapeada a (f) y corresponde a **(g)**. [V]

**5. 14d queda como hueco documentado, no como pregunta.** Se anadio una nota trazada en el Instrumento 2 con las dos tablas (7 filas de la Tabla 6 y 8 letras del reglamento), y una fila 14d en la `Matriz de Cobertura Tecnica` que lo registra explicitamente. **La numeracion 14e-14g no se renumera** porque romperia las referencias cruzadas de la matriz, el Dossier y `Scripts\matriz_data.py`.

**6. Instrumento 7 movido.** De `ISCAM\` a `Instrumentos\`, que es donde lo referencian nueve archivos del paquete. Actualizadas las notas de ubicacion en los dos documentos de `ISCAM\` que lo citan y la nota de cabecera del indice en `EUDR\Herramientas de Diagnostico EUDR - Cooperativas.md`. Cierra el punto pendiente registrado el 2026-10-02.

**7. Matriz de cobertura reconstruida desde el script.** `Scripts\matriz_data.py` pasa a 76 filas y corrige el mapeo de las letras del Art. 2(40) en las filas D3. La tabla del `.md` se regenero desde el script, que es la fuente de verdad; el encabezado del documento paso de 73 a 76 filas. **Pendiente:** la version `.docx` de la matriz quedo desactualizada respecto del `.md` y hay que regenerarla.

**Leccion operativa que queda:** cuando se necesite el manual PROMPERU/BID, la copia verificada esta en `culturasostenible.pe/archivos/galeria-caminosostenibilidad/`. No estaba en el repo y su ausencia fue la causa de que 14d quedara dos dias sin resolver.

### 2026-10-02 — Ajuste del Instrumento 2 por el hallazgo de verificabilidad

**Contexto:** revisión de limpieza del paquete de instrumentos tras medir el hueco de legalidad ambiental (§8.10.1). Dos correcciones aplicadas.

**Aplicado:**

1. **14b reetiquetada como autodeclarada sin verificación pública.** El encabezado de la pregunta ahora lo declara, y se añadió una nota de advertencia antes del bloque de puntuar D3. La nota documenta que la autorización ambiental agraria la emite MIDAGRI y no está publicada como datos abiertos; que ninguna de las 38 apps del catálogo público la cubre; y que OEFA (14.724 expedientes, corte 2024-04-30) cubre sanciones, no autorizaciones, por lo que no sirve para verificar conformidad. **Regla operativa resultante:** el puntaje agregado de D3 se reporta como *percepción de cumplimiento declarada por la cooperativa*, nunca como conformidad verificada. La pregunta se mantiene en el instrumento y conserva su puntaje — lo que se limita es lo que el puntaje puede afirmar.

2. **Conteos unificados a 75** en `Ficha Tecnica y Guia de Aplicacion - Instrumento 2.md` (que se contradecía a sí mismo: 75 en el párrafo de estructura, 73 en el de remapeo) y en `Plan de Trabajo - Proximos 75 Dias.md`. El 73 era válido pero estaba congelado antes del agregado de P11 y P12 (2026-09-17).

**Corrección de un error previo propio:** §8.13 afirma que hay conflicto de numeración D1–D11 entre los instrumentos y un informe anterior. **Es falso.** La numeración de `Instrumento 1` y `Instrumento 2` es correcta y coincide con §2.6. La numeración antigua proviene del informe preliminar descartado. No se modificó ningún instrumento por este punto.

**Observación registrada, sin acción:** el Instrumento 7 vive en `ISCAM\`, no en `Instrumentos\`, pese a que nueve archivos del paquete lo referencian desde `Instrumentos\`. No se movió el archivo.

⚠ **Punto 11 de la lista de verificación queda parcialmente resuelto:** falta resolver 14d. Requiere la Tabla 6 del Manual PROMPERÚ/BID o del *Documento orientador ADEX/MIDAGRI/EFI*, **ninguno de los dos presente en el repo**. No se redactó la pregunta porque implicaría reconstruir una categoría legal sin anclaje al texto oficial.

---

### 2026-10-01 — Línea base

**Contexto:** sesión de investigación sobre el impacto del EUDR en cooperativas de café y cacao. Se investigó marco regulatorio, avances institucionales, estado de preparación y exposición cuantificada.

**Hitos registrados:**
- Confirmada la clasificación **`standard risk`** del Perú y, con ella, la **inaplicabilidad del Art. 4a**. Este es el hallazgo que reorganiza todo el análisis.
- Confirmado el calendario: 30-dic-2026 (grandes), 30-jun-2027 (micro/pequeñas), 30-dic-2027 (café soluble).
- MEDIDO: **0 de 126 exportadores** tienen certificación ambiental SENACE; **1 de 1.870** proyectos menciona café/cacao y es una planta industrial.
- MEDIDO: el universo de riesgo se reduce a **52 cooperativas con destino UE y US$2.786,5M de FOB acumulado**.
- Corrección: el informe inicial sobreestimaba la exposición al citar "245 organizaciones" y "118 con destino UE". Las cifras operativas son 54 café/cacao → 52 con destino UE.
- **Brecha abierta:** no existe conector a las evaluaciones ambientales del sector agrario de MIDAGRI (el complemento de §2.5). Es el corte que falta para cerrar D3 con dato propio.
- **Nota de infraestructura (repo `appsperu`):** el diagnóstico `rastro_health` reporta `sin_base / Sin NEON_DATABASE_URL` para apps en modo stdio. **Ese mensaje no significa que falte la base** — el verificación de salud evalúa un secret de Neon inexistente, mientras el dato real va por HTTP al puerto local. El diagnóstico útil es el `ECONNREFUSED` en los logs del servidor. Las apps del repo requieren `docker compose up -d` porque solo persiste el volumen, no el contenedor.

**Endpoints que se intentaron y resultaron inútiles para el Anexo VII** (`catastro-forestal`, `areas-protegidas`) y **el único que aporta algo** (`infracciones-ambientales`) están documentados en §8.10.1, con sus conteos reales y sus límites de fecha.

⚠ **Hallazgo relevante de esta revisión:** `infracciones-ambientales` (OEFA) tiene **14.724 expedientes**, pero su **corte es 2024-04-30**. No cubre 2024–2026, la ventana que decide el EUDR. Se puede usar como línea de base histórica, no como verificación actual. Registrado para que nadie lo cite sin la salvedad.

⚠ `actividad-agraria` tiene el contenedor levantado pero **sin ninguna tabla** — ni siquiera `schema_migrations`. Necesita `npm run migrate` + `npm run ingest` antes de ser citable. No se hizo porque queda fuera del alcance del hallazgo de §2.5.

**Nota de infraestructura:** las cuatro apps auditadas estaban en `Exited (255)` desde hacía 2 días. Solo el volumen persiste, no el contenedor. `docker compose up -d` por app. Ninguna escritura persistente: la staging table `stage_eudr_exp` se creó y se eliminó en cada cruce.

---

## 6. Comandos de verificación re-ejecutables

### 6.1 Levantar la app SENACE y confirmar el dataset

```powershell
cd C:\Users\acuba\appsperu\apps\senace-cartera-proyectos\api
docker compose up -d        # el volumen persiste; el contenedor NO
npm run migrate             # "Sin migraciones nuevas" → datos intactos
npm run dev                 # puerto 4033
```

### 6.2 Recargar desde el origen público (si la data está vieja)

```powershell
npm run ingest:senace       # 3 llamadas a datosabiertos.senace.gob.pe, sin auth
```

### 6.3 Repetir el cruce exportadores ↔ SENACE

```powershell
docker cp C:\Users\acuba\eudrperu\data\backup\sunat_todos_exportadores.csv `
  senace-cartera-proyectos-postgres-1:/tmp/exp.csv

docker exec senace-cartera-proyectos-postgres-1 psql -U senace_cartera_proyectos `
  -d senace_cartera_proyectos -c `
  "CREATE TABLE IF NOT EXISTS stage_eudr_exp (ruc text, name text, fob double precision, ops int, npaises int, anio_min int, anio_max int, paises text);"

docker exec senace-cartera-proyectos-postgres-1 psql -U senace_cartera_proyectos `
  -d senace_cartera_proyectos -c `
  "COPY stage_eudr_exp FROM '/tmp/exp.csv' WITH (FORMAT csv, HEADER true);"

# → debe devolver 0. Si devuelve >0, hay nuevos registros SENACE: anotarlo en §5.
docker exec senace-cartera-proyectos-postgres-1 psql -U senace_cartera_proyectos `
  -d senace_cartera_proyectos -c `
  "SELECT count(DISTINCT e.ruc) AS cruzan_senace FROM stage_eudr_exp e JOIN senace_cartera_proyectos s ON s.ruc = e.ruc;"

docker exec senace-cartera-proyectos-postgres-1 psql -U senace_cartera_proyectos `
  -d senace_cartera_proyectos -c "DROP TABLE IF EXISTS stage_eudr_exp;"
```

### 6.4 Consulta directa al origen público (sin base de datos)

```
GET https://datosabiertos.senace.gob.pe/home/VistaDatos/JsonCarteraProyecto?q=<estado>
```
`q` ∈ {`Aprobado`, `Desaprobado`, `En Evaluacion`} → 1.568 + 176 + 126 = **1.870 filas**.

⚠ La respuesta viene en una sola línea de ~700 KB. Las herramientas de búsqueda con límite de 64 KB por registro no pueden buscar texto adentro — usar la API en su lugar.

### 6.5 Comandos MCP (con la app levantada)

| Objetivo | Tool |
|---|---|
| Bucket agrícola | `senace_cartera_proyectos` con `actividad: "Agricultura"` |
| Búsqueda de cultivo | `senace_cartera_proyectos` con `texto: "cafe"` / `"cacao"` |
| Un RUC puntual | `senace_cartera_proyectos` con `ruc: "20113940515"` |
| Detalle de un proyecto | `senace_cartera_proyecto_detalle` con `senaceId` |
| Infracciones ambientales (OEFA) | `infracciones_ambientales` con `departamento` / `subsector_economico` |

### 6.6 Levantar las apps de apoyo (§8.10.1)

```powershell
foreach ($a in 'infracciones-ambientales','catastro-forestal','areas-protegidas','actividad-agraria') {
  docker compose -f "C:\Users\acuba\appsperu\apps\$a\api\docker-compose.yml" up -d
}
```

⚠ **`actividad-agraria` requiere `npm run migrate` + `npm run ingest`** — el volumen está vacío, no tiene tablas.

⚠ El cruce OEFA usa credenciales distintas a las demás apps: usuario `infracciones_ambientales`, base `infracciones_ambientales`.

```powershell
# Verificar freshness antes de citar cualquier cifra de infracciones
docker exec infracciones-ambientales-postgres-1 psql -U infracciones_ambientales \
  -d infracciones_ambientales -t -c \
  "SELECT max(fecha_corte), max(fecha_inicio_sup), count(*) FROM infracciones_ambientales;"
# Al corte: 2024-04-30 | 2023-06-12 | 14724  → NO cubre 2024-2026
```

---

## 7. Fuentes

**Primarias (normativa):** Reg. (UE) 2023/1115 · Reg. (UE) 2025/2650 · Reg. Impl. (UE) 2025/1093 (benchmarking) · Reg. Impl. (UE) 2026/1565 · COM(2026)191 final · Green Forum EC (Country Classification List · Information System) · Acta Delegado Anexo I 13-jul-2026.

**Institucionales (Perú):** MIDAGRI (PPA/Identidad Digital, RM D000325-2026-MIDAGRI-DM) · MINCETUR · PROMPERÚ (notas may-2026 y jul-2026) · SENACE (datos abiertos, 1.870 proyectos) · GeoBosques/MINAM · MapBiomas Perú.

**Sectoriales:** Cámara Peruana de Café y Cacao (jul-2025) · CENFROCAFE · PRODUCE · ADEX · Inforegión (jul-2026) · Solidaridad Latam (jun-sep 2026) · Rainforest Alliance (Origin Issue Assessment café Perú; ficha Perú 2026) · EFI.

**Externas:** Global Forest Watch · European Forest Institute.

**Secundarias (usar con cautela, marcar como tales):** vira.pe · eudr.today · eudr-navigator · tanso.de · roedl.com · coolset · ICE · Mayer Brown · Tanso.

**Datos propios:** `eudrperu/data/backup/sunat_todos_exportadores.csv` · `EUDRPERU_universo_consolidado.csv` · `eda_output/EDA_EUDR_hallazgos.md` · `docs/FUNDAMENTOS_UNIVERSO_ENCUESTABLE.md` · base `senace_cartera_proyectos` (appsperu).

**Enlaces oficiales citados en §8:** `https://ppa.midagri.gob.pe/` · `https://rutex.promperu.gob.pe/` · `https://pro.globalforestwatch.org/` · `https://www.secompetitivo.com/` · `https://datosabiertos.senace.gob.pe/home/VistaDatos/JsonCarteraProyecto` · MIDAGRI Mesa Ayuda PPA `sisppa@midagri.gob.pe` (950 105 25 / 990 533 188) · PROMPERÚ Sostenibilidad `sostenibilidad@promperu.gob.pe`.

---

## 8. ANEXO — Avances institucionales en detalle (endpoint por endpoint)

> Anexo documental. No es línea base: es el desarrollo fino de §2.4, con la trazabilidad de cada consulta. Congelado al 2026-10-01. Registra **qué se invocó, contra qué endpoint, y qué devolvió**, para que una actualización diaria pueda re-ejecutar exactamente las mismas llamadas y comparar deltas.

### 8.1 MIDAGRI — estrategia nacional de información y geolocalización

**8.1.1 Padrón de Productores Agrarios (PPA) — infraestructura base**

| Indicador | Valor | Fuente |
|---|---|---|
| Productores registrados | 2,1+ millones | gob.pe, 05-03-2026 |
| Productores café/cacao/palma | ~410.000 | Doc. técnico MIDAGRI 2025 |
| Con celular + georreferencia de punto | >80% de cafetaleros/cacaoteros | Doc. técnico MIDAGRI 2025 |
| Variables registradas | 38 + georreferencia de parcela | Doc. técnico MIDAGRI 2025 |
| Meta 2026 | 50% de productores café/cacao/palma con polígono | Doc. técnico MIDAGRI 2025 |
| Tasa de éxito de georreferencia | 86% | MIDAGRI 2024 |

⚠ **Contradicción interna que hay que resolver:** la meta declarada es *50% con polígono*, y el resultado reportado es 181.731 parcelas. Si la meta se cumplió, entonces las 181.731 sería el 50% de ~363.000 productores, lo que es consistente con el rango de 350.000 de la Cámara. Esto **reforza** que la cobertura real de café+cacao está por debajo del 100% pero no tan baja como sugería la lectura inicial. Anotar en §5 cuando MIDAGRI aclare el denominador exacto de la meta.

**8.1.2 AgroDigital — aplicativo móvil oficial**

- Lanzamiento: Foro Internacional de Tarapoto, **30-09-2025** (Min. Manero).
- Funcionalidades núcleo: georreferenciación de polígonos **offline** para zonas sin cobertura; monitoreo satelital con integración **GeoBosques/MINAM**; consulta de precios, alertas técnicas, insumos y certificaciones; **Identidad Digital del Productor** (documento electrónico único); plataforma bidireccional Estado↔productor; gestor de oferta de servicios (créditos, semillas, seguros agrarios).
- **Visor de avance en tiempo real** del despliegue de georreferenciación en campo.
- Beneficiarios declarados: 400.000+ productores de café y cacao (~25% de los productores nacionales).

**8.1.3 Resultado de georreferenciación masiva (marzo 2026)**

| Métrica | Valor | Detalle |
|---|---|---|
| Parcelas geolocalizadas | **181.731** | Café, cacao y palma aceitera |
| Memorandos de entendimiento | **69** | DEVIDA, IICA, Helvetas, AL-Invest Verde UE, organizaciones de productores |
| Alianzas tecnológicas | **WRI (Global Forest Watch)** + **FAO (WHISP)** | Evaluación libre de deforestación EUDR |
| Plataforma web nacional | En desarrollo | Centraliza información oficial, herramientas y materiales de difusión |
| Cobertura territorial | 13 regiones clave | Ucayali, San Martín, Cajamarca, Junín, Cusco, Amazonas, entre otras |

**8.1.4 Piloto Tocache (dic-2023) — precedente técnico**

- Ubicación: Tocache, San Martín (DRASAM). Cooperación: Solidaridad + European Investment Initiative (EII).
- Resultado: **500+ productores georreferenciados en jornada única**.
- Salida del piloto: mejora de la app que desemboca en la versión final con georreferenciación *offline* y visor en tiempo real.
- Proceso de validación probado: parcela georreferenciada → cruce con GeoBosques (MINAM) → si instalación **pre-2021** → emisión de **Constancia Libre de Deforestación** vía app.

**8.1.5 Hoja de ruta georreferenciación → Constancia (lanzada 24-06-2026)**

```
Productor PPA → App Identidad Digital → Georreferencia polígono → Envía a MIDAGRI
→ Validación GeoBosques (corte pre-2021) → Constancia Libre de Deforestación (app)
```

- **260+ cartas cursadas** a asociaciones, cooperativas y exportadoras de la UE solicitando polígonos.
- ⚠ **Financiamiento pendiente:** ampliación presupuestal del MEF para el escalamiento nacional. Bloqueante real, no administrativo.
- Aliados de escalamiento: AL-Invest, Solidaridad, EII.

**8.1.6 Documento Orientador de Legalidad Café/Cacao (publicado 17-06-2026)**

- Proceso: grupo multisectorial de **16 instituciones** → análisis de **~200 normas** → selección de las vinculadas a EUDR.
- Contenido: normativa peruana clasificada por categorías legales EUDR (DD.HH., ambientales, tenencia de tierra, laboral, fiscal).
- Propósito: orientar a operadores UE y compradores sobre las evidencias legales exigibles en el Perú.
- **Carácter:** no vinculante, no crea obligaciones, no reemplaza la debida diligencia propia.
- Apoyo: proyecto SAFE (GIZ), cofinanciado por UE, Países Bajos y Alemania.
- Descarga oficial: `gob.pe/institucion/midagri/informes-publicaciones/8275709`.

**8.1.7 Perfil de Riesgo País (en consolidación, compromiso de entrega mayo-2026)**

- Objetivo: dar contexto legal del Perú a operadores UE para reducir la intensidad de su debida diligencia.
- Contenido: **40 normas nacionales clave** (DD.HH., ambientales, tenencia).
- Estado al corte: **en consolidación**. No consta entrega.
- Impacto esperado si se concreta: facilitar la calificación de "riesgo despreciable" a importadores de la UE.

⚠ Ver §0 punto 2 y §2.1: el *country risk classification* del Perú es lo que habilita el Art. 4a, y este *Perfil de Riesgo País* es un documento distinto, de alcance nacional. No confundir.

### 8.2 PROMPERÚ — Programa de Debida Diligencia (2023–2026)

**8.2.1 Cronología y alcance por ediciones**

| Edición | Año | Organizaciones | Productores | Regiones |
|---|---|---|---|---|
| Piloto | 2024 | 17 | ~9.000 familias | Amazonas, Cajamarca, Cusco, Junín, San Martín |
| 1.ª edición | 2025 | 11 (políticas antideforestación) + 21 (programa completo) | 7.880 | Cajamarca, San Martín, Lima |
| 2.ª edición | 2026 | **21** | 8.000+ | Amazonas (4), Cajamarca (4), San Martín (5), Junín (6), Cusco (1), Ayacucho (1) |

Apoyo técnico y financiero por edición: BID, Rikolto, WRI, CEPAL, Helvetas, SeCompetitivo, FOLUR, APPCACAO, SAFE/GIZ.

**8.2.2 Requisitos de ingreso de una organización**

1. Constitución legal ≥2 años, RUC activo, Registro Público.
2. Contraparte técnica identificada (sostenibilidad / certificaciones / SIC).
3. Certificación sostenible (orgánica, Fairtrade, Rainforest Alliance u otra).
4. Estructura de comunicaciones e imagen corporativa (web, correo corporativo).
5. Test Exportador RUTEX ≤1 año — `https://rutex.promperu.gob.pe/`.
6. Sin deudas documentarias o económicas con PROMPERÚ.
7. Exportación directa o indirecta a la UE en el último año.

⚠ El requisito 7 es unarestriction estructural: el programa **excluye por diseño** a las cooperativas que no exportan a la UE. Dado que el universo relevante son 52 organizaciones con destino UE (§3.2), la cobertura del programa respecto de ese universo es mucho mayor que respecto del total de 245 — y esto **no estaba claro** en versiones previas de este análisis.

**8.2.3 Entregables por organización**

1. **Política Cero Deforestación** (documento corporativo).
2. **Protocolo de Debida Diligencia** alineado a EUDR (recolección de información, análisis de riesgo, mitigación).
3. **Plan de Prevención/Mitigación** de riesgos de deforestación en la cadena de suministro.
4. **Protocolos anti-mezcla** (producto conforme vs. producto no verificado).
5. **Manual de Debida Diligencia de Deforestación** (guía replicable).

**8.2.4 Curso de Formación para Implementadores (agosto 2025)**

- 3 sedes: Tarapoto (5–7/08), Jaén-Cajamarca (19–21/08), Lima (26–28/08).
- 60+ participantes: exportadores, cooperativas, académicos, funcionarios.
- Financiamiento: BID + apoyo GIZ + Rikolto.
- Metodología: bloques teórico-prácticos con simulación de los pasos de debida diligencia sobre casos reales.
- Anfitrión local: Plataforma Multiactor Café de Cajamarca.

**8.2.5 Ciclo de talleres multiplicadores 2026 (mayo–junio)**

| Taller | Fecha | Ubicación | Participantes | Alcance indirecto |
|---|---|---|---|---|
| 1 | Mayo | Pucallpa (Ucayali) | ~20 | 1.300+ productores |
| 2 | 26–28/05 | Pichanaqui (Junín) | ~20 | 1.300+ |
| 3 | 2–4/06 | Quillabamba (Cusco-La Convención) | ~20 | 1.300+ |
| 4 | 9–11/06 | Chachapoyas (Amazonas) | ~20 | 1.300+ |
| **Total** | | **4 talleres** | **80+** | **13.000+** |

- Financiamiento: proyecto SAFE (GIZ), cofinanciado por UE + Países Bajos (BZ) + Alemania (BMZ).
- Liderazgo SAFE: MIDAGRI. Ejecución: GIZ GmbH.
- Contacto: `sostenibilidad@promperu.gob.pe`.

**8.2.6 Eventos de difusión de resultados 2025 (celebrados en 2026)**

- 3 eventos: Jaén (Cajamarca), Moyobamba (San Martín), Lima.
- Capacitación en Global Forest Watch Pro: **90+ participantes** en Cajamarca, San Martín, Amazonas y Junín.
- Objetivo: monitoreo, análisis y verificación de producción libre de deforestación.

### 8.3 MINCETUR + Cooperación Suiza (SeCompetitivo) — ecosistema articulado

**8.3.1 Iniciativa "Sostenibilidad y Escalamiento RPE"**

- Marco: SeCompetitivo Fase III (SECO/Suiza, 2023–2027, USD 12 MM).
- Facilitador: HELVETAS Swiss Intercooperation Perú.
- Contraparte nacional: MEF/VME + CNCF + Cámara de Comercio de La Libertad.
- Regiones de intervención: Piura, San Martín, La Libertad, Amazonas.
- Aliados EUDR: BID, CEPAL, Cooperación Suiza, SeCompetitivo, SAFE, Rikolto, WRI, FOLUR (MINAM).

**8.3.2 Resultados reportados (El Peruano, ago-2026)**

| Actividad | Alcance |
|---|---|
| Productores capacitados | **13.000+** (café y cacao: asociaciones, cooperativas, MIPYMES) |
| Políticas antideforestación 2025 | **11 organizaciones** (Amazonas, Cajamarca, Cusco, Junín, San Martín) |
| Manual de Debida Diligencia | 1 documento base, elaborado desde las experiencias piloto de 2024 |
| Capacitación Global Forest Watch Pro | **90+ participantes** en 4 regiones |
| 2.ª edición del Programa de Debida Diligencia | **21 organizaciones / 8.000+ productores**, 6 regiones, en ejecución 2026 |

**8.3.3 Mapa de articulación institucional**

```
MINCETUR (rector de comercio)
  ↔ PROMPERÚ (ejecución de capacitación y asistencia técnica)
  ↔ MIDAGRI (PPA, AgroDigital, GeoBosques, marco legal)
  ↔ SeCompetitivo / HELVETAS (financiamiento, metodología, escalamiento)
  ↔ SAFE / GIZ (cofinanciamiento UE + PB + Alemania; ejecución técnica)
  ↔ FOLUR / MINAM (cadenas de valor libres de deforestación en la Amazonía)
  ↔ APPCACAO (representación gremial de cacaoteros)
  ↔ Rikolto / WRI / BID / CEPAL (asistencia técnica especializada)
```

### 8.4 Exportaciones piloto con trazabilidad verificada (2025)

| Organización | Producto | Volumen | Destino | Trazabilidad | Región |
|---|---|---|---|---|---|
| AP Cuencas del Huallaga | Cacao orgánico | **100 TM** | Italia | Georreferenciada completa | San Martín |
| Asoc. Mujeres Las Flores de Luya | Café verde | **37 TM** | UE + EEUU | Primera exportación trazada | Amazonas |
| CAECAM (Coop. Agraria Ecológica Caniari Amazónica) | Cacao | **175 TM** | UE + Norteamérica | Trazabilidad geográfica | Ucayali |

**Lectura para el análisis:** son **312 TM en total** frente a las ~173.700 TM de exportaciones de cacao y ~242.000.000 kg de café de 2025. Es decir, los pilotos suman **0,2%** de las exportaciones anuales de cacao y son **0,1%** de las de café. Demuestran factibilidad técnica y comercial, **no un precedente de volumen**. Ninguna de las tres está en el universo de 52 organizaciones con destino UE (§3.2), lo que sugiere que el piloto no escaló a las organizaciones exportadoras de tamaño relevante.

### 8.5 Arquitectura tecnológica integrada del Estado

```
PPA (2,1M productores, 38 variables + georreferencia)
  ↕
AgroDigital (app móvil: polígonos, offline, Identidad Digital)
  ↕
Observatorio PPA (visor geoespacial: análisis espacial, focalización de servicios)
  ↕
PLATAFORMA NACIONAL DE TRAZABILIDAD (en desarrollo)
  DNI del productor + manifiesto de carga ↔ polígonos PPA → origen
  acceso libre web → aduanas de la UE
  ↕
Global Forest Watch Pro (WRI)          WHISP (FAO)
```

**Interoperabilidades validadas:**
- PPA ↔ Global Forest Watch Pro (WRI): monitoreo de deforestación en tiempo real.
- PPA ↔ WHISP (FAO): parámetros de superficie armonizados|scale global.
- PPA ↔ GeoBosques (MINAM): mapa de cobertura forestal oficial → Constancia Libre de Deforestación.
- TRACES NT (UE): sistema aduanero + ventanilla de debida diligencia + código único de operación.
- Declaración anual agregada: simplificación del Reglamento 2025/2650 (múltiples lotes en una declaración).

### 8.6 Mapa de cooperación internacional

| Programa | Donante / Ejecutor | Periodo | Foco EUDR |
|---|---|---|---|
| **SAFE** (Agricultura Sostenible Ecosistemas Forestales) | UE + Países Bajos + Alemania / GIZ; lidera MIDAGRI | 2023–2027 | Capacitación, metodología de debida diligencia, talleres multiplicadores, plataforma de legalidad |
| **SeCompetitivo Fase III** | SECO (Suiza) / HELVETAS / MEF-CNCF | USD 12 MM / 2023–2027 | Competitividad de cadenas, escalamiento RPE, 13.000+ productores |
| **FOLUR** (Food Systems, Land Use and Restoration) | GEF / MINAM / Banco Mundial (GEF ID 10307) | — | Cadenas de valor libres de deforestación en la Amazonía; actualización PROCOMPITE San Martín |
| **AL-Invest Verde** | UE / IICA / Helvetas | 2021–2025 (extensión) | 69 MoUs, georreferenciación masiva, asistencia técnica en campo |
| **Pilotos SAFE** | BID / Rikolto / WRI / CEPAL / Helvetas | 2024–2025 | 17 organizaciones piloto, kit de herramientas, manual de debida diligencia |
| **Global Forest Watch Pro** | WRI / BID | Acceso gratuito | Monitoreo satelital, alertas de deforestación, verificación |
| **WHISP** | FAO | Acceso gratuito | Parámetros de superficie globales, evaluación libre de deforestación |

### 8.7 Cronograma oficial de hitos 2026

| Fecha | Hito | Responsable | Estado al corte |
|---|---|---|---|
| 24-06-2026 | Lanzamiento oficial **Identidad Digital del Productor Agrario** | MIDAGRI | Anunciado |
| 30-06-2026 | Entrega del **Perfil de Riesgo País** (40 normas) a la UE | MINCETUR / MIDAGRI / UE | En consolidación |
| Jul–dic 2026 | Escalamiento de georreferenciación nacional (con ampliación MEF) | MIDAGRI + AL-Invest + Solidaridad + EII | Pendiente presupuesto |
| **30-12-2026** | **Entrada en vigencia EUDR — operadores grandes (UE)** | Comisión Europea | **Fecha límite** |
| **30-06-2027** | Entrada en vigencia — micro y pequeños operadores | Comisión Europea | **Fecha límite** |
| 2026 | 2.ª edición del Programa de Debida Diligencia (21 orgs, 8.000 prod.) | PROMPERÚ / SeCompetitivo / FOLUR / APPCACAO | En ejecución |
| 2026 | Plataforma Nacional de Trazabilidad operativa | MIDAGRI / SIEA | En desarrollo |

### 8.8 Brechas declaradas por las propias fuentes oficiales

Estas brechas están **reconocidas en documentos del Estado y de la cooperación**, no son una interpretación nuestra. Es el material más citable para el paper, porque las admite quien las implementa.

| Brecha | Evidencia textual de la fuente | Impacto |
|---|---|---|
| **Georreferencia de punto vs. polígono** | Doc. MIDAGRI: *"la ubicación en punto no es suficientemente precisa para EUDR"* | Los ~410.000 cafetaleros/cacaoteros requieren upgrade a polígono |
| **Cobertura asistida vs. universo** | 59 organizaciones asistidas (17+21+21) vs. 245 cooperativas mapeadas = **<25%** | La mayoría de cooperativas sin asistencia técnica directa |
| **Financiamiento del escalamiento** | MIDAGRI: *"ampliación presupuestal del MEF pendiente"* | Riesgo de no alcanzar la meta de 50% de polígonos en 2026 |
| **Actualización continua** | Ethiquable (Solidaridad): *"la actualización permanente de bases de datos genera costos adicionales por ingreso/retiro de socios y ampliación de parcelas"* | Costo recurrente no cubierto por ningún actor |
| **Pequeños no asociados** | Solidaridad: *"70% de 300.000 familias no está asociado"* | Exclusión masiva si no hay mecanismo inclusivo |
| **Calidad de datos satelitales** | CamCafé: *"deficiencias en la calidad de datos satelitales, uso de la información y mapeo real de parcelas"* | Falsos positivos y falsos negativos en la verificación de libre deforestación |

### 8.9 Endpoints y consultas invocadas

**8.9.1 API pública de SENACE** — fuente del hallazgo de §2.5

```
GET https://datosabiertos.senace.gob.pe/home/VistaDatos/JsonCarteraProyecto?q=<estado>
```
- `q` = `Aprobado` → 1.568 filas
- `q` = `Desaprobado` → 176 filas
- `q` = `En Evaluacion` → 126 filas
- **Total: 1.870 registros.** Sin autenticación.

⚠ La respuesta llega en una sola línea de ~700 KB. Las herramientas con límite de tamaño por registro no pueden buscar texto dentro de la respuesta; hay que pasar por la API o por la base local.

**8.9.2 Tools MCP (Rastro) usadas para el cruce**

| Tool | Parámetros | Propósito |
|---|---|---|
| `senace_cartera_proyectos` | `actividad: "Agricultura"` | Bucket agrícola → 182 proyectos |
| `senace_cartera_proyectos` | `texto: "cafe"` / `texto: "cacao"` | Búsqueda de cultivo → 0 / 0 |
| `senace_cartera_proyectos` | `ruc: "20601645964"` | Localización del único hit (BRITT) |
| `senace_cartera_proyecto_detalle` | `senaceId: 697` | Ficha completa del hit: resolución, coordenadas, titular |
| `infracciones_ambientales` | `departamento` / `subsector_economico` | Cruce negativo contra el universo exportador → 0, salvo COCLA (§8.10.1) |

**8.9.3 Consultas SQL de cruce** (ver §6.3 para el procedimiento completo)

```sql
-- Cruce por RUC (devuelve 0)
SELECT count(DISTINCT e.ruc)
FROM stage_eudr_exp e
JOIN senace_cartera_proyectos s ON s.ruc = e.ruc;

-- Búsqueda de café/cacao en todos los campos de texto (devuelve 1)
SELECT senace_id, titular, titulo_proyecto, tipo, estado
FROM senace_cartera_proyectos
WHERE titular ILIKE '%cafe%' OR titular ILIKE '%cacao%'
   OR titulo_proyecto ILIKE '%cafe%' OR titulo_proyecto ILIKE '%cacao%'
   OR unidad_proyecto ILIKE '%cafe%' OR unidad_proyecto ILIKE '%cacao%'
   OR descripcion ILIKE '%cafe%' OR descripcion ILIKE '%cacao%'
   OR actividad ILIKE '%cafe%' OR actividad ILIKE '%cacao%';

-- Descomposición del bucket agrícola
SELECT tipo, count(*), count(*) FILTER (WHERE titular_publico) FROM senace_cartera_proyectos
WHERE actividad = 'Agricultura' GROUP BY tipo ORDER BY count(*) DESC;
```

**8.9.4 Comandos de infraestructura**

```powershell
docker compose up -d          # apps/senace-cartera-proyectos/api
npm run migrate               # "Sin migraciones nuevas por aplicar"
npm run dev                   # puerto 4033
docker exec senace-cartera-proyectos-postgres-1 psql -U senace_cartera_proyectos -d senace_cartera_proyectos -c "..."
```

**8.9.5 Consultas web aplicadas al marco regulatorio y a los avances institucionales**

Búsquedas ejecutadas para construir §2 y §8:
- Aplicación EUDR 2026-2027, revisiones 2025/2650 y COM(2026)191, reglas técnicas 2026/1565.
- Country risk classification del Perú (bajo / estándar / alto).
- Art. 4a *micro and small primary operator* y requisitos.
- MIDAGRI AGRODIGITAL PPA georreferenciación polígonos EUDR 2026.
- PROMPERÚ programa debida diligencia EUDR 2025-2026 manual.
- MINCETUR SeCompetitivo SAFE GIZ FOLUR capacitación 2026.
- Rainforest Alliance EUDR opt-in criteria, Origin Issue Assessment café Perú.
- SOLIDARIDAD, ADEX, CENFROCAFE y PRODUCE sobre cumplimiento, riesgos y documentación de origen.

⚠ Estas consultas son de motores de búsqueda general. Los datos así obtenidos son `[V]` solo cuando la fuente es primaria identificable; en caso contrario tratarlos como `[I]` hasta confirmar contra el documento oficial.

### 8.10 Endpoint que falta y por qué importa

No existe endpoint público de **evaluaciones ambientales del sector agrario**. La autorización ambiental del agro la emite MIDAGRI bajo su reglamento sectorial (DS 006-2024-MIDAGRI, en proceso de modificación por la RM D000325-2026), y ese registro no está publicado como datos abiertos.

Consecuencia directa: el §2.5 del análisis no puede cerrarse con una vía pública. Para un operador europeo, la verificación de la legalidad ambiental de una parcela de café o cacao en el Perú **no tiene fuente oficial consultable**. Ese es el hallazgo estructural más fuerte del proyecto, y se sostiene precisamente porque el endpoint no existe.

**Es el corte de investigación prioritario para la línea base.** Si en algún momento MIDAGRI publica el registro, hay que (a) re-ejecutar §6.3, (b) esperar a que el ordenamiento de §2.5 caiga, y (c) anotar en §5 con `⚠ SUSTITUIDO`.

#### 8.10.1 Búsqueda de un endpoint sustituto — apps locales (ejecutado 2026-10-01)

Se levantó y auditó el conjunto de apps de `appsperu` buscando alguna fuente que cubriera el hueco de legalidad del Anexo VII. **Ninguna lo cubre**, pero una aporta un dato negativo nuevo y citable.

| App | Contenedor | Registros | ¿Aporta al Anexo VII? |
|---|---|---|---|
| `senace-cartera-proyectos` | `senace-cartera-proyectos-postgres-1` | 1.870 | No — es EIA industrial/energía, no evaluación agraria (§2.5) |
| `infracciones-ambientales` | `infracciones-ambientales-postgres-1` | **14.724** | **Parcial — ver abajo** |
| `catastro-forestal` | `catastro-forestal-postgres-1` | 5.391 | No — titulación forestal (SERFOR), no infracción ambiental |
| `areas-protegidas` | `areas-protegidas-postgres-1` | 466 | No — lista áreas SERNANP, no a nivel de parcela |
| `actividad-agraria` | `actividad-agraria-postgres-1` | **0 (sin esquema)** | No — la tabla no existe; requiere migración + ingesta |

⚠ **Las cuatro apps estaban en `Exited (255)` desde hace 2 días.** El volumen persiste pero el contenedor no. Se resuelven con `docker compose up -d` en `appsperu\apps\<app>\api`. Ninguna modificó datos: solo se levantó PostgreSQL y se hizo una staging table temporal, ya eliminada.

**`actividad-agraria` está vacía de hecho:** el esquema tiene las credenciales correctas (`POSTGRES_USER=agraria`) pero **no existe ninguna tabla**, ni siquiera `schema_migrations`. Corre `npm run migrate` + `npm run ingest` en esa app antes de citarla.

**Hallazgo nuevo — `infracciones-ambientales` (OEFA):** es la **única** fuente del catálogo que permite un cruce negativo real, porque trae `nombre_administrado` (persona jurídica) y `subsector_economico`.

- Perfil: 14.724 expedientes OEFA, **corte 2024-04-30**, rango 2009-05-12 a 2023-06-12.
- Por subsector: Hidrocarburos 4.816 · Minería 2.325 · Industria 2.324 · *(sin clasificar) 2.083* · Pesquería 1.267 · Electricidad 993 · Residuos Sólidos 491 · **Agricultura 364** · Consultoras ambientales 61.
- Cruce contra las 54 cooperativas café/cacao depuradas: **0 coincidencias por normalización de nombre exacta.**
- **Un solo registro del universo aparece:** `CENTRAL DE COOPERATIVAS AGRARIAS CAFETALERAS COCLA LTDA. N° 281` — RD N° 1878-2019-OEFA/DFAI, Callao, 2016-03-07, tipo *"No contar con IGA"* (no contar con Instrumento de Gestión Ambiental), multa **S/ 0**, detalle: *"El administrado realizó el cierre de sus actividades sin contar con un Plan de Cierre aprobado por la DGAA"*.
- Otras dos registraciones agrícolas corresponden a asociaciones, no a nuestro universo: Central Unitaria de Asociaciones Agrarias de Villa Rica (Pasco, RD 0696-2023-OEFA/DFAI, S/ 9.34 + S/ 2.74, 2021) y un tercero.
- Perfil de las 364 infracciones agrícolas: Residuos Sólidos 133 · Eficacia de la fiscalización 45 · Monitoreos ambientales 39 · **No contar con IGA 32** · Incumplimientos formales 27.

⚠ **Límite duro que invalida el uso operativo de este dato:** el corte es **2024-04-30**, es decir, **no cubre 2024–2026**, que es exactamente la ventana en la que la presión EUDR se vuelve exigible. Serviría como línea de base histórica, no como verificación actual.

⚠ **Sobre COCLA:** el registro existe y es real, pero es de 2016, con multa cero, por un motivo formal (cierre sin plan aprobado, en Callao), y **no es una infracción de deforestación**. No debe presentarse como evidencia de riesgo ambiental EUDR. Si se menciona en el paper, debe ir con esas tres salvedades explícitas.

**Conclusión de la búsqueda de endpoint:** el hueco del Anexo VII **no tiene sustituto** en el catálogo de 38 apps. La evidencia negativa de OEFA confirma que las cooperativas no están masivamente sancionadas, pero no resuelve el problema de fondo: para una parcela de café o cacao sigue sin existir fuente pública de legalidad ambiental. **§2.5 se mantiene sin cambio y §8.10 se refuerza con evidencia medida, no con inferencia.**

### 8.11 Riesgos estructurales con cita textual

| Riesgo | Fuente textual | Impacto |
|---|---|---|
| Transferencia de costos al agricultor | Presidente del Comité Café-Cacao de ADEX: *"trasladar los costos al agricultor con precios bajos sería criminal"* | Exclusión de pequeños productores |
| Margen insuficiente | Margen del cacao <8–9 soles = abandono del cultivo | Desincentivo de permanencia |
| Solo 30% de asociados | Solidaridad: 300.000 familias de café/cacao, **70% sin organización formal** | Brecha de trazabilidad masiva |
| Calidad satelital | CamCafé: *"deficiencias en calidad de datos satelitales"* | Falsos positivos/negativos EUDR |
| Concentración exportadora | Top 4 de cacao = 52% del FOB; top 1 de café = 11,6% | Riesgo sistémico si falla un gran exportador |
| Dependencia de la UE | Café: UE = 44% del volumen · Cacao: UE = 41,3% | Concentración de destino |

### 8.12 Cifras de exportación (conservar ambas versiones)

⚠ **Conflicto de fuentes sin resolver** — anotado en §5 y a resolver antes de citar en cualquier documento:

| Indicador | Valor A | Valor B | Nota |
|---|---|---|---|
| Exportaciones de café 2025 | **US$ 1.672 M FOB** | **US$ 1.796 M FOB** | Discrepancia de ~7%. Verificar contra ADEX/PromPerú antes de usar |
| Exportaciones de cacao 2025 | US$ 1.591 M FOB (+27,5%), 173,7 mil TM | — | Coherente |
| Total café + cacao | US$ 3.386 M | | Suma de los valores A |
| Destino UE | Café 44% del volumen (1,78 M sacos, 20 países) | Cacao 41,3% (US$ 657,8 M) | Alemania y Bélgica concentran el café; Países Bajos es el hub del cacao |
| Precio del cacao | US$ 7,80/kg (2025) | US$ 338/qq café (2025, récord) | Ventana de rentabilidad para invertir |

⚠ **El total de US$3.386 M depende del valor A (1.672).** Si el café fue 1.796, el total sería ~3.510 M. No publicar el total sin fijar antes la cifra de café.

### 8.13 Mapeo documental del proyecto

| Documento interno | Contenido | Estado |
|---|---|---|
| `docs/FUNDAMENTOS_UNIVERSO_ENCUESTABLE.md` | Fundamenta las 245 organizaciones; 177 con GPS/contacto; 56 exportadoras; +83 no exportadoras = 328 | Base del universo |
| `EUDR/Herramientas de Diagnostico EUDR - Cooperativas.md` | Definición de las dimensiones D1–D11 y campos requeridos | ⚠ Ver nota de numeración abajo |
| `eda_output/EDA_EUDR_hallazgos.md` | EDA de cooperativas y avances EUDR |-supporto de §2.6 |
| `Directorio Cooperativas Cafe-Cacao Peru.xlsx` | Directorio de cooperativas | Fuente local |
| `data/backup/sunat_todos_exportadores.csv` | 126 exportadores café/cacao 2010–2025 | Base de §2.5 y §3.2 |

⚠ **⚠ SUSTITUIDO (2026-10-02). Este apartado estaba equivocado y se corrige a continuación.**

**Lo que este apartado afirmaba (incorrecto):** que existía un conflicto de numeración D1–D11 entre los instrumentos y una "primera versión" del diagnóstico.

**Lo que es cierto, verificado el 2026-10-02:**

1. **No hay conflicto entre los instrumentos.** `Instrumento 1 - Marco de Dimensiones de Diagnostico.md` y `Instrumento 2 - Encuesta Cuantitativa.md` usan una numeración D1–D11 consistente entre sí, e idéntica a la de §2.6 de esta memoria:

   | Dim. | Nombre en los instrumentos y en §2.6 |
   |---|---|
   | D1 | Clasificación regulatoria |
   | D2 | Trazabilidad y geolocalización |
   | D3 | Legalidad de la producción |
   | D4 | Riesgo de deforestación |
   | D5 | Sistema interno de diligencia debida |
   | D6 | Capacidad organizacional y digital |
   | D7 | Cadena de valor |
   | D8 | Gobernanza interna y apropiación de los socios |
   | D9 | Sostenibilidad económica del cumplimiento |
   | D10 | Confusión certificación voluntaria / EUDR |
   | D11 | Ecosistema de apoyo externo |

2. **La numeración antigua proviene de un informe preliminar descartado**, no del paquete de instrumentos. No hay ningún archivo vigente que la use.

**Causa del error:** afirmé el conflicto sin verificar los instrumentos. Fue una inferencia no verificada, presentada como hallazgo. No se modificó ningún instrumento por este punto, y no hace falta hacerlo.

**Lo que sí queda pendiente, y es distinto:** el Instrumento 7 está en `ISCAM\`, no en `Instrumentos\`, pese a que nueve archivos del paquete lo referencian desde `Instrumentos\`. Quien abra el directorio de instrumentos no encontrará el documento que justifica D10, D11 y la batería ambiental complementaria.
