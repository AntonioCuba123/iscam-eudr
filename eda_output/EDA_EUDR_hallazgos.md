# EDA EUDR — Cooperativas Café Perú
*Generado: 2026-09-17 14:55 · Proyecto eudrperu*

---

## 1. Resumen de Datos

| Archivo | Descripción | Registros | Columnas | Tasa Llenado |
|---------|-------------|-----------|----------|-------------|
| 1 | Directorio PAC Café 2018–2025 | 673 | 115 | ~84% |
| 2 | Directorio PAC Mango/Banano | 6 | 31 | ~86% |
| 3 | Perfil Cooperativas San Martín (EUDR) | 25 | 49 | ~87% |

---

## 2. Hallazgos Clave

### Archivo 1 — Directorio PAC Café (673 organizaciones)

**Cobertura geográfica:** 25 departamentos. Los 5 principales son:
- **CUSCO**: 66 orgs
- **JUNIN**: 57 orgs
- **PUNO**: 37 orgs
- **HUANUCO**: 36 orgs
- **CAJAMARCA**: 35 orgs

**Productos:** 96 categorías detectadas. Principales:
- **CACAO**: 87 orgs
- **CAFÉ**: 72 orgs
- **PALTA**: 53 orgs
- **FIBRA DE ALPACA**: 45 orgs

**Tipos de organización:**
- **01 Asociación**: 394
- **02 Cooperativa**: 224
- **07 Otros**: 17
- **05 Comunidades Campesinas**: 15

**Ventas acumuladas 2018–2025:** S/ 175,409 en 8 años con dato.
- El año con mayor venta agregada: 2025 (S/ 26,942)
- NOTA: varias celdas contienen `#REF!` (fórmulas Excel rotas al exportar) — estos valores están excluidos.

**Beneficiarios acumulados:** ~175,409 en 8 años con dato.

---

### Archivo 3 — Perfil Cooperativas San Martín (25 organizaciones)

**Escala:** ~5,590 socios varones + ~1,990 socias = ~7,580 productores en 25 cooperativas.

**Superficie:** ~21,235 hectáreas total.

**Volumen cosecha 2026:** ~136,505 qq de café verde estimado.

**Exportaciones FOB 2025:** $33,926,205 USD
- Tasa de exportación: 13/25 (52%)

**Certificaciones vigentes (de 25 orgs):**
- **Orgánica**: 24 (96%)
- **Fair Trade**: 24 (96%)

**Mercados de destino:** Estados Unidos, Belgica, Alemania, Suecia, Francia

**EUDR:** 17 de 25 cooperativas registran avance EUDR. Promedio: 0.79/1.0

---

## 3. Problemas de Calidad de Datos

1. **Archivo 1 — Celdas `#REF!`:** Fórmulas Excel que referencian celdas movidas/eliminadas. Afectan columnas de ventas incrementales. Se recomienda recalcular o reimportar desde la fuente.
2. **Archivo 1 — Headers multilínea:** Las columnas de beneficiarios están en filas de encabezado intermedias (merge vertical de celdas), lo que requiere lógica de limpieza especial.
3. **Archivo 2 — Solo 6 registros:** El directorio mango/banano está casi vacío. Útil como muestra piloto pero no representativo.
4. **Archivo 3 — Texto libre mezclado:** Las columnas de certificaciones, calidad y EUDR contienen texto narrativo, no valores estructurados. Se requiere procesamiento de texto (NLP) para extraer datos estructurados.
5. **Archivo 3 — Formatos numéricos inconsistentes:** Algunos campos numéricos usan comas como separadores de miles (estilo peruano). Se limpian correctamente en el análisis pero indican inconsistencia en la fuente.

---

## 4. Visualizaciones Generadas

| # | Gráfico | Archivo fuente |
|---|---------|---------------|
| v01 | Deptos PAC | A1 |
| v02 | Tipos organización | A1 |
| v03 | Ventas anuales | A1 |
| v04 | Beneficiarios anuales | A1 |
| v05 | Productos principales | A1 |
| v06 | Heatmap productos × deptos | A1 |
| v07 | Distribución socios | A3 |
| v08 | Hectáreas vs volumen | A3 |
| v09 | Certificaciones | A3 |
| v10 | FOB exportaciones | A3 |
| v11 | Mercados destino | A3 |
| v12 | Avance EUDR | A3 |
