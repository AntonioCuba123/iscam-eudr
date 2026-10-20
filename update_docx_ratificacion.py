# -*- coding: utf-8 -*-
"""
Actualiza el documento de metodología con la ratificación [R] (2026-10-15)
contra las fuentes originales del Instrumento 2:
  · §2.2 — la tabla de codificación ya no usa destinos de exportación en el puntaje
    (B0.8 es Bloque 0 y no promedia) y se agrega la nota de ratificación.
  · §2.4 — se documentan los 4 casos de Comercio Justo resueltos.
  · §2.6 — el agregado de dimensiones excluye banderas/mapeos; D11 no promedia.
  · §5  — hito: codificación ratificada contra las fuentes del instrumento.
"""
import os, shutil, datetime
import docx

ROOT = r"C:\Users\acuba\eudrperu"
DOCX = os.path.join(ROOT, "ISCAM", "Metodologia - Instrumento 2 e Indice ISCAM.docx")
ts = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
bak = os.path.join(ROOT, "ISCAM", "respaldos", f"Metodologia.backup_{ts}_pre-ratificacion-doc.docx")
shutil.copy2(DOCX, bak); print("respaldo:", bak)

d = docx.Document(DOCX)
ps = d.paragraphs


def find(sub, start=0):
    for i in range(start, len(ps)):
        if sub in ps[i].text:
            return i
    raise KeyError(sub)


def set_text(p, text):
    for r in list(p.runs):
        r._element.getparent().remove(r._element)
    p.add_run(text)


# ── §2.2 — tabla de codificación ────────────────────────────────────────────
i = find("La conversión de las respuestas categóricas a puntaje")
set_text(ps[i],
    "La conversión de las respuestas categóricas a puntaje es explícita y auditable: "
    "la hoja CODIFICACION es la tabla de codificación del instrumento (una fila por opción "
    "de respuesta) y asigna a cada opción un valor de 0 a 100 —100 indica el mayor "
    "alineamiento con el EUDR y el Pacto Verde— o la marca «sin dato». Las preguntas de "
    "escala 0–4 se convierten ×25; las de porcentaje entran directas en 0–100; las de "
    "casillas múltiples puntúan por el número de componentes marcados. Las opciones que "
    "expresan desconocimiento o no aplicación («No sabe», «No verifica», «No se ha medido», "
    "«No aplica») se codifican como «sin dato» y no promedian: la ausencia de respuesta nunca "
    "se convierte en incumplimiento. La tabla es editable; la dirección de cada ítem quedó "
    "ratificada contra las fuentes del propio instrumento (nota siguiente).")
i041 = i

anchor = find("2.3 Paridad entre café y cacao")
anchor_p = ps[anchor]
anchor_p.insert_paragraph_before(
    "Ratificación de la codificación (2026-10-15). La dirección de los quince ítems que "
    "estaban marcados «[R]» se contrastó contra las fuentes del instrumento —la nota de "
    "puntaje del Instrumento 2, la Tabla 5 del documento de trabajo (qué promedia y qué no "
    "en cada dimensión) y las reglas de integridad de la estructura de la hoja de respuestas—. "
    "El resultado: ocho ítems no entran a ningún promedio, porque el propio instrumento los "
    "ubica fuera de él —B0.8 (identificación, Bloque 0); P8, P10, P13 y P14 (desempeño, "
    "Bloque P); las banderas D2.10, D2.5b, D3.14i, D4.15a, D7.28, D10.36 y D10.37; la "
    "verificación D3.14g; y los mapeos D5.19a, D7.28c, D11.38 y D11.39a—. No se elimina su "
    "captura: se recogen y se reportan por separado, que es su lugar (banderas de alerta, "
    "mapeos e insumos del Instrumento 4). Los siete restantes sí promedian y su dirección "
    "queda confirmada: D1.1 (introducción bajo nombre propio), D1.4 (umbral micro/pequeña "
    "empresa), D3.12 (severidad de la superposición a áreas protegidas), D4.15 (verificación "
    "del cambio de uso posterior al 31-dic-2020), D6.25b (última prueba del protocolo), D9.34 "
    "(carga financiera de la adecuación) y PP1 (reutilización del saco, que alimenta PPWR y "
    "no el ISA-EUDR). Las dimensiones afectadas cambian de insumo por esta razón: los "
    "promedios de D2, D5 y D7 se computan sobre las preguntas que el instrumento define como "
    "promediables, y D10 y D11 dejan de promediar como madurez —D11 es inventario—.",
    style="List Paragraph")

# ── §2.4 — casos de Comercio Justo resueltos ────────────────────────────────
i = find("Regla sobre la base precensal")
set_text(ps[i], ps[i].text.rstrip() +
    " Los cuatro casos de Comercio Justo que quedaban en revisión se resolvieron en la misma "
    "pasada: en tres de ellos la celda de origen contenía texto de certificación orgánica "
    "—no hay evidencia de Comercio Justo— y se mantienen en «sin dato»; el cuarto, AGUILAYOC, "
    "se recodificó a SI con la fuente del directorio de la JNC («Orgánica y Comercio Justo»).")

# ── §2.6 — NORMALIZADO ──────────────────────────────────────────────────────
i = find("NORMALIZADO — resultado automático")
set_text(ps[i],
    "NORMALIZADO — resultado automático: 0-100 por pregunta y el promedio de cada dimensión "
    "sobre las preguntas que efectivamente promedian (D1–D10; D11 es inventario y no promedia, "
    "y de D10 solo puntúa la asesoría EUDR, porque su certificación y su oferta de "
    "«certificación EUDR» son banderas). Las banderas y los mapeos no entran al promedio. "
    "Alimenta directo al motor ISCAM_Score. No se edita.")

# ── §5 — hito de ratificación ───────────────────────────────────────────────
anchor = find("Piloto de comprensibilidad y ajuste de ítems")
ps[anchor].insert_paragraph_before(
    "Codificación ratificada contra las fuentes del instrumento (2026-10-15). Los quince "
    "ítems «[R]» quedaron resueltos y la hoja CODIFICACION no conserva marcas pendientes. La "
    "consecuencia es de insumo, no de definición: los promedios de dimensión ahora excluyen "
    "banderas, mapeos y los bloques 0 y P, tal como el instrumento los define. La "
    "reconciliación completa, ítem por ítem, está en el registro de decisiones del proyecto.",
    style="List Paragraph")

d.save(DOCX)
d2 = docx.Document(DOCX)
js = "\n".join(p.text for p in d2.paragraphs)
print("párrafos:", len(d2.paragraphs), "| tablas:", len(d2.tables))
print("check §2.2 :", "Ratificación de la codificación (2026-10-15)" in js)
print("check §2.4 :", "AGUILAYOC" in js)
print("check §2.6 :", "D11 es inventario y no promedia" in js)
print("check §5   :", "Codificación ratificada contra las fuentes" in js)
print("check viejo:", "[R] = revisar" in js or "marca con «[R]» los ítems" in js)
