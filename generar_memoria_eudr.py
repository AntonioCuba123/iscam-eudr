# -*- coding: utf-8 -*-
"""
Genera DOCX y PDF de la Memoria Diaria EUDR.
Requiere: python-docx, reportlab
"""

import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import reportlab
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

# ── Rutas ────────────────────────────────────────────────────────────────────
SRC = (r"C:\Users\acuba\.minimax\v2\assets\2026\10\01"
       r"\17-41-27-653-asset_20261001-174127-653_"
       r"7634a625047b_ed338c6a-Memoria Diaria EUDR.md")
OUT_DOCX = r"C:\Users\acuba\eudrperu\Memoria_Diaria_EUDR.docx"
OUT_PDF  = r"C:\Users\acuba\eudrperu\Memoria_Diaria_EUDR.pdf"

# ── Colores institucionales ───────────────────────────────────────────────────
DARK_GREEN  = RGBColor(0x1B, 0x5E, 0x20)   # #1B5E20
MID_GREEN   = RGBColor(0x2E, 0x7D, 0x32)   # #2E7D32
LIGHT_GREEN = RGBColor(0xA5, 0xD6, 0xA7)   # #A5D6A7
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
ACCENT      = RGBColor(0x0D, 0x47, 0xA1)   # #0D47A1  (tablas)
LIGHT_GREY  = RGBColor(0xF5, 0xF5, 0xF5)
MID_GREY    = RGBColor(0x9E, 0x9E, 0x9E)

# ReportLab hex colors
RL_DARK_GREEN  = colors.HexColor("#1B5E20")
RL_MID_GREEN   = colors.HexColor("#2E7D32")
RL_LIGHT_GREEN = colors.HexColor("#A5D6A7")
RL_ACCENT      = colors.HexColor("#0D47A1")
RL_LIGHT_GREY  = colors.HexColor("#F5F5F5")
RL_MID_GREY    = colors.HexColor("#9E9E9E")
RL_WHITE       = colors.white
RL_DARK_TEXT   = colors.HexColor("#212121")

# ── Parser minimalista del MD ─────────────────────────────────────────────────
def parse_markdown(path):
    """Devuelve lista de (tipo, nivel, texto, extra)"""
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    blocks = []
    in_table = False
    table_lines = []
    in_code = False
    code_lines = []

    def finish_table():
        nonlocal table_lines
        if table_lines:
            blocks.append(("table", 0, "", list(table_lines)))
        table_lines = []

    for raw in lines:
        line = raw.rstrip("\n")
        # Fin de bloque MD especial
        if line.strip().startswith("```") and in_code:
            blocks.append(("code_block", 0, "", "\n".join(code_lines)))
            code_lines = []
            in_code = False
            continue
        if in_code:
            code_lines.append(line)
            continue
        if line.strip().startswith("```"):
            in_code = True
            continue

        # HR
        if line.strip() in ("---", "***", "___"):
            finish_table()
            blocks.append(("hr", 0, "", ""))
            continue

        # Tabla
        if "|" in line and line.strip().startswith("|"):
            if not in_table:
                finish_table()
                in_table = True
            table_lines.append(line)
            continue
        else:
            if in_table:
                finish_table()
                in_table = False

        # Headings
        stripped = line.strip()
        if stripped.startswith("# "):
            finish_table()
            blocks.append(("h1", 1, stripped[2:], ""))
        elif stripped.startswith("## "):
            finish_table()
            blocks.append(("h2", 2, stripped[3:], ""))
        elif stripped.startswith("### "):
            finish_table()
            blocks.append(("h3", 3, stripped[4:], ""))
        elif stripped.startswith("#### "):
            finish_table()
            blocks.append(("h4", 4, stripped[5:], ""))
        elif stripped.startswith(">"):
            finish_table()
            blocks.append(("blockquote", 0, stripped[1:].strip(), ""))
        elif stripped.startswith("|") and "---" not in stripped:
            pass  # tabla, se maneja arriba
        elif stripped == "":
            blocks.append(("blank", 0, "", ""))
        else:
            blocks.append(("para", 0, stripped, ""))

    finish_table()
    return blocks

def strip_markdown_inline(text):
    """Quita negritas, cursivas, enlaces y código inline del texto."""
    import re
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"__(.+?)__", r"\1", text)
    text = re.sub(r"_(.+?)_", r"\1", text)
    text = re.sub(r"`(.+?)`", r"\1", text)
    text = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", text)
    return text

def parse_table_row(line):
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return cells

def is_header_row(line):
    return "---" in line or "|---|" in line

# ── DOCX ─────────────────────────────────────────────────────────────────────
def add_run(para, text, bold=False, italic=False, color=None, size=None):
    run = para.add_run(text)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = color
    if size:
        run.font.size = Pt(size)
    return run

def set_cell_bg(cell, hex_color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)

def docx_add_table(doc, table_lines):
    rows = [parse_table_row(l) for l in table_lines if not is_header_row(l) and "|" in l]
    if not rows:
        return
    col_count = max(len(r) for r in rows)
    t = doc.add_table(rows=len(rows), cols=col_count)
    t.style = "Table Grid"
    is_header = True
    for i, row_data in enumerate(rows):
        for j, cell_text in enumerate(row_data):
            cell = t.rows[i].cells[j]
            cell.text = strip_markdown_inline(cell_text)
            if is_header:
                set_cell_bg(cell, "1B5E20")
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                add_run(p, cell.text, bold=True, color=WHITE)
            else:
                if i % 2 == 0:
                    set_cell_bg(cell, "F5F5F5")
    return t

def build_docx(blocks, out_path):
    doc = Document()
    # Márgenes
    section = doc.sections[0]
    section.page_width  = int(A4[0])
    section.page_height = int(A4[1])
    section.left_margin   = Cm(2.5)
    section.right_margin  = Cm(2.5)
    section.top_margin    = Cm(2.5)
    section.bottom_margin = Cm(2.5)

    # Estilos base
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(10)

    # Portada
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_run(p, "\n\n\n\nMEMORIA DIARIA EUDR", bold=True, size=24, color=DARK_GREEN)
    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_run(p2, "Situación Institucional y Estado de Preparación", bold=False, size=14, color=MID_GREEN)
    p3 = doc.add_paragraph()
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_run(p3, "Cooperativas de Café y Cacao del Perú · Reglamento (UE) 2023/1115", size=11)
    p4 = doc.add_paragraph()
    p4.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_run(p4, f"Corte: 01 de octubre de 2026", size=10, color=MID_GREY)
    doc.add_page_break()

    i = 0
    while i < len(blocks):
        kind, lvl, text, extra = blocks[i]
        if kind == "h1":
            p = doc.add_heading(text, level=0)
            p.runs[0].font.color.rgb = DARK_GREEN
        elif kind == "h2":
            p = doc.add_heading(text, level=1)
            p.runs[0].font.color.rgb = DARK_GREEN
        elif kind == "h3":
            p = doc.add_heading(text, level=2)
            p.runs[0].font.color.rgb = MID_GREEN
        elif kind == "h4":
            p = doc.add_heading(text, level=3)
            p.runs[0].font.color.rgb = ACCENT
        elif kind == "para":
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            # procesar inline
            parts = split_inline(text)
            for part in parts:
                if part.startswith("**") and part.endswith("**"):
                    add_run(p, part[2:-2], bold=True)
                elif part.startswith("*") and part.endswith("*"):
                    add_run(p, part[1:-1], italic=True)
                elif part.startswith("`") and part.endswith("`"):
                    add_run(p, part[1:-1], color=ACCENT)
                else:
                    add_run(p, part)
        elif kind == "blockquote":
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(1)
            p.paragraph_format.right_indent = Cm(1)
            add_run(p, f"« {text} »", italic=True, color=MID_GREEN)
        elif kind == "code_block":
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(1)
            run = p.add_run(extra)
            run.font.name = "Courier New"
            run.font.size = Pt(8)
            run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
        elif kind == "hr":
            p = doc.add_paragraph()
            pPr = p._p.get_or_add_pPr()
            pBdr = OxmlElement("w:pBdr")
            bottom = OxmlElement("w:bottom")
            bottom.set(qn("w:val"), "single")
            bottom.set(qn("w:sz"), "6")
            bottom.set(qn("w:space"), "1")
            bottom.set(qn("w:color"), "1B5E20")
            pBdr.append(bottom)
            pPr.append(pBdr)
        elif kind == "table":
            docx_add_table(doc, extra)
        elif kind == "blank":
            doc.add_paragraph()
        i += 1

    doc.save(out_path)
    print(f"DOCX guardado: {out_path}")

def split_inline(text):
    """Separa texto en partes (plain/bold/italic/code)."""
    import re
    # Orden: primero bold, luego italic, luego code
    parts = []
    i = 0
    while i < len(text):
        if text[i:i+2] == "**":
            end = text.find("**", i+2)
            if end != -1:
                parts.append(text[i:end+2])
                i = end+2
                continue
        elif text[i] == "*" and (i == 0 or text[i-1] not in ["*", "`"]):
            end = text.find("*", i+1)
            if end != -1 and text[end-1] != "*":
                parts.append(text[i:end+1])
                i = end+1
                continue
        elif text[i] == "`":
            end = text.find("`", i+1)
            if end != -1:
                parts.append(text[i:end+1])
                i = end+1
                continue
        # plain
        j = i
        while j < len(text) and text[j:j+2] not in ["**", "`"] and (text[j] != "*" or j == 0 or text[j-1] in ["*", "`"]):
            j += 1
        if j == i:
            parts.append(text[i])
            i += 1
        else:
            parts.append(text[i:j])
            i = j
    return parts

# ── PDF ──────────────────────────────────────────────────────────────────────
def build_pdf(blocks, out_path):
    doc = SimpleDocTemplate(
        out_path,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm, bottomMargin=2.5*cm,
        title="Memoria Diaria EUDR",
        author="Proyecto EUDR Perú",
        subject="Situación Institucional y Estado de Preparación",
    )

    styles = getSampleStyleSheet()

    # Estilos custom
    title_style = ParagraphStyle("TitleStyle",
        fontName="Helvetica-Bold", fontSize=22, leading=28,
        textColor=RL_DARK_GREEN, alignment=TA_CENTER, spaceAfter=8)
    subtitle_style = ParagraphStyle("SubtitleStyle",
        fontName="Helvetica", fontSize=13, leading=18,
        textColor=RL_MID_GREEN, alignment=TA_CENTER, spaceAfter=4)
    meta_style = ParagraphStyle("MetaStyle",
        fontName="Helvetica", fontSize=10, leading=14,
        textColor=RL_MID_GREY, alignment=TA_CENTER, spaceAfter=20)
    h1_style = ParagraphStyle("H1Style",
        fontName="Helvetica-Bold", fontSize=15, leading=20,
        textColor=RL_DARK_GREEN, spaceBefore=18, spaceAfter=6,
        borderPad=4, backColor=RL_LIGHT_GREEN,
        borderWidth=0, borderRadius=2)
    h2_style = ParagraphStyle("H2Style",
        fontName="Helvetica-Bold", fontSize=12, leading=16,
        textColor=RL_DARK_GREEN, spaceBefore=12, spaceAfter=4)
    h3_style = ParagraphStyle("H3Style",
        fontName="Helvetica-Bold", fontSize=10.5, leading=14,
        textColor=RL_MID_GREEN, spaceBefore=8, spaceAfter=3)
    h4_style = ParagraphStyle("H4Style",
        fontName="Helvetica-Bold", fontSize=10, leading=13,
        textColor=RL_ACCENT, spaceBefore=6, spaceAfter=2)
    para_style = ParagraphStyle("ParaStyle",
        fontName="Helvetica", fontSize=9.5, leading=14,
        textColor=RL_DARK_TEXT, alignment=TA_JUSTIFY, spaceAfter=4)
    bold_para_style = ParagraphStyle("BoldParaStyle",
        fontName="Helvetica-Bold", fontSize=9.5, leading=14,
        textColor=RL_DARK_TEXT, alignment=TA_JUSTIFY, spaceAfter=4)
    code_style = ParagraphStyle("CodeStyle",
        fontName="Courier", fontSize=7.5, leading=11,
        textColor=colors.HexColor("#555555"),
        backColor=RL_LIGHT_GREY,
        leftIndent=8, rightIndent=8, spaceBefore=4, spaceAfter=4)
    blockquote_style = ParagraphStyle("BlockquoteStyle",
        fontName="Helvetica-Oblique", fontSize=9.5, leading=14,
        textColor=RL_MID_GREEN, leftIndent=16, rightIndent=16,
        alignment=TA_JUSTIFY, spaceBefore=4, spaceAfter=4)
    hr_style = ParagraphStyle("HrStyle",
        fontName="Helvetica", fontSize=6, leading=6,
        textColor=RL_MID_GREEN, spaceBefore=6, spaceAfter=6)

    def style_cell(cell, is_header):
        return ParagraphStyle("Cell",
            fontName="Helvetica-Bold" if is_header else "Helvetica",
            fontSize=8.5, leading=12,
            textColor=RL_WHITE if is_header else RL_DARK_TEXT,
            alignment=TA_CENTER if is_header else TA_LEFT)

    def build_table(table_lines):
        rows = [parse_table_row(l) for l in table_lines if not is_header_row(l) and "|" in l]
        if not rows:
            return None
        col_count = max(len(r) for r in rows)
        data = [[Paragraph(cell, style_cell(None, False)) for cell in row] for row in rows]

        # Anchos
        col_widths = [None] * col_count

        tbl = Table(data, colWidths=col_widths, repeatRows=1)
        ts = TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), RL_DARK_GREEN),
            ("TEXTCOLOR",  (0, 0), (-1, 0), RL_WHITE),
            ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE",   (0, 0), (-1, -1), 8.5),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [RL_WHITE, RL_LIGHT_GREY]),
            ("GRID",       (0, 0), (-1, -1), 0.5, RL_MID_GREY),
            ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING",  (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING",   (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
        ])
        tbl.setStyle(ts)
        return tbl

    def inline_to_spans(text):
        """Convierte texto con **bold* *italic* `code` a ReportLab spans."""
        import re
        spans = []
        pattern = re.compile(
            r'(\*\*(.+?)\*\*)|(\*(.+?)\*)|(`(.+?)`)|(\[([^\]]+)\]\([^\)]+\))|([^*`[]+)',
            re.DOTALL
        )
        for m in pattern.finditer(text):
            if m.group(1):       # bold
                spans.append((m.group(2), "Helvetica-Bold", 9.5))
            elif m.group(3):     # italic
                spans.append((m.group(4), "Helvetica-Oblique", 9.5))
            elif m.group(5):     # code
                spans.append((m.group(6), "Courier", 8.5))
            elif m.group(7):     # link text
                spans.append((m.group(7), "Helvetica", 9.5))
            elif m.group(0):
                spans.append((m.group(0), "Helvetica", 9.5))
        return spans

    def para_from_spans(text, base_style=None):
        from reportlab.platypus import Paragraph as P
        spans = inline_to_spans(text)
        style = base_style or para_style
        parts = []
        for content, font, size in spans:
            parts.append(f'<font name="{font}" size="{size}">{content}</font>')
        combined = "".join(parts)
        return P(combined, style)

    # Portada
    story = [
        Spacer(1, 3*cm),
        Paragraph("MEMORIA DIARIA EUDR", title_style),
        Spacer(1, 0.3*cm),
        Paragraph("Situación Institucional y Estado de Preparación", subtitle_style),
        Spacer(1, 0.2*cm),
        Paragraph("Cooperativas de Café y Cacao del Perú · Reglamento (UE) 2023/1115", subtitle_style),
        Spacer(1, 0.5*cm),
        Paragraph("Corte: 01 de octubre de 2026", meta_style),
        HRFlowable(width="100%", thickness=2, color=RL_MID_GREEN, spaceAfter=20),
        PageBreak(),
    ]

    i = 0
    while i < len(blocks):
        kind, lvl, text, extra = blocks[i]
        if kind == "h1":
            story.append(Paragraph(text, h1_style))
        elif kind == "h2":
            story.append(Paragraph(text, h2_style))
        elif kind == "h3":
            story.append(Paragraph(text, h3_style))
        elif kind == "h4":
            story.append(Paragraph(text, h4_style))
        elif kind == "para":
            story.append(para_from_spans(text, para_style))
        elif kind == "blockquote":
            story.append(Paragraph(f"« {text} »", blockquote_style))
        elif kind == "code_block":
            story.append(Paragraph(extra, code_style))
        elif kind == "hr":
            story.append(HRFlowable(width="100%", thickness=1, color=RL_MID_GREEN,
                                    spaceBefore=6, spaceAfter=6))
        elif kind == "table":
            tbl = build_table(extra)
            if tbl:
                story.append(Spacer(1, 4))
                story.append(tbl)
                story.append(Spacer(1, 6))
        elif kind == "blank":
            story.append(Spacer(1, 4))
        i += 1

    doc.build(story)
    print(f"PDF guardado: {out_path}")

# ── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Parseando MD...")
    blocks = parse_markdown(SRC)
    print(f"  {len(blocks)} bloques")

    print("Generando DOCX...")
    build_docx(blocks, OUT_DOCX)

    print("Generando PDF...")
    build_pdf(blocks, OUT_PDF)

    print("\n✓ Listo:")
    print(f"  {OUT_DOCX}")
    print(f"  {OUT_PDF}")
