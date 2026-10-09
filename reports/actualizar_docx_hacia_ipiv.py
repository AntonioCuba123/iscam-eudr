"""
Inserta en 'EUDR Café Perú — Diagnóstico Integrado (2).docx' las secciones nuevas
que acercan el informe hacia el Índice de Preparación (IP) / Índice de
Vulnerabilidad (IV) que postula el equipo ISCAM, con datos reales calculados por
generar_tablas_informe_eudr.py (PPA/SUNAT/Registro Sanitario, IV1 por país real
de Aduanas, capa de confianza/triangulación y mapa de cobertura de las 10
subdimensiones de IP/IV).

No reescribe el documento desde cero: localiza párrafos ancla por texto y
agrega contenido nuevo alrededor, dejando intacto todo lo ya redactado y
aprobado. Pensado para ejecutarse una sola vez sobre el archivo "(2).docx";
volver a correrlo duplicaría las secciones nuevas.

Uso:
    python actualizar_docx_hacia_ipiv.py

Requiere: python-docx, y que generar_tablas_informe_eudr.py esté en la misma
carpeta (se importa como módulo para reutilizar exactamente los mismos
cálculos que alimentan informe_eudr_tablas.xlsx).
"""

from pathlib import Path

import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Pt

import generar_tablas_informe_eudr as gt

BASE_DIR = Path(__file__).resolve().parent
DOCX_FILE = BASE_DIR / "EUDR Café Perú — Diagnóstico Integrado (2).docx"


# ---------------------------------------------------------------------------
# Utilidades de inserción (python-docx no trae "insertar tabla antes de X";
# se usa el mismo truco de bajo nivel que python-docx usa internamente para
# insert_paragraph_before, aplicado también a tablas).
# ---------------------------------------------------------------------------

def find_paragraph(doc: docx.Document, text_startswith: str):
    for p in doc.paragraphs:
        if p.text.strip().startswith(text_startswith):
            return p
    raise ValueError(f"No se encontró un párrafo que empiece con: {text_startswith!r}")


def insert_paragraphs_before(anchor, blocks: list[tuple[str, str]]):
    """blocks: lista de (estilo, texto). Cada insert_paragraph_before(anchor) cae
    justo antes de `anchor`, es decir, justo despues del ultimo insertado -- por
    eso se recorre `blocks` en orden normal (NO invertido) para que el resultado
    final quede en el mismo orden en que aparecen en la lista."""
    for style, text in blocks:
        new_p = anchor.insert_paragraph_before(text, style=style)
        new_p.paragraph_format.space_after = Pt(6)


def insert_table_before(doc: docx.Document, anchor, headers: list[str], rows: list[list[str]]):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"  # mismo estilo que las 5 tablas ya existentes en el documento
    for j, h in enumerate(headers):
        cell = table.rows[0].cells[j]
        cell.text = h
        for run in cell.paragraphs[0].runs:
            run.bold = True
    for i, row in enumerate(rows, start=1):
        for j, val in enumerate(row):
            table.rows[i].cells[j].text = str(val)
    # mover la tabla (creada al final del documento) justo antes del ancla
    anchor._p.addprevious(table._tbl)
    # parrafo vacio entre la tabla y lo que sigue, para que no queden pegados
    anchor.insert_paragraph_before("")
    return table


def pct(x: float) -> str:
    return f"{x:.1f}%"


def money(x: float) -> str:
    return f"US$ {x:,.0f}"


def main() -> None:
    doc = docx.Document(DOCX_FILE)

    # --- recalcular todo con el pipeline real (misma fuente que el .xlsx) ---
    midagri = gt.load_midagri()
    dua = gt.load_dua()
    dua_detalle = gt.load_dua_detalle()
    oece_sheets = gt.load_oece()
    readiness = gt.readiness_index(midagri, dua)
    cert_gap = gt.certification_gap(midagri, dua)
    ip_insumos = gt.ip_insumos_externos(midagri, oece_sheets)
    iv1 = gt.iv1_dependencia_ue(midagri, dua_detalle)
    confianza = gt.capa_confianza_triangulacion(readiness, cert_gap)
    cobertura = gt.mapa_cobertura_ip_iv()

    # ---- cifras puntuales citadas en el texto (todas derivadas, ninguna inventada) ----
    n_sin_registro_sanitario = (ip_insumos["registro_sanitario_ip4"] == "Sin registro").sum()
    exportadores_ruc = set(readiness.loc[readiness["exporta"] == "SI", "ruc"])
    sin_registro_exportadoras = ip_insumos[
        (ip_insumos["ruc"].isin(exportadores_ruc)) &
        (ip_insumos["registro_sanitario_ip4"] == "Sin registro")
    ]["organizacion"].tolist()
    n_declara_organica = int(cert_gap["organica_declarada"].sum())
    n_evidencia_organica = int((cert_gap["n_items_organico"] > 0).sum())
    n_declara_fairtrade = int(cert_gap["fairtrade_declarado"].sum())
    n_evidencia_fairtrade = int((cert_gap["n_items_fairtrade"] > 0).sum())
    n_confianza_baja = int((confianza["nivel_confianza_triangulacion"] == "Baja (diverge en todo lo verificable)").sum())
    n_confianza_sin = int(confianza["nivel_confianza_triangulacion"].str.startswith("Sin verificación").sum())

    # =====================================================================
    # 1) Linea de fecha, resumen y palabras clave
    # =====================================================================
    fecha_p = find_paragraph(doc, "Oct 8, 2026")
    fecha_p.add_run(" (actualizado 9 oct. 2026)")

    resumen_p = find_paragraph(doc, "Resumen.")
    resumen_p.add_run(
        " Como ejercicio complementario, el documento evalúa en qué medida este índice "
        "administrativo se acerca a las diez subdimensiones del Índice de Preparación (IP) y el "
        "Índice de Vulnerabilidad (IV) que postula el equipo ISCAM, y qué tan factible es hoy "
        "construir cada una de ellas a partir de fuentes verificables distintas al autorreporte."
    )

    keywords_p = find_paragraph(doc, "Palabras clave:")
    keywords_p.add_run(", Índice de Preparación (IP), Índice de Vulnerabilidad (IV), ISCAM.")

    # =====================================================================
    # 2) Nueva 3.3, antes de "4. Resultados"
    # =====================================================================
    anchor_resultados = find_paragraph(doc, "4. Resultados")
    insert_paragraphs_before(anchor_resultados, [
        ("Heading 3", "3.3 Relación con el Índice de Preparación (IP) y el Índice de "
                       "Vulnerabilidad (IV) de ISCAM"),
        ("Normal",
         "Este ejercicio no construye el IP ni el IV que postula el equipo ISCAM —esa "
         "arquitectura, de cinco subdimensiones separables por índice, requiere el Instrumento 2 "
         "aplicado a cooperativas reales, lo cual todavía no ha ocurrido—. Su propósito es doble: "
         "conocer a fondo estos 25 casos documentados por MIDAGRI, y obtener una primera idea, "
         "preliminar, de qué tan factible e idóneo resulta el instrumento frente a fuentes "
         "administrativas que sí existen hoy. El índice de cuatro criterios de la sección 3.2 es "
         "más grueso que IP —colapsa en un solo campo autodeclarado lo que IP separa en IP1 "
         "(trazabilidad/origen) e IP2 (cumplimiento ambiental/legal)— pero también más verificado, "
         "porque cruza Aduanas y SUNAT, fuentes que el Instrumento 2 todavía no tiene con qué "
         "contrastar en ningún caso real."),
        ("Normal",
         "Las secciones 4.9 a 4.11 retoman esta relación con tres piezas concretas: qué tan bien "
         "resiste la certificación autorreportada frente a la evidencia documental de Aduanas "
         "(4.9); qué tan dependiente es cada organización exportadora del mercado europeo "
         "específicamente, calculado con datos reales y no autorreportados (4.10, IV1); y un mapa "
         "de cobertura que documenta, subdimensión por subdimensión, cuánto de IP/IV es hoy "
         "verificable sin la encuesta y cuánto sigue dependiendo íntegramente de aplicarla (4.11)."),
    ])

    # =====================================================================
    # 3) Addendum a 4.5 (antes de "4.6 Concentración logística")
    # =====================================================================
    anchor_46 = find_paragraph(doc, "4.6 Concentración logística")
    insert_paragraphs_before(anchor_46, [
        ("Normal",
         f"Este contraste FOB-vs-Aduanas no es, en rigor, una subdimensión de IP ni de IV: es el "
         f"mecanismo de triangulación que el propio diseño de ISCAM exige como paso metodológico, "
         f"sin que hasta ahora existiera una forma concreta de ejecutarlo. Al extenderlo a las dos "
         f"variables de certificación (orgánica y Fairtrade, sección 4.9) y consolidarlo en un "
         f"solo indicador por organización, resulta que {n_confianza_baja} organizaciones "
         f"—entre ellas Cooperativa Agraria Valle Grande, el mayor exportador de toda la muestra— "
         f"divergen en las tres variables verificables a la vez, y {n_confianza_sin} no tienen "
         f"ninguna fuente externa con la que contrastar. Ser Tier 1 por los criterios de la "
         f"sección 3.2 no implica, entonces, tener la confianza más alta en esta capa de "
         f"triangulación: son dos lecturas distintas, y conviene reportarlas por separado en "
         f"cualquier aplicación futura del índice."),
    ])

    # =====================================================================
    # 4) Addendum a 4.6 (antes de "4.7 Sensibilidad...")
    # =====================================================================
    anchor_47 = find_paragraph(doc, "4.7 Sensibilidad")
    insert_paragraphs_before(anchor_47, [
        ("Normal",
         "Esta señal no corresponde hoy a ninguna de las diez subdimensiones de IP/IV: es "
         "candidata a sumarse a IV5 (riesgo social y comercial), pero queda documentada como "
         "pendiente de una decisión de alcance explícita —el mismo criterio ya aplicado cuando se "
         "evaluó, y no se incorporó sin más, la pregunta de CLPI en Instrumento 7— antes de "
         "asumir que es un vacío que corresponde llenar automáticamente."),
    ])

    # =====================================================================
    # 5) Bloque nuevo 4.9 / 4.10 / 4.11, antes de "5. Discusión"
    # =====================================================================
    anchor_discusion = find_paragraph(doc, "5. Discusión")

    insert_paragraphs_before(anchor_discusion, [
        ("Heading 3", "4.9 Certificaciones: autorreporte vigente frente a evidencia documental en Aduanas"),
        ("Normal",
         f"El Art. 10(2) del Reglamento ya establece que las certificaciones voluntarias son "
         f"información complementaria, no evidencia sustitutiva; esta sección cuantifica además "
         f"cuánto rastro documental deja cada certificación en el expediente que un comprador "
         f"europeo puede auditar directamente. De las 14 organizaciones con registro real en "
         f"Aduanas, {n_declara_fairtrade} declaran certificación Fairtrade vigente en su ficha "
         f"MIDAGRI, pero solo {n_evidencia_fairtrade} tiene la palabra 'fairtrade' en la "
         f"descripción comercial de al menos un ítem de su propia Declaración de Aduanas (COCLA). "
         f"La certificación orgánica deja un rastro más consistente, aunque tampoco pleno: "
         f"{n_declara_organica} de 14 la declaran vigente y {n_evidencia_organica} tienen evidencia "
         f"descriptiva en Aduanas."),
        ("Normal",
         "La lectura no es que las certificaciones sean falsas —la descripción comercial de una "
         "Declaración de Aduanas no está diseñada para documentar sellos de sostenibilidad, y su "
         "ausencia no prueba que el certificado no exista—. La lectura correcta es que el criterio "
         "cerrado de validación externa que ISCAM ya identificó ('Certificaciones') necesita, en la "
         "práctica, dos capas distintas: certificación autorreportada vigente, y evidencia "
         "documental en el expediente transaccional. Tratarlas como una sola señal sobreestimaría "
         "la confianza de cualquier verificación externa basada solo en Aduanas."),

        ("Heading 3", "4.10 Dependencia real del mercado europeo (IV1)"),
        ("Normal",
         "IV1 (dependencia del mercado europeo) requería, en el diseño original, una pregunta de "
         "encuesta sobre volumen total exportado a todos los destinos —el denominador que no "
         "estaba disponible—. Para las 14 organizaciones con registro real en Aduanas, ese "
         "denominador ya existe: cada Declaración Única de Aduana (DUA) trae un código de país de "
         "destino y un FOB propio, lo que permite calcular el porcentaje real del FOB exportado "
         "específicamente hacia la Unión Europea (27 miembros más Guadalupe, territorio aduanero "
         "de la UE; se excluye deliberadamente el Reino Unido, no miembro desde el Brexit, pese a "
         "ser uno de los destinos más frecuentes de la muestra)."),
        ("Normal",
         "El resultado separa dos lecturas que el índice de la sección 3.2 no distingue. Tres "
         "organizaciones —Valle del Biavo, Villa Rica (CEMCAVIR) y Tropical Products— exportan el "
         "100% de su FOB verificado hacia la UE: cualquier fricción EUDR las deja sin mercado "
         "alternativo inmediato. En el otro extremo, COCLA (20.3% hacia la UE) y La Florida (15.4%) "
         "son Tier 1 por preparación declarada, pero su exposición real a un bloqueo específicamente "
         "europeo es baja porque la mayor parte de su FOB ya se dirige a otros mercados (Japón, "
         "Estados Unidos). Esta es, en esencia, la lectura conjunta que el diseño IP×IV de ISCAM ya "
         "anticipaba: preparación alta y dependencia alta no son lo mismo, y solo la segunda "
         "determina cuánto duele, en términos comerciales, que la primera falle."),
    ])

    headers_iv1 = ["Organización", "FOB real UE", "FOB real no-UE", "FOB real total", "% hacia la UE"]
    rows_iv1 = [
        [r["organizacion"], money(r["fob_ue"]), money(r["fob_no_ue"]), money(r["fob_total"]), pct(r["pct_fob_ue"])]
        for _, r in iv1.iterrows()
    ]
    insert_table_before(doc, anchor_discusion, headers_iv1, rows_iv1)

    insert_paragraphs_before(anchor_discusion, [
        ("Normal",
         "Para las 11 organizaciones restantes, sin registro DUA, IV1 sigue dependiendo "
         "íntegramente de la pregunta P1b ya diseñada para Instrumento 2 — este dato administrativo "
         "no las cubre."),

        ("Heading 3", "4.11 Mapa de cobertura hacia el índice IP/IV de ISCAM"),
        ("Normal",
         f"La pieza más directamente útil de este ejercicio para evaluar la factibilidad del "
         f"instrumento es esta: de las diez subdimensiones que ISCAM postula (cinco de IP, cinco de "
         f"IV), ¿cuántas se pueden acotar hoy con fuentes administrativas verificables, sin esperar "
         f"a aplicar la encuesta? Un ejemplo concreto ilustra el tipo de hallazgo que esta cobertura "
         f"permite: {n_sin_registro_sanitario} de las 25 organizaciones no tienen ningún Registro "
         f"Sanitario vigente, y dos de ellas —{' y '.join(sin_registro_exportadoras[:2])}— son, "
         f"precisamente, los dos mayores exportadores de la muestra y Tier 1 por los criterios de "
         f"la sección 3.2. Es exactamente el mismo patrón ya documentado para la vigencia de "
         f"mandatos en la sección 4.8: una brecha documental real que el índice de cuatro criterios "
         f"no observa porque no la mide, no porque no exista."),
    ])

    headers_cob = ["Índice", "Subdimensión", "Cobertura hoy", "Fuente externa disponible", "Pendiente de Instrumento 2"]
    rows_cob = [list(r) for _, r in cobertura.iterrows()]
    insert_table_before(doc, anchor_discusion, headers_cob, rows_cob)

    insert_paragraphs_before(anchor_discusion, [
        ("Normal",
         "De las diez subdimensiones, dos tienen hoy una fuente externa fuerte en al menos un "
         "componente (IP2 por el lado tributario, IV1 para 14 de las 25 organizaciones), cuatro "
         "tienen cobertura parcial o un proxy grueso (IP1, IP3, IP4, IV3), y cuatro no tienen "
         "ninguna fuente administrativa disponible (IP5, IV2, IV4, y la señal nueva de IV5 sin "
         "asignar todavía). Dicho de otro modo: el dato administrativo que ya existe puede acotar "
         "o corregir piezas específicas de IP/IV, pero no puede reconstruir la arquitectura "
         "completa que el instrumento está diseñado para levantar — la idoneidad preliminar del "
         "Instrumento 2 queda, con este ejercicio, más clara en qué resuelve que las fuentes "
         "administrativas no resuelven por sí solas."),
    ])

    # =====================================================================
    # 6) Addendum a la Discusión (antes de "6. Limitaciones")
    # =====================================================================
    anchor_limitaciones = find_paragraph(doc, "6. Limitaciones")
    insert_paragraphs_before(anchor_limitaciones, [
        ("Normal",
         "Un último punto de discusión conecta este ejercicio con el diseño IP/IV de ISCAM. El "
         "campo único de avance EUDR autodeclarado que sostiene el índice de la sección 3.2 no "
         "puede, por construcción, reconstruir las cinco subdimensiones separables que IP exige: "
         "una organización con Art. 9 (geolocalización) resuelto pero Art. 3b (legalidad) "
         "pendiente, y otra en la situación inversa, producirían el mismo valor declarado si ambas "
         "redondean su propio avance a una sola cifra. Este ejercicio confirma, con los 25 casos "
         "documentados, que ese nivel de agregación es insuficiente para el diseño que ISCAM "
         "busca —y, a la vez, que un subconjunto específico de variables (inscripción PPA, "
         "formalidad SUNAT, FOB por país de destino, Registro Sanitario) sí tiene hoy una fuente "
         "externa capaz de auditar las respuestas que Instrumento 2 recoja una vez se aplique a "
         "cooperativas reales."),
    ])

    # =====================================================================
    # 7) Cuarta conclusión (antes de "Referencias y fuentes de datos")
    # =====================================================================
    anchor_referencias = find_paragraph(doc, "Referencias y fuentes de datos")
    insert_paragraphs_before(anchor_referencias, [
        ("Normal",
         "Cuarta, como ejercicio de factibilidad del instrumento: una sola pregunta autorreportada "
         "de avance EUDR es insuficiente para reconstruir las subdimensiones separables que IP/IV "
         "requieren, pero existen hoy fuentes administrativas verificables —PPA, SUNAT, Registro "
         "Sanitario, y el FOB por país de destino en Aduanas— capaces de auditar externamente un "
         "subconjunto específico de las futuras respuestas de Instrumento 2, antes incluso de que "
         "la encuesta se aplique a una sola cooperativa real. El mapa de cobertura de la sección "
         "4.11 deja ese subconjunto delimitado con precisión: no sustituye la encuesta, pero "
         "acota, desde ahora, qué parte de ella podrá contrastarse externamente y qué parte "
         "seguirá dependiendo por completo de lo que cada organización decida reportar."),
    ])

    doc.save(DOCX_FILE)
    print(f"Documento actualizado: {DOCX_FILE}")
    print(f"  Párrafos totales ahora: {len(doc.paragraphs)}")
    print(f"  Tablas totales ahora: {len(doc.tables)}")


if __name__ == "__main__":
    main()
