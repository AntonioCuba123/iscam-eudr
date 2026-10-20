# Estructura de la Google Sheet de Respuestas — Instrumento 2

**Tarea:** Fase 1, Plan de Trabajo 75 días — "Definir la estructura de la Google Sheet de respuestas". Cerrado 2026-10-06.

**Principio de diseño:** una fila = una respuesta completa de una cooperativa al Instrumento 2 (Bloque 0 + Bloque P + D1–D11 + módulo Pacto Verde + PPWR + Bloque R). Las columnas usan el **mismo ID de pregunta que el Form** (ej. `D8.30`, no "pregunta 30 de gobernanza") para que el análisis posterior lea la hoja sin tener que reconciliar nombres de columna a mano. Si Google Forms no permite fijar el texto del encabezado de columna directamente, renombrar la fila de encabezados de la Sheet de respuestas inmediatamente después de crear el Form, antes de la primera respuesta real.

**Total de columnas de datos: 139** — 6 metadata + 17 Bloque 0 + 15 Bloque P + 68 D1–D11 + 21 módulo Pacto Verde (D12–D15, de las cuales 4 activas) + 2 PPWR + 10 Bloque R.

**Registro de cambios de columnas:**
- v0.3 (2026-10-12): +B0.13, +B0.14 (insumos IV3 territorio), +P13, +P14 (presión Pacto Verde / financiamiento verde), +D6.22a (base de datos centralizada), +D6.25a (respaldo de archivos), +D7.28b (presión CSDDD del comprador).
- v0.4 (2026-10-13): +D6.22b (tipo de sistema digital), +D6.25b (origen y prueba del protocolo de respaldo), +D7.28c (tipo y cobertura de documentación CSDDD/CSRD del comprador).
- **v0.4 final (2026-10-14, Instrumento 2 reforzado):** +B0.15, +B0.16, +B0.17 (tipo de organización, departamento, RNCA), +D1.3a (rol EUDR), +D2.5a, +D2.5b (proveedores externos), +D3.14h (autorizaciones ambientales), +D3.14i (sanciones OEFA/SINEFA), +D4.15a (alertas de deforestación), +D6.22c (personal de datos), +D7.26a (comprador UE/CSDDD), +D7.26b (cláusula contractual), +D10.36a (asesoría EUDR), +D11.39a (plataforma APPCACAO/JNC), +PP1, +PP2 (envases PPWR), +R1–R10 (indicadores PVE). Además, las versiones mínimas **D12.42, D13.45, D14.51 y D15.58** activan 4 de las 21 columnas reservadas del módulo Pacto Verde.
- Las letras de columna se recalcularon de extremo a extremo en v0.4 final: las versiones anteriores tenían letras colisionadas (los bloques P y D1 reiniciaban en `S` y `AF`), una fila duplicada (D5.18b) y filas declaradas sin letra (D6.22a/b, D6.25a/b, D7.28b/c). Las letras de esta versión son únicas de `A` a `EI`.

---

## 1. Columnas de metadata (no vienen del instrumento — se agregan en la Sheet)

| Col | Nombre de columna | Origen | Notas |
|---|---|---|---|
| A | `timestamp` | Automático de Google Forms | No editar — es la marca de envío |
| B | `id_respuesta` | Fórmula `=ROW()-1` o UUID manual | Clave primaria de la fila |
| C | `RUC` | Pregunta B0.2 | **Clave de deduplicación entre fuentes** (mismo criterio que `Directorio Cooperativas Cafe-Cacao Peru (v3).xlsx` y `EUDRPERU_universo_consolidado.csv`) — usar para unir contra el marco muestral, nunca el nombre comercial |
| D | `fecha_aplicacion` | Manual, campo del Form o del protocolo de campo | Fecha real de la entrevista, puede diferir de la marca de tiempo si se aplicó sin conexión y se cargó después |
| E | `encuestador` | Manual, campo del Form | Para auditoría de calidad y detección de sesgo por encuestador |
| F | `canal_aplicacion` | Manual o desplegable fijo | `Google Form directo` / `Piggyback GIZ` / `Piggyback SAFE` / `Piggyback MIDAGRI` / `Evento gremial` — para el informe de Fase 4 ("qué funcionó del canal de despliegue") |

---

## 2. Bloque 0 — Ficha de identificación (17 columnas, no puntúa)

| Col | ID | Pregunta (resumen) | Tipo de dato en la Sheet |
|---|---|---|---|
| G | B0.1 | Nombre de la cooperativa / razón social | Texto |
| H | B0.2 | RUC | Texto (11 dígitos, duplicado de col. C para trazabilidad del Form) |
| I | B0.3 | Producto(s) exportado(s) (+ código SA si se conoce) | Texto |
| J | B0.4 | N.º de socios productores / hectáreas totales | Texto (dos valores, "socios\|hectáreas") |
| K | B0.5 | ¿Exporta directo a UE o a través de tercero? | Categórica: `Directo` / `Indirecto` |
| L | B0.6 | Si indirecto: ¿quién es el comprador? | Texto, vacío si B0.5=Directo |
| M | B0.7 | % aprox. volumen destinado a UE | Numérico 0–100 |
| N | B0.8 | Destino(s) de exportación, principal primero (dentro y fuera de la UE) (v0.4) | Texto, multivalor separado por `;` |
| O | B0.9 | Certificaciones voluntarias vigentes | Multivalor: `Rainforest Alliance;Fairtrade;Orgánico;UTZ;Otra;Ninguna` |
| P | B0.10 | Dispersión geográfica de los socios (insumo IV3) | Categórica: `Un solo distrito` / `Varios distritos, misma provincia` / `Varias provincias o regiones` |
| Q | B0.11 | Distancia a centro de acopio (insumo IV3) | Categórica: `<5km` / `5-20km` / `20-50km` / `>50km` / `No medido` |
| R | B0.12 | % de mujeres en la directiva (insumo IV5) | Numérico 0–100 |
| S | B0.13 | % socios en zonas riesgo alto/muy alto deforestación — insumo IV3 (v0.3) | Categórica: `<10%` / `10–30%` / `30–60%` / `>60%` / `No evaluado` |
| T | B0.14 | Capacidad técnica de verificación directa en campo — insumo IV3/IP3 (v0.3) | Categórica: `No tiene` / `Parcial <50%` / `Parcial >50%` / `Suficiente` |
| U | B0.15 | Tipo de organización (v0.4) — alimenta `MATRIZ_174!P` (hoy aproximación de IV5) | Categórica: `Asociación` / `Cooperativa agraria` / `Cooperativa de servicios` / `Central o federación` / `Empresa` / `Otro` |
| V | B0.16 | Departamento (y provincia) de la sede (v0.4) — validación cruzada contra SUNAT y contra `MATRIZ_174!C` | Texto |
| W | B0.17 | ¿Inscrita en el RNCA? (v0.4) — insumo IV2 diseñado | Categórica: `Sí` / `En trámite` / `No` / `No aplica` |

---

## 3. Bloque P — desempeño (15 columnas, no puntúa, es resultado no madurez)

| Col | ID | Pregunta (resumen) | Tipo |
|---|---|---|---|
| X | P1 | Volumen exportado UE, último año | Texto (valor + unidad) |
| Y | P1b | Volumen TOTAL exportado (todos destinos), último año — insumo IV1 | Texto (valor + unidad) |
| Z | P2 | Volumen exportado UE, hace 3 años (retrospectivo) | Texto (valor + unidad) |
| AA | P3 | Ingreso total por ventas de exportación a UE, último año | Texto (valor + moneda) |
| AB | P4 | N.º compradores UE activos actualmente — insumo IV1 | Numérico |
| AC | P5 | N.º compradores UE activos hace 3 años (retrospectivo) | Numérico |
| AD | P6 | Precio promedio pagado al socio, último año | Texto (valor + moneda) |
| AE | P7 | Precio promedio pagado al socio, hace 3 años (retrospectivo) | Texto (valor + moneda) |
| AF | P8 | ¿Lote rechazado/observado por trazabilidad/deforestación, últimos 2 años? | `Sí` / `No` / `No sabe` |
| AG | P9 | Si P8=Sí: N.º aprox. de lotes rechazados | Numérico, vacío si P8≠Sí |
| AH | P10 | ¿Perdió contrato/comprador UE por incumplimiento, últimos 2 años? | `Sí` / `No` / `No sabe` |
| AI | P11 | % volumen exportado con trazabilidad verificada hasta parcela (criterio de validación externa, no promedia) | Numérico 0–100 |
| AJ | P12 | N.º años consecutivos exportando a UE (criterio de validación externa, no promedia) | Numérico |
| AK | P13 | Comprador exigió requisitos PV más allá del EUDR — insumo variable resultado PV (v0.3) | Ordinal 4 niveles |
| AL | P14 | Accedió/intentó acceder a financiamiento verde/crédito de impacto (v0.3) | Ordinal 4 niveles |

**Indicadores derivados** (calcular en análisis, no son columnas de captura): `var_volumen_UE = (P1-P2)/P2`, `var_compradores = P4-P5`, `var_precio_socio = (P6-P7)/P7`.

---

## 4. D1–D11 (68 columnas)

| Col | ID | Pregunta (resumen) | Tipo |
|---|---|---|---|
| AM | D1.1 | Introduce producto bajo propio nombre en UE | Sí/No |
| AN | D1.2 | Transforma el producto antes de vender | Transforma/No transforma |
| AO | D1.3 | Sabe con certeza su rol EUDR | Sí con certeza/Idea aproximada/No sabe |
| AP | D1.3a | Rol EUDR explícito (rama de D1.3, v0.4) | 5 opciones |
| AQ | D1.4 | Cumple umbrales micro/pequeña empresa | Sí/No/No sabe |
| AR | D2.5 | Existe geolocalización por parcela | 0–4 |
| AS | D2.6 | % socios con parcela geolocalizada | 0–100 |
| AT | D2.7 | Sistema vincula lote con parcela | 0–4 |
| AU | D2.8 | Quién levantó la información | Categórica (5 opciones) |
| AV | D2.9 | Frecuencia de actualización | Categórica (4 opciones) |
| AW | D2.10 | Mezcla física de lotes sin registro — **bandera roja** | 3 opciones |
| AX | D2.5a | % volumen de proveedores externos no socios (v0.4) | 5 opciones |
| AY | D2.5b | Trazabilidad de proveedores externos (rama de D2.5a, v0.4) | 5 opciones |
| AZ | D3.11 | % socios con título reconocido | 0–100 |
| BA | D3.12 | Parcelas superpuestas a ANP/zona amortiguamiento, reservas o territorios indígenas (v0.4: opción ANP) | 5 opciones |
| BB | D3.13 | Verifica cumplimiento laboral a nivel finca | 0–4 |
| BC | D3.14 | Parcela en zona de desarrollo alternativo/conflicto | Sí/No/No verificado |
| BD | D3.14a | Autorización de uso de agua | 4 opciones |
| BE | D3.14b | Tratamiento aguas residuales cumple norma (autodeclarada) | 4 opciones |
| BF | D3.14c | Parcela en faja marginal (verificable externamente) | Sí/No/No sabe |
| BG | D3.14d | Derechos de terceros sobre la tierra | 6 opciones, promedia 4→0 |
| BH | D3.14e | Al día en obligaciones tributarias/aduaneras/comerciales | 4 opciones |
| BI | D3.14f | Mecanismos anticorrupción | 3 opciones |
| BJ | D3.14g | Proceso CLPI cuando corresponde — **verificación, no promedia** | 4 opciones |
| BK | D3.14h | Autorizaciones ambientales vigentes (EIA/DIA/forestal) (v0.4) — variable `aut_ambiental` del proxy | 4 opciones |
| BL | D3.14i | Proceso sancionador vigente OEFA/SINEFA (v0.4) — variable `sancion_oea`; **bandera**, reemplaza el puntaje de legalidad externo con corte 2024-04 | 4 opciones |
| BM | D4.15 | Verificó cambio uso de suelo post 31-dic-2020 con cruce GEOSERFOR/PNCB/GFW (v0.4) | 5 opciones |
| BN | D4.16 | Usa monitoreo satelital | 0–4 |
| BO | D4.17 | Conoce clasificación de riesgo de su zona | 3 opciones |
| BP | D4.15a | Alertas activas de deforestación en parcelas de socios (v0.4) — variable `alerta_deforest`; **bandera** | 4 opciones |
| BQ | D5.18 | Procedimiento escrito de diligencia debida | 0–4 |
| BR | D5.18a | Política de deforestación formal escrita | 0–4 |
| BS | D5.18b | Prioriza riesgos con criterio probabilidad×impacto | 3 opciones |
| BT | D5.19 | Declaración de diligencia debida | 4 opciones |
| BU | D5.19a | Componentes del plan de gestión — **mapeo, no promedia** | Multivalor (7 opciones) |
| BV | D5.20 | Responsable designado EUDR | 3 opciones |
| BW | D5.21 | Capacitación formal últimos 12 meses | 3 opciones |
| BX | D5.21a | Frecuencia de revisión del plan | 3 opciones |
| BY | D5.21b | Reporte de diligencia debida con indicadores | 3 opciones |
| BZ | D6.22 | Presupuesto asignado EUDR, distingue partida de tecnología y datos (v0.4) | 4 opciones |
| CA | D6.22a | Base de datos centralizada socio-parcela-lote (v0.3) | 4 opciones |
| CB | D6.22b | Tipo de sistema digital (rama de D6.22a, v0.4) | 4 opciones |
| CC | D6.22c | Personal asignado a gestión de datos (v0.4) — variable `personal_datos` del proxy | 4 opciones |
| CD | D6.23 | Digitalización de registros | 3 opciones |
| CE | D6.24 | Conectividad a internet | 3 opciones |
| CF | D6.25 | Gestionó apoyo externo | 4 opciones |
| CG | D6.25a | Respaldos recuperables en <48h (v0.3) | 4 opciones |
| CH | D6.25b | Origen del protocolo y última prueba (rama de D6.25a, v0.4) | 6 opciones |
| CI | D7.26 | Comprador exigió geolocalización/DD | 3 opciones |
| CJ | D7.27 | Comprador ofrece financiamiento/AT condicionada | Sí/No |
| CK | D7.28 | Riesgo percibido de perder contrato — **no promedia con el resto de D7** | 4 opciones |
| CL | D7.28b | Comunicación de obligaciones CSDDD/CSRD del comprador (v0.3) | 4 opciones |
| CM | D7.28c | Tipo y cobertura de documentación del comprador (rama de D7.28b, v0.4) | Multivalor (8 opciones) |
| CN | D7.26a | Comprador principal UE o sujeto a CSDDD (v0.4) — variable `comprador_ue` | 4 opciones |
| CO | D7.26b | Contrato escrito con cláusula de diligencia/geolocalización (v0.4) — variable `contrato_eudr` | 4 opciones |
| CP | D8.29 | Asambleas informativas EUDR a socios | 0–4 |
| CQ | D8.30 | % socios que entienden por qué se pide geolocalización — **único ítem de D8 que entra a IV5** (`fricción_D8 = 100 − D8.30`) | 0–100 |
| CR | D8.31 | Mecanismo interno para entrega de información | 3 opciones |
| CS | D8.32 | Rotación de directiva últimos 2 años | 3 opciones |
| CT | D9.33 | Costo de adecuación vs. presupuesto anual | 4 opciones |
| CU | D9.34 | Cómo financia la adecuación (v0.4: incluye fuente identificada) — variable `financiamiento` | 5 opciones |
| CV | D9.35 | Riesgo de traslado de costo al socio | 4 opciones |
| CW | D10.36 | Cree que certificación ya cubre EUDR — **bandera, no promedia como madurez** | 4 opciones |
| CX | D10.37 | Le ofrecieron "certificación EUDR" como producto | Sí/No |
| CY | D10.36a | Asesoría específica sobre EUDR (v0.4) — variable `asesoria_eudr` | 4 opciones |
| CZ | D11.38 | Actores con contacto activo — **mapeo, no promedia** | Multivalor (7 opciones) |
| DA | D11.39 | Actores conocidos no contactados, y por qué | Texto libre |
| DB | D11.39a | Inscrita en plataforma de trazabilidad APPCACAO/JNC (v0.4) — variable `plataforma_traz` | 4 opciones |

---

## 5. Módulo D12–D15 — Pacto Verde (21 columnas reservadas, 4 activas)

> **Activas con el Form v0.4 (versión mínima 0/1/2):** D12.42, D13.45, D14.51, D15.58 — activan las columnas `W:Z` de `MATRIZ_174` y con ellas ISA-PV (30% de ISA-Completo), hoy en ceros.
> **Pendientes de evaluación de comprensibilidad con el técnico de campo** (protocolo `DOC_TRABAJO_Instrumento2_ISCAM_v2.md` §10.2): las 17 columnas restantes. Sus letras quedan reservadas para no recalcular la Sheet cuando se escalen.

| Col | ID | Pregunta (resumen) | Tipo |
|---|---|---|---|
| DC | D12.40 | Conoce CalCafé v2.1 o equivalente cacao | 4 opciones — pendiente |
| DD | D12.41 | Registra insumos para huella (fertilizantes, combustible, energía, distancia) | 4 opciones — pendiente |
| DE | D12.42 | Mide/calcula huella de carbono (alcance 1 y 2) — **activa, versión mínima 0/1/2** | 3 opciones: `No (0)` / `En curso (1)` / `Verificada por tercero (2)` |
| DF | D12.43 | Tiene objetivo cuantificado de reducción de emisiones | 4 opciones — pendiente |
| DG | D12.44 | Reporta huella a compradores/plataformas (CDP, etc.) | 4 opciones — pendiente |
| DH | D13.45 | Elabora y publica reporte anual de sostenibilidad / memoria RSE — **activa, versión mínima 0/1/2** | 3 opciones: `No (0)` / `En preparación (1)` / `Publicado (2)` |
| DI | D13.46 | Reporte incluye indicadores ambientales (deforestación, carbono, agua, biodiversidad, residuos) | 4 opciones — pendiente |
| DJ | D13.47 | Reporte incluye indicadores sociales (trabajo infantil, forzoso, igualdad, mujeres, salud) | 4 opciones — pendiente |
| DK | D13.48 | Reporte incluye indicadores de gobernanza (directiva, anticorrupción, riesgos, canal denuncias) | 4 opciones — pendiente |
| DL | D13.49 | Información verificada/auditada por tercero independiente | 4 opciones — pendiente |
| DM | D13.50 | Reporte se comparte proactivamente con compradores UE y partes interesadas | 3 opciones — pendiente |
| DN | D14.51 | Gestiona residuos y subproductos del beneficio (economía circular) — **activa, versión mínima 0/1/2** | 3 opciones: `No (0)` / `En transición (1)` / `Avanzado (2)` |
| DO | D14.52 | Envases de exportación: reutilizables/reciclables/compostables | 4 opciones — pendiente (PP1/PP2 cubren el caso sacos) |
| DP | D14.53 | Plan de reducción de plásticos de un solo uso (bolsas, film, flejes, etiquetas) | 4 opciones — pendiente |
| DQ | D14.54 | Subproductos valorizados (cáscara→biocombustible, mucílago→bioinsumos, agua→riego) | 4 opciones — pendiente |
| DR | D14.55 | Trazabilidad de envases y residuos por lote exportado | 4 opciones — pendiente |
| DS | D15.56 | Conoce los LMR de la UE y alertas RASFF para su producto | 4 opciones — pendiente |
| DT | D15.57 | Protocolo interno que prohíbe/restringe pesticidas según LMR de la UE | 4 opciones — pendiente |
| DU | D15.58 | Realiza análisis/monitoreo de residuos de pesticidas sobre producto de exportación — **activa, versión mínima 0/1/2** | 3 opciones: `No verificado (0)` / `En monitoreo interno (1)` / `Cumple límites UE verificado (2)` |
| DV | D15.59 | Comprador europeo ha exigido certificados de análisis o declaraciones LMR | 4 opciones — pendiente |
| DW | D15.60 | Lote retenido/observado/rechazado en frontera UE por exceso de pesticidas — **bandera** | 4 opciones — pendiente |

---

## 6. PPWR y Bloque R (12 columnas nuevas, v0.4)

> No alimentan ISA-EUDR. PP1/PP2 alimentan `SCORECARDS!M` (PPWR) y el ponderador editable de `PONDERADORES!A18` (5% del índice PVE). R1–R10 alimentan las columnas PVE `AC, AE–AN` de `MATRIZ_174` y `AO` (P_Global). El prefijo **R** evita la colisión con las columnas `P1–P14` de `MATRIZ_174` (indicadores PVE) y con el Bloque P del Form (desempeño comercial).

| Col | ID | Pregunta (resumen) | Tipo |
|---|---|---|---|
| DX | PP1 | Tipo de saco de exportación principal — variable `tipo_saco` del proxy | Categórica (5 opciones) |
| DY | PP2 | Sacos con certificación FSC o equivalente — variable `fsc` del proxy | `Sí` / `No` / `No sabe` |
| DZ | R1 | % socios con acceso a crédito → `MATRIZ_174!AC` (P3) | Numérico 0–100 |
| EA | R2 | % socios formalizados (contrato/planilla/seguridad social) → `AE` (P5) | Numérico 0–100 |
| EB | R3 | Capacitaciones por socio al año → `AF` (P6) | Numérico |
| EC | R4 | % socios de hace 3 años que siguen activos → `AG` (P7) | Numérico 0–100 |
| ED | R5 | % ingresos de productos distintos del café/cacao → `AH` (P8) | Numérico 0–100 |
| EE | R6 | % volumen en mercados premium o con prima → `AI` (P9) | Numérico 0–100 |
| EF | R7 | Inversión en adecuación EUDR último año (moneda) → `AJ` (P10) | Texto (valor + moneda) |
| EG | R8 | % reclamos de socios resueltos → `AL` (P12) | Numérico 0–100 |
| EH | R9 | % energía de fuentes renovables → `AM` (P13) | Numérico 0–100 |
| EI | R10 | % residuos del beneficio gestionados con tratamiento → `AN` (P14) | Numérico 0–100 |

Indicadores PVE que **no** se preguntan en el Form (derivar en análisis): P1 productividad y P2 ingreso neto USD/ha (de P3 + B0.4); P4 puntaje de género (de B0.12); P11 puntaje de trazabilidad (de la pregunta P11).

---

## 7. Encabezados listos para pegar en la fila 1 de la Google Sheet

```
timestamp	id_respuesta	RUC	fecha_aplicacion	encuestador	canal_aplicacion	B0.1	B0.2	B0.3	B0.4	B0.5	B0.6	B0.7	B0.8	B0.9	B0.10	B0.11	B0.12	B0.13	B0.14	B0.15	B0.16	B0.17	P1	P1b	P2	P3	P4	P5	P6	P7	P8	P9	P10	P11	P12	P13	P14	D1.1	D1.2	D1.3	D1.3a	D1.4	D2.5	D2.6	D2.7	D2.8	D2.9	D2.10	D2.5a	D2.5b	D3.11	D3.12	D3.13	D3.14	D3.14a	D3.14b	D3.14c	D3.14d	D3.14e	D3.14f	D3.14g	D3.14h	D3.14i	D4.15	D4.16	D4.17	D4.15a	D5.18	D5.18a	D5.18b	D5.19	D5.19a	D5.20	D5.21	D5.21a	D5.21b	D6.22	D6.22a	D6.22b	D6.22c	D6.23	D6.24	D6.25	D6.25a	D6.25b	D7.26	D7.27	D7.28	D7.28b	D7.28c	D7.26a	D7.26b	D8.29	D8.30	D8.31	D8.32	D9.33	D9.34	D9.35	D10.36	D10.37	D10.36a	D11.38	D11.39	D11.39a	D12.40	D12.41	D12.42	D12.43	D12.44	D13.45	D13.46	D13.47	D13.48	D13.49	D13.50	D14.51	D14.52	D14.53	D14.54	D14.55	D15.56	D15.57	D15.58	D15.59	D15.60	PP1	PP2	R1	R2	R3	R4	R5	R6	R7	R8	R9	R10
```

(Separador: tabulación — pegar directamente en A1 de la Sheet con "Pegar sin formato"; Google Sheets separa automáticamente por columna. **139 columnas totales**, de `A` a `EI`.)

---

## 8. Reglas de integridad para quien cargue la Sheet

1. **RUC (col. C) nunca queda vacío.** Es la clave de unión contra `EUDRPERU_universo_consolidado.csv`. Si el Form se aplicó sin RUC a mano, completar después contra el marco muestral por nombre antes de analizar.
2. **No reordenar columnas** una vez iniciado el levantamiento — el script de carga asumirá posición fija por nombre de columna, no por letra. Las letras de este documento son la referencia canónica de la versión v0.4.
3. **Banderas/excepciones: D2.10, D2.5b, D3.14i, D4.15a, D7.28, D10.36, D15.60** — no promediarlas junto con el resto de su dimensión; reportar siempre por separado.
4. **Mapeo (no promedian): D5.19a, D7.28c, D11.38/D11.39** — alimentan directamente el Instrumento 4; no entran a ningún promedio.
5. **D12–D15 (ISA-PactoVerde) no promedian en ISA-EUDR** — alimentan ISA-PV (media aritmética simple) e ISA-Completo (70/30). Hoy solo 4 de las 21 columnas se capturan (D12.42, D13.45, D14.51, D15.58); las demás quedan vacías hasta que se escalen sus preguntas.
6. **B0.13 y B0.14 no puntúan** — son contexto puro para IV3; no entran a ningún índice. B0.15–B0.17 tampoco puntúan: B0.15 y B0.16 alimentan la matriz de organizaciones (`P` y departamento) y B0.17 alimenta IV2.
7. **PP1/PP2 no alimentan ISA-EUDR** — van a `SCORECARDS!M` y al ponderador PPWR. **R1–R10 no alimentan ISA-EUDR** — van a `MATRIZ_174!AC, AE–AN` y a `P_Global` (`AO`).
8. **Ramas condicionales** (dejar la celda vacía si la rama no aplica, no inventar valor): B0.5→B0.6; P8→P9; D1.3→D1.3a; D2.5a→D2.5b; D6.25a→D6.25b; D7.28b→D7.28c.
9. Mantener esta fila de encabezados **congelada** (`Ver > Congelar > 1 fila`) para que no se pierda al ordenar o filtrar.
