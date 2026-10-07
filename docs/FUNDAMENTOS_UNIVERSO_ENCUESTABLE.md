# Fundamentos del universo de cooperativas potencialmente encuestables — EUDR Perú

**Fecha:** septiembre 2026
**Elaborado por:** Mavis / Ricardo
**Versión:** 1.0

---

## 1. ¿Por qué decimos que son más de 200 cooperativas potencialmente encuestables?

### Respuesta corta

Porque tenemos **245 organizaciones con RUC validado por SUNAT** — es decir, personas jurídicas existentes, con número de identificación tributaria vigente — y de esas, **177 tienen geolocalización GPS y datos de contacto directo** (presidente, gerente, teléfono, correo) provenientes del **CENCOOP 2017**. Las demás al menos tienen dirección fiscal verificable via SUNAT. Ninguna es una organización inventada: todas existen en al menos una fuente administrativa.

### Respuesta extensa

El número "200+" no sale de un directorio cualquiera. Se construye cruzando **seis fuentes independientes** y exigiendo que cada organización cumpla al menos uno de estos criterios:

**Criterio de inclusión (al menos uno):**

| # | Criterio | Fuente | Org que lo cumplen |
|---|----------|--------|-------------------|
| 1 | Tiene operaciones de exportación registradas | PRODUCE | 56 |
| 2 | Está inscrita como organización agraria | MIDAGRI | ~220 |
| 3 | Aparece en el directorio PAC (café/cacao) | PAC directo | 48 |
| 4 | Existe en el CENCOOP 2017 con RUC vigente | SOPARSE | 177 |
| 5 | Tiene keywords café/cacao + RUC validado SUNAT | SUNAT | 245 |

Cada organización de las 245 cumple **al menos dos** de estos criterios simultáneamente.

---

## 2. Las 245 organizaciones

### De dónde salen

Las 245 organizaciones se construyeron a partir de **un proceso de consolidación en cuatro etapas:**

**Etapa 1 — Archivo Directorio PAC (PAC = Productores Asociados Cafetaleros, Cepicafe-Norandino) (PAC = Productores Asociados Cafetaleros, Cepicafe / Norandino)**
48 organizaciones con nombre, RUC, departamento, macro-zona, producto (café o cacao), representante y certificación. Este archivo es el punto de partida más antiguo y más validado por campo.

**Etapa 2 — MIDAGRI (cooperativas agrarias inscritas)**
Se descargó el directorio de cooperativas agrarias registradas del MIDAGRI y se hizo un cruce por RUC + nombre con keywords café/cacao. Esto añadió organizaciones que no estaban en PAC.

**Etapa 3 — PRODUCE (base de exportadores)**
Se cruzó la base de operaciones de exportación del PRODUCE con el universo agrario. Las organizaciones que tienen al menos una operación de exportación en 2024 fueron incorporadas con datos de FOB, número de operaciones, número de países destino y número de socios.

**Etapa 4 — Validación SUNAT**
Los 245 RUCs fueron validados uno por uno contra la API de identidad-fiscal de SUNAT (puerto 4006, identidad-fiscal). Resultado: **245 de 245 = 100% válidos**. Esto significa que ninguna organización en la matriz tiene un RUC inventado, dado de baja o duplicado.

**Etapa 5 — Cruce con CENCOOP 2017 (SOPARSE)**
El archivo SPSS del Directorio del Censo Nacional de Cooperativas 2017 (INESI/MINCETUR) se cruzó por RUC. Las 177 organizaciones que hicieron match recibieron datos adicionales de geolocalización (GPS), contactos de directivos, año de constitución, año de inicio de operaciones y CIIU.

### Perfil de las 245 organizaciones

**Por producto:**
- Café: ~210 organizaciones (86%)
- Cacao: ~25 organizaciones (10%)
- Ambas: ~10 organizaciones (4%)

**Por departamento (principales):**
- Junín: ~70 organizaciones
- Cajamarca: ~45 organizaciones
- Cusco (La Convención): ~40 organizaciones
- San Martín: ~35 organizaciones
- Amazonas: ~20 organizaciones
- Pasco, Ayacucho, Puno, Huánuco: ~35 organizaciones restantes

**Por nivel de datos disponibles:**

| Nivel | Descripción | Cantidad |
|-------|-------------|----------|
| **Alto** | Tiene GPS + contacto + año inicio operaciones | 177 orgs |
| **Medio** | Tiene contacto SUNAT (dirección fiscal) + año inscripción | 68 orgs |
| **Bajo** | Solo RUC validado + nombre | 0 orgs |

Ninguna organización tiene solo RUC. Incluso las 68 sin match en CENCOOP tienen al menos razón social, departamento y estado validado por SUNAT.

---

## 3. ¿Por qué las 83 orgs del CENCOOP 2017 que no exportan también son relevantes?

En el CENCOOP 2017 (SOPARSE) encontramos **160 organizaciones que mencionan "café", "cacao" o "cocoa" en su razón social**. De esas:

- **77 ya estaban en las 245** (y por tanto ya tienen datos de exportación o son proveedoras de exportadoras)
- **83 no estaban** en ninguna fuente administrativa de exportación

De esas 83, **ninguna aparece en PRODUCE, MIDAGRI ni PAC directo**. Esto significa que o bien:

a) Son cooperativas de café/cacao que operan **solo en el mercado interno** — venden a acopiadores locales o a intermediarios que sí exportan
b) Son cooperativas **tan pequeñas** que no alcanzan el umbral de registro en PRODUCE
c) Se constituyeron **después de 2017** y no fueron censadas de nuevo
d) Tienen un RUC diferente al que SUNAT les asignó post-2017

**¿Por qué importan para el ISCAM?** Porque aunque no exporten directamente, pueden estar en la **cadena de suministro** de un exportador que sí lo hace. El EUDR alcanza a todos los operadores de la cadena — no solo al exportador final. Una cooperativa que produce café orgánico y se lo vende a una exportadora está dentro del alcance del EUDR como "operador".

Por eso las 83 se mantienen en un archivo separado ("SOPARSE NO EXPORTADORAS") como **banco de organizaciones candidates** para verificar en campo.

**Total del universo extendido:** 245 + 83 = **328 organizaciones** con nombre, RUC y ubicación conocidas.

---

## 4. ¿Por qué estas organizaciones son realmente verificables?

Para que una organización sea incluidas en el Instrumento 2 del ISCAM necesita:

| Requisito ISCAM | Estado en la matriz |
|-----------------|-------------------|
| RUC vigente | ✅ 100% validado SUNAT |
| Ubicación (departamento) | ✅ 100% |
| Contacto (teléfono o correo) | ✅ 177 con contacto directo CENCOOP; resto con SUNAT |
| Producto (café o cacao) | ✅ Confirmado por keywords en al menos 2 fuentes |
| Capacidad exportar | ✅ 56 confirmadas por PRODUCE; resto por presencia en PAC/MIDAGRI |

Esto significa que para las **245 organizaciones del universo consolidado** tenemos lo mínimo necesario para **contactarlas, clasificarlas y aplicarles el Instrumento 2**. Las 56 exportadoras pueden priorizarse primero.

---

## 5. Lo que falta por verificar en campo

Ninguna fuente administrativa provee los datos del Instrumento 2 (D1-D7). Esto es esperado: el EUDR requiere información que solo se obtiene conversando con la organización.

| Dimensión ISCAM | Datos administrativos | Requiere campo |
|-----------------|----------------------|-----------------|
| D1 — Trazabilidad de lotes | ❌ | ✅ |
| D2 — Registro de productores | ❌ | ✅ |
| D3 — Deforestación | ❌ | ✅ |
| D4 — Manejo ambiental | ❌ | ✅ |
| D5 — Condiciones laborales | ❌ | ✅ |
| D6 — No infancia / trabajo forzado | ❌ | ✅ |
| D7 — Seguridad y salud | ❌ | ✅ |
| D8 — Años de operación / socios | ✅ 177 por CENCOOP; 68 por MIDAGRI | Parcial |
| D9 — Capacidad exportar | ✅ 56 por PRODUCE; resto por PAC | Parcial |
| D10 — Certificaciones | ✅ 35 de PAC directo | Parcial |
| D11 — Volumen FOB | ✅ 56 por PRODUCE | Solo exportadores |

---

## 6. Resumen ejecutivo

| Concepto | Cantidad |
|----------|----------|
| Universo consolidado (con RUC validado) | **245 orgs** |
| Con GPS y contacto directo (CENCOOP 2017) | **177 orgs** |
| Con operaciones de exportación confirmadas (PRODUCE) | **56 orgs** |
| Con al menos una certificación | **35 orgs** |
| Banco de orgs café/cacao no exportadoras (CENCOOP) | **83 orgs** |
| **Universo extendido total (con RUC y ubicación)** | **328 orgs** |

**El número "200+ cooperativas potencialmente verificables" es conservador.** Se sustenta en RUC validado al 100%, datos de contacto para 177 organizaciones, y ubicación geográfica conocida para la totalidad. Las 83 orgs del banco SOPARSE son candidatos adicionales que requieren verificación de campo antes de inclusión.

---

## 7. Fuentes utilizadas

| Fuente | Institucion | Contenido | Organizaciones |
|--------|-------------|-----------|----------------|
| PAC directo | Cepicafe / Norandino | Nombre, RUC, certificación, contacto | 48 |
| MIDAGRI | MIDAGRI Peru | Cooperativas agrarias inscritas | ~220 |
| PRODUCE | Produce Peru | Operaciones de exportacion 2024 | 56 |
| SUNAT | SUNAT | Validacion RUC, raz. social, estado | 245 |
| SOPARSE (CENCOOP 2017) | INESI / MINCETUR | GPS, contactos, constitucion, CIIU | 177 matched |
| Modelo ISCAM | Toolkit EUDR ISCAM | Instrumento 2 (76 preguntas, D1-D11) | 8 ejemplo |

**Archivos generados:**
- `MATRIZ_IP_IV_v5_EUDRPERU.xlsx` — Base maestra consolidada (6 hojas)
- `data/soparse_cencoop2017.csv` — CENCOOP 2017 exportado (1,965 orgs)
- `docs/ANALISIS_CRUCE_SOPARSE.html` — Informe visual del cruce
