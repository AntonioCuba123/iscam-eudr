<!-- Generated: 2026-10-16 | Files scanned: 238 | Token estimate: ~520 -->
# Frontend — superficies, no una SPA

No hay `src/`, React, Vue ni router. Lo que el usuario abre es un libro, un HTML estático o un formulario de Google.

## Superficies

| Superficie | Path | Quién la produce |
|---|---|---|
| Libro maestro fiscal | `ficharucsunat/BASE CONSOLIDADA.xlsx` | conectores ADUANET + carga manual |
| Directorio de trabajo | `3 directorio - trabajo en base global cafe cacao 12.10.26.xlsx` | edición directa; `07.10.26` y backup son cortes |
| Universo 174 | `BASE CAFE CACAO 174/MATRIZ_ORGANIZACIONES_174_FINAL.xlsx` | `build_matriz_final.py` |
| Índice operativo | `PLANTILLA_INDICE_PVE.xlsx` | `build_pve_index.py` + parches `fix_*` / `update_*` |
| Índice ISCAM | `PLANTILLA_INDICE_PVE_ISCAM.xlsx` | `build_iscam_v3.py` |
| Matriz IP/IV | `Instrumentos/MATRIZ_IP_IV_v18_EUDRPERU.xlsx` | versiones previas en `data/backup/MATRIZ_IP_IV_*` |
| DUA consolidada | `fichaduanas-cafe/DUA_CONSOLIDADO.xlsx` | `generar_duas.py` |
| Enlaces ADUANET | `BASE CAFE CACAO 174/CONSULTA MASIVA RUC 10.10.26/ENLACES_BUSQUEDA_DUA_2024-2026.xlsx` | `build_enlaces_dua.py` |
| Cruce FOB | `.../CRUCE_DUAs_FOB_POR_ORGANIZACION.xlsx` | `cruce_fob_dua.py` |
| Triaje | `.../TRIAJE_Y_DEPURACION_174.xlsx`, `ACCIONES_EJECUTADAS.xlsx` | sesión 10–12 oct |
| Trazabilidad (vacía) | `.../PLANTILLA_TRAZABILIDAD_EUDR.xlsx` | plantilla; sin coordenadas cargadas |
| Scorecard | `reports/scorecards/SCORECARD_*.docx` | `generate_scorecards.py` |

## Hojas del libro PVE (la “UI” del índice)

```
INSTRUCCIONES
PONDERADORES          pesos editables (amarillo = input)
MATRIZ_174            una fila por organización
PREGUNTAS_PROXY       campo rápido por dimensión
SCORECARDS            semáforo PVE
RADAR_BRECHAS         resumen por departamento
```

`build_ingesta.py` usa Excel COM para no perder caché de fórmulas, comentarios y VML. `openpyxl` solo no basta en ese paso.

## HTML estático (sin estado)

| Archivo | Origen |
|---|---|
| `eda_output/EDA_EUDR.html` | `Scripts/eda_eudr.py` |
| `eda_output_cc/EDA_CAFE_CACAO.html` | `Scripts/eda_cafe_cacao.py` |
| `eval_output/EVAL_NUEVOS_DATOS.html` | evaluación SUNAT/FOB |
| `docs/ANALISIS_*.html`, `FUNDAMENTOS_UNIVERSO_*.html`, `ARQUITECTURA_GOOGLESHEET_EUDR.html` | notas publicadas a HTML |

No comparten estado con el Excel. Regenerar el script sobrescribe el HTML.

## Campo (fuera del repo)

```
Instrumentos/Google Apps Script - Crear Formulario Instrumento 2.gs
  → Google Form
  → Google Sheet   (contrato: Instrumentos/Estructura Google Sheet - Respuestas Instrumento 2.md)
  → Plantilla Google Sheet - Respuestas Instrumento 2.csv
```

No hay cliente que lea esas respuestas y escriba `MATRIZ_174`. El puente es manual o vía `build_ingesta.py`.

## Documentos que se editan como entregable

`DT-ISCAM-001_Indice_ISCAM_Trabajo.docx`, `ISCAM_UU_Peru_EUDR_DocumentoTrabajo.docx`, `Memoria_Diaria_EUDR.docx`, `reports/Informe_Diagnostico_EUDR_MIDAGRI.*`. Los `update_docx_*.py` parchean numeración, D10, IP5 y notas de “sin dato”.
