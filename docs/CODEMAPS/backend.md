<!-- Generated: 2026-10-16 | Files scanned: 238 | Token estimate: ~780 -->
# Backend — pipelines (no hay API en este repo)

No hay rutas HTTP, middleware ni servidor. El análogo de “ruta” es script → libro o CSV. La ruta prevista `GET /eudr/cobertura` está en appsperu, no aquí.

## Universo y padrón

```
MIDAGRI xlsx → Scripts/procesar_base_midagri.py → data/midagri_cafe_cacao_limpio.*
SUNAT lote   → Scripts/batch_sunat_validation.py | batch_sunat_retry.py | cruzar_sunat_completo.py
             → data/backup/SUNAT_*.csv
PG / nombre  → Scripts/batch_pg_*.py | batch_buscar_por_nombre.py | investigar_faltantes.py
Versiones    → Scripts/build_v7.py | build_v8.py | cruce_universo.py | cruce_v7_a3.py
             → data/backup/EUDRPERU_universo_*.csv | universo_v6.csv
```

## Aduanas y FOB

```
ADUANET ieITS01Alias
  → ficharucsunat/ruc_fob_connector.py          reconstruye RUC-año-mes-aduana-agente-país
  → ficharucsunat/dua_canal_connector.py        dua_canal_full.py | dua_canal_retry_2024.py
  → ficharucsunat/load_dua_canal.py             vuelca canal al libro
  → BASE CONSOLIDADA.xlsx  hojas HECHO_EXPORTACION, RUC_FOB, RUC_FOB_DUA, DIM_ORGANIZACION

PDF locales fichaduanas-cafe/*.pdf
  → desc_items.py            clasifica texto de serie
  → generar_duas.py          parse_serie | parse_consulta | construir_duas | escribir_excel
  → DUA_CONSOLIDADO.xlsx + duas_parsed.json

build_enlaces_dua.py → ENLACES_BUSQUEDA_DUA_2024-2026.xlsx   (no consulta en vivo)
verificar_enlaces_bg.py → _verif_dua_links.csv
cruce_fob_dua.py → CRUCE_DUAs_FOB_POR_ORGANIZACION.xlsx
  clave: (ruc, anio, mes, aduana, agente, pais)
extract_ue_fob.py, validar_cruce.py, generar_informe.py
```

Estos tres no están orquestados: `cruce_fob_dua.py`, `verificar_enlaces_bg.py`, `build_enlaces_dua.py`.

## Legalidad D3 (Neon, solo lectura)

```
batch_neon_d3.py | batch_neon_d3_v2.py | batch_d3_query.py | batch_d3_neon.py
  → batch_d3_final.py          bases proveedores_sancionados + infracciones_ambientales
  → d3_batch_results.json
  → d3_populate_all.py | populate_d3_excel.py     escribe la plantilla
oefa_rucs.py | oefa_emisiones.py                  mismo cruce OEFA, script suelto
d3_vs_isapv_analysis.py | d3_query_all.py | test_neon_conn.py
```

DSN está hardcodeado en esos archivos. No copiarlo a docs ni a commits nuevos.

## Índices ISCAM

```
build_pve_index.py
  build_instrucciones | build_ponderadores | build_matriz | build_preguntas
  build_scorecards | build_radar
  → PLANTILLA_INDICE_PVE.xlsx   hojas INSTRUCCIONES, PONDERADORES, MATRIZ_174,
                                 PREGUNTAS_PROXY, SCORECARDS, RADAR_BRECHAS

build_iscam.py → build_iscam_v2.py → build_iscam_v3.py → PLANTILLA_INDICE_PVE_ISCAM.xlsx
enrich_pve.py | build_ingesta.py | populate_d12_proxy.py | fao_huella.py
codificacion_instrumento2.py     REGLAS + NO_PROMEDIA + RULING (ratificado 2026-10-15)
Scripts/matriz_data.py           (bloque, id, pregunta, ruta_ip, ruta_iv); D12–D14
generate_scorecards.py           → reports/scorecards/SCORECARD_<ORG>_<RUC>.docx
qa_pve.py | verify_iscam.py | verify_final_pv.py | verify_d10_ip5.py
test_sintetico_pv.py | test_sintetico_ip5.py
```

Parches de libro y de documento (no son pipeline nuevo): `fix_*.py`, `update_docx_*.py`, `update_matriz.py`, `update_registro_*.py`, `add_nota_ratificacion.py`. Tocan `DT-ISCAM-001` y el documento de trabajo ISCAM.

## Matriz 174 e identidad

```
BASE CAFE CACAO 174/findings_parte1.py … findings_parte10.py
  → build_matriz_final.py     DIM_ORGANIZACION + hallazgos web
  → build_informe.py          HALLAZGOS_174_ORGANIZACIONES.md/.docx
ficharucsunat/identidad_fiscal_oece_ppa.py | oece_contrataciones_por_ruc.py
ficharucsunat/gerencia_gobernanza_build.py
ficharucsunat/ppaconsultamultiple/*        padrón PPA / OECE
ficharucsunat/rucconsultamultiple/*        dumps SUNAT txt → xlsx
ficharucsunat/convert_to_gsheets.py        BASE CONSOLIDADA_GSheets.xlsx
```

## Informes

```
Scripts/eda_eudr.py | eda_cafe_cacao.py
Scripts/generar_dossier_word.py | generar_matriz_docx.py | docx_a_pdf.py
generar_doc_iscam.py | generar_doc_academico.py | generar_pdf_academico.py
generar_memoria_eudr.py
reports/generar_tablas_informe_eudr.py → reports/informe_eudr_tablas.xlsx
Instrumentos/md_to_docx.py
```

## Side track ICRPP (puertos, no núcleo EUDR)

`Scripts/icrpp_serie_historica.py | icrpp_monte_carlo.py | icrpp_naves_2023_callao.py | icrpp_rlac_verificacion.py` leen `data/icrpp/`.
