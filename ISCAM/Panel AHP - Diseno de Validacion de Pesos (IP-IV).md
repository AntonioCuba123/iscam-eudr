# Panel AHP — Diseño de validación de pesos para IP e IV

**Qué resuelve este documento:** hasta ahora, tanto `Remapeo D1-D9 a Indice de Preparacion (IP-ISCAM).md` como `Diseno - Indice de Vulnerabilidad (IV-ISCAM).md` usan **pesos iguales por defecto** (20% cada sub-dimensión), señalados explícitamente como "pendiente de validar con panel AHP". Este documento diseña ese panel de forma ejecutable — quién debería estar, qué se les pide exactamente, y cómo se agregan sus respuestas — para que quede listo para correr, no solo mencionado como pendiente.

---

## 1. Qué se está validando (y qué NO)

El panel AHP (Analytic Hierarchy Process, Saaty 1980) sirve para reemplazar el supuesto de "las 5 sub-dimensiones pesan igual" por pesos derivados de comparaciones pareadas de expertos, con un indicador propio de qué tan consistentes fueron esas comparaciones.

**Dos matrices independientes, no una sola jerarquía combinada:**
1. Peso de las 5 sub-dimensiones de **IP** entre sí (Trazabilidad y origen / Cumplimiento ambiental / Capacidades organizacionales / Información y documentación / Capacidad de adaptación y acceso a recursos).
2. Peso de las 5 sub-dimensiones de **IV** entre sí (Dependencia del mercado europeo / Exposición regulatoria / Fragilidad productiva y territorial / Brechas tecnológicas y financieras / Riesgo social y comercial).

**No se pide un peso relativo entre IP e IV.** La relación entre ambos ya está fijada por la fórmula `RE_c = IV_c · (1 − IP_c/100)` (multiplicativa, no suma ponderada) — introducir un peso IP-vs-IV sería redundante y contradiría el propio diseño de RE.

**Fuera de alcance de esta primera ronda:** ponderar los ítems *dentro* de cada sub-dimensión (ej. D3 vs. D4 dentro de "Cumplimiento ambiental"). Esa granularidad duplica el esfuerzo del panel y, para las sub-dimensiones núcleo del reglamento, ya está resuelta por la regla de agregación geométrica (no admite compensación, por diseño, no por peso). Queda como una fase 2 opcional si el equipo del proyecto madre la pide explícitamente.

---

## 2. Composición del panel

**Tamaño recomendado: 8–10 expertos.** Justificación: la literatura de validez de contenido (Lynn, 1986) considera riesgoso un panel de menos de 6 (el acuerdo puede deberse al azar) y señala rendimientos decrecientes más allá de 10-15 — un panel de este tamaño es manejable logísticamente y suficiente para el cálculo de consistencia que exige AHP.

**Composición mixta por grupo de interés** (no solo académicos — esto es lo que le da validez de contenido real, no solo de escritorio):

| Grupo | N.º sugerido | Rol en el panel |
|---|---|---|
| Especialistas EUDR/legal-regulatorio | 2 | Juzgan qué tan crítico es "Cumplimiento ambiental" y "Exposición regulatoria" frente al resto — son quienes mejor conocen el costo real de un incumplimiento |
| Gerencia de cooperativas o gremios (JNC/APPCACAO/Central Café y Cacao) | 2 | Aportan el peso "desde adentro" — qué tan determinante es realmente la capacidad organizacional o la fragilidad territorial en la práctica, no solo en el papel |
| Certificación/sostenibilidad (Rainforest Alliance, Fairtrade, auditores) | 2 | Conocen de primera mano qué sub-dimensiones predicen mejor el desempeño en auditorías reales |
| Cooperación técnica en territorio (GIZ, EFI, PNCB) | 1–2 | Ven directamente la fragilidad productiva/territorial y las brechas tecnológicas — grupo que valida específicamente las sub-dimensiones de IV, menos representadas en los otros perfiles |
| Equipo académico/metodológico (proyecto madre ISCAM, Universidad del Pacífico) | 1–2 | Garantizan coherencia con el objetivo de investigación y manejan el aparato estadístico de agregación |

**No se fabrican nombres.** Esta tabla define roles y cantidades, no personas — la convocatoria real depende del equipo del proyecto madre y de los contactos ya identificados en `Directorio Preliminar - JNC y APPCACAO.md` (ej. la directiva JNC 2024–2027 es candidata natural para el grupo de gremios).

---

## 3. Procedimiento

1. **Sesión de nivelación conceptual (antes de comparar nada).** Se entrega a cada experto la definición exacta de las 5 sub-dimensiones de IP (o de IV, según la matriz) tal como quedaron en el Remapeo/Diseño de IV — sin esto, dos expertos pueden estar comparando cosas distintas bajo el mismo nombre. Formato: documento de una página + 15 min de aclaración de dudas, no una presentación larga.

2. **Comparaciones individuales, a ciegas entre expertos.** Cada experto llena su matriz por separado, sin ver las respuestas de los demás — igual que el principio de anonimato de un panel Delphi, para evitar que la opinión de alguien con más jerarquía arrastre al resto. Con 5 elementos por matriz, son **10 comparaciones pareadas por matriz** (n(n−1)/2), es decir 20 en total si el mismo experto evalúa IP e IV — una sesión de 30–45 minutos es realista.

3. **Escala de Saaty (1–9):** cada comparación pregunta "¿cuánto más importante es la sub-dimensión A frente a B para predecir preparación/vulnerabilidad?", con 1 = igual importancia, 3 = moderadamente más importante, 5 = fuertemente más importante, 7 = muy fuertemente, 9 = extrema, y valores pares como intermedios.

4. **Cálculo de consistencia (CR) por experto.** Antes de aceptar la matriz de un experto, se calcula su Índice de Consistencia (CI) y Radio de Consistencia (CR = CI/RI). Saaty (2008) fija el umbral en **CR ≤ 0.10 para matrices de 5×5** (el umbral es más estricto para matrices más chicas: 0.05 para 3×3, 0.08 para 4×4 — aplica el de 0.10 en nuestro caso). Una matriz con CR > 0.10 significa que el experto se contradijo (ej. dijo A>B, B>C, pero también C>A) — no se descarta al experto, se le devuelve su propia matriz señalando la inconsistencia y se le pide revisarla una vez, igual que una ronda de retroalimentación Delphi.

5. **Agregación entre expertos: media geométrica de las matrices, no de los pesos finales.** Este es el punto metodológico más importante y el que más se presta a error: Forman & Peniwati (1998) demuestran que cuando el panel actúa como un grupo que busca un juicio conjunto (no como partes con intereses distintos que hay que promediar por separado), la forma correcta de combinar N matrices de expertos es tomar la **media geométrica elemento por elemento de las matrices de comparación pareada** (método AIJ, *Aggregation of Individual Judgments*) y luego calcular los pesos finales sobre esa matriz agregada — no promediar aritméticamente los pesos ya calculados de cada experto por separado (eso sería AIP, *Aggregation of Individual Priorities*, apropiado solo cuando los expertos representan intereses en conflicto que deben promediarse, no es nuestro caso). Esto es coherente, además, con la preferencia ya justificada en la Metodología del ISA por la media geométrica sobre la aritmética (precedente IDH-PNUD 2010) — es la misma familia de argumento aplicada a un problema distinto.

6. **Reporte de consistencia global**, no solo de los pesos finales: el CR de la matriz agregada, más el rango de CR individuales de cada experto antes de la agregación — es la evidencia concreta que un revisor Q1/Q2 pediría para el pilar "ponderación explícita" (Comparativa §3.1).

---

## 4. Qué hacer con el resultado

- **Los pesos derivados del AHP reemplazan el 20% parejo por sub-dimensión** en las fórmulas de IP_c e IV_c ya definidas.
- **Sensibilidad obligatoria:** correr el índice con los pesos AHP y con los pesos iguales originales sobre el mismo piloto, y reportar la correlación de Spearman entre ambos rankings — esto ya estaba previsto como paso de robustez en la Metodología del ISA; aplica igual aquí. Si ambos rankings son casi idénticos, es evidencia de que el índice es robusto a la elección de pesos (buena noticia, no un panel desperdiciado); si difieren mucho, el panel AHP era necesario y su resultado debe primar.
- Documentar el resultado (matriz agregada, CR final, pesos resultantes) como un anexo metodológico del piloto — no reemplazar este documento de diseño, agregar los resultados reales cuando el panel se ejecute.

---

## 5. Pendientes

- [ ] Convocar el panel real (8–10 personas, composición de §2 y `Directorio - Pool de Expertos Panel AHP.xlsx`) — depende del equipo del proyecto madre, no se puede avanzar sin contactos confirmados.
- [x] **Instrumento de captura de comparaciones pareadas — construido 2026-09-16.** Artifact online: https://claude.ai/code/artifact/323b416c-1678-4fd0-a5c9-b02b7d874f1e. Wizard de 4 pasos (identificación → matriz IP → matriz IV → revisar y enviar), 10 comparaciones por matriz con la escala de Saaty (control segmentado de 9 posiciones), cálculo de CR en vivo con el umbral 0.10 (Saaty 2008), y una pestaña de "Resultados agregados" que calcula la media geométrica de las matrices de todos los expertos (método AIJ, Forman & Peniwati 1998) y sus pesos resultantes en tiempo real vía `db`. Piloto interno (mismo patrón/constraint que el Instrumento 2 online).
- [ ] Ejecutar la fase 2 opcional (ponderar ítems dentro de cada sub-dimensión) solo si el proyecto madre lo requiere explícitamente — no es parte de esta primera ronda.
