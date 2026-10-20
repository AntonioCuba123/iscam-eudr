# -*- coding: utf-8 -*-
"""Registra la re-ponderación de ISA-PV y la observación de ceros-fórmula."""
import os
from datetime import date

MD = r"C:\Users\acuba\eudrperu\ISCAM\DIAGNOSTICO_COBERTURA_INDICE.md"

lines = ["", "---", "",
         f"## ISA-PV re-ponderada sobre componentes presentes ({date.today().isoformat()})", "",
         "Cambio pedido: que ISA-PV use la misma regla que ISA-EUDR. Implementado en `MATRIZ_174!AP`.", "",
         "| | Antes | Ahora |", "|---|---|---|",
         "| Fórmula | `Σ(wᵢ·vᵢ) ÷ 100` | `Σ(wᵢ·vᵢ) ÷ Σwᵢ` (solo componentes con dato) |",
         "| Componente sin dato | contaba como 0 | se excluye y se re-normaliza |",
         "| PPWR (w=4) | 0 en numerador, 4 en denominador | excluido (sin fuente aún), reportado en `AQ` |",
         "| Fila 3 (ejemplo) | 0,125 | 0,260 |", "",
         "Efecto en las 174 organizaciones: media 0,060 (PVE promedio 6/100); 125 en 0 porque sus "
         "componentes presentes valen 0. `AQ` (cobertura) usa ahora el mismo criterio de presencia que la "
         "fórmula, para que el conteo y el cálculo no se contradigan. Documentado en la §2.4 del documento y "
         "en `PONDERADORES!B29`.", "",
         "### Observación abierta (no bloquea)", "",
         "La re-ponderación excluye bien lo que está en blanco, pero dos componentes siguen entrando como 0 "
         "porque en `MATRIZ_174` son **ceros de fórmula**, no celdas vacías:", "",
         "- `M3` (% UE/FOB) = `IF(E3>0, ROUND(L3/E3*100,1), 0)` → 138 de 174 organizaciones quedan en 0 por "
         "falta de FOB, no por exportar 0 a la UE.",
         "- `O` (score de certificación) = 0 para 171 de 174.",
         "",
         "Mientras esos dos sigan devolviendo 0 en lugar de «sin dato», ISA-PV subestima a las organizaciones "
         "sin dato de comercio exterior o de certificación. Corregirlo implica tocar `M3` y `O` (y con ello "
         "IV1 y el resto de `MATRIZ_174`), así que se deja como decisión aparte.", ""]

with open(MD, "a", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("registro actualizado")
