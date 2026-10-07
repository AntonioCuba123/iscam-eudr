"""Regenera el .docx de la Matriz de Cobertura Tecnica - Instrumento 2.

El .md es la fuente editable; el .docx se produce siempre desde el, de modo que
no se editen a mano. Preserva el formato del documento anterior: horizontal,
tabla con borde, encabezados en negrita y la fila de estado al pie.
"""
import os
import re

import docx
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, Inches

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(RAIZ, "Instrumentos",
                  "Matriz de Cobertura Tecnica - Instrumento 2.md")
DOCX = os.path.join(RAIZ, "Instrumentos",
                    "Matriz de Cobertura Tecnica - Instrumento 2.docx")

TITULO = ("MATRIZ DE COBERTURA TÉCNICA — INSTRUMENTO 2 "
          "(NIVEL DE PREGUNTA, RUTA IP/IV SEPARADA)")


def clean(s):
    """Quita el marcado de Markdown que no tiene equivalente en Word."""
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)          # negrita
    s = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"\1", s)  # cursiva
    s = re.sub(r"`(.+?)`", r"\1", s)                # codigo
    return s.strip()


def leer_tabla(md):
    filas = []
    for linea in md.splitlines():
        t = linea.strip()
        if not t.startswith("|"):
            continue
        celdas = [clean(c) for c in t.strip("|").split("|")]
        if all(set(c) <= set("-: ") for c in celdas):   # separador
            continue
        filas.append(celdas)
    return filas


def main():
    with open(MD, encoding="utf-8") as fh:
        md = fh.read()
    filas = leer_tabla(md)
    encabezado, datos = filas[0], filas[1:]

    doc = docx.Document()
    sec = doc.sections[0]
    sec.orientation = WD_ORIENT.LANDSCAPE
    sec.page_width, sec.page_height = Inches(11), Inches(8.5)
    sec.left_margin = sec.right_margin = Inches(0.5)
    sec.top_margin = sec.bottom_margin = Inches(0.5)

    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(9)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(TITULO)
    r.bold = True
    r.font.size = Pt(13)

    n_preg = sum(1 for f in datos if "SIN PREGUNTA" not in f[1])
    n_crit = len(encabezado) - 2
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run("%d filas de tabla, las %d son preguntas reales, cruzada contra "
              "%d columnas de criterio: %s."
              % (len(datos), n_preg, n_crit, " · ".join(encabezado[2:]))).font.size = Pt(9)

    t = doc.add_table(rows=1, cols=len(encabezado))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(encabezado):
        celda = t.rows[0].cells[i]
        celda.text = ""
        run = celda.paragraphs[0].add_run(h)
        run.bold = True
        run.font.size = Pt(9)

    for fila in datos:
        celdas = t.add_row().cells
        for i, v in enumerate(fila[:len(encabezado)]):
            celdas[i].text = ""
            run = celdas[i].paragraphs[0].add_run(v)
            run.font.size = Pt(8)

    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run("Estado: documento de trabajo, generado desde el .md por "
              "generar_matriz_docx.py. Fuente editable: «Matriz de Cobertura "
              "Tecnica - Instrumento 2.md». Editar el .md y volver a ejecutar; "
              "no editar el .docx a mano.").font.size = Pt(8)

    doc.save(DOCX)
    print("docx: %s" % DOCX)
    print("  filas de tabla: %d  (preguntas reales: %d)" % (len(datos), n_preg))
    print("  columnas: %d  celdas: %d"
          % (len(encabezado), len(datos) * len(encabezado)))


if __name__ == "__main__":
    main()