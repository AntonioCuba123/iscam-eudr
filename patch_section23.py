with open('ISCAM/Metodologia - Indice de Alineamiento (ISA) y Marco Muestral.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the exact section
idx = content.find('### 2.3 Ponderación y agregación')
end_idx = content.find('### 2.4 Reglas de datos faltantes')
old_section = content[idx:end_idx]

new_section = """### 2.3 Ponderación y agregación

**ISA-EUDR (D1–D9) — Pesos (a validar con el piloto, ver §4 — análisis de sensibilidad):**

- **D1–D7 (dimensiones núcleo, derivadas directamente del texto del reglamento):** peso igual entre sí → 87.5% del ISA-EUDR.
- **D8–D9 (dimensiones extendidas — gobernanza y sostenibilidad económica):** peso igual entre sí → 12.5% del ISA-EUDR.

**Regla de agregación — corregida el 2026-09-16, de aritmética a geométrica híbrida.** La versión anterior de este documento promediaba D1–D9 con una media aritmética ponderada. Eso permite **sustitución perfecta** entre dimensiones: una cooperativa con D2 (trazabilidad) en 4 pero D5 (diligencia debida) en 0 saldría con un ISA "aceptable" a pesar de no tener ningún sistema de diligencia debida — exactamente el tipo de brecha crítica que el Instrumento 4 necesita ver, no esconder. El precedente que corrige esto es el propio **Índice de Desarrollo Humano del PNUD**: hasta 2009 usaba media aritmética; desde el *Informe de Desarrollo Humano 2010* usa **media geométrica**, documentando que penaliza el desbalance entre dimensiones porque estas no son sustitutos entre sí. Las dimensiones EUDR tampoco lo son: el reglamento no permite compensar la ausencia de diligencia debida con buena geolocalización.

Con la salvedad de que la media geométrica exige valores > 0 (un cero anula el producto completo — deseable en D1–D7, excesivo en D8–D9, que son moduladoras y no deberían anular el índice por sí solas), se agrega en dos niveles:

```
Núcleo_i     = ( Π (D1_i × D2_i × D3_i × D4_i × D5_i × D6_i × D7_i) )^(1/7)      [media geométrica, D1–D7, cada Dim_d,i en 0–100]
Extendido_i  = (D8_i + D9_i) / 2                                                [media aritmética, D8–D9]

ISA_EUDR_i = 0.875 × Núcleo_i + 0.125 × Extendido_i
```

**ISA-PactoVerde (D12–D14) — Agregación aritmética simple (módulos i, iv, v son complementarios, no sustitutos estrictos):**

```
D12_i = promedio preguntas D12 (0–100)
D13_i = promedio preguntas D13 (0–100)
D14_i = promedio preguntas D14 (0–100)

ISA_PactoVerde_i = (D12_i + D13_i + D14_i) / 3
```

**ISA-Completo:**

```
ISA_Completo_i = 0.70 × ISA_EUDR_i + 0.30 × ISA_PactoVerde_i
```

**Justificación del esquema de pesos entre bloques:** las dimensiones núcleo EUDR determinan directamente el acceso al mercado (lo que el reglamento exige textualmente); las extendidas EUDR (D8–D9) son moduladoras de sostenibilidad del cumplimiento en el tiempo (Instrumento 7, §2). Los tres módulos PactoVerde (D12–D14) son complementarios entre sí (huella de carbono informa el reporte, la circularidad reduce la huella) y no anulan el acceso al mercado por sí solos — por eso media aritmética entre ellos y peso 30% en el compuesto final. El esquema de pesos iguales *dentro* de cada bloque sigue siendo el default recomendado por el OECD/JRC Handbook en ausencia de un proceso de consenso de expertos (Delphi, o Analytic Hierarchy Process de Saaty) — no se recomienda un esquema de pesos "de experto" sin esa validación, que hoy no existe en el proyecto. Una vez haya datos reales del piloto, correr un **Análisis de Componentes Principales (PCA)** sobre D1–D14 como chequeo de robustez (§4): si el primer componente explica una fracción alta de la varianza, los pesos iguales son razonables; si dos dimensiones aparecen altamente correlacionadas, están sobre-representando un mismo fenómeno en el índice y el esquema debe ajustarse."""

if old_section in content:
    content = content.replace(old_section, new_section)
    with open('ISCAM/Metodologia - Indice de Alineamiento (ISA) y Marco Muestral.md', 'w', encoding='utf-8') as f:
        f.write(content)
    print('SUCCESS!')
else:
    print('MISMATCH - checking...')
    for i, (a, b) in enumerate(zip(old_section, content[idx:idx+len(old_section)])):
        if a != b:
            print(f'Diff at {i}: old={repr(a)} new={repr(b)}')
            print(f'Context old: {repr(old_section[max(0,i-20):i+20])}')
            print(f'Context new: {repr(content[idx+max(0,i-20):idx+i+20])}')
            break