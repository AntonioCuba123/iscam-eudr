# Ficha Técnica y Guía de Aplicación — Instrumento 2 (Encuesta Cuantitativa EUDR)

**Serie:** parte del paquete de 7 instrumentos. **Documento único** que reemplaza lo que originalmente se planteó como 3 documentos separados (ficha técnica, guía metodológica, guía de llenado) — consolidado a pedido del usuario para tener un solo punto de referencia. Tres secciones, cada una respondiendo una pregunta distinta:

1. **Ficha técnica** — ¿qué es esta encuesta, a quién se aplica, cómo se seleccionó la muestra?
2. **Guía metodológica** — ¿por qué el instrumento está diseñado así (dimensiones, escala, agregación)?
3. **Guía de llenado** — ¿quién responde cada bloque y qué hacer ante la duda al aplicar?

**Efecto en el resto del toolkit (ver §4 al final):** este documento absorbe contenido que antes vivía repartido en `Instrumento 6`, `Metodología - Índice de Alineamiento (ISA) y Marco Muestral.md` y las notas "Cómo llenar" del formulario online. Esos documentos se recortaron para no duplicar — quedan como la fuente de detalle técnico/matemático (Metodología ISA) y de alcance multi-instrumento (Instrumento 6), y remiten aquí para lo que ahora es la referencia única.

---

## 1. Ficha técnica

### 1.1 Identificación

| Campo | Valor |
|---|---|
| **Nombre del instrumento** | Encuesta Cuantitativa EUDR para Cooperativas Exportadoras de Café y Cacao (Instrumento 2) |
| **Objetivo** | Diagnosticar el nivel de preparación de organizaciones cafetaleras/cacaoteras peruanas frente al Reglamento (UE) 2023/1115 (EUDR), y alimentar el Índice Sintético de Alineamiento (ISA) y los índices de Preparación/Vulnerabilidad (IP/IV) del proyecto madre ISCAM. |
| **Base normativa** | Reglamento (UE) 2023/1115, modificado por Reglamento (UE) 2025/2650. |
| **Entidad/proyecto que ejecuta** | Proyecto "El impacto del Pacto Verde Europeo en la performance de las cooperativas peruanas" (ISCAM, Universidad del Pacífico) — este toolkit opera como su instrumento operativo para el submódulo EUDR. |

### 1.2 Población, unidad de análisis y ámbito

| Campo | Valor |
|---|---|
| **Población objetivo** | Organizaciones productoras de café y/o cacao con estructura asociativa formal (cooperativa o asociación de productores) con potencial exportador directo o indirecto a la UE. |
| **Unidad de análisis** | La organización (cooperativa/asociación), no el productor individual. El productor individual es la unidad de análisis de un instrumento distinto (la encuesta de campo vía Google Form, `Encuesta Productor - Version Corregida v2.md`). |
| **Ámbito geográfico** | Perú, zonas cafetaleras/cacaoteras — macro-regiones Norte (San Martín, Amazonas, Cajamarca), Centro (Junín, Pasco, Huánuco), Sur (Cusco, Puno, VRAEM). |
| **Exclusiones** | Productores individuales sin estructura asociativa formal; organizaciones de otros cultivos no cubiertos por el Anexo I del EUDR. |

### 1.3 Marco muestral y muestra

| Campo | Valor |
|---|---|
| **Tamaño de muestra objetivo (levantamiento completo)** | 100–150 organizaciones — número de conveniencia/recursos, no derivado de cálculo de margen de error. |
| **Tamaño de muestra del piloto (Fase 2, plan a 75 días)** | 15–25 organizaciones. |
| **Estado actual del marco muestral (actualizado 2026-10-06)** | ⚠ **Corrección:** el dato "46 organizaciones" quedó obsoleto el mismo día en que se escribió (2026-09-17) — ese mismo día se cerró la consolidación a **245 organizaciones con RUC validado al 100% por SUNAT** (ver `docs/FUNDAMENTOS_UNIVERSO_ENCUESTABLE.md`), más un banco adicional de 83 organizaciones no exportadoras (universo extendido: 328). De las 245, **177 tienen GPS y contacto directo** (CENCOOP 2017) y **95 no tienen ningún contacto** (ni teléfono ni correo) — ese es el gap real pendiente, no el conteo total. **Tarea C (expansión del marco) está satisfecha**; lo pendiente es enriquecimiento de contacto para esas 95. |
| **Fuentes del marco** | JNC, APPCACAO, padrones MIDAGRI/DRA regionales, CENAGRO (solo como auxiliar de calibración, no de selección), organizaciones ya cubiertas por la encuesta de campo. |
| **Método de muestreo** | **No probabilístico, por cuotas.** Cuatro variables de estratificación: producto principal (café/cacao/ambos), vía de exportación (directa/indirecta/mixta), tamaño (pequeña/mediana/grande, por N° de socios o hectáreas), territorio (Norte/Centro/Sur). Meta mínima: 8–10 organizaciones por celda no vacía de Producto × Tamaño (hasta 24 celdas posibles). |
| **Margen de error / nivel de confianza** | **No aplica.** El diseño es no probabilístico; reportar un margen de error sería atribuir una precisión estadística que el muestreo por cuotas no tiene. En su lugar, se reporta la composición de la cuota lograda y, cuando existan totales poblacionales auxiliares, un ajuste ex-post por **raking** (Deville & Särndal, 1992) como análisis de sensibilidad — nunca como corrección que oculte el sesgo de selección. Detalle matemático completo en `Metodologia - Indice de Alineamiento (ISA) y Marco Muestral.md` §3. |
| **Selección dentro de cada celda** | Intencional, buscando heterogeneidad en antigüedad, presencia/ausencia de certificaciones voluntarias, y nivel de digitalización. |

### 1.4 Instrumento y técnica de recolección

| Campo | Valor |
|---|---|
| **Estructura del instrumento** | Bloque 0 — Ficha de identificación (12 ítems, no puntúa) · Bloque P — Variables de performance (13 ítems, preliminar v0.1 — incluye P11/P12, criterios de validación externa ISCAM) · D1–D11 (⚠ **corregido 2026-10-06: 51 ítems**, no 50 — recuento directo sobre `Instrumento 2 - Encuesta Cuantitativa.md`: D1=4, D2=6, D3=11 [incluye 14a–14g], D4=3, D5=9 [incluye 18a/18b/19a/21a/21b], D6=4, D7=3, D8=4, D9=3, D10=2, D11=2). Total: **76 preguntas** (no 75 — ver `Instrumentos/Estructura Google Sheet - Respuestas Instrumento 2.md` para el detalle columna por columna). |
| **Escala de madurez** | Ordinal 0–4 en las preguntas tipo escala (0 = no existe/no sabe, 4 = implementado y verificado/auditado). |
| **Modo de aplicación** | Autoadministrado o asistido, vía **Google Forms**. |
| **Almacenamiento de respuestas** | **Google Sheets**, una fila por organización/aplicación, columnas por ID de pregunta (mismo esquema de `matriz_data.py`). |
| **Duración estimada de aplicación** | **Por calibrar durante el piloto** — no se declara una cifra sin datos reales (salida esperada de la Fase 4 del plan a 75 días). |
| **Informantes** | Ver §3 (Guía de llenado) — varía por bloque/dimensión, no es una sola persona. |

### 1.5 Periodo de aplicación

| Campo | Valor |
|---|---|
| **Piloto** | Fase 2 del plan a 75 días — días 26 a 50 desde el inicio (aprox. 2026-09-18 + 25 a 50 días). |
| **Línea base general** | Antes de diciembre de 2026, para anticipar la fecha de aplicación general del Reglamento (UE) 2025/2650. |
| **Ronda de seguimiento** | A los 6–9 meses de la línea base, idealmente antes del cierre de la ventana de junio 2027 para organizaciones que califiquen como micro/pequeño operador primario. |
| **Revisión de alta frecuencia** | D10 (percepción sobre certificación) y D11 (ecosistema de apoyo) — revisar en cada ronda aunque el resto del diagnóstico no cambie, por ser sensibles a intervenciones de bajo costo/alto impacto en poco tiempo. |

### 1.6 Confidencialidad, uso y limitaciones declaradas

- Los datos recogidos (RUC, volúmenes exportados, ingresos, precios pagados al socio) son de naturaleza institucional/comercial, no datos personales sensibles de individuos — el sujeto de análisis es la organización, no una persona.
- Uso previsto: diagnóstico interno de la organización, y agregado (sin identificación individual de la cooperativa) para el ISA/IP/IV/RE del proyecto madre.
- **Advertencia de uso:** este instrumento no constituye asesoría legal ni sustituye una auditoría formal de diligencia debida. Su función es diagnóstica y de priorización de recursos.
- **Limitaciones:** (1) no probabilístico, sin margen de error formal; (2) Bloque P es transversal con recall retrospectivo (P2, P5, P7) — cualquier correlación ISA↔performance es asociación, nunca causalidad; (3) marco muestral aún incompleto (46 de ~100–150 objetivo); (4) el piloto (15–25 orgs) no equivale al levantamiento completo.

---

## 2. Guía metodológica (resumen)

**Por qué el instrumento está diseñado así** — versión condensada; el razonamiento completo con citas está en `Instrumento 1 - Marco de Dimensiones de Diagnostico.md`, `Instrumento 7 - Evaluacion Critica y Elementos Adicionales.md` y `Metodologia - Indice de Alineamiento (ISA) y Marco Muestral.md` §0–§2.

- **11 dimensiones, dos niveles:** D1–D7 son núcleo (derivadas directamente del texto del reglamento: clasificación regulatoria, trazabilidad, legalidad, riesgo de deforestación, sistema de diligencia debida, capacidad organizacional, cadena de valor). D8–D11 son extendidas (gobernanza, sostenibilidad económica, confusión certificación/EUDR, ecosistema de apoyo) — se agregaron porque una cooperativa puede puntuar bien en D1–D7 y aun así fracasar en la práctica (Instrumento 7 §1).
- **Escala ordinal 0–4, no libre:** replica la lógica de los modelos de madurez por capacidades (CMMI) — los niveles no son intercambiables, cada uno presupone que el anterior ya está resuelto.
- **Agregación geométrica en el núcleo, no aritmética:** D1–D7 se agregan con media geométrica (no aritmética) porque las dimensiones núcleo no son sustitutos entre sí — una cooperativa no puede compensar la ausencia de diligencia debida (D5=0) con buena geolocalización (D2=4). Mismo precedente que el cambio del IDH-PNUD de aritmética a geométrica en 2010. D8–D9 sí se agregan aritméticamente (son moduladoras, no deberían anular el índice por sí solas).
- **D10 y D11 nunca se promedian como madurez:** D10 es una bandera de falsa seguridad (un puntaje alto sería mala noticia); D11 es un inventario de oportunidades, no una medida de preparación.
- **Regla de datos faltantes — nunca imputar, re-ponderar:** una dimensión sin respuesta se excluye y las restantes del mismo bloque se re-ponderan proporcionalmente; nunca se rellena con la media muestral (sesgaría el índice hacia arriba justo donde debería mostrar el vacío — lógica MNAR de Rubin/Little & Rubin).
- **Remapeo a IP/IV/RE del proyecto madre:** las mismas **75** preguntas alimentan, además del ISA (D1–D9), los índices IP (Preparación) e IV (Vulnerabilidad) del proyecto ISCAM, combinados en RE = IV·(1−IP/100) — detalle completo en `Remapeo D1-D9 a Indice de Preparacion (IP-ISCAM).md` y `Diseno - Indice de Vulnerabilidad (IV-ISCAM).md`.

---

## 3. Guía de llenado

### 3.1 Antes de empezar

- **No es una auditoría ni una certificación.** Es un autodiagnóstico. Responder "No" o "No verificado" no es un mal resultado — es información necesaria para priorizar en qué orden actuar.
- **Escala 0–4:** 0 = no existe/no sabe · 1 = informal o parcial · 2 = en desarrollo · 3 = implementado · 4 = implementado y verificado/auditado.
- **Quién debe estar presente:** ver la tabla 3.3 — cada bloque tiene un informante ideal distinto; no todos los responde la misma persona.

### 3.2 Regla general ante la duda

| Situación | Qué hacer |
|---|---|
| No se sabe la respuesta exacta | Marcar "No sabe" / "No verificado" — nunca inventar un valor optimista sin haberlo consultado realmente. |
| El dato requiere revisar registros que no están a la mano | Dejar el campo vacío y volver a él, en vez de estimarlo de memoria — aplica sobre todo a Bloque P. |
| Una pregunta retrospectiva ("hace 3 años") no se recuerda con certeza | Mejor dejarla vacía que inventar una cifra — se trata como tendencia aproximada. |
| Una pregunta pide información sensible (conflicto social, agua, fajas marginales, tributario) | Responder con honestidad — es mejor "No verificado" que un "No" optimista sin sustento. |

### 3.3 Quién responde cada bloque

| Bloque / Dimensión | Informante ideal | Por qué |
|---|---|---|
| **Bloque 0** (identificación) | Quien tenga acceso a registros de venta/exportación | Datos duros (RUC, volumen, certificaciones), no de memoria. |
| **Bloque P** (performance) | Idem | Las preguntas retrospectivas (P2, P5, P7) son mejor dejarlas vacías que forzar una cifra sin sustento contable. |
| **D1** (clasificación regulatoria) | Gerencia general o asesoría legal/contable | Es estatus jurídico-comercial que el área técnica de campo rara vez maneja con certeza. |
| **D2** (trazabilidad) | Responsable técnico/de campo, junto con gerencia | La pregunta 10 (mezcla de lotes) es una bandera: decirlo aunque el resto de D2 sea alto. |
| **D3** (legalidad) | Gerencia + responsable de campo | Preguntas 14–14g piden información sensible — mejor "No verificado" que un "No" optimista. **Advertencia de verificabilidad:** 14a y 14b son autodeclaradas y **no tienen fuente pública de contraste** (la autorización ambiental agraria la emite MIDAGRI y no está publicada); la 14d (derechos de terceros, desde 2026-10-02) solo admite contraste documental parcial y su "No verificado" se computa como 0. Reportar D3 como *percepción de cumplimiento declarada*, nunca como conformidad verificada. Ver la nota completa en `Instrumento 2 - Encuesta Cuantitativa.md` (D3) y `Memoria Diaria EUDR.md` §8.10.1. |
| **D4** (riesgo de deforestación) | Responsable técnico/de campo | Si nunca se ha verificado, marcar honestamente "No verificado" en la 15. |
| **D5** (sistema de diligencia debida) | Responsable técnico o de cumplimiento, si el cargo existe | Si nadie lo tiene, esa ausencia es el dato correcto en la 20. La 19a es un mapeo, no una escala. |
| **D6** (capacidad organizacional/digital) | Gerencia general o administración | El personal de campo rara vez maneja cifras de presupuesto o digitalización. |
| **D7** (cadena de valor) | Gerencia comercial | La 28 (riesgo percibido) es indicador de urgencia, no de madurez — no se promedia con el resto de D7. |
| **D8** (gobernanza) | Directiva + 1–2 socios de base por separado | La directiva suele ser más optimista sobre "cuánto entienden los socios" que la realidad. |
| **D9** (sostenibilidad económica) | Tesorería o gerencia administrativa | Si quien responde no maneja cifras reales, es preferible anotarlo que forzar una estimación. |
| **D10** (certificación vs. EUDR) | Directiva o gerencia | Sondear con tacto — registrar la respuesta tal cual, sin suavizarla. |
| **D11** (ecosistema de apoyo) | Gerencia o responsable de relaciones institucionales | Marcar solo contacto real y activo, no el simple conocimiento de que el actor existe. |

### 3.4 Banderas y casos especiales — no promediar como el resto

- **D2.10** (mezcla sin control) — bandera roja, anula en la práctica cualquier puntaje alto de las preguntas 5–7.
- **D3.14g** (CLPI) — pregunta de verificación, no promedia dentro de D3. Aplica solo si hay socios en territorio de comunidades indígenas/nativas/campesinas específicas.
- **D5.19a** (componentes del plan) — mapeo (marcar todos los que apliquen), no promedia dentro de D5.
- **D7.28** (riesgo percibido) — indicador de urgencia, no de madurez, no se promedia con el resto de D7.
- **D9** completo — se reutiliza, invertido, como insumo de IV4 (Índice de Vulnerabilidad).
- **D10** — no se promedia como madurez; "Sí, totalmente" en la 36 es la **peor** respuesta, no la mejor.
- **D11** — no se promedia como madurez; se reporta como inventario.

### 3.5 Después de aplicar

- Verificar que no queden preguntas de escala en blanco sin razón anotada ("no aplica" vs. "no se supo responder" son cosas distintas para el cálculo del índice).
- Anotar cualquier pregunta que haya generado confusión reiterada — insumo para el ajuste del instrumento en la Fase 4 del plan a 75 días.
- Confirmar que la respuesta quedó registrada en la Google Sheet correspondiente antes de cerrar la sesión.

---

## 4. Efecto de la consolidación en el resto del toolkit

Este documento absorbió contenido que antes estaba repartido. Para no dejar información duplicada (y con eso, riesgo de que dos documentos digan cosas distintas si uno se actualiza y el otro no), se ajustó lo siguiente:

- **`Instrumento 6 - Nota Metodologica de Aplicacion.md`** — su §1 ("Quién debe responder") queda como una versión general de 2 líneas; el detalle por bloque/dimensión (tabla completa) ahora vive solo aquí (§3.3), y Instrumento 6 debe remitir a este documento en vez de duplicarlo. Instrumento 6 conserva lo que sí le es propio y no se duplica aquí: el alcance según recurso disponible entre los instrumentos 2–5 (§2), la muestra sugerida para Instrumento 3/FGD (§3), y la frecuencia de aplicación general (§4, ya reflejada aquí en §1.5 solo para Instrumento 2).
- **`Metodologia - Indice de Alineamiento (ISA) y Marco Muestral.md`** — su §1 ("Marco muestral") queda como la versión que sí explica el detalle matemático del ajuste por raking (§3 de ese documento); los campos de la ficha técnica propiamente dicha (universo, unidad de análisis, tamaño de muestra, estado actual del marco) ahora tienen como fuente única a este documento (§1 aquí). Metodología ISA conserva íntegro lo que le es propio: construcción del ISA (§2), ajuste de representatividad (§3), validación de robustez (§4) y conexión con performance (§5) — nada de eso se duplicó aquí.
- **Los dos documentos previos** (`Ficha Tecnica - Instrumento 2.md` y `Guia de Llenado - Instrumento 2.md`, creados minutos antes en esta misma sesión) **se eliminaron** — su contenido íntegro está aquí, en §1 y §3 respectivamente. No quedó ninguna referencia a esos dos archivos en otros documentos del toolkit (se crearon y no llegaron a citarse en otro lado).

---

**Estado:** documento de trabajo, 2026-09-17. Es ahora la referencia única de ficha técnica + guía metodológica resumida + guía de llenado para Instrumento 2 — actualizar aquí primero ante cualquier cambio, y solo después decidir si algo debe reflejarse también en Instrumento 6 o en Metodología ISA (lo específico de cada uno, no lo que ya vive aquí).
