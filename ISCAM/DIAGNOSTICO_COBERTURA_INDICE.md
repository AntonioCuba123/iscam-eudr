# Diagnóstico de cobertura — Índice ISCAM (ISA-EUDR · IP)

**Fecha:** 2026-10-15 · **Muestra:** 174 organizaciones (café/cacao) · **Libro:** `PLANTILLA_INDICE_PVE_ISCAM.xlsx`

---

## 1. Resumen ejecutivo

El problema del ISA-EUDR **no es D4 ni D7 puntualmente: es que 10 de las 11 dimensiones del bloque ISA están en 0 como marcador de posición**, porque el Instrumento 2 todavía no se ha levantado.

Hoy **solo D3 (Legalidad OSCE/OEFA) está poblado** (174/174). Todo lo demás son ceros duros de la plantilla, no mediciones.

Consecuencia en cadena:

```
D1..D2, D4..D11 = 0  →  IP = 0  y  ISA-EUDR = 0
                      →  RE = IV (el término de preparación desaparece)
                      →  158 organizaciones rotuladas «Riesgo Crítico»
```

Ese «Riesgo Crítico» **no es un hallazgo: es el reflejo de que no hay datos de preparación (IP)**. En un documento para presentar, esto es el defecto más grave del paquete.

---

## 2. Cobertura real por dimensión

### Bloque ISA (núcleo EUDR)

| Dim | Qué mide | Fuente prevista | Cobertura | Estado |
|---|---|---|---|---|
| **D1** | Clasificación regulatoria | Instrumento D1.1–D1.4 | **0/174** | cero-placeholder |
| **D2** | Trazabilidad | Instrumento D2.x → `SCORECARDS!H` | **0/174** | cero-placeholder |
| **D3** | Legalidad OSCE/OEFA | Neon (OSCE + OEFA) | **174/174** | ✅ poblado |
| **D4** | Deforestación cero | Instrumento D4.15–D4.17 + geodatos | **0/174** | cero-placeholder |
| **D5** | Diligencia debida | Instrumento D5.x → `SCORECARDS!I` | **0/174** | cero-placeholder |
| **D6** | Capacidad digital | Instrumento D6.x → `SCORECARDS!J` | **0/174** | cero-placeholder |
| **D7** | Presión comprador | Instrumento D7.x (+ `B0.8` destino) | **0/174** | cero-placeholder |
| **D8** | Gobernanza | Instrumento D8.x | **0/174** | cero-placeholder |
| **D9** | Riesgo financiero | Instrumento D9.x | **0/174** | cero-placeholder |
| **D10** | Certificación / confusión EUDR | Instrumento D10.x (bandera) | **0/174** | cero-placeholder |
| **D11** | Ecosistema de apoyo | Instrumento D11.x | **0/174** | cero-placeholder |

### Bloque ambiental del ISA-PV (D12–D15)

| Dim | Cobertura | Estado |
|---|---|---|
| D12 Huella de carbono | 45/174 con valor (todos = 1 «en curso») | parcial |
| D13 Reporte de sostenibilidad | 0/174 | vacío |
| D14 Economía circular | 0/174 | vacío |
| D15 Fitosanitario / LMR | 0/174 | vacío |

> El ISA-PV (8 componentes) solo tiene **2 alimentados**: `% UE/FOB` (20 %) y `D12–D15` (20 %, y de estos solo D12 parcial). Por eso el ISA-PV nunca pasa de 0,225.

---

## 3. Qué datos administrativos SÍ existen (y hasta dónde llegan)

Buscados en `3 directorio - trabajo en base global cafe cacao 07.10.26.xlsx` (hojas `base 174 detallada`, `base dua 25 detallada`, `base consolidad MIDAGRI`) y en `duas_parsed.json`.

| Dato disponible | Cobertura | Podría alimentar |
|---|---|---|
| `% UE/FOB` (MATRIZ_174!M) | **174/174** | D1 · IV1 |
| `Exporta SÍ/NO` | **174/174** | D1 |
| `Tipo de Organización` | **174/174** | IV5 |
| Destinos (MIDAGRI) | 51/174 | D7 |
| `DESTINOS DUA` | 39/174 | D7 |
| FOB DUA 2024/2025 depurado | 35–37/174 | D9 |
| N.º socios y hectáreas | 22/174 | D8 · IV3 |
| Certificación Comercio Justo | 21/174 | Cert · D10 |
| «Indicar avance reglamento EUDR» | 17/174 | D2 · D4 |
| Otras certificaciones (BIO, RA…) | 12/174 | Cert · D10 |

**Lectura:** solo **D1** es reconstruible para las 174. **D7 (30–50/174) y D9 (~37/174) están a media cobertura.** **D2, D4, D5, D6, D8, D10, D11 no tienen fuente** fuera del Instrumento 2.

---

## 4. Por qué la agregación agrava el problema

`ISA-EUDR = GEOM(D1..D7)^(1/7) × 0,875 + ((D8+D9)/2) × 0,125`

La **media geométrica colapsa a 0 si cualquier dimensión es 0**, y `IP2 = √(D3×D4)` también. Es decir: aun con datos parciales, **una sola dimensión sin levantar anula el índice**. No existe hoy ninguna combinación de datos administrativos que produzca un ISA-EUDR ≠ 0 para la muestra.

---

## 5. Decisión e implementación

**Decidido 2026-10-15: Opción A — «sin dato» honesto.** El índice es un instrumento de medición; publicar ceros donde no hay medición es un error de validez, no una estimación conservadora.

### Qué se cambió

| Elemento | Antes | Ahora |
|---|---|---|
| `ISCAM_Score` D1, D4, D7–D11 | `0` literal | vacío (sin dato) |
| `SCORECARDS` D2, D5, D6, PPWR | `0` literal | vacío (sin dato) |
| `ISA-EUDR` (AK) | `0` | `N/A` (<7 de 9 dimensiones con dato) |
| `IP` (Z) | `0` | `—` (<8 de 8 dimensiones con dato) |
| `RE` (AB) | `= IV` | `—` (requiere IP) |
| `ISA-Completo` (AL) | `0,3 × ISA-PV × 100` | `—` |
| Tipología (AC) | 158 «🔴 Riesgo Crítico» + 16 «Riesgo Latente» | 174 «⬜ Pendiente de instrumento» |
| `SCORECARDS` semáforo | «🔴 Crítico» | «— Sin Inst.2» |
| `MATRIZ_174` clasificación (T) | «🔴 Crítico» | «⬜ Parcial · Inst. 2 pendiente» (nuevo `AQ` = cobertura ISA-PV, 3/7) |
| `RADAR_BRECHAS` | promedio por departamento con ceros | «—» por dimensión sin dato; promedio solo con ≥7 dimensiones |
| Panel de cobertura | no existía | `ISCAM_Score!A182:C199` |

**Umbrales (alineados con la §2.4 del documento metodológico):** ISA-EUDR se computa con **7 de 9** dimensiones D1–D9 y re-pondera proporcionalmente las presentes; **IP exige las 8** dimensiones D2–D9, porque cada subíndice IP1–IP5 depende de un conjunto fijo.

**Se conserva lo realmente medido:** D3 (legalidad OSCE/OEFA, 174/174) y el ISA-PV parcial (indicativo, no comparable). No se alteró ninguna cifra de IV1–IV5 (proxies documentados por diseño).

**Cifras que desaparecieron:** el «ISA-Completo promedio 2,9» y los «158 Riesgo Crítico» eran artefactos de dato faltante. El PVE promedio (ISA-PV, 0–100) se mantiene como 2,9 con la etiqueta de parcial.

### Cómo se revierte o se avanza
- Todo estado anterior es reconstruible: respaldo en `ISCAM\respaldos\PLANTILLA_INDICE_PVE_ISCAM.backup_2026-10-15_pre-sindato.xlsx`.
- La capa de proxies (Opción B) puede activarse **dimensión por dimensión**, a medida que se cierre la captura, sin rehacer el motor: basta con cargar el valor y el `N/A`/`—` pasa a número solo.

---

## 6. Conclusión

El «brecha de ISA-EUDR» no era un problema de D4 y D7: era que **10 de 11 dimensiones ISA eran ceros-placeholder**. Con los datos administrativos existentes no es posible computar el ISA-EUDR para la muestra (solo D1 es reconstruible al 100 %; D7 alcanza 30 %; D2, D4, D5, D6, D8, D10 y D11 no tienen fuente). El índice queda, por tanto, declarado como **pendiente del Instrumento 2**, y así queda dicho en el libro y en el documento — en lugar de afirmar que 158 cooperativas están en riesgo crítico sin haberlas medido.

---

## Capa de ingesta del Instrumento 2 — implementada (2026-10-15)

Con esto desaparece el único bloqueante del cálculo que quedaba (§5 del documento de metodología): los datos del instrumento ya tienen dónde cargarse y cómo convertirse en índice.

Tres hojas nuevas en `PLANTILLA_INDICE_PVE_ISCAM.xlsx` (orden del libro: INSTRUCCIONES → INSTRUMENTO_2_PREGUNTAS → **CODIFICACION** → **CAPTURA** → **NORMALIZADO** → ISCAM_Score → PONDERADORES → MATRIZ_174 → SCORECARDS → RADAR_BRECHAS):

| Hoja | Rol | Contenido |
|---|---|---|
| `CODIFICACION` | Regla de conversión | 290 filas: cada opción de respuesta con su puntaje 0-100 o «sin dato». Editable; marca `[R]` los ítems a ratificar. |
| `CAPTURA` | Entrada de datos | 174 cooperativas × 119 preguntas. RUC y razón social precargados. 63 listas desplegables, validación 0-4 y 0-100. Única hoja de escritura. |
| `NORMALIZADO` | Cálculo intermedio | 0-100 por pregunta (77 que puntúan) + agregado de las 11 dimensiones D1-D11. Fórmulas, no se edita. |

**Cableado del motor.** `ISCAM_Score!E:O` (D1-D11) ahora lee `NORMALIZADO`; `SCORECARDS!H:I:J` espeja D2/D5/D6; `MATRIZ_174!W:Z` (D12-D15) lee la captura conservando el valor previo como respaldo. D3 usa la encuesta y, si no hay respuesta, conserva la consulta OSCE/OEFA (`MATRIZ_174!U`). ISA-PV se blindó para tolerar componentes «sin dato» (antes `""/100` daba `#VALUE!`). El panel de cobertura `ISCAM_Score!A182:C201` ya cuenta la captura real.

**Probado de extremo a extremo.** Con respuestas sintéticas (mejor/peor caso) el índice calcula: mejor caso ISA-EUDR 99,2 / IP 92,5 / ISA-Completo 92,8; peor caso ISA-EUDR 5,9 / IP 4,7. Sin captura, todo sigue en «—»/«N/A» y `ISCAM_Score!AA4` (IV) conserva 60.

### Ítems a ratificar (`[R]`) antes del levantamiento de campo

La codificación categórica no estaba especificada en el documento de metodología; se propuso una interpretación (100 = mayor alineamiento con el EUDR). **Resuelto el 2026-10-15 contra las fuentes originales del propio instrumento** — véase *«Ratificación resuelta (2026-10-15)»* más abajo. La tabla es editable en la hoja `CODIFICACION`.

| Ítem | Pregunta | Codificación propuesta |
|---|---|---|
| `D1.1` | ¿La cooperativa introduce el producto directamente en el mercado de la UE bajo su propio nombre? | Sí = 100 · No = 50 |
| `D1.4` | ¿Cumple los umbrales de microempresa/pequeña empresa (Directiva 2013/34/UE)? | Sí = 100 · No = 50 · No sabe = «sin dato» |
| `D3.12` | ¿Hay parcelas superpuestas a áreas naturales protegidas o su zona de amortiguamiento, reservas comunales o territorios indígena... | Sí, extensa = 0 · Sí, puntual = 50 · Sí, en área natural protegida o zona de amortiguamiento = 0 · No verificado = «sin dato» · No, ninguna = 100 |
| `D4.15` | ¿Se verificó cambio de uso de suelo posterior al 31 de diciembre de 2020 mediante cruce de las parcelas con mapas de deforestac... | No verificado = «sin dato» · Verificación parcial = 50 · Verificado sin hallazgos = 75 · Casos detectados sin resolver = 0 · Verificado sistemáticamente y documentado = 100 |
| `D6.25b` | *(Rama: solo si D6.25a = "Sí, con respaldo definido pero no probado" o "Sí, con protocolo probado")* ¿El protocolo fue diseñado... | Diseñado internamente = 50 · Con apoyo de ONG o programa = 50 · Con apoyo de consultoría o proveedor IT = 50 · Nunca se ha probado = 0 · Probado hace más de 12 meses = 50 · Probado en los últimos 12 meses = 100 |
| `B0.8` | Destino(s) de sus exportaciones, marcando primero el principal — incluya destinos fuera de la UE | casillas múltiples: % de destinos de la UE sobre el total marcado |
| `P10` | ¿Ha perdido algún contrato o comprador europeo en los últimos 2 años por motivos de cumplimiento (EUDR u otro requisito de sost... | Sí = 0 · No = 100 · No sabe = «sin dato» |
| `D7.28` | Riesgo percibido de perder el contrato si no cumple a tiempo | No sabe = «sin dato» · Bajo = 33 · Medio = 67 · Alto = 100 |
| `D7.28c` | *(Rama: solo si D7.28b = "Sí, ha enviado documentación" o "Sí, lo ha formalizado como cláusula")* ¿Qué tipo de documentación ha... | casillas múltiples: n.º marcados ÷ 8 |
| `D9.34` | ¿Cómo ha financiado (o financiaría) la organización la adecuación al EUDR? | Con crédito o endeudamiento = 33 · Con recursos propios = 100 · Existe fuente de financiamiento identificada (verde, cooperación o programa público), aún no ejecutada = 67 · No ha sido necesario = 100 · No sabe = «sin dato» |
| `PP1` | ¿Qué tipo de sacos de exportación utiliza principalmente? | Yute reutilizable = 100 · Yute nuevo de un solo uso = 75 · Big-bag o saco plástico = 25 · Saco de papel = 50 · Otro (especificar) = 50 |
| `D10.36` | ¿La cooperativa cree que su certificación vigente (Rainforest Alliance, Fairtrade, Orgánico, etc.) ya cubre las obligaciones de... | Sí, totalmente = 0 · Sí, en parte = 33 · No, sabe que son cosas distintas = 100 · No tiene certificación = «sin dato» |
| `D10.37` | ¿Algún proveedor o consultor le ha ofrecido una "certificación EUDR" como producto? | Sí = 0 · No = 100 |
| `D11.38` | Marque los actores con los que la cooperativa ya tiene contacto o apoyo activo | casillas múltiples: n.º marcados ÷ 7, «Ninguno» = 0 |
| `D11.39a` | ¿La organización está inscrita en una plataforma de trazabilidad del sector (APPCACAO, Junta Nacional del Café u otra equivalen... | Sí = 100 · En proceso de inscripción = 50 · No = 0 · No conoce la plataforma = «sin dato» |

> Nota histórica: `[R]` era solo de ratificación de dirección, no un bloqueo. El motor ya era coherente y reproducible; lo que cambió con la ratificación fue qué insumo entra en cada promedio, no la arquitectura del índice.

---

## ISA-PV re-ponderada sobre componentes presentes (2026-10-15)

Cambio pedido: que ISA-PV use la misma regla que ISA-EUDR. Implementado en `MATRIZ_174!AP`.

| | Antes | Ahora |
|---|---|---|
| Fórmula | `Σ(wᵢ·vᵢ) ÷ 100` | `Σ(wᵢ·vᵢ) ÷ Σwᵢ` (solo componentes con dato) |
| Componente sin dato | contaba como 0 | se excluye y se re-normaliza |
| PPWR (w=4) | 0 en numerador, 4 en denominador | excluido (sin fuente aún), reportado en `AQ` |
| Fila 3 (ejemplo) | 0,125 | 0,260 |

Efecto en las 174 organizaciones: media 0,060 (PVE promedio 6/100); 125 en 0 porque sus componentes presentes valen 0. `AQ` (cobertura) usa ahora el mismo criterio de presencia que la fórmula, para que el conteo y el cálculo no se contradigan. Documentado en la §2.4 del documento y en `PONDERADORES!B29`.

> Cifras históricas. La regla de reporte cambió dos veces más abajo (umbral primero, valor provisional después): hoy ISA-PV se computa **siempre** sobre los componentes con dato y, por debajo del umbral Pacto Verde, se muestra como valor provisional con la etiqueta «◐ Parcial · n/7». El 0,260 de la fila 3 es, de hecho, lo que hoy se muestra.

### Resuelto: ceros de relleno → «sin dato» (2026-10-15)

La observación anterior quedó cerrada aplicando el criterio «sin dato»: **un cero que no es una medición pasa a celda vacía, nunca a 0**. Un cero medido se conserva.

| Celda | Antes | Ahora | Por qué |
|---|---|---|---|
| `M` (% UE/FOB) | 0 si no había FOB total | `""` si no hay FOB total | el 0 confundía «no exporta a la UE» con «no hay dato de comercio» |
| `O` (puntaje de certificación) | 0 salvo `H="SI"` exacto | `""` si no hay dato; 0,6·H + 0,4·I si lo hay | 0 era relleno para 152 organizaciones |
| `H` / `I` (cert. orgánica / fairtrade) | texto truncado a 3 caracteres (`"Cer"`, `"PE-"`, `"Si "`) | `SI` / `NO` / vacío, desde el texto fuente | `build_pve_index.py` aplicaba `str(...)[:3]` sobre texto libre; la prueba `="SI"` fallaba en 18 organizaciones certificadas |
| `L` (FOB UE) | 0 en 138 | vacío en 122 (organizaciones sin DUAs); se conservan los 16 ceros medidos | en la fuente el faltante es nulo, no 0 |
| `E` (FOB total) | 32 ceros de relleno | vacío | ídem |
| `AA:AN` (P1–P14) | 2436 ceros | vacío | indicadores socioeconómicos no levantados |

Cascada corregida para que el vacío no se lea como 0: `ISCAM_Score!U` (IV1), `ISCAM_Score!X` (IV4), `ISCAM_Score!T` (IP5), los subíndices IP1–IP5 y `SCORECARDS!F` devuelven «—»/vacío cuando su insumo falta. El texto original de certificación se conserva en `MATRIZ_174!AR/AS`.

Efecto: IV1 con dato 36 / 0 medido 16 / sin dato 122; IV4 con dato 22 / sin dato 152; el % UE y el FOB UE con dato 52 (coincide exactamente con las organizaciones con DUAs). Ninguna organización queda con un 0 de relleno.

### UMBRAL ISA-PACTOVERDE → valor provisional (2026-10-15)

El documento (§2.4) exige «3 de las 4 dimensiones Pacto Verde (D12–D15) con dato» para reportar ISA-PV como medición cerrada. El libro aplicó primero ese umbral de forma binaria (por debajo, «—»); el pedido posterior fue **mostrar el valor y etiquetarlo como parcial**, no ocultarlo.

| Estado (`MATRIZ_174!AT`, espejo en `ISCAM_Score!AM`) | Condición | Qué se muestra |
|---|---|---|
| `completo` | 7 de 7 componentes con dato **y** ≥3 de 4 dimensiones D12–D15 capturadas (`NORMALIZADO!BV:BY`) | valor + veredicto de color (🔴/🟡/🟢) |
| `parcial · n/7 · D12-D15 k/4` | hay ≥1 componente con dato, pero no se cumple lo anterior | valor re-ponderado + «◐ Parcial · n/7», **sin** color |
| `sin dato` | ningún componente con dato | `AP`/`S` = «—» y «⬜ Sin dato PVE» |

`AP` (ISA-PV 0–1) y `S` (PVE puntaje 0–100) ya no tienen puerta: se computan siempre sobre los componentes con dato, re-normalizando los pesos. El veredicto de color se reserva para la medición completa, porque un color sobre una base parcial sería la «medición falsa» que la §2.4 quiere evitar. La cobertura por organización sigue en `AQ`.

Con la captura vacía (0 de 4 D12–D15): **61 organizaciones** tienen algún componente con dato y su valor es provisional; **113** quedan en «sin dato». `SCORECARDS!B186` (PVE promedio) pasó a **41,7** y su rótulo advierte que incluye parciales.

### Los ceros de relleno de D12–D15 (2026-10-15)

Al abrir la puerta de `AP`, un cero de relleno que quedaba oculto salió a la superficie: `MATRIZ_174!X/Y/Z` (D13/D14/D15) valían `0` en las **174** filas y `W` (D12) en **129**, de modo que el componente AMBIENTAL contaba como presente y valía 0 —ISA-PV salía 0 en lugar de «—»—. Igual que M, O y L/E, eran relleno del generador, no medición: se vaciaron. Se conserva **solo el proxy FAO/IPCC documentado de D12** (`W = 1` en las 45 organizaciones con hectáreas conocidas), que es el valor provisional que la §2.4 y la propia hoja declaran hasta levantar el Instrumento 2.

### IP5 corregido de escala (2026-10-15)

`ISCAM_Score!T` (IP5 · Mercado y riesgo) sumaba `(D7 + D9 + Cert) / 3` con dos dimensiones en 0–100 y el puntaje de certificación en 0–1: una organización con certificación plena perdía ~0,33 de subíndice frente a una sin certificado. Corregido a `(D7 + D9 + Cert×100) / 3`. El defecto era latente (sin captura, IP5 devuelve vacío), pero quedaba a la vista en las columnas IP1–IP5 del motor. En la misma pasada, IP1–IP5 devuelven **vacío** (no 0) cuando falta su insumo, coherente con «sin dato = «—», nunca 0».

### Ratificación resuelta (2026-10-15)

**Qué se hizo.** En lugar de esperar la confirmación del autor, los 15 ítems `[R]` y los 4 casos de Fairtrade ambiguos se resolvieron **contra las fuentes originales** y no por criterio propio:

| Fuente | Qué rige |
|---|---|
| `Instrumentos/Instrumento 2 - Encuesta Cuantitativa.md` — *Nota de puntaje* | D1–D9 promedian solo preguntas de escala/porcentaje; **D10 no se promedia como madurez** (bandera); **D11 no se promedia** (inventario); Bloque P son variables de resultado («no puntúan, no forman parte del ISA») |
| `Instrumentos/DOC_TRABAJO_Instrumento2_ISCAM_v2.md` — **Tabla 5** | Qué promedia y qué no, por dimensión: D2/Q10, D3/Q14g, D5/Q19a, D7/Q28 y Q28c, D10/Q36–Q37 y D11/Q38–Q39 quedan **fuera** del promedio |
| `Instrumentos/Estructura Google Sheet - Respuestas Instrumento 2.md` — reglas de integridad 3–7 | Banderas (`D2.10, D2.5b, D3.14i, D4.15a, D7.28, D10.36, D15.60`) se reportan aparte; mapeos (`D5.19a, D7.28c, D11.38/D11.39`) **no entran a ningún promedio**; Bloque 0 = identificación, no puntúa |

**Resultado — 8 ítems salen de todo promedio** (se siguen capturando y se reportan por separado), y con ellos los ítems que la misma regla alcanza aunque no estuvieran en la lista `[R]`:

| Ítem | Motivo (fuente) |
|---|---|
| `B0.8` | Bloque 0 — identificación; variable de verificación de destinos |
| `P8`, `P10`, `P13`, `P14` | Bloque P — variables de resultado |
| `D2.10`, `D2.5b` | Banderas — no promedian en D2 |
| `D3.14i` | Bandera OEFA/SINEFA — no promedia en D3 |
| `D4.15a` | Bandera de deforestación — no promedia en D4 |
| `D7.28`, `D7.28c` | Urgencia / mapeo — no promedian en D7 |
| `D10.36`, `D10.37` | Banderas — no promedian en D10 |
| `D11.38`, `D11.39a` | D11 es inventario — no promedia |
| `D3.14g`, `D5.19a` | Verificación / mapeo — no promedian (misma regla, no estaban en `[R]`) |

**Resultado — 7 ítems sí promedian y su dirección quedó confirmada:** `D1.1` (100 = operador directo), `D1.4` (100 = umbral micro/pequeña empresa), `D3.12` (severidad: ninguna 100 · puntual 50 · extensa/ANP 0), `D4.15` (verificación del cambio de uso post-2020; casos sin resolver = 0), `D6.25b` (manda la última prueba; el origen es contexto), `D9.34` (carga financiera: propios 100 · fuente identificada 67 · crédito 33) y `PP1` (reutilización; alimenta PPWR, no el ISA-EUDR).

**Efecto en el motor.** `NORMALIZADO` recomputa el promedio de cada dimensión sobre las preguntas que sí promedian; `D11` queda como inventario (sin promedio) y `D10` puntúa solo por la asesoría EUDR. `ISCAM_Score`, `SCORECARDS` y el núcleo geométrico de ISA-EUDR no cambian de definición — cambia su insumo, que era el punto. Verificado con caso sintético: mejor caso ISA-EUDR 99 · IP 100 · ISA-Completo 95,9; con la captura vacía todo sigue en `—`/`N/A`.

**Fairtrade — 4 casos resueltos por la fuente.** La celda `Cert. Comercio Justo (interno)` de la matriz contiene, en tres casos, texto de **certificación orgánica** («Vigencia orgánica hasta 26/03/2027») —que es exactamente el valor repetido en esas tres filas—, sin evidencia de Comercio Justo ni mención web: permanecen en **«sin dato»** (`20132489824`, `20147443120`, `20200880448`). El cuarto, **`20132505455` (AGUILAYOC)**, tenía la celda interna vacía pero el campo `Certificaciones (web)` y la fuente del directorio de la JNC (`juntadelcafe.org.pe/socios`) registran «Orgánica y Comercio Justo»: se recodificó a **SI**. Su puntaje de certificación pasa de 0,6 a 1,0.

**Observaciones abiertas (no aplicadas).**

- 14 organizaciones más tienen mención de Comercio Justo/Fairtrade **solo** en el campo derivado `Certificaciones (web)` (p. ej. «promueve Comercio Justo», «en implementación»). No se imputaron: es un campo derivado y ambiguo, y usarlo cambiaría la regla «sin dato = sin evidencia». Queda como tarea de verificación documental opcional.
- ~~`ISCAM_Score!T` (IP5) mezcla escalas: `(D7 + D9 + Cert) / 3` suma dos dimensiones 0–100 con el puntaje de certificación 0–1. Es un defecto latente que no se muestra hoy (IP5 está vacío sin captura).~~ **Resuelto (2026-10-15):** `(D7 + D9 + Cert×100) / 3`; ver «IP5 corregido de escala».
