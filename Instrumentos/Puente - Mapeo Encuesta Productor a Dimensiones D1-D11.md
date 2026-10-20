# Puente — Mapeo de la Encuesta a Productores (Google Forms, 108 preguntas) a las Dimensiones D1–D11

**Propósito:** este documento traduce el formulario ya aplicado en campo (`Encuesta - Formularios de Google.pdf`, nivel productor individual) al marco de 11 dimensiones del **Instrumento 1** / **Instrumento 2**, que fue diseñado a nivel cooperativa. No reemplaza al Instrumento 2 — lo alimenta parcialmente. Las preguntas del form se referencian por su número de pregunta en el PDF (1–108).

**Regla general de agregación:** cuando una dimensión se puntúa 0–4 a nivel cooperativa (Instrumento 2) y la fuente es una pregunta Sí/No o categórica a nivel productor, la cooperativa se puntúa según el **% de productores** que responden en la categoría de mayor madurez, usando los cortes:
> **0** <20% · **1** 20–40% · **2** 40–65% · **3** 65–90% · **4** >90%, salvo que se indique otra regla en la fila.

---

## D1 — Clasificación regulatoria

El form fue diseñado para productor individual; D1 es una decisión que corresponde a la **cooperativa como operador**, no al productor. Cobertura parcial:

| Pregunta(s) | Contenido | Ítem D1 | Regla de agregación | Observación |
|---|---|---|---|---|
| 1 | Rol: productor / representante de cooperativa | — | Usar como filtro, no como dato | Solo las respuestas de "Representante de cooperativa" pueden en principio responder D1 con propiedad |
| 19 | ¿Su cultivo se vende a compradores que exportan a la UE? | D1.1 (indirecto) | % que responde "Sí" indica exposición de la cooperativa al mercado UE | No sustituye la pregunta directa a la cooperativa sobre su propio rol |
| 78 | ¿Cuenta con RUC? (solo cooperativas que exportan directamente) | D1.1 / D1.4 | Dato binario a nivel organización | Ya está filtrado en el form solo para quien exporta directo — es el ítem más cercano a D1 real |

**Brecha:** D1.2 (transforma el producto), D1.3 (certeza sobre su rol regulatorio), D1.4 (umbral micro/pequeña empresa) **no están cubiertos** — requieren aplicar el bloque D1 del Instrumento 2 directamente a la directiva/gerencia.

---

## D2 — Trazabilidad y geolocalización

| Pregunta(s) | Contenido | Ítem D2 | Regla de agregación | Observación |
|---|---|---|---|---|
| 37 | ¿Conoce la ubicación geográfica (coordenadas) de sus parcelas? (Todas/Algunas/Ninguna) | D2.5, D2.6 | % de productores en "Todas" = proxy directo de D2.6 | |
| 38 | ¿Coordenadas registradas con GPS, celular u otro dispositivo? | D2.5 | % "Sí" | Complementa 37: registrado ≠ conocido de memoria |
| 39 | ¿Cuenta con mapa o polígono que delimite sus parcelas? | D2.5 | % "Todas" | Polígono es más exigente que punto GPS — no promediar con 37/38 sin distinguir |
| 40 | ¿Quién realizó la georreferenciación? | D2.8 | Distribución de respuestas (productor propio / cooperativa / comprador / certificadora / ONG / Estado / no sabe) | Responde directamente D2.8; útil también para D11 (quién apoya) |
| 41 | ¿Coordenadas almacenadas en algún registro o sistema? | D2.5, D2.7 (parcial) | % "Sí" | Indicio de sistema, pero no confirma que el sistema vincule lote exportado ↔ parcela (eso es D2.7 completo, ver brecha) |
| 82, 83 | ¿Compra a otros productores para revender? / Si compra a terceros, ¿registra proveedor, cantidad, fecha y procedencia? | **D2.10 (bandera de mezcla sin trazabilidad)** | Cualquier "Sí" en 82 + "No" o "Parcialmente" en 83 = bandera roja activa | Esta es la correspondencia más valiosa del mapeo: 82+83 operacionalizan exactamente la bandera D2.10 que el Instrumento 2 planteaba en abstracto |

**Brecha:** D2.9 (frecuencia de actualización del registro) no se pregunta — el form es una foto única, no captura periodicidad. D2.7 (vínculo lote exportado↔parcela específica) solo se infiere parcialmente vía Q41; falta la pregunta directa a nivel de cooperativa/acopio.

---

## D3 — Legalidad de la producción

Esta dimensión es, con diferencia, la mejor cubierta por el form — probablemente porque el form organiza sus propias secciones EUDR ("Derechos de uso de suelo", "Derechos de terceros", "Derechos laborales", "Derechos humanos", "Impuestos, comercio, aduanas y anticorrupción") siguiendo la misma lista de "legislación pertinente" del artículo 3(b) del reglamento que da origen a D3.

| Pregunta(s) | Contenido | Ítem D3 | Regla de agregación | Observación |
|---|---|---|---|---|
| 30 | Relación con las tierras (propietario/comunero/arrendatario/posesionario/concesionario/otra) | D3.11 | % en categorías con reconocimiento legal formal (propietario, comunero, concesionario con CCUSAF) vs. informal | |
| 31, 32 | ¿Cuenta con documento que acredite propiedad/posesión? / Qué documento posee | D3.11 | % "Sí, todas" en 31 | 32 da el detalle cualitativo (título vs. constancia vs. contrato) |
| 33, 34 | ¿Parcela dentro de comunidad campesina/nativa? / ¿Autorización de la comunidad? | D3.12 (parcial) | Cruce: 33="Sí" y 34="No" = brecha activa | |
| 35, 36 | ¿Parcela en área natural protegida/zona restringida? / ¿Cuenta con permisos? | D3.12 | Cruce: 35="Sí" y 36="No" = brecha activa | |
| 60–64 | Contratación de trabajadores, acuerdo de pago, jornal, N° de personas, registro de pagos | D3.13 | % con registro (64="Sí") entre quienes contratan (60≠"No") | |
| 65–70 | Descanso, retiro voluntario, trabajo forzoso/deuda, EPP, capacitación pesticidas, accidentes | D3.13 | Cada ítem por separado; **67 ("trabaja para pagar deuda") es bandera dura**: cualquier "Sí" detiene el promedio y se reporta aparte, no se diluye | Es información sensible (indicio de trabajo forzoso) — tratar como el resto de banderas del marco (igual que D2.10/D10), nunca promediar |
| 71–77 | Igualdad salarial, trabajo infantil, interferencia escolar, discriminación, violencia/acoso, participación de mujeres en decisiones | D3.13 extendido (derechos humanos) | Igual criterio: 72 ("participan menores de 18") y 75/76 (discriminación/violencia) son banderas, no promedio | El Instrumento 2 no desagregaba explícitamente "derechos humanos" de "cumplimiento laboral" dentro de D3.13 — este form sí lo hace, y se recomienda que el Instrumento 1 explicite esta subdivisión en su próxima revisión |
| 84–86 | Solicitud de pago no oficial, reglas anticorrupción, registros de exportación | D3 (tributario/anticorrupción) | 84="Sí" es bandera; 85/86 miden control interno | |
| 87, 88 | Documentación aduanera / sanciones aduaneras | D3 (aduanas) | % "Sí"/"Parcial" en 87; 88="Sí" es bandera | |
| 55–59 | Conflicto con vecinos, mecanismo de reclamos, sitios de importancia cultural, consulta previa | D3 (derechos de terceros) | 55="Sí" y 56="No sabe"/"No" = brecha | |

**Ítem 14 (nuevo) del Instrumento 2** — "¿parcela en zona de desarrollo alternativo / antecedentes de conflicto social-territorial?" — **no está en el form**. Es una pregunta sensible que probablemente se omitió deliberadamente en un instrumento auto-administrado; si se necesita, debe levantarse en la Guía de Entrevista Semiestructurada (Instrumento 3), no en la encuesta masiva.

---

## D4 — Riesgo de deforestación

| Pregunta(s) | Contenido | Ítem D4 | Regla de agregación | Observación |
|---|---|---|---|---|
| 24 | Uso del terreno antes del 01/01/2021 | D4.15 | Insumo cualitativo (no promedia) | Cruzar con 25/26 para construir el indicador real |
| 25 | ¿Ha talado bosque desde el 1/1/2021? | D4.15 | 25="Sí" es bandera dura (posible incumplimiento del corte regulatorio) | Esta es la pregunta más crítica de todo el form frente al EUDR |
| 26, 27 | ¿Ha ampliado área desde 2021? / Uso anterior del área ampliada | D4.15 | 26="Sí" + 27 en {Pastos, Purma, Bosque virgen} = bandera; 27="Cacao/Café/otro cultivo" = expansión sobre tierra ya agrícola, menor riesgo | |
| 28 | ¿Cuenta con documentos/fotos/mapas que demuestren uso pre-2021? | D4.15 | % "Sí" entre quienes ampliaron o son dudosos | Evidencia documental, clave para la declaración de diligencia debida (D5.19) |
| 29 | ¿Cooperativa/comprador ha verificado no deforestación post-2020? | D4.15 | % "Sí" | Verificación por tercero, más fuerte que autodeclaración |

**Brecha:** D4.16 (uso de herramientas de monitoreo satelital tipo Global Forest Watch) y D4.17 (conocimiento de la clasificación de riesgo del país/región) son decisiones/capacidades de la **cooperativa**, no del productor — no están en el form y deben tomarse del Instrumento 2 aplicado a la organización.

---

## D5 — Sistema interno de diligencia debida

**Cobertura mínima.** El form no pregunta por procedimientos escritos, declaraciones de diligencia debida ni responsable designado — son decisiones organizacionales.

| Pregunta(s) | Contenido | Ítem D5 | Observación |
|---|---|---|---|
| 21, 22 | Capacitaciones y asistencia técnica recibidas en el último año, por fuente | D5.21 (parcial) | Mide si el productor recibió capacitación, pero no si la cooperativa tiene un **sistema formal** de diligencia debida — son cosas distintas. Útil como proxy débil, no sustituto |
| 89/90 | ¿Su cooperativa o comprador le ha informado sobre requisitos ambientales o sociales que debe cumplir? | D5 (comunicación interna) | Nota: **la pregunta 89 y 90 del PDF están duplicadas literalmente** — revisar el formulario original en Google Forms y corregir antes de la siguiente ronda de aplicación |

**Brecha real:** D5.18 (procedimiento escrito), D5.19 (declaración de diligencia debida presentada), D5.20 (responsable designado) — ninguno cubierto. Aplicar directamente el bloque D5 del Instrumento 2 a la gerencia/directiva.

---

## D6 — Capacidad organizacional y digital

**Sin cobertura.** Presupuesto, digitalización de registros, conectividad y gestión de apoyo externo son atributos de la cooperativa como organización — el form nunca pregunta esto porque está dirigido al productor de base. Aplicar el Instrumento 2 completo (D6) a la gerencia.

---

## D7 — Cadena de valor

| Pregunta(s) | Contenido | Ítem D7 | Observación |
|---|---|---|---|
| 19 | ¿Su cultivo se vende a compradores que exportan a la UE? | D7.26 (parcial) | Confirma exposición a la cadena UE, pero no si el comprador **exige formalmente** geolocalización/diligencia debida (eso es la pregunta real de D7.26) |

**Brecha:** D7.26 (exigencia formal del comprador), D7.27 (financiamiento/asistencia condicionada) y D7.28 (riesgo percibido de perder el contrato) no están en el form — son percepciones que requieren la pregunta directa del Instrumento 2, idealmente a la cooperativa (que es quien negocia con el comprador), no al productor individual.

---

## D8 — Gobernanza interna y apropiación de los socios

| Pregunta(s) | Contenido | Ítem D8 | Regla de agregación | Observación |
|---|---|---|---|---|
| 21, 22 (fila "Cooperativa o asociación") | ¿Recibió capacitación/asistencia técnica de su cooperativa? | D8.29 (proxy) | % "Sí" en la columna "Cooperativa o asociación" | Es un indicio de que la cooperativa está comunicando activamente a sus socios, pero no mide si el contenido fue específico sobre EUDR |
| 23 | ¿Conoce o ha escuchado sobre el Pacto Verde Europeo? | D8.30 (proxy directo) | % "Sí, conozco la normativa" = aproximación directa a "% de socios que entienden por qué se les pide geolocalización/documentación" | Buena correspondencia, aunque el Pacto Verde es más amplio que el EUDR específicamente — tratarlo como cota superior optimista, no como medida exacta |

**Brecha:** D8.31 (mecanismo formal/incentivo para que el socio entregue información) y D8.32 (rotación de directiva) son preguntas de diseño institucional — no están en el form, van al Instrumento 2 con la directiva.

---

## D9 — Sostenibilidad económica del cumplimiento

**Sin cobertura.** Costo de adecuación frente al presupuesto, financiamiento con deuda y riesgo de traslado del costo al productor son preguntas de la cooperativa como entidad económica. El form no las contiene. Aplicar el bloque D9 del Instrumento 2 a la gerencia/tesorería.

---

## D10 — Confusión entre certificación voluntaria y cumplimiento EUDR

| Pregunta(s) | Contenido | Ítem D10 | Observación |
|---|---|---|---|
| 20 | ¿Cuenta con alguna certificación? (Orgánico, Fairtrade, Rainforest Alliance, etc.) | Insumo previo a D10.36 | Solo confirma existencia de certificación — no pregunta si el productor **cree que esa certificación ya lo cubre frente al EUDR**, que es el núcleo de la bandera D10 |
| 23 | ¿Conoce el Pacto Verde Europeo? | Insumo indirecto | Contexto general, no la confusión específica |

**Brecha crítico:** la pregunta central de D10 ("¿cree que su certificación vigente ya cubre las obligaciones del EUDR?") **no existe en el form** y es, según el Instrumento 7, uno de los hallazgos de mayor valor del marco (una bandera de falsa seguridad). Se recomienda **agregar una pregunta de seguimiento condicional** después de la Q20 cuando el productor marque alguna certificación: *"¿Considera que esta certificación ya cumple con los requisitos del reglamento europeo de deforestación (EUDR)?"* con las mismas opciones del Instrumento 2 (Sí totalmente / Sí en parte / No, son cosas distintas / No tiene certificación).

---

## D11 — Ecosistema de apoyo externo

| Pregunta(s) | Contenido | Ítem D11 | Regla de agregación | Observación |
|---|---|---|---|---|
| 21, 22 | Tablas de capacitación y asistencia técnica por fuente: Estado (MIDAGRI/DRA/Agrorural/INIA/SENASA), ONG, Empresa Privada, CITE, Cooperativa, Universidad, Otro | **D11.38 (mapeo directo)** | Para cada actor: % de productores que marcó "Sí" = intensidad de contacto actual con ese actor | Esta es la mejor correspondencia 1:1 de todo el mapeo — las categorías de actor del form calzan casi exactamente con la lista de D11.38 (falta solo "Junta Nacional del Café / APPCACAO u otro gremio" y "PNCB-MINAM" como opciones explícitas) |
| 40 | ¿Quién realizó la georreferenciación? | D11.38 (complemento) | Distribución de respuestas | Confirma si el apoyo de geolocalización vino de un actor externo específico |

**Recomendación de mejora:** añadir "Junta Nacional del Café / APPCACAO / gremio" y "PNCB-MINAM (monitoreo satelital)" como opciones explícitas en las preguntas 21 y 22 para que D11 quede completamente cubierto por el form en la próxima ronda.

---

## Contenido del form sin equivalente en D1–D11 (candidato a dimensión ambiental operativa)

Las preguntas 42–54 y 93–106 (pesticidas y su disposición, fuente y autorización de agua, tratamiento de aguas residuales, manejo de residuos, biodiversidad, fertilizantes, combustible, energía de procesamiento, transporte y huella de carbono/GEI) **no tienen dimensión asignada** en el marco actual de 11 dimensiones. El Instrumento 1 las trataría hoy, en el mejor de los casos, como parte difusa de D4 (ambiental) o D3 (legalidad ambiental), pero son en realidad una **batería operativa independiente** — más cercana a una futura huella de carbono/gestión ambiental de finca que a diligencia debida EUDR estricta.

**Recomendación:** no forzar estas ~25 preguntas dentro de D1–D11. Documentarlas como **anexo ambiental complementario** (o una eventual D12 si el toolkit decide institucionalizarlo) y dejar constancia en el Instrumento 7 de que fueron cubiertas por el form pero quedan fuera del alcance de puntaje EUDR actual — igual que Instrumento 7 ya documenta otras exclusiones deliberadas.

---

## Resumen de cobertura por dimensión

| Dimensión | Cobertura por el form | Acción pendiente |
|---|---|---|
| D1 | Muy baja (1 pregunta indirecta) | Aplicar Instrumento 2 a directiva/gerencia |
| D2 | Alta (incluye la bandera D2.10) | Completar D2.9 (frecuencia) y D2.7 (vínculo lote-parcela) a nivel cooperativa |
| D3 | Muy alta — la mejor cubierta | Agregar el ítem 14 (zona de conflicto/desarrollo alternativo) vía entrevista, no encuesta |
| D4 | Alta en corte 2021, nula en capacidad de monitoreo | Completar D4.16/D4.17 con la cooperativa |
| D5 | Muy baja | Aplicar Instrumento 2 completo a la gerencia |
| D6 | Nula | Aplicar Instrumento 2 completo a la gerencia |
| D7 | Muy baja (1 pregunta parcial) | Aplicar Instrumento 2 con quien negocia con el comprador |
| D8 | Media (dos proxies razonables) | Completar D8.31/D8.32 con la directiva |
| D9 | Nula | Aplicar Instrumento 2 completo a tesorería/gerencia |
| D10 | Insuficiente — falta la pregunta núcleo | Agregar pregunta de seguimiento condicional tras Q20 |
| D11 | Alta — mapeo casi directo | Agregar 2 opciones de actor faltantes |

**Conclusión operativa:** el form cubre muy bien el diagnóstico de **campo/parcela** (D2, D3, D4) pero no puede, por diseño, cubrir las dimensiones que dependen de decisiones **organizacionales** (D1, D5, D6, D7, D9) ni la bandera D10. La combinación correcta no es fusionar los cuestionarios, sino: (1) usar este form como fuente de datos agregados para D2–D4 y D8/D11 parcial, y (2) aplicar el Instrumento 2 en su forma original — sin cambios — a la directiva/gerencia de cada cooperativa para cerrar D1, D5, D6, D7, D9 y D10.

**Correcciones al formulario recomendadas antes de la próxima ronda de campo:**
1. Eliminar la duplicación literal de las preguntas 89 y 90.
2. Revisar la duplicación entre 104 y 105 (ambas preguntan por información de emisiones GEI; 105 agrega la definición extendida — probablemente 104 sobra o debía ser una pregunta distinta).
3. Agregar la pregunta condicional de D10 tras la Q20.
4. Agregar "Junta Nacional del Café / APPCACAO / gremio" y "PNCB-MINAM" en las tablas de las preguntas 21 y 22.
