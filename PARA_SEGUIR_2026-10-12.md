# Para seguir mañana — 12 de octubre de 2026

**Proyecto:** EUDR — café y cacao peruano · base de 174 organizaciones
**Última sesión:** 11 de octubre de 2026
**Registro en memoria:** `Memoria Diaria EUDR.md` §5, entradas `2026-10-11` y `2026-10-11b`

---

## 1. Dónde está todo

| Qué | Ruta |
|---|---|
**Trabajo de datos (raíz del proyecto)** | `C:\Users\acuba\eudrperu\BASE CAFE CACAO 174\CONSULTA MASIVA RUC 10.10.26\` |
**App / esquema** | `C:\Users\acuba\appsperu\apps\identidad-fiscal\` |
**Base de datos local** | Docker, `postgres://fiscal:fiscal@localhost:5438/identidad_fiscal` |
**Consolidado interno (fuente maestra)** | `C:\Users\acuba\eudrperu\ficharucsunat\BASE CONSOLIDADA.xlsx` |
**Archivo de trabajo MIDAGRI** | `C:\Users\acuba\eudrperu\3 directorio - trabajo en base global cafe cacao 07.10.26.xlsx` |
**Scripts de esta sesión** | `C:\Users\acuba\appsperu\*.py` (ver §6) y `...\BASE CAFE CACAO 174\*.py` |

### Entregables producidos

| Archivo | Contenido |
|---|---|
`MATRIZ_ORGANIZACIONES_174_FINAL.csv` / `.xlsx` | 174 organizaciones × 34 columnas, con hallazgos web y URLs |
`HALLAZGOS_174_ORGANIZACIONES.md` / `.docx` | Informe de las 174 fichas en 10 grupos |
`ENLACES_BUSQUEDA_DUA_2024-2026.xlsx` | 1.840 enlaces ADUANET; 699 verificados en vivo |
`CRUCE_DUAs_FOB_POR_ORGANIZACION.xlsx` | Cruce DUAs × FOB en dólares, 5 hojas |
`INFORME_CRUCE_DUAs_FOB.md` / `.docx` + 5 PNG | Informe con tablas y gráficos |
`TRIAJE_Y_DEPURACION_174.xlsx` | Triaje de los 32 RUC sin movimiento + duplicados |
`ACCIONES_EJECUTADAS.xlsx` | Las 6 acciones ejecutadas, 15 hojas |
`PLANTILLA_TRAZABILIDAD_EUDR.xlsx` + `.csv` | Plantilla de geolocalización con validaciones |
`013_eudr_trazabilidad.sql` | Migración del módulo de trazabilidad |
`docs/data-contracts/eudr-trazabilidad.md` | Contrato de datos del módulo |

---

## 2. Estado en una línea

Base de 174 organizaciones cerrada y depurada (**165 activas**), con exportación medida
(**US$ 243.192.124 y 1.141 DUAs** en 44 de 76 exportadores), y la dimensión de trazabilidad
(D2) **abierta a nivel de esquema, sin datos todavía**.

---

## 3. Lo primero que hay que hacer mañana

### 3.1 Decidir sobre Neon (bloquea producción)

Apliqué la migración 013 al Neon de producción por confusión de `.env`. **Neon está vacío**: no
tiene ninguna de las 12 migraciones previas. Quedaron 6 tablas `eudr_*` vacías y 1 fila en
`schema_migrations`.

Dos opciones, una sola cosa que hacer:

- **Revertir** (si Neon no es la base activa): `DROP` de las 6 tablas `eudr_*` y las 2 vistas
  `v_eudr_*`, y `DELETE FROM schema_migrations WHERE filename='013_eudr_trazabilidad.sql'`.
  El script que lo hace está en `appsperu\aplicar_migracion.py` como referencia del patrón.
- **Completar** (si Neon debe quedar como producción): aplicar 001-013 en orden con
  `appsperu\aplicar_migraciones_local.py`, cambiando la `URL` por la de Neon.

**Mientras tanto**, el destino correcto de trabajo sigue siendo el Docker local, que quedó con
13/13 migraciones y datos reales.

### 3.2 Verificar el RUC 20611316616 con MIDAGRI

Caso abierto de la sesión anterior. Ver §5.

### 3.3 Decidir el alcance del universo (acción 6)

Tres opciones documentadas en `ACCIONES_EJECUTADAS.xlsx`, hoja `6b. Opciones alcance`. Mi
recomendación: **opción B**, 171 unidades productivas. Si se elige B o C hay que regenerar matriz
e informe.

---

## 4. Trabajo pendiente, por orden de valor

### 4.1 Ingerir `RUC_FOB_DUA` como tabla propia — **lo más urgente del esquema**

Hoy las DUAs viven solo en el Excel `BASE CONSOLIDADA.xlsx`, hoja `RUC_FOB_DUA`. La base tiene
`ruc_exportaciones_fob`, que trae FOB agregado por mes/aduana/agente/país y **sin número de DUA**.
Consecuencia: la cadena parcela → lote → DUA no se puede resolver dentro de la base.

Falta: migración `014_ruc_fob_dua.sql` + conector en `src/ingest/` (connector + normalize,
siguiendo el patrón de `exportaciones-fob-connector.ts`). Son 1.704 filas y la clave
`(ruc, anio, aduana_codigo, agente_codigo, pais_codigo)` ya existe en el Excel.

### 4.2 Conector de la plantilla de trazabilidad

La plantilla existe pero no hay quien la ingeste. Falta `eudr-parcelas-connector.ts` +
`eudr-parcelas-normalize.ts` con el patrón del proyecto. Las validaciones de negocio ya están en
la base (constraints), así que el conector solo lee, normaliza e inserta.

### 4.3 Ruta HTTP y tests

Siguiendo `src/routes/exportaciones-fob.ts` y sus tests en `src/__tests__/`. Mínimo: un
`GET /eudr/cobertura` que lea `v_eudr_cobertura_org`.

### 4.4 Recolectar geolocalización real

**Ninguna de las 174 organizaciones ha entregado coordenadas.** Sin eso, D2 sigue en cero por más
esquema que se abra. Nota del data contract: la geolocalización es el dato más fácil de falsificar
y el más difícil de verificar.

### 4.5 Refresco del pipeline

`cruce_fob_dua.py`, `verificar_enlaces_bg.py` y `build_enlaces_dua.py` regeneran todo desde
ADUANET. No están orquestados: hay que correrlos a mano.

---

## 5. Casos abiertos que hay que arrastrar

### RUC 20611316616 — no usar como cacaotera

Asociación de Productores Agropecuarios San Miguel. Contradicciones sin resolver:

| Fuente | Dice |
|---|---|
SUNAT | Áncash, **Nuevo Chimbote** (costa); CIIU principal **"cría de animales domésticos"**; inscrita **03/11/2025** |
MIDAGRI | Beneficiaria PAC desde **2019**, 22 beneficiados; sede **Piura, San Miguel de el Faique**; producto **cacao** |

Una organización no puede operar 6 años antes de tener RUC. En la misma base existe la
Organización Zonal San Miguel del Faique (RUC `20604401187`). Lectura: RUC mal asignado o cruzado
al cargar. Está recuperada la razón social; falta aclarar a qué organización corresponde.

### RUC con riesgo de suspensión que "parecen" exportadores relevantes

Dos de los 9 excluidos tienen peso público y conviene no confundirlos:

- `20561140091` **CECAFE de Lonya Grande** — 851 socios, tesis PUCP, suspendida.
- `20486668335` **CAI Sonomoro** — suspendida. La que exporta es `20486973219` (COAS, US$ 30,3 M).

### Déficit de cobertura del FOB 2024

`ruc-exportaciones-fob.txt` arranca en 2025. El FOB de 2024 salió de `HECHO_EXPORTACION`
(278 filas, agente en cero). Las DUAs de 2024 existen por combinación, pero el listado por combo
de ese año no está armado.

---

## 6. Scripts de reproducción

Todos en `C:\Users\acuba\appsperu\` salvo indicación:

| Script | Para qué |
|---|---|
`build_matriz_final.py` (en `...\BASE CAFE CACAO 174\`) | Regenera la matriz desde los 10 `findings_parte*.py` |
`build_informe.py` (ídem) | Regenera el informe de hallazgos `.md` y `.docx` |
`generar_informe.py` (en `eudrperu\`) | Regenera el informe del cruce DUAs×FOB y los 5 gráficos |
`build_enlaces_dua.py` | Regenera los enlaces ADUANET (sin verificación en vivo) |
`verificar_enlaces_bg.py` | Verifica los enlaces en vivo; reanudable, guarda en `_verif_dua_links.csv` |
`cruce_fob_dua.py` | Regenera el cruce DUAs × FOB |
`validar_cruce.py` | Cuadre del cruce (4 hojas deben dar el mismo total) |
`ejecutar_acciones.py` | Regenera el Excel de las 6 acciones |
`triaje_entregable.py` | Regenera el Excel de triaje y duplicados |
`generar_plantilla_eudr.py` | Regenera la plantilla de trazabilidad |
`validar_migracion_eudr.py` | Valida las reglas EUDR en Neon (transaccional, revierte) |
`validar_local.py` | **Valida las reglas EUDR en el Docker local** — usar este |
`aplicar_migraciones_local.py` | Aplica las migraciones pendientes al Docker local |
`aplicar_migracion.py` | Aplica solo la 013 (patrón de `migrate.ts`) |

**Nota:** varios scripts tienen rutas absolutas apuntando a `appsperu`. Si se ejecutan desde otro
directorio, revisar primero.

---

## 7. Comandos de arranque

```powershell
# 1. levantar Docker (si está parado)
& "$env:LOCALAPPDATA\Programs\DockerDesktop\resources\bin\docker.exe" desktop start

# 2. levantar el Postgres de la app
cd C:\Users\acuba\appsperu\apps\identidad-fiscal\api
& "$env:LOCALAPPDATA\Programs\DockerDesktop\resources\bin\docker.exe" compose up -d

# 3. comprobar cuántas migraciones faltan
python C:\Users\acuba\appsperu\aplicar_migraciones_local.py

# 4. validar las reglas EUDR sin dejar rastro
python C:\Users\acuba\appsperu\validar_local.py
```

---

## 8. Lecciones de la sesión anterior (para no repetirlas)

1. **Dos `.env`, dos bases.** `C:\Users\acuba\appsperu\.env.local` → **Neon (producción)**.
   `apps\identidad-fiscal\api\.env` → **Docker local:5438**. Antes de tocar una base, confirmar
   cuál es.
2. **Las razones sociales tienen faltas de ortografía.** "COORDILLERA" con doble D hizo que
   buscara mal una organización que sí existía. Usar búsquedas tolerantes.
3. **`schema_migrations` vacío no significa base limpia.** Verificar las tablas reales antes de
   concluir.
4. **Un campo vacío en el consolidado no significa dato ausente.** El RUC 20611316616 no estaba en
   `BASE CONSOLIDADA.xlsx` pero sí en el archivo de trabajo de MIDAGRI.
5. **Validar contra la base real, no solo en papel.** La validación transaccional detectó que
   `ruc_fob_dua` no existe como tabla; un análisis solo en Excel no lo habría visto.
6. **Cerrar cada `fetchall()` sobre INSERT.** Un `INSERT` no devuelve filas.
