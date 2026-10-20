<!-- Generated: 2026-10-16 | Files scanned: 238 | Token estimate: ~720 -->
# Architecture — EUDR Perú (café y cacao)

Research workspace, not a deployed app. One repo, many batch scripts. The operational UI is Excel. The production API lives outside this tree.

```
MIDAGRI / SUNAT / ADUANET / OECE / OEFA
        |                |              |
        v                v              v
 Scripts/universo   ficharucsunat/   Neon (OSCE, OEFA)
 data/backup/*.csv  BASE CONSOLIDADA  batch_d3_*.py
        \                /              /
         v              v              v
          BASE CAFE CACAO 174  (174 orgs, ~165 activas)
                    |
                    v
     PLANTILLA_INDICE_PVE*.xlsx  ← codificacion_instrumento2.py
                    |                 Instrumentos/ D1–D14
                    v
        ISA / IP / IV / RE   +  scorecards .docx
                    |
                    v
     HTML EDA · informes .docx/.pdf · memoria diaria

Fuera del repo (no escanear como código de aquí):
  appsperu/apps/identidad-fiscal   API + migraciones 001–013
  Docker Postgres identidad_fiscal :5438   (trabajo activo)
  Neon producción                  migración 013 sola, tablas eudr_* vacías
```

## Boundaries

| Boundary | Owns | Does not own |
|---|---|---|
| Este repo | Universo, cruce FOB/DUA, índices ISCAM, informes | HTTP, auth, migraciones SQL |
| `ficharucsunat/` | Identidad fiscal y hecho de exportación en Excel | Persistencia de parcela |
| `fichaduanas-cafe/` | PDF de DUA → filas de ítem | Consulta en vivo a ADUANET |
| `Instrumentos/` | Preguntas, codificación, Google Form | Respuestas de campo (aún no hay coordenadas) |
| appsperu | `eudr_parcela → lote → embarque → declaracion` | Cálculo ISA/IP/IV |

## Canonical entry points

No `main` único. Se corre cada script a mano desde la raíz.

| Pipeline | Entry | Output |
|---|---|---|
| Universo MIDAGRI | `Scripts/procesar_base_midagri.py` | `data/midagri_cafe_cacao_limpio.*` |
| FOB ADUANET | `ficharucsunat/ruc_fob_connector.py` | `ruc_fob.csv` → hoja `RUC_FOB` |
| Canal DUA | `ficharucsunat/dua_canal_full.py` | `dua_canal_final.csv` |
| Parseo PDF | `fichaduanas-cafe/generar_duas.py` | `DUA_CONSOLIDADO.xlsx`, `duas_parsed.json` |
| Enlaces | `build_enlaces_dua.py` | `ENLACES_BUSQUEDA_DUA_2024-2026.xlsx` |
| Cruce | `cruce_fob_dua.py` | `CRUCE_DUAs_FOB_POR_ORGANIZACION.xlsx` |
| Matriz 174 | `BASE CAFE CACAO 174/build_matriz_final.py` | `MATRIZ_ORGANIZACIONES_174_FINAL.*` |
| Plantilla PVE | `build_pve_index.py` | `PLANTILLA_INDICE_PVE.xlsx` |
| Libro ISCAM | `build_iscam.py` → `v2` → `v3` | `PLANTILLA_INDICE_PVE_ISCAM.xlsx` |
| Codificación | `codificacion_instrumento2.py` | tabla opción → 0–100 (no promedia `None`) |
| Legalidad D3 | `batch_d3_final.py` → `d3_populate_all.py` | `d3_batch_results.json` + Excel |
| EDA | `Scripts/eda_eudr.py`, `eda_cafe_cacao.py` | `eda_output*/` |

## Index flow

`Scripts/matriz_data.py` mapea cada pregunta a IP e IV. `codificacion_instrumento2.py` puntúa 0–100; ausencia = sin dato, no cero.

```
Instrumento 2 (D1–D14, Bloque 0, Bloque P)
    ├─ ISA  = 0.875·geom(D1–D7) + 0.125·arit(D8–D9)    D10/D11 fuera del promedio
    ├─ IP   = media igual IP1..IP5   (D2; √(D3×D4); D8+D5+D6; D6.23+D2.9; D7+D9+certs)
    ├─ IV   = media igual IV1..IV5   (mercado UE, exposición, territorio, tech, social)
    └─ RE   = IV · (1 − IP/100)
Banderas (D2.10, D10, trabajo forzoso) se reportan aparte. Pesos AHP aún no aplicados.
D12 huella, D13 reporte, D14 circular: añadidos 2026-10-08; D12 usa proxy FAO en fao_huella.py.
```

## Handoff

`PARA_SEGUIR_2026-10-12.md` es el estado operativo al 12 oct. La ratificación de codificación es del 15 oct (`add_nota_ratificacion.py`). Leer el código de índices si discrepan.
