# Fuentes y Endpoints — Ficha RUC SUNAT/eudrperu

> Ricardo | Generado: 2026-09-22

---

## 1 · rucs.txt
**Contenido:** Lista de 598 RUCs (solo el número, sin más campos).

**Fuente de origen:** Es el universo de consulta — fue la **base de partida** para cruzar con todas las demás fuentes. No es un dataset público per se; es la entrada que define el universo de cooperativas agrarias.

---

## 2 · ruc-exportaciones-fob.txt
**Contenido:** Operaciones de exportación FOB por RUC, año, mes, aduana, país de destino y valor FOB en USD. (680 registros).

### Fuentes oficiales para re-construir o ampliar este dato

| Recurso | URL / Endpoint | Notas |
|---|---|---|
| SUNAT — Estadísticas de exportaciones | https://www.sunat.gob.pe/estadisticasestudios/exportaciones.html | 14 cuadros (G1–G14), incluye exportación por sector, país, aduanas |
| SUNAT — Exportaciones FOB por Aduanas (anuario XLS) | https://www.sunat.gob.pe/estad-comExt/modelo_web/informes/anuarios/2024/cdro_33.xlsx | Cuadro N°33 por aduanas 2023–2024, actualización frecuente |
| SUNAT — Consulta de exportaciones (web) | https://ww3.sunat.gob.pe/servlet/HRGDecExp?opcion=aduanaexp&codr=50 | Formulario web: consulta por aduana, partida, fechas |
| SUNAT — Acumulado por subpartida/país (Aduanet) | http://www.aduanet.gob.pe/cl-ad-itestadispartida/resumenPPaisS01Alias | Acumulado por subpartida nacional y país de destino, incluye valor FOB exportación |
| PNDA — Datos Abiertos (si estuviera publicado) | https://datosabiertos.gob.pe | Buscar dataset de "exportaciones" |

**Nota:** La descarga por RUC individual no tiene API pública oficial. El anuario SUNAT ofrece totales por aduana/país pero no por empresa específica.

---

## 3 · ruc-oece-ficha.txt
**Contenido:** Ficha de organizaciones — razón social, tipo de empresa, estado SUNAT, condición, ubicación, teléfono, correo, código de registro. (597 registros).

### Fuentes oficiales para re-construir o ampliar

| Recurso | URL / Endpoint | Notas |
|---|---|---|
| OpenRUC — API gratuita RUC SUNAT | `GET https://openruc.com/api/ruc/{ruc}` | Sin API key, JSON, razón social + estado + condición + dirección. Patrocinado por Latinfo |
| APISUNAT — Documentación | https://docs.apisunat.pe/consulta/sunat-ruc | `GET https://dev.apisunat.pe/api/v1/business/ruc/{RUC}` — requiere API key |
| APIperu — Consulta RUC | https://docs.apiperu.dev/referencia/consultar-ruc/ | `POST https://api.apiperu.dev/ruc` — plan gratuito disponible |
| json.pe — Consulta RUC | https://docs.json.pe/api-consulta/endpoint/ruc | `POST https://api.json.pe/api/ruc` — requiere token |
| SUNAT — Consulta RUC (web oficial) | https://e.sunat.gob.pe/ | Formulario web con CAPTCHA, no es API |

---

## 4 · ruc-oece-personas.txt
**Contenido:** Órganos de administración y representantes legales — rol, DNI, nombre, cargo, tipo de órgano, fecha de ingreso. (815 registros).

### Fuentes oficiales para re-construir o ampliar

| Recurso | URL / Endpoint | Notas |
|---|---|---|
| OECE — Portal de Contrataciones Abiertas (OCDS) | https://contratacionesabiertas.oece.gob.pe | JSON/Excel/CSV de todos los procesos de contratación 2003–presente |
| OECE — Datos abiertos | https://www.gob.pe/institucion/oece/tema/transparencia-y-datos-abiertos | Enlaces a estadísticas, inteligencia de negocios, observatory de precios |
| Croma API — OECE Contrataciones | `POST https://api.croma.run/pe/oece/processes-search/v1` | Búsqueda por RUC de proveedor, buyer, texto, categoría, fechas. Dataset indexado |
| Apify — Peru OECE Tender Scraper | https://apify.com/publicmoney/peru-oece-scraper | Actor que lee `contratacionesabiertas.oece.gob.pe` directamente y exporta JSON/CSV/Excel |
| SEACE — Consulta por RUC (si existiera bulk) | https://www.gob.pe/oece | Enlaza al SEACE; la ficha de proveedor incluye directivos en el registro de contratistas |

**Nota:** Los datos de "órganos de administración" (roles como CONSEJO DE ADMINISTRACION, REPRESENTANTE) parecen provenir del RNP o de la ficha extendida OECE/SUNAT. No hay un endpoint público OCDS específico para esta estructura de gobierno corporativo.

---

## 5 · ruc-oece-ficha-inscritos-rnp.txt
**Contenido:** Igual estructura que ficha OECE, pero solo los RUCs inscritos en el RNP (Registro Nacional de Proveedores). (155 registros).

### Fuentes oficiales para re-construir o ampliar

| Recurso | URL / Endpoint | Notas |
|---|---|---|
| RNP — Consulta RUC | https://www.rnp.gob.pe/Constancia/RNP_Constancia/ConsultaRuc.asp | Formulario web con CAPTCHA — verificación de inscripción |
| RNP — Consulta RUC y Condiciones | https://www.rnp.gob.pe/Constancia/RNP_Constancia/ConsultaRucEyC.asp | Verificación de constancia de inscripción |
| RNP — Trámites en línea | https://www.gob.pe/7832-acceder-a-tramites-en-linea-del-registro-nacional-de-proveedores-rnp | Portal del.gob.pe para acceso al RNP |
| OECE — SEACE / Registro de proveedores | https://www.gob.pe/oece | Entrada al sistema de proveedores del Estado |

**Nota:** El RNP no tiene API REST pública de descarga masiva. La consulta es una por una con CAPTCHA.

---

## 6 · ruc-padron-ppa.txt
**Contenido:** Padrón de Productores Agrarios (PPA) — RUC, indicador de registro, nombre. (597 registros).

### Fuentes oficiales para re-construir o ampliar

| Recurso | URL / Endpoint | Notas |
|---|---|---|
| MIDAGRI — PPA Portal oficial | https://ppa.midagri.gob.pe | Portal del Padrón de Productores Agrarios |
| PPA — Ficha técnica (PDF) | https://ppa.midagri.gob.pe/media/attachments/2022/02/18/ft_ficha-tcnica.pdf | Metodología y estructura del padrón |
| PPA — Consulta de inscripción (web) | https://www.gob.pe/29665-consultar-si-estas-registrado-en-el-padron-de-productores-agrarios-ppa | Consulta individual por DNI/RUC — portal.gob.pe |
| MIDAGRI — Padrones públicos | https://midagri.gob.pe | Enlaces a padrones agrarios,stats |

**Nota:** El PPA es manejado por MIDAGRI (Ministerio de Desarrollo Agrario y Riego). No hay API pública de descarga bulk al cierre de este informe. El registro se hace presencialmente en centros de empadronamiento.

---

## Resumen de endpoints útiles para ampliación futura

| Dataset | Endpoint / Portal | Tipo de acceso |
|---|---|---|
| RUC SUNAT (básico) | `https://openruc.com/api/ruc/{ruc}` | API GET, sin auth, gratis |
| RUC SUNAT (completo) | `https://api.apiperu.dev/ruc` | API POST, requiere token (plan gratuito) |
| Exportaciones FOB | https://www.sunat.gob.pe/estadisticasestudios/exportaciones.html | Descarga XLS por año/sector |
| Exportaciones por RUC | http://www.aduanet.gob.pe/cl-ad-itestadispartida/resumenPPaisS01Alias | Formulario web por subpartida/país |
| Contrataciones OECE | `POST https://api.croma.run/pe/oece/processes-search/v1` | API, búsqueda por RUC proveedor |
| Contrataciones OECE (bulk) | https://contratacionesabiertas.oece.gob.pe | JSON/CSV/Excel diario, OCDS |
| Padrón Productores Agrarios | https://ppa.midagri.gob.pe | Web, consulta individual |
| RNP Proveedores | https://www.rnp.gob.pe | Web, consulta individual con CAPTCHA |

---

*Fuentes verificadas: 2026-09-22. Los endpoints pueden cambiar — se recomienda verificar cada URL antes de automatizar.*
