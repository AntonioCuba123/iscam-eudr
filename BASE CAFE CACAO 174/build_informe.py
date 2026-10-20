# -*- coding: utf-8 -*-
"""Genera el informe de hallazgos de las 174 organizaciones en Markdown y DOCX."""
import pandas as pd

FINDINGS = {}
ORDEN = []
DIR = r"C:\Users\acuba\eudrperu\BASE CAFE CACAO 174"
for f in ["findings_parte1.py", "findings_parte2.py", "findings_parte3.py", "findings_parte4.py",
          "findings_parte5.py", "findings_parte6.py", "findings_parte7.py", "findings_parte8.py",
          "findings_parte9.py", "findings_parte10.py"]:
    with open(DIR + "\\" + f, encoding="utf-8") as fh:
        src = fh.read()
    antes = set(FINDINGS.keys())
    exec(src, globals())
    nuevos = [k for k in FINDINGS if k not in antes]
    ORDEN.extend(nuevos)

df = pd.read_csv(r"C:\Users\acuba\eudrperu\BASE CAFE CACAO 174\MATRIZ_ORGANIZACIONES_174_FINAL.csv", dtype={"RUC": str})
df = df.set_index("RUC")

# Asignar badge por orden original de la consulta de 174
rucs_orden = pd.read_excel(
    r"C:\Users\acuba\eudrperu\BASE CAFE CACAO 174\CONSULTA MASIVA RUC 10.10.26\ruces_lotes_174.xlsx")
rucs_orden["RUC"] = rucs_orden["RUC"].astype(str).str.zfill(11)
orden_consulta = rucs_orden["RUC"].tolist()

BADGE = {}
BATCH = 18
for i, r in enumerate(orden_consulta):
    num = i // BATCH + 1
    BADGE.setdefault(num, []).append(r)

TOTAL = len(orden_consulta)
HOY = "10 de octubre de 2026"

CAMPOS = [
    ("Socios", "socios"),
    ("Hectareas / area", "hectareas"),
    ("Certificaciones", "certificaciones"),
    ("Exportaciones / mercados", "exportaciones"),
    ("Hallazgo detallado", "hallazgo_clave"),
    ("Fuentes citadas", "fuentes"),
]


def val(ruc, k):
    d = FINDINGS.get(ruc, {})
    v = d.get(k)
    return "" if v in (None, "No verificado") else str(v)


def org_label(ruc):
    pub = val(ruc, "nombre_publico")
    try:
        sol = df.loc[ruc, "Razón Social (SUNAT)"]
    except KeyError:
        sol = None
    sol = "" if sol is None or str(sol) == "nan" else str(sol)
    return pub or sol or "(sin razon social)"


def dep(ruc):
    try:
        v = df.loc[ruc, "Departamento"]
    except KeyError:
        return ""
    return "" if v is None or str(v) == "nan" else str(v)


# ---------------------------------------------------------------- Markdown
md = []
md.append("# Informe de hallazgos de fuentes publicas")
md.append("")
md.append("## Base de 174 organizaciones cafetaleras y cacaoteras del Peru")
md.append("")
md.append("| | |")
md.append("|---|---|")
md.append("| **Organizaciones investigadas** | %d |" % TOTAL)
md.append("| **Fecha de acceso a fuentes** | %s |" % HOY)
md.append("| **Metodo** | Busqueda web por RUC y razon social, con citacion de URL por organizacion |")
md.append("| **Organizacion** | 10 grupos (badges) de 17-18 organizaciones |")
md.append("| **Cobertura de hallazgo** | %d de %d (100%%) |" % (TOTAL, TOTAL))
md.append("")
md.append("> **Nota metodologica.** Cada ficha indica lo que dicen las fuentes publicas sobre la")
md.append("> organizacion. Cuando no se localizo evidencia publica para un dato, se consigna")
md.append("> explicitamente \"No verificado\" en lugar de inferirlo. Los datos internos del proyecto")
md.append("> (socios, hectareas, FOB, certificaciones, EUDR) se mantienen en la matriz")
md.append("> `MATRIZ_ORGANIZACIONES_174_FINAL.xlsx` en columnas separadas.")
md.append("")
md.append("---")
md.append("")

for num in sorted(BADGE):
    rucs = BADGE[num]
    md.append("## Grupo %d de 10 - %d organizaciones" % (num, len(rucs)))
    md.append("")
    for j, ruc in enumerate(rucs, 1):
        md.append("### %d.%d  %s" % (num, j, org_label(ruc)))
        md.append("")
        md.append("- **RUC:** %s" % ruc)
        if dep(ruc):
            md.append("- **Departamento:** %s" % dep(ruc))
        web = val(ruc, "web")
        if web:
            md.append("- **Web / referencia principal:** %s" % web)
        md.append("")
        for titulo, k in CAMPOS:
            v = val(ruc, k)
            if not v:
                continue
            if k == "fuentes":
                md.append("**%s:**" % titulo)
                md.append("")
                for u in [x.strip() for x in v.replace(" | ", "|").split("|") if x.strip()]:
                    md.append("- %s" % u)
                md.append("")
            else:
                md.append("**%s:** %s" % (titulo, v))
                md.append("")
        md.append("---")
        md.append("")

md.append("## Resumen de fuentes institucionales citadas")
md.append("")
inst = {
    "MIDAGRI / AGROIDEAS / PROCOMPITE": ["gob.pe/institucion/midagri", "agroideas", "sierra y selva"],
    "DEVIDA (desarrollo alternativo)": ["devida", "gob.pe/institucion/devida"],
    "AGROMERCADO": ["agromercado"],
    "El Peruano / ANDINA / Inforegion / Agraria.pe": ["elperuano", "andina", "inforegion", "agraria.pe"],
    "SENASA / SUNAT / RNP": ["sunat.gob.pe", "devida.gob.pe", "compuempresa", "datosperu", "elruc.pe",
                             "universidadperu", "ubicania"],
    "Academico (PUCP / CONCYTEC)": ["tesis.pucp.edu.pe", "alicia.concytec.gob.pe"],
    "ONG y cooperacion (Helvetas, UNODC, Solidaridad, NESsT, WWF)": [
        "helvetas.org", "unodc.org", "solidaridadlatam.org", "nesst.org", "regenerativo.org"],
    "Certificacion y sellos (Fairtrade, Rainforest, Indecopi)": [
        "comerciojusto.org", "fairtrade", "unglobalcompact.org", "compuempresa.com/marca"],
    "Directorios y plataformas de mercado": ["algrano.com", "producersmarket.com", "perumarketplace.com",
                                             "connectamericas.com", "specialtycoffee.stonex.com",
                                             "coffeeapothecary", "cafecontacto.pe"],
    "Federacion Junta Nacional del Cafe": ["juntadelcafe.org.pe"],
}
for nombre, keys in inst.items():
    urls = set()
    for ruc in orden_consulta:
        for k in ("fuentes", "web"):
            for u in [x.strip() for x in val(ruc, k).replace(" | ", "|").split("|") if x.strip()]:
                if any(kk in u for kk in keys):
                    urls.add(u)
    if urls:
        md.append("### %s" % nombre)
        md.append("")
        for u in sorted(urls):
            md.append("- %s" % u)
        md.append("")

md_text = "\n".join(md)
out_md = r"C:\Users\acuba\eudrperu\BASE CAFE CACAO 174\HALLAZGOS_174_ORGANIZACIONES.md"
with open(out_md, "w", encoding="utf-8") as fh:
    fh.write(md_text)
print("MD  ->", out_md, "|", len(md_text), "caracteres")

# ---------------------------------------------------------------- DOCX
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()
st = doc.styles["Normal"]
st.font.name = "Calibri"
st.font.size = Pt(10)

AZUL = RGBColor(0x1F, 0x4E, 0x78)

for s in doc.sections:
    s.left_margin = s.right_margin = Pt(56)
    s.top_margin = s.bottom_margin = Pt(56)


def h(texto, nivel):
    p = doc.add_heading(texto, level=nivel)
    for r in p.runs:
        r.font.color.rgb = AZUL
    return p


def par(texto, negrita=False, italic=False, sangria=0):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.left_indent = Pt(sangria)
    r = p.add_run(texto)
    r.bold = negrita
    r.italic = italic
    return p


def kv(clave, valor):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run(clave + ": ")
    r.bold = True
    p.add_run(valor)
    return p


t = doc.add_paragraph()
t.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = t.add_run("Informe de hallazgos de fuentes publicas")
r.bold = True
r.font.size = Pt(20)
r.font.color.rgb = AZUL
t2 = doc.add_paragraph()
t2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r2 = t2.add_run("Base de 174 organizaciones cafetaleras y cacaoteras del Peru")
r2.font.size = Pt(12)
r2.italic = True

doc.add_paragraph()
kv("Organizaciones investigadas", "%d" % TOTAL)
kv("Fecha de acceso a fuentes", HOY)
kv("Metodo", "Busqueda web por RUC y razon social, con citacion de URL por organizacion")
kv("Organizacion del informe", "10 grupos (badges) de 17-18 organizaciones")
kv("Cobertura de hallazgo", "%d de %d (100%%)" % (TOTAL, TOTAL))
par("Nota metodologica: cada ficha indica lo que dicen las fuentes publicas sobre la organizacion. "
    "Cuando no se localizo evidencia publica para un dato, se consigna explicitamente \"No verificado\" "
    "en lugar de inferirlo. Los datos internos del proyecto (socios, hectareas, FOB, certificaciones, EUDR) "
    "se mantienen en la matriz MATRIZ_ORGANIZACIONES_174_FINAL.xlsx en columnas separadas.",
    italic=True)

for num in sorted(BADGE):
    rucs = BADGE[num]
    doc.add_page_break()
    h("Grupo %d de 10 - %d organizaciones" % (num, len(rucs)), 1)
    for j, ruc in enumerate(rucs, 1):
        h("%d.%d  %s" % (num, j, org_label(ruc)), 2)
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        rr = p.add_run("RUC: %s" % ruc)
        rr.bold = True
        if dep(ruc):
            par("Departamento: %s" % dep(ruc))
        web = val(ruc, "web")
        if web:
            kv("Web / referencia principal", web)
        for titulo, k in CAMPOS:
            v = val(ruc, k)
            if not v:
                continue
            if k == "fuentes":
                par("Fuentes citadas:", negrita=True)
                for u in [x.strip() for x in v.replace(" | ", "|").split("|") if x.strip()]:
                    pu = doc.add_paragraph(u, style="List Bullet")
                    pu.paragraph_format.space_after = Pt(1)
            else:
                kv(titulo, v)
        doc.add_paragraph("_" * 70)

out_docx = r"C:\Users\acuba\eudrperu\BASE CAFE CACAO 174\HALLAZGOS_174_ORGANIZACIONES.docx"
doc.save(out_docx)
print("DOCX->", out_docx)
