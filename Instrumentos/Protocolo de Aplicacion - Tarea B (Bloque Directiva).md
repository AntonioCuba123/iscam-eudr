# Protocolo de Aplicación — Tarea B: Bloque Directiva (D1, D5, D6, D7, D9, D10)

**Qué resuelve este documento:** la Checklist (`Checklist - Correccion de Encuesta y Aplicacion de Instrumento 2.md`) dejó la Tarea B con 6 pasos (B1–B6). El paso B3 ("aplicar el bloque D1/D5/D6/D7/D9/D10") **ya está resuelto** — el `Instrumento 3 - Guia de Entrevista Semiestructurada.md` ya trae las preguntas de entrevista para las seis dimensiones, dirigidas a directiva/gerencia. No hay que crear un guion nuevo.

Lo que faltaba, y que ningún instrumento existente cubre explícitamente, es la parte operativa: **a quién se entrevista según cada dimensión, con qué muestra, y cómo se cruza D10 contra los datos de productores**. Eso es lo que resuelve este protocolo (B1, B2, B5, B6).

---

## B1 — Informante correcto por dimensión

El Instrumento 3 asume "gerencia y personal técnico" como bloque genérico. En la práctica, aplicar las 6 dimensiones a una sola persona produce respuestas débiles en las que esa persona no tiene información directa. Antes de agendar la entrevista, identificar y — si es posible — convocar a más de un rol:

| Dimensión | Informante primario | Informante secundario (si existe el cargo) | Por qué importa la distinción |
|---|---|---|---|
| D1 — Clasificación regulatoria | Gerente general / representante legal | Asesor legal o contable externo | Es una pregunta de estatus jurídico-comercial; el personal técnico de campo típicamente no la sabe con certeza |
| D5 — Sistema de diligencia debida | Responsable técnico o de cumplimiento (si existe el cargo) | Gerente general, si no existe el cargo dedicado | Si nadie tiene el cargo, esa ausencia **es** el dato (D5.20 = "No") |
| D6 — Capacidad organizacional y digital | Gerente general o administrador | Encargado de sistemas/TI si existe | Presupuesto y conectividad son decisiones de gerencia, no de campo |
| D7 — Cadena de valor | Gerente comercial / quien negocia con el comprador | Gerente general | Es la única persona que sabe qué ha exigido realmente el comprador por escrito vs. de palabra |
| D9 — Sostenibilidad económica | Tesorería / gerencia administrativa | Gerente general | Requiere ver o al menos conocer cifras — no es una pregunta de percepción general |
| D10 — Certificación vs. EUDR | Gerente general **y** responsable de certificaciones si existe | — | Es la dimensión más sensible: si el responsable de certificaciones cree que su certificación cubre el EUDR, esa creencia probablemente ya se transmitió a los socios — entrevistarlo es más informativo que entrevistar solo a gerencia |

**Regla práctica:** si la cooperativa es pequeña y una sola persona cubre varios roles, está bien entrevistar a una sola persona para varias dimensiones — pero registrar explícitamente en la ficha de la entrevista qué cargo(s) ocupa esa persona, para poder interpretar después por qué ciertas dimensiones (ej. D9) tuvieron respuestas vagas si la persona no maneja las cifras.

---

## B2 — Selección de la muestra

1. Partir del universo de cooperativas ya cubiertas por la encuesta de productores (Tarea A / campo), no de una lista nueva — el objetivo es completar el diagnóstico de cooperativas que ya tienen datos de D2/D3/D4, no abrir un frente nuevo.
2. Aplicar primero el **Instrumento 5 (Ficha de Triaje Rápido)** a cada cooperativa del universo, si no se hizo antes de la encuesta de productores. El triaje prioriza por:
   - Volumen/relevancia de exportación a la UE.
   - Señales de riesgo ya visibles en los datos de campo (ej. alta proporción de "Sí" en la pregunta 26/v2 "talado bosque desde 2021", o bandera D2.10 activa por las preguntas 84–85/v2).
3. Priorizar para la entrevista de directiva, en este orden:
   - Cooperativas con banderas activas detectadas en el campo (D2.10, D3 trabajo forzoso, D4 deforestación post-2021) — la entrevista de directiva es la única forma de entender la causa y la respuesta organizacional a esas banderas.
   - Cooperativas con mayor volumen de exportación a la UE (mayor impacto de negocio si fallan).
   - El resto, según capacidad de agenda disponible.
4. Meta mínima razonable: al menos **una cooperativa por cada categoría de riesgo** que resulte del triaje (alto/medio/bajo), no solo las de mayor riesgo — para poder comparar y no sesgar las conclusiones de D1–D11 hacia los casos más problemáticos.

---

## B4 — Registro en la Brújula de Diligencia

- Completar el semáforo D1–D9 de la cooperativa en el Artifact solo cuando estén las seis dimensiones de directiva (D1, D5, D6, D7, D9) **y** las de campo (D2, D3, D4) ya cargadas — evitar publicar un semáforo parcial que promedie solo 5 de 9 dimensiones sin dejarlo indicado como incompleto.
- Cargar D10 como bandera (no como parte del promedio) apenas se tenga la respuesta de directiva, siguiendo el mismo criterio ya implementado en el panel (ver Instrumento 7, §5).
- Cargar D8 con los proxies de campo (preguntas 22/23 en v2 del form, ver Puente) más lo que aporte la entrevista de directiva sobre D8.31/D8.32 (mecanismo formal de entrega de información, rotación de directiva) — D8 es la única dimensión extendida que combina fuente de campo + fuente de directiva, documentarlo así en el panel para no perder esa trazabilidad.

## B5 — Cruce D10: directiva vs. productores

1. Una vez aplicada la pregunta núcleo de D10 a la directiva (Instrumento 3) **y** disponible la respuesta equivalente de productores (pregunta 21/v2 del form corregido, condicional a tener certificación), construir la comparación:

| Caso | Directiva cree que la certificación cubre el EUDR | Productores creen que la certificación cubre el EUDR | Lectura |
|---|---|---|---|
| A | Sí | Mayoría sí | Falsa seguridad institucionalizada — el mensaje equivocado viene de arriba y se replicó. Prioridad alta de corrección. |
| B | Sí | Mayoría no/no sabe | Rareza: la directiva está mal informada pero no lo ha comunicado así a los socios (o los socios no le creen). Igual prioridad de corrección en directiva, pero el daño aún no se propagó. |
| C | No, sabe que son distintas | Mayoría sí | El malentendido nace en la base, no en la dirigencia — la corrección debe ir dirigida a campo/socios (capacitación), no a gerencia. |
| D | No | Mayoría no/no sabe | Coherente y de menor prioridad — reforzar con información, no corregir un malentendido activo. |

2. Documentar el caso resultante en la ficha de la cooperativa como hallazgo cualitativo aparte de la bandera binaria D10 — el Instrumento 4 (Matriz de Brechas y Oportunidades) debería recibir este hallazgo como insumo para la recomendación específica (capacitación a socios vs. corrección a directiva).

## B6 — Actualización del Puente

Cada vez que se cierre una cooperativa (campo + directiva completos), actualizar la tabla resumen de cobertura del `Puente - Mapeo Encuesta Productor a Dimensiones D1-D11.md`:
- Mover la fila de la dimensión correspondiente de "Aplicar Instrumento 2 a directiva/gerencia" a "Cubierto — ver ficha de [nombre de cooperativa] en la Brújula".
- Mantener el Puente como documento de **diseño del mapeo** (no como bitácora de campo) — el detalle de qué cooperativa está en qué estado va en la Brújula de Diligencia, no aquí. El Puente solo se actualiza para reflejar que el gap de diseño ya fue cerrado en la práctica, la primera vez que ocurre.

---

## Checklist de cierre de la Tarea B por cooperativa

- [ ] Identificado el informante por dimensión (B1) y registrado su cargo.
- [ ] Cooperativa priorizada según triaje (B2), con su categoría de riesgo anotada.
- [ ] Entrevista aplicada con el guion del Instrumento 3, D1/D5/D6/D7/D9/D10 (B3 — ya resuelto, solo ejecutar).
- [ ] Resultados cargados en la Brújula de Diligencia (B4), semáforo D1–D9 completo (no parcial).
- [ ] Cruce D10 directiva-productores realizado y clasificado en uno de los 4 casos (B5).
- [ ] Puente actualizado si esta cooperativa cierra por primera vez un gap de diseño (B6).
