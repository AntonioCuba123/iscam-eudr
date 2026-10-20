# Lista de verificación — Tareas pendientes para cerrar la alineación operativa

Referencia: `Puente - Mapeo Encuesta Productor a Dimensiones D1-D11.md` (brechas identificados), `Instrumento 7 - Evaluacion Critica y Elementos Adicionales.md` (decisiones de alcance) y `Metodologia - Indice de Alineamiento (ISA) y Marco Muestral.md` (diseño del ISA).

**Aclaración de estado (2026-09-16):** ninguna cooperativa tiene datos reales todavía. El PDF de la encuesta de campo es el **formulario vacío** (estructura de preguntas, sin respuestas). Los dos casos en la Brújula de Diligencia son ejemplos marcados `esEjemplo:true`. Esto **reordena las prioridades**: no hay nada que "corregir en datos ya recolectados" — todo el trabajo pendiente es de diseño y de arranque de campo real. La Tarea A (corregir el form) se puede aplicar ya mismo, sin ningún costo de migración de respuestas, porque no hay respuestas que migrar. Las Tareas C y D (nuevas, abajo) son ahora bloqueantes reales antes de que la Tarea B tenga sentido: no se puede entrevistar directiva de "la muestra" si la muestra todavía no existe como lista concreta de organizaciones.

**Orden de ejecución recomendado:** A → C → (piloto, dentro de C) → B → D en paralelo con B.

**Avances 2026-09-16 (posteriores al reordenamiento de arriba):**
- El **Bloque P** (Tarea D) ya está insertado en el Instrumento 2 — ver Tarea D abajo, actualizada.
- El Instrumento 2 completo (Bloque 0 + Bloque P + D1–D11) ya existe como **encuesta aplicable en línea**, con guardado compartido en vivo para piloto interno: https://claude.ai/code/artifact/5b99e447-cbce-46e6-ae84-195b3ea34fbd — cada módulo trae descripción y ayuda de llenado. Sirve directamente para ejecutar **C7**. Limitación conocida: solo funciona para gente de la organización de Claude del usuario — no apto todavía para las 100–150 cooperativas externas (ver Tarea C).
- La **Metodología del ISA** se corrigió en tres puntos reales (no cosméticos): agregación aritmética → **geométrica híbrida** en D1–D9 (evita que una dimensión núcleo en 0 quede "escondida" por un promedio alto en otras), post-estratificación por celda → **raking** (más estable con 100–150 casos repartidos en ~24 celdas), y se agregó **PCA** como chequeo de robustez de los pesos una vez haya datos reales. Ver `Metodologia...md` §0, §2.3, §3, §4.

---

## Tarea A — Corregir el Google Form (`Encuesta - Formularios de Google.pdf`, edit en línea)

- [ ] **A1. Eliminar duplicado de las preguntas 89 y 90.** Son literalmente la misma pregunta ("¿Su cooperativa o comprador le ha informado sobre requisitos ambientales o sociales que debe cumplir?"). Decidir cuál se mantiene o si la 90 debía ser una pregunta distinta (revisar el diseño original de la sección "Debida diligencia en sostenibilidad" para saber qué faltaba realmente).
- [ ] **A2. Revisar duplicado de las preguntas 104 y 105.** Ambas preguntan por información de emisiones GEI; 105 solo agrega la definición extendida entre paréntesis. Confirmar si 104 debía eliminarse o si estaba pensada como una pregunta de seguimiento distinta.
- [ ] **A3. Agregar la pregunta núcleo de D10** inmediatamente después de la Q20 ("¿Cuenta con alguna certificación?"), condicional a marcar alguna certificación:
  > *"¿Considera que esta certificación ya cumple con los requisitos del reglamento europeo de deforestación (EUDR)?"*
  > Opciones: Sí, totalmente / Sí, en parte / No, son cosas distintas / No tiene certificación.
- [ ] **A4. Completar las opciones de actor en las preguntas 21 y 22** (capacitación y asistencia técnica por fuente), agregando:
  - "Junta Nacional del Café / APPCACAO u otro gremio"
  - "PNCB-MINAM (monitoreo satelital)"
- [ ] **A5. (Opcional, mejora de cobertura D3)** Evaluar si conviene agregar en el form las dos preguntas de agua ya incorporadas al Instrumento 2 (14a/14b: autorización de uso de agua, cumplimiento de tratamiento de aguas residuales) — hoy el form solo pregunta *de dónde* procede el agua (Q46) y *si tiene autorización* (Q47) de forma parcial; verificar que Q47 cubra completamente 14a o si falta granularidad.
- [ ] **A6. Republicar el form** y anotar la fecha de la nueva versión — para no mezclar respuestas de la versión con duplicados con las de la versión corregida al analizar resultados.

---

## Tarea B — Aplicar el Instrumento 2 (bloques D1, D5, D6, D7, D9, D10) a la directiva/gerencia de cada cooperativa

Estas seis dimensiones no tienen ninguna fuente de dato todavía porque dependen de decisiones organizacionales, no del productor individual.

- [ ] **B1. Definir el informante correcto por dimensión** (no siempre es la misma persona):
  - D1 (clasificación regulatoria) y D7 (cadena de valor) → gerente/responsable comercial, quien negocia con el comprador.
  - D5 (sistema de diligencia debida) y D6 (capacidad organizacional/digital) → responsable técnico o de cumplimiento, si existe el cargo.
  - D9 (sostenibilidad económica) → tesorería o gerencia administrativa.
  - D10 (confusión certificación/EUDR) → puede aplicarse tanto a la directiva como triangularse con lo que ya se sabe de los productores (Q20/Q23 del form), pero **la pregunta núcleo de D10 debe hacerse a nivel organización**, no inferirse solo de productores.
- [ ] **B2. Seleccionar la muestra de cooperativas** a las que se aplicará esta ronda — idealmente cruzando con el Instrumento 5 (Ficha de Triaje Rápido) para priorizar por riesgo/tamaño antes de gastar tiempo de entrevista en las 100+ preguntas restantes del marco.
- [ ] **B3. Aplicar el bloque D1, D5, D6, D7, D9, D10 del Instrumento 2** (formato entrevista estructurada, no encuesta auto-administrada — ver Instrumento 3 para el guion de entrevista semiestructurada que puede adaptarse a estos bloques).
- [ ] **B4. Registrar los resultados en la Brújula de Diligencia** (Artifact ya implementado) para la cooperativa correspondiente, completando el semáforo D1–D9 que hoy solo puede calcularse parcialmente con datos de campo (D2, D3, D4).
- [ ] **B5. Cruzar D10 (bandera de falsa seguridad) obtenida de la directiva contra la percepción de los productores** (Q20/Q23 del form, una vez corregido con A3) — si hay una brecha grande entre lo que cree la directiva y lo que creen los productores, documentarlo como hallazgo aparte (posible mensaje interno inconsistente sobre el tema).
- [ ] **B6. Actualizar el Puente** con los datos reales obtenidos, moviendo cada dimensión de "brecha" a "cubierto" en la tabla resumen de cobertura, a medida que se van cerrando cooperativa por cooperativa.

---

## Tarea C — Construir el marco muestral real (bloqueante para B)

Ver `Metodologia - Indice de Alineamiento (ISA) y Marco Muestral.md`, §1. Sin esto, B no tiene a quién entrevistar.

- [~] **C1. Directorio JNC (café) — avance parcial 2026-09-16.** Ver `Directorio Preliminar - JNC y APPCACAO.md`: ~18 de 56-62 organizaciones identificadas por búsqueda pública (≈30% de cobertura); el sitio oficial devuelve error de servidor en sus páginas internas. Falta solicitud formal directa a JNC para el directorio completo y para N° de socios/hectáreas por organización.
- [~] **C2. Directorio APPCACAO (cacao) — avance parcial 2026-09-16.** Ver mismo documento: 24 de ~25+ organizaciones identificadas vía la página "Explorar los Orígenes" (≈95% de cobertura estimada), ya agrupadas por macro-región. Falta confirmar por contacto directo si hay asociadas no listadas ahí, y obtener N° de socios/hectáreas.
- [ ] **C3. Complementar con el padrón de MIDAGRI/DRA regionales** donde JNC/APPCACAO no cubran (organizaciones no afiliadas a gremio).
- [ ] **C4. Obtener los totales poblacionales del último CENAGRO disponible** por región/producto — no como marco de selección, sino como insumo de calibración ex-post (Metodología §3). Esto puede hacerse en paralelo, no bloquea el inicio de C1-C3.
- [ ] **C5. Construir la tabla de cuotas real** (Producto × Vía de exportación × Tamaño × Territorio) a partir de C1-C3, y verificar qué celdas de la Metodología §1.2 tienen incidencia real baja o nula en el universo peruano (ej. cooperativas "grandes" de cacao) para ajustar la meta por celda en vez de forzarla.
- [ ] **C6. Seleccionar las 5-8 organizaciones piloto** (Metodología §1.4) cubriendo al menos 3 de las celdas de mayor incidencia esperada.
- [ ] **C7. Aplicar el piloto** con el Instrumento 2 v2 (con 14a/14b y Bloque P) — ya disponible como encuesta en línea con guardado en vivo: https://claude.ai/code/artifact/5b99e447-cbce-46e6-ae84-195b3ea34fbd. Revisar tiempo de aplicación, comprensibilidad y no-respuesta por ítem antes de escalar a las 100-150 organizaciones. Activar el enlace desde el menú de compartir del artifact para que el equipo del piloto pueda responder.
- [ ] **C8. (nuevo, depende de C7) Correr el Análisis de Componentes Principales (PCA)** sobre los datos de la primera ronda completa — no del piloto de 5-8 casos, que no alcanza — para validar el esquema de pesos de la Metodología §2.3/§4. No es bloqueante para avanzar a B, pero sí para reportar el ISA como definitivo en vez de provisional.

> Nota: esto es trabajo de campo/gestión institucional (contactar gremios, pedir directorios), no de escritorio — no lo puedo ejecutar yo directamente, pero puedo ayudar a redactar la solicitud formal a JNC/APPCACAO/MIDAGRI si es útil, o buscar si alguno de estos directorios ya es público.

## Tarea D — Definir la variable de desempeño (objetivo f del proyecto madre)

Ver `Metodologia...md`, §5. **Actualización 2026-09-16:** D1 ya tiene un borrador aplicable — se agregó el **Bloque P** al `Instrumento 2 - Encuesta Cuantitativa.md` con 10 preguntas de desempeño (volumen exportado UE, N° compradores europeos, precio pagado al socio, rechazos/pérdida de contratos, cada una con su versión retrospectiva a 3 años). Falta la validación formal con el equipo del proyecto madre antes del levantamiento definitivo, pero ya no bloquea el piloto (Tarea C7).

- [x] **D1 (borrador).** Bloque P insertado en el Instrumento 2 — pendiente solo la validación/ajuste con el equipo del proyecto madre, no el diseño desde cero.
- [ ] **D1b. Validar el Bloque P con el equipo del proyecto madre** — confirmar que los 4 indicadores elegidos (volumen, N° compradores, precio al socio, rechazos/pérdida de contrato) son los que ellos esperan, o ajustar antes de que el piloto los fije de facto.
- [x] **D2 (resuelto por diseño).** El Bloque P ya incluye la solución de "proxy retrospectivo" (P2, P5, P7 preguntan la cifra de hace 3 años) para aproximar tendencia sin necesitar panel real — documentado en el propio Bloque P y en la Metodología §5 como limitación explícita a declarar en cualquier reporte (asociación transversal, no causalidad).
- [x] **D3 (resuelto).** Las preguntas de desempeño ya están insertadas — como Bloque P propio, no dentro del Bloque 0 (más limpio: el Bloque 0 es identificación fija de la organización, el Bloque P es resultado de negocio, tienen naturalezas distintas). El modelo de análisis (correlación, cuartiles) quedó documentado en la Metodología del ISA, §5.

---

## Orden recomendado

**A → C → B, con D en paralelo a B una vez que exista variable de desempeño decidida.** A no depende de nada (edición de un formulario vacío, sin datos que preservar) y puede hacerse ya. C es hoy el verdadero cuello de botella: sin marco muestral real no hay a quién aplicarle ni el Instrumento 2 ni el Protocolo de Tarea B. D puede decidirse en paralelo a C/B porque es una conversación con el equipo del proyecto madre, no un paso de campo — pero debe estar resuelta antes de reportar cualquier resultado sobre "impacto en desempeño", o el entregable prometerá algo que la metodología en curso no puede sustentar.
