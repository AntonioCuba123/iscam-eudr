# Plan de Trabajo — Próximos 75 días

**Fecha de elaboración:** 2026-09-17. **Horizonte:** día 1 (~2026-09-18) a día 75 (~2026-12-01).

**Punto de partida:** el diseño metodológico (D1–D11, ISA, IP, IV, RE, AHP) está esencialmente cerrado y sincronizado en sus 4 formatos (Word, artifacts, Excel, matriz de cobertura). Lo que falta no es más diseño — es **ejecución**: convocar al equipo del proyecto madre, cerrar el marco muestral, correr un piloto real y recalibrar con datos reales. Este plan asume eso: prioriza desbloquear dependencias externas primero, porque son las que tienen el mayor tiempo de espera y no se pueden acelerar trabajando más rápido internamente.

**Cómo leer este plan:** cada tarea tiene una etiqueta de propietario:
- 🟢 **Interno** — se puede avanzar sin depender de nadie más
- 🟡 **Mixto** — requiere una acción externa puntual (una reunión, una aprobación) pero el trabajo pesado es interno
- 🔴 **Externo/bloqueado** — depende enteramente de terceros (equipo madre, gremios, panel AHP); solo se puede *iniciar* el contacto, no forzar el ritmo

---

## Regla de secuenciación

Las tareas 🔴 se inician el **día 1**, no cuando "haya tiempo" — son las que tienen el lead time más largo de todo el plan (convocar 8–10 expertos, conseguir inputs del equipo madre) y correrlas en paralelo desde el inicio es lo único que hace viable el horizonte de 75 días. Todo lo demás se organiza alrededor de esa espera, no al revés.

---

## Fase 0 — Días 1–5: Desbloqueo y kickoff

| Tarea | Propietario | Detalle |
|---|---|---|
| Enviar solicitud formal de inputs al equipo del proyecto madre (ISCAM/UP) | 🔴 | Nombres del equipo de investigación, validación del Bloque P (objetivo f), totales de población para calibración de la muestra. Ya existe el "Resumen Ejecutivo - Propuesta ISCAM.docx" listo para acompañar el pedido — usarlo. |
| Iniciar convocatoria del panel AHP (8–10 expertos, 5 grupos) | 🔴 | Usar `Directorio - Pool de Expertos Panel AHP.xlsx` como punto de partida; contactar primero a los 5 nombres ya verificados (Delky Gutiérrez, Raquel Condori, Luis Navarro/Antonio Arbe, Carmen Vegas, Pilar Chamorro) — son el núcleo con mayor probabilidad de respuesta rápida. |
| ~~Decidir infraestructura de despliegue~~ — **decidido: Google Forms + Google Sheets** | ✅ | Todo el relevamiento (Instrumento 2, Tarea A, Tarea B, FGD) se hace en Google Forms; cada respuesta se guarda en Google Sheets, que pasa a ser la base de datos real del piloto. Reemplaza cualquier alternativa (KoBoToolbox/ODK, o el artifact `db`-interno como canal de campo). Sigue pendiente decidir el canal de *distribución* del formulario — eventos gremiales y/o piggyback en visitas técnicas (GIZ/SAFE/MIDAGRI) — eso es independiente de la herramienta. |
| Solicitud formal a JNC y APPCACAO (ya redactadas) | 🔴 | `Solicitud Formal - JNC.md` y `Solicitud Formal - APPCACAO.md` ya existen — solo falta enviarlas. |

**Entregable de fase:** 3 solicitudes externas enviadas, panel AHP con contacto iniciado, estrategia de despliegue decidida.

---

## Fase 1 — Días 6–25: Marco muestral y forma de campo

Mientras se espera respuesta externa (Fase 0), el trabajo interno se concentra en dejar el instrumento y el marco muestral listos para ejecutar en cuanto llegue luz verde.

| Tarea | Propietario | Detalle |
|---|---|---|
| Completar Tarea C — marco muestral | 🟢/🟡 | Acceder al Directorio Nacional de Cooperativas de PRODUCE (necesita navegador interactivo, no fetch) y solicitar el RNCA de MIDAGRI. Objetivo: pasar de 46 a ~100–150 organizaciones con RUC verificado. |
| Aplicar Tarea A — correcciones al Google Form vivo (encuesta a productores) | 🟡 | `Encuesta Productor - Version Corregida v2.md` ya tiene las 107 preguntas corregidas — falta que alguien con acceso a Google Forms lo aplique (el asistente no puede editarlo directamente). |
| Construir el Google Form de Instrumento 2 (Bloque 0 + Bloque P + D1–D11) | 🟡 | Traducir las 76 preguntas de `Instrumento 2 - Encuesta Cuantitativa.md` a un Google Form real, con las respuestas cayendo a una Google Sheet — reemplaza al artifact `db`-interno como instrumento de campo (ese artifact queda solo como piloto/demo interno). El asistente puede dejar listo el texto/estructura exacta pregunta por pregunta; la creación del Form en sí requiere acceso a Google Forms. |
| Definir la estructura de la Google Sheet de respuestas | 🟢 | Una fila por cooperativa/respuesta, columnas = IDs de pregunta (mismo esquema que `matriz_data.py`) para que el análisis posterior (Excel de cálculo IP/IV/RE) pueda leerla sin reconciliar nombres de columna a mano. |
| Cerrar definición de "fricción D8 → IV5" | 🟢 | Pendiente documentado en Diseño IV — decidir qué ítems exactos de D8 cuentan como fricción antes de que el piloto genere datos que dependan de esa definición. |
| Preparar protocolo de 1 página para field staff (piggyback GIZ/SAFE) | 🟢 | Si se usa ese canal de distribución — formaliza cómo el personal técnico externo aplica el Google Form durante sus visitas ya programadas. |

**Entregable de fase:** marco muestral con ≥100 organizaciones verificadas por RUC, formulario de campo listo para aplicarse (vía el canal elegido), Tarea B con roles y muestra de cooperativas priorizadas confirmada.

---

## Fase 2 — Días 26–50: Piloto de campo

Esta fase depende de que la Fase 0 haya dado al menos una respuesta parcial (ej. acceso a un evento gremial, o autorización de un proyecto de cooperación para el piggyback). Si a día 26 no hay ninguna respuesta externa, esta fase se retrasa proporcionalmente — es el riesgo principal del plan, y no es resoluble desde el lado interno.

| Tarea | Propietario | Detalle |
|---|---|---|
| Ejecutar Tarea B — entrevistas a directiva (5–8 cooperativas piloto) | 🟡 | Usar `Protocolo de Aplicacion - Tarea B (Bloque Directiva).md` — prioriza cooperativas con banderas rojas ya detectadas en datos de campo existentes. Llena D1/D5/D6/D7/D9/D10, hoy vacíos para todas las organizaciones. |
| Aplicar Instrumento 2 completo a la muestra piloto (Google Forms) | 🟡 | Meta realista para 25 días de campo: 15–25 cooperativas, no las 100–150 completas (eso es un piloto, no el levantamiento final). |
| Correr al menos 1 grupo focal (FGD) con socios de base | 🟡 | Usar el anexo ya redactado en Instrumento 3 — moderador distinto de quien entrevistó a la directiva de esa misma cooperativa. |
| Monitoreo semanal de calidad de datos entrantes | 🟢 | Revisar consistencia (ej. D10 vs. certificaciones de Bloque 0), completitud, y banderas D2.10/D10/D3.14 apenas entren respuestas — no esperar al final del piloto para detectar errores de captura. |

**Entregable de fase:** datos reales de 15–25 cooperativas en Instrumento 2 + Bloque P, entrevistas de directiva de esas mismas organizaciones, al menos 1 FGD documentado.

---

## Fase 3 — Días 51–65: Panel AHP y recalculo con datos reales

| Tarea | Propietario | Detalle |
|---|---|---|
| Ejecutar el panel AHP (si ya está convocado desde Fase 0) | 🔴/🟡 | Usar el wizard ya construido (artifact 323b416c-...). Sesión de nivelación conceptual → comparaciones individuales → chequeo CR → agregación AIJ (ver el diagrama del proceso ya publicado). |
| Recalcular IP/IV/RE con datos reales del piloto | 🟢 | Exportar la Google Sheet de respuestas y cargarla en el Excel `Modelo de Calculo - ISA-IP-IV-RE-AHP.xlsx`, reemplazando las 8 filas de ejemplo sintético por los datos reales de las 15–25 cooperativas piloto. |
| Fijar el corte alto/bajo de la matriz de tipología 2×2 | 🟢 | Ahora sí con mediana muestral real, no arbitraria (documentado como pendiente en el Diseño IV). |
| Verificación de sensibilidad (Spearman, pesos AHP vs. pesos iguales) | 🟢 | Paso 6 del proceso AHP — obligatorio antes de reportar cualquier resultado como definitivo. |
| Validar Bloque P con el equipo madre (si respondieron en Fase 0) | 🟡 | Confirmar si los 10 indicadores de desempeño siguen siendo los que el objetivo (f) necesita, o si requieren ajuste. |

**Entregable de fase:** pesos AHP reales (no 20% parejo), ISA/IP/IV/RE calculados con datos reales de 15–25 cooperativas, matriz de tipología con corte real, y validación (o ajuste) de Bloque P.

---

## Fase 4 — Días 66–75: Consolidación y reporte

| Tarea | Propietario | Detalle |
|---|---|---|
| Redactar informe de piloto (metodología + hallazgos + limitaciones) | 🟢 | Instrumento 6 ya tiene la estructura de nota metodológica — se usa como esqueleto. |
| Sincronizar todos los artifacts/Word/Excel con los datos y decisiones reales del piloto | 🟢 | Reemplazar los datos de ejemplo (`esEjemplo:true`) por los reales o por un resumen agregado anónimo, según lo que se decida compartir. |
| Documento de recomendaciones para el levantamiento completo (100–150 orgs) | 🟢 | Qué funcionó del canal de despliegue elegido, qué preguntas generaron más "no sabe"/abandono, ajustes de tiempo de aplicación real vs. estimado. |
| Presentación de resultados al equipo del proyecto madre | 🟡 | Cierre del ciclo de 75 días — pedir su decisión sobre si se procede al levantamiento completo con este diseño o se ajusta antes. |

**Entregable de fase:** informe de piloto, toolkit actualizado con evidencia real (ya no solo diseño teórico), y una decisión explícita del equipo madre sobre los siguientes pasos.

---

## Riesgos explícitos del plan

1. **El riesgo más grande no es técnico, es de dependencia externa.** Si el equipo del proyecto madre o los gremios no responden en los primeros 15–20 días, todo el plan se corre — no hay forma de compensarlo trabajando más rápido en las tareas internas, porque el piloto de campo (Fase 2) no puede empezar sin al menos un canal de acceso a cooperativas reales.
2. **75 días alcanza para un piloto (15–25 organizaciones), no para el levantamiento completo (100–150).** Si la expectativa real es tener el ISA/IP/IV/RE de las 100–150 organizaciones en 75 días, ese alcance no es realista dado que hoy no existe ni un solo dato de campo real — este plan lo dice explícitamente en vez de prometer un alcance que no se puede sostener.
3. **El panel AHP tiene el lead time más largo de todo el plan.** Convocar 8–10 expertos de 5 grupos distintos, coordinar 30–45 min de su tiempo cada uno, y dejar margen para una ronda de revisión de consistencia, típicamente toma más de 30 días en proyectos similares — por eso se inicia el día 1, no se agenda "cuando el piloto esté listo".

---

**Estado:** documento de trabajo, 2026-09-17. Revisar y ajustar fechas una vez se tenga la primera respuesta real de alguna de las tareas 🔴 de la Fase 0 — este plan es un punto de partida planificado, no un compromiso fijo, porque depende de terceros que el equipo no controla.
