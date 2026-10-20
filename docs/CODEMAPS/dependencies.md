<!-- Generated: 2026-10-16 | Files scanned: 238 | Token estimate: ~560 -->
# Dependencies — servicios y librerías

Declaradas en `requirements.txt` (piso, no lockfile):

```
pandas>=2.0  openpyxl>=3.1  python-docx>=1.1  reportlab>=4.0
numpy>=1.24  scipy>=1.10    matplotlib>=3.7
```

Usadas en código y no pinneadas ahí: `psycopg2` (Neon), PyMuPDF (parseo de DUA en `generar_duas.py`), Excel COM / `pywin32` (`build_ingesta.py`). No hay `package.json` ni entorno de app web.

## Servicios externos

| Servicio | Para qué | Dónde se llama |
|---|---|---|
| ADUANET `cl-ad-itconsultadwh/ieITS01Alias` | FOB y listado de DUA | `ficharucsunat/ruc_fob_connector.py`, `dua_canal_*.py` |
| SUNAT consulta RUC masiva | Estado, condición, CIIU, ubigeo | dumps en `ficharucsunat/rucconsultamultiple/`; `Scripts/batch_sunat_*.py` |
| OECE / OSCE | Contrataciones, RNP, padrón PPA, inhabilitaciones | `oece_contrataciones_por_ruc.py`, `ppaconsultamultiple/`, Neon `proveedores_sancionados` |
| OEFA | Infracciones y emisiones | `oefa_rucs.py`, `oefa_emisiones.py`, Neon `infracciones_ambientales` |
| MIDAGRI / catastro rural | Universo de cooperativas y titulación | Excel de directorio; `reports/consulta_catastro_rural_25_orgs.py` |
| PRODUCE | Padrón de cooperativas | `data/backup/Cooperativas_2024_PRODUCE.csv` |
| Neon Postgres | Lectura OSCE/OEFA; accidente de migración 013 | `batch_d3_*.py`, `batch_neon_d3*.py`, `d3_query_all.py`, `test_neon_conn.py`, `oefa_*.py` |
| Docker Postgres local | Identidad fiscal + trazabilidad EUDR | no hay cliente en este repo; lo usa appsperu |
| Google Forms / Sheets | Instrumento 2 | `.gs` + CSV plantilla en `Instrumentos/` |
| Apify | Búsqueda OECE | `ficharucsunat/ppaconsultamultiple/apify_search_oece.py` |
| FAO / IPCC / SETAC | Factores de huella D12 (proxy, no API) | `fao_huella.py` |

El conector FOB es un puerto en Python de `appsperu/apps/identidad-fiscal/api/src/ingest/exportaciones-fob-connector.ts`.

## Secretos

Varios scripts traen el DSN de Neon en claro (`batch_d3_final.py`, `batch_d3_neon.py`, `batch_neon_d3.py`, `batch_neon_d3_v2.py`, `oefa_rucs.py`, y los `connect()` de `d3_query_all.py` / `test_neon_conn.py`). Este mapa no reproduce host, usuario ni clave. Rotar esa clave si el archivo salió del disco local. El handoff `PARA_SEGUIR_2026-10-12.md` también escribe la URL local con usuario y clave: no copiarla a sitios nuevos.

## Librerías compartidas (patrones, no paquetes)

No hay un módulo `lib/` importado por todos. Cada script abre el xlsx por ruta absoluta `C:\Users\acuba\eudrperu\...`.

| Pieza reutilizable | Qué concentra |
|---|---|
| `Scripts/matriz_data.py` | Mapa pregunta → ruta IP / ruta IV |
| `codificacion_instrumento2.py` | Opción → puntaje y lista `NO_PROMEDIA` |
| `build_pve_index.py` | Estilos de celda (input amarillo, fórmula negro, pendiente gris) |
| `fichaduanas-cafe/desc_items.py` | Limpieza y clasificación de descripción de serie |
| `ficharucsunat/convert_to_gsheets.py` | Fórmulas Excel → sintaxis de Google Sheets |

## Lo que no es dependencia de runtime

PDFs en `EUDR/`, `EUDR_ISCAM_Referencias/`, `adex cein 2025 2026 cafe cacao/` y el corpus `fichaduanas-cafe/*.pdf` son evidencia, no librerías. `ISCAM/respaldos/` y `respaldos/` son copias de trabajo.
