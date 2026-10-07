# Estructura de la Google Sheet de Respuestas — Instrumento 2

**Tarea:** Fase 1, Plan de Trabajo 75 días — "Definir la estructura de la Google Sheet de respuestas". Cerrado 2026-10-06.

**Principio de diseño:** una fila = una respuesta completa de una cooperativa al Instrumento 2 (Bloque 0 + Bloque P + D1–D11). Las columnas usan el **mismo ID de pregunta que `Scripts/matriz_data.py`** (ej. `D8.30`, no "pregunta 30 de gobernanza") para que el análisis posterior (carga al Excel `Modelo de Calculo - ISA-IP-IV-RE-AHP.xlsx`) lea la hoja sin tener que reconciliar nombres de columna a mano. Si Google Forms no permite fijar el texto del encabezado de columna directamente, renombrar la fila de encabezados de la Sheet de respuestas inmediatamente después de crear el Form, antes de la primera respuesta real.

**Total de columnas de datos:** 76 preguntas (12 Bloque 0 + 13 Bloque P + 51 de D1–D11) + 6 columnas de metadata = **82 columnas**.

---

## 1. Columnas de metadata (no vienen del instrumento — se agregan en la Sheet)

| Col | Nombre de columna | Origen | Notas |
|---|---|---|---|
| A | `timestamp` | Automático de Google Forms | No editar — es la marca de envío |
| B | `id_respuesta` | Fórmula `=ROW()-1` o UUID manual | Clave primaria de la fila |
| C | `RUC` | Pregunta B0.2 | **Clave de deduplicación entre fuentes** (mismo criterio que `Directorio Cooperativas Cafe-Cacao Peru (v3).xlsx` y `EUDRPERU_universo_consolidado.csv`) — usar para hacer JOIN contra el marco muestral, nunca el nombre comercial |
| D | `fecha_aplicacion` | Manual, campo del Form o del protocolo de campo | Fecha real de la entrevista, puede diferir del timestamp si se aplicó offline y se cargó después |
| E | `encuestador` | Manual, campo del Form | Para auditoría de calidad y detección de sesgo por encuestador |
| F | `canal_aplicacion` | Manual o desplegable fijo | `Google Form directo` / `Piggyback GIZ` / `Piggyback SAFE` / `Piggyback MIDAGRI` / `Evento gremial` — para el informe de Fase 4 ("qué funcionó del canal de despliegue") |

---

## 2. Bloque 0 — Ficha de identificación (12 columnas, no puntúa)

| Col | ID | Pregunta (resumen) | Tipo de dato en la Sheet |
|---|---|---|---|
| G | B0.1 | Nombre de la cooperativa / razón social | Texto |
| H | B0.2 | RUC | Texto (11 dígitos, duplicado de col. C para trazabilidad del Form) |
| I | B0.3 | Producto(s) exportado(s) (+ código SA si se conoce) | Texto |
| J | B0.4 | N.º de socios productores / hectáreas totales | Texto (dos valores, "socios\|hectáreas") |
| K | B0.5 | ¿Exporta directo a UE o a través de tercero? | Categórica: `Directo` / `Indirecto` |
| L | B0.6 | Si indirecto: ¿quién es el comprador? | Texto, vacío si B0.5=Directo |
| M | B0.7 | % aprox. volumen destinado a UE | Numérico 0–100 |
| N | B0.8 | País(es) de destino dentro de la UE | Texto, multivalor separado por `;` |
| O | B0.9 | Certificaciones voluntarias vigentes | Multivalor: `Rainforest Alliance;Fairtrade;Orgánico;UTZ;Otra;Ninguna` |
| P | B0.10 | Dispersión geográfica de los socios (insumo IV3) | Categórica: `Un solo distrito` / `Varios distritos, misma provincia` / `Varias provincias o regiones` |
| Q | B0.11 | Distancia a centro de acopio (insumo IV3) | Categórica: `<5km` / `5-20km` / `20-50km` / `>50km` / `No medido` |
| R | B0.12 | % de mujeres en la directiva (insumo IV5) | Numérico 0–100 |

---

## 3. Bloque P — Performance (13 columnas, no puntúa, es resultado no madurez)

| Col | ID | Pregunta (resumen) |
|---|---|---|
| S | P1 | Volumen exportado UE, último año |
| T | P1b | Volumen TOTAL exportado (todos destinos), último año — insumo IV1 |
| U | P2 | Volumen exportado UE, hace 3 años (retrospectivo) |
| V | P3 | Ingreso total por ventas de exportación a UE, último año |
| W | P4 | N.º compradores UE activos actualmente |
| X | P5 | N.º compradores UE activos hace 3 años (retrospectivo) |
| Y | P6 | Precio promedio pagado al socio, último año |
| Z | P7 | Precio promedio pagado al socio, hace 3 años (retrospectivo) |
| AA | P8 | ¿Lote rechazado/observado por trazabilidad/deforestación, últimos 2 años? (Sí/No/No sabe) |
| AB | P9 | Si P8=Sí: N.º aprox. de lotes rechazados |
| AC | P10 | ¿Perdió contrato/comprador UE por incumplimiento, últimos 2 años? (Sí/No/No sabe) |
| AD | P11 | % volumen exportado con trazabilidad verificada hasta parcela (criterio de validación externa, no promedia) |
| AE | P12 | N.º años consecutivos exportando a UE (criterio de validación externa, no promedia) |

**Indicadores derivados** (calcular en análisis, no son columnas de captura): `var_volumen_UE = (P1-P2)/P2`, `var_compradores = P4-P5`, `var_precio_socio = (P6-P7)/P7`.

---

## 4. D1–D11 (51 columnas)

| Col | ID | Pregunta (resumen) | Tipo |
|---|---|---|---|
| AF | D1.1 | Introduce producto bajo propio nombre en UE | Sí/No |
| AG | D1.2 | Transforma el producto antes de vender | Transforma/No transforma |
| AH | D1.3 | Sabe con certeza su rol EUDR | Sí con certeza/Idea aproximada/No sabe |
| AI | D1.4 | Cumple umbrales micro/pequeña empresa | Sí/No/No sabe |
| AJ | D2.5 | Existe geolocalización por parcela | 0–4 |
| AK | D2.6 | % socios con parcela geolocalizada | 0–100 |
| AL | D2.7 | Sistema vincula lote con parcela | 0–4 |
| AM | D2.8 | Quién levantó la información | Categórica (5 opciones) |
| AN | D2.9 | Frecuencia de actualización | Categórica (4 opciones) |
| AO | D2.10 | Mezcla física de lotes sin registro — **bandera roja** | 3 opciones |
| AP | D3.11 | % socios con título reconocido | 0–100 |
| AQ | D3.12 | Parcelas superpuestas a áreas protegidas/territorios indígenas | 4 opciones |
| AR | D3.13 | Verifica cumplimiento laboral a nivel finca | 0–4 |
| AS | D3.14 | Parcela en zona de desarrollo alternativo/conflicto | Sí/No/No verificado |
| AT | D3.14a | Autorización de uso de agua | 4 opciones |
| AU | D3.14b | Tratamiento aguas residuales cumple norma (autodeclarada, sin fuente de verificación) | 4 opciones |
| AV | D3.14c | Parcela en faja marginal (verificable externamente) | Sí/No/No sabe |
| AW | D3.14d | Derechos de terceros sobre la tierra | 6 opciones, promedia 4→0 |
| AX | D3.14e | Al día en obligaciones tributarias/aduaneras/comerciales | 4 opciones |
| AY | D3.14f | Mecanismos anticorrupción | 3 opciones |
| AZ | D3.14g | Proceso CLPI cuando corresponde — **verificación, no promedia** | 4 opciones |
| BA | D4.15 | Verificó cambio uso de suelo post 31-dic-2020 | 5 opciones |
| BB | D4.16 | Usa monitoreo satelital | 0–4 |
| BC | D4.17 | Conoce clasificación de riesgo de su zona | 3 opciones |
| BD | D5.18 | Procedimiento escrito de diligencia debida | 0–4 |
| BE | D5.18a | Política de deforestación formal escrita | 0–4 |
| BF | D5.18b | Prioriza riesgos con criterio probabilidad×impacto | 3 opciones |
| BG | D5.19 | Declaración de diligencia debida | 4 opciones |
| BH | D5.19a | Componentes del plan de gestión — **mapeo, no promedia** | Multivalor (7 opciones) |
| BI | D5.20 | Responsable designado EUDR | 3 opciones |
| BJ | D5.21 | Capacitación formal últimos 12 meses | 3 opciones |
| BK | D5.21a | Frecuencia de revisión del plan | 3 opciones |
| BL | D5.21b | Reporte de diligencia debida con indicadores | 3 opciones |
| BM | D6.22 | Presupuesto asignado EUDR | 3 opciones |
| BN | D6.23 | Digitalización de registros | 3 opciones |
| BO | D6.24 | Conectividad a internet | 3 opciones |
| BP | D6.25 | Gestionó apoyo externo | 4 opciones |
| BQ | D7.26 | Comprador exigió geolocalización/DD | 3 opciones |
| BR | D7.27 | Comprador ofrece financiamiento/AT condicionada | Sí/No |
| BS | D7.28 | Riesgo percibido de perder contrato — **no promedia con el resto de D7** | 4 opciones |
| BT | D8.29 | Asambleas informativas EUDR a socios | 0–4 |
| BU | D8.30 | % socios que entienden por qué se pide geolocalización — **único ítem de D8 que entra a IV5** (`fricción_D8 = 100 − D8.30`) | 0–100 |
| BV | D8.31 | Mecanismo interno para entrega de información | 3 opciones |
| BW | D8.32 | Rotación de directiva últimos 2 años | 3 opciones |
| BX | D9.33 | Costo de adecuación vs. presupuesto anual | 4 opciones |
| BY | D9.34 | Financió adecuación con deuda | 3 opciones |
| BZ | D9.35 | Riesgo de traslado de costo al socio | 4 opciones |
| CA | D10.36 | Cree que certificación ya cubre EUDR — **bandera, no promedia como madurez** | 4 opciones |
| CB | D10.37 | Le ofrecieron "certificación EUDR" como producto | Sí/No |
| CC | D11.38 | Actores con contacto activo — **mapeo, no promedia** | Multivalor (7 opciones) |
| CD | D11.39 | Actores conocidos no contactados, y por qué | Texto libre |

---

## 5. Encabezados listos para pegar en la fila 1 de la Google Sheet

```
timestamp	id_respuesta	RUC	fecha_aplicacion	encuestador	canal_aplicacion	B0.1	B0.2	B0.3	B0.4	B0.5	B0.6	B0.7	B0.8	B0.9	B0.10	B0.11	B0.12	P1	P1b	P2	P3	P4	P5	P6	P7	P8	P9	P10	P11	P12	D1.1	D1.2	D1.3	D1.4	D2.5	D2.6	D2.7	D2.8	D2.9	D2.10	D3.11	D3.12	D3.13	D3.14	D3.14a	D3.14b	D3.14c	D3.14d	D3.14e	D3.14f	D3.14g	D4.15	D4.16	D4.17	D5.18	D5.18a	D5.18b	D5.19	D5.19a	D5.20	D5.21	D5.21a	D5.21b	D6.22	D6.23	D6.24	D6.25	D7.26	D7.27	D7.28	D8.29	D8.30	D8.31	D8.32	D9.33	D9.34	D9.35	D10.36	D10.37	D11.38	D11.39
```

(Separador: tabulación — pegar directamente en A1 de la Sheet con "Pegar sin formato"; Google Sheets separa automáticamente por columna.)

---

## 6. Reglas de integridad para quien cargue la Sheet

1. **RUC (col. C) nunca queda vacío.** Es la clave de join contra `EUDRPERU_universo_consolidado.csv`. Si el Form se aplicó sin RUC a mano, completar después contra el marco muestral por nombre antes de analizar.
2. **No reordenar columnas** una vez iniciado el levantamiento — el script de carga al Excel de cálculo (a construir en Fase 3) asumirá posición fija por nombre de columna, no por letra.
3. **D2.10, D10.36 y D7.28 son banderas/excepciones** — no promediarlas junto con el resto de su dimensión al calcular D2, D10 o D7 (ver Instrumento 2, notas de puntaje).
4. **D5.19a y D11.38/D11.39 son de mapeo, no de madurez** — no entran a ningún promedio de dimensión; alimentan directamente el Instrumento 4.
5. Mantener esta fila de encabezados **congelada** (`Ver > Congelar > 1 fila`) para que no se pierda al ordenar o filtrar.
