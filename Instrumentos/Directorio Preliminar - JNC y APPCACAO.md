# Directorio Preliminar — JNC, APPCACAO y otras fuentes federativas/institucionales

**Actualización 2026-09-16 (segunda pasada):** además de JNC y APPCACAO, se mapearon otras 4 fuentes reales que amplían o cruzan el marco muestral. La más importante es el **Directorio Nacional de Cooperativas de PRODUCE** — es literalmente la fuente que nombra la metodología del proyecto madre ("encuesta PRODUCE/CENACOOP"), y tiene una categoría específica "COOPERATIVAS AGRARIAS CAFETALERAS".


**Qué es esto:** avance de la Tarea C1/C2 de la Checklist (`Checklist - Correccion de Encuesta y Aplicacion de Instrumento 2.md`). Es información pública recogida por búsqueda web el 2026-09-16 — **no es el directorio oficial completo** de ninguna de las dos instituciones. Ambas fuentes tienen limitaciones reales documentadas abajo. Sirve para arrancar la construcción del marco muestral (Metodología del ISA, §1), no para cerrarlo.

---

## 1. Junta Nacional del Café (JNC) — café

**Estado real:** la JNC agrupa **56–62 organizaciones cafetaleras** (el número varía según la fuente/fecha consultada — 56 en una nota, 62 en otra, probablemente por afiliaciones recientes) entre cooperativas y asociaciones, con más de 70,000 familias asociadas en 14 zonas cafetaleras. **El sitio oficial (`juntadelcafe.org.pe`) devolvió error de servidor (HTTP 500) en todas las páginas internas que se intentó consultar** (Nosotros, Acción de Filiales, Organización de Filiales) — no es un problema de acceso nuestro, el sitio parece tener una falla real en esas rutas al momento de la consulta. Solo la portada y algunas páginas de noticias/PDF respondieron en el buscador, no en fetch directo.

**Organizaciones confirmadas por nombre (vía snippets de búsqueda, no vía el sitio directamente):**

| Organización | Región/sede (si se identificó) |
|---|---|
| COCLA (fundadora) | Cusco |
| CECOVASA (fundadora) | Puno |
| CAFÉ PERÚ (fundadora) | — |
| VRAQUS (fundadora) | VRAEM |
| CEOACNOR (fundadora) | — |
| CENFROCAFE | Jaén, Cajamarca |
| Aproselva | Chanchamayo, Junín |
| Unicafec | San Ignacio, Cajamarca |
| Cooperativa Agraria Cafetalera ACPC | Pichanaki, Chanchamayo, Junín |
| Coopbam Ltda. | Rioja, San Martín |
| La Florida | — |
| Bagua Grande | Amazonas |
| Cepicafé | Piura |
| San Juan del Oro | San Martín/Puno (zona VRAEM-sur) |
| Valle del Río Apurímac | VRAEM |
| San Jorge | — |
| Café Montaña (asociación) | — |
| Asociación de Productores de Rodríguez de Mendoza | Amazonas |

**Filiales regionales operativas conocidas:** Filial Cajamarca, Filial Selva Central, Filial San Martín, Filial Cusco — esto sugiere que el universo real está concentrado en esas 4 macro-zonas más VRAEM/Puno, coherente con los estratos de Territorio ya definidos en la Metodología §1.2.

**Cobertura de esta lista frente al universo declarado:** ~18 de ~56-62 organizaciones (≈30%). **Insuficiente para construir la cuota real** — falta la mayoría.

---

## 2. APPCACAO — cacao

**Estado real:** APPCACAO declara **25+ cooperativas, 30,000+ productores, en 10+ departamentos**. El sitio (`appcacao.org`) **no tiene una página de directorio único** — la información de miembros está repartida en páginas individuales por cooperativa (ej. `/acopagro/`, `/approcap/`) enlazadas desde una página de "Explorar los Orígenes", que sí se pudo consultar completa.

**Organizaciones listadas en "Explorar los Orígenes" (`appcacao.org/explorar-los-origenes/`), agrupadas por macro-región tal como las presenta la propia APPCACAO:**

| Macro-región (según APPCACAO) | Organizaciones |
|---|---|
| Piura y Tumbes | Cacao Tumbes, Norandino, APPROCAP |
| Amazonas y Cajamarca | CEPROAA, APROCAM, Cacao Fronteras |
| San Martín | ACOPAGRO, Choba Choba, Oro Verde, Cacao Aroma, ASPROC, Tocache |
| Huánuco | Naranjillo, Divisoria, Cacao Alto Huallaga |
| Ucayali y Pasco | Palcazú, San Alejandro, Campos Verdes |
| Junín y Lima | Pangoa, Satipo, Café y Cacao Perú |
| Ayacucho, Cusco y Puno | El Quinacho, CACVRA, Alto Urubamba, San Gabán |

**Total: 24 organizaciones nombradas**, cubriendo prácticamente todas las macro-regiones cacaoteras del país — esta lista es más completa proporcionalmente que la de JNC (~24 de ~25+ declaradas, ≈95%), aunque APPCACAO marca varias como "próximamente" en su plataforma de trazabilidad, lo que no significa que no sean asociadas, solo que su ficha de trazabilidad individual no está publicada todavía.

**Cruce con la Metodología (§1.2, Territorio):** esta lista ya viene pre-agrupada por macro-región de forma muy similar a los estratos Norte/Centro/Sur definidos en la Metodología — usar directamente esta agrupación de APPCACAO como base del estrato Territorio para cacao, en vez de reconstruirlo desde cero.

---

## 3. Otras fuentes federativas/institucionales mapeadas (2026-09-16)

### 3.1 PRODUCE — Directorio Nacional de Cooperativas *(la fuente más importante de esta segunda pasada)*

**Qué es:** el registro oficial que sustenta el propio CENACOOP (Censo Nacional de Cooperativas 2017: 1,245 cooperativas a nivel nacional, de las cuales **6.1% son cooperativas agrarias cafetaleras** — ≈76 organizaciones — y otro 3.2% agroindustriales y 1.9% agropecuarias, que pueden incluir cacao). Es exactamente la fuente que la metodología del proyecto madre nombra ("encuesta PRODUCE/CENACOOP adaptada") — más autorizada que JNC/APPCACAO para efectos de marco muestral, aunque menos rica en detalle sectorial específico de café/cacao.

**Herramienta real, filtrable:** `http://directoriocoop.produce.gob.pe/directorio-cooperativa.php` — permite filtrar por región (24 regiones), actividad económica y **tipo de cooperativa**, con "COOPERATIVAS AGRARIAS CAFETALERAS" como categoría propia. Muestra RUC, razón social, dirección, ubicación, teléfono y correo por cooperativa.

**Limitación de esta consulta:** es un formulario dinámico (selects + botón de búsqueda), no una página estática — no se pudo extraer la lista de resultados filtrados con las herramientas de esta sesión. **Requiere consultarlo interactivamente** (navegador) o solicitar el export a PRODUCE directamente. Es la gestión de mayor prioridad para completar C1/C2 con una fuente oficial y no solo con lo que cada gremio publica de sí mismo.

### 3.2 MIDAGRI — Registro Nacional de Cooperativas Agrarias (RNCA)

Registro específico para cooperativas **agrarias** (no todas las cooperativas de PRODUCE lo son) — la primera inscrita fue Cooperativa Agraria Norandino Ltda. (Piura). MIDAGRI reportó más de 10,000 socios en cooperativas agrarias inscritas ante esa entidad. Complementa al Directorio PRODUCE con una mirada específicamente agraria — ya estaba contemplado como fuente en la Metodología §1.1 (MIDAGRI/DRA), esto lo hace más concreto: el RNCA es el instrumento exacto a pedir, no solo "MIDAGRI" en general.

### 3.3 Central Café y Cacao (`centralcafeycacao.org.pe`) — federación independiente, no visible en búsquedas de JNC/APPCACAO

Red de **9,000 familias productoras** que coordina **10 cooperativas** de zonas centro, norte y sur, operando de forma **independiente** de JNC y APPCACAO (sin mención de afiliación cruzada en su sitio):

| Cooperativa |
|---|
| La Florida |
| Perené |
| Satipo |
| Tahuantinsuyo |
| Alto El Palomar |
| Pangoa |
| Cacvra |
| El Quinacho |
| Incahuasi |
| San Juan del Oro |

Nótese que **Pangoa, Cacvra, El Quinacho y San Juan del Oro ya aparecían** en las listas de JNC/APPCACAO — es esperable que una misma cooperativa pertenezca a más de una federación (JNC + Central Café y Cacao, por ejemplo). Al construir el marco final, **deduplicar por RUC/razón social**, no asumir que cada fuente aporta organizaciones 100% nuevas.

### 3.4 Cámara Peruana del Café y Cacao (`camcafeperu.com.pe`) — fuente del lado comprador, no de cooperativas

Sus "asociados" (AICASA, ANDES TRADE, CAMSA-ECOM, COINCA, Comercio Amazonía, Exportadora Romex, N.B. Tealdo, OFI, Verdum, Volcafe, Café Parish) son **empresas comercializadoras/exportadoras**, no cooperativas productoras — varias son literalmente los "compradores que exportan a la UE" que el Bloque 0 y D7 del Instrumento 2 preguntan. **No sirve como fuente de marco muestral de cooperativas**, pero sí como insumo cruzado para validar las respuestas de Bloque 0 ("¿quién es el comprador que sí exporta a la UE?") y de D7 (exigencias del comprador) — vale la pena guardar esta lista para ese propósito, no para C1/C2.

### 3.5 Bases de certificadoras (Fairtrade/FLOCERT, Rainforest Alliance) — fuente de cruce, no primaria

Fairtrade International/FLOCERT mantiene una base pública de organizaciones productoras certificadas, consultable por país. Ya se confirmaron por búsqueda: **CECOVASA** (triple certificada Fairtrade/orgánico/Rainforest Alliance), **Norandino** (90 organizaciones de base, ~4,790 productores), **CACVRA** (~1,600 socios), **Cooperativa Agroindustrial Tocache Ltda.** (cacao, 109 familias en un proyecto puntual). Útil como **variable auxiliar de calibración** (Metodología §3) — permite cruzar cuántas de las organizaciones muestreadas tienen certificación voluntaria vigente, dato que además retroalimenta directamente el Bloque 0 y la bandera D10.

---

## 4. Qué falta y cómo cerrarlo (actualiza Tarea C1/C2 de la Checklist)

- [ ] **JNC:** el sitio oficial no es utilizable por fetch automatizado en este momento (error 500 persistente en subpáginas). Recomendación: **solicitar el directorio directamente por contacto institucional** (`juntadelcafe.org.pe/contacto/`), no seguir intentando extraerlo del sitio. Puedo redactar esa solicitud formal si se necesita.
- [ ] **APPCACAO:** no tiene directorio único ni siquiera cuando el sitio funciona bien — su información está repartida por diseño. Recomendación: la lista de 24 organizaciones de este documento es un punto de partida razonable (95% de cobertura estimada), pero conviene **confirmar por contacto directo** (`appcacao.org`, sección de contacto) si hay cooperativas asociadas no listadas en "Explorar los Orígenes" — esa página parece ser una vitrina de trazabilidad, no necesariamente el padrón completo de afiliados.
- [ ] Ninguna de las dos fuentes públicas trae **N° de socios ni hectáreas** por organización — dato necesario para el estrato Tamaño de la Metodología §1.2. Eso solo se obtiene por contacto directo o en el propio Bloque 0 del Instrumento 2 al aplicar la encuesta.
- [ ] Complementar ambas listas con el padrón de **MIDAGRI/DRA regionales** (Tarea C3) para las organizaciones no afiliadas a ningún gremio — ninguna de las dos listas de arriba pretende ser exhaustiva del universo total café/cacao, solo del universo *afiliado a gremio*.
- [ ] **(nuevo) Consultar interactivamente el Directorio Nacional de Cooperativas de PRODUCE** (`http://directoriocoop.produce.gob.pe/directorio-cooperativa.php`, filtro "COOPERATIVAS AGRARIAS CAFETALERAS") — es un formulario dinámico, no se pudo extraer por fetch automatizado en esta sesión; requiere navegador o solicitud de export directa a PRODUCE. Es la fuente de mayor autoridad (es la que la metodología del proyecto madre nombra explícitamente) y debería tratarse como prioritaria sobre JNC/APPCACAO para el marco final, no solo como complemento.
- [ ] **(nuevo) Solicitar el RNCA (Registro Nacional de Cooperativas Agrarias) a MIDAGRI** — más específico que "MIDAGRI/DRA regionales" en general; es el registro exacto donde se inscriben las cooperativas agrarias, incluye Norandino como primera inscrita.
- [ ] **(nuevo) Deduplicar por RUC/razón social al consolidar todas las fuentes** — se confirmó que una misma cooperativa aparece en más de una federación (ej. Pangoa, Cacvra, El Quinacho y San Juan del Oro aparecen tanto en listas de JNC/APPCACAO como en Central Café y Cacao). Sumar los conteos de cada fuente sin deduplicar sobreestimaría el universo real.

**Actualización de estado de C1/C2:** de "sin iniciar" a **"avance parcial vía fuentes públicas (JNC, APPCACAO, Central Café y Cacao) — falta consultar interactivamente el Directorio PRODUCE (fuente prioritaria), pedir el RNCA a MIDAGRI, deduplicar, y obtener tamaño (socios/hectáreas) por organización"**.
