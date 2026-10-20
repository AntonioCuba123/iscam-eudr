1: README — Base de organizaciones agrarias por RUC (SUNAT · OECE/RNP · MIDAGRI-PPA · Exportaciones FOB)
2: Libro armado el 22/09/2026 a partir de los archivos .txt entregados y de la documentación fuentes_urls.md (Ricardo, 22/09/2026). Los conteos de las tablas son fórmulas que leen cada pestaña.
4: 1. CONTENIDO DEL LIBRO Y DE CADA PESTAÑA
5: Pestaña | Contenido | Archivo / fuente de origen | Filas de datos | RUCs únicos | Rango
6: README | Esta hoja: documentación del libro, metodología, tratamiento y diccionario de atributos. | — | —
7: b1 | Hoja preexistente del libro (no modificada). 6 organizaciones con datos de intervención 2025: producto, sede/ubigeo, certificados, beneficiarios, ventas 2018-2025 y comprobantes 2025. | Fuente interna del libro (no documentada en fuentes_urls.md) | 6 | 6 | b1!A1:AE7
8: b2 | Hoja preexistente del libro (no modificada). Histórico por organización 2018-2025: intervención, beneficiarios por sexo, asistencia técnica/talleres, ventas nacionales y de exportación, comprobantes. Fila 1 = numeración de columnas; encabezados en fila 2. | Fuente interna del libro (no documentada en fuentes_urls.md) | 673 | 589 | b2!A1:DK680
9: b3 | Hoja preexistente del libro (no modificada). Ficha de 25 organizaciones cafetaleras con PAC: socios, hectáreas, producción y cosecha 2026, altitud, variedades, certificaciones, calidad, avance EUDR y contactos. | Fuente interna del libro (no documentada en fuentes_urls.md) | 25 | 25 | b3!A1:AW26
10: RUC_ID | Lista maestra RUC + razón social (596 RUCs). Le falta 20404057805 respecto de rucs.txt. | Hoja preexistente del libro / rucs.txt (universo de consulta) | 596 | 596 | RUC_ID!A1:B597
11: RUC_CONSULTAMASIVA | Ficha SUNAT completa por RUC (24 campos): contribuyente, estado/condición, fechas, ubicación, dirección, comercio exterior, CIIU, regímenes. | 9 archivos RM20260919*.txt — Consulta RUC múltiple SUNAT (19/09/2026) | 597 | 597 | RUC_CONSULTAMASIVA!A1:X598
12: RUC_OECE | Ficha de proveedor OECE por RUC: datos SUNAT resumidos + teléfono, email y código de registro RNP. | ruc-oece-ficha.txt (consulta 20/09/2026) | 597 | 597 | RUC_OECE!A1:L598
13: RUC_OECE_PERSONAS | Órganos de administración, representantes legales y socios por RUC (DNI, nombre, cargo, fecha de ingreso). Contiene datos personales. | ruc-oece-personas.txt (consulta 20/09/2026) | 815 | 139 | RUC_OECE_PERSONAS!A1:I816
14: RNP | Subconjunto de RUC_OECE: solo proveedores inscritos en el Registro Nacional de Proveedores (con código de registro). | ruc-oece-ficha-inscritos-rnp.txt (consulta 20/09/2026) | 155 | 155 | RNP!A1:L156
15: RUC_PPA | Inscripción en el Padrón de Productores Agrarios (MIDAGRI) y nombre registrado. | ruc-padron-ppa.txt (consulta 20/09/2026) | 597 | 597 | RUC_PPA!A1:D598
16: RUC_FOB | Detalle de exportaciones: una fila por RUC-anio-mes-aduana-agente-pais con valor FOB (USD). Ene-2025 a may-2026 (fuente original, 597 RUC) mas 2024 completo para 33 RUC que ya exportaban en 2025-2026 (fuente historica 2010-2025, ver CTL_FUENTE_CONSULTA fila 8). El resto del universo no tiene 2024. | ruc-exportaciones-fob.txt (consulta 19/09/2026) mas SUNAT exportaciones 2010-2025.xlsx (archivo aportado por el usuario, cargado 17/09/2026, agregado el 23/09/2026) | 958 | 66 | RUC_FOB!A1:K681
17: RUC_FOB (2) | Resumen de RUC_FOB agrupado por RUC (una fila por RUC), calculado con fórmulas; fila 67 = totales y fila 68 = control contra el detalle. Estas dos filas NO son RUCs: están resaltadas en amarillo con nota en A67; cualquier suma de columna (p.ej. fob_total_usd) debe acotarse a filas 2:65, nunca a la columna completa ni a un rango que incluya 66:68, o se duplica el total. | Derivada de RUC_FOB | 64 | 64 | RUC_FOB (2)'!A1:M68
20: 2. METODOLOGÍA DE ACCESO A LOS DATASETS
21: Universo: rucs.txt (597 RUCs únicos; fuentes_urls.md indica 598). Cada fuente se consultó RUC por RUC sobre ese universo y el resultado se exportó a .txt (campo fecha_consulta en cada fila). Las URLs son las documentadas en fuentes_urls.md como fuentes oficiales para reconstruir o ampliar cada dato.
22: Dataset (pestaña) | Institución / sistema | Forma de acceso | Fecha de consulta | Fuentes oficiales / endpoints para reconstruir o ampliar | Limitaciones
23: rucs.txt (RUC_ID) | Input interno | Lista entregada: define el universo de cooperativas y asociaciones agrarias a cruzar | — | No es un dataset público; es la base de partida | Solo contiene el número de RUC
24: RM20260919*.txt (RUC_CONSULTAMASIVA) | SUNAT — Consulta RUC | Consulta múltiple de RUC en SUNAT, en lotes de hasta 100 RUCs; descarga en .txt separado por '|' (9 archivos) | 19/09/2026 | https://e.sunat.gob.pe/ (formulario web) · APIs de terceros: https://openruc.com/api/ruc/{ruc}, https://docs.apisunat.pe/consulta/sunat-ruc, https://docs.apiperu.dev/referencia/consultar-ruc/ | Formulario con CAPTCHA; no hay API oficial de descarga masiva
25: ruc-oece-ficha.txt (RUC_OECE) | OECE — ficha de proveedor | Consulta de la ficha OECE/SEACE por RUC; exportación a .txt tabulado | 20/09/2026 | https://www.gob.pe/oece · https://contratacionesabiertas.oece.gob.pe · APIs RUC: openruc.com, apisunat, apiperu, json.pe | Teléfono/email/código solo cuando el RUC figura como proveedor
26: ruc-oece-personas.txt (RUC_OECE_PERSONAS) | OECE / RNP — directivos y representantes | Consulta de la ficha extendida del proveedor (órganos de administración, representantes, socios) por RUC | 20/09/2026 | https://contratacionesabiertas.oece.gob.pe (OCDS) · https://www.gob.pe/institucion/oece/tema/transparencia-y-datos-abiertos · POST https://api.croma.run/pe/oece/processes-search/v1 · https://apify.com/publicmoney/peru-oece-scraper | No existe endpoint OCDS público para la estructura de gobierno; datos personales (DNI)
27: ruc-oece-ficha-inscritos-rnp.txt (RNP) | RNP — Registro Nacional de Proveedores | Filtro de la ficha OECE a los RUCs con inscripción RNP vigente (código de registro) | 20/09/2026 | https://www.rnp.gob.pe/Constancia/RNP_Constancia/ConsultaRuc.asp · https://www.rnp.gob.pe/Constancia/RNP_Constancia/ConsultaRucEyC.asp · https://www.gob.pe/7832-acceder-a-tramites-en-linea-del-registro-nacional-de-proveedores-rnp | Sin API REST pública; consulta una por una con CAPTCHA
28: ruc-padron-ppa.txt (RUC_PPA) | MIDAGRI — Padrón de Productores Agrarios | Consulta de inscripción en el PPA por RUC | 20/09/2026 | https://ppa.midagri.gob.pe · https://ppa.midagri.gob.pe/media/attachments/2022/02/18/ft_ficha-tcnica.pdf · https://www.gob.pe/29665-consultar-si-estas-registrado-en-el-padron-de-productores-agrarios-ppa | Sin API bulk; consulta individual; el empadronamiento es presencial
29: ruc-exportaciones-fob.txt (RUC_FOB) | SUNAT — Aduanas (exportaciones) | Consulta de declaraciones de exportación por RUC, agregadas por año, mes, aduana, agente y país | 19/09/2026 | https://www.sunat.gob.pe/estadisticasestudios/exportaciones.html · https://www.sunat.gob.pe/estad-comExt/modelo_web/informes/anuarios/2024/cdro_33.xlsx · https://ww3.sunat.gob.pe/servlet/HRGDecExp?opcion=aduanaexp&codr=50 · http://www.aduanet.gob.pe/cl-ad-itestadispartida/resumenPPaisS01Alias · https://datosabiertos.gob.pe | No hay API pública por RUC; los anuarios solo dan totales por aduana/país
30: ruc-contratacion-estatal.txt (RUC_CONTRATACION) | OECE / Open Contracting Partnership (mirror OCDS) | Descarga bulk anual de OCDS republicada por Open Contracting Partnership; filtrada por los 597 RUC del universo (script oece_contrataciones_por_ruc.py) | 23/09/2026 | https://data.open-contracting.org/en/publication/135 (bulk anual) · https://contratacionesabiertas.oece.gob.pe (endpoint search?supplier= no filtra por proveedor) | Solo 10 de 597 RUC tienen procesos/contratos; el endpoint de búsqueda de OECE no filtra por proveedor, se usó el bulk anual como vía verificada
33: 2.1 Endpoints públicos directos e indirectos
34: Directo = portal, servicio o archivo oficial de la entidad que produce el dato (SUNAT, OECE, RNP, MIDAGRI, PNDA). Indirecto = servicio de terceros que replica, indexa o consulta la fuente oficial (OpenRUC, APISUNAT, APIperu, json.pe, Croma, Apify). Fuente: fuentes_urls.md.
35: Dataset (pestañas) | Tipo | Recurso | Endpoint / URL | Método y acceso | Formato / notas
36: RUC_CONSULTAMASIVA · RUC_OECE · RNP (ficha RUC) | Directo | SUNAT — Consulta RUC (web oficial) | https://e.sunat.gob.pe/ | Web · formulario con CAPTCHA · consulta individual y múltiple | HTML / descarga .txt (consulta múltiple)
37: RUC_CONSULTAMASIVA · RUC_OECE · RNP (ficha RUC) | Indirecto | OpenRUC — API RUC SUNAT (Latinfo) | GET https://openruc.com/api/ruc/{ruc} | API REST GET · sin API key · gratis | JSON: razón social, estado, condición, dirección
38: RUC_CONSULTAMASIVA · RUC_OECE · RNP (ficha RUC) | Indirecto | APISUNAT — Consulta RUC | GET https://dev.apisunat.pe/api/v1/business/ruc/{RUC}  (doc: https://docs.apisunat.pe/consulta/sunat-ruc) | API REST GET · requiere API key | JSON
39: RUC_CONSULTAMASIVA · RUC_OECE · RNP (ficha RUC) | Indirecto | APIperu — Consultar RUC | POST https://api.apiperu.dev/ruc  (doc: https://docs.apiperu.dev/referencia/consultar-ruc/) | API REST POST · token · plan gratuito | JSON (ficha RUC completa)
40: RUC_CONSULTAMASIVA · RUC_OECE · RNP (ficha RUC) | Indirecto | json.pe — Consulta RUC | POST https://api.json.pe/api/ruc  (doc: https://docs.json.pe/api-consulta/endpoint/ruc) | API REST POST · requiere token | JSON
41: RUC_OECE · RUC_OECE_PERSONAS | Directo | OECE — Portal de Contrataciones Abiertas (OCDS) | https://contratacionesabiertas.oece.gob.pe | Descarga masiva (bulk) · sin autenticación · actualización diaria | JSON / CSV / Excel (OCDS), procesos 2003–presente
42: RUC_OECE · RUC_OECE_PERSONAS | Directo | OECE — Transparencia y datos abiertos | https://www.gob.pe/institucion/oece/tema/transparencia-y-datos-abiertos | Web · enlaces a estadísticas, BI y observatorio de precios | HTML / descargas
43: RUC_OECE · RUC_OECE_PERSONAS · RNP | Directo | OECE — SEACE / Registro de proveedores | https://www.gob.pe/oece | Web · consulta por RUC (ficha de proveedor con directivos) | HTML · sin bulk
44: RUC_OECE · RUC_OECE_PERSONAS | Indirecto | Croma API — OECE Contrataciones | POST https://api.croma.run/pe/oece/processes-search/v1 | API REST POST · búsqueda por RUC proveedor, entidad, texto, categoría, fechas | JSON (dataset indexado)
45: RUC_OECE · RUC_OECE_PERSONAS | Indirecto | Apify — Peru OECE Tender Scraper | https://apify.com/publicmoney/peru-oece-scraper | Actor/scraper sobre contratacionesabiertas.oece.gob.pe · cuenta Apify | JSON / CSV / Excel
46: RNP | Directo | RNP — Consulta RUC | https://www.rnp.gob.pe/Constancia/RNP_Constancia/ConsultaRuc.asp | Web · formulario con CAPTCHA · uno por uno | HTML (verificación de inscripción)
47: RNP | Directo | RNP — Consulta RUC y Condiciones | https://www.rnp.gob.pe/Constancia/RNP_Constancia/ConsultaRucEyC.asp | Web · formulario con CAPTCHA | HTML (constancia de inscripción)
48: RNP | Directo | RNP — Portal de proveedores | https://www.rnp.gob.pe | Web · consulta individual con CAPTCHA | HTML
49: RNP | Directo | RNP — Trámites en línea (gob.pe) | https://www.gob.pe/7832-acceder-a-tramites-en-linea-del-registro-nacional-de-proveedores-rnp | Web · acceso a trámites del RNP | HTML
50: RUC_PPA | Directo | MIDAGRI — Portal PPA | https://ppa.midagri.gob.pe | Web · consulta individual | HTML · sin API bulk
51: RUC_PPA | Directo | PPA — Ficha técnica | https://ppa.midagri.gob.pe/media/attachments/2022/02/18/ft_ficha-tcnica.pdf | Descarga directa | PDF (metodología y estructura del padrón)
52: RUC_PPA | Directo | PPA — Consulta de inscripción (gob.pe) | https://www.gob.pe/29665-consultar-si-estas-registrado-en-el-padron-de-productores-agrarios-ppa | Web · consulta individual por DNI/RUC | HTML
53: RUC_PPA | Directo | MIDAGRI — Padrones públicos | https://midagri.gob.pe | Web · enlaces a padrones y estadísticas | HTML
54: RUC_FOB · RUC_FOB (2) | Directo | SUNAT — Estadísticas de exportaciones | https://www.sunat.gob.pe/estadisticasestudios/exportaciones.html | Descarga directa · 14 cuadros G1–G14 (sector, país, aduanas) | XLS · agregado, no por RUC
55: RUC_FOB · RUC_FOB (2) | Directo | SUNAT — Anuario: Exportaciones FOB por aduanas (Cuadro 33) | https://www.sunat.gob.pe/estad-comExt/modelo_web/informes/anuarios/2024/cdro_33.xlsx | Descarga directa del archivo | XLSX · 2023–2024 por aduana
56: RUC_FOB · RUC_FOB (2) | Directo | SUNAT — Consulta de exportaciones (servlet) | https://ww3.sunat.gob.pe/servlet/HRGDecExp?opcion=aduanaexp&codr=50 | Web · formulario por aduana, partida y fechas | HTML
57: RUC_FOB · RUC_FOB (2) | Directo | SUNAT Aduanet — Acumulado por subpartida y país | http://www.aduanet.gob.pe/cl-ad-itestadispartida/resumenPPaisS01Alias | Web · formulario por subpartida nacional y país de destino | HTML · incluye valor FOB
58: RUC_FOB · RUC_FOB (2) | Directo | Plataforma Nacional de Datos Abiertos (PNDA) | https://datosabiertos.gob.pe | Portal de datos abiertos · búsqueda de datasets de exportaciones (si están publicados) | CSV / XLSX según dataset
59: RUC_CONTRATACION · HECHO_CONTRATACION_ESTATAL | Directo (bulk, republicado por Open Contracting Partnership) | OCDS bulk anual (mirror OCP de OECE Contrataciones Abiertas) | https://data.open-contracting.org/en/publication/135/download?name={año}.jsonl.gz | Descarga directa por año (jsonl.gz) · sin autenticación · filtrado por RUC en script propio | JSONL comprimido · OCDS; el endpoint search?supplier= de OECE no filtra por proveedor (2.75M+ resultados)
61: 3. TRATAMIENTO DE LOS DATOS
62: Paso | Pestaña(s) | Tratamiento aplicado
63: 1 | RUC_ID / rucs.txt | Validación del universo: rucs.txt tiene 597 RUCs únicos de 11 dígitos, sin duplicados. RUC_ID tiene 596; el único faltante es 20404057805 (COOPERATIVA AGRARIA ACOPAGRO LTDA).
64: 2 | RUC_CONSULTAMASIVA | Unión de los 9 archivos SUNAT (698 registros). Se eliminaron 101 duplicados idénticos entre archivos → 597 RUCs. Se normalizó la codificación (UTF-8 / Latin-1), se quitaron comillas externas y espacios sobrantes. Orden = el de los archivos.
65: 3 | RUC_OECE | Carga de 597 RUCs ordenados por número. Contraste con SUNAT: 6 diferencias (5 razones sociales que en SUNAT vienen con comillas truncadas y 1 distrito truncado en OECE); se conservó el valor del archivo OECE. Campos sin dato (teléfono, email, código) quedan en blanco.
66: 4 | RNP | Se verificó que el archivo de inscritos RNP es idéntico, fila por fila, a los 155 RUCs de RUC_OECE con código de registro.
67: 5 | RUC_OECE_PERSONAS | Carga de 815 filas (139 RUCs) sin deduplicar: una misma persona puede figurar con varios roles o cargos. Se conservan DNI con ceros a la izquierda. Contiene datos personales: uso interno.
68: 6 | RUC_PPA | Carga de 597 RUCs; los 597 figuran como registrados (true) y nombre_ppa coincide con la razón social de RUC_OECE.
69: 7 | RUC_FOB | Carga de 680 operaciones (64 RUCs). mes y fob_usd como números (fob_usd con formato #,##0.00); RUC, año y códigos de aduana/agente/país como texto para conservar ceros a la izquierda.
70: 8 | RUC_FOB (2) | Agrupación por RUC con fórmulas sobre RUC_FOB (UNIQUE, SUMIFS, COUNTIFS, FILTER, TEXTJOIN): n° de operaciones, FOB total y por año, primer/último período, países, aduanas y agentes. Control (fila 68) = 0 contra el detalle.
71: 9 | Todas las cargadas | Controles de calidad: suma de verificación de cada bloque contra el archivo original, conteo de filas y RUCs únicos, revisión de celdas vacías. RUC guardado como texto (11 dígitos). Formato común: encabezado en negrita con fondo azul claro, fila 1 inmovilizada y comentario de fuente en A1.
72: 10 | b1, b2, b3 | Hojas preexistentes del libro: no fueron modificadas; solo se documentan aquí.
73: 11 | RUC_CONTRATACION | Carga del archivo subido ruc-contratacion-estatal.txt (53 filas, 10 RUC de los 597). RUC y entidad_ruc guardados como texto. Se construyó HECHO_CONTRATACION_ESTATAL con fórmulas FILTER sobre esta pestaña y se agregó la fila 8 en CTL_FUENTE_CONSULTA.
75: 4. ATRIBUTOS ADICIONALES AL RUC POR PESTAÑA
76: Pestaña | N° | Atributo (columna) | Descripción | Tipo
77: RUC_ID | 1 | RAZON SOCIAL | Razón social de la organización | Texto
78: RUC_CONSULTAMASIVA | 1 | Nombre ó RazonSocial | Razón social registrada en SUNAT | Texto
79: RUC_CONSULTAMASIVA | 2 | Tipo de Contribuyente | Tipo (asociación, cooperativa, comunidad, S.A.C., etc.) | Texto
80: RUC_CONSULTAMASIVA | 3 | Profesion u Oficio | Profesión u oficio (aplica a personas naturales) | Texto
81: RUC_CONSULTAMASIVA | 4 | Nombre Comercial | Nombre comercial declarado | Texto
82: RUC_CONSULTAMASIVA | 5 | Condicion del Contribuyente | HABIDO / NO HABIDO | Texto
83: RUC_CONSULTAMASIVA | 6 | Estado del Contribuyente | ACTIVO, BAJA DE OFICIO, SUSPENSIÓN TEMPORAL, etc. | Texto
84: RUC_CONSULTAMASIVA | 7 | Fecha de Inscripcion | Fecha de inscripción en el RUC (dd/mm/aaaa) | Fecha (texto)
85: RUC_CONSULTAMASIVA | 8 | Fecha de Inicio de Actividades | Fecha de inicio de actividades (dd/mm/aaaa) | Fecha (texto)
86: RUC_CONSULTAMASIVA | 9 | Departamento | Departamento del domicilio fiscal | Texto
87: RUC_CONSULTAMASIVA | 10 | Provincia | Provincia del domicilio fiscal | Texto
88: RUC_CONSULTAMASIVA | 11 | Distrito | Distrito del domicilio fiscal | Texto
89: RUC_CONSULTAMASIVA | 12 | Direccion | Dirección del domicilio fiscal | Texto
90: RUC_CONSULTAMASIVA | 13 | Telefono | Teléfono (sin dato en este universo: '-') | Texto
91: RUC_CONSULTAMASIVA | 14 | Fax | Fax (sin dato: '-') | Texto
92: RUC_CONSULTAMASIVA | 15 | Actividad de Comercio Exterior | EXPORTADOR, IMPORTADOR, IMPORTADOR/EXPORTADOR o SIN ACTIVIDAD | Texto
93: RUC_CONSULTAMASIVA | 16 | Principal- CIIU | Actividad económica principal (CIIU) | Texto
94: RUC_CONSULTAMASIVA | 17 | Secundario 1- CIIU | Actividad económica secundaria 1 | Texto
95: RUC_CONSULTAMASIVA | 18 | Secundario 2- CIIU | Actividad económica secundaria 2 | Texto
96: RUC_CONSULTAMASIVA | 19 | Afecto Nuevo RUS | Afecto al Nuevo RUS (SI/NO) | Texto
97: RUC_CONSULTAMASIVA | 20 | Buen Contribuyente | Incorporación al régimen de Buenos Contribuyentes | Texto
98: RUC_CONSULTAMASIVA | 21 | Agente de Retencion | Condición de agente de retención de IGV | Texto
99: RUC_CONSULTAMASIVA | 22 | Agente de Percepcion VtaInt | Agente de percepción – venta interna | Texto
100: RUC_CONSULTAMASIVA | 23 | Agente de Percepcion ComLiq | Agente de percepción – combustibles líquidos | Texto
101: RUC_OECE | 1 | razon_social | Razón social | Texto
102: RUC_OECE | 2 | tipo_empresa | Tipo de contribuyente/empresa | Texto
103: RUC_OECE | 3 | estado_sunat | Estado SUNAT | Texto
104: RUC_OECE | 4 | condicion_sunat | Condición SUNAT | Texto
105: RUC_OECE | 5 | departamento | Departamento | Texto
106: RUC_OECE | 6 | provincia | Provincia | Texto
107: RUC_OECE | 7 | distrito | Distrito | Texto
108: RUC_OECE | 8 | telefono | Teléfono de contacto registrado en OECE | Texto
109: RUC_OECE | 9 | email | Correo de contacto registrado en OECE | Texto
110: RUC_OECE | 10 | codigo_registro | Código de inscripción RNP (S… / B…); vacío = no inscrito | Texto
111: RUC_OECE | 11 | fecha_consulta | Fecha y hora de la consulta (UTC) | Fecha-hora (texto)
112: RUC_OECE_PERSONAS | 1 | rol | ORGANO_ADMINISTRACION, REPRESENTANTE o SOCIO | Texto
113: RUC_OECE_PERSONAS | 2 | source_id | Identificador del registro en la fuente | Texto
114: RUC_OECE_PERSONAS | 3 | dni | Documento de identidad (dato personal) | Texto
115: RUC_OECE_PERSONAS | 4 | nombre | Nombre de la persona (dato personal) | Texto
116: RUC_OECE_PERSONAS | 5 | tipo_organo | Órgano: consejo de administración, consejo directivo, directorio, gerencia, etc. | Texto
117: RUC_OECE_PERSONAS | 6 | cargo | Presidente, vicepresidente, secretario, tesorero, vocal, fiscal, gerente, etc. | Texto
118: RUC_OECE_PERSONAS | 7 | fecha_ingreso | Fecha de ingreso al cargo (aaaa-mm-dd) | Fecha (texto)
119: RUC_OECE_PERSONAS | 8 | fecha_consulta | Fecha y hora de la consulta (UTC) | Fecha-hora (texto)
120: RNP | 1 | razon_social · tipo_empresa · estado_sunat · condicion_sunat · departamento · provincia · distrito · telefono · email · codigo_registro · fecha_consulta | Mismos 11 atributos que RUC_OECE, solo para los 155 inscritos en el RNP | Texto
121: RUC_PPA | 1 | registrado | Inscrito en el Padrón de Productores Agrarios (true/false) | Texto
122: RUC_PPA | 2 | nombre_ppa | Nombre con el que figura en el PPA | Texto
123: RUC_PPA | 3 | fecha_consulta | Fecha y hora de la consulta (UTC) | Fecha-hora (texto)
124: RUC_FOB | 1 | anio | Año de la exportación | Texto
125: RUC_FOB | 2 | mes | Mes (1-12) | Número
126: RUC_FOB | 3 | aduana_codigo | Código de aduana de salida | Texto
127: RUC_FOB | 4 | aduana_nombre | Aduana: Marítima del Callao, Paita, Aérea del Callao | Texto
128: RUC_FOB | 5 | agente_codigo | Código del agente de aduana | Texto
129: RUC_FOB | 6 | agente_nombre | Agente de aduana | Texto
130: RUC_FOB | 7 | pais_codigo | Código ISO del país de destino | Texto
131: RUC_FOB | 8 | pais_nombre | País de destino | Texto
132: RUC_FOB | 9 | fob_usd | Valor FOB exportado (USD) | Número
133: RUC_FOB | 10 | fecha_consulta | Fecha y hora de la consulta (UTC) | Fecha-hora (texto)
134: RUC_FOB (2) | 1 | razon_social | Razón social (traída de RUC_OECE) | Fórmula
135: RUC_FOB (2) | 2 | n_operaciones | N° de filas de exportación del RUC | Fórmula
136: RUC_FOB (2) | 3 | fob_total_usd | FOB total exportado (USD) | Fórmula
137: RUC_FOB (2) | 4 | 2025 | FOB exportado en 2025 (USD) | Fórmula
138: RUC_FOB (2) | 5 | 2026 | FOB exportado en 2026 (USD) | Fórmula
139: RUC_FOB (2) | 6 | primer_periodo | Primer mes con exportación (aaaa-mm) | Fórmula
140: RUC_FOB (2) | 7 | ultimo_periodo | Último mes con exportación (aaaa-mm) | Fórmula
141: RUC_FOB (2) | 8 | n_paises | N° de países de destino | Fórmula
142: RUC_FOB (2) | 9 | paises_destino | Lista de países de destino | Fórmula
143: RUC_FOB (2) | 10 | aduanas | Aduanas utilizadas | Fórmula
144: RUC_FOB (2) | 11 | agentes_aduana | Agentes de aduana utilizados | Fórmula
145: RUC_FOB (2) | 12 | fecha_consulta | Fecha de consulta de la fuente | Fórmula
146: b1 | 1 | 30 columnas | Organización, producto dominante y secundario, sede, ubigeo, departamento/provincia/distrito, tipo de certificado, servicio y años de intervención, beneficiarios 2025 (hombres/mujeres/total), ventas 2018-2025, ventas nacionales/exportación 2025, incremento y diferencia de ventas, comprobantes 2025 (boleta, DJ, factura, guía, liquidación), tipo de organización | Mixto
147: b2 | 1 | ≈106 columnas | Organización, productos, sede, ubigeo y ubicación, años de intervención 2018-2025, servicio, beneficiarios por sexo y año 2018-2025, asistencia técnica y talleres 2020-2025, ventas nacionales/internacionales/totales 2018-2025 con incrementos y diferencias, comprobantes 2023-2025, nombre SUNAT y tipo de organización | Mixto
148: b3 | 1 | 48 columnas | N°, región/provincia/distrito, estado SUNAT, inicio de actividades, año y etapa del PAC, descripción y avance, socios (varones/mujeres), hectáreas, producción y meses de cosecha 2026, disponibilidad de embarque, altitud, variedades, certificaciones (orgánica, comercio justo, otras), calidad 2026, avance EUDR, dirección, correo, celular, web, redes, gerente y representante legal (contactos), registro sanitario, marca y presentación de café tostado | Mixto
149: RUC_CONTRATACION | 15 columnas | ruc, razon_social_ruc | Identificación de la organización contratista | Texto
150: RUC_CONTRATACION | — | ocid, nivel_registro, entidad_ruc, entidad_nombre, objeto, monto, moneda, fecha, estado, metodo_contratacion, rol_en_proceso, fuente, fecha_consulta | Identificador OCDS del proceso/contrato; nivel (proceso o contrato); entidad contratante; objeto y monto (PEN); fecha; estado; método de contratación; rol de la organización (tenderer/supplier) | Mixto
152: 5. ESTRUCTURA DE DATOS PROPUESTA POR RUC (máximo de atributos, priorizando lo más vigente y directo)
153: Modelo con el RUC (11 dígitos, texto) como llave única: una tabla maestra con una fila por RUC (el 'golden record') y tablas satélite para los datos que tienen varias filas por RUC. Cada valor guarda su fuente y fecha, y se elige con reglas de prioridad explícitas.
155: 5.1 Reglas de prioridad para elegir el valor vigente
156: N° | Regla | Aplicación
157: 1 | Fuente directa antes que indirecta | Un valor de SUNAT, OECE, RNP o MIDAGRI prevalece sobre OpenRUC, APISUNAT, APIperu, json.pe, Croma o Apify. Las indirectas solo rellenan vacíos y quedan marcadas como tales.
158: 2 | Entidad dueña del dato | Datos tributarios y de ubicación: SUNAT. Proveedor del Estado, contacto y directivos: OECE/RNP. Productor agrario: MIDAGRI-PPA. Exportaciones: SUNAT-Aduanas. Datos del programa (socios, hectáreas, ventas, beneficiarios): registros internos b1/b2/b3.
159: 3 | Lo más reciente gana | Entre fuentes del mismo nivel se toma la de fecha_consulta o fecha de corte más reciente. Si la fecha es la misma, se aplica la regla 2.
160: 4 | Valor informado antes que vacío | Un valor vacío, '-' o '0' no reemplaza a uno informado. Se registra como 'sin dato' con su fuente.
161: 5 | Trazabilidad por atributo | Cada atributo lleva {atributo}_fuente, {atributo}_tipo_fuente (directa/indirecta) y {atributo}_fecha. El histórico de valores reemplazados se guarda en HIST_ATRIBUTO.
162: 6 | Vigencia de relaciones | En personas y cargos se marca vigente = SI para el último período por RUC, rol y cargo; los anteriores quedan con fecha_fin.
163: 7 | Caducidad y refresco | Estado y condición SUNAT: mensual. RNP y OECE: trimestral o antes de un proceso. PPA: anual. Exportaciones: mensual. Datos del programa: por campaña o año. Se marca desactualizado si se supera el plazo.
164: 8 | Normalización de llaves | RUC como texto de 11 dígitos sin espacios; DNI de 8 dígitos con ceros a la izquierda; ubigeo INEI de 6 dígitos; códigos de aduana, agente, país (ISO-2) y CIIU como texto.
166: 5.2 Tablas del modelo
167: Tabla | Grano (1 fila por…) | Llave | Contenido principal | Fuente directa prioritaria (alternativa) | Pestañas actuales que la alimentan | Pestaña construida
168: DIM_ORGANIZACION (maestra) | RUC | ruc (PK) | Identidad, estado/condición tributaria, ubicación, actividad, contacto, registros (RNP, PPA), ventas totales 2024-2025, indicadores resumidos de exportación, directivos y programa | SUNAT Consulta RUC (OECE / APIs RUC) | RUC_ID, RUC_CONSULTAMASIVA, RUC_OECE, RNP, RUC_PPA, RUC_FOB (2), b1, b2, b3 | Sí — DIM_ORGANIZACION
169: REG_RNP | RUC + código de registro | ruc + codigo_registro | Inscripción de proveedor, capítulo (bienes/servicios), vigencia, constancia | RNP (OECE-SEACE) | RNP, RUC_OECE | Sí — REG_RNP
170: REG_PPA | RUC + registro PPA | ruc | Condición de productor agrario, nombre registrado, fecha de empadronamiento | MIDAGRI-PPA | RUC_PPA | Sí — REG_PPA
171: REL_PERSONA_CARGO | RUC + DNI + rol + cargo + fecha_ingreso | ruc + dni + rol + cargo + fecha_ingreso | Directivos, representantes y socios, con tipo de órgano, fechas y bandera 'vigente' | OECE/RNP (SUNAT representantes legales) | RUC_OECE_PERSONAS | Sí — REL_PERSONA_CARGO
172: DIM_PERSONA | DNI (o documento) | dni (PK) | Nombre normalizado de la persona (dato personal: acceso restringido) | OECE/RNP (RENIEC si se autoriza) | RUC_OECE_PERSONAS | Sí — DIM_PERSONA
173: HECHO_EXPORTACION | RUC + año + mes + aduana + agente + país | ruc + anio + mes + aduana_codigo + agente_codigo + pais_codigo | Valor FOB (USD); ampliable con subpartida, producto y peso neto | SUNAT-Aduanas (Aduanet) | RUC_FOB | Sí — HECHO_EXPORTACION
174: HECHO_CONTRATACION_ESTATAL | RUC + proceso OCDS | ruc + ocid | Procesos y contratos con el Estado: entidad, objeto, monto, fecha, estado | OECE Contrataciones Abiertas OCDS (Croma / Apify) | RUC_CONTRATACION | Sí — HECHO_CONTRATACION_ESTATAL
175: HECHO_PROGRAMA_ANUAL | RUC + año | ruc + anio | Servicio o intervención, beneficiarios por sexo, asistencia técnica, talleres, ventas nacionales y de exportación, comprobantes | Registros internos del programa | b1, b2 | Sí — HECHO_PROGRAMA_ANUAL
176: HECHO_CAMPANIA_PRODUCTIVA | RUC + campaña | ruc + campania | Socios por sexo, hectáreas, producción estimada, meses de cosecha y embarque, altitud, variedades, calidad, EUDR | Registros internos del programa (declarado por la organización) | b3 | Sí — HECHO_CAMPANIA_PRODUCTIVA
177: REL_CERTIFICACION | RUC + tipo + número de certificado | ruc + tipo_cert + nro_cert | Orgánica, Comercio Justo y otras, con fecha de vigencia | Organismo certificador / registro interno | b1, b3 | Sí — REL_CERTIFICACION
178: REL_CONTACTO | RUC + tipo + valor | ruc + tipo_contacto + valor | Teléfonos, correos, web y redes, con fuente y fecha (varios por RUC) | OECE (SUNAT, registro interno) | RUC_OECE, RNP, b3 | Sí — REL_CONTACTO
179: CTL_FUENTE_CONSULTA | Fuente + lote de consulta | id_consulta | Bitácora: fuente, endpoint, tipo directo/indirecto, fecha_consulta, RUCs consultados y devueltos, archivo | — | README sección 2, fecha_consulta de cada pestaña | Sí — CTL_FUENTE_CONSULTA
180: HIST_ATRIBUTO | RUC + atributo + fecha | ruc + atributo + fecha_valor | Histórico de valores reemplazados, para auditar cambios de estado, dirección, contacto, etc. | — | — | Sí (plantilla vacía) — HIST_ATRIBUTO
182: 5.3 Diccionario de la tabla maestra DIM_ORGANIZACION (una fila por RUC)
183: Atributo | Tipo | Fuente 1: directa y vigente | Fuente 2: respaldo | Dónde está hoy (pestaña!columna) | Cobertura actual (registros con dato)
184: ruc | Texto(11) | rucs.txt / RUC_ID (universo) | SUNAT Consulta RUC | RUC_CONSULTAMASIVA!A | 597
185: razon_social | Texto | SUNAT Consulta RUC | OECE ficha; MIDAGRI-PPA | RUC_CONSULTAMASIVA!B · RUC_OECE!B | 597
186: nombre_comercial | Texto | SUNAT Consulta RUC | b2/b3 (sigla declarada) | RUC_CONSULTAMASIVA!E | 110
187: tipo_contribuyente | Texto | SUNAT Consulta RUC | OECE tipo_empresa | RUC_CONSULTAMASIVA!C | 597
188: tipo_organizacion_programa | Texto | Registro interno (b2) | Derivar de tipo_contribuyente | b2!DK | 650
189: estado_contribuyente | Texto | SUNAT (la fecha de consulta más reciente) | OECE estado_sunat | RUC_CONSULTAMASIVA!G | 597
190: condicion_contribuyente | Texto | SUNAT (la fecha de consulta más reciente) | OECE condicion_sunat | RUC_CONSULTAMASIVA!F | 597
191: fecha_inscripcion_ruc | Fecha | SUNAT Consulta RUC | — | RUC_CONSULTAMASIVA!H | 597
192: fecha_inicio_actividades | Fecha | SUNAT Consulta RUC | b3 (declarado) | RUC_CONSULTAMASIVA!I | 597
193: ubigeo | Texto(6) | INEI, derivado de departamento/provincia/distrito SUNAT | b2 Ubigeo | b2!E | 648
194: departamento / provincia / distrito | Texto | SUNAT domicilio fiscal | OECE; b2/b3 | RUC_CONSULTAMASIVA!J:L | 597
195: direccion_fiscal | Texto | SUNAT domicilio fiscal | b3 dirección declarada | RUC_CONSULTAMASIVA!M | 597
196: actividad_comercio_exterior | Texto | SUNAT Consulta RUC | Derivar de HECHO_EXPORTACION | RUC_CONSULTAMASIVA!P | 597
197: ciiu_principal / sec1 / sec2 | Texto | SUNAT Consulta RUC | — | RUC_CONSULTAMASIVA!Q:S | 597
198: buen_contribuyente / agente_retencion | Texto | SUNAT Consulta RUC | — | RUC_CONSULTAMASIVA!U:V | 9
199: telefono_principal | Texto | OECE ficha de proveedor | b3 celular; SUNAT (vacío en este universo) | RUC_OECE!I | 116
200: email_principal | Texto | OECE ficha de proveedor | b3 correo | RUC_OECE!J | 111
201: inscrito_rnp / codigo_rnp | SI-NO / Texto | RNP (OECE) | OECE ficha codigo_registro | RNP!K · RUC_OECE!K | 155
202: inscrito_ppa / nombre_ppa | SI-NO / Texto | MIDAGRI-PPA | — | RUC_PPA!B:C | 0
203: ventas_totales_2024 | Número | Registro interno (b2, HECHO_PROGRAMA_ANUAL) | b2 ventas nacionales + exportación 2024 | DIM_ORGANIZACION!AA | 187
204: ventas_totales_2025 | Número | Registro interno (b2, HECHO_PROGRAMA_ANUAL) | b2 ventas nacionales + exportación 2025 | DIM_ORGANIZACION!AB | 258
205: exporta (SI/NO) | SI-NO | SUNAT-Aduanas (HECHO_EXPORTACION) | SUNAT actividad_comercio_exterior | RUC_FOB (2)!A | 64
206: fob_total_usd / fob_ultimo_anio_usd | Número | SUNAT-Aduanas (HECHO_EXPORTACION) | b2 ventas de exportación | RUC_FOB (2)!D:F | 64
207: ultimo_periodo_exportacion / n_paises | Texto / Número | SUNAT-Aduanas (HECHO_EXPORTACION) | — | RUC_FOB (2)!H:I | 1
208: presidente_vigente | Texto | OECE/RNP (REL_PERSONA_CARGO, vigente) | b3 (declarado) | RUC_OECE_PERSONAS!G | 126
209: representante_legal_vigente | Texto | OECE/RNP (rol REPRESENTANTE) | b3 representante legal | RUC_OECE_PERSONAS!B | 139
210: gerente_general | Texto | OECE/RNP (cargo Gerente General) | b3 gerente general | b3!AE | 24
211: n_directivos_vigentes | Número | OECE/RNP (REL_PERSONA_CARGO) | — | RUC_OECE_PERSONAS | 129
212: producto_dominante | Texto | Registro interno (b2) | CIIU principal SUNAT | b2!B | 672
213: anios_intervencion / servicio | Texto | Registro interno (b2) | b1 | b2!Q:R | 673
214: n_socios (varones / mujeres) | Número | Registro interno (b3, última campaña) | OECE socios (rol SOCIO) | b3!M:N | 25
215: hectareas_totales | Número | Registro interno (b3, última campaña) | — | b3!O | 25
216: certificacion_organica / comercio_justo (vigencia) | Texto | Organismo certificador (REL_CERTIFICACION) | b3 declarado; b1 tipo de certificado | b3!U:V | 24
217: avance_eudr | Texto | Registro interno (b3) | — | b3!Y | 20
218: fecha_ultima_actualizacion | Fecha-hora | MAX de fecha_consulta de todas las fuentes del RUC | — | fecha_consulta de cada pestaña | —
219: score_completitud | Número (%) | Derivado: atributos con dato / atributos del modelo | — | — | —
221: Nota: la cobertura cuenta los registros con dato en la pestaña actual (sobre 597 RUCs en SUNAT, OECE y PPA; 64 en FOB; 139 en personas; 25 en b3; 678 filas en b2). Lo ideal es construir DIM_ORGANIZACION con XLOOKUP por RUC sobre cada fuente, aplicando las reglas de 5.1.
223: 6. TABLAS DEL MODELO CONSTRUIDAS (pestañas nuevas, generadas a partir de las fuentes de las secciones 1-4)
224: Implementación del modelo descrito en la sección 5.2. Incluye la fuente RUC_CONTRATACION agregada el 23/09/2026 (archivo subido por el usuario) y la tabla HECHO_CONTRATACION_ESTATAL construida a partir de ella. Los conteos son fórmulas que leen cada pestaña.
225: Tabla | Tipo | Filas de datos | Fuente / cómo se construyó
226: RUC_CONTRATACION | Fuente (pestaña raíz, como RUC_FOB) | 53 | Archivo subido ruc-contratacion-estatal.txt (OECE / Open Contracting Partnership, bulk OCDS), consulta 23/09/2026. Ver CTL_FUENTE_CONSULTA fila 8.
227: DIM_ORGANIZACION | Tabla maestra | 597 | Fórmulas XLOOKUP/FILTER sobre RUC_CONSULTAMASIVA, RUC_OECE, REG_RNP, REG_PPA, HECHO_EXPORTACION, REL_PERSONA_CARGO, b2, b3 (reglas 5.1).
228: REG_RNP | Registro | 155 | Derivada de la pestaña RNP.
229: REG_PPA | Registro | 597 | Derivada de la pestaña RUC_PPA.
230: REL_PERSONA_CARGO | Relación (varias filas por RUC) | 815 | Derivada de RUC_OECE_PERSONAS.
231: DIM_PERSONA | Dimensión (una fila por DNI) | 712 | Derivada de REL_PERSONA_CARGO.
232: HECHO_EXPORTACION | Hecho | 958 | Derivada de RUC_FOB.
233: HECHO_CONTRATACION_ESTATAL | Hecho | 53 | Derivada de RUC_CONTRATACION (agregada 23/09/2026): vista en vivo 1:1 con fórmulas FILTER, mismo grano y mismas filas que la fuente (no es una agregación como HECHO_EXPORTACION). No editar esta pestaña directamente — cualquier corrección debe hacerse en RUC_CONTRATACION y se propaga sola.
234: HECHO_PROGRAMA_ANUAL | Hecho | 4928 | Derivada de b2 (616 RUC × 8 años 2018-2025).
235: HECHO_CAMPANIA_PRODUCTIVA | Hecho | 25 | Derivada de b3 (campaña 2026).
236: REL_CERTIFICACION | Relación (varias filas por RUC) | 66 | Derivada de b1 y b3.
237: REL_CONTACTO | Relación (varias filas por RUC) | 288 | Derivada de RUC_OECE y b3.
238: CTL_FUENTE_CONSULTA | Control | 8 | Carga manual, bitácora de cada consulta a las fuentes oficiales.
239: HIST_ATRIBUTO | Control | 0 | Plantilla vacía: se llena cuando se detecten cambios entre dos actualizaciones de las fuentes.
