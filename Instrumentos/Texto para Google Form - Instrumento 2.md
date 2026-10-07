# Texto para Google Form — Instrumento 2 (76 preguntas)

**Tarea:** Fase 1, Plan de Trabajo 75 días — "Construir el Google Form de Instrumento 2". El asistente no puede crear el Form directamente (requiere acceso a Google Forms); este documento deja listo el texto exacto, pregunta por pregunta, tipo de campo y opciones, para que se cargue en ~30–45 minutos de trabajo manual (o se pegue vía un complemento de importación masiva tipo "Form Builder from Spreadsheet").

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
| B0.8 | País(es) de destino dentro de la UE | Casillas de verificación | Alemania / Bélgica / Países Bajos / Francia / Italia / España / Suecia / Dinamarca / Otro (especificar) |
| B0.9 | Certificaciones voluntarias vigentes | Casillas de verificación | Rainforest Alliance / Fairtrade / Orgánico / UTZ / Otra / Ninguna |
| B0.10 | ¿Las parcelas de los socios están concentradas en un solo distrito, repartidas en varios distritos de una misma provincia, o dispersas en varias provincias/regiones? | Opción múltiple | Un solo distrito / Varios distritos, misma provincia / Varias provincias o regiones |
| B0.11 | Distancia aproximada entre las parcelas más alejadas de los socios y el centro de acopio o planta de procesamiento más cercano | Opción múltiple | Menos de 5 km / Entre 5 y 20 km / Entre 20 y 50 km / Más de 50 km / No se ha medido |
| B0.12 | % de mujeres en la directiva/consejo directivo | Respuesta corta (validación numérica 0-100) | — |

---

## Sección 2 — Bloque P: Variables de Performance

**Texto de encabezado de sección:** "Esta sección mide resultados de negocio, no madurez de cumplimiento. Las preguntas que piden una cifra de hace 3 años son un recuerdo aproximado, no un dato verificado — tómelo como referencia, no como registro exacto."

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

---

## Sección 3 — D1: Clasificación regulatoria

| # | Pregunta | Tipo de campo | Opciones |
|---|---|---|---|
| D1.1 | ¿La cooperativa introduce el producto directamente en el mercado de la UE bajo su propio nombre? | Opción múltiple | Sí / No |
| D1.2 | ¿Transforma el producto (trilla, tostado, fermentado, aserrío) antes de venderlo? | Opción múltiple | Transforma / No transforma |
| D1.3 | ¿Sabe con certeza qué rol le corresponde (operador, operador posterior, comerciante, micro/pequeño operador primario)? | Opción múltiple | Sí con certeza / Idea aproximada / No sabe |
| D1.4 | ¿Cumple los umbrales de microempresa/pequeña empresa (Directiva 2013/34/UE)? | Opción múltiple | Sí / No / No sabe |

## Sección 4 — D2: Trazabilidad y geolocalización

| # | Pregunta | Tipo de campo | Opciones |
|---|---|---|---|
| D2.5 | ¿Existe registro de geolocalización (GPS/polígono) por parcela de socio? | Escala lineal 0-4 | 0 = No existe/No sabe … 4 = Implementado y verificado/auditado |
| D2.6 | % de socios con parcela geolocalizada | Respuesta corta (validación numérica 0-100) | — |
| D2.7 | ¿El sistema vincula un lote exportado con la(s) parcela(s) específica(s)? | Escala lineal 0-4 | Misma leyenda que D2.5 |
| D2.8 | ¿Quién levantó la información de geolocalización? | Opción múltiple | Técnico propio / Consultor / Proyecto de cooperación / Socio por su cuenta / No se ha levantado |
| D2.9 | Frecuencia de actualización de la geolocalización | Opción múltiple | Nunca / Al ingreso del socio / Anual / Por cosecha |
| D2.10 | ¿Existe algún punto en el proceso de acopio o beneficio donde se mezclan físicamente lotes de distinto origen sin registro de qué parcelas los componen? | Opción múltiple | Sí, se mezclan sin control / Se mezclan pero con registro de origen / No, se mantiene segregación física completa |

## Sección 5 — D3: Legalidad de la producción

| # | Pregunta | Tipo de campo | Opciones |
|---|---|---|---|
| D3.11 | % de socios con título de propiedad o posesión reconocida legalmente | Respuesta corta (validación numérica 0-100) | — |
| D3.12 | ¿Hay parcelas superpuestas a áreas protegidas, reservas comunales o territorios indígenas sin sanear? | Opción múltiple | Sí extensa / Sí puntual / No verificado / No, ninguna |
| D3.13 | ¿Se verifica cumplimiento laboral (no trabajo infantil, seguridad social) a nivel de finca? | Escala lineal 0-4 | Misma leyenda que D2.5 |
| D3.14 | ¿Alguna parcela de socios se ubica en una zona de desarrollo alternativo (ex-cultivo de coca) o con antecedentes de conflicto social/territorial? | Opción múltiple | Sí / No / No verificado |
| D3.14a | ¿Los socios cuentan con autorización de uso de agua para su actividad productiva, cuando corresponde? | Opción múltiple | Sí, todas las fuentes verificadas / Parcialmente / No / No aplica |
| D3.14b | ¿El tratamiento de aguas residuales del beneficio/procesamiento cumple con lo exigido por la autoridad ambiental? | Opción múltiple | Siempre / A veces / No / No aplica |
| D3.14c | ¿Alguna parcela de socios se encuentra dentro de la faja marginal de un río, quebrada, lago o laguna? | Opción múltiple | Sí / No / No sabe |
| D3.14d | En las parcelas de los socios y en el inmueble donde opera la cooperativa, ¿existe algún derecho de terceros (carga, embargo, servidumbre, usufructo, arrendamiento o derecho de uso consuetudinario) que condicione o restrinja el uso de la tierra para cultivar café o cacao, o el derecho de la cooperativa a operar en esa finca? | Opción múltiple | No existe ningún derecho de terceros / Existe, pero está registrado y no restringe el uso / Existe un acuerdo documentado con el titular o con la autoridad que legitima el uso, aunque la cooperativa o el socio no tenga título formal / Existe usufructo, arrendamiento o carga sin acuerdo que lo resuelva / Se han invocado derechos de uso tradicional o consuetudinarios por una comunidad o pueblo indígena sin proceso de acuerdo / No verificado |
| D3.14e | ¿La cooperativa y sus socios están al día en sus obligaciones tributarias, aduaneras y comerciales vinculadas a la actividad exportadora? | Opción múltiple | Sí, verificado / Parcialmente / No verificado / No sabe |
| D3.14f | ¿Existen políticas o mecanismos internos contra la corrupción (código de conducta, canal de denuncias) aplicables a la cadena de abastecimiento? | Opción múltiple | Sí, formalizado / Informal / No existe |
| D3.14g | Cuando corresponde (parcelas de socios en territorio de comunidades indígenas, nativas o campesinas), ¿se ha realizado un proceso de Consentimiento Libre, Previo e Informado (CLPI)? | Opción múltiple | Sí, proceso documentado / Aplica pero no se ha realizado / No aplica, no hay territorios de este tipo / No sabe |

## Sección 6 — D4: Riesgo de deforestación

| # | Pregunta | Tipo de campo | Opciones |
|---|---|---|---|
| D4.15 | ¿Se verificó cambio de uso de suelo posterior al 31 de diciembre de 2020? | Opción múltiple | No verificado / Verificación parcial / Verificado sin hallazgos / Casos detectados sin resolver / Verificado sistemáticamente y documentado |
| D4.16 | ¿Usa herramientas de monitoreo satelital (Global Forest Watch, plataformas nacionales)? | Escala lineal 0-4 | Misma leyenda que D2.5 |
| D4.17 | ¿Conoce la clasificación de riesgo (bajo/estándar/alto) de su zona? | Opción múltiple | Sí documentado / Idea aproximada / No sabe |

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
| D6.22 | Presupuesto asignado para cumplimiento EUDR | Opción múltiple | No / Parcial / Sí |
| D6.23 | Digitalización de registros | Opción múltiple | Papel / Mixto / Digital |
| D6.24 | Conectividad a internet | Opción múltiple | No hay / Limitada / Confiable |
| D6.25 | ¿Ha gestionado apoyo externo para adecuarse? | Opción múltiple | No y lo necesita / No lo cree necesario / Sí en el pasado / Sí activo |

## Sección 9 — D7: Cadena de valor

| # | Pregunta | Tipo de campo | Opciones |
|---|---|---|---|
| D7.26 | ¿El comprador ha exigido formalmente geolocalización/diligencia debida? | Opción múltiple | Aún no / Informalmente / Formalmente por escrito |
| D7.27 | ¿El comprador ofrece financiamiento/asistencia técnica condicionada al cumplimiento? | Opción múltiple | Sí / No |
| D7.28 | Riesgo percibido de perder el contrato si no cumple a tiempo | Opción múltiple | No sabe / Bajo / Medio / Alto |

## Sección 10 — D8: Gobernanza interna y apropiación de los socios

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
| D9.34 | ¿La cooperativa ha financiado la adecuación con deuda? | Opción múltiple | Sí / No / No ha sido necesario |
| D9.35 | ¿Existe riesgo de que el costo de adecuación se traslade a un menor precio pagado al socio productor? | Opción múltiple | Sí, ya ha ocurrido / Es un riesgo latente / No aplica / No se ha evaluado |

## Sección 12 — D10: Confusión entre certificación voluntaria y cumplimiento EUDR

| # | Pregunta | Tipo de campo | Opciones |
|---|---|---|---|
| D10.36 | ¿La cooperativa cree que su certificación vigente (Rainforest Alliance, Fairtrade, Orgánico, etc.) ya cubre las obligaciones del EUDR? | Opción múltiple | Sí, totalmente / Sí, en parte / No, sabe que son cosas distintas / No tiene certificación |
| D10.37 | ¿Algún proveedor o consultor le ha ofrecido una "certificación EUDR" como producto? | Opción múltiple | Sí / No |

## Sección 13 — D11: Ecosistema de apoyo externo

| # | Pregunta | Tipo de campo | Opciones |
|---|---|---|---|
| D11.38 | Marque los actores con los que la cooperativa ya tiene contacto o apoyo activo | Casillas de verificación | SERFOR (legalidad forestal) / PNCB-MINAM (monitoreo satelital) / MIDAGRI o programa regional de café-cacao / Gobierno regional (catastro/saneamiento) / Cooperación internacional (GIZ, USAID, UE, ONG) / Junta Nacional del Café, APPCACAO u otro gremio / Ninguno |
| D11.39 | De los actores no marcados en la pregunta anterior, ¿cuáles conoce pero no ha contactado, y por qué? | Párrafo | — |

---

## Notas de configuración por tipo de pregunta sensible

- **D2.10, D7.28, D10.36 son banderas/excepciones** — en Google Forms no hay forma de marcar esto visualmente para el encuestado; dejar como pregunta normal, la bandera se aplica en el análisis posterior (ver nota de puntaje del Instrumento 2).
- **D5.19a y D11.38/D11.39 son de mapeo** — usar "Casillas de verificación" (permite 0, 1 o varias opciones), no "Opción múltiple" (fuerza una sola).
- **Preguntas con "(deje en blanco si no aplica)" (B0.6, P9)** — en Google Forms usar lógica condicional ("Ir a la sección basado en la respuesta") desde la pregunta anterior (B0.5 y P8 respectivamente) para saltarlas automáticamente, en vez de confiar en que el encuestado las deje vacías.
- Las preguntas de escala 0-4 deben mostrar la leyenda completa (`0 No existe/No sabe · 1 Informal o parcial · 2 En desarrollo · 3 Implementado · 4 Implementado y verificado/auditado`) como texto de ayuda bajo cada una — Google Forms permite "Descripción" por pregunta; pegar la leyenda ahí en las 8 preguntas de escala (D2.5, D2.7, D3.13, D4.16, D5.18, D5.18a, D8.29).
