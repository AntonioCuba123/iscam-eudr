# -*- coding: utf-8 -*-
"""Appendea al registro de cobertura el hito de la capa de ingesta + ítems [R]."""
import os, importlib.util, openpyxl
from datetime import date

ROOT = r"C:\Users\acuba\eudrperu"
MD = os.path.join(ROOT, "ISCAM", "DIAGNOSTICO_COBERTURA_INDICE.md")

sp = importlib.util.spec_from_file_location("cod", os.path.join(ROOT, "codificacion_instrumento2.py"))
cod = importlib.util.module_from_spec(sp); sp.loader.exec_module(cod)

REVISAR = ["D1.1", "D1.4", "D3.12", "D4.15", "D6.25b", "B0.8", "P10", "D7.28", "D7.28c",
           "D9.34", "PP1", "D10.36", "D10.37", "D11.38", "D11.39a"]

ws = openpyxl.load_workbook(os.path.join(ROOT, "PLANTILLA_INDICE_PVE_ISCAM.xlsx"),
                            data_only=True)["INSTRUMENTO_2_PREGUNTAS"]
enun = {}
for r in range(3, ws.max_row + 1):
    if ws.cell(r, 2).value:
        enun[ws.cell(r, 2).value] = (ws.cell(r, 4).value or "").replace("|", "/")

lines = []
lines.append("")
lines.append("---")
lines.append("")
lines.append(f"## Capa de ingesta del Instrumento 2 — implementada ({date.today().isoformat()})")
lines.append("")
lines.append("Con esto desaparece el único bloqueante del cálculo que quedaba (§5 del documento de "
             "metodología): los datos del instrumento ya tienen dónde cargarse y cómo convertirse en índice.")
lines.append("")
lines.append("Tres hojas nuevas en `PLANTILLA_INDICE_PVE_ISCAM.xlsx` (orden del libro: "
             "INSTRUCCIONES → INSTRUMENTO_2_PREGUNTAS → **CODIFICACION** → **CAPTURA** → **NORMALIZADO** "
             "→ ISCAM_Score → PONDERADORES → MATRIZ_174 → SCORECARDS → RADAR_BRECHAS):")
lines.append("")
lines.append("| Hoja | Rol | Contenido |")
lines.append("|---|---|---|")
lines.append("| `CODIFICACION` | Regla de conversión | 290 filas: cada opción de respuesta con su puntaje "
             "0-100 o «sin dato». Editable; marca `[R]` los ítems a ratificar. |")
lines.append("| `CAPTURA` | Entrada de datos | 174 cooperativas × 119 preguntas. RUC y razón social "
             "precargados. 63 listas desplegables, validación 0-4 y 0-100. Única hoja de escritura. |")
lines.append("| `NORMALIZADO` | Cálculo intermedio | 0-100 por pregunta (77 que puntúan) + agregado de las "
             "11 dimensiones D1-D11. Fórmulas, no se edita. |")
lines.append("")
lines.append("**Cableado del motor.** `ISCAM_Score!E:O` (D1-D11) ahora lee `NORMALIZADO`; `SCORECARDS!H:I:J` "
             "espeja D2/D5/D6; `MATRIZ_174!W:Z` (D12-D15) lee la captura conservando el valor previo como "
             "respaldo. D3 usa la encuesta y, si no hay respuesta, conserva la consulta OSCE/OEFA "
             "(`MATRIZ_174!U`). ISA-PV se blindó para tolerar componentes «sin dato» (antes `\"\"/100` daba "
             "`#VALUE!`). El panel de cobertura `ISCAM_Score!A182:C201` ya cuenta la captura real.")
lines.append("")
lines.append("**Probado de extremo a extremo.** Con respuestas sintéticas (mejor/peor caso) el índice "
             "calcula: mejor caso ISA-EUDR 99,2 / IP 92,5 / ISA-Completo 92,8; peor caso ISA-EUDR 5,9 / "
             "IP 4,7. Sin captura, todo sigue en «—»/«N/A» y `ISCAM_Score!AA4` (IV) conserva 60.")
lines.append("")
lines.append("### Ítems a ratificar (`[R]`) antes del levantamiento de campo")
lines.append("")
lines.append("La codificación categórica no estaba especificada en el documento de metodología; se propuso "
             "una interpretación (100 = mayor alineamiento con el EUDR). Estos 15 ítems tienen una decisión "
             "de dirección que conviene confirmar. La tabla es editable en la hoja `CODIFICACION`.")
lines.append("")
lines.append("| Ítem | Pregunta | Codificación propuesta |")
lines.append("|---|---|---|")
for q in REVISAR:
    t, v = cod.TABLA[q]
    if isinstance(v, list):
        codif = " · ".join(f"{o} = {'«sin dato»' if s is None else s}" for o, s in v)
    else:
        codif = {"C": f"casillas múltiples: n.º marcados ÷ {v}",
                 "Cn": f"casillas múltiples: n.º marcados ÷ {v}, «Ninguno» = 0",
                 "X": "casillas múltiples: % de destinos de la UE sobre el total marcado",
                 "N": "valor nativo 0-100", "E": "escala 0-4 ×25"}.get(t, str(v))
    e = enun.get(q, "")
    if len(e) > 130:
        e = e[:127] + "..."
    lines.append(f"| `{q}` | {e} | {codif} |")
lines.append("")
lines.append("> Nota: `[R]` es solo de ratificación de dirección, no un bloqueo. Aunque no se revise nada, el "
             "motor ya es coherente y reproducible; lo que cambia con la ratificación es el puntaje de esos "
             "ítems, no la arquitectura.")
lines.append("")

with open(MD, "a", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("registro actualizado:", MD)
print("ítems [R]:", len(REVISAR))
