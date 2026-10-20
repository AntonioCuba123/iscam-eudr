# Actualización Instrumento 2 — Inclusión de Módulos Pacto Verde (D12–D14)

**Fecha:** 2026-10-08  
**Motivo:** Revertir exclusión de módulos (i) huella de carbono, (iv) reporte de sostenibilidad, (v) economía circular/envases del proyecto madre ISCAM.

---

## Resumen de cambios

### 1. Instrumento 2 — Encuesta Cuantitativa (`Instrumentos/Instrumento 2 - Encuesta Cuantitativa.md`)

**Nuevas dimensiones agregadas:**

| Dimensión | Módulo Pacto Verde | Preguntas | Tema |
|---|---|---|---|
| **D12** | (i) Huella de carbono | 5 (40–44) | CalCafé v2.1, registros insumos, cálculo huella, objetivo reducción, reporte a compradores |
| **D13** | (iv) Reporte sostenibilidad | 6 (45–50) | Reporte anual (GRI/ESRS), indicadores ESG, verificación externa, difusión proactiva |
| **D14** | (v) Economía circular/envases | 5 (51–55) | Residuos beneficio, envases exportación, plásticos un solo uso, subproductos valorizados, trazabilidad envases/residuos |

**Total preguntas:** 80 (antes 76)  
**Escala:** 0–4 en todas (igual que D1–D11)  
**Puntaje:** D12–D14 **no promedian en ISA-EUDR**; sí promedian en **ISA-PactoVerde** (media aritmética simple).

---

### 2. Ficha Técnica (`Instrumentos/Ficha Tecnica y Guia de Aplicacion - Instrumento 2.md`)

- Estructura actualizada: Bloque 0 (12) + Bloque P (13) + D1–D11 (51) + **D12–D14 (16) = 80 preguntas**
- Informantes por módulo Pacto Verde:
  - D12: gerencia + responsable técnico/calidad
  - D13: gerencia + comunicación/transparencia
  - D14: gerencia + operaciones/beneficio
- Duración estimada: +15 min por módulos Pacto Verde

---

### 3. Metodología ISA (`ISCAM/Metodologia - Indice de Alineamiento (ISA) y Marco Muestral.md`)

**Nueva arquitectura de tres índices:**

```
ISA-EUDR (D1–D9)          → 70% del ISA-Completo
  Núcleo (D1–D7): media geométrica → 87.5%
  Extendido (D8–D9): media aritmética → 12.5%

ISA-PactoVerde (D12–D14)  → 30% del ISA-Completo
  D12: Huella carbono (CalCafé v2.1 café; brecha cacao)
  D13: Reporte sostenibilidad (CSRD/ESRS/taxonomía)
  D14: Economía circular/envases (PPWR)

ISA-Completo = 0.70 × ISA-EUDR + 0.30 × ISA-PactoVerde
```

**Reglas de datos faltantes separadas:**
- ISA-EUDR: ≥7 de 9 dimensiones D1–D9 con ≥70% respondido
- ISA-PactoVerde: ≥2 de 3 dimensiones D12–D14 con ≥70% respondido
- ISA-Completo: requiere ambos sub-índices calculables

**Validación robustez actualizada:**
- PCA sobre D1–D14 (antes D1–D9)
- Sensibilidad al peso 70/30 (alternativas: 80/20, 60/40, 50/50)
- Bootstrap sobre ISA-EUDR, ISA-PactoVerde, ISA-Completo

---

### 4. Instrumento 7 — Evaluación Crítica (`Instrumentos/Instrumento 7 - Evaluacion Critica y Elementos Adicionales.md`)

- **Huella de carbono (D12):** actualizado de "descartado" a **incluido como módulo Pacto Verde i** (CalCafé v2.1 para café; brecha cacao documentada). Preguntas de agua/residuales (D3.14a/14b) permanecen en D3.
- **D13 (Reporte sostenibilidad):** nuevo — módulo Pacto Verde iv (CSRD/ESRS/taxonomía)
- **D14 (Economía circular):** nuevo — módulo Pacto Verde v (PPWR, estrategia "granja a mesa")
- Implementación digital: **14 dimensiones** (D1–D14) con ISA-Completo (70/30)

---

## Justificación del peso 70/30

| Factor | Peso | Razón |
|---|---|---|
| **ISA-EUDR (70%)** | Acceso al mercado UE | El Reglamento 2023/1115 decide si el producto entra o no; D1–D9 miden cumplimiento textual |
| **ISA-PactoVerde (30%)** | Competitividad largo plazo | Módulos i, iv, v no deciden acceso inmediato pero determinan resiliencia, acceso a financiamiento verde, preferencia de compradores, alineación CSRD/CBAM/taxonomía |

*Pesos a validar en piloto (§4 Metodología ISA — análisis de sensibilidad).*

---

## Herramientas de referencia por módulo

| Módulo | Herramienta | Estado |
|---|---|---|
| **(i) Huella carbono** | CalCafé v2.1 (PromPerú/PUCP-PELCAN, ISO 14040/44, PEFCR) | ✅ Café validado, gratuito, público — **brecha: no cubre cacao** |
| **(iv) Reporte sostenibilidad** | GRI, ESRS simplificado, taxonomía UE | Marco de referencia, no herramienta de cálculo |
| **(v) Economía circular** | Plan Acción Economía Circular UE, PPWR (Directiva envases) | Marco normativo, no herramienta de cálculo |

---

## Impacto en el toolkit

| Componente | Impacto |
|---|---|
| **Instrumento 1 (Marco Dimensiones)** | Debe actualizarse a 14 dimensiones (D1–D14) en próxima revisión |
| **Instrumento 3 (Entrevista Semiestructurada)** | Agregar guía para D12–D14 (entrevista a gerencia/técnico) |
| **Instrumento 4 (Brújula de Diligencia)** | Panel extendido: semáforo D12–D14 + ISA-PactoVerde + ISA-Completo |
| **Instrumento 5 (Triaje)** | Decidir si aplica diagnóstico completo (D1–D14) o solo EUDR (D1–D9) |
| **Instrumento 6 (Aplicación)** | Informantes adicionales para D12–D14 |
| **Encuesta Productor (Google Forms)** | No cambia — D12–D14 son a nivel cooperativa, no productor |
| **Puente (Mapeo)** | D12–D14 no tienen correspondencia en formulario productor; requieren Instrumento 2 directo |

---

## Próximos pasos (Checklist)

- [ ] Actualizar `Instrumento 1 - Marco de Dimensiones de Diagnostico.md` a 14 dimensiones
- [ ] Actualizar `Instrumento 3 - Guia de Entrevista Semiestructurada.md` con bloques D12–D14
- [ ] Actualizar `Instrumento 4 - Matriz de Riesgo y Brújula de Diligencia.md` (panel 14 dims + ISA-Completo)
- [ ] Actualizar `Instrumento 5 - Triaje de Organizaciones.md` (criterio diagnóstico completo vs. EUDR-only)
- [ ] Actualizar `Instrumento 6 - Nota Metodologica de Aplicacion.md` (informantes D12–D14)
- [ ] Actualizar `Scripts/matriz_data.py` (esquema columnas D12–D14 + fórmulas ISA-Completo)
- [ ] Actualizar `Estructura Google Sheet - Respuestas Instrumento 2.md` (80 columnas)
- [ ] Pilotear Instrumento 2 v3 (con D12–D14) en 5–8 cooperativas (§1.1 Metodología ISA)
- [ ] Validar pesos 70/30 y CalCafé v2.1 con equipo ISCAM (Tarea D1)

---

## Referencias normativas clave

- **EUDR:** Reglamento (UE) 2023/1115 mod. 2025/2650 + Guía C(2026) 3896
- **Pacto Verde módulo (i):** Taxonomía UE, CSRD, CBAM, CalCafé v2.1 (PromPerú)
- **Pacto Verde módulo (iv):** CSRD/ESRS, Taxonomía Verde, SFDR
- **Pacto Verde módulo (v):** Plan Acción Economía Circular UE 2020, PPWR (Reglamento envases), Estrategia "De la granja a la mesa"
- **Validación externa:** Documento Orientador ADEX/MIDAGRI/MINCETUR/GIZ/EFI 2026 (RM 0128-2025-MIDAGRI)

---

*Documento generado automáticamente tras actualización 2026-10-08. Verificar consistencia cruzada entre los 4 archivos modificados antes de piloto.*

---

# Actualización Instrumento 2 — Cierre de sesgo Pacto Verde café/cacao (D15 + ajustes)

**Fecha:** 2026-10-09
**Motivo:** corregir tres sesgos identificados en análisis de cobertura: (1) D12 anclado a CalCafé/solo café, (2) D13 sin escala intermedia adaptada al universo objetivo, (3) pilares Pacto Verde ausentes — Farm to Fork/LMR es la brecha de mayor impacto operativo sin dimensión propia.

---

## Resumen de cambios

### 1. Instrumento 2 — Encuesta Cuantitativa (`Instrumentos/Instrumento 2 - Encuesta Cuantitativa.md`)

**Renombrado:** D1–D11 + Desempeño → **D1–D15 + Desempeño** | v0.2

| Cambio | Tipo | Q afectadas |
|---|---|---|
| Encabezado: actualizado a D1–D15, total 89 preguntas | Editorial | — |
| **D7 — nueva Q28b** presión CSDDD del comprador | Pregunta nueva | Q28b |
| **D12 — Q40 reformulada** producto-neutral (café y cacao sin sesgo CalCafé-only) | Modificación | Q40 |
| **D12 — Encabezado** actualizado: herramienta por producto, instrucción cacao | Aclaración editorial | — |
| **D13 — nueva Q44b** escala de entrada nivel 0→1 | Pregunta nueva | Q44b |
| **D15 (nueva)** Gestión fitosanitaria y LMR — módulo Pacto Verde vi, Farm to Fork | Dimensión nueva | Q56–Q60 |
| **Bloque P v0.2** — P13 (exigencias PV del comprador) y P14 (financiamiento verde) | Preguntas nuevas | P13, P14 |
| **Nota de puntaje** actualizada: D12–D15 entran a ISA-PactoVerde; Q60 es bandera | Editorial | — |

**Total preguntas:** 89 (antes 80: +1 Q28b D7, +1 Q44b D13, +5 D15, +2 P13/P14)

### 2. Instrumento 1 — Marco de Dimensiones (`Instrumentos/Instrumento 1 - Marco de Dimensiones de Diagnostico.md`)

- Tabla módulos Pacto Verde: añadida fila **D15** (Gestión fitosanitaria y LMR, módulo vi, RASFF/Directiva 2009/128/CE/Farm to Fork)
- Scoring diferenciado: `ISA-PactoVerde = (D12 + D13 + D14 + D15) / 4`
- Cómo se usa: referencias actualizadas a D1–D15 y D12–D15

### 3. Metodología ISA (`ISCAM/Metodologia - Indice de Alineamiento (ISA) y Marco Muestral.md`)

- Alcance actualizado a 2026-10-09: módulo (vi) Farm to Fork, D15
- ISA-PactoVerde: fórmula actualizada a 4 módulos `(D12 + D13 + D14 + D15) / 4`
- Umbral mínimo ISA-PactoVerde: ≥3 de 4 dimensiones (antes ≥2 de 3)
- Q60 D15 declarada bandera independiente (no entra al promedio)
- PCA y Cronbach: actualizados a D1–D15
- Informantes: D15 = gerencia + responsable técnico de campo

---

## Nueva arquitectura ISA-PactoVerde

```
ISA-PactoVerde (módulos i + iv + v + vi)
  D12: Huella de carbono — módulo (i)
  D13: Reporte de sostenibilidad — módulo (iv)
  D14: Economía circular/envases — módulo (v)
  D15: Fitosanitarios/LMR — módulo (vi) Farm to Fork ← NUEVO

ISA_PactoVerde_i = (D12_i + D13_i + D14_i + D15_i) / 4

ISA_Completo_i = 0.70 × ISA_EUDR_i + 0.30 × ISA_PactoVerde_i
```

---

## Justificación de D15 vs. no-dimensión

| Factor | Decisión |
|---|---|
| ¿Afecta acceso al mercado UE directamente? | **Sí** — rechazo en frontera por LMR tiene el mismo efecto que rechazo por deforestación |
| ¿Encaja en D1–D9 existentes? | No — LMR no es legalidad peruana (D3) ni posición en cadena de valor (D7) |
| ¿Aplica por igual a café y cacao? | **Sí** — elimina el sesgo café/cacao de D12 (CalCafé) |
| ¿Tiene referente normativo UE claro? | **Sí** — Directiva 2009/128/CE, RASFF, Farm to Fork -50% pesticidas 2030 |
| ¿Por qué no entra al ISA-EUDR? | El reglamento 2023/1115 no regula residuos de pesticidas; va al ISA-PactoVerde como competitividad de largo plazo |

---

## Pilares del Pacto Verde — estado de cobertura post-actualización

| Pilar | Normativa UE principal | Cobertura en instrumento |
|---|---|---|
| (i) Huella de carbono / GEI | Taxonomía UE, CSRD, CBAM | ✅ D12 (producto-neutral desde 2026-10-09) |
| (ii) Deforestación / trazabilidad | EUDR 2023/1115 | ✅ D1–D7 núcleo |
| (iii) Diligencia debida DD.HH./ambiente | EUDR Art. 2(40) | ✅ D1–D9, D3 completo |
| (iv) Reporte de sostenibilidad | CSRD/ESRS, taxonomía | ✅ D13 (con Q44b escala intermedia) |
| (v) Economía circular / envases | PPWR, Plan EC UE 2020 | ✅ D14 |
| (vi) Farm to Fork / LMR pesticidas | Directiva 2009/128/CE, RASFF | ✅ **D15 (nuevo 2026-10-09)** |
| CSDDD (presión del comprador) | Directiva 2024/1760/UE | ✅ D7.Q28b (captura traslado contractual) |
| Financiamiento verde / taxonomía | Taxonomía UE, SFDR | ✅ P14 (variable de resultado) |
| Biodiversidad | Regl. Restauración Naturaleza 2024 | ⚠️ Cubierta en encuesta productores Q55; sin peso en ISA. Decisión de alcance documentada. |
| CBAM | Regl. (UE) 2023/956 | ❌ No aplica a café/cacao (sectores cubiertos: acero, cemento, electricidad, fertilizantes, aluminio, hidrógeno) |

---

## Próximos pasos (Lista de verificación — post 2026-10-09)

- [ ] Actualizar `Instrumentos/Ficha Tecnica y Guia de Aplicacion - Instrumento 2.md` (estructura: 89 preguntas, informante D15)
- [ ] Actualizar `Instrumentos/Instrumento 3 - Guia de Entrevista Semiestructurada.md` con bloque D15
- [ ] Actualizar `Instrumentos/Instrumento 4 - Matriz de Brechas y Oportunidades.md` (semáforo D15, fila en matriz)
- [ ] Actualizar `Instrumentos/Instrumento 5 - Ficha de Triaje Rapido.md` (¿D15 como criterio de alerta en triaje?)
- [ ] Actualizar `Instrumentos/Instrumento 7 - Evaluacion Critica y Elementos Adicionales.md` §3 (D15 justificación) y §5 (implementación digital 15 dimensiones)
- [ ] Actualizar `Scripts/matriz_data.py` (esquema columnas D15 Q56–Q60, fórmulas ISA-PactoVerde 4 módulos)
- [ ] Actualizar `Instrumentos/Estructura Google Sheet - Respuestas Instrumento 2.md` (89 columnas)
- [ ] Pilotear Q56–Q60 (D15) y Q28b, Q44b, P13, P14 en 5–8 cooperativas — verificar comprensibilidad y tasa de respuesta

---

*Documento actualizado 2026-10-09. Verificar consistencia entre los 4 archivos modificados (Instrumento 2, Instrumento 1, Metodología ISA, este documento) antes del piloto.*
