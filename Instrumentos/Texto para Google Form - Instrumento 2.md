# Texto para Google Form — Instrumento 2 (119 preguntas, v0.4)

**Tarea:** Fase 1, Plan de Trabajo 75 días — "Construir el Google Form de Instrumento 2". El asistente no puede crear el Form directamente (requiere acceso a Google Forms); este documento deja listo el texto exacto, pregunta por pregunta, tipo de campo y opciones, para que se cargue en ~45–60 minutos de trabajo manual (o se pegue vía un complemento de importación masiva tipo "Form Builder from Spreadsheet").

**Configuración general del Form (una sola vez, antes de la primera sección):**
- Activar "Recopilar direcciones de correo electrónico" → No (la identificación es por RUC, no por correo del encuestador).
- Vincular a una Google Sheet nueva, usando exactamente los encabezados de `Estructura Google Sheet - Respuestas Instrumento 2.md`.
- Desactivar "Limitar a 1 respuesta" (una misma cooperativa puede tener más de una entrevista si se reaplica).
- Todas las preguntas obligatorias excepto las marcadas `(opcional)`.

---

## Sección 0 — Metadata de campo (agregar antes del Bloque 0, no viene del instrumento original)

| Pregunta | Tipo de campo Google Forms | Opciones |
|---|---|---|
| Fecha de aplicación | Fecha | — |
| Nombre del encuestador/a | Respuesta corta | — |
| Canal de aplicación | Lista desplegable | Google Form directo / Piggyback GIZ / Piggyback SAFE / Piggyback MIDAGRI / Evento gremial / Otro |

---

## Sección 1 — Bloque 0: Ficha de identificación

**Texto de encabezado de sección:** "Esta sección identifica a la organización. No se puntúa — es la ficha base."

| # | Pregunta (texto a pegar) | Tipo de campo | Opciones |
|---|---|---|---|
| B0.1 | Nombre de la cooperativa / razón social | Respuesta corta | — |
| B0.2 | RUC | Respuesta corta (validación: regex 11 dígitos si el Form lo permite) | — |
| B0.3 | Producto(s) exportado(s) (café, cacao, madera, otro — indique código SA si lo conoce) | Párrafo | — |
| B0.4 | N.º de socios productores y hectáreas totales asociadas (indique ambos: "N.º socios: ___ / Hectáreas: ___") | Párrafo | — |
| B0.5 | ¿Exporta directamente a la Unión Europea o a través de un tercero? | Opción múltiple | Directamente / A través de un tercero |
| B0.6 | Si respondió "a través de un tercero": ¿quién es el comprador que sí exporta a la UE? (deje en blanco si no aplica) | Respuesta corta (opcional) | — |
| B0.7 | Volumen anual aproximado destinado a la UE, como % del total exportado | Respuesta corta (validación numérica 0-100) | — |
| B0.8 | Destino(s) de sus exportaciones, marcando primero el principal — incluya destinos fuera de la UE | Casillas de verificación | Alemania / Bélgica / Países Bajos / Francia / Italia / España / Suecia / Dinamarca / Estados Unidos / Japón / China / Otro (especificar) |

**Destino:** variable `destino_principal` del cuestionario de verificación rápida (D7) y validación cruzada de países destino contra DUAs en la matriz de organizaciones.
| B0.9 | Certificaciones voluntarias vigentes | Casillas de verificación | Rainforest Alliance / Fairtrade / Orgánico / UTZ / Otra / Ninguna |
| B0.10 | ¿Las parcelas de los socios están concentradas en un solo distrito, repartidas en varios distritos de una misma provincia, o dispersas en varias provincias/regiones? | Opción múltiple | Un solo distrito / Varios distritos, misma provincia / Varias provincias o regiones |
| B0.11 | Distancia aproximada entre las parcelas más alejadas de los socios y el centro de acopio o planta de procesamiento más cercano | Opción múltiple | Menos de 5 km / Entre 5 y 20 km / Entre 20 y 50 km / Más de 50 km / No se ha medido |
| B0.12 | % de mujeres en la directiva/consejo directivo | Respuesta corta (validación numérica 0-100) | — |
| B0.13 | ¿Qué porcentaje aproximado de los socios productores opera en zonas clasificadas como de riesgo alto o muy alto de deforestación según el Mapa de Deforestación del MINAM o Global Forest Watch? | Opción múltiple | Menos del 10% / Entre 10% y 30% / Entre 30% y 60% / Más del 60% / No se ha evaluado |
| B0.14 | ¿La cooperativa tiene capacidad técnica de verificación directa en campo —personal o prestataire con formación agronómica— para supervisar las prácticas de los socios en sus parcelas de forma periódica? | Opción múltiple | No tiene capacidad de verificación / Parcial, cubre menos de la mitad de los socios / Parcial, cubre más de la mitad / Sí, capacidad suficiente para visitas periódicas a todos los socios |
| B0.15 | Tipo de organización | Opción múltiple | Asociación / Cooperativa agraria / Cooperativa de servicios / Central o federación de cooperativas / Empresa / Otro (especificar) |
| B0.16 | Departamento (y provincia) donde está registrada la sede de la organización | Respuesta corta | — |
| B0.17 | ¿La organización está inscrita en el RNCA (Registro Nacional de Cooperativas Agrarias)? | Opción múltiple | Sí / En trámite / No / No aplica (no es cooperativa agraria) |

**Destino:** B0.15 → columna `P` (Tipo org.) de `MATRIZ_174`, hoy usada como proxy de IV5; B0.16 → columna `C` (Depto) de `MATRIZ_174`, validación cruzada contra SUNAT y alimentación de `RADAR_BRECHAS`; B0.17 → `ISCAM_Score!V` (IV2 diseñado = RNCA) y variable `rnca` del proxy.

---

## Sección 2 — Bloque P: Variables de desempeño

**Texto de encabezado de sección:** "Esta sección mide resultados de negocio, no madurez de cumplimiento. Las preguntas que piden una cifra de hace 3 años son un recuerdo aproximado, no un dato verificado — tómelo como referencia, no como registro exacto."

**Destino:** P1/P1b/P3/P4 alimentan IV1 (presión UE) del índice; P3 + B0.4 permiten derivar los indicadores PVE P1 (productividad) y P2 (ingreso neto USD/ha) de `MATRIZ_174`; P11 coincide con la columna `AK` (Score trazabilidad). Este bloque no puntúa dimensiones ISCAM.

| # | Pregunta | Tipo de campo | Opciones |
|---|---|---|---|
| P1 | Volumen exportado a la Unión Europea en el último año (especifique unidad —kg o toneladas— y producto si exporta ambos) | Párrafo | — |
| P1b | Volumen TOTAL exportado a todos los destinos (UE y no UE) en el último año, mismo producto y misma unidad que la pregunta anterior | Párrafo | — |
| P2 | Volumen exportado a la Unión Europea hace 3 años, mismo producto (kg o toneladas) | Párrafo | — |
| P3 | Ingreso total generado por ventas de exportación a la UE en el último año (especifique moneda: S/ o USD) | Párrafo | — |
| P4 | N.º de compradores/clientes europeos activos actualmente | Respuesta corta (numérica) | — |
| P5 | N.º de compradores/clientes europeos activos hace 3 años | Respuesta corta (numérica) | — |
| P6 | Precio promedio pagado al socio productor por kg/quintal en el último año (especifique S/ o USD) | Respuesta corta | — |
| P7 | Precio promedio pagado al socio productor por kg/quintal hace 3 años | Respuesta corta | — |
| P8 | ¿Ha tenido algún lote rechazado u observado por un comprador europeo por motivos de trazabilidad/deforestación en los últimos 2 años? | Opción múltiple | Sí / No / No sabe |
| P9 | Si la respuesta anterior fue "Sí": N.º aproximado de lotes rechazados u observados (deje en blanco si no aplica) | Respuesta corta (opcional) | — |
| P10 | ¿Ha perdido algún contrato o comprador europeo en los últimos 2 años por motivos de cumplimiento (EUDR u otro requisito de sostenibilidad del comprador)? | Opción múltiple | Sí / No / No sabe |
| P11 | % del volumen total exportado en el último año que cuenta con trazabilidad completa verificada hasta la parcela de origen (0-100%) | Respuesta corta (validación numérica 0-100) | — |
| P12 | N.º de años consecutivos exportando a la Unión Europea, contando el año actual | Respuesta corta (numérica) | — |
| P13 | ¿Algún comprador europeo ha exigido formalmente, en los últimos 2 años, información sobre huella de carbono, LMR de pesticidas u otro requisito de sostenibilidad más allá del EUDR? | Opción múltiple | No / Sí, de forma verbal o informal / Sí, como cuestionario de proveedor o documentación formal / Sí, como cláusula contractual o condición de pago |
| P14 | ¿La cooperativa ha accedido o intentado acceder a financiamiento verde, crédito de impacto o fondos condicionados a criterios de sostenibilidad del Pacto Verde en los últimos 2 años? | Opción múltiple | No ha intentado / Lo intentó pero no cumplió los criterios / Sí, recibió financiamiento verde / No sabe si aplica a su caso |

---

## Sección 3 — D1: Clasificación regulatoria

| # | Pregunta | Tipo de campo | Opciones |
|---|---|---|---|
| D1.1 | ¿La cooperativa introduce el producto directamente en el mercado de la UE bajo su propio nombre? | Opción múltiple | Sí / No |
| D1.2 | ¿Transforma el producto (trilla, tostado, fermentado, aserrío) antes de venderlo? | Opción múltiple | Transforma / No transforma |
| D1.3 | ¿Sabe con certeza qué rol le corresponde (operador, operador posterior, comerciante, micro/pequeño operador primario)? | Opción múltiple | Sí con certeza / Idea aproximada / No sabe |
| D1.4 | ¿Cumple los umbrales de microempresa/pequeña empresa (Directiva 2013/34/UE)? | Opción múltiple | Sí / No / No sabe |
| D1.3a | *(Rama: solo si D1.3 = "Sí con certeza" o "Idea aproximada")* ¿Cuál es el rol que le corresponde a la organización? | Opción múltiple | Operador / Operador posterior / Comerciante / Micro o pequeño operador primario / No sabe |

## Sección 4 — D2: Trazabilidad y geolocalización

| # | Pregunta | Tipo de campo | Opciones |
|---|---|---|---|
| D2.5 | ¿Existe registro de geolocalización (GPS/polígono) por parcela de socio? | Escala lineal 0-4 | 0 = No existe/No sabe … 4 = Implementado y verificado/auditado |
| D2.6 | % de socios con parcela geolocalizada | Respuesta corta (validación numérica 0-100) | — |
| D2.7 | ¿El sistema vincula un lote exportado con la(s) parcela(s) específica(s)? | Escala lineal 0-4 | Misma leyenda que D2.5 |
| D2.8 | ¿Quién levantó la información de geolocalización? | Opción múltiple | Técnico propio / Consultor / Proyecto de cooperación / Socio por su cuenta / No se ha levantado |
| D2.9 | Frecuencia de actualización de la geolocalización | Opción múltiple | Nunca / Al ingreso del socio / Anual / Por cosecha |
| D2.10 | ¿Existe algún punto en el proceso de acopio o beneficio donde se mezclan físicamente lotes de distinto origen sin registro de qué parcelas los componen? | Opción múltiple | Sí, se mezclan sin control / Se mezclan pero con registro de origen / No, se mantiene segregación física completa |
| D2.5a | ¿Qué porcentaje aproximado del volumen exportado proviene de proveedores externos (productores que no son socios de la cooperativa)? | Opción múltiple | 0%, todo proviene de socios / Menos del 10% / Entre 10% y 30% / Más del 30% / No se ha cuantificado |
| D2.5b | *(Rama: solo si D2.5a ≠ "0%, todo proviene de socios" y ≠ "No se ha cuantificado")* Si compra a proveedores externos: ¿se registra el nombre, la cantidad y el origen (parcela o zona) de cada proveedor externo? | Opción múltiple | Sí, verificado con georreferencia / Sí, pero sin georreferencia / Solo nombre y cantidad / No se registra / No aplica |

**Destino:** variables `pct_ext` y `traza_ext` del proxy; dimensión D2 (`ISCAM_Score!F`, vía `SCORECARDS!H`). La debida diligencia del operador EUDR cubre también a proveedores no socios — por eso estas preguntas no estaban en el proxy como opcionales.

## Sección 5 — D3: Legalidad de la producción

| # | Pregunta | Tipo de campo | Opciones |
|---|---|---|---|
| D3.11 | % de socios con título de propiedad o posesión reconocida legalmente | Respuesta corta (validación numérica 0-100) | — |
| D3.12 | ¿Hay parcelas superpuestas a áreas naturales protegidas o su zona de amortiguamiento, reservas comunales o territorios indígenas sin sanear? | Opción múltiple | Sí, extensa / Sí, puntual / Sí, en área natural protegida o zona de amortiguamiento / No verificado / No, ninguna |
| D3.13 | ¿Se verifica cumplimiento laboral (no trabajo infantil, seguridad social) a nivel de finca? | Escala lineal 0-4 | Misma leyenda que D2.5 |
| D3.14 | ¿Alguna parcela de socios se ubica en una zona de desarrollo alternativo (ex-cultivo de coca) o con antecedentes de conflicto social/territorial? | Opción múltiple | Sí / No / No verificado |
| D3.14a | ¿Los socios cuentan con autorización de uso de agua para su actividad productiva, cuando corresponde? | Opción múltiple | Sí, todas las fuentes verificadas / Parcialmente / No / No aplica |
| D3.14b | ¿El tratamiento de aguas residuales del beneficio/procesamiento cumple con lo exigido por la autoridad ambiental? | Opción múltiple | Siempre / A veces / No / No aplica |
| D3.14c | ¿Alguna parcela de socios se encuentra dentro de la faja marginal de un río, quebrada, lago o laguna? | Opción múltiple | Sí / No / No sabe |
| D3.14d | En las parcelas de los socios y en el inmueble donde opera la cooperativa, ¿existe algún derecho de terceros (carga, embargo, servidumbre, usufructo, arrendamiento o derecho de uso consuetudinario) que condicione o restrinja el uso de la tierra para cultivar café o cacao, o el derecho de la cooperativa a operar en esa finca? | Opción múltiple | No existe ningún derecho de terceros / Existe, pero está registrado y no restringe el uso / Existe un acuerdo documentado con el titular o con la autoridad que legitima el uso, aunque la cooperativa o el socio no tenga título formal / Existe usufructo, arrendamiento o carga sin acuerdo que lo resuelva / Se han invocado derechos de uso tradicional o consuetudinarios por una comunidad o pueblo indígena sin proceso de acuerdo / No verificado |
| D3.14e | ¿La cooperativa y sus socios están al día en sus obligaciones tributarias, aduaneras y comerciales vinculadas a la actividad exportadora? | Opción múltiple | Sí, verificado / Parcialmente / No verificado / No sabe |
| D3.14f | ¿Existen políticas o mecanismos internos contra la corrupción (código de conducta, canal de denuncias) aplicables a la cadena de abastecimiento? | Opción múltiple | Sí, formalizado / Informal / No existe |
| D3.14g | Cuando corresponde (parcelas de socios en territorio de comunidades indígenas, nativas o campesinas), ¿se ha realizado un proceso de Consentimiento Libre, Previo e Informado (CLPI)? | Opción múltiple | Sí, proceso documentado / Aplica pero no se ha realizado / No aplica, no hay territorios de este tipo / No sabe |
| D3.14h | ¿La organización cuenta con autorizaciones ambientales vigentes para su planta y actividad (EIA, DIA, certificación forestal o certificado de habilitación, según corresponda)? | Opción múltiple | Sí, vigentes y verificadas / Parcial, alguna falta o está vencida / No / No aplica (sin actividad que la requiera) |
| D3.14i | ¿Existe algún proceso sancionador vigente de OEFA, SINEFA u otra autoridad ambiental contra la organización o sus socios? | Opción múltiple | Sí, vigente y sin resolver / Sí, en proceso de resolución / No / No sabe |

**Destino:** variables `aut_ambiental` y `sancion_oea` del proxy; dimensión D3 (`ISCAM_Score!G`); D3.14i actualiza `MATRIZ_174!U` (hoy solo score OSCE con corte a abril 2024) y alimenta la bandera `ISCAM_Score!AD` e `X` (IV4).

## Sección 6 — D4: Riesgo de deforestación

| # | Pregunta | Tipo de campo | Opciones |
|---|---|---|---|
| D4.15 | ¿Se verificó cambio de uso de suelo posterior al 31 de diciembre de 2020 mediante cruce de las parcelas con mapas de deforestación (GEOSERFOR/PNCB o Global Forest Watch)? | Opción múltiple | No verificado / Verificación parcial / Verificado sin hallazgos / Casos detectados sin resolver / Verificado sistemáticamente y documentado |
| D4.16 | ¿Usa herramientas de monitoreo satelital (Global Forest Watch, plataformas nacionales)? | Escala lineal 0-4 | Misma leyenda que D2.5 |
| D4.17 | ¿Conoce la clasificación de riesgo (bajo/estándar/alto) de su zona? | Opción múltiple | Sí documentado / Idea aproximada / No sabe |
| D4.15a | ¿Se han detectado alertas activas de deforestación en parcelas de socios de la organización (GEOSERFOR, PNCB o Global Forest Watch)? | Opción múltiple | Sí, detectadas y sin resolver / Sí, detectadas y mitigadas o aclaradas / No se han detectado / No se monitorea |

**Destino:** variable `alerta_deforest` del proxy; dimensión D4 (`ISCAM_Score!H`) e IP2 (`√(D3×D4)`).

## Sección 7 — D5: Sistema interno de diligencia debida

| # | Pregunta | Tipo de campo | Opciones |
|---|---|---|---|
| D5.18 | ¿Existe procedimiento escrito de diligencia debida? | Escala lineal 0-4 | Misma leyenda que D2.5 |
| D5.18a | ¿Existe una política de deforestación formal y escrita (distinta del procedimiento operativo), con objetivos, metas medibles y plazos (ej. compromiso de "cero deforestación" a una fecha determinada)? | Escala lineal 0-4 | Misma leyenda que D2.5 |
| D5.18b | ¿La cooperativa prioriza sus riesgos de deforestación con algún criterio de probabilidad e impacto (aunque sea informal), o los atiende sin un orden definido? | Opción múltiple | No se prioriza, se atiende lo que surge / Priorización informal, sin criterio escrito / Priorización estructurada con matriz probabilidad×impacto o similar |
| D5.19 | ¿Ha elaborado o participado en una declaración de diligencia debida / simplificada? | Opción múltiple | No sabe qué es / No pero lo entiende / En proceso / Presentada y aceptada |
| D5.19a | Del plan de gestión de riesgos de la cooperativa (si existe), marque los componentes que incluye explícitamente | Casillas de verificación | Plazos definidos / Recursos (humanos o financieros) asignados / Responsables designados / Procedimientos de consulta con socios y comunidades / Sistema de seguimiento y monitoreo / Protocolo ante incumplimiento de un socio / Atención diferenciada a productoras mujeres |
| D5.20 | ¿Existe responsable designado para el cumplimiento EUDR? | Opción múltiple | No / Función adicional / Dedicado |
| D5.21 | ¿Capacitación formal en los últimos 12 meses? | Opción múltiple | No / Hace más de 12 meses / Sí, reciente |
| D5.21a | ¿El plan de gestión de riesgos se revisa con una frecuencia definida (ej. anual, por campaña)? | Opción múltiple | No hay revisión definida / Revisión reactiva, sin frecuencia fija / Revisión periódica definida |
| D5.21b | ¿La cooperativa elabora y comunica un reporte de debida diligencia con indicadores (ej. % de producto trazado hasta finca, N.º de alertas tempranas detectadas, N.º de productores capacitados)? | Opción múltiple | No / Sí, uso interno solamente / Sí, interno y compartido con compradores u otras partes interesadas |

## Sección 8 — D6: Capacidad organizacional y digital

| # | Pregunta | Tipo de campo | Opciones |
|---|---|---|---|
| D6.22 | Presupuesto asignado al cumplimiento EUDR | Opción múltiple | No / Parcial, solo actividades de cumplimiento / Parcial, incluye tecnología y datos / Sí, con partida explícita para tecnología y datos |
| D6.22a | ¿La cooperativa cuenta con una base de datos o sistema centralizado (digital o no) que permite vincular a cada socio proveedor con sus parcelas geolocalizadas, los lotes que ha entregado y su volumen? | Opción múltiple | No existe / Existe en papel desorganizado / Existe digital pero sin vínculos entre tablas / Existe digital con vínculos actualizados entre socio-parcela-lote |
| D6.22b | *(Rama: solo si D6.22a ≠ "No existe" y ≠ "Existe en papel desorganizado")* ¿Qué tipo de sistema digital utiliza? | Opción múltiple | Excel o Access básico / Software especializado de trazabilidad (ChainPoint, Teia, BQuant, otro) / Sistema web propio o de tercero / Base de datos personalizada con soporte técnico regular |
| D6.23 | Digitalización de registros | Opción múltiple | Papel / Mixto / Digital |
| D6.24 | Conectividad a internet | Opción múltiple | No hay / Limitada / Confiable |
| D6.25 | ¿Ha gestionado apoyo externo para adecuarse? | Opción múltiple | No y lo necesita / No lo cree necesario / Sí en el pasado / Sí activo |
| D6.25a | ¿Los registros documentales de la cooperativa (actas, contratos con socios, guías de transporte, certificados, reportes de trazabilidad) se almacenan de forma segura —digital con respaldo o física en archivo— con capacidad de ser recuperados en menos de 48 horas si se pierden los originales? | Opción múltiple | No existe política de respaldo / Parcial, solo los más críticos / Sí, con respaldo definido pero no probado / Sí, con protocolo probado periódicamente |
| D6.25b | *(Rama: solo si D6.25a = "Sí, con respaldo definido pero no probado" o "Sí, con protocolo probado")* ¿El protocolo fue diseñado internamente o con apoyo externo? ¿Cuándo se probó por última vez? | Opción múltiple | Diseñado internamente / Con apoyo de ONG o programa / Con apoyo de consultoría o proveedor IT / Nunca se ha probado / Probado hace más de 12 meses / Probado en los últimos 12 meses |
| D6.22c | ¿Hay personal asignado a la gestión de datos y trazabilidad (aunque sea a medio tiempo)? | Opción múltiple | Sí, personal dedicado / Parcial, como función adicional / No / No sabe |

**Destino:** variable `personal_datos` del proxy; dimensión D6 (`ISCAM_Score!J`, vía `SCORECARDS!J`); componente CAPAC de `PONDERADORES!A15`.

## Sección 9 — D7: Cadena de valor

| # | Pregunta | Tipo de campo | Opciones |
|---|---|---|---|
| D7.26 | ¿El comprador ha exigido formalmente geolocalización/diligencia debida? | Opción múltiple | Aún no / Informalmente / Formalmente por escrito |
| D7.27 | ¿El comprador ofrece financiamiento/asistencia técnica condicionada al cumplimiento? | Opción múltiple | Sí / No |
| D7.28 | Riesgo percibido de perder el contrato si no cumple a tiempo | Opción múltiple | No sabe / Bajo / Medio / Alto |
| D7.28b | ¿El comprador europeo ha comunicado que sus propias obligaciones (EUDR, CSRD, CSDDD u otra) implican requisitos adicionales sobre la cadena de suministro más allá de la geolocalización? | Opción múltiple | No ha mencionado nada / Lo ha mencionado verbalmente sin requisito formal / Sí, ha enviado documentación o cuestionario de proveedores / Sí, lo ha formalizado como cláusula contractual |
| D7.28c | *(Rama: solo si D7.28b = "Sí, ha enviado documentación" o "Sí, lo ha formalizado como cláusula")* ¿Qué tipo de documentación ha enviado o solicitado el comprador? ¿Cubre solo a la cooperativa o también a sus proveedores? | Opción múltiple | Cuestionario de autoevaluación / Guía de diligencia debida propia del comprador / Plantilla de trazabilidad (lotes, volúmenes, GPS) / Evaluación de riesgo de deforestación / Requisito de certificación de terceros (Fairtrade, Rainforest, orgánica) / Solo cubre a la cooperativa / Cubre también a los proveedores directos / Cubre hasta proveedores de segundo nivel |
| D7.26a | ¿El comprador principal (primera mano) es una empresa de la Unión Europea o está sujeto a la Directiva de diligencia debida empresarial (CSDDD)? | Opción múltiple | Sí, empresa de la UE / No es de la UE pero está sujeto a CSDDD / No / No sabe |
| D7.26b | ¿Existe contrato o acuerdo escrito con el comprador principal que incluya cláusula de debida diligencia, geolocalización o trazabilidad? | Opción múltiple | Sí, con cláusula explícita EUDR o equivalente / Sí, pero sin cláusula específica / No hay contrato escrito / No sabe |

**Destino:** variables `comprador_ue` y `contrato_eudr` del proxy; dimensión D7 (`ISCAM_Score!K`); IV1 (`ISCAM_Score!U`) y componente PRESION de `PONDERADORES!A16`.

## Sección 10 — D8: Gobernanza y participación de socios

| # | Pregunta | Tipo de campo | Opciones |
|---|---|---|---|
| D8.29 | ¿Se han realizado asambleas o reuniones informativas sobre el EUDR dirigidas a los socios (no solo a la directiva)? | Escala lineal 0-4 | Misma leyenda que D2.5 |
| D8.30 | % estimado de socios que entienden, al menos en términos generales, por qué se les pide geolocalización/documentación | Respuesta corta (validación numérica 0-100) | — |
| D8.31 | ¿Existe algún mecanismo interno (incentivo o condición) para que los socios entreguen su información de parcela? | Opción múltiple | No existe / Se pide informalmente / Es requisito formal para vender a la cooperativa |
| D8.32 | Rotación de la directiva en los últimos 2 años | Opción múltiple | Alta / Moderada / Baja/estable |

## Sección 11 — D9: Sostenibilidad económica del cumplimiento

| # | Pregunta | Tipo de campo | Opciones |
|---|---|---|---|
| D9.33 | Estimación del costo total de adecuación (geolocalización, saneamiento, sistemas, capacitación) frente al presupuesto anual de la cooperativa | Opción múltiple | Costo mayor al 10% del presupuesto anual / Entre 3-10% / Menor al 3% / No se ha estimado |
| D9.34 | ¿Cómo ha financiado (o financiaría) la organización la adecuación al EUDR? | Opción múltiple | Con crédito o endeudamiento / Con recursos propios / Existe fuente de financiamiento identificada (verde, cooperación o programa público), aún no ejecutada / No ha sido necesario / No sabe |
| D9.35 | ¿Existe riesgo de que el costo de adecuación se traslade a un menor precio pagado al socio productor? | Opción múltiple | Sí, ya ha ocurrido / Es un riesgo latente / No aplica / No se ha evaluado |

## Sección 12 — D10: Confusión entre certificación voluntaria y cumplimiento EUDR

| # | Pregunta | Tipo de campo | Opciones |
|---|---|---|---|
| D10.36 | ¿La cooperativa cree que su certificación vigente (Rainforest Alliance, Fairtrade, Orgánico, etc.) ya cubre las obligaciones del EUDR? | Opción múltiple | Sí, totalmente / Sí, en parte / No, sabe que son cosas distintas / No tiene certificación |
| D10.37 | ¿Algún proveedor o consultor le ha ofrecido una "certificación EUDR" como producto? | Opción múltiple | Sí / No |
| D10.36a | ¿La organización ha recibido asesoría específica sobre el EUDR (a diferencia de asesoría genérica de sostenibilidad)? | Opción múltiple | Sí, asesoría especializada en EUDR / Solo asesoría genérica de sostenibilidad / No ha recibido asesoría / No sabe |

## Sección 13 — D11: Ecosistema de apoyo externo

| # | Pregunta | Tipo de campo | Opciones |
|---|---|---|---|
| D11.38 | Marque los actores con los que la cooperativa ya tiene contacto o apoyo activo | Casillas de verificación | SERFOR (legalidad forestal) / PNCB-MINAM (monitoreo satelital) / MIDAGRI o programa regional de café-cacao / Gobierno regional (catastro/saneamiento) / Cooperación internacional (GIZ, USAID, UE, ONG) / Junta Nacional del Café, APPCACAO u otro gremio / Ninguno |
| D11.39 | De los actores no marcados en la pregunta anterior, ¿cuáles conoce pero no ha contactado, y por qué? | Párrafo | — |
| D11.39a | ¿La organización está inscrita en una plataforma de trazabilidad del sector (APPCACAO, Junta Nacional del Café u otra equivalente)? | Opción múltiple | Sí / En proceso de inscripción / No / No conoce la plataforma |

---

## Sección 14 — D12–D15: Pacto Verde europeo (alimentan ISA-PV, 30% de ISA-Completo)

**Texto de encabezado de sección:** "Esta sección mide desempeño ambiental, no cumplimiento EUDR. Responda según el estado actual, aunque sea incipiente: 'en curso' es una respuesta válida."

| # | Pregunta | Tipo de campo | Opciones |
|---|---|---|---|
| D12.42 | ¿La organización mide o ha calculado la huella de carbono de su actividad productiva y de procesamiento (alcance 1 y 2)? | Opción múltiple | No mide (0) / Registra insumos o mide parcialmente, en curso (1) / Calculada y verificada por tercero (2) |
| D13.45 | ¿La organización elabora y publica un reporte de sostenibilidad con información de su desempeño ambiental y social? | Opción múltiple | No (0) / En preparación (1) / Publicado (2) |
| D14.51 | ¿La organización gestiona los residuos y subproductos del beneficio (compostaje, reutilización de agua, aprovechamiento de pulpa o cáscara, u otras prácticas de economía circular)? | Opción múltiple | No (0) / En transición, prácticas aisladas (1) / Avanzado, procesos establecidos (2) |
| D15.58 | ¿La organización monitorea residuos de plaguicidas (LMR) en su producto para asegurar el cumplimiento de los límites de la Unión Europea? | Opción múltiple | No verificado (0) / En monitoreo interno (1) / Cumple límites UE verificado (2) |

**Destino:** columnas `W` (D12.42), `X` (D13.45), `Y` (D14.51) y `Z` (D15.58) de `MATRIZ_174` — escala 0 = No / 1 = En curso o en transición / 2 = Certificado o verificado; de ahí a `ISCAM_Score!AE:AH` → `AI` (ISA-PV) → 30% de `AL` (ISA-Completo). Hoy esas cuatro columnas están en 0 para las 174 organizaciones.

**Nota de alcance:** estas 4 preguntas son la **versión mínima** (0/1/2) de los módulos Pacto Verde cuyos IDs ya están reservados en la Google Sheet (`D12.40–D12.44`, `D13.45–D13.50`, `D14.51–D14.55`, `D15.56–D15.60`). Activan hoy las columnas `W:Z` de `MATRIZ_174`; las 17 preguntas restantes de esos módulos quedan pendientes de evaluación de comprensibilidad con el técnico de campo (igual que D15.56/57/59/60) y no bloquean el cálculo del índice.

---

## Sección 15 — PPWR: Envases y packaging (Reglamento europeo de envases)

| # | Pregunta | Tipo de campo | Opciones |
|---|---|---|---|
| PP1 | ¿Qué tipo de sacos de exportación utiliza principalmente? | Opción múltiple | Yute reutilizable / Yute nuevo de un solo uso / Big-bag o saco plástico / Saco de papel / Otro (especificar) |
| PP2 | ¿Los sacos de exportación tienen certificación FSC o equivalente? | Opción múltiple | Sí / No / No sabe |

**Destino:** `SCORECARDS!M` (PPWR) y componente PPWR de `PONDERADORES!A18` (5% del índice PVE).

---

## Sección 16 — Bloque R: Indicadores PVE (columnas P1–P14 de `MATRIZ_174`)

**Texto de encabezado de sección:** "Esta sección alimenta el índice de Pacto Verde Europeo (PVE). Son datos de gestión; si no lleva registro, responda con su mejor estimación e indíquelo."

| # | Pregunta | Tipo de campo | Opciones |
|---|---|---|---|
| R1 | ¿Qué porcentaje aproximado de sus socios productores tiene acceso a crédito formal, fondo rotatorio o programa de financiamiento? | Respuesta corta (validación numérica 0-100) | — |
| R2 | ¿Qué porcentaje de los socios productores trabajadores está formalizado (contrato, planilla o aportación a seguridad social)? | Respuesta corta (validación numérica 0-100) | — |
| R3 | ¿Cuántas capacitaciones técnicas recibe en promedio cada socio productor al año? | Respuesta corta (numérica) | — |
| R4 | ¿Qué porcentaje de los socios que tenía hace 3 años siguen activos entregando producto a la organización? | Respuesta corta (validación numérica 0-100) | — |
| R5 | ¿Qué porcentaje del ingreso total de la organización proviene de productos distintos del café o cacao? | Respuesta corta (validación numérica 0-100) | — |
| R6 | ¿Qué porcentaje de su volumen se comercializa en mercados premium o con prima (certificado, especial, single origin u otro)? | Respuesta corta (validación numérica 0-100) | — |
| R7 | ¿Cuánto invirtió la organización en adecuación al EUDR en el último año? (especifique moneda: S/ o USD) | Respuesta corta | — |
| R8 | ¿Qué porcentaje de los reclamos o quejas formales de socios presentados en los últimos 2 años fueron resueltos? | Respuesta corta (validación numérica 0-100) | — |
| R9 | ¿Qué porcentaje de la energía que consume la organización (sede y planta de procesamiento) proviene de fuentes renovables? | Respuesta corta (validación numérica 0-100) | — |
| R10 | ¿Qué porcentaje de los residuos y subproductos del beneficio se gestionan con tratamiento (compostaje, reciclaje, biogás u otro)? | Respuesta corta (validación numérica 0-100) | — |

**Destino:** columnas `AC` (R1), `AE` (R2), `AF` (R3), `AG` (R4), `AH` (R5), `AI` (R6), `AJ` (R7), `AL` (R8), `AM` (R9) y `AN` (R10) de `MATRIZ_174`, que alimentan `AO` (P_Global). No se preguntan: P1 (productividad) y P2 (ingreso neto USD/ha) se derivan de P3 + B0.4; P4 procede de B0.12; P11 es la pregunta P11 de este Form.

---

## Notas de configuración por tipo de pregunta sensible

- **D2.10, D3.14i, D4.15a, D7.28 y D10.36 son banderas/excepciones** — en Google Forms no hay forma de marcar esto visualmente para el encuestado; dejar como pregunta normal, la bandera se aplica en el análisis posterior (ver nota de puntaje del Instrumento 2).
- **D5.19a y D11.38/D11.39 son de mapeo** — usar "Casillas de verificación" (permite 0, 1 o varias opciones), no "Opción múltiple" (fuerza una sola).
- **Preguntas con "(deje en blanco si no aplica)" (B0.6, P9)** — en Google Forms usar lógica condicional ("Ir a la sección basado en la respuesta") desde la pregunta anterior (B0.5 y P8 respectivamente) para saltarlas automáticamente, en vez de confiar en que el encuestados las deje vacías.
- Las preguntas de escala 0-4 deben mostrar la leyenda completa (`0 No existe/No sabe · 1 Informal o parcial · 2 En desarrollo · 3 Implementado · 4 Implementado y verificado/auditado`) como texto de ayuda bajo cada una — Google Forms permite "Descripción" por pregunta; pegar la leyenda ahí en las preguntas de escala (D2.5, D2.7, D3.13, D4.16, D5.18, D5.18a, D8.29).
- Las preguntas D12.42, D13.45, D14.51 y D15.58 (versión mínima del módulo Pacto Verde) usan escala de 3 niveles equiparable a 0 / 1 / 2 (columnas `W:Z` de `MATRIZ_174`); el valor ya está indicado entre paréntesis en cada opción.
- Ramas condicionales que deben configurarse con "Ir a la sección basado en la respuesta": B0.5 → B0.6; P8 → P9; D1.3 → D1.3a; D2.5a → D2.5b; D6.25a → D6.25b; D7.28b → D7.28c.

> **Total de preguntas en este Form (v0.4): 119** — 3 metadata + 17 Bloque 0 (B0.1–B0.17) + 15 Bloque P (P1–P14 + P1b) + 68 preguntas D1–D11 (incluye D1.3a, D2.5a/b, D3.14h/i, D4.15a, D6.22c, D7.26a/b, D10.36a, D11.39a) + 4 versión mínima Pacto Verde (D12.42, D13.45, D14.51, D15.58) + 2 PPWR (PP1–PP2) + 10 Bloque R (R1–R10).
> v0.4 cierra los huecos de correspondencia con `PLANTILLA_INDICE_PVE_ISCAM.xlsx` detectados en el análisis inverso: 13 variables del proxy sin pregunta, 4 columnas D12–D15 en cero, 10 indicadores PVE sin fuente, y campos de ficha (tipo de organización, departamento, RNCA). Las preguntas de módulo restantes (D12.40/41/43/44, D13.46–D13.50, D14.52–D14.55, D15.56/57/59/60) quedan pendientes de evaluación de comprensibilidad con el técnico de campo — ver protocolo en `DOC_TRABAJO_Instrumento2_ISCAM_v2.md` §10.2; la versión mínima ya activa las 4 columnas que alimentan ISA-PV.

---

## Anexo v0.4 — Correspondencia de preguntas nuevas y modificadas con `PLANTILLA_INDICE_PVE_ISCAM.xlsx`

| ID | Qué cambia | Destino en el índice |
|---|---|---|
| B0.8 | Modificada — destinos dentro y fuera de la UE, principal primero | Variable `destino_principal` del cuestionario de verificación rápida (D7); validación de países destino en `MATRIZ_174` |
| B0.15 | Nueva — tipo de organización | `MATRIZ_174!P` (Tipo org.); hoy usado como proxy de `ISCAM_Score!Y` (IV5) |
| B0.16 | Nueva — departamento de la sede | `MATRIZ_174!C` (validación cruzada SUNAT; alimenta `RADAR_BRECHAS`) |
| B0.17 | Nueva — inscrita en RNCA | `ISCAM_Score!V` (IV2 diseñado = RNCA); variable `rnca` del proxy |
| D1.3a | Nueva (rama de D1.3) — rol EUDR explícito | `ISCAM_Score!E` (D1) vía codificación D1.3 |
| D2.5a | Nueva — % volumen de proveedores externos | `ISCAM_Score!F` vía `SCORECARDS!H` (D2); variable `pct_ext` |
| D2.5b | Nueva (rama) — trazabilidad de proveedores externos | ídem + bandera D2.10; variable `traza_ext` |
| D3.12 | Modificada — opción ANP / zona de amortiguamiento | `ISCAM_Score!G` (D3); variable `anp` |
| D3.14h | Nueva — autorizaciones ambientales vigentes | `ISCAM_Score!G`; variable `aut_ambiental` |
| D3.14i | Nueva — sanción OEFA/SINEFA vigente | `MATRIZ_174!U` (reemplaza el score OSCE histórico, corte 2024-04); bandera `ISCAM_Score!AD`; `X` (IV4) |
| D4.15 | Modificada — precisa el cruce GEOSERFOR/PNCB/GFW | `ISCAM_Score!H` (D4); variable `cruce_deforest` |
| D4.15a | Nueva — alertas activas de deforestación | `ISCAM_Score!H`; `Q` (IP2 `√(D3×D4)`); variable `alerta_deforest` |
| D6.22 | Modificada — distingue partida de tecnología y datos | `ISCAM_Score!J` (D6); componente CAPAC (`PONDERADORES!A15`) |
| D6.22c | Nueva — personal asignado a datos | `ISCAM_Score!J`; variable `personal_datos` |
| D7.26a | Nueva — comprador UE / sujeto a CSDDD | `ISCAM_Score!K` (D7); `U` (IV1); variable `comprador_ue` |
| D7.26b | Nueva — contrato con cláusula de diligencia | `ISCAM_Score!K`; componente PRESION (`PONDERADORES!A16`); variable `contrato_eudr` |
| D9.34 | Modificada — fuente de financiamiento identificada | `ISCAM_Score!M` (D9); variable `financiamiento` |
| D10.36a | Nueva — asesoría EUDR específica | `ISCAM_Score!N` (D10); variable `asesoria_eudr` |
| D11.39a | Nueva — plataforma de trazabilidad APPCACAO/JNC | `ISCAM_Score!O` (D11); variable `plataforma_traz` |
| D12.42 | Nueva — huella de carbono medida (versión mínima del módulo D12; D12.40/41/43/44 pendientes) | `MATRIZ_174!W` → `ISCAM_Score!AE` → `AI` (ISA-PV) → 30% de `AL` |
| D13.45 | Nueva — reporte de sostenibilidad (versión mínima del módulo D13; D13.46–D13.50 pendientes) | `MATRIZ_174!X` → `AF` → `AI` |
| D14.51 | Nueva — gestión de residuos del beneficio (versión mínima del módulo D14; D14.52–D14.55 pendientes) | `MATRIZ_174!Y` → `AG` → `AI` |
| D15.58 | Nueva — monitoreo LMR/fitosanitario (versión mínima del módulo D15; D15.56/57/59/60 pendientes) | `MATRIZ_174!Z` → `AH` → `AI` |
| PP1 | Nueva — tipo de saco de exportación | `SCORECARDS!M` (PPWR); `PONDERADORES!A18`; variable `tipo_saco` |
| PP2 | Nueva — saco con certificación FSC | ídem; variable `fsc` |
| R1 | Nueva — % socios con acceso a crédito | `MATRIZ_174!AC` (P3) → `AO` (P_Global) |
| R2 | Nueva — % socios formalizados | `MATRIZ_174!AE` (P5) |
| R3 | Nueva — capacitaciones por socio al año | `MATRIZ_174!AF` (P6) |
| R4 | Nueva — % retención de socios | `MATRIZ_174!AG` (P7) |
| R5 | Nueva — % diversificación de ingresos | `MATRIZ_174!AH` (P8) |
| R6 | Nueva — % mercados premium | `MATRIZ_174!AI` (P9) |
| R7 | Nueva — inversión EUDR USD/año | `MATRIZ_174!AJ` (P10) |
| R8 | Nueva — % reclamos de socios resueltos | `MATRIZ_174!AL` (P12) |
| R9 | Nueva — % energía renovable | `MATRIZ_174!AM` (P13) |
| R10 | Nueva — % residuos gestionados | `MATRIZ_174!AN` (P14) |

**Con este anexo, las 36 variables del proxy quedan cubiertas** (17 ya lo estaban, 6 por fusión en preguntas existentes, 13 por preguntas nuevas). Pendiente fuera del Form: hoja de codificación 0-4 → 0-100 y hoja de ingesta con join por RUC, que hoy no existen en la Plantilla.
