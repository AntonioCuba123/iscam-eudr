# Diseño del Índice de Vulnerabilidad (IV) — proyecto ISCAM

> **Nota de ubicación (2026-10-01):** el `Instrumento 7 - Evaluacion Critica y Elementos Adicionales.md` fue trasladado de `ISCAM\` a `Instrumentos\`. Las referencias a "Instrumento 7" en este documento apuntan a `..\Instrumentos\Instrumento 7 - Evaluacion Critica y Elementos Adicionales.md`.

**Qué resuelve este documento:** diseña IV desde cero — la pieza que, según `Comparativa - ISA D1-D11 vs IP-IV-RE ISCAM.md` (§2, punto 2), es el vacío real del toolkit, sin equivalente en D1–D11. A diferencia del remapeo de IP (`Remapeo D1-D9 a Indice de Preparacion (IP-ISCAM).md`, que solo reagrupa preguntas existentes), aquí sí hacen falta preguntas nuevas — documentadas como tal, no rellenadas con supuestos.

**Principio general de reúso:** varias preguntas de D1–D11 ya miden, desde el ángulo de "capacidad", lo mismo que IV necesita medir desde el ángulo de "exposición/riesgo". Se reutilizan **invertidas** en vez de escribir preguntas nuevas duplicadas — mismo dato, dos usos. Esto ya se identificó parcialmente en el Remapeo (§3.2–3.3 de ese documento) para D6.24 y D9; aquí se completa para el resto de IV.

---

## 1. Tabla de mapeo por sub-dimensión

| Sub-dimensión IV (ISCAM) | Fuente | Tipo de fuente | Regla de inversión / cálculo |
|---|---|---|---|
| **1. Dependencia del mercado europeo** | Bloque P (P1 volumen exportado UE + **P1b, nueva**: volumen total todos los destinos) + P4 (N° compradores europeos) | Reúso parcial + **1 pregunta nueva, ya redactada (P1b)** | `% volumen a UE = P1 / P1b` — dato duro, mismo período, en vez de la estimación de Bloque 0. Concentración de compradores: `100 / P4` como proxy simple (menos compradores UE = más dependencia de cada uno) |
| **2. Exposición regulatoria** | **D1 completo** (clasificación regulatoria: tipo de operador, si declara DDS propia o depende de un tercero) | Reúso total — resuelve el "huérfano" de D1 | D1 queda fuera de IP (es estatus jurídico, no capacidad) pero encaja perfecto en IV: ser operador grande que declara su propia DDS es *más* exposición regulatoria directa que ser proveedor de un comercializador que declara por ti. Normalización: mayor responsabilidad directa declarativa = mayor puntaje de exposición |
| **3. Fragilidad productiva y territorial** | **Corregido tras revisión (2026-09-16): 2 de 3 candidatas ya existían, no eran vacío real.** (a) Tamaño promedio de parcela — **no requiere pregunta nueva**, se deriva de Bloque 0 (`hectáreas totales asociadas / N.º de socios`), mismo patrón que las variaciones P1-P2 de Bloque P; (b) zona de riesgo social/coca — **ya existe como ítem cerrado en D3.14** del propio Instrumento 2 (agregado esta sesión), se reutiliza directo, no había que reconvertir nada de Instrumento 3; (c) dispersión geográfica y distancia al centro de acopio — **este sí era el vacío real, 2 preguntas nuevas ya redactadas** en Bloque 0 | `IV3 = promedio( D3.14_recodificada, dispersión_geográfica, distancia_centro_acopio, 100−tamaño_parcela_norm )` — el tamaño de parcela se invierte porque parcela más pequeña y fragmentada = mayor fragilidad productiva |
| **4. Brechas tecnológicas y financieras** | **D6.24 (conectividad)** + **D9 completo** (riesgo financiero: costo desproporcionado, financiado con deuda, riesgo de traslado al precio del socio) | Reúso total, invertido | `IV4 = 100 − D6.24_norm` promediado con `100 − D9_norm` — ya identificado en el Remapeo (§3.2, §3.3 de ese doc) como el mejor caso de reúso de todo el ejercicio |
| **5. Riesgo social y comercial** | **D7** (concentración de comprador único, "qué pasaría si perdieran el mercado") + D8 (fricción con socios: negativa a compartir ubicación, resistencia a la formalización) + **% de mujeres en la directiva, nueva (2026-09-16)** | Reúso parcial, invertido + **1 pregunta nueva** | `IV5 = 100 − D7_norm` combinado con la fracción de D8 que mide fricción/resistencia interna, y con `100 − %mujeres_directiva` como proxy de riesgo de exclusión por baja representación (ver §3.1 sobre por qué se agregó) |

---

## 2. Qué es reúso limpio y qué exige preguntas nuevas — sin mezclar ambas cosas

**Reúso limpio (sin preguntas nuevas), 3 de 5 sub-dimensiones:**
- IV2 (Exposición regulatoria) ← D1 completo.
- IV4 (Brechas tecnológicas y financieras) ← D6.24 + D9 completo.
- IV5 (Riesgo social y comercial) ← D7 + fracción de D8.

**Vacíos reales, ya redactados en Instrumento 2 (2026-09-16):**
- **P1b** (Bloque P) — volumen total exportado a todos los destinos, cierra IV1. Esta misma pregunta, además, cierra parcialmente la brecha de "% volumen trazable" que el propio Comparativa (§3.3) marcó como faltante para la validación externa de ISCAM.
- **2 ítems nuevos en Bloque 0** — dispersión geográfica de los socios (concentrados/dispersos por distrito-provincia) y distancia al centro de acopio, cierran la parte real del vacío de IV3.

**Vacíos que resultaron NO ser reales, al revisar el instrumento con más cuidado antes de escribir preguntas nuevas:**
- Tamaño promedio de parcela → ya derivable de Bloque 0 (hectáreas totales / N.º de socios), sin pregunta nueva.
- Zona de riesgo social/cultivo de coca → ya existe como ítem cerrado en D3.14 del propio Instrumento 2 (no había que tocar Instrumento 3).

Esto es la razón por la que se revisó el instrumento completo antes de redactar — escribir 2 preguntas de más habría sido duplicar dato ya disponible.

---

### 3.1 Adición 2026-09-16 — representación de género como insumo de IV5 (hallazgo de la evaluación de preparación EUDR de Vietnam, Team Europe Initiative 2025)

Ese estudio trata "Gender & inclusion" como criterio transversal de preparación EUDR, con **"riesgo de exclusión"** como uno de sus indicadores explícitos — el mismo nombre que nuestro RE. Instrumento 7 ya había decidido correctamente que género **no debe entrar al puntaje D1–D9** (no determina el acceso al mercado bajo el reglamento) — esa decisión no cambia. Pero IV es una capa distinta, pensada para vulnerabilidad social/estructural, no para cumplimiento legal — ahí sí encaja un indicador de representación.

**Pregunta nueva agregada a Bloque 0:** "% de mujeres en la directiva/consejo directivo" — mide representación en el órgano de decisión (no solo membresía), que es el indicador que usa el estudio de referencia. Baja representación se trata como proxy de riesgo de exclusión de esos intereses en la toma de decisiones sobre el proceso de adecuación EUDR — no como juicio sobre la organización, sino como uso justo del mismo criterio que ya validamos en IV para otros factores (dispersión, conectividad, etc.).

---

## 3. Fórmula

```
IV1_c = ( (P1_c/P1b_c)×100 + 100/P4_c ) / 2
IV2_c = D1_c (recodificado 0-100, mayor exposición declarativa = mayor puntaje)
IV3_c = ( D3.14_recodificada_c + dispersión_geográfica_c + distancia_centro_acopio_c + (100 − tamaño_parcela_norm_c) ) / 4
IV4_c = ( (100 − D6.24_c) + (100 − D9_c) ) / 2
IV5_c = ( (100 − D7_c) + fricción_D8_c + (100 − %mujeres_directiva_c) ) / 3

IV_c = 0.20×IV1_c + 0.20×IV2_c + 0.20×IV3_c + 0.20×IV4_c + 0.20×IV5_c
```

Pesos iguales por defecto — misma salvedad que en IP: pendiente de validación con panel AHP (Fase 1 de ISCAM, todavía no ejecutada para ningún índice de este proyecto).

Con las preguntas de §2 ya redactadas en Instrumento 2, **las 5 sub-dimensiones son calculables desde el primer piloto** — no queda ninguna huérfana de dato como se pensó inicialmente. La regla de datos faltantes de la Metodología del ISA (Rubin/Little & Rubin — nunca imputar una dimensión totalmente ausente, re-ponderar en su lugar) sigue aplicando solo al caso genérico de no-respuesta puntual, no a un vacío estructural de instrumento.

---

## 4. Riesgo de Exclusión (RE) — ya calculable con esta pieza

Con IP (Remapeo D1-D9) e IV (este documento) definidos:

```
RE_c = IV_c · (1 − IP_c/100)
```

Interpretación: una cooperativa muy vulnerable (IV alto) pero muy preparada (IP alto) tiene RE bajo — la preparación *modera* la vulnerabilidad, tal como lo plantea la Hipótesis 3 del proyecto madre (ver Comparativa §1, fila "Operacionalización de impacto en desempeño/exclusión"). Esto ya es calculable en el piloto interno (artifact en línea) una vez se agreguen las 3-4 preguntas nuevas de IV1/IV3 al Bloque 0/P.

---

## 5. Matriz de tipología 2×2 (Preparación × Vulnerabilidad)

Con IP y IV ya definidos, se puede construir directamente la matriz que ISCAM usa para priorización (Comparativa §1, fila "Tipología de priorización"):

| | IV bajo | IV alto |
|---|---|---|
| **IP alto** | Resilientes y mejor posicionadas | Expuestas pero adaptables |
| **IP bajo** | Riesgo latente | Riesgo crítico de exclusión |

El punto de corte alto/bajo (mediana muestral vs. umbral fijo) se decide con los primeros datos reales del piloto, no antes — fijar un umbral sin datos sería inventar un criterio.

---

## 6. Pendientes después de este diseño

- [x] Redactar las preguntas nuevas realmente faltantes (§2): P1b (IV1) y los 2 ítems de dispersión geográfica (IV3), ya incorporadas en `Instrumento 2 - Encuesta Cuantitativa.md` (2026-09-16).
- [x] Agregar esas mismas 3 preguntas al artifact en línea — hecho 2026-09-16, mismo patrón ya usado para 14a/14b/14c y RUC. Documento y artifact vuelven a estar sincronizados.
- [x] Agregar "% de mujeres en la directiva" a Bloque 0 e IV5 (§3.1) — hecho 2026-09-16, incorporada a `Instrumento 2 - Encuesta Cuantitativa.md`.
- [x] **Fracción de D8 que cuenta como "fricción" para IV5 — cerrado 2026-09-17.** Es **D8.30** (% de socios que entienden por qué se les pide geolocalización/documentación), invertida: `fricción_D8_c = 100 − D8.30_c`. Es el único ítem de D8 que mide directamente la brecha de comprensión/aceptación del socio de base — D8.29 (asambleas realizadas) y D8.31 (mecanismo de entrega) miden esfuerzo institucional, no resistencia del socio; D8.32 (rotación de directiva) mide continuidad, no fricción. Usar solo D8.30 evita diluir IV5 con ítems que no miden resistencia real.
- [ ] Ejecutar el panel AHP para validar pesos de IP e IV juntos (Fase 1 ISCAM) — sigue pendiente desde el Remapeo, ahora se puede hacer en una sola ronda para ambos índices.
- [ ] Una vez el piloto tenga datos reales, fijar el punto de corte alto/bajo de la matriz 2×2 (§5).
- [ ] Actualizar la Metodología del ISA para declarar la relación entre ISA (D1–D11) e IP/IV/RE: no son competidores, ISA sigue siendo el motor de cumplimiento regulatorio con sus banderas duras (D2.10, D10, trabajo forzoso) que se reportan aparte, nunca absorbidas en IP/IV/RE — punto ya acordado en Comparativa §2.4, pendiente de trasladarse formalmente al documento de Metodología.
