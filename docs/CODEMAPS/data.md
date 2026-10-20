<!-- Generated: 2026-10-16 | Files scanned: 238 | Token estimate: ~740 -->
# Data — archivos de este repo y tablas que viven afuera

No hay ORM ni migraciones en el árbol. El grano de identidad es el RUC de 11 dígitos (`zfill`).

## Granos

```
organización (RUC)
  ├─ universo MIDAGRI / PRODUCE / padrón     data/backup, data/midagri_cafe_cacao_limpio.*
  ├─ hecho exportación agregado              BASE CONSOLIDADA.xlsx ! HECHO_EXPORTACION / RUC_FOB
  │     clave (ruc, anio, mes, aduana, agente, pais)   SIN número de DUA
  ├─ DUA + canal                             dua_canal_final.csv  y hoja RUC_FOB_DUA
  ├─ ítem de DUA (PDF)                       fichaduanas-cafe/DUA_CONSOLIDADO.xlsx
  ├─ scores D1–D14                           PLANTILLA_INDICE_PVE*.xlsx ! MATRIZ_174
  └─ parcela → lote → embarque → declaración SOLO en Postgres de appsperu (vacío de coordenadas)
```

## Archivos canónicos (cortes)

| Archivo | Rol | Notas al 2026-10-16 |
|---|---|---|
| `data/midagri_cafe_cacao_limpio.csv` | Padrón limpio café/cacao | sale de `procesar_base_midagri.py` |
| `data/resumen_universo_midagri.json` | Conteos del universo | mismo script |
| `data/backup/EUDRPERU_universo_final.csv` | Corte de universo | también `universo_v2`, `universo_v6`, `consolidado` |
| `data/backup/SUNAT_validacion_ruc.csv` | Estado/condición SUNAT | par `*_no_encontrados.csv` |
| `ficharucsunat/BASE CONSOLIDADA.xlsx` | Fuente maestra fiscal | hojas `DIM_ORGANIZACION`, `HECHO_EXPORTACION`, `RUC_FOB`, `RUC_FOB_DUA` |
| `ficharucsunat/dua_canal_final.csv` | Número de DUA + canal | se cruza con FOB por la clave agregada |
| `ficharucsunat/_verif_dua_links.csv` | Verificación en vivo de enlaces | |
| `fichaduanas-cafe/duas_parsed.json` | Caché del parseo PDF | `pdf_cache.json` al lado |
| `d3_batch_results.json` | Sanciones OSCE + OEFA de 36 orgs FOB UE | no es tabla |
| `name_mapping.pkl` | Mapa de nombres | binario local |

`data/backup/` guarda 26 cortes (csv/xlsx/json). No es un historial de migraciones: es respaldo de universo.

`data/icrpp/` es otra línea (cargas, naves, incidentes portuarios 2010–2023 y licencias APN). No une por RUC de cooperativa salvo los scripts `icrpp_*`.

## Excel de trabajo que no se regenera solo

- `3 directorio - trabajo en base global cafe cacao 12.10.26.xlsx` (el `07.10.26` y el `.BACKUP_PRE_ADUANET` son cortes).
- `LISTA_DEFINITIVA_ENRIQUECIDA.xlsx`, `LISTA_DEFINITIVA_FINAL_AUDITORIA.xlsx`.
- `REPORTE_FINAL_SOCIOS_HECTAREAS.xlsx`.
- `ISCAM/Modelo de Calculo - ISA-IP-IV-RE-AHP.xlsx`.

## Postgres (fuera de este repo)

Definido en `appsperu/apps/identidad-fiscal/api/src/db/migrations/`, citado por `Memoria Diaria EUDR.md`.

| Objeto | Dónde está poblado | Relación |
|---|---|---|
| `eudr_parcela` | ningún lado | 1 org → n parcelas (geometría aún sin datos) |
| `eudr_lote` | ningún lado | |
| `eudr_lote_parcela` | ningún lado | n:n lote–parcela |
| `eudr_lote_embarque` | ningún lado | |
| `eudr_declaracion` | ningún lado | DUA |
| `eudr_declaracion_lote` | ningún lado | n:n declaración–lote |
| `v_eudr_cobertura_org` | vista | cobertura por organización |
| `v_eudr_trazabilidad` | vista | cadena parcela → declaración |
| `ruc_exportaciones_fob` | Docker local | FOB agregado, sin número de DUA |
| `schema_migrations` | Docker 13/13; Neon solo `013_eudr_trazabilidad.sql` | |

Docker local (`identidad_fiscal`, puerto 5438) es el destino de trabajo. Neon de producción quedó con las 6 tablas `eudr_*` vacías y sin las migraciones 001–012. No hay `014_ruc_fob_dua.sql` en este repo: el número de DUA sigue solo en Excel.

Lecturas de apoyo en Neon (otras bases, no el esquema EUDR): `proveedores_sancionados`, `infracciones_ambientales`. `stage_eudr_exp` fue tabla temporal de cruce y se eliminó.

## Reglas de dato que el código ya aplica

- RUC siempre a 11 dígitos.
- Año ADUANET en la URL = año real − 1992 (`ruc_fob_connector.py`).
- Puntaje de encuesta: `None` no entra al promedio (`codificacion_instrumento2.py`).
- ISA no imputa dimensiones faltantes: repondera. Umbral: 7 de 9 dimensiones con ≥70% de ítems.
- D10 y D11 no se promedian. Banderas duras quedan fuera de IP/IV/RE.
- Control de PDF: suma de FOB de ítems vs campo 6.5; suma de pesos vs “OTROS DATOS” (`generar_duas.py`).
