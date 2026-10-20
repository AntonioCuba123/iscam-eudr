# Instrumento 2 — Encuesta Cuantitativa de Alineamiento al Pacto Verde Europeo

**Cooperativas exportadoras de café y cacao, Perú**

Oct 12, 2026 · Grupo ISCAM – CIUP

Documento de trabajo · versión 0.3 — actualizada según recomendaciones DT-ISCAM-001 §7 (IP4, IV3, D15)

---

**Resumen.** Este documento describe el diseño, la arquitectura y la cobertura temática del Instrumento 2, la encuesta cuantitativa del toolkit de diagnóstico EUDR del proyecto *El impacto del Pacto Verde Europeo en el desempeño de las cooperativas peruanas* (ISCAM, Universidad del Pacífico). El instrumento opera sobre **95 preguntas** (antes 89: +2 preguntas nuevas B0-13 y B0-14 para IV3; +2 preguntas nuevas Q22a y Q25a para IP4; +2 ramales condicionales Q22b y Q25b para profundizar la capacidad digital en organizaciones avanzadas) organizadas en 15 dimensiones (D1–D15) más un bloque de variables de resultado (Bloque P), y produce dos sub-índices separables: el ISA-EUDR, que mide madurez regulatoria frente al Reglamento (UE) 2023/1115, y el ISA-PactoVerde, que mide alineamiento competitivo con las cuatro estrategias del Pacto Verde con mayor impacto operativo para el sector —huella de carbono, reporte de sostenibilidad, economía circular y gestión fitosanitaria/LMR. El documento expone la lógica de diseño de cada dimensión, las decisiones de alcance tomadas con argumentos verificables, las cuatro preguntas que actúan como banderas no compensables, y el mapa completo del instrumento con opciones de respuesta, referencia normativa y rol en el índice. Se concluye que el instrumento cubre las dos vías por las que el Pacto Verde afecta a una cooperativa exportadora peruana —el acceso legal al mercado y la competitividad de largo plazo—, y que la separación entre ISA-EUDR e ISA-PactoVerde es una condición de diseño necesaria para que el diagnóstico produzca recomendaciones diferenciadas, no una elección cosmética.

**Palabras clave:** EUDR, Pacto Verde Europeo, cooperativas cafetaleras, cooperativas cacaoteras, Perú, índice de alineamiento, ISA, diligencia debida, trazabilidad, LMR, Farm to Fork, CSRD.

> **Nota sobre cambios v0.3 (2026-10-12).** Las cuatro preguntas nuevas responden a tres recomendaciones del documento de trabajo DT-ISCAM-001 (versión 4.0): **(1) IP4 tiene solo 2 ítems** — se agregan Q22a y Q25a para fortalecer la sub-dimensión de información y documentación; **(2) IV3 tiene cobertura territorial insuficiente** — se agregan B0-13 y B0-14 al Bloque 0 para capturar dispersión por zona de riesgo y capacidad de verificación de campo; **(3) D15.Q56–Q60 requiere evaluación de comprensibilidad en piloto** — añadida nota de evaluación en la introducción de D15. Ningún cambio altera fórmulas de índice ni puntajes existentes.

---

## 1. Introducción

El Reglamento (UE) 2023/1115 sobre productos libres de deforestación —conocido como EUDR— convierte la trazabilidad del café y el cacao exportados a Europa en una condición obligatoria de acceso al mercado a partir del 30 de diciembre de 2026, fecha fijada por el Reglamento (UE) 2025/2650 tras tres postergaciones previas. Pero el EUDR es solo uno de los instrumentos del Pacto Verde Europeo que afectan a una cooperativa exportadora peruana: los Límites Máximos de Residuos de pesticidas establecidos por la Directiva 2009/128/CE y monitoreados por el sistema RASFF pueden bloquear un lote en frontera con el mismo efecto comercial que un rechazo por deforestación; la Directiva (UE) 2024/1760 sobre diligencia debida corporativa traslada obligaciones de sus propios compradores europeos hacia la cadena de suministro peruana; y los requerimientos de reporte ESG derivados de la Directiva (UE) 2022/2464 (CSRD) condicionan ya hoy el acceso a financiamiento verde y la preferencia de compradores que deben reportar su huella de cadena.

El Instrumento 2 es la encuesta cuantitativa diseñada para operacionalizar este diagnóstico en una muestra de 100–150 organizaciones. Su objetivo es doble: producir un índice de preparación regulatoria ante el EUDR que oriente la priorización de asistencia técnica, y medir el alineamiento más amplio con el Pacto Verde para responder al objetivo (f) del proyecto madre —cuantificar el impacto de esa adecuación sobre el desempeño de las cooperativas.

La sección 2 encuadra los pilares del Pacto Verde con impacto verificable para este sector. La sección 3 describe la arquitectura del instrumento y el sistema de índices. La sección 4 presenta la matriz completa con opciones de respuesta, referencia normativa y rol en el índice. La sección 5 documenta las decisiones de alcance y los elementos evaluados que quedaron fuera. La sección 6 describe las cuatro banderas no compensables. La sección 7 introduce el Bloque P. La sección 8 provee la guía de llenado, y la sección 9 cierra con un glosario de acrónimos con fuentes.

---

## 2. El Pacto Verde Europeo y su relevancia para cooperativas exportadoras de café y cacao

El Pacto Verde Europeo no es un instrumento único sino un conjunto de estrategias y reglamentos con calendarios de implementación distintos (Comisión Europea, 2019). Para las cooperativas peruanas de café y cacao, la relevancia no es uniforme entre pilares: algunos generan obligaciones legales cuyo incumplimiento bloquea el acceso al mercado de forma directa e inmediata; otros crean presión competitiva de largo plazo a través de los compradores europeos o del acceso a financiamiento. Confundirlos —o tratar la preparación como un continuo único— produce recomendaciones incorrectas.

La Tabla 1 sistematiza los pilares con impacto real y verificable para este sector, junto con la dimensión del Instrumento 2 que los operacionaliza.

**Tabla 1**
*Pilares del Pacto Verde Europeo con impacto para cooperativas exportadoras de café y cacao peruanas*

| Pilar | Instrumento normativo | Impacto concreto para la cooperativa | Dimensión en Instrumento 2 | Tipo de obligación |
|---|---|---|---|---|
| Deforestación / trazabilidad | Reglamento (UE) 2023/1115, mod. 2025/2650 | Sin declaración de diligencia debida con geolocalización verificada → el producto no entra al mercado UE desde el 30 dic. 2026 | D1–D9 | Legal — acceso al mercado |
| Fitosanitarios / LMR | Directiva 2009/128/CE; sistema RASFF | Un lote rechazado en frontera por exceso de residuos de pesticidas tiene el mismo efecto comercial que un rechazo por deforestación: pérdida del lote y del comprador | D15 | Legal + competitividad |
| Presión CSDDD del comprador | Directiva (UE) 2024/1760 | El comprador europeo tiene obligación propia de diligencia debida sobre su cadena de suministro y traslada requisitos adicionales de forma contractual | D7.Q28b; P13 | Legal + competitividad |
| Huella de carbono / GEI | Taxonomía UE (Regl. 2020/852); CSRD | Compradores europeos y fondos de inversión sostenible exigen datos de huella. Para café: CalCafé v2.1 (PromPerú/PUCP-PELCAN) disponible y validado. Para cacao: sin herramienta nacional equivalente | D12 | Competitividad |
| Reporte de sostenibilidad (ESG) | Directiva (UE) 2022/2464 (CSRD); ESRS | El comprador europeo debe reportar su huella de cadena bajo CSRD y necesita datos ESG de sus proveedores para cumplir | D13 | Competitividad |
| Economía circular / envases | Reglamento (UE) 2025/40 (PPWR); Plan Acción EC UE 2020 | Requisitos de reciclabilidad de envases de exportación y gestión de residuos del beneficio | D14 | Competitividad |
| Financiamiento verde | Taxonomía UE (Regl. 2020/852); SFDR (Regl. 2019/2088) | El acceso a crédito de impacto o fondos climáticos condiciona la elegibilidad a criterios de sostenibilidad del Pacto Verde | P14 | Competitividad |

*Nota.* Se omiten el CBAM (Regl. 2023/956, no aplica a café ni cacao — los sectores cubiertos son acero, cemento, aluminio, fertilizantes, hidrógeno y electricidad) y la conservación de biodiversidad forestal del Art. 2(40)(c) del EUDR (solo legislación pertinente cuando se relaciona directamente con la cosecha de madera; café y cacao no son productos madereros). Estas son decisiones de alcance documentadas, no omisiones; ver sección 5.

La distinción que estructura el instrumento nace de esta tabla. El acceso legal al mercado se juega en D1–D9 (EUDR) y en D15 (LMR): ambas son condiciones de entrada, no de competitividad. El alineamiento competitivo de largo plazo se juega en D12–D14 y en las señales que provienen del comprador (D7.Q28b, P13, P14). Un instrumento que promediara estas dos familias en un solo índice produciría diagnósticos incorrectos: una cooperativa con trazabilidad completa pero sin gestión de huella de carbono tiene un perfil completamente distinto —y requiere recomendaciones completamente distintas— que una cooperativa con buen reporte ESG pero sin geolocalización de sus socios.

---

## 3. Arquitectura del Instrumento 2

### 3.1 Estructura general

El instrumento opera sobre 90 preguntas distribuidas en cuatro bloques. La Tabla 2 resume la estructura.

**Tabla 2**
*Estructura del Instrumento 2 (versión D1–D15 + Bloque P v0.3)*

| Bloque | Descripción | N.º ítems | Entra al índice |
|---|---|---|---|
| Bloque 0 | Ficha de identificación | **14** (antes 12: +B0-13 IV3-territorio, +B0-14 IV3-verificación) | No — contexto e insumos IV/IP |
| D1–D11 | Dimensiones EUDR (núcleo + extendidas) | **60** (v0.4: +Q22a, Q25a, Q22b, Q25b para IP4; +Q28c para D7; +Q36a para D10, 2026-10-15) | ISA-EUDR (D1–D9); bandera (D10); inventario (D11) |
| D12–D15 | Módulos Pacto Verde | 21 | ISA-PactoVerde |
| Bloque P | Variables de desempeño | 14 | No — variable de resultado |
| **Total** | | **94** | |

### 3.2 Escala de madurez

Todas las preguntas de escala usan una escala ordinal 0–4 inspirada en la lógica del Capability Maturity Model Integration (CMMI) de Carnegie Mellon (Chrissis et al., 2011): los niveles no son intercambiables, cada uno presupone que el anterior está resuelto. Una respuesta de 3 sin evidencia de haber transitado los niveles 1 y 2 no es admisible como respuesta honesta. Esta propiedad ordinal es lo que hace a la escala adecuada para este instrumento: el EUDR no admite cumplimiento parcial compensado —o la parcela está geolocalizada o no lo está—, y la escala reproduce esa lógica en el diagnóstico.

**Tabla 3**
*Escala de madurez del Instrumento 2*

| Nivel | Descripción |
|---|---|
| **0** | No existe / No sabe |
| **1** | Informal o parcial |
| **2** | En desarrollo |
| **3** | Implementado |
| **4** | Implementado y verificado/auditado |

### 3.3 Sistema de índices

El instrumento alimenta tres índices. Su construcción sigue el proceso de ocho pasos del *OECD/JRC Handbook on Constructing Composite Indicators* (Nardo et al., 2008), referencia estándar de Eurostat y el Banco Mundial para este tipo de índice.

```
ISA-EUDR (submódulos ii + iii del proyecto madre)
  ├── Núcleo (D1–D7): media geométrica → 87.5% del ISA-EUDR
  └── Extendido (D8–D9): media aritmética → 12.5% del ISA-EUDR

ISA-PactoVerde (módulos i + iv + v + vi del proyecto madre)
  ├── D12 — Huella de carbono (módulo i)
  ├── D13 — Reporte de sostenibilidad (módulo iv)
  ├── D14 — Economía circular/envases (módulo v)
  └── D15 — Fitosanitarios/LMR (módulo vi)
       → media aritmética: (D12 + D13 + D14 + D15) / 4

ISA-Completo = 0.70 × ISA-EUDR + 0.30 × ISA-PactoVerde
```

La elección de media geométrica para el núcleo EUDR no es arbitraria: las dimensiones D1–D7 no son sustitutos entre sí en ningún sentido regulatorio — el Reglamento (UE) 2023/1115 exige simultáneamente geolocalización *y* declaración de diligencia debida *y* legalidad de la producción; cumplir dos de las tres no salva el tercer incumplimiento. La media geométrica castiga este desbalance porque un cero en cualquier dimensión reduce fuertemente el resultado final, de la misma manera que el PNUD cambió el IDH de media aritmética a geométrica en 2010 exactamente por esta razón (UNDP, 2010). Las dimensiones extendidas D8–D9 son moduladoras de la sostenibilidad del cumplimiento —no determinan el acceso al mercado por sí solas—, por lo que se agregan aritméticamente para evitar que un cero en gobernanza interna anule un índice EUDR que sí tiene las condiciones técnicas resueltas.

La media aritmética para D12–D15 refleja que los módulos del Pacto Verde son complementarios entre sí pero no tienen entre ellos la relación de prerequisito estricta que sí existe entre las dimensiones EUDR: una cooperativa sin gestión de huella de carbono puede tener plena trazabilidad de lotes, y ese no es un escenario de incumplimiento del reglamento.

Los pesos 70/30 del ISA-Completo reflejan que el acceso inmediato al mercado lo decide el EUDR (D1–D9), mientras que la competitividad de largo plazo depende del Pacto Verde completo. Estos pesos se validarán mediante análisis de sensibilidad en el piloto (Greco et al., 2019; ver `ISCAM/Metodologia - Indice de Alineamiento (ISA) y Marco Muestral.md` §4).

### 3.4 Dimensiones fuera del ISA

Tres dimensiones operan con una lógica distinta al semáforo de madurez y, por esa razón, no promedian en ninguno de los sub-índices.

**D10 — Confusión certificación/EUDR.** Una respuesta "Sí, totalmente cubierto" en Q36 es la peor señal posible, no la mejor: indica que la cooperativa no está actuando porque cree erróneamente que su certificación voluntaria la exime. El Art. 30 del Reglamento (UE) 2023/1115 es explícito en que un esquema de certificación puede informar la evaluación de riesgo, pero no sustituye la geolocalización ni la declaración de diligencia debida. Promediar D10 como madurez introduciría un incentivo perverso en el diagnóstico.

**D11 — Ecosistema de apoyo.** Esta dimensión no mide qué tan preparada está la cooperativa sino a qué actores tiene acceso para resolver sus brechas. Su salida es un inventario de cobertura —actores ya contactados, actores conocidos no contactados, actores desconocidos—, que alimenta directamente la columna "oportunidad" de la Matriz de Brechas (Instrumento 4). Agregarlo como puntaje de madurez confundiría preparación con conectividad institucional, dos fenómenos que requieren intervenciones distintas.

**IP4 — Información y documentación (actualizado en v0.3).** Antes de la versión 0.3, IP4 se sustentaba únicamente en D6.23 (digitalización de registros) y D2.9 (frecuencia de actualización de geolocalización) — dos preguntas que miden aspectos parciales de la capacidad de generar y almacenar evidencia. A partir de v0.3, se agregan Q22a (base de datos centralizada socio-parcela-lote) y Q25a (respaldo y seguridad de archivos documentales), Ilevando IP4 a cuatro preguntas que cubren de forma más completa la capacidad de producir evidencia verificable bajo requerimiento del EUDR o de un comprador. Las cuatro preguntas se promedian con igual peso en IP4. Q22b (tipo de sistema digital) y Q25b (origen y prueba del protocolo de respaldo) son ramales condicionales: se aplican solo a organizaciones que declararon tener un sistema digital (Q22a ≠ "No existe" / "Existe en papel desorganizado") o un protocolo definido (Q25a = penúltimo o último nivel), y no pesan en el índice — alimentan el perfil cualitativo de la cooperativa.

**D15.Q60 — Rechazo en frontera por LMR.** Una respuesta afirmativa en esta pregunta (rechazo real de un lote por exceso de residuos de pesticidas) se reporta siempre por separado, independientemente del puntaje promedio de D15. El mismo criterio aplica a D2.Q10 (mezcla física de lotes sin control): ambas son banderas cuya presencia no puede ser compensada por ningún puntaje alto en las preguntas restantes de su dimensión. La justificación de cada bandera se detalla en la sección 6.

### 3.5 Conexión con los índices IP/IV/RE del proyecto madre

Las preguntas de D1–D9 alimentan también los índices del proyecto madre ISCAM. El **IP (Índice de Preparación)** remapea D1–D9 en cinco sub-dimensiones de capacidad operativa. El **IV (Índice de Vulnerabilidad)** reutiliza el Bloque 0 —dependencia del mercado europeo, dispersión territorial— y D9 —costo de adecuación— como insumos de sus cinco sub-dimensiones de exposición estructural. El **RE (Riesgo de Exclusión)** combina ambos bajo la fórmula RE = IV × (1 − IP/100), cuantificando la probabilidad de que una brecha de preparación se traduzca en pérdida efectiva de acceso al mercado. El detalle matemático de este remapeo vive en `ISCAM/Remapeo D1-D9 a Indice de Preparacion (IP-ISCAM).md` y `ISCAM/Diseno - Indice de Vulnerabilidad (IV-ISCAM).md`.

---

## 4. Matriz completa del instrumento

La Tabla 4 presenta las 89 preguntas del instrumento con sus opciones de respuesta, referencia normativa, tipo de variable, rol en el índice y tipo de obligación. Las dimensiones aparecen en el orden en que se aplican.

**Leyenda de columnas**

- **Estrategia PV:** pilar del Pacto Verde al que responde la pregunta
- **Tipo:** escala 0–4 · porcentaje · binaria · ordinal · mapeo · numérica · texto libre
- **Rol:** ISA-EUDR · ISA-PactoVerde · bandera · inventario · variable resultado · contexto/IV
- **Obligación:** Legal (acceso al mercado) · Competitividad (largo plazo) · Ambas

---

**Tabla 4**
*Matriz completa del Instrumento 2 — Bloque 0: Ficha de identificación (no puntúa)*

| # | Pregunta | Opciones de respuesta | Estrategia PV | Tipo | Rol | Obligación |
|---|---|---|---|---|---|---|
| B0-1 | Nombre de la cooperativa / razón social | Texto | — | Texto libre | Contexto | — |
| B0-2 | RUC | Número | — | Numérica | Deduplicación marco muestral | — |
| B0-3 | Producto(s) exportado(s) + código SA | Café / Cacao / Madera / Otro | EUDR | Categórica múltiple | Contexto / estrato de cuota | Legal |
| B0-4 | N.º de socios productores / hectáreas totales | Número | EUDR | Numérica | Contexto / IV tamaño | Legal |
| B0-5 | ¿Exporta directamente a la UE o a través de tercero? | Directamente / A través de tercero | EUDR | Binaria | Contexto / D1 | Legal |
| B0-6 | Si indirecto: ¿quién es el comprador que exporta a la UE? | Texto libre | EUDR | Texto libre | Contexto / D7 | Legal |
| B0-7 | Volumen anual aproximado destinado a la UE (% del total) | % estimado | EUDR | Porcentaje estimado | IV1 dependencia de mercado | Legal |
| B0-8 | País(es) de destino dentro de la UE | Texto libre | EUDR | Texto libre | Contexto | Legal |
| B0-9 | Certificaciones voluntarias vigentes | Rainforest Alliance / Fairtrade / Orgánico / UTZ / Otra / Ninguna | EUDR | Categórica múltiple | IP5 — conteo 0/33/66/100 (no D10, que es bandera) | Competitividad |
| B0-10 | Dispersión geográfica de los socios | Un solo distrito / Varios distritos, misma provincia / Varias provincias o regiones | EUDR | Ordinal 3 niveles | IV3 fragilidad territorial | Legal |
| B0-11 | Distancia entre parcelas más alejadas y acopio | Menos de 5 km / 5–20 km / 20–50 km / Más de 50 km / No se ha medido | EUDR | Ordinal 5 niveles | IV3 fragilidad territorial | Legal |
| B0-12 | % mujeres en directiva / consejo directivo | % | CSRD/ESRS | Porcentaje | IV5 riesgo de exclusión (variable de contexto) | Competitividad |
| B0-13 | ¿Qué porcentaje aproximado de los socios productores opera en zonas clasificadas como de riesgo alto o muy alto de deforestación según el Mapa de Deforestación del MINAM o Global Forest Watch? | Menos del 10% / 10–30% / 30–60% / Más del 60% / No se ha evaluado | EUDR Art. 10 / MINAM | Ordinal 5 niveles | **IV3 — Fragilidad territorial (v0.3)** | Legal |
| B0-14 | ¿La cooperativa tiene capacidad técnica de verificación directa en campo —personal o prestataire con formación agronómica— para supervisar las prácticas de los socios en sus parcelas de forma periódica? | No tiene / Parcial, cubre menos de la mitad / Parcial, cubre más de la mitad / Sí, capacidad suficiente para visitas periódicas a todos los socios | EUDR (sostenibilidad del proceso) | Ordinal 4 niveles | **IV3 — Fragilidad territorial / IP3 gobernanza (v0.3)** | Legal |

---

**Tabla 4** *(continuación) — D1: Clasificación regulatoria (ISA-EUDR · Núcleo)*

| # | Pregunta | Opciones de respuesta | Estrategia PV | Tipo | Rol | Obligación |
|---|---|---|---|---|---|---|
| Q1 | ¿La cooperativa introduce el producto directamente al mercado UE bajo su nombre? | Sí / No | EUDR Art. 3 | Binaria | ISA-EUDR | Legal |
| Q2 | ¿Transforma el producto antes de venderlo? | Transforma / No transforma | EUDR Art. 2 | Binaria categórica | ISA-EUDR | Legal |
| Q3 | ¿Sabe con certeza qué rol le corresponde (operador, operador posterior, comerciante, micro/pequeño operador primario)? | Sí con certeza / Idea aproximada / No sabe | EUDR Art. 2 | Ordinal 3 niveles | ISA-EUDR | Legal |
| Q4 | ¿Cumple los umbrales de microempresa/pequeña empresa (Directiva 2013/34/UE)? | Sí / No / No sabe | EUDR Art. 13 | Ordinal 3 niveles | ISA-EUDR | Legal |

---

**Tabla 4** *(continuación) — D2: Trazabilidad y geolocalización (ISA-EUDR · Núcleo)*

| # | Pregunta | Opciones de respuesta | Estrategia PV | Tipo | Rol | Obligación |
|---|---|---|---|---|---|---|
| Q5 | ¿Existe registro de geolocalización (GPS/polígono) por parcela de socio? | 0–4 | EUDR Art. 9 | Escala 0–4 | ISA-EUDR | Legal |
| Q6 | % de socios con parcela geolocalizada | % | EUDR Art. 9 | Porcentaje | ISA-EUDR | Legal |
| Q7 | ¿El sistema vincula un lote exportado con la(s) parcela(s) específica(s)? | 0–4 | EUDR Art. 9 | Escala 0–4 | ISA-EUDR | Legal |
| Q8 | ¿Quién levantó la información geográfica? | Técnico propio / Consultor / Proyecto de cooperación / Socio por su cuenta / No se ha levantado | EUDR Art. 9 | Categórica 5 opciones | ISA-EUDR (sostenibilidad del dato) | Legal |
| Q9 | Frecuencia de actualización de la geolocalización | Nunca / Al ingreso del socio / Anual / Por cosecha | EUDR Art. 9 | Ordinal 4 niveles | ISA-EUDR | Legal |
| Q10 | ¿Se mezclan físicamente lotes de distinto origen sin registro de qué parcelas los componen? | Sí, sin control / Se mezclan con registro de origen / No, segregación completa | EUDR Art. 3 | Ordinal 3 niveles | 🚩 **Bandera** — anula puntaje Q5–Q7 si responde "sin control" | Legal |

---

**Tabla 4** *(continuación) — D3: Legalidad de la producción (ISA-EUDR · Núcleo)*

| # | Pregunta | Opciones de respuesta | Estrategia PV | Tipo | Rol | Obligación |
|---|---|---|---|---|---|---|
| Q11 | % de socios con título de propiedad o posesión reconocida legalmente | % | EUDR Art. 2(40)(a) | Porcentaje | ISA-EUDR | Legal |
| Q12 | ¿Hay parcelas superpuestas a áreas protegidas, reservas comunales o territorios indígenas sin sanear? | Sí, extensa / Sí, puntual / No verificado / No, ninguna | EUDR Art. 2(40)(a)(g) | Ordinal 4 niveles | ISA-EUDR | Legal |
| Q13 | ¿Se verifica cumplimiento laboral (no trabajo infantil, seguridad social) a nivel de finca? | 0–4 | EUDR Art. 2(40)(e)(f) | Escala 0–4 | ISA-EUDR | Legal |
| Q14 | ¿Alguna parcela de socios se ubica en una zona de desarrollo alternativo (ex-coca) o con antecedentes de conflicto social/territorial? | Sí / No / No verificado | EUDR (contexto) | Ordinal 3 niveles | ISA-EUDR (modulador interpretativo — cambia la naturaleza de la brecha) | Legal |
| Q14a | ¿Los socios tienen autorización de uso de agua para su actividad productiva, cuando corresponde? | Sí, verificadas / Parcialmente / No / No aplica | EUDR Art. 2(40)(b) | Ordinal 4 niveles | ISA-EUDR | Legal |
| Q14b | ¿El tratamiento de aguas residuales del beneficio cumple con lo exigido por la autoridad ambiental? *(autodeclarada)* | Siempre / A veces / No / No aplica | EUDR Art. 2(40)(b) | Ordinal 4 niveles | ISA-EUDR *(percepción declarada — sin fuente de contraste pública; ver nota)* | Legal |
| Q14c | ¿Alguna parcela está dentro de la faja marginal de un río, quebrada, lago o laguna? | Sí / No / No sabe | EUDR Art. 2(40)(b) | Ordinal 3 niveles | ISA-EUDR *(verificable externamente: mapa de fajas marginales, datosabiertos.gob.pe)* | Legal |
| Q14d | En las parcelas de los socios, ¿existe algún derecho de terceros —carga, embargo, servidumbre, usufructo, arrendamiento o derecho de uso consuetudinario— que restrinja el cultivo de café o cacao? | No existe / Existe registrado sin restricción / Acuerdo documentado con la autoridad / Usufructo o carga sin acuerdo que lo resuelva / Derechos consuetudinarios invocados sin proceso / No verificado | EUDR Art. 2(40)(d) | Ordinal 6 niveles (4→0) | ISA-EUDR — "No verificado" = 0 | Legal |
| Q14e | ¿La cooperativa y sus socios están al día en obligaciones tributarias, aduaneras y comerciales vinculadas a la actividad exportadora? | Sí, verificado / Parcialmente / No verificado / No sabe | EUDR Art. 2(40)(h) | Ordinal 4 niveles | ISA-EUDR | Legal |
| Q14f | ¿Existen políticas o mecanismos internos anticorrupción aplicables a la cadena de abastecimiento? | Sí, formalizado / Informal / No existe | EUDR Art. 2(40)(h) | Ordinal 3 niveles | ISA-EUDR | Legal |
| Q14g | Cuando corresponde, ¿se realizó un proceso de Consentimiento Libre, Previo e Informado (CLPI) con comunidades indígenas, nativas o campesinas? | Sí, documentado / Aplica pero no se ha realizado / No aplica / No sabe | EUDR Art. 2(40)(g) | Categórica 4 opciones | Verificación — **no promedia en D3** | Legal |

*Nota sobre D3.* Las preguntas Q14a, Q14b y Q14d son autodeclaradas y no tienen fuente de verificación pública completa —la autorización ambiental agraria (DS 006-2024-MIDAGRI) no está publicada como datos abiertos. El puntaje de D3 debe reportarse como *percepción de cumplimiento declarada por la cooperativa*, nunca como conformidad verificada. Q14c es la excepción: sí admite contraste externo con el mapa de fajas marginales de datosabiertos.gob.pe. Q14d admite contraste documental parcial vía SUNAT y Registro Catastral; su opción "No verificado" se computa como 0 porque el EUDR coloca la carga de la prueba sobre el operador, no sobre el verificador.

---

**Tabla 4** *(continuación) — D4: Riesgo de deforestación (ISA-EUDR · Núcleo)*

| # | Pregunta | Opciones de respuesta | Estrategia PV | Tipo | Rol | Obligación |
|---|---|---|---|---|---|---|
| Q15 | ¿Se verificó cambio de uso de suelo posterior al 31 de diciembre de 2020? | No verificado / Verificación parcial / Verificado sin hallazgos / Casos detectados sin resolver / Verificado sistemáticamente y documentado | EUDR Art. 3 | Ordinal 5 niveles | ISA-EUDR — "No verificado" reportado aparte | Legal |
| Q16 | ¿Usa herramientas de monitoreo satelital (Global Forest Watch, PNCB-MINAM)? | 0–4 | EUDR Art. 10 | Escala 0–4 | ISA-EUDR | Legal |
| Q17 | ¿Conoce la clasificación de riesgo (bajo/estándar/alto) de la zona de producción de sus socios? | Sí, documentado / Idea aproximada / No sabe | EUDR Art. 10 | Ordinal 3 niveles | ISA-EUDR | Legal |

---

**Tabla 4** *(continuación) — D5: Sistema interno de diligencia debida (ISA-EUDR · Núcleo)*

| # | Pregunta | Opciones de respuesta | Estrategia PV | Tipo | Rol | Obligación |
|---|---|---|---|---|---|---|
| Q18 | ¿Existe procedimiento escrito de diligencia debida? | 0–4 | EUDR Art. 8 | Escala 0–4 | ISA-EUDR | Legal |
| Q18a | ¿Existe política de deforestación formal y escrita, con objetivos, metas medibles y plazos? | 0–4 | EUDR Art. 8 | Escala 0–4 | ISA-EUDR | Legal |
| Q18b | ¿La cooperativa prioriza sus riesgos de deforestación con algún criterio de probabilidad e impacto, o los atiende sin orden definido? | No se prioriza / Priorización informal, sin criterio escrito / Priorización estructurada con matriz P×I o equivalente | EUDR Art. 10 | Ordinal 3 niveles | ISA-EUDR | Legal |
| Q19 | ¿Ha elaborado o participado en una declaración de diligencia debida o simplificada? | No sabe qué es / No pero lo entiende / En proceso / Presentada y aceptada | EUDR Art. 4 | Ordinal 4 niveles | ISA-EUDR | Legal |
| Q19a | Del plan de gestión de riesgos, marcar los componentes que incluye explícitamente | Plazos definidos / Recursos asignados / Responsables designados / Consulta con socios y comunidades / Seguimiento y monitoreo / Protocolo ante incumplimiento de socio / Atención diferenciada a productoras mujeres | EUDR Art. 10 | Mapeo múltiple | **Mapeo — no promedia en D5;** insumo Instrumento 4 | Legal |
| Q20 | ¿Existe responsable designado para el cumplimiento EUDR? | No / Función adicional / Dedicado | EUDR Art. 8 | Ordinal 3 niveles | ISA-EUDR | Legal |
| Q21 | ¿Hubo capacitación formal sobre EUDR en los últimos 12 meses? | No / Hace más de 12 meses / Sí, reciente | EUDR Art. 8 | Ordinal 3 niveles | ISA-EUDR | Legal |
| Q21a | ¿El plan de gestión de riesgos se revisa con una frecuencia definida? | No hay revisión definida / Revisión reactiva sin frecuencia fija / Revisión periódica definida | EUDR Art. 10 | Ordinal 3 niveles | ISA-EUDR | Legal |
| Q21b | ¿La cooperativa elabora y comunica un reporte de diligencia debida con indicadores? | No / Sí, uso interno / Sí, interno y compartido con compradores u otras partes interesadas | EUDR Art. 8 | Ordinal 3 niveles | ISA-EUDR | Legal |

---

**Tabla 4** *(continuación) — D6: Capacidad organizacional y digital (ISA-EUDR · Núcleo)*

| # | Pregunta | Opciones de respuesta | Estrategia PV | Tipo | Rol | Obligación |
|---|---|---|---|---|---|---|
| Q22 | Presupuesto asignado para cumplimiento EUDR | No / Parcial / Sí | EUDR Art. 8 | Ordinal 3 niveles | ISA-EUDR | Legal |
| Q23 | Digitalización de registros | Papel / Mixto / Digital | EUDR Art. 9 | Ordinal 3 niveles | ISA-EUDR | Legal |
| Q24 | Conectividad a internet en la sede de la cooperativa | No hay / Limitada / Confiable | EUDR Art. 9 | Ordinal 3 niveles | ISA-EUDR | Legal |
| Q25 | ¿Ha gestionado apoyo externo para adecuarse al EUDR? | No y lo necesita / No lo cree necesario / Sí en el pasado / Sí, actualmente activo | EUDR Art. 8 | Ordinal 4 niveles | ISA-EUDR | Legal |
| Q22a | ¿La cooperativa cuenta con una base de datos o sistema centralizado (digital o no) que permite vincular a cada socio proveedor con sus parcelas geolocalizadas, los lotes que ha entregado y su volumen? | No existe / Existe en papel desorganizado / Existe digital pero sin vínculos entre tablas / Existe digital con vínculos actualizados entre socio-parcela-lote | EUDR Art. 9 | Ordinal 4 niveles | **IP4 — Información y documentación (v0.3)** — insumo clave: antes solo D6.23 (digitalización) y D2.9 (frecuencia actualización geo); esta pregunta mide la capacidad real de generar evidencia para EUDR | Legal |
| Q22b | *(Rama: solo si Q22a ≠ "No existe" y ≠ "Existe en papel desorganizado")* ¿Qué tipo de sistema digital utiliza? | Excel o Access básico / Software especializado de trazabilidad (ChainPoint, Teia, BQuant, otro) / Sistema web propio o de tercero / Base de datos personalizada con soporte técnico regular | EUDR Art. 9 | Ordinal 4 niveles | **IP4 (v0.3)** | Legal |
| Q25a | ¿Los registros documentales de la cooperativa (actas, contratos con socios, guías de transporte, certificados, reportes de trazabilidad) se almacenan de forma segura —digital con respaldo o física en archivo— con capacidad de ser recuperados en menos de 48 horas si se pierden los originales? | No existe política de respaldo / Parcial, solo los más críticos / Sí, con respaldo definido pero no probado / Sí, con protocolo probado periódicamente | EUDR Art. 8 | Ordinal 4 niveles | **IP4 — Información y documentación (v0.3)** — antes solo D6.23+D2.9; esta pregunta mide la resistencia del sistema de información ante un requerimiento de evidencia del EUDR | Legal |
| Q25b | *(Rama: solo si Q25a = "Sí, con respaldo definido pero no probado" o "Sí, con protocolo probado")* ¿El protocolo de respaldo y recuperación fue diseñado internamente o con apoyo externo? ¿Cuándo se probó por última vez? | Diseñado internamente / Con apoyo de ONG o programa / Con apoyo de consultancy o proveedor IT / Nunca se ha probado / Probado hace más de 12 meses / Probado en los últimos 12 meses | EUDR Art. 8 | Ordinal 4 niveles (0→3) + binaria de prueba | **IP4 (v0.3)** | Legal |

---

**Tabla 4** *(continuación) — D7: Posición en la cadena de valor (ISA-EUDR · Núcleo)*

| # | Pregunta | Opciones de respuesta | Estrategia PV | Tipo | Rol | Obligación |
|---|---|---|---|---|---|---|
| Q26 | ¿El comprador europeo ha exigido formalmente geolocalización o diligencia debida? | Aún no / Informalmente / Formalmente por escrito | EUDR Art. 9 | Ordinal 3 niveles | ISA-EUDR | Legal |
| Q27 | ¿El comprador ofrece financiamiento o asistencia técnica condicionada al cumplimiento EUDR? | Sí / No | EUDR / Taxonomía UE | Binaria | ISA-EUDR | Ambas |
| Q28 | Riesgo percibido de perder el contrato si no cumple a tiempo | No sabe / Bajo / Medio / Alto | EUDR | Ordinal 4 niveles | **Indicador de urgencia — no promedia en D7** | Legal |
| Q28b | ¿El comprador europeo ha comunicado que sus propias obligaciones (EUDR, CSRD, CSDDD u otra) implican requisitos adicionales sobre la cadena de suministro más allá de la geolocalización? | No ha mencionado nada / Lo ha mencionado verbalmente sin requisito formal / Sí, ha enviado documentación o cuestionario de proveedores / Sí, lo ha formalizado como cláusula contractual | CSDDD / CSRD | Ordinal 4 niveles (0→3) | ISA-EUDR (D7) | Ambas |
| Q28c | *(Rama: solo si Q28b = "Sí, ha enviado documentación" o "Sí, lo ha formalizado como cláusula")* ¿Qué tipo de documentación ha enviado o solicitado el comprador? ¿Cubre solo a la cooperativa o también a sus proveedores (trazabilidad de segundo nivel)? | Cuestionario de autoevaluación / Guía de diligencia debida propia del comprador / Plantilla de trazabilidad (lotes, volúmenes, GPS) / Evaluación de riesgo de deforestación / Requisito de certificación de terceros (Fairtrade, Rainforest, orgánica) / Solo cubre a la cooperativa / Cubre también a los proveedores directos de la cooperativa / Cubre hasta proveedores de segundo nivel | CSDDD / CSRD | Ordinal 4 niveles (0→3) + escala de cobertura (cooperativa → segundo nivel) | **ISA-EUDR (D7)** — variable de cobertura: indica si el alcance del requerimiento llega a los pequeños productores de la base de la cadena | Ambas |

---

**Tabla 4** *(continuación) — D8: Gobernanza interna y apropiación de los socios (ISA-EUDR · Extendida)*

| # | Pregunta | Opciones de respuesta | Estrategia PV | Tipo | Rol | Obligación |
|---|---|---|---|---|---|---|
| Q29 | ¿Se han realizado asambleas o reuniones informativas sobre el EUDR dirigidas a los socios (no solo a la directiva)? | 0–4 | EUDR Art. 8 | Escala 0–4 | ISA-EUDR | Legal |
| Q30 | % estimado de socios que entienden por qué se les pide geolocalización o documentación | % | EUDR Art. 8 | Porcentaje estimado | ISA-EUDR | Legal |
| Q31 | ¿Existe algún mecanismo (incentivo o condición) para que los socios entreguen información de su parcela? | No existe / Se pide informalmente / Es requisito formal para vender a la cooperativa | EUDR Art. 9 | Ordinal 3 niveles | ISA-EUDR | Legal |
| Q32 | Rotación de la directiva en los últimos 2 años | Alta / Moderada / Baja/estable | EUDR (sostenibilidad del proceso) | Ordinal 3 niveles | ISA-EUDR | Legal |

---

**Tabla 4** *(continuación) — D9: Sostenibilidad económica del cumplimiento (ISA-EUDR · Extendida)*

| # | Pregunta | Opciones de respuesta | Estrategia PV | Tipo | Rol | Obligación |
|---|---|---|---|---|---|---|
| Q33 | Estimación del costo total de adecuación (geolocalización, saneamiento, sistemas, capacitación) frente al presupuesto anual de la cooperativa | Costo mayor al 10% del presupuesto / Entre 3–10% / Menor al 3% / No se ha estimado | EUDR | Ordinal 4 niveles | ISA-EUDR / IV4 vulnerabilidad | Legal |
| Q34 | ¿La cooperativa ha financiado la adecuación con deuda? | Sí / No / No ha sido necesario | EUDR | Ordinal 3 niveles | ISA-EUDR / IV4 | Legal |
| Q35 | ¿Existe riesgo de que el costo de adecuación se traslade a un menor precio pagado al socio productor? | Sí, ya ha ocurrido / Es un riesgo latente / No aplica / No se ha evaluado | EUDR | Ordinal 4 niveles | ISA-EUDR / IV4 | Legal |

---

**Tabla 4** *(continuación) — D10: Confusión certificación/EUDR (bandera — no promedia)*

| # | Pregunta | Opciones de respuesta | Estrategia PV | Tipo | Rol | Obligación |
|---|---|---|---|---|---|---|
| Q36 | ¿La cooperativa cree que su certificación vigente (Rainforest Alliance, Fairtrade, Orgánica, etc.) ya cubre las obligaciones del EUDR? | Sí, totalmente / Sí, en parte / No, sabe que son cosas distintas / No tiene certificación | EUDR Art. 30 | Ordinal 4 niveles | 🚩 **Bandera percepción** — "Sí, totalmente" = alerta máxima, independiente del resto del semáforo | Legal |
| Q37 | ¿Algún proveedor o consultor le ha ofrecido una "certificación EUDR" como producto? | Sí / No | EUDR | Binaria | 🚩 **Bandera comercial** — no existe tal certificación oficial | Legal |
| Q36a | ¿La organización ha recibido asesoría específica sobre el EUDR (a diferencia de asesoría genérica de sostenibilidad)? | Sí, asesoría especializada en EUDR / Solo asesoría genérica de sostenibilidad / No ha recibido asesoría / No sabe | EUDR | Ordinal 4 niveles | **No promedia** — se captura, se codifica y se reporta aparte (no es bandera roja como Q36/Q37) | Legal |

---

**Tabla 4** *(continuación) — D11: Ecosistema de apoyo externo (inventario — no promedia)*

| # | Pregunta | Opciones de respuesta | Estrategia PV | Tipo | Rol | Obligación |
|---|---|---|---|---|---|---|
| Q38 | Marcar los actores con los que la cooperativa ya tiene contacto o apoyo activo | SERFOR / PNCB-MINAM / MIDAGRI o programa regional / Gobierno regional (catastro/saneamiento) / Cooperación internacional (GIZ, USAID, UE, ONG) / JNC, APPCACAO u otro gremio / Ninguno | EUDR | Mapeo múltiple | **Inventario de oportunidades** — insumo Instrumento 4 | Legal |
| Q39 | De los actores no marcados, ¿cuáles conoce pero no ha contactado y por qué? | Texto libre | EUDR | Texto libre | Inventario — brecha de conexión | Legal |

---

**Tabla 4** *(continuación) — D12: Huella de carbono y gestión de emisiones GEI (ISA-PactoVerde · Módulo i)*

*Nota de aplicación.* Las preguntas son válidas para café y cacao por igual. Para café, la herramienta de referencia es CalCafé v2.1 (PromPerú/PUCP-PELCAN, validada bajo ISO 14040/44 y metodología PEFCR). Para cacao, no existe herramienta nacional validada equivalente; el encuestador debe anotar qué alternativa usa la cooperativa (herramienta del comprador, consultoría externa, COSA tool u otra) o registrar "ninguna". No imputar ni ajustar el puntaje: la brecha entre productos debe aparecer en los datos.

| # | Pregunta | Opciones de respuesta | Estrategia PV | Tipo | Rol | Obligación |
|---|---|---|---|---|---|---|
| Q40 | ¿La cooperativa conoce alguna herramienta para calcular la huella de carbono de su producto de exportación? | No sabe qué es una huella de carbono / Conoce el concepto pero no ha identificado herramienta / Conoce una herramienta pero no la ha usado / La ha usado al menos una vez / La usa sistemáticamente | Taxonomía UE / CSRD / CBAM | Ordinal 5 niveles | ISA-PactoVerde (D12) | Competitividad |
| Q41 | ¿Cuenta con registros de insumos para calcular huella (fertilizantes por campaña, combustible, energía de procesamiento, distancia finca-acopio)? | No registra nada / Registra algún insumo / Registra la mayoría / Registra todo sistemáticamente | Taxonomía UE / CSRD | Ordinal 4 niveles | ISA-PactoVerde (D12) | Competitividad |
| Q42 | ¿Ha calculado la huella de carbono de su café o cacao de exportación en los últimos 2 años? | No / Sí, estimación interna sin herramienta validada / Sí, con herramienta validada [anotar cuál] / Sí, verificada por tercero independiente | Taxonomía UE / CSRD | Ordinal 4 niveles | ISA-PactoVerde (D12) | Competitividad |
| Q43 | ¿Tiene objetivo cuantificado de reducción de emisiones (por ejemplo, −X% al 2030)? | No / En definición / Sí, interno / Sí, público y con plan de acción | Taxonomía UE / CSRD | Ordinal 4 niveles | ISA-PactoVerde (D12) | Competitividad |
| Q44 | ¿Reporta huella de carbono a compradores o plataformas (CDP, plataforma del comprador)? | No / Solo si lo piden / Sí, regularmente | CSRD / Taxonomía UE | Ordinal 3 niveles | ISA-PactoVerde (D12) | Competitividad |

---

**Tabla 4** *(continuación) — D13: Reporte de sostenibilidad y transparencia (ISA-PactoVerde · Módulo iv)*

*Nota de aplicación.* Comenzar siempre con Q44b antes de Q45. Muchas cooperativas no tienen reporte formal pero sí elaboran algún tipo de documentación interna; Q44b captura ese tramo y evita que toda la dimensión resulte en ceros (efecto suelo). El promedio de D13 incluye Q44b y Q45–Q50 (siete preguntas en total).

| # | Pregunta | Opciones de respuesta | Estrategia PV | Tipo | Rol | Obligación |
|---|---|---|---|---|---|---|
| Q44b | ¿La cooperativa elabora actualmente algún documento que recoja indicadores de su desempeño ambiental, social o de gestión, aunque sea para uso interno y sin seguir ningún estándar formal? | No existe ningún documento de este tipo / Sí, registros internos informales sin estructura / Sí, informe estructurado de uso interno / Sí, informe publicado o compartido con terceros | CSRD/ESRS | Ordinal 4 niveles | ISA-PactoVerde (D13) — escala de entrada | Competitividad |
| Q45 | ¿Elabora algún reporte anual de sostenibilidad o memoria de responsabilidad social? | No / Interno, informal / Formal, interno / Público según estándar reconocido (GRI, ESRS simplificado) | CSRD/ESRS | Ordinal 4 niveles | ISA-PactoVerde (D13) | Competitividad |
| Q46 | ¿El reporte incluye indicadores ambientales (deforestación, huella carbono, agua, biodiversidad, residuos)? | No / Parcial / Sí, básicos / Sí, completos y con metas | CSRD/ESRS | Ordinal 4 niveles | ISA-PactoVerde (D13) | Competitividad |
| Q47 | ¿El reporte incluye indicadores sociales (trabajo infantil, trabajo forzoso, igualdad salarial, participación de mujeres, salud ocupacional)? | No / Parcial / Sí, básicos / Sí, completos y con metas | CSRD/ESRS | Ordinal 4 niveles | ISA-PactoVerde (D13) | Competitividad |
| Q48 | ¿El reporte incluye indicadores de gobernanza (estructura directiva, anticorrupción, gestión de riesgos, canal de denuncias)? | No / Parcial / Sí, básicos / Sí, completos | CSRD/ESRS | Ordinal 4 niveles | ISA-PactoVerde (D13) | Competitividad |
| Q49 | ¿La información reportada es verificada o auditada por un tercero independiente? | No / Auto-declarada / Verificación parcial / Auditoría completa externa | CSRD/ESRS | Ordinal 4 niveles | ISA-PactoVerde (D13) | Competitividad |
| Q50 | ¿El reporte se comparte proactivamente con compradores europeos y partes interesadas? | No / Solo bajo solicitud / Sí, sistemáticamente | CSRD/ESRS | Ordinal 3 niveles | ISA-PactoVerde (D13) | Competitividad |

---

**Tabla 4** *(continuación) — D14: Economía circular, envases y gestión de residuos (ISA-PactoVerde · Módulo v)*

| # | Pregunta | Opciones de respuesta | Estrategia PV | Tipo | Rol | Obligación |
|---|---|---|---|---|---|---|
| Q51 | Gestión de residuos del beneficio y acopio (cáscara, mucílago, agua miel, trilla, despulpado) | Eliminación sin tratamiento / Compostaje parcial / Compostaje o biogás sistemático con reuso en fincas / Economía circular cerrada con subproductos valorizados | PPWR / Economía Circular UE | Ordinal 4 niveles | ISA-PactoVerde (D14) | Competitividad |
| Q52 | ¿Los envases de exportación (sacos, big-bags, contenedores) son reutilizables, reciclables o compostables? | Ninguno / Parcialmente / Mayoría / Todos, con certificación o trazabilidad de retorno | PPWR | Ordinal 4 niveles | ISA-PactoVerde (D14) | Competitividad |
| Q53 | Plásticos de un solo uso en la cadena (bolsas, film, flejes, etiquetas): ¿existe plan de reducción o eliminación? | No / En análisis / Sí, en implementación / Sí, cumplido y verificado | PPWR | Ordinal 4 niveles | ISA-PactoVerde (D14) | Competitividad |
| Q54 | ¿Se comercializa o transforma algún subproducto o residuo del proceso (cáscara, mucílago, agua tratada)? | No / Piloto / Sí, escala parcial / Sí, escala comercial | Economía Circular UE | Ordinal 4 niveles | ISA-PactoVerde (D14) | Competitividad |
| Q55 | ¿Existe registro de qué envases salen, cuáles retornan y qué residuos se generan por lote exportado? | No / Parcial / Sí, para envases / Sí, completo envases y residuos | PPWR | Ordinal 4 niveles | ISA-PactoVerde (D14) | Competitividad |

---

**Tabla 4** *(continuación) — D15: Gestión fitosanitaria y LMR (ISA-PactoVerde · Módulo vi · Farm to Fork)*

*Nota de aplicación.* Esta dimensión aplica por igual a café y cacao — es el módulo del instrumento sin sesgo de producto. El informante clave es el responsable técnico de campo, no la gerencia comercial. Q60 es bandera independiente del promedio: si la respuesta es afirmativa (rechazo real en frontera), reportarla siempre por separado sin importar el puntaje promedio de D15.

> ⚠️ **Evaluación de comprensibilidad (Fase piloto, Hoja de ruta DT-ISCAM-001 §8.1).** Antes de escalar la aplicación de D15.Q56–Q60 a las 174 organizaciones, el equipo de campo debe validar la comprensibilidad de estas cinco preguntas con 5–8 cooperativas piloto. En particular, verificar: (a) que el término "LMR" sea conocido por el técnico de campo o pueda ser traducido al vocabulario local ("límites de residuos permitidos en destino"); (b) que Q57 (protocolo interno de pesticidas) no genere confusión con la lista de pesticidas prohibidos por DIGESA/SENASA Peru — son requisitos distintos; (c) que Q59 (exigencia del comprador) aplique para organizaciones que nunca exportaron a la UE. Si el piloto revela incomprensión sistemática en alguna pregunta, documentar la alternativa lingüística usada y reportar al equipo ISCAM antes de escalar.

| # | Pregunta | Opciones de respuesta | Estrategia PV | Tipo | Rol | Obligación |
|---|---|---|---|---|---|---|
| Q56 | ¿La cooperativa conoce los LMR de la UE para su producto, incluyendo las alertas del sistema RASFF para café o cacao peruano? | No sabe qué son los LMR / Los conoce en términos generales pero no verifica / Los conoce y verifica cumplimiento en fincas de los socios / Los verifica sistemáticamente por lote antes del embarque | Farm to Fork / Dir. 2009/128/CE | Ordinal 4 niveles | ISA-PactoVerde (D15) | Ambas |
| Q57 | ¿Existe un protocolo interno que prohíbe o restringe pesticidas específicos en las fincas de los socios en función de los LMR de la UE? | No existe / Lista informal comunicada verbalmente / Protocolo escrito no verificado en campo / Protocolo escrito verificado en campo con evidencia | Farm to Fork | Ordinal 4 niveles | ISA-PactoVerde (D15) | Ambas |
| Q58 | ¿Se realizan análisis de residuos de pesticidas sobre el producto de exportación? | Nunca / Ocasionalmente, sin sistema definido / Sistemáticamente por campaña / Por lote antes del embarque, con resultado documentado y archivado | Farm to Fork / RASFF | Ordinal 4 niveles | ISA-PactoVerde (D15) | Ambas |
| Q59 | ¿El comprador europeo ha exigido certificados de análisis de residuos o declaraciones de cumplimiento de LMR en los últimos 2 años? | No ha exigido nada / Lo exigió de forma puntual / Lo exige regularmente / Es parte del contrato vigente | Farm to Fork | Ordinal 4 niveles | ISA-PactoVerde (D15) | Ambas |
| Q60 | ¿Ha tenido algún lote retenido, observado o rechazado en frontera UE por exceso de residuos de pesticidas en los últimos 3 años? | Sí, más de un evento / Sí, un evento / No / No sabe | Farm to Fork / RASFF | Ordinal 4 niveles | 🚩 **Bandera** — reportar siempre por separado del promedio D15 | Ambas |

---

**Tabla 5**
*Resumen numérico por dimensión: preguntas que promedian vs. que no promedian*

| Dimensión | Preguntas que promedian | Preguntas que no promedian | Total ítems |
|---|---|---|---|
| D1 | 4 | — | 4 |
| D2 | 5 (Q5–Q9) | Q10 (bandera) | 6 |
| D3 | 10 (Q11–Q14f) | Q14g (verificación) | 11 |
| D4 | 3 | — | 3 |
| D5 | 8 (Q18–Q21b) | Q19a (mapeo) | 9 |
| D6 | 8 (Q22–Q25, Q22a, Q22b, Q25a, Q25b) | Q22b, Q25b (ramales condicionales, no pesan en IP4) | 6 |
| D7 | 4 (Q26–Q28c) | Q28 (urgencia); Q28c (ramal condicional sobre tipo de documentación CSDDD/CSRD) | 4 |
| D8 | 4 | — | 4 |
| D9 | 3 | — | 3 |
| D10 | — | Q36, Q37 y Q36a (no promedian; se reportan aparte) | 3 |
| D11 | — | Q38–Q39 (inventario) | 2 |
| D12 | 5 | — | 5 |
| D13 | 7 (Q44b + Q45–Q50) | — | 7 |
| D14 | 5 | — | 5 |
| D15 | 4 (Q56–Q59) | Q60 (bandera) | 5 |
| **Total D1–D15** | **71** (antes 67: +Q22a, +Q25a de v0.3; +Q22b, +Q25b, +Q28c de v0.4) | **9** | **80** (antes 75) |
| Bloque 0 | — | **14** (antes 12: +B0-13, +B0-14) | 14 |
| Bloque P | — | 14 (resultado) | 14 |
| **Total general** | | | **104 ítems / 95 preguntas** (v0.4: +Q28c; +Q36a, 2026-10-15) |

*Nota.* La diferencia entre 103 ítems y 94 preguntas proviene de que los ramales condicionales (Q22b, Q25b) son sub-preguntas que no se cuentan como ítems independientes del índice.

---

## 5. Decisiones de alcance

Un instrumento de diagnóstico es, inevitablemente, un conjunto de inclusiones y exclusiones. Las siguientes decisiones de alcance se documentan con argumento verificable, no como nota al margen, porque determinan qué conclusiones se pueden y no se pueden extraer del ISA.

**CBAM (Reglamento (UE) 2023/956).** El mecanismo de ajuste en frontera por carbono no aplica a café ni cacao: los sectores cubiertos en la primera fase son acero, cemento, aluminio, fertilizantes, hidrógeno y electricidad. Su inclusión en el instrumento generaría ruido sin señal para este universo.

**Biodiversidad forestal — Art. 2(40)(c) del EUDR.** La legislación forestal es pertinente bajo el EUDR únicamente cuando se relaciona directamente con la cosecha de madera. Café y cacao no son productos madereros y, por tanto, esta categoría no genera obligación en el marco de este toolkit. Esta es una decisión de alcance documentada, reabrirla si el proyecto incorpora madera.

**Dimensión de género como criterio de cumplimiento.** La dimensión de género es relevante para la Directiva CSDDD/CS3DD y para estándares ESG, pero no determina el acceso al mercado bajo el EUDR de manera directa. Incorporarla como dimensión de madurez —con el mismo peso que trazabilidad o legalidad— diluiría el diagnóstico y podría desviar recursos de lo que sí decide si el producto entra o no a la UE. Se mantiene únicamente como variable de contexto en B0-12 y como proxy del IV5 del proyecto madre.

**CLPI como criterio de cumplimiento.** El Documento Orientador del grupo de trabajo multisectorial ADEX/MIDAGRI/MINCETUR/GIZ/EFI (2026), avalado por la Resolución Ministerial N.º 0128-2025-MIDAGRI con metodología del European Forest Institute, evaluó los requisitos legales para café y cacao peruano y concluyó que no existe requisito legal pertinente en la categoría de Consentimiento Libre, Previo e Informado a nivel nacional. Q14g se conserva como verificación de bajo costo para el caso particular de cooperativas con socios en territorios de comunidades indígenas o campesinas específicas, pero no promedia en D3.

---

## 6. Banderas no compensables

Las banderas son preguntas cuyo resultado se reporta siempre de forma independiente del puntaje promedio de su dimensión. Su presencia en rojo no puede ser compensada por ningún puntaje alto en otras preguntas. El criterio de diseño es el mismo que gobierna las preguntas obligatorias no compensables del SAI Platform Farm Sustainability Assessment (SAI Platform, 2022), el estándar de referencia mundial para evaluaciones de sostenibilidad a nivel de cooperativa.

### Bandera Q10 — Mezcla física de lotes sin control (D2)

El EUDR prohíbe el sistema de "balance de masas" —mezclar producto de origen verificado con no verificado y prorratear el resultado—; exige segregación física o identidad preservada del lote (Art. 3). Una cooperativa puede tener el mejor registro documental de geolocalización de todas sus parcelas y aun así invalidarlo completamente si en el punto de acopio o beneficio mezcla físicamente los lotes sin registro de qué parcelas los componen. Una respuesta "Sí, se mezclan sin control" activa la bandera independientemente de cuánto midan Q5–Q7.

### Bandera Q36 — Falsa seguridad sobre certificación voluntaria (D10)

El Art. 10(2) del Reglamento (UE) 2023/1115 es explícito: un esquema de certificación puede usarse como información complementaria, no como sustituto de la evidencia directa de geolocalización y legalidad. Una cooperativa que responde "Sí, totalmente cubierto" en Q36 probablemente no está tomando acción propia porque cree, erróneamente, estar exenta. Esa creencia es más peligrosa que no saber qué es el EUDR, porque genera falsa seguridad activa. La bandera se activa con cualquier respuesta que refleje cobertura total o parcial por certificación.

### Bandera Q37 — Oferta comercial de "certificación EUDR" (D10)

No existe ninguna certificación oficial emitida por la UE o reconocida por la Comisión como equivalente al cumplimiento del EUDR. Una respuesta afirmativa en Q37 indica que la cooperativa ha sido contactada por una oferta que, en el mejor de los casos, confunde marketing con regulación y, en el peor, representa una práctica comercial engañosa que puede haber llevado a la asignación incorrecta de recursos.

### Bandera Q60 — Rechazo en frontera por exceso de residuos de pesticidas (D15)

A diferencia de las banderas Q10, Q36 y Q37, que son señales de riesgo potencial, Q60 es evidencia de un incidente ya ocurrido. Un lote rechazado en frontera UE por exceso de LMR tiene el mismo efecto comercial que un rechazo por deforestación, y su presencia implica que el riesgo de D15 ya se materializó. Reportar siempre el número de eventos y, cuando se conozca, el lote afectado.

---

## 7. Variables de desempeño — Bloque P

### 7.1 Propósito

El ISA-EUDR y el ISA-PactoVerde miden el nivel de preparación —son el predictor. El objetivo (f) del proyecto madre requiere además medir el impacto de esa preparación sobre resultados de negocio reales. El Bloque P recoge ese resultado en el mismo instrumento para permitir el cruce ISA↔desempeño sobre la misma organización sin depender de fuentes externas.

### 7.2 Limitación de diseño

El levantamiento es transversal. Las preguntas P2, P5 y P7 son retrospectivas por autodeclaración —piden recordar una cifra de hace tres años—, no datos de panel verificados. Cualquier correlación ISA↔desempeño que resulte del análisis debe reportarse como asociación transversal con recall retrospectivo, nunca como evidencia de causalidad. Esta limitación no invalida el bloque: es la información disponible para el diseño, y es preferible una correlación con limitaciones declaradas que ningún indicador de resultado en absoluto.

### 7.3 Tabla del Bloque P

**Tabla 6**
*Bloque P — Variables de desempeño (v0.2)*

| # | Pregunta | Opciones de respuesta | Estrategia PV | Tipo | Rol | Obligación |
|---|---|---|---|---|---|---|
| P1 | Volumen exportado a la UE en el último año (kg o toneladas; especificar unidad y producto) | Número + unidad | EUDR | Numérica | Variable resultado EUDR | Legal |
| P1b | Volumen TOTAL exportado a todos los destinos (UE y no UE) en el último año | Número + unidad | EUDR | Numérica | Variable resultado — permite calcular % dependencia UE = P1/P1b | Legal |
| P2 | Volumen exportado a la UE hace 3 años, mismo producto *(retrospectivo)* | Número + unidad | EUDR | Numérica | Variable resultado — tendencia aproximada | Legal |
| P3 | Ingreso total por exportaciones a la UE en el último año (S/ o USD; especificar moneda) | Número + moneda | EUDR | Numérica | Variable resultado EUDR | Legal |
| P4 | N.º de compradores o clientes europeos activos actualmente | Número | EUDR | Numérica | Variable resultado EUDR | Legal |
| P5 | N.º de compradores europeos activos hace 3 años *(retrospectivo)* | Número | EUDR | Numérica | Variable resultado — tendencia | Legal |
| P6 | Precio promedio pagado al socio productor por kg/quintal en el último año (S/ o USD) | Número + moneda | EUDR / D9 | Numérica | Variable resultado — conecta con D9.Q35 | Legal |
| P7 | Precio promedio pagado al socio productor por kg/quintal hace 3 años *(retrospectivo)* | Número + moneda | EUDR / D9 | Numérica | Variable resultado — tendencia | Legal |
| P8 | ¿Ha tenido algún lote rechazado u observado por un comprador europeo por motivos de trazabilidad o deforestación en los últimos 2 años? | Sí / No / No sabe | EUDR | Binaria | Variable resultado EUDR | Legal |
| P9 | Si P8 = Sí: N.º aproximado de lotes rechazados u observados | Número | EUDR | Numérica | Variable resultado EUDR | Legal |
| P10 | ¿Ha perdido algún contrato o comprador europeo en los últimos 2 años por motivos de cumplimiento regulatorio o de sostenibilidad? | Sí / No / No sabe | EUDR | Binaria | Variable resultado EUDR | Legal |
| P11 | % del volumen total exportado en el último año que cuenta con trazabilidad completa verificada hasta la parcela de origen | 0–100% | EUDR | Porcentaje | Criterio de validación externa ISCAM — no promedia | Legal |
| P12 | N.º de años consecutivos exportando a la UE (contando el año actual) | Número | EUDR | Numérica | Criterio de validación externa ISCAM — no promedia | Legal |
| P13 | ¿Algún comprador europeo ha exigido formalmente, en los últimos 2 años, información sobre huella de carbono, LMR de pesticidas u otro requisito de sostenibilidad más allá del EUDR? | No / Sí, de forma verbal o informal / Sí, como cuestionario de proveedor o documentación formal / Sí, como cláusula contractual o condición de pago | CSDDD / CSRD / Farm to Fork | Ordinal 4 niveles | Variable resultado Pacto Verde ampliado | Ambas |
| P14 | ¿La cooperativa ha accedido o intentado acceder a financiamiento verde, crédito de impacto o fondos condicionados a criterios de sostenibilidad del Pacto Verde en los últimos 2 años? | No ha intentado / Lo intentó pero no cumplió los criterios / Sí, recibió financiamiento verde / No sabe si aplica a su caso | Taxonomía UE / SFDR | Ordinal 4 niveles | Variable resultado Pacto Verde ampliado | Competitividad |

### 7.4 Indicadores derivados

Los siguientes indicadores se calculan en el análisis a partir de las respuestas del Bloque P; no son preguntas adicionales al instrumento.

- Variación de volumen exportado a la UE = (P1 − P2) / P2
- Variación de N.º de compradores europeos = P4 − P5
- Variación del precio pagado al socio = (P6 − P7) / P7
- % dependencia del mercado europeo = P1 / P1b

---

## 8. Guía de llenado

### 8.1 Quién responde cada dimensión

La encuesta no es respondible por una sola persona. La Tabla 7 identifica el informante adecuado para cada bloque y la razón por la que ese informante, y no otro, produce el dato más confiable.

**Tabla 7**
*Informantes por dimensión*

| Dimensión | Informante ideal | Razón |
|---|---|---|
| Bloque 0 + Bloque P | Quien tenga acceso a registros de exportación y contabilidad | Los datos duros (RUC, volúmenes, precios) no son de memoria; las preguntas retrospectivas (P2, P5, P7) es preferible dejarlas en blanco antes de forzar una estimación sin sustento contable |
| D1 — Clasificación regulatoria | Gerencia general o asesoría legal/contable | El estatus jurídico-comercial frente al EUDR rara vez lo maneja el personal de campo con certeza |
| D2 — Trazabilidad | Responsable técnico/de campo + gerencia | Q10 (mezcla de lotes) es bandera — es importante que quien responde tenga acceso real al proceso de acopio, no solo a los registros |
| D3 — Legalidad | Gerencia + responsable de campo | Las preguntas Q14a, Q14b y Q14d son autodeclaradas: mejor "No verificado" que un "No" optimista sin sustento; mejor dejar el puntaje bajo que sobreestimarlo |
| D4 — Riesgo de deforestación | Responsable técnico/de campo | "No verificado" en Q15 es información valiosa, no una respuesta evasiva — la línea base nacional es que entre el 40% y el 60% de productores no tiene título inscrito (Cavassa, 2022) |
| D5 — Sistema de diligencia debida | Responsable técnico o de cumplimiento | Si no existe ese cargo, esa ausencia es el dato correcto en Q20; Q19a es mapeo, marcar todos los componentes que apliquen, no solo uno |
| D6 — Capacidad organizacional | Gerencia general o administración | El personal de campo rara vez maneja cifras de presupuesto o nivel de digitalización |
| D7 — Cadena de valor | Gerencia comercial | Q28 (riesgo percibido) no promedia — es un indicador de urgencia; Q28b requiere conocimiento del contenido de los contratos con compradores europeos |
| D8 — Gobernanza | Directiva + 1–2 socios de base, por separado | La directiva tiende a sobrestimar cuánto entienden los socios; la comparación de las dos respuestas es en sí misma un dato |
| D9 — Sostenibilidad económica | Tesorería o gerencia administrativa | Si no hay estimación real del costo de adecuación, "No se ha estimado" en Q33 es preferible a inventar una cifra |
| D10 — Certificación/EUDR | Directiva o gerencia | Sondear con tacto; registrar la respuesta exacta sin suavizarla — la bandera Q36 pierde su utilidad si quien aplica "ayuda" a la cooperativa a responder |
| D11 — Ecosistema de apoyo | Gerencia o responsable de relaciones institucionales | Marcar solo contacto real y activo, no el conocimiento de que el actor existe |
| D12 — Huella de carbono | Gerencia + responsable técnico/calidad | Q40 aplica igual a café y cacao — anotar qué herramienta usa o "ninguna" para cacao; no asumir CalCafé |
| D13 — Reporte de sostenibilidad | Gerencia + comunicación | Empezar con Q44b — incluso un registro interno informal puntúa y es mejor que dejar la dimensión en cero |
| D14 — Economía circular | Gerencia + operaciones/beneficio | Quien conoce los procesos de acopio y empaque en detalle, no solo la gerencia |
| D15 — Fitosanitarios/LMR | Gerencia + **responsable técnico de campo** | Es quien supervisa las prácticas agronómicas en fincas de socios y tiene acceso a los resultados de análisis de residuos; Q60 (rechazo en frontera) anotar aunque el resto de D15 sea positivo |

### 8.2 Tres reglas ante la duda

1. **Nunca inventar.** Si no se sabe la respuesta con certeza, marcar "No sabe" o "No verificado". Un cero real es más valioso que un 3 sin sustento — el diagnóstico correcto parte de la brecha real, no de la brecha que la cooperativa preferiría no tener.
2. **Distinguir "No aplica" de "No verificado".** Las dos tienen significado radicalmente distinto para el análisis: "No aplica" indica que la pregunta no corresponde al contexto de esta cooperativa; "No verificado" indica que aplica pero no se ha chequeado. Confundirlas infla artificialmente el puntaje.
3. **Dejar en blanco si no hay dato.** Para preguntas numéricas del Bloque P, un campo vacío es preferible a una estimación de memoria no respaldada por registros contables. La regla de datos faltantes del ISA (re-ponderar, nunca imputar con la media) maneja los blancos correctamente; no maneja los valores inventados.

---

## 9. Referencias

Cavassa, R. (2022). *Situación de la tenencia de tierra en productores de café y cacao en el Perú*. MIDAGRI.

Chrissis, M. B., Konrad, M., & Shrum, S. (2011). *CMMI for development: Guidelines for process integration and product improvement* (3rd ed.). Addison-Wesley.

Comisión Europea. (2019). *Comunicación de la Comisión: El Pacto Verde Europeo* (COM/2019/640 final). https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=COM%3A2019%3A640%3AFIN

Comisión Europea. (2026). *Documento de orientación para la aplicación del Reglamento (UE) 2023/1115* (3.ª ed., C/2026/3896). Diario Oficial de la Unión Europea. https://eur-lex.europa.eu

Directiva 2009/128/CE del Parlamento Europeo y del Consejo, de 21 de octubre de 2009, por la que se establece el marco de la actuación comunitaria para conseguir un uso sostenible de los plaguicidas. Diario Oficial de la Unión Europea, L 309, 71–86. http://data.europa.eu/eli/dir/2009/128/oj

Directiva (UE) 2022/2464 del Parlamento Europeo y del Consejo, de 14 de diciembre de 2022, por la que se modifican el Reglamento (UE) n.º 537/2014 y las Directivas 2004/109/CE, 2006/43/CE y 2013/34/UE, en lo que respecta a la presentación de información sobre sostenibilidad por parte de las empresas. Diario Oficial de la Unión Europea, L 322, 15–80. https://eur-lex.europa.eu/eli/dir/2022/2464

Directiva (UE) 2024/1760 del Parlamento Europeo y del Consejo, de 13 de junio de 2024, sobre diligencia debida de las empresas en materia de sostenibilidad. Diario Oficial de la Unión Europea, L 2024/1760. https://eur-lex.europa.eu/eli/dir/2024/1760/oj

Documento Orientador ADEX/MIDAGRI/MINCETUR/GIZ/EFI. (2026). *Diligencia debida en legalidad para café y cacao en el marco del EUDR: documento orientador para el Perú*. Resolución Ministerial N.º 0128-2025-MIDAGRI.

Grabs, J. (2024). The construction of compliance with the European Union Deforestation Regulation in global coffee value chains. *Regulation & Governance*. https://doi.org/10.1111/rego.12632

Greco, S., Ishizaka, A., Tasiou, M., & Torrisi, G. (2019). On the methodological framework of composite indices: A review of the issues of weighting, aggregation, and robustness. *Social Indicators Research, 141*(1), 61–94. https://doi.org/10.1007/s11205-017-1832-9

Nardo, M., Saisana, M., Saltelli, A., Tarantola, S., Hoffman, A., & Giovannini, E. (2008). *Handbook on constructing composite indicators: Methodology and user guide* (OECD Statistics Working Papers, 2005/3). OECD Publishing. https://doi.org/10.1787/533411815016

PromPerú / PUCP-PELCAN. (2021). *Manual de uso CalCafé v2.1: calculadora de ciclo de vida para café peruano de exportación* (ISO 14040/44, PEFCR). PromPerú.

Reglamento (UE) 2019/2088 del Parlamento Europeo y del Consejo, de 27 de noviembre de 2019, sobre la divulgación de información relativa a la sostenibilidad en el sector de los servicios financieros. Diario Oficial de la Unión Europea, L 317, 1–16. https://data.europa.eu/eli/reg/2019/2088/oj

Reglamento (UE) 2020/852 del Parlamento Europeo y del Consejo, de 18 de junio de 2020, relativo al establecimiento de un marco para facilitar las inversiones sostenibles. Diario Oficial de la Unión Europea, L 198, 13–43. https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=uriserv:OJ.L_.2020.198.01.0013.01.ENG

Reglamento (UE) 2023/1115 del Parlamento Europeo y del Consejo, de 31 de mayo de 2023, relativo a la comercialización en el mercado de la Unión y a la exportación desde la Unión de determinadas materias primas y productos asociados a la deforestación y la degradación forestal. Diario Oficial de la Unión Europea, L 150, 206–290. https://eur-lex.europa.eu/legal-content/es/ALL/?uri=CELEX:32023R1115

Reglamento (UE) 2023/956 del Parlamento Europeo y del Consejo, de 10 de mayo de 2023, por el que se establece un mecanismo de ajuste en frontera por carbono. Diario Oficial de la Unión Europea, L 130, 52–104.

Reglamento (UE) 2025/40 del Parlamento Europeo y del Consejo, de 22 de enero de 2025, relativo a los envases y residuos de envases. Diario Oficial de la Unión Europea. https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32025R0040

Reglamento (UE) 2025/1093 de Ejecución de la Comisión, por el que se establece la clasificación de países por nivel de riesgo a efectos del Reglamento (UE) 2023/1115. Diario Oficial de la Unión Europea.

Reglamento (UE) 2025/2650 del Parlamento Europeo y del Consejo, de 19 de diciembre de 2025, por el que se modifica el Reglamento (UE) 2023/1115 en lo que respecta a determinadas obligaciones de los operadores y comerciantes. Diario Oficial de la Unión Europea. https://eur-lex.europa.eu/eli/reg/2025/2650/oj

SAI Platform. (2022). *Farm Sustainability Assessment (FSA) version 3.0: Methodology and scoring guide*. Sustainable Agriculture Initiative Platform. https://saiplatform.org/fsa/

Team Europe Initiative on Deforestation-free Value Chains. (2025). *EUDR preparación assessment: Coffee, rubber and timber value chains in Vietnam*. European Commission.

UNDP. (2010). *Human Development Report 2010: The real wealth of nations — Pathways to human development*. United Nations Development Programme. https://hdr.undp.org/content/human-development-report-2010

Vargas, G., & Willems, S. (2017). *Línea base de deforestación en zonas cafetaleras peruanas*. PNUD/MIDAGRI.

---

## 10. Protocolos de campo para el piloto (v0.3)

*Esta sección es nueva en v0.3. Recoge los procedimientos operativos derivados de las recomendaciones del DT-ISCAM-001 (versión 4.0, sección 8.1) para la Fase 1 del piloto. Su audiencia es el equipo de campo, no el lector académico del documento.*

### 10.1 Calibración de D3 con OSCE — organizaciones sin puntaje en Neon

**Problema:** D3.Q11–Q14f se sustentan en puntajes Neon/OSCE para organizaciones que ya tienen inh. vigente o registro público. Para organizaciones sin puntaje en la base Neon (`proveedores_sancionados.inhabilitaciones`), el puntaje D3 depende solo de las respuestas autodeclaradas.

**Procedimiento de calibración:**

1. **Antes de la visita**, ejecutar consulta a Neon para el RUC de la organización:
   - Endpoint: `neon(proveedores_sancionados.inhabilitaciones)` filtrado por RUC
   - Si el RUC aparece con inh. vigente → D3 puntaje parcial = 0 por Neon, usar preguntas Q11–Q14f para documentar la brecha específica
   - Si el RUC no aparece → registrar "RUC no encontrado en Neon" y proceder con preguntas Q11–Q14f

2. **Si el RUC no está en Neon pero la organización tiene contratos con el Estado:**
   - Consultar OSCEcheck (`oscecheck.pe`) buscando el RUC en la lista de proveedores inhabilitados
   - Descargar bulk CSV si la organización no aparece: contrastar NIT de SUNAT con la lista OSCE

3. **Si la organización tiene puntaje D3 bajo (≤2) por autodeclaración:**
   - Marcar D3.Q11 = "No verificado" con nota de campo: "puntaje OSCE no disponible; se requiere consulta directa a OSCE para confirmar"
   - No inventar un puntaje más alto; dejar que el diagnóstico refleje la incertidumbre

4. **Después de la visita**, reportar al equipo ISCAM: organizaciones sin puntaje OSCE verificable → lista para consulta OSCE masiva

**Responsable:** técnico de campo + responsable de datos OSCE (rol separado).  
**Tiempo adicional estimado:** 10–15 minutos por organización.

### 10.2 Evaluación de comprensibilidad de D15.Q56–Q60 en piloto

**Problema:** Las preguntas Q56–Q60 usan vocabulario técnico (LMR, RASFF, análisis de residuos) que puede no ser conocido por el responsable técnico de campo en cooperativas pequeñas.

**Protocolo de evaluación (aplicar en las primeras 5–8 cooperativas piloto):**

Para cada pregunta, antes de registrado el valor:

1. **Preguntar al informante** si entiende el concepto antes de responder. Si no lo entiende:
   - Registrar: "Concepto no conocido por el informante. Alternativa usada: [describir]."
   - No inducir la respuesta con una definición antes de que intente responder primero.

2. **Puntos críticos a verificar:**

| Pregunta | Concepto riesgo | Qué observar en el piloto |
|---|---|---|
| Q56 | "LMR de la UE" vs. LMR DIGESA/SENASA Perú | El técnico puede confundir requisitos nacionales con requisitos de frontera UE |
| Q57 | "Protocolo interno de pesticidas" vs. "lista de prohibidos SENASA" | Son cosas distintas; un protocolo EU requiere evidencia de que se supervisa en campo, no solo que existe un documento |
| Q58 | "Análisis de residuos" vs. "control de calidad general" | El técnico puede reportar que "sí hace análisis" referring a control de calidad del grano, no a residuos de pesticidas |
| Q59 | Aplica solo a orgs. con comprador EU | Una cooperativa que nunca exportó a la UE puede responder "no ha exigido" cuando la pregunta no aplica |
| Q60 | "Rechazo en frontera" vs. "rechazo por calidad del grano" | El técnico puede confundir un rechazo comercial (calidad) con un rechazo por LMR |

3. **Al final de D15**, preguntar al técnico de campo: *"¿Hay alguna pregunta que le resultó difícil de responder o que no entendió bien?"* — registrar la respuesta textual.

4. **Reportar al equipo ISCAM**: número de cooperativas piloto donde hubo incomprensión + alternativa lingüística usada → feedeback para versión final del instrumento.

**Responsable:** entrevistador principal.  
**Tiempo adicional estimado:** 5 minutos por organización.

### 10.3 Lista de verificación de verificación rápida antes de cerrar la entrevista

*Entregar al entrevistador como ficha de control.*

- [ ] ¿Se respondió B0-13 (zona de riesgo deforestación) antes de D1?
- [ ] ¿Se respondió B0-14 (capacidad de verificación en campo)?
- [ ] ¿D3.Q11–Q14f: se consultó Neon/OSCE antes de registrar?
- [ ] ¿D15.Q56–Q60: el técnico entendió los conceptos o se usó alternativa?
- [ ] ¿Q60 (bandera rechazo LMR): se reportó aunque el resto de D15 sea alto?
- [ ] ¿Q10 (bandera mezcla de lotes): se preguntó en acopio, no solo en gerencia?
- [ ] ¿Preguntas retrospectivas P2, P5, P7: se tienen registros contables o se dejaron en blanco?
- [ ] ¿Banderas Q36, Q37: se registró la respuesta exacta sin suavizar?

---

*Documento de trabajo — Grupo ISCAM, Centro de Investigación de la Universidad del Pacífico.*
*Instrumento 2 versión D1–D15 + Bloque P v0.3 · 93 preguntas · 2026-10-12.*
*Para actualizaciones metodológicas del sistema de índices: `ISCAM/Metodologia - Indice de Alineamiento (ISA) y Marco Muestral.md`.*
*Para el texto aplicable en Google Forms: `Instrumentos/Instrumento 2 - Encuesta Cuantitativa.md`.*
*Reproducibilidad: la matriz de la sección 4 se genera automáticamente desde `Scripts/matriz_data.py`.*
