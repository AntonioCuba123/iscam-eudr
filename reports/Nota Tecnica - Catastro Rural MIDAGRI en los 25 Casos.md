# Nota Técnica: Cobertura del Catastro Rural de MIDAGRI en los territorios de las 25 organizaciones cafetaleras

Oct 9, 2026 · Documento de trabajo, complementario al informe "Nivel de preparación frente al EUDR en 25 cooperativas cafetaleras peruanas"

## 1. Objetivo

El informe principal (sección 4.11, mapa de cobertura hacia el índice IP/IV de ISCAM) dejó marcado IP1 (Trazabilidad y origen, Art. 9 EUDR) como **"Parcial"**: el PPA confirma inscripción organizacional al 100%, pero no hay fuente administrativa que confirme geolocalización o titulación a nivel de parcela/socio individual. Esta nota consulta en vivo el geoservicio público del Catastro Rural de MIDAGRI para ver qué tan lejos llega una fuente real y verificable en cerrar ese hueco específico — sin inventar una conclusión que los datos no sostienen.

**Resultado adelantado, para no enterrarlo:** el geoservicio aporta contexto territorial real y verificable, pero **no puede vincularse a las 25 organizaciones ni a sus socios por nombre, DNI o RUC** — es información anonimizada por distrito. Lo que sí permite, con matices que se explican abajo, es detectar en qué zonas el catastro parece claramente atrasado frente a lo que las propias organizaciones declaran tener.

## 2. Fuente y método

**Fuente:** geoservicio público de MIDAGRI, `https://georural.midagri.gob.pe/geoservicios/rest/services/public/Catastro_Rural/MapServer` (ArcGIS REST Server, sin autenticación, consultado el 9 de octubre de 2026).

**Capas usadas:**
- Capa 0, **"Predio Rural"**: 19 campos — geometría, `area_ha`, `id_dist` (ubigeo INEI de 6 dígitos), `cod_predio`, `num_predio`, `observacion`. **No tiene** campo de titular, DNI, RUC, fecha de actualización, ni estado de titulación.
- Capa 8, **"Proyectos Catastrales"**: nombre y código de cada proyecto catastral vigente, a nivel de **departamento** (no de distrito).

**Método:** se identificaron los 16 distritos únicos (ubigeo) donde están las 25 organizaciones de `base 25 detallada (café)`, y se consultó la capa 0 agrupando por distrito (`groupByFieldsForStatistics`), sumando número de predios y hectáreas catastradas por distrito. Se consultó también el total nacional de la capa, y la capa 8 para los 7 departamentos involucrados (Amazonas, Ayacucho, Cajamarca, Cusco, Junín, Pasco, San Martín).

**Script reproducible:** `consulta_catastro_rural_25_orgs.py` (en esta misma carpeta) — ejecuta las consultas en vivo y genera `catastro_rural_25_orgs.xlsx`. Nota técnica de entorno: el servidor no envía la cadena de certificados TLS completa; `requests` con el almacén `certifi` por defecto rechaza la conexión aunque el navegador y `curl` la aceptan (porque usan el almacén de certificados de Windows). El script usa el paquete `truststore` para que `requests` use ese mismo almacén del sistema, sin desactivar la verificación de certificados.

**Contexto nacional:** la capa 0 contiene **3,060,135 predios** a nivel Perú (consultado directamente, no tomado de un artículo de prensa — una nota de prensa de MIDAGRI citó "más de 3.5 millones", del mismo orden de magnitud pero no idéntico; no se puede explicar la diferencia sin más información, posiblemente actualización de la capa en fechas distintas).

## 3. Resultado por distrito

| Ubigeo | Región | Provincia / Distrito | Organizaciones | Socios decl. | Ha declaradas | Predios catastrados (distrito) | Ha catastradas (distrito) |
|---|---|---|---|---|---|---|---|
| 050510 | Ayacucho | La Mar / Anchihuay | Yuraq Yacu | 94 | 94.0 | **0** | **0.0** |
| 220105 | San Martín | Moyobamba / Soritor | Valle Grande | 622 | 4,031.0 | 198 | 770.8 |
| 220201 | San Martín | Bellavista / Bellavista | Valle del Biavo, Cordillera Azul | 797 | 2,391.0 | 43 | 614.5 |
| 220501 | San Martín | Lamas / Lamas | CAFCER | 698 | 921.1 | 519 | 983.1 |
| 010513 | Amazonas | Luya / Ocumal | OCUMAL | 256 | 685.0 | 18 | 1,009.9 |
| 060901 | Cajamarca | San Ignacio / San Ignacio | CASIL, APROCASJ | 483 | 1,136.0 | 1,641 | 2,829.0 |
| 220104 | San Martín | Moyobamba / Jepelacio | Cerro Blanco | 187 | 600.0 | 1,345 | 3,688.7 |
| 120302 | Junín | Chanchamayo / Perené | La Florida | 450 | 1,605.8 | 2,512 | 9,360.0 |
| 080901 | Cusco | La Convención / Santa Ana | Aguilayoc, Pumacahua, COCLA, Ccochapampa | 986 | 2,493.9 | 5,550 | 13,365.9 |
| 010706 | Amazonas | Utcubamba / Lonya Grande | Lonya Grande, Line Coffee Marañón | 495 | 1,387.9 | 2,189 | 8,857.0 |
| 220101 | San Martín | Moyobamba / Moyobamba | APROSELVANOR, Asoc. San Martín | 1,559 | 3,610.0 | 11,422 | 33,328.8 |
| 120607 | Junín | Satipo / Río Negro | Rosas Pampa | 162 | 454.5 | 2,007 | 7,833.5 |
| 120303 | Junín | Chanchamayo / Pichanaki | Tropical Products, Chankas | 460 | 1,380.0 | 5,878 | 21,664.0 |
| 080905 | Cusco | La Convención / Ocobamba | Tirijuay Pavayoc | 74 | 150.0 | 1,670 | 12,083.8 |
| 190307 | Pasco | Oxapampa / Villa Rica | CEMCAVIR (Villa Rica) | 177 | 213.0 | 3,382 | 19,555.1 |
| 080408 | Cusco | Calca / Yanatile | Chancamayo, Jorge Chávez | 80 | 82.0 | 4,586 | 58,026.8 |

*(ordenado de menor a mayor "ratio ha catastradas / ha declaradas" — ver lectura en la sección 4, no es una tabla de ordenamiento de cobertura)*

## 4. Lectura honesta de la tabla — qué sí dice y qué no dice

**Las hectáreas catastradas del distrito son de TODOS los predios rurales del distrito, no solo de los socios de estas organizaciones.** Un distrito agrícola tiene miles de predios de personas sin relación alguna con estas 25 cafetaleras. Por eso, cuando el total catastrado del distrito es *mayor* que lo que las organizaciones declaran (la mayoría de los casos de la tabla, con ratios de 1.1 a más de 700), **eso no prueba que el socio de esa cooperativa tenga su parcela catastrada o titulada** — simplemente el distrito tiene mucha actividad catastral ajena a la cooperativa. No se puede leer ese número como "% de cobertura" de la organización.

**Lo que sí es una señal dura y interpretable es cuando el total catastrado del distrito es *menor* que lo que una sola organización declara tener.** Si ni sumando todos los predios catastrados de todo el distrito se alcanza el área que una cooperativa dice tener ella sola, eso es evidencia directa de atraso catastral real en esa zona — no una inferencia, un hecho aritmético. Hay exactamente **tres casos así** en la muestra:

- **Anchihuay (La Mar, Ayacucho)** — Yuraq Yacu: **0 predios catastrados** en todo el distrito, frente a 94 ha declaradas por la cooperativa. Es el caso más severo. Dato adicional honesto: la capa 8 sí lista un proyecto catastral nombrado para la provincia ("0502W LA MAR - CHILCA" y "165/PAY1 SAN FRANCISCO - PICHARI - RIO ENE"), es decir, hay un proyecto catastral formalmente existente para la zona, pero cero predios digitizados en la capa pública — no se puede distinguir si es porque el levantamiento no ha llegado aún a Anchihuay específicamente, o si la capa pública no está actualizada para esa zona.
- **Soritor (Moyobamba, San Martín)** — Valle Grande: solo 770.8 ha catastradas en todo el distrito, frente a 4,031 ha que esta única cooperativa declara (622 socios). El distrito completo catastrado no llega a un quinto de lo que un solo gremio reporta tener.
- **Bellavista (San Martín)** — Valle del Biavo + Cordillera Azul: 614.5 ha catastradas en todo el distrito, frente a 2,391 ha declaradas entre las dos organizaciones.

Es notable que los tres casos más severos están en San Martín/Ayacucho — exactamente la región de mayor volumen exportador de la muestra (Valle Grande es el mayor exportador de las 25 organizaciones, según el informe principal). Esto no es una coincidencia menor: el mayor peso comercial de la muestra coincide con el atraso catastral más documentado.

Dos casos quedan en zona ambigua, apenas sobre 1 (Ocumal 1.47, Lamas/CAFCER 1.07) — ni confirman ni descartan atraso, están demasiado cerca del límite para concluir algo.

## 5. Proyectos catastrales nombrados (capa 8)

Se encontraron **155 proyectos catastrales** nombrados en los 7 departamentos de interés (lista completa en `catastro_rural_25_orgs.xlsx`, hoja `proyectos_catastrales`). Esta capa solo tiene granularidad departamental, no distrital, así que **no se puede confirmar que un proyecto nombrado cubra exactamente el distrito de una organización específica** — solo que existe, con ese nombre, en el departamento correspondiente. Ejemplos que por nombre parecen corresponder directamente a zonas de la muestra: "JUN1 CHANCHAMAYO" y "JUN3 GPS PICHANAKI" (Junín), "PAS7 VILLARICA" (Pasco), "088 LA CONVENCION" (Cusco), "JAE1/JAE2 SAN IGNACIO - JAEN" (Cajamarca), "2210W ALTO MAYO", "2508 ALTO BIAVO" y "2509 BAJO BIAVO" (San Martín) — estos últimos dos, justamente, nombran la zona de Bellavista donde se documentó el déficit catastral del punto anterior: hay un proyecto con ese nombre, pero los predios reales catastrados en el distrito siguen siendo pocos.

## 6. Limitaciones (explícitas, no omitidas)

1. **Sin vínculo a personas u organizaciones.** La capa pública no tiene titular, DNI ni RUC. No se puede verificar si un socio específico de una cooperativa específica tiene o no su predio catastrado — solo se puede hablar a nivel de distrito completo.
2. **"Catastrado" no es "titulado".** El campo `observacion` (revisado directamente, con muestras reales) distingue "Una persona vinculada" de "Varias personas vinculadas, ver Sistema SSET" — es decir, señala si el predio tiene un solo reclamante o varios en disputa/trámite en el Sistema de Saneamiento (SSET), pero no confirma si el predio ya tiene título inscrito. Catastro (levantamiento/medición) y título (derecho de propiedad inscrito) son procesos distintos que esta capa no permite distinguir con certeza.
3. **Sin fecha de actualización.** La capa no tiene ningún campo de fecha de carga o última actualización. No se puede afirmar qué tan vigente es el dato — el distrito con 0 predios (Anchihuay) podría reflejar ausencia real o simplemente que esa zona no se ha cargado aún a este servicio público en particular.
4. **La comparación por "ratio" solo es interpretable en un sentido**, como se explicó en la sección 4 — valores altos no son evidencia de cobertura, solo valores bajos (por debajo de 1) lo son.
5. **La capa de "Proyectos Catastrales" no tiene granularidad distrital** — el match con los nombres de zona es por similitud de nombre/ubicación conocida, no una confirmación geométrica de que el polígono del proyecto efectivamente cubre el distrito exacto.
6. **No se intentó ningún cruce con datos de identidad** en este ejercicio — eso es exactamente lo que se planteó en la Parte B de la solicitud formal a MIDAGRI (`Solicitud Formal - MIDAGRI (Catastro Rural - PTRT3).md`), que sigue pendiente de respuesta.

## 7. Qué cambia (y qué no) en el mapa de cobertura IP/IV

Esto **no** mueve IP1 de "Parcial" a "Fuerte" — el vacío central (vínculo a socio/parcela individual) sigue sin resolverse con fuentes públicas, y sigue dependiendo de la Parte B de la solicitud a MIDAGRI o de Instrumento 2. Lo que sí aporta, de forma verificada y no inventada, es:

- Una primera señal territorial objetiva de **dónde** el atraso catastral es más severo (Soritor, Bellavista, Anchihuay) — útil para priorizar, no para puntuar.
- Evidencia de que el atraso más documentado coincide con la zona de mayor peso exportador de la muestra (San Martín/Valle Grande), lo que refuerza — con un dato nuevo e independiente — la misma lectura de riesgo que el informe principal ya hacía sobre esa organización por otras vías (triangulación de Aduanas, Registro Sanitario).
- Una ruta ya probada y reproducible (`consulta_catastro_rural_25_orgs.py`) para repetir este chequeo si se agregan más organizaciones a la muestra, o si MIDAGRI actualiza la capa.
