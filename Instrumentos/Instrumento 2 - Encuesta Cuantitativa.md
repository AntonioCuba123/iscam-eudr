# Instrumento 2 — Encuesta Cuantitativa (D1–D15 + Performance)

**Serie:** parte del paquete de 7 instrumentos. Ver `Instrumento 1 - Marco de Dimensiones de Diagnostico.md` para la justificación de cada dimensión, y `Ficha Tecnica y Guia de Aplicacion - Instrumento 2.md` para la ficha técnica, la guía metodológica resumida y la guía de llenado (quién responde cada bloque). Aplicable en Google Forms (canal elegido para el relevamiento real; respuestas a Google Sheets), o en el panel digital "Brújula de Diligencia", que ya implementa las 11 dimensiones descritas en este documento.

**Fuente incorporada (2026-09-17):** Manual de Debida Diligencia en Deforestación — Pasos para su implementación en cadenas exportadoras de café y cacao (PROMPERÚ, financiado por BID, setiembre 2025, basado en el Manual OCDE-FAO y en el piloto 2024 con 17 organizaciones cafetaleras/cacaoteras peruanas). Contrastado pregunta por pregunta contra D1–D11; brechas cerradas en D3 (14e tributario/aduanero/comercial, 14f anticorrupción — 2 de las 7 categorías de legalidad EUDR que faltaban; 14g CLPI se agregó solo como verificación de bajo costo, no promedia — el *Documento orientador ADEX/MIDAGRI/EFI* ya determinó que no es un requisito legal pertinente a nivel nacional para café/cacao peruano) y D5 (18a política de deforestación formal, 18b priorización de riesgos, 19a componentes del plan de gestión, 21a frecuencia de revisión, 21b reporte de debida diligencia con KPIs — los 5 pasos del manual, antes solo parcialmente cubiertos).

**Actualización 2026-10-09 — ajuste de cobertura Pacto Verde completo (café y cacao sin sesgo):**
- **D7:** nueva pregunta 28b sobre presión CSDDD del comprador
- **D12:** Q40 reformulada producto-neutral (café y cacao); eliminado sesgo CalCafé-only
- **D13:** nueva Q44b como escala de entrada (nivel 0→1 adaptado a cooperativas)
- **D15 (nueva):** Gestión fitosanitaria y LMR — módulo Pacto Verde vi, Estrategia Farm to Fork (5 preguntas, Q56–Q60; aplica igual a café y cacao)
- **Bloque P:** P13 (exigencias Pacto Verde del comprador) y P14 (acceso a financiamiento verde) — variables de resultado Pacto Verde ampliado
- **ISA-PactoVerde:** ahora 4 módulos (i/iv/v/vi) = (D12 + D13 + D14 + D15) / 4
- **Total preguntas:** 89 (antes 80)

**Estado del Bloque P (Performance):** **v0.2** — actualizado 2026-10-09. Los indicadores P1–P12 se mantienen de v0.1; P13 y P14 son nuevos. Pendiente validación con el equipo del proyecto madre (Checklist, Tarea D1) antes del levantamiento de 100–150 organizaciones. El resto del instrumento (D1–D15) es versión vigente para piloto.

**Escala de madurez (preguntas 0–4):**
> **0** No existe / No sabe · **1** Informal o parcial · **2** En desarrollo · **3** Implementado · **4** Implementado y verificado/auditado

---

## Bloque 0 — Ficha de identificación (no puntúa)

- Nombre de la cooperativa / razón social
- **RUC** — clave de deduplicación entre fuentes del marco muestral (ver `Directorio Cooperativas Cafe-Cacao Peru (v3 - Cepicafe-Norandino).xlsx`, donde una misma organización aparece bajo distinto nombre comercial en JNC/APPCACAO/Central Café y Cacao; el RUC es lo único que identifica sin ambigüedad)
- Producto(s) exportado(s) (café, cacao, madera, otro — código SA si se conoce)
- N.º de socios productores / hectáreas totales asociadas
- ¿Exporta directamente a la UE o a través de un tercero?
- Si es indirecto: ¿quién es el comprador que sí exporta a la UE?
- Volumen anual aproximado destinado a la UE (% del total)
- País(es) de destino dentro de la UE
- Certificaciones voluntarias vigentes (Rainforest Alliance / Fairtrade / Orgánico / UTZ / Otra / Ninguna) — **insumo directo para D10**
- **(nuevo, 2026-09-16 — insumo IV3, Índice de Vulnerabilidad)** Dispersión geográfica de los socios: ¿las parcelas de los socios están concentradas en un solo distrito, repartidas en varios distritos de una misma provincia, o dispersas en varias provincias/regiones? (Un solo distrito / Varios distritos, misma provincia / Varias provincias o regiones)
- **(nuevo, 2026-09-16 — insumo IV3)** Distancia aproximada entre las parcelas más alejadas de los socios y el centro de acopio o planta de procesamiento más cercano (Menos de 5 km / Entre 5 y 20 km / Entre 20 y 50 km / Más de 50 km / No se ha medido) — junto con la pregunta anterior, aproxima la fragilidad territorial (mayor dispersión y distancia = mayor dificultad de supervisión, geolocalización y control de origen)
- **(nuevo, 2026-09-16 — insumo IV5, hallazgo de la evaluación de preparación EUDR de Vietnam, Team Europe Initiative 2025)** % de mujeres en la directiva/consejo directivo — variable de contexto (no entra al puntaje D1–D9, decisión ya justificada en Instrumento 7); se usa exclusivamente como proxy de riesgo de exclusión por baja representación dentro del Índice de Vulnerabilidad (IV5)

---

## Bloque P — Variables de Performance *(ver versión actualizada v0.2 al final del documento — 2026-10-09)*

> **Nota:** este bloque fue reubicado al final del instrumento (después de D15) como parte de la actualización 2026-10-09. La versión activa con P1–P14 está en la sección "Bloque P — Variables de Performance v0.2" al final. Lo que sigue a continuación corresponde a la versión v0.1 archivada para trazabilidad del historial de cambios.

**Por qué existe este bloque:** el ISA (D1–D9) mide qué tan preparada está la cooperativa — es el predictor. El proyecto madre pide además medir el **impacto** de esa preparación en resultados de negocio. Estas preguntas recogen ese resultado en el mismo instrumento, para poder cruzarlas después contra el ISA de la misma organización.

**Limitación de diseño que debe quedar explícita en cualquier reporte:** el levantamiento es transversal (un solo corte). Las preguntas P2, P5 y P7 son **retrospectivas por autodeclaración** (piden recordar una cifra de hace 3 años), no datos de panel verificados — sirven para aproximar una tendencia, no para un análisis causal riguroso. Tratar cualquier correlación ISA↔performance resultante como asociación, nunca como prueba de causalidad.

- P1. Volumen exportado a la Unión Europea en el último año (kg o toneladas, especificar unidad y producto si exporta ambos)
- P1b. **(nuevo, 2026-09-16 — insumo IV1, Índice de Vulnerabilidad)** Volumen TOTAL exportado a todos los destinos (UE y no UE) en el último año, mismo producto y misma unidad que P1 (kg o toneladas) — permite calcular `% dependencia del mercado europeo = P1 / P1b` con un dato duro y del mismo período, en vez de la estimación aproximada de Bloque 0 ("Volumen anual aproximado destinado a la UE, % del total"). Bloque 0 se mantiene como estimación rápida de identificación; P1/P1b es el dato preciso para el índice.
- P2. Volumen exportado a la Unión Europea hace 3 años, mismo producto (kg o toneladas) — *retrospectivo, ver limitación arriba*
- P3. Ingreso total generado por ventas de exportación a la UE en el último año (S/ o USD, especificar moneda)
- P4. N.º de compradores/clientes europeos activos actualmente
- P5. N.º de compradores/clientes europeos activos hace 3 años — *retrospectivo*
- P6. Precio promedio pagado al socio productor por kg/quintal en el último año (S/ o USD) — **conecta directamente con D9.35** (riesgo de que el costo de adecuación se traslade a un menor precio pagado al socio)
- P7. Precio promedio pagado al socio productor por kg/quintal hace 3 años — *retrospectivo*
- P8. ¿Ha tenido algún lote rechazado u observado por un comprador europeo por motivos de trazabilidad/deforestación en los últimos 2 años? (Sí / No / No sabe)
- P9. Si la respuesta anterior es "Sí": N.º aproximado de lotes rechazados u observados
- P10. ¿Ha perdido algún contrato o comprador europeo en los últimos 2 años por motivos de cumplimiento (EUDR u otro requisito de sostenibilidad del comprador)? (Sí / No / No sabe)
- P11. **(nuevo, 2026-09-17 — criterio de validación externa ISCAM)** % del volumen total exportado en el último año que cuenta con trazabilidad completa verificada hasta la parcela de origen (0–100%) — distinto de D2, que mide si *existe* el sistema de trazabilidad, no qué fracción del volumen efectivamente lo usa. Cierra el vacío de "% volumen trazable" identificado en `Comparativa - ISA D1-D11 vs IP-IV-RE ISCAM.md` §3.3. No promedia dentro de ninguna dimensión — es criterio de validación externa, se correlaciona contra IP/RE una vez calculados, no es insumo de su fórmula.
- P12. **(nuevo, 2026-09-17 — criterio de validación externa ISCAM)** N.º de años consecutivos exportando a la Unión Europea, contando el año actual — cierra el vacío de "continuidad exportadora" (mismo §3.3). No promedia dentro de ninguna dimensión, mismo tratamiento que P11.

**Indicadores derivados a calcular en el análisis (no preguntas nuevas):**
- Variación de volumen exportado UE = (P1 − P2) / P2
- Variación de N.º de compradores europeos = P4 − P5
- Variación del precio pagado al socio = (P6 − P7) / P7 — cruzar con P6/P7 nominal si se quiere deflactar por inflación en el análisis, no en el levantamiento
- Tasa de incidencia de rechazo = P9 / (lotes totales exportados en el periodo, si se levanta ese dato aparte)

---

## D1 — Clasificación regulatoria
1. ¿La cooperativa introduce el producto directamente en el mercado de la UE bajo su propio nombre? (Sí/No)
2. ¿Transforma el producto (trilla, tostado, fermentado, aserrío) antes de venderlo? (Transforma/No transforma)
3. ¿Sabe con certeza qué rol le corresponde (operador, operador posterior, comerciante, micro/pequeño operador primario)? (Sí con certeza / Idea aproximada / No sabe)
4. ¿Cumple los umbrales de microempresa/pequeña empresa (Directiva 2013/34/UE)? (Sí/No/No sabe)

## D2 — Trazabilidad y geolocalización
5. ¿Existe registro de geolocalización (GPS/polígono) por parcela de socio? (0–4)
6. % de socios con parcela geolocalizada
7. ¿El sistema vincula un lote exportado con la(s) parcela(s) específica(s)? (0–4)
8. ¿Quién levantó la información? (técnico propio / consultor / proyecto de cooperación / socio por su cuenta / no se ha levantado)
9. Frecuencia de actualización (nunca / al ingreso del socio / anual / por cosecha)
10. **(nuevo)** ¿Existe algún punto en el proceso de acopio o beneficio donde se mezclan físicamente lotes de distinto origen sin registro de qué parcelas los componen? (Sí, se mezclan sin control / Se mezclan pero con registro de origen / No, se mantiene segregación física completa) — una respuesta "se mezclan sin control" **anula** en la práctica cualquier puntaje alto obtenido en las preguntas 5–7; señalarlo como bandera roja independiente del promedio de D2.

## D3 — Legalidad de la producción
11. % de socios con título de propiedad o posesión reconocida legalmente
12. ¿Hay parcelas superpuestas a áreas protegidas, reservas comunales o territorios indígenas sin sanear? (Sí extensa / Sí puntual / No verificado / No, ninguna)
13. ¿Se verifica cumplimiento laboral (no trabajo infantil, seguridad social) a nivel de finca? (0–4)
14. **(nuevo)** ¿Alguna parcela de socios se ubica en una zona de desarrollo alternativo (ex-cultivo de coca) o con antecedentes de conflicto social/territorial? (Sí / No / No verificado) — no es un criterio del reglamento europeo, pero cambia la naturaleza de la brecha: de "falta de gestión" a "problema estructural que excede a la cooperativa" (ver Instrumento 7).
14a. **(nuevo)** ¿Los socios cuentan con autorización de uso de agua para su actividad productiva, cuando corresponde? (Sí, todas las fuentes verificadas / Parcialmente / No / No aplica)
14b. **(nuevo, 2026-10-01 — reetiquetada por límite de verificabilidad)** ¿El tratamiento de aguas residuales del beneficio/procesamiento cumple con lo exigido por la autoridad ambiental? (Siempre / A veces / No / No aplica) — **pregunta autodeclarada: el cumplimiento se afirma, no se verifica.** No existe fuente pública contra la cual contrastar la respuesta (ver nota de advertencia inmediatamente debajo). Mantener en el instrumento: sí aporta señal de cultura de cumplimiento, pero **su puntaje no debe interpretarse como evidencia de conformidad ambiental.**
14c. **(nuevo, 2026-09-16 — Documento orientador ADEX/MIDAGRI/EFI)** ¿Alguna parcela de socios se encuentra dentro de la faja marginal de un río, quebrada, lago o laguna? (Sí / No / No sabe) — las fajas marginales son intangibles y de dominio público; producir dentro de ellas es un incumplimiento de legalidad ambiental, no una zona gris. Verificable de forma independiente con el mapa de fajas marginales de datosabiertos.gob.pe.
14d. **(nuevo, 2026-10-02 — Art. 2(40)(d), derechos de terceros; cierra la brecha que hasta 2026-10-01 estaba abierta)** En las parcelas de los socios y en el inmueble donde opera la cooperativa, ¿existe algún derecho de terceros —carga, embargo, servidumbre, usufructo, arrendamiento o derecho de uso consuetudinario— que condicione o restrinja el uso de la tierra para cultivar café o cacao, o el derecho de la cooperativa a operar en esa finca? (No existe ningún derecho de terceros / Existe, pero está registrado y no restringe el uso / Existe un acuerdo documentado con el titular o con la autoridad que legitima el uso, aunque la cooperativa o el socio no tenga título formal / Existe usufructo, arrendamiento o carga sin acuerdo que lo resuelva / Se han invocado derechos de uso tradicional o consuetudinarios por una comunidad o pueblo indígena sin proceso de acuerdo / No verificado) — **promedia dentro de D3, escala 4→0 en el orden en que aparecen las opciones.**
> **Por qué esta pregunta y no una más genérica (2026-10-02).** La letra (d) del Art. 2(40) define los derechos de terceros como los *"derechos de uso y tenencia afectados por la producción, incluidos los derechos de uso tradicional de pueblos indígenas y comunidades locales"*, y la guía de la Comisión (C(2024) 7027, §6) la desarrolla con **cargas, usufructo y acuerdos constructivos con el Estado**. La pregunta se diseñó contra esa definición, **no por analogía con la Tabla 6** del manual PROMPERÚ/BID — la Tabla 6 no tiene fila para (d), y por eso las 7 filas pueden estar cubiertas mientras la letra (d) sigue sin cubrirse.
>
> **Cómo se distingue de las otras tres preguntas que se le parecen.** La 12 pregunta por *superposición espacial* con áreas protegidas o territorios indígenas; la 14g pregunta por el *proceso* de consentimiento cuando esa superposición existe. Esta 14d pregunta por el *título que weighs sobre la tierra*, con independencia de si hay superposición: una parcela en zona no protegida puede tener usufructo de un tercero, y una parcela con servidumbre registral puede no tener conflicto espacial alguno. Un mismo caso puede activar las tres, y eso es correcto: son failing distintos.
>
> **"Acuerdo documentado" como categoría propia, y por qué.** La guía de la Comisión admite los *acuerdos constructivos* con el Estado: una tenencia legítima sin título formal puede ser válida si está documentada. Por eso "acuerdo documentado sin título formal" puntúa 2 y no 0. No es unaleben permisiva: es el criterio del regulador.
>
> **Cómo se trata "No verificado".** Se computa como **0** en el promedio, porque bajo el EUDR la carga de la prueba recae sobre el operador: lo no acreditado se trata como no acreditado. Pero **además se reporta aparte el porcentaje de respuestas "No verificado"**, para que un cero por falta de información no se confunda con un cero por incumplimiento real. Es el mismo tratamiento que la 15 de D4.
>
> **Numeración.** El hueco 14d que existía desde el 2026-10-01 queda **ocupado por esta pregunta**, no renumerado. 14e–14g conservan su número, y las referencias cruzadas de la `Matriz de Cobertura Tecnica`, del `Dossier Completo` y de `Scripts\matriz_data.py` siguen válidas sin cambiar.
>
> **Mapeo verificado contra el PDF descargado del manual (37 págs., Tabla 6 en la pág. 23), no contra una paráfrasis.** Nota de lectura: la Tabla 6 tiene 7 filas y **ninguna fila es la letra (d)** del reglamento — esa es exactamente la razón por la que "las 7 filas están cubiertas" y "las 8 letras están cubiertas" son afirmaciones distintas.
>
> | Fila Tabla 6 | Categoría | Pregunta que la cubre |
> |---|---|---|
> | 1 | Tenencia de la tierra y uso de suelo | 11 y 12 |
> | 2 | Permisos ambientales y cumplimiento forestal | 14a, 14b, 14c |
> | 3 | Normas laborales | 13 |
> | 4 | Consentimiento libre, previo e informado (CLPI) | 14g (verificación, no promedia) |
> | 5 | Cumplimiento de la normativa tributaria y aduanera | 14e |
> | 6 | Cumplimiento de la normativa comercial | 14e |
> | 7 | Medidas anticorrupción | 14f |
>
> **Corrección de conteo (2026-10-01):** la nota de alcance que aparece después de 14f decía "5 de las 7 categorías". El número correcto es **7 de 7 filas de la Tabla 6**, con la fila 4 (CLPI) cubierta por 14g y las filas 5 y 6 cubiertas por una sola pregunta (14e).
>
> **Distinción que hay que mantener:** la Tabla 6 (7 filas) y el Art. 2(40) del Reglamento (UE) 2023/1115 (8 letras, (a)–(h)) **no son el mismo universo** y sus conteos no deben mezclarse. El reglamento desglosa en ocho categorías; el manual PROMPERÚ/BID las agrupa en siete filas. Clic de las 8 letras del reglamento a las 7 filas del manual:
>
> | Art. 2(40) | Categoría (reglamento) | Fila Tabla 6 (manual) | Pregunta |
> |---|---|---|---|
> | (a) | Derechos de uso del suelo | 1 — Tenencia de la tierra y uso de suelo | 11, 12 |
> | (b) | Protección ambiental | 2 — Permisos ambientales y cumplimiento forestal | 14a, 14b, 14c |
> | (c) | Reglas forestales, incluida gestión forestal y conservación de biodiversidad, **cuando estén directamente relacionadas con la cosecha de madera** | *(sin fila propia — ver nota de no aplicabilidad abajo)* | No aplica a café/cacao |
> | (d) | Derechos de terceros | *(sin fila propia en la Tabla 6)* | **14d** (desde 2026-10-02) |
> | (e) | Derechos laborales | 3 — Normas laborales | 13 |
> | (f) | Derechos humanos protegidos por el derecho internacional | 3 y 4 (parcial) | 13, 14g (parcial) |
> | (g) | Principio del consentimiento libre, previo e informado | 4 — CLPI | 14g |
> | (h) | Normativa tributaria, anticorrupción, comercial y aduanera | 5, 6 y 7 | 14e, 14f |
>
> **No aplicabilidad de la letra (c).** La regla forestal solo es legislación pertinente cuando se relaciona directamente con la cosecha de madera. El café y el cacao no son productos madereros, de modo que (c) no genera obligación para este toolkit. **Esto es una decisión de alcance documentada, no una omisión:** si el proyecto adiciona productos madereros, hay que reabrirla.
>
> **La letra (d) — derechos de terceros: cerrada el 2026-10-02.** Hasta esa fecha ninguna pregunta la abordaba de forma directa y solo la cubría parcialmente y oblicuamente la 12, que es un subconjunto (superposición espacial). La pregunta **14d** se diseñó contra la definición del Art. 2(40)(d) y el desarrollo de la guía de la Comisión (C(2024) 7027, §6) — cargas, usufructo, acuerdos constructivos con el Estado —, no por analogía con la Tabla 6. Con esto, **las 8 letras del reglamento tienen cobertura directa**: (a) 11 y 12, (b) 14a/14b/14c, (c) no aplicable, (d) 14d, (e) 13, (f) 13 parcialmente, (g) 14g, (h) 14e y 14f. Ya no queda ninguna letra abierta por decisión de diseño.
>
> **Lo que sigue sin cubrirse, y es distinto:** la 14d **autodeclara** el estado de los derechos de terceros. No hay fuente pública contra la cual verificarla, porque el registro de cargas, usufructos y derechos consuetudinarios no es de acceso abierto en el Perú. Esto no la degrada a la categoría de 14a/14b: aquellas no admiten ni contraste parcial, mientras que la 14d admite contraste documental limitado y el RUC del socio permite cruzar con SUNAT y con el Registro Catastral. Pero **su puntaje se lee como percepción declarada, igual que el resto de D3** (ver la advertencia de verificabilidad más abajo).
>
> **Fuente primaria de esta nota:** *Manual de debida diligencia en deforestación. Pasos para su implementación en cadenas exportadoras de café y cacao*, PROMPERÚ/BID, setiembre 2025, 37 págs. — Tabla 6 en la pág. 23 ("Categorías de legalidad consideradas por el EUDR"). Copia pública verificada: `culturasostenible.pe/archivos/galeria-caminosostenibilidad/MANUAL DE DEBIDA DILIGENCIA EN DEFORESTACION.pdf`. Art. 2(40) verificado contra la *Guidance on the application of the EUDR* de la Comisión Europea, C(2024) 7027, §6 "Legality", que reproduce las letras (a)–(h) y confirma que el desglose del reglamento tiene ocho, no siete.

14e. **(nuevo, 2026-09-17 — Manual de Debida Diligencia en Deforestación, PROMPERÚ/BID 2025)** ¿La cooperativa y sus socios están al día en sus obligaciones tributarias, aduaneras y comerciales vinculadas a la actividad exportadora? (Sí, verificado / Parcialmente / No verificado / No sabe)
14f. **(nuevo, 2026-09-17 — mismo manual)** ¿Existen políticas o mecanismos internos contra la corrupción (código de conducta, canal de denuncias) aplicables a la cadena de abastecimiento? (Sí, formalizado / Informal / No existe)
> **Alcance de D3 en legalidad (corregido 2026-10-01, ampliado 2026-10-02):** las preguntas 11-13, 14a, 14b, 14c, **14d**, 14e, 14f y 14g cubren **las 7 filas de la Tabla 6 y las 8 letras del Art. 2(40)** (tablas de mapeo en la nota 14d, mas arriba; la letra (c) se declara no aplicable y la (d) la cubre 14d desde el 2026-10-02). 14a, 14b, 14c, **14d**, 14e y 14f si promedian dentro de D3; 14g es verificacion y no promedia; 11, 12 y 13 promedian. La version anterior de esta nota decia "5 de las 7 categorias" y era incorrecta. **No confundir con el resto de la bateria ambiental operativa** (pesticidas, fertilizantes, combustible, huella de carbono/GEI) - esa bateria fue evaluada y quedo explicitamente fuera del puntaje EUDR; ver el caso "Huella de carbono, gestion de emisiones GEI y bateria ambiental operativa" en el Instrumento 7 y el detalle pregunta por pregunta en `Puente - Mapeo Encuesta Productor a Dimensiones D1-D11.md`.
14g. **(nuevo, 2026-09-17 — verificación, no promedia)** Cuando corresponde (parcelas de socios en territorio de comunidades indígenas, nativas o campesinas), ¿se ha realizado un proceso de Consentimiento Libre, Previo e Informado (CLPI)? (Sí, proceso documentado / Aplica pero no se ha realizado / No aplica, no hay territorios de este tipo / No sabe) — **pregunta de verificación, no promedia dentro de D3.** El *Documento orientador ADEX/MIDAGRI/MINCETUR/GIZ/EFI* (2026, con respaldo de la Resolución Ministerial N.º 0128-2025-MIDAGRI) ya evaluó esta categoría a nivel nacional para café/cacao peruano y concluyó que "no se ha identificado ningún requisito legal pertinente" (ver Instrumento 7, §6) — esa es la línea base oficial del sector, y no se revierte aquí. Se conserva únicamente como chequeo de bajo costo para el caso particular no cubierto por un análisis agregado nacional: una cooperativa cuyos socios sí tengan parcelas superpuestas a territorio de una comunidad indígena, nativa o campesina específica (ver pregunta 12).

> ⚠ **Advertencia de verificabilidad — leer antes de puntuar D3 (añadida 2026-10-01)**
>
> Las preguntas **14a, 14b y 14d** son **autodeclaradas y sin fuente de verificación pública completa**. No es una limitación del instrumento sino del Estado Peruano, y está medida:
>
> - La autorización ambiental del sector agrario la emite **MIDAGRI** bajo su reglamento sectorial (DS 006-2024-MIDAGRI, en proceso de modificación por la RM D000325-2026-MIDAGRI-DM). **Ese registro no está publicado como datos abiertos.** No existe endpoint público de evaluaciones ambientales del sector agrario.
> - Verificado sobre las **38 apps** del catálogo público de datos del Estado: ninguna cubre la legalidad ambiental agraria a nivel de parcela.
> - La única fuente con posibilidad de cruce negativo (`infracciones_ambientales`, OEFA, 14.724 expedientes) tiene **corte 2024-04-30** y cubre sanciones, no autorizaciones. **No sirve para verificar conformidad.**
> - Contraste: **14c sí es verificable externamente** con el mapa de fajas marginales de datosabiertos.gob.pe, y 12 admite contraste con áreas protegidas. La **14d admite contraste documental parcial** (SUNAT para Identify al socio, Registro Catastral para cargas y usufructos) pero no tiene fuente abierta masiva, y su "No verificado" se computa como 0 por la carga de la prueba que el reglamento impone al operador.
>
> **Cómo leer el puntaje de D3 en consecuencia:** el índice agregado de D3 debe reportarse siempre como **percepción de cumplimiento declarada por la cooperativa**, nunca como conformidad verificada. Un puntaje alto en 14a/14b significa que la cooperativa *afirma* cumplir, lo que es información válida sobre su cultura de gestión y sobre su exposición a riesgo — no sobre el estado real de sus permisos.
>
> **Para una auditoría externa esto significa:** quien audite necesitará complementar con evidencia documental propia (copia de autorización, resolución, certificado de inspección de la autoridad). El instrumento orienta el diagnóstico; no sustituye el expediente.
>
> **Esta nota no reduce el puntaje de D3 ni retira la pregunta.** Reduce lo que el puntaje puede afirmar. Ref: `Memoria Diaria EUDR.md` §8.10.1 (medición del 2026-10-01).

## D4 — Riesgo de deforestación
15. ¿Se verificó cambio de uso de suelo posterior al 31 dic. 2020? (No verificado / Verificación parcial / Verificado sin hallazgos / Casos detectados sin resolver / Verificado sistemáticamente y documentado)
16. ¿Usa herramientas de monitoreo satelital (Global Forest Watch, plataformas nacionales)? (0–4)
17. ¿Conoce la clasificación de riesgo (bajo/estándar/alto) de su zona? (Sí documentado / Idea aproximada / No sabe)

## D5 — Sistema interno de diligencia debida
18. ¿Existe procedimiento escrito de diligencia debida? (0–4)
18a. **(nuevo, 2026-09-17 — Manual de Debida Diligencia en Deforestación, PROMPERÚ/BID 2025, Paso 1)** ¿Existe una política de deforestación formal y escrita (distinta del procedimiento operativo de la pregunta 18), con objetivos, metas medibles y plazos — ej. un compromiso de "cero deforestación" a una fecha determinada? (0–4)
18b. **(nuevo, 2026-09-17 — mismo manual, Paso 2.3)** ¿La cooperativa prioriza sus riesgos de deforestación con algún criterio de probabilidad e impacto (aunque sea informal), o los atiende sin un orden definido? (No se prioriza, se atiende lo que surge / Priorización informal, sin criterio escrito / Priorización estructurada con matriz probabilidad×impacto o similar)
19. ¿Ha elaborado o participado en una declaración de diligencia debida / simplificada? (No sabe qué es / No pero lo entiende / En proceso / Presentada y aceptada)
19a. **(nuevo, 2026-09-17 — mismo manual, Paso 3)** Del plan de gestión de riesgos de la cooperativa (si existe), marcar los componentes que incluye explícitamente: plazos definidos / recursos (humanos o financieros) asignados / responsables designados / procedimientos de consulta con socios y comunidades / sistema de seguimiento y monitoreo / protocolo ante incumplimiento de un socio / atención diferenciada a productoras mujeres — *(mapeo, no promedia; insumo para Instrumento 4, mismo criterio que D11)*
20. ¿Existe responsable designado para el cumplimiento EUDR? (No / Función adicional / Dedicado)
21. ¿Capacitación formal en los últimos 12 meses? (No / Hace más de 12 meses / Sí, reciente)
21a. **(nuevo, 2026-09-17 — mismo manual, Paso 4)** ¿El plan de gestión de riesgos se revisa con una frecuencia definida (ej. anual, por campaña)? (No hay revisión definida / Revisión reactiva, sin frecuencia fija / Revisión periódica definida)
21b. **(nuevo, 2026-09-17 — mismo manual, Paso 5)** ¿La cooperativa elabora y comunica un reporte de debida diligencia con indicadores (ej. % de producto trazado hasta finca, N.º de alertas tempranas detectadas, N.º de productores capacitados)? (No / Sí, uso interno solamente / Sí, interno y compartido con compradores u otras partes interesadas)
> D5 ahora refleja los 5 pasos completos del manual PROMPERÚ/BID (política → identificar/priorizar riesgos → plan de prevención/mitigación → monitoreo → comunicación). 19a es mapeo y no promedia; el resto de la dimensión (18, 18a, 18b, 19, 20, 21, 21a, 21b) sí entra al promedio de D5.

## D6 — Capacidad organizacional y digital
22. Presupuesto asignado para cumplimiento EUDR (No / Parcial / Sí)
23. Digitalización de registros (Papel / Mixto / Digital)
24. Conectividad a internet (No hay / Limitada / Confiable)
25. ¿Ha gestionado apoyo externo para adecuarse? (No y lo necesita / No lo cree necesario / Sí en el pasado / Sí activo)

## D7 — Cadena de valor
26. ¿El comprador ha exigido formalmente geolocalización/diligencia debida? (Aún no / Informalmente / Formalmente por escrito)
27. ¿El comprador ofrece financiamiento/asistencia técnica condicionada al cumplimiento? (Sí/No)
28. Riesgo percibido de perder el contrato si no cumple a tiempo (No sabe / Bajo / Medio / Alto) — **indicador de urgencia, no de madurez**; no promediar junto con las demás preguntas de D7.
28b. **(nuevo, 2026-10-09 — CSDDD/presión regulatoria de la cadena)** ¿Algún comprador europeo le ha comunicado que sus propias obligaciones de diligencia debida bajo normativa europea (EUDR, CSRD, CSDDD u otra) implican requisitos adicionales sobre su cadena de suministro que van más allá de la geolocalización y la declaración de deforestación? (No ha mencionado nada / Lo ha mencionado verbalmente sin requisito formal / Sí, ha enviado documentación o cuestionario de proveedores / Sí, lo ha formalizado como cláusula contractual) — **promedia dentro de D7, escala 0→3 en el orden en que aparecen las opciones.** Captura la presión CSDDD que ya está trasladándose contractualmente desde los compradores; distingue cooperativas con compradores "adelantados" (que ya alinearon su propia CSRD/CSDDD con sus requisitos a proveedores) de aquellas cuyo comprador aún no se ha movido.

---

## D8 — Gobernanza interna y apropiación de los socios *(dimensión extendida)*
29. ¿Se han realizado asambleas o reuniones informativas sobre el EUDR dirigidas a los socios (no solo a la directiva)? (0–4)
30. % estimado de socios que entienden, al menos en términos generales, por qué se les pide geolocalización/documentación
31. ¿Existe algún mecanismo interno (incentivo o condición) para que los socios entreguen su información de parcela? (No existe / Se pide informalmente / Es requisito formal para vender a la cooperativa)
32. Rotación de la directiva en los últimos 2 años (Alta / Moderada / Baja/estable) — una rotación alta es un riesgo de continuidad del proceso de adecuación, independientemente de cuán bien esté documentado hoy.

## D9 — Sostenibilidad económica del cumplimiento *(dimensión extendida)*
33. Estimación del costo total de adecuación (geolocalización, saneamiento, sistemas, capacitación) frente al presupuesto anual de la cooperativa (Costo mayor al 10% del presupuesto anual / Entre 3–10% / Menor al 3% / No se ha estimado)
34. ¿La cooperativa ha financiado la adecuación con deuda? (Sí / No / No ha sido necesario)
35. ¿Existe riesgo de que el costo de adecuación se traslade a un menor precio pagado al socio productor? (Sí, ya ha ocurrido / Es un riesgo latente / No aplica / No se ha evaluado)

## D10 — Confusión entre certificación voluntaria y cumplimiento EUDR *(dimensión extendida — bandera de alerta, no promedio de madurez)*
36. ¿La cooperativa cree que su certificación vigente (Rainforest Alliance, Fairtrade, Orgánico, etc.) ya cubre las obligaciones del EUDR? (Sí, totalmente / Sí, en parte / No, sabe que son cosas distintas / No tiene certificación)
   — Una respuesta "Sí, totalmente" es una **bandera roja de percepción**, independientemente de cuán buena sea la certificación real: indica que la cooperativa puede no estar tomando acción propia porque cree (erróneamente) que ya está cubierta.
37. ¿Algún proveedor o consultor le ha ofrecido una "certificación EUDR" como producto? (Sí / No) — una respuesta "Sí" amerita advertencia: no existe tal certificación oficial.
36a. **(nuevo — no promedia, se reporta aparte)** ¿La organización ha recibido asesoría específica sobre el EUDR (a diferencia de asesoría genérica de sostenibilidad)? (Sí, asesoría especializada en EUDR / Solo asesoría genérica de sostenibilidad / No ha recibido asesoría / No sabe) — ítem de capacidad de D10: se captura y se codifica, pero no entra a ningún promedio.

## D11 — Ecosistema de apoyo externo *(dimensión extendida — mapeo, no promedio)*
38. Marcar los actores con los que la cooperativa ya tiene contacto o apoyo activo: SERFOR (legalidad forestal) / PNCB-MINAM (monitoreo satelital) / MIDAGRI o programa regional de café-cacao / Gobierno regional (catastro/saneamiento) / Cooperación internacional (GIZ, USAID, UE, ONG) / Junta Nacional del Café, APPCACAO u otro gremio / Ninguno
39. De los actores no marcados en la pregunta anterior, ¿cuáles conoce pero no ha contactado, y por qué?

---

## D12 — Huella de carbono y gestión de emisiones GEI *(dimensión extendida — módulo Pacto Verde i)*

**Contexto:** este módulo corresponde al pilar (i) del proyecto madre ISCAM ("huella de carbono"). El EUDR no exige inventario de GEI, pero el Pacto Verde Europeo (taxonomía, CSRD, CBAM) y los compradores europeos cada vez lo demandan. **Herramienta de referencia por producto:** para café, **CalCafé v2.1** (PromPerú/PUCP-PELCAN, ISO 14040/44, PEFCR) — calculadora validada y gratuita que cubre 8 categorías de impacto. Para cacao, no existe herramienta nacional validada equivalente — el encuestador debe registrar qué herramienta usa la cooperativa (herramienta del comprador, consultoría externa, COSA tool u otra) o si no usa ninguna. Este bloque mide si la cooperativa tiene capacidad de medir y reportar su huella, no el valor absoluto; las preguntas son válidas para ambos productos.

40. **(actualizado 2026-10-09 — producto-neutral)** ¿La cooperativa conoce alguna herramienta o metodología para calcular la huella de carbono de su producto de exportación? *(Para café: referencia CalCafé v2.1, PromPerú, gratuita. Para cacao: herramienta del comprador, consultoría externa, COSA tool u otra — anotar cuál si aplica.)* (No sabe qué es una huella de carbono / Conoce el concepto pero no ha identificado herramienta / Conoce una herramienta pero no la ha usado / La ha usado al menos una vez / La usa sistemáticamente)
41. ¿Cuenta con registros de insumos necesarios para calcular huella de carbono (fertilizantes por campaña, combustible en maquinaria/transporte, energía de procesamiento, distancia finca-acopio)? *(Aplica a café y cacao por igual.)* (No registra nada / Registra algún insumo / Registra la mayoría / Registra todo sistemáticamente)
42. ¿Ha calculado la huella de carbono de su café/cacao de exportación en los últimos 2 años? (No / Sí, estimación interna sin herramienta validada / Sí, con herramienta validada [especificar cuál] / Sí, verificada por tercero independiente)
43. ¿Tiene objetivo cuantificado de reducción de emisiones (ej. -X% al 2030)? (No / En definición / Sí, interno / Sí, público y con plan de acción)
44. ¿Reporta huella de carbono a compradores o plataformas (ej. CDP, plataforma del comprador)? (No / Solo si lo piden / Sí, regularmente)

> **Nota de alcance y tratamiento café/cacao:** la Q40 reformulada es producto-neutral — funciona igual para café y para cacao. En el análisis, cruzar D12 por producto principal para detectar la brecha estructural de herramientas entre café (CalCafé disponible) y cacao (sin equivalente nacional). No imputar ni ajustar el puntaje — la brecha debe aparecer en los datos, no ocultarse. Este bloque NO promedia en el ISA-EUDR (D1–D9) — es dimensión extendida del Pacto Verde, se reporta aparte y alimenta el módulo (i) del ISA-PactoVerde.

---

## D13 — Reporte de sostenibilidad y transparencia *(dimensión extendida — módulo Pacto Verde iv)*

**Contexto:** corresponde al pilar (iv) del proyecto madre ("reporte de sostenibilidad"). Alineado con CSRD/ESRS, taxonomía verde UE, y expectativas de compradores europeos. Mide capacidad de la cooperativa para producir información estructurada, verificable y comparable sobre su desempeño ambiental, social y de gobernanza (ESG), más allá de lo que exige estrictamente el EUDR.

44b. **(nuevo, 2026-10-09 — escala de entrada para el universo objetivo)** ¿La cooperativa elabora actualmente algún documento que recoja indicadores de su desempeño ambiental, social o de gestión, aunque sea para uso interno y sin seguir ningún estándar formal? (No existe ningún documento de este tipo / Sí, registros internos informales sin estructura / Sí, informe estructurado de uso interno / Sí, informe publicado o compartido con terceros) — **promedia dentro de D13 igual que Q45–Q50.** Provee el nivel 0→1 de la escala adaptado al contexto de una cooperativa agraria, donde la mayoría de las organizaciones no habrá llegado aún al umbral de un reporte formal según estándar reconocido. Sin esta pregunta, D13 produce efecto suelo masivo y no discrimina dentro del rango bajo de la muestra.
45. ¿Elabora algún reporte anual de sostenibilidad / memoria de responsabilidad social? (No / Interno, informal / Formal, interno / Público, según estándar reconocido ej. GRI, ESRS simplificado)
46. ¿El reporte incluye indicadores ambientales (deforestación, huella carbono, agua, biodiversidad, residuos)? (No / Parcial / Sí, básicos / Sí, completos y con metas)
47. ¿El reporte incluye indicadores sociales (trabajo infantil, trabajo forzoso, igualdad salarial, participación mujeres, salud ocupacional)? (No / Parcial / Sí, básicos / Sí, completos y con metas)
48. ¿El reporte incluye indicadores de gobernanza (estructura directiva, anticorrupción, gestión de riesgos, canal de denuncias)? (No / Parcial / Sí, básicos / Sí, completos)
49. ¿La información reportada es verificada/auditada por tercero independiente? (No / Auto-declarada / Verificación parcial / Auditoría completa externa)
50. ¿El reporte se comparte proactivamente con compradores europeos y partes interesadas? (No / Solo bajo solicitud / Sí, sistemáticamente)

> **Nota de alcance:** NO promedia en el ISA-EUDR (D1–D9). Es dimensión extendida del Pacto Verde. Una cooperativa puede tener alta madurez EUDR (D1–D9) y nulo reporte de sostenibilidad, y viceversa. Se correlaciona contra performance (Bloque P) y alimenta el módulo (iv) del ISA-PactoVerde. El promedio de D13 incluye Q44b + Q45–Q50 (7 preguntas).

---

## D14 — Economía circular, envases y gestión de residuos *(dimensión extendida — módulo Pacto Verde)*

**Contexto:** corresponde al pilar (v) del proyecto madre ("economía circular/envases"). Alineado con Plan de Acción de Economía Circular UE, Directiva de envases y residuos de envases (PPWR), y estrategia "De la granja a la mesa". El EUDR no regula el envase del producto terminado, pero el Pacto Verde sí impulsa circularidad en toda la cadena. Mide prácticas de la cooperativa en acopio, beneficio y empaque de exportación.

51. **Gestión de residuos del beneficio/acopio:** ¿Qué se hace con cáscara, mucílago, agua miel, residuos de trilla/despulpado? (Eliminación sin tratamiento / Compostaje parcial / Compostaje/biogás sistemático + reuso en fincas / Economía circular cerrada con subproductos valorizados)
52. **Envases de exportación (sacos, big-bags, contenedores):** ¿Son reutilizables, reciclables o compostables? (Ninguno / Parcialmente / Mayoría / Todos, con certificación/trazabilidad de retorno)
53. **Plásticos de un solo uso en la cadena (bolsas, film, flejes, etiquetas):** ¿Hay plan de reducción/eliminación? (No / En análisis / Sí, en implementación / Sí, cumplido y verificado)
54. **Subproductos valorizados:** ¿Se comercializa o transforma algún residuo (cáscara → biocombustible, mucílago → bioinsumos, agua tratada → riego)? (No / Piloto / Sí, escala parcial / Sí, escala comercial)
55. **Trazabilidad de envases y residuos:** ¿Existe registro de qué envases salen, cuáles retornan y qué residuos se generan por lote exportado? (No / Parcial / Sí, para envases / Sí, completo envases + residuos)

> **Nota de alcance:** NO promedia en el ISA-EUDR (D1–D9). Es dimensión extendida del Pacto Verde. El Reglamento (UE) 2023/1115 regula materias primas (Anexo I), no envases terminados — pero la normativa de envases (PPWR) y taxonomía sí afectan la competitividad. Se reporta aparte y alimenta el módulo (v) del ISA-PactoVerde.

---

## D15 — Gestión fitosanitaria y LMR *(dimensión extendida — módulo Pacto Verde vi, Estrategia Farm to Fork)*

**Contexto:** corresponde al pilar Farm to Fork del Pacto Verde Europeo (meta de reducción del 50% de pesticidas al 2030, Directiva 2009/128/CE sobre uso sostenible de plaguicidas, y la Red de Alerta Rápida RASFF de la UE). El EUDR no regula residuos de pesticidas, pero un rechazo por exceso de LMR (Límites Máximos de Residuos) en frontera UE tiene el mismo efecto de mercado que un rechazo por deforestación: pérdida del lote y del comprador. Los LMR son una vía de exclusión del mercado europeo que opera en paralelo al EUDR y que no está capturada en ninguna de las dimensiones D1–D14. **Aplica por igual a café y cacao.** Este bloque mide si la cooperativa tiene capacidad de identificar, prevenir y documentar el riesgo fitosanitario de su producto.

56. ¿La cooperativa conoce los LMR (Límites Máximos de Residuos de Pesticidas) de la UE aplicables a su producto de exportación, en particular los que el RASFF ha alertado para café o cacao peruano? (No sabe qué son los LMR / Los conoce en términos generales pero no verifica / Los conoce y verifica cumplimiento en las fincas de los socios / Los verifica sistemáticamente por lote antes del embarque)
57. ¿Existe un protocolo interno que prohíbe o restringe el uso de plaguicidas específicos en las fincas de los socios, en función de los LMR de la UE? (No existe / Lista informal comunicada verbalmente / Protocolo escrito, no verificado en campo / Protocolo escrito verificado en campo con evidencia)
58. ¿Se realizan análisis de residuos de pesticidas en el producto de exportación? (Nunca / Ocasionalmente, sin sistema definido / Sistemáticamente por campaña / Por lote antes del embarque, con resultado documentado y archivado)
59. ¿El comprador europeo ha exigido certificados de análisis de residuos o declaraciones de cumplimiento de LMR en los últimos 2 años? (No ha exigido nada / Lo exigió de forma puntual / Lo exige regularmente / Es parte del contrato vigente)
60. ¿La cooperativa ha tenido algún lote retenido, observado o rechazado en frontera UE por exceso de residuos de pesticidas en los últimos 3 años? (Sí, más de un evento / Sí, un evento / No / No sabe) — **bandera de alerta:** una respuesta "Sí" debe reportarse por separado e independientemente del puntaje promedio de D15.

> **Nota de alcance:** NO promedia en el ISA-EUDR (D1–D9). Es dimensión extendida del Pacto Verde, módulo (vi) Farm to Fork. Aplica a café y cacao sin distinción de herramienta — elimina el sesgo de D12 hacia café. Entra al ISA-PactoVerde como cuarto módulo (i/iv/v/vi), con peso igual a D12–D14 en la media aritmética del ISA-PactoVerde (ver Metodología ISA, §2.3 actualizado). La Q60 es bandera independiente del promedio de D15: un rechazo real en frontera anula cualquier percepción de preparación en las preguntas anteriores y debe reportarse siempre, igual que D2.10.

---

## Nota de puntaje (actualizada 2026-10-09)

- El promedio de cada dimensión **D1–D9** se calcula sobre las preguntas tipo escala/porcentaje únicamente (no las de texto libre ni las de mapeo).
- **D10 no se promedia como madurez** — sus tres ítems (Q36, Q37 y Q36a) se reportan aparte: Q36 y Q37 como banderas (falsa seguridad y oferta engañosa de "certificación EUDR"), porque un puntaje alto en "creer que ya está cubierto" sería, perversamente, una mala noticia, no una buena; Q36a como ítem de capacidad de asesoría recibida, que se codifica pero no promedia.
- **D11 no se promedia como madurez** — se reporta como inventario de oportunidades ya usadas vs. disponibles, insumo directo para el Instrumento 4 (columna "oportunidad").
- **D12, D13, D14, D15 no promedian en el ISA-EUDR** — son dimensiones extendidas del **Pacto Verde Europeo** (módulos i, iv, v, vi del proyecto madre ISCAM). Se reportan con su propio semáforo 0–4 por pregunta, se agregan internamente (media aritmética simple por dimensión) y conforman el **ISA-PactoVerde** = (D12 + D13 + D14 + D15) / 4. No anulan ni compensan el ISA-EUDR.
- **D15.Q60 (lote rechazado por LMR)** es bandera independiente del promedio de D15, igual que D2.10: un rechazo real en frontera se reporta siempre por separado, nunca absorbido en el promedio.
- **Bloque P (v0.2):** P1–P12 son variables de resultado/performance (no puntúan, no forman parte del ISA). P13–P14 son variables de resultado Pacto Verde ampliado, mismo tratamiento.

---

## Bloque P — Variables de Performance *(actualizado v0.2 — 2026-10-09)*

**Por qué existe este bloque:** el ISA (D1–D9 + D12–D15) mide qué tan preparada está la cooperativa — es el predictor. El proyecto madre pide además medir el **impacto** de esa preparación en resultados de negocio bajo el Pacto Verde completo. Estas preguntas recogen ese resultado para poder cruzarlas después contra el ISA de la misma organización.

**Limitación de diseño (mantener en todo reporte):** el levantamiento es transversal. Las preguntas P2, P5 y P7 son retrospectivas por autodeclaración — sirven para aproximar tendencia, no para análisis causal riguroso. Cualquier correlación ISA↔performance es asociación, nunca prueba de causalidad.

- P1. Volumen exportado a la Unión Europea en el último año (kg o toneladas, especificar unidad y producto si exporta ambos)
- P1b. Volumen TOTAL exportado a todos los destinos (UE y no UE) en el último año — permite calcular `% dependencia del mercado europeo = P1 / P1b`
- P2. Volumen exportado a la Unión Europea hace 3 años, mismo producto — *retrospectivo*
- P3. Ingreso total generado por ventas de exportación a la UE en el último año (S/ o USD, especificar moneda)
- P4. N.º de compradores/clientes europeos activos actualmente
- P5. N.º de compradores/clientes europeos activos hace 3 años — *retrospectivo*
- P6. Precio promedio pagado al socio productor por kg/quintal en el último año (S/ o USD) — conecta con D9.35
- P7. Precio promedio pagado al socio productor por kg/quintal hace 3 años — *retrospectivo*
- P8. ¿Ha tenido algún lote rechazado u observado por un comprador europeo por motivos de trazabilidad/deforestación en los últimos 2 años? (Sí / No / No sabe)
- P9. Si P8 = "Sí": N.º aproximado de lotes rechazados u observados
- P10. ¿Ha perdido algún contrato o comprador europeo en los últimos 2 años por motivos de cumplimiento (EUDR u otro requisito de sostenibilidad)? (Sí / No / No sabe)
- P11. % del volumen total exportado en el último año que cuenta con trazabilidad completa verificada hasta la parcela de origen (0–100%) — criterio de validación externa ISCAM; no promedia en ninguna dimensión
- P12. N.º de años consecutivos exportando a la Unión Europea, contando el año actual — criterio de validación externa ISCAM; mismo tratamiento que P11
- P13. **(nuevo, 2026-10-09 — Pacto Verde ampliado)** ¿Algún comprador europeo le ha exigido formalmente, en los últimos 2 años, información sobre huella de carbono, plan de reducción de emisiones, cumplimiento de LMR de pesticidas u otro requisito de sostenibilidad más allá del EUDR (ej. exigencias derivadas de CSRD/CSDDD del comprador)? (No / Sí, de forma verbal/informal / Sí, como cuestionario de proveedor o documentación formal / Sí, como cláusula contractual o condición de pago) — variable de resultado Pacto Verde; no promedia en ninguna dimensión del ISA.
- P14. **(nuevo, 2026-10-09 — acceso a financiamiento verde)** ¿La cooperativa ha accedido o intentado acceder en los últimos 2 años a financiamiento verde, crédito de impacto o fondos condicionados a criterios de sostenibilidad del Pacto Verde (ej. criterios de taxonomía UE, banco verde, fondo de cooperación climática)? (No ha intentado acceder / Lo intentó pero no cumplió los criterios / Sí, recibió financiamiento verde / No sabe si aplica a su caso) — variable de resultado Pacto Verde; no promedia en ninguna dimensión del ISA.

**Indicadores derivados a calcular en el análisis (no preguntas nuevas):**
- Variación de volumen exportado UE = (P1 − P2) / P2
- Variación de N.º de compradores europeos = P4 − P5
- Variación del precio pagado al socio = (P6 − P7) / P7
- Tasa de incidencia de rechazo = P9 / lotes totales exportados en el período
