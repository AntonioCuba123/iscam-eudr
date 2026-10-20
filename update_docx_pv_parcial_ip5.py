# -*- coding: utf-8 -*-
"""
Actualiza el documento de metodología (2026-10-15) con dos correcciones:

  1. ISA-PactoVerde por debajo del umbral ya no queda en «—»: se reporta el valor
     re-ponderado sobre los componentes con dato, etiquetado como PROVISIONAL
     («◐ Parcial · n/7»), sin veredicto de color hasta que la medición sea completa.
  2. IP5 (Mercado y riesgo) mezclaba escalas: sumaba D7 y D9 (0–100) con el score de
     certificación (0–1); ahora la certificación entra ×100.

Toca §2.4 (párrafos 56, 58, 60), el pendiente de IV/IP (párrafo 88), una tabla de
fórmulas (IP5 e ISA-PV), la tabla de decisiones (dato faltante) y agrega un hito en §5.
"""
import os, copy, datetime, shutil
import docx
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

ROOT = r"C:\Users\acuba\eudrperu"
DOC = os.path.join(ROOT, "ISCAM", "Metodologia - Instrumento 2 e Indice ISCAM.docx")
ts = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
bak = os.path.join(ROOT, "ISCAM", "respaldos", f"Metodologia - Instrumento 2 e Indice ISCAM.backup_{ts}_pre-pv-parcial-ip5.docx")
shutil.copy2(DOC, bak); print("respaldo:", bak)

d = docx.Document(DOC)


def set_text(par, text):
    """Reemplaza el texto conservando el formato del primer run (Arial 11)."""
    if not par.runs:
        par.add_run()
    first = par.runs[0]
    for r in par.runs[1:]:
        r._element.getparent().remove(r._element)
    first.text = text
    if first.font.name is None:
        first.font.name = "Arial"
    if first.font.size is None:
        first.font.size = Pt(11)
    return par


P56 = ("Umbral mínimo ISA-PactoVerde: 3 de las 4 dimensiones Pacto Verde (D12–D15) con dato. "
       "Por debajo del umbral, ISA-PactoVerde no se deja en blanco: se computa igual sobre los "
       "componentes que sí tienen dato, re-normalizando los pesos, y el valor se reporta como "
       "PROVISIONAL, con la etiqueta «◐ Parcial · n/7» en la matriz (columnas T y AT, donde n es el "
       "número de los siete componentes con dato). El veredicto de clasificación (🔴/🟡/🟢) se "
       "reserva para la medición completa —los siete componentes con dato y el umbral Pacto Verde "
       "cumplido—, porque un color sobre una base parcial sería una medición falsa. «—» queda sólo "
       "para las organizaciones sin ningún componente con dato. El umbral se evalúa sobre la "
       "captura (hoja NORMALIZADO), no sobre el proxy precensal.")

P58 = ("Regla operativa en la hoja de cálculo (2026-10-15): sin dato se muestra como «—» y nunca "
       "como 0. El semáforo de las scorecards indica «— Sin Inst.2», la clasificación del PVE indica "
       "«⬜ Sin dato PVE» cuando la organización no tiene ningún componente con dato, y la tipología "
       "«⬜ Pendiente de instrumento» mientras el Instrumento 2 no se levante. La ausencia de dato no "
       "se convierte en una medición: no implica cumplimiento, pero tampoco debe leerse como "
       "incumplimiento. El panel de cobertura por dimensión está en ISCAM_Score (a partir de la fila 182).")

P60 = ("Regla sobre la base precensal (MATRIZ_174, 2026-10-15): los ceros que provenían de la falta "
       "de dato ya no se muestran como 0. La certificación se recodificó a SI/NO tomando el texto "
       "fuente —venía truncada a tres caracteres por el generador de la matriz—, y el score de "
       "certificación, el % UE/FOB, el FOB total y el de la Unión Europea, los indicadores P1–P14 y "
       "las dimensiones D12–D15 aparecen vacíos cuando falta la fuente. En D12–D15 se conserva "
       "únicamente el proxy FAO/IPCC documentado de la huella de carbono, calculado sobre las "
       "hectáreas conocidas; el resto de ceros era relleno del generador y se vació. Un cero medido "
       "—por ejemplo, una organización que exporta pero no a la Unión Europea— se conserva. Los "
       "índices derivados (IV1, IV4 e IP5) quedan sin dato cuando su insumo lo está. Los cuatro casos "
       "de Comercio Justo que quedaban en revisión se resolvieron en la misma pasada: en tres de ellos "
       "la celda de origen contenía texto de certificación orgánica —no hay evidencia de Comercio "
       "Justo— y se mantienen en «sin dato»; el cuarto, AGUILAYOC, se recodificó a SI con la fuente "
       "del directorio de la JNC («Orgánica y Comercio Justo»).")

P88 = (d.paragraphs[88].text + " IP5 quedó además corregido de escala: sumaba D7 y D9 (0–100) con la "
       "certificación en 0–1; la certificación entra ahora multiplicada por 100, de modo que las tres "
       "componentes están en la misma escala 0–100.")

NUEVO = ("ISA-PactoVerde provisional (2026-10-15). Por debajo del umbral Pacto Verde, ISA-PactoVerde "
         "ya no se deja en «—»: se reporta el valor re-ponderado sobre sus componentes con dato y se "
         "etiqueta como parcial (MATRIZ_174, columnas AT y T; el mismo estado viaja al motor en "
         "ISCAM_Score, columna AM). Con la captura todavía vacía, 61 de las 174 organizaciones tienen "
         "algún componente con dato y su valor es provisional; las 113 restantes quedan en «sin dato». "
         "Al levantar el Instrumento 2 el umbral se cumple y las etiquetas parciales desaparecen.")

set_text(d.paragraphs[56], P56)
set_text(d.paragraphs[58], P58)
set_text(d.paragraphs[60], P60)
set_text(d.paragraphs[88], P88)

# hito nuevo en §5, insertado justo después del hito de ratificación (párrafo 85),
# copiando el formato de lista del párrafo 86 (numId 2) para conservar la numeración.
src = d.paragraphs[85]
modelo = d.paragraphs[86]
nuevo_p = copy.deepcopy(modelo._p)
for r in list(nuevo_p.findall(qn('w:r'))):
    nuevo_p.remove(r)
src._p.addnext(nuevo_p)
np = Paragraph(nuevo_p, src._parent)
np.add_run(NUEVO)
set_text(np, NUEVO)

# ── tabla de fórmulas (T1) ───────────────────────────────────────────────────
T1 = d.tables[1]
set_text(T1.rows[6].cells[1].paragraphs[0],
         "= (D7 + D9 + Certificación) / 3, con la certificación llevada a 0–100 "
         "(el score 0–1 se multiplica por 100) para que las tres componentes compartan escala")
set_text(T1.rows[17].cells[1].paragraphs[0],
         "= EXP_UE×20% + TRAZA×16% + DILIG×12% + CAPAC×8% + PRESION×12% + CERTIF×8% + PPWR×4% + "
         "AMBIENTAL(D12-D15)×20% — pesos en PONDERADORES, escala 0–1. Por debajo del umbral Pacto "
         "Verde (3 de 4 D12–D15 con dato) se reporta como valor PROVISIONAL sobre los componentes "
         "con dato, etiquetado «◐ Parcial · n/7», sin veredicto de color")

# ── tabla de decisiones (T3) : excepción declarada de ISA-PV ─────────────────
T3 = d.tables[3]
set_text(T3.rows[5].cells[1].paragraphs[0],
         "Sin dato se muestra «—» (nunca 0). ISA-EUDR, IP, RE, ISA-Completo, el promedio del radar y "
         "los semáforos quedan sin dato; la tipología pasa a «⬜ Pendiente de instrumento». ISA-PV es "
         "la única excepción declarada: por debajo de su umbral no queda en «—» sino en un valor "
         "provisional etiquetado «parcial · n/7».")

d.save(DOC)
print("OK — documento actualizado:", len(d.paragraphs), "párrafos /", len(d.tables), "tablas")
