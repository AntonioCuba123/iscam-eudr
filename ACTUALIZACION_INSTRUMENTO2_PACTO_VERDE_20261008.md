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