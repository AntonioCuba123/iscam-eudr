# -*- coding: utf-8 -*-
"""
Propaga el criterio ratificado del 2026-10-15 a los docx que habían quedado
con la definición vieja de IP5 (incluía D11 y la certificación ponderada):

  · DT-ISCAM-001_Indice_ISCAM_Trabajo.docx  — Tabla 3 (IP5) y Tabla 8 (fórmulas)
  · ISCAM/Metodologia_ISA_MarcoMuestral.docx — Tabla de fórmulas (IP5)

Además corrige dos defectos ortográficos arrastrados (caracteres CJK
intruidos por el portapapeles: "文献" → "bibliografía") y actualiza la línea
de hoja de ruta que mandaba a "poblar D10" con certificaciones: ahora las
certificaciones alimentan IP5 por conteo (MATRIZ_174!AU/AV) y D10 es bandera.
"""
import os, shutil, datetime, re
import docx

ROOT = r"C:\Users\acuba\eudrperu"
RESP = os.path.join(ROOT, "ISCAM", "respaldos")
ts = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")

DT = os.path.join(ROOT, "DT-ISCAM-001_Indice_ISCAM_Trabajo.docx")
MM = os.path.join(ROOT, "ISCAM", "Metodologia_ISA_MarcoMuestral.docx")


def replace_in_doc(d, old, new, tag):
    """Reemplaza old por new en el primer párrafo (o celda) que lo contenga.
    Tolera que el texto esté partido entre runs: consolida en el primer run.
    Idempotente: si old ya no está pero new sí, lo cuenta como aplicado."""
    def fix_par(p):
        for r in p.runs:
            if old in r.text:
                if new in r.text:      # ya aplicado en este run
                    return False
                r.text = r.text.replace(old, new)
                return True
        full = "".join(r.text for r in p.runs)
        if old in full:
            if new in full:            # ya aplicado en el párrafo
                return False
            merged = full.replace(old, new)
            p.runs[0].text = merged
            for r in p.runs[1:]:
                r.text = ""
            return True
        return False

    for p in d.paragraphs:
        if fix_par(p):
            print(f"OK {tag}")
            return
    for tb in d.tables:
        for row in tb.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    if fix_par(p):
                        print(f"OK {tag}")
                        return
    # si new ya está en el documento, se considera aplicado
    texto = "\n".join(p.text for p in d.paragraphs) + "\n" + "\n".join(
        c.text for tb in d.tables for r in tb.rows for c in r.cells)
    if new in texto:
        print(f"YA APLICADO {tag}")
        return
    raise SystemExit(f"NO ENCONTRADO en {tag}: {old[:80]!r}")


def collapse_dup(d, suffix, tag):
    """Colapsa un sufijo duplicado por una corrida previa del script
    (old era subcadena de new y el reemplazo se aplicó dos veces)."""
    doubled = suffix + suffix
    hits = 0
    for p in d.paragraphs:
        for r in p.runs:
            if doubled in r.text:
                r.text = r.text.replace(doubled, suffix); hits += 1
    for tb in d.tables:
        for row in tb.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    for r in p.runs:
                        if doubled in r.text:
                            r.text = r.text.replace(doubled, suffix); hits += 1
    if hits:
        print(f"REPARADO {tag} ({hits} run(s))")


# ── 1) DT-ISCAM-001 ────────────────────────────────────────────────────────
bak = os.path.join(RESP, f"DT-ISCAM-001_Indice_ISCAM_Trabajo.backup_{ts}_pre-ip5-conteo.docx")
shutil.copy2(DT, bak); print("respaldo:", bak)
d = docx.Document(DT)

collapse_dup(d, " · Cert = conteo 0/33/66/100", "DT T8 sufijo duplicado")

replace_in_doc(d,
    "D7 + D9 + D11 + Certificaciones",
    "D7 + D9 + Certificación (conteo 0/33/66/100; sin D11, que es inventario)",
    "DT T3 IP5")

replace_in_doc(d,
    "= (D7 + D9 + Cert) / 3",
    "= (D7 + D9 + Cert) / 3 · Cert = conteo 0/33/66/100",
    "DT T8 IP5")

replace_in_doc(d,
    "D10, D11 — Certificaciones, género en directiva.",
    "D10, D11 — ítems pendientes de captura; se reportan aparte "
    "(bandera e inventario), no alimentan índices.",
    "DT P86 pendientes")

replace_in_doc(d,
    "Poblar D10 con certificaciones conocidas (Rainforest, UTZ, Orgánico, Fairtrade, 4C) "
    "— dato accesible sin visita de campo.",
    "Poblar el registro de certificaciones vigentes (B0.9 → MATRIZ_174!AU/AV) con "
    "certificaciones conocidas (Rainforest, UTZ, Orgánico, Fairtrade, 4C) — dato "
    "accesible sin visita de campo; alimenta IP5 por conteo. D10 mismo es bandera: "
    "sus ítems se reportan aparte.",
    "DT P102 hoja de ruta")

replace_in_doc(d, "se sustenta en文献 de OECD", "se sustenta en bibliografía de OECD",
    "DT P95 文献→bibliografía")
replace_in_doc(d, "validados por文献 de OECD", "validados por bibliografía de OECD",
    "DT P120 文献→bibliografía")
replace_in_doc(d, "no se compensa con满分 en trazabilidad",
    "no se compensa con un puntaje máximo en trazabilidad",
    "DT P53 满分→puntaje máximo")

d.save(DT); print("docx guardado:", DT)

# ── 2) Metodologia_ISA_MarcoMuestral.docx ───────────────────────────────────
bak = os.path.join(RESP, f"Metodologia_ISA_MarcoMuestral.backup_{ts}_pre-ip5-conteo.docx")
shutil.copy2(MM, bak); print("respaldo:", bak)
m = docx.Document(MM)

collapse_dup(m, " · Certificación = conteo 0/33/66/100", "MM T0 sufijo duplicado")

replace_in_doc(m,
    "= (D7 + D9 + Certificación) / 3",
    "= (D7 + D9 + Certificación) / 3 · Certificación = conteo 0/33/66/100",
    "MM T0 IP5")

m.save(MM); print("docx guardado:", MM)

# ── 3) Verificación: sin CJK residual ni fórmula vieja ──────────────────────
cjk = re.compile(r'[\u4e00-\u9fff\uff00-\uffef]')
for path in (DT, MM):
    dd = docx.Document(path)
    malos = []
    for i, p in enumerate(dd.paragraphs):
        if cjk.search(p.text):
            malos.append(("P%d" % i, p.text[:80]))
    for ti, tb in enumerate(dd.tables):
        for ri, row in enumerate(tb.rows):
            for ci, cell in enumerate(row.cells):
                if cjk.search(cell.text):
                    malos.append(("T%dR%dC%d" % (ti, ri, ci), cell.text[:80]))
    full = "\n".join(p.text for p in dd.paragraphs) + "\n" + "\n".join(
        c.text for tb in dd.tables for r in tb.rows for c in r.cells)
    print(os.path.basename(path),
          "| CJK residual:", len(malos), malos[:3],
          "| 'D11 + Cert' presente:", "D11 + Cert" in full,
          "| conteo 0/33/66/100 presente:", "0/33/66/100" in full)
