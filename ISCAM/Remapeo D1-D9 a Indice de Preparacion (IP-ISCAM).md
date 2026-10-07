# Remapeo D1–D9 → Índice de Preparación (IP) del proyecto ISCAM

**Qué resuelve este documento:** convierte las 9 dimensiones de madurez del Instrumento 2 (D1–D9) en las 5 sub-dimensiones del Índice de Preparación (IP) que define `Projet ISCAM - INDICE de Vulnerabilite et de preparation.png`, sin reescribir ni una sola pregunta del instrumento — es un remapeo de agregación, no un instrumento nuevo. Es el primer paso de la combinación acordada en `Comparativa - ISA D1-D11 vs IP-IV-RE ISCAM.md`.

---

## 1. Principio de mapeo

- **D1 (clasificación regulatoria) y D10 (bandera de certificación) quedan fuera de IP**, igual que quedan fuera del ISA — D1 es estatus jurídico, no capacidad; D10 es una bandera de percepción, no una madurez a sumar. Esto es consistente con la Nota de puntaje del Instrumento 2.
- **D11 cambia de tratamiento respecto al ISA.** En el ISA, D11 es inventario puro (no se promedia). Para IP, ISCAM sí incluye "Certificaciones" y una noción de relación con actores externos dentro de su sub-dimensión 5 ("Capacidad de adaptación y acceso a recursos") — así que aquí D11 **sí aporta un puntaje**, calculado de forma distinta al resto (ver §3.5). Esto es una divergencia deliberada entre las reglas del ISA y las reglas de IP, no un error — cada índice mide algo distinto y puede tratar la misma dimensión de forma diferente.
- Dentro de cada sub-dimensión IP que agrupa más de una dimensión D, se aplica la misma lógica híbrida que ya usa el ISA (Metodología §2.3): **geométrica donde la no-sustitución importa** (legalidad/ambiental), **aritmética donde las dimensiones sí son sustitutos razonables entre sí** (capacidades organizacionales, recursos).

---

## 2. Tabla de mapeo

| Sub-dimensión IP (ISCAM) | Ítems declarados por ISCAM | Fuente en D1–D11 | Regla de agregación interna |
|---|---|---|---|
| **1. Trazabilidad y origen** | Registro de productores, Geolocalización de parcelas, Trazabilidad lote-parcela, Segregación de producto | **D2 completo** — mapeo casi 1:1: D2.5/D2.6 ≈ Registro/Geolocalización; D2.7 ≈ Trazabilidad lote-parcela; **D2.10 ≈ Segregación de producto** (la bandera de mezcla de lotes es literalmente el mismo concepto que "segregación") | Directo — es una sola dimensión D, sin combinar |
| **2. Cumplimiento ambiental** | Deforestación cero/EUDR, Uso del suelo, Manejo ambiental, Cumplimiento normativo | **D3 + D4** — D4 ≈ Deforestación cero/EUDR (match exacto); D3 ≈ Uso del suelo + Manejo ambiental (14a/14b/14c) + Cumplimiento normativo general | **Geométrica** entre D3 y D4 — son los dos requisitos núcleo del reglamento, no sustituibles entre sí (mismo argumento del IDH ya usado en el ISA) |
| **3. Capacidades organizacionales** | Gobernanza, Personal técnico, Control interno, Sistemas de gestión | **D8 + D5 + D6 (parcial)** — D8 ≈ Gobernanza (match exacto); D5 ≈ Control interno (procedimiento escrito, responsable designado, capacitación — es literalmente "control interno"); D6.22 (presupuesto) y D6.25 (apoyo externo gestionado) ≈ Sistemas de gestión | Aritmética simple — son capacidades organizacionales genuinamente sustituibles (una cooperativa puede compensar debilidad en gobernanza con buen control interno, a diferencia de legalidad/ambiental) |
| **4. Información y documentación** | Bases de datos, Evidencia documental, Monitoreo, Auditoría | **D6.23 (digitalización de registros)** — el único ítem que encaja limpio; D2.9 (frecuencia de actualización del registro de geolocalización) también aporta como proxy de "monitoreo" | Aritmética simple entre D6.23 y D2.9 — sub-dimensión delgada, con solo 2 ítems fuente (ver §3.4, limitación real) |
| **5. Capacidad de adaptación y acceso a recursos** | Financiamiento, Asistencia técnica, Certificaciones, Relación con compradores | **D7 + D9 + D11 (recalculado) + Certificaciones (Bloque 0, recalculado)** — D7 ≈ Relación con compradores (match exacto); D9 ≈ Financiamiento; D11 y Certificaciones ≈ Asistencia técnica/Certificaciones, ambos recalculados solo para IP (ver §3.5) | Aritmética simple |

---

## 3. Notas y decisiones que requieren atención

### 3.1 D6 quedó partido entre dos sub-dimensiones IP — es la más difícil de mapear limpio
D6 (Capacidad organizacional y digital) tiene 4 preguntas que ISCAM separaría en dos sub-dimensiones distintas: presupuesto y apoyo externo (→ Capacidades organizacionales / Sistemas de gestión), digitalización de registros (→ Información y documentación). **La cuarta pregunta de D6 — conectividad a internet (D6.24) — no encaja bien en ningún lado de IP.** Ver §3.3, es más candidata a Vulnerabilidad.

### 3.2 D9 encaja en IP como "Financiamiento", pero su contenido real es más de fragilidad que de capacidad
D9 pregunta si el costo de adecuación es proporcional, si se financió con deuda, y si hay riesgo de trasladarlo al precio del socio — son preguntas sobre **riesgo financiero**, no sobre "tener recursos". Lo dejamos en IP5 porque ISCAM nombra "Financiamiento" ahí, pero es la dimensión con más tensión conceptual del remapeo: casi toda su información también es útil, sin reescribir nada, para el Índice de Vulnerabilidad que viene después (sub-dimensión "Brechas tecnológicas y financieras" de IV, que habla explícitamente de "costos de cumplimiento" e "inversión insuficiente" — es casi el espejo invertido de D9).

### 3.3 Hallazgo importante: D6.24 (conectividad) probablemente pertenece a IV, no a IP
La sub-dimensión de Vulnerabilidad "Brechas tecnológicas y financieras" de ISCAM incluye explícitamente "Limitado acceso digital" como indicador de **vulnerabilidad**, no de preparación. D6.24 ya pregunta exactamente eso ("Conectividad a internet: No hay/Limitada/Confiable"). **Recomendación para la fase de diseño de IV (siguiente paso):** no escribir una pregunta nueva de conectividad — reutilizar D6.24 invertida (poca conectividad = alta vulnerabilidad) como insumo directo de IV. Mismo dato, dos usos, cero preguntas nuevas de encuesta para ese ítem.

### 3.4 Información y documentación es la sub-dimensión más débil del remapeo — limitación real, no oculta
Con solo D6.23 y D2.9 como fuente, esta sub-dimensión de IP queda sostenida por apenas 2 ítems, muy por debajo de las 4 que ISCOM describe conceptualmente (Bases de datos, Evidencia documental, Monitoreo, Auditoría). **Esto es un vacío real del Instrumento 2 frente a lo que IP necesita** — no hay ninguna pregunta actual sobre "evidencia documental" o "auditoría" como prácticas explícitas (archivos, expedientes, revisiones periódicas) más allá de lo que ya cubren D2 y D6. Si se quiere una sub-dimensión de Información y documentación con el mismo peso metodológico que las otras 4, hacen falta 1-2 preguntas nuevas — ojo, esto es una tarea de **instrumento**, no de remapeo, y debería evaluarse junto con el diseño de IV para no fragmentar el trabajo.

### 3.5 D11 y Certificaciones recalculados solo para IP (regla nueva, no toca el ISA)
- **D11 → IP5:** en vez de "inventario sin promediar" (regla del ISA), para IP se calcula `% de actores de D11.38 con contacto activo` como puntaje 0-100 directo. Ejemplo: si una cooperativa marcó 3 de 7 actores, su aporte a IP5 es 43. Es una regla simple, defendible, y no contradice la regla del ISA porque son índices distintos con propósitos distintos (el ISA no quiere premiar "conocer gente", IP sí lo considera parte de la capacidad de adaptación).
- **Certificaciones (Bloque 0) → IP5:** hoy Bloque 0 solo registra qué certificaciones tiene la cooperativa, sin puntaje (es insumo de D10). Para IP, se propone un puntaje simple por conteo: 0 certificaciones = 0, 1 = 33, 2 = 66, 3+ = 100 (o el conteo normalizado sobre el máximo observado en la muestra, a decidir en la fase de normalización real con datos).

### 3.6 Fórmula final

```
IP2_c = ( D3_c × D4_c )^(1/2)                         [geométrica]
IP3_c = ( D8_c + D5_c + D6_sistemas_gestión_c ) / 3    [aritmética]
IP4_c = ( D6.23_c + D2.9_c ) / 2                       [aritmética, sub-dimensión delgada — ver §3.4]
IP5_c = ( D7_c + D9_c + D11_recalc_c + Certif_recalc_c ) / 4   [aritmética]
IP1_c = D2_c                                            [directo]

IP_c = 0.20×IP1_c + 0.20×IP2_c + 0.20×IP3_c + 0.20×IP4_c + 0.20×IP5_c
```
Pesos iguales (20% cada sub-dimensión) por defecto, siguiendo el propio criterio de ISCOM ("Pesos iguales • AHP • Delphi") — a validar con el panel Delphi/AHP antes de reportar resultados finales (Fase 1 y Fase 4 de la metodología ISCAM, todavía pendientes).

---

## 4. Qué queda pendiente después de este remapeo

- [ ] Diseñar el Índice de Vulnerabilidad (IV) — reutilizando D6.24 (conectividad) y el contenido de riesgo financiero de D9 donde aplique, en vez de escribir todo desde cero (ver §3.2 y §3.3).
- [ ] Decidir si se agregan 1-2 preguntas nuevas para reforzar "Información y documentación" (§3.4) o si se acepta la sub-dimensión delgada como limitación documentada.
- [ ] Ejecutar el panel Delphi/AHP (Fase 1 de ISCAM) antes de fijar los pesos definitivos de IP — hoy son pesos iguales por defecto, no validados.
- [ ] Una vez exista IV, calcular `RE_c = IV_c · (1 − IP_c/100)` como estaba previsto.
