# -*- coding: utf-8 -*-
"""
build_pve_index.py — Construye PLANTILLA_INDICE_PVE.xlsx
Plantilla para clasificar preparación y vulnerabilidad de cooperativas
de café y cacao peruano ante el Pacto Verde Europeo (EUDR).

Hojas:
  1. INSTRUCCIONES  — guía de uso
  2. PONDERADORES   — pesos editables (bloque de supuestos)
  3. MATRIZ_174    — 174 organizaciones con variables existentes
  4. PREGUNTAS_PROXY — preguntas campo rápido por dimensión
  5. SCORECARDS    — score PVE por organización + semáforo
  6. RADAR_BRECHAS — resumen por departamento
"""

import openpyxl
from openpyxl.styles import (Font, PatternFill, Alignment, Border, Side,
                              GradientFill)
from openpyxl.styles.numbers import FORMAT_PERCENTAGE_00
from openpyxl.formatting.rule import ColorScaleRule, CellIsRule, FormulaRule
from openpyxl.chart import BarChart, Reference
from openpyxl.chart.series import SeriesLabel
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
import pandas as pd
import os, math

# ─── Rutas ────────────────────────────────────────────────────────────────────
BASE_DIR   = r"C:\Users\acuba\eudrperu"
DATA_DIR   = os.path.join(BASE_DIR, "BASE CAFE CACAO 174")
OUT_FILE   = os.path.join(BASE_DIR, "PLANTILLA_INDICE_PVE.xlsx")

# ─── Estilos reutilizables ────────────────────────────────────────────────────
HEADER_FILL   = PatternFill("solid", fgColor="1F497D")  # azul oscuro
HEADER_FONT   = Font(bold=True, color="FFFFFF", name="Calibri", size=11)
TITLE_FILL    = PatternFill("solid", fgColor="2E75B6")  # azul medio
TITLE_FONT    = Font(bold=True, color="FFFFFF", name="Calibri", size=13)
SUBHDR_FILL   = PatternFill("solid", fgColor="D6E4F0")  # azul claro
SUBHDR_FONT   = Font(bold=True, color="1F497D", name="Calibri", size=10)
INPUT_FILL    = PatternFill("solid", fgColor="FFFFCC")  # amarillo = input editable
INPUT_FONT    = Font(color="0000FF", name="Calibri", size=10)  # azul = hardcoded
FORMULA_FONT  = Font(color="000000", name="Calibri", size=10)  # negro = derivada
PENDING_FILL  = PatternFill("solid", fgColor="F2F2F2")  # gris = pendiente
PENDING_FONT  = Font(color="999999", italic=True, name="Calibri", size=10)
GREEN_FILL    = PatternFill("solid", fgColor="C6EFCE")  # verde
GREEN_FONT    = Font(color="375623", bold=True)
YELLOW_FILL   = PatternFill("solid", fgColor="FFEB9C")  # amarillo
YELLOW_FONT   = Font(color="9C6500", bold=True)
RED_FILL      = PatternFill("solid", fgColor="FFC7CE")  # rojo
RED_FONT      = Font(color="9C0006", bold=True)
THIN_BORDER   = Border(
    left=Side(style="thin"), right=Side(style="thin"),
    top=Side(style="thin"), bottom=Side(style="thin")
)
CENTER_ALIGN  = Alignment(horizontal="center", vertical="center", wrap_text=True)
LEFT_ALIGN    = Alignment(horizontal="left", vertical="center", wrap_text=True)
RIGHT_ALIGN   = Alignment(horizontal="right", vertical="center")


# ════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ════════════════════════════════════════════════════════════════════════════

def set_header(ws, row, col, value, width=None):
    c = ws.cell(row=row, column=col, value=value)
    c.font    = HEADER_FONT
    c.fill    = HEADER_FILL
    c.border  = THIN_BORDER
    c.alignment = CENTER_ALIGN
    if width:
        ws.column_dimensions[get_column_letter(col)].width = width
    return c

def set_title(ws, row, col, value, span=None):
    c = ws.cell(row=row, column=col, value=value)
    c.font  = TITLE_FONT
    c.fill  = TITLE_FILL
    c.alignment = CENTER_ALIGN
    if span:
        ws.merge_cells(start_row=row, start_column=col,
                       end_row=row, end_column=col+span-1)
    return c

def set_subhdr(ws, row, col, value, span=1):
    c = ws.cell(row=row, column=col, value=value)
    c.font   = SUBHDR_FONT
    c.fill   = SUBHDR_FILL
    c.border = THIN_BORDER
    c.alignment = CENTER_ALIGN
    if span > 1:
        ws.merge_cells(start_row=row, start_column=col,
                       end_row=row, end_column=col+span-1)
    return c

def data_cell(ws, row, col, value, fill=None, font=None,
              align=None, number_format=None):
    c = ws.cell(row=row, column=col, value=value)
    c.border  = THIN_BORDER
    c.font    = font or FORMULA_FONT
    c.alignment = align or LEFT_ALIGN
    if fill:
        c.fill = fill
    if number_format:
        c.number_format = number_format
    return c

def input_cell(ws, row, col, value, number_format=None):
    c = ws.cell(row=row, column=col, value=value)
    c.font    = INPUT_FONT
    c.fill    = INPUT_FILL
    c.border  = THIN_BORDER
    c.alignment = LEFT_ALIGN
    if number_format:
        c.number_format = number_format
    return c

def pending_cell(ws, row, col, value="PENDIENTE"):
    c = ws.cell(row=row, column=col, value=value)
    c.font    = PENDING_FONT
    c.fill    = PENDING_FILL
    c.border  = THIN_BORDER
    c.alignment = CENTER_ALIGN
    return c

def dv_dropdown(ws, formula1, sqref):
    dv = DataValidation(type="list", formula1=formula1, allow_blank=True,
                       showDropDown=False)
    dv.sqref = sqref
    ws.add_data_validation(dv)

# ════════════════════════════════════════════════════════════════════════════
#  HOJA 1 — INSTRUCCIONES
# ════════════════════════════════════════════════════════════════════════════

def build_instrucciones(wb):
    ws = wb.create_sheet("INSTRUCCIONES")
    ws.sheet_view.showGridLines = False

    # Título
    set_title(ws, 1, 1,
              "PLANTILLA ÍNDICE PVE — PACTO VERDE EUROPEO", 8)
    ws.row_dimensions[1].height = 32

    set_title(ws, 2, 1,
              "Clasificación de preparación y vulnerabilidad de cooperativas "
              "café y cacao ante el EUDR / Pacto Verde Europeo", 8)
    ws.row_dimensions[2].height = 22

    instructions = [
        ("PROPÓSITO", None),
        ("", "Esta plantilla calcula el Índice de Preparación ante el Pacto Verde "
             "Europeo (PVE) para cada una de las 174 organizaciones del universo. "
             "El índice es un score compuesto 0–100 que combina exposición al mercado "
             "UE, nivel de trazabilidad, capacidad organizacional y presión del "
             "comprador."),
        ("", ""),
        ("CÓMO FUNCIONA", None),
        ("", "La plantilla tiene 6 hojas. La hoja MATRIZ_174 contiene los datos "
             "existentes de cada organización. La hoja PREGUNTAS_PROXY contiene las "
             "preguntas de verificación rápida por dimensión. La hoja SCORECARDS "
             "calcula el PVE y muestra el semáforo."),
        ("", ""),
        ("FLUJO DE USO", None),
        ("Paso 1", "Revisar PONDERADORES — los pesos son editables en celdas amarillas"),
        ("Paso 2", "Ir a MATRIZ_174 — verificar/actualizar FOB, país destino, certificaciones"),
        ("Paso 3", "Para cada organización con FOB UE > 0, completar PREGUNTAS_PROXY "
                   "usando llamada telefónica o visita de 30 min"),
        ("Paso 4", "Revisar SCORECARDS — el semáforo se actualiza automáticamente"),
        ("Paso 5", "Usar RADAR_BRECHAS para comparación por departamento"),
        ("", ""),
        ("SEMÁFORO", None),
        ("🔴 Crítico (0–33)", "La cooperativa no puede generar la declaración EUDR. "
                               "Riesgo de rechazo en frontera UE desde dic 2026."),
        ("🟡 Vulnerable (34–66)", "Tiene infraestructura parcial pero incompleta. "
                                   "Necesita inversión en geolocalización y proceso."),
        ("🟢 Preparado (67–100)", "Cumple los requisitos mínimos. "
                                   "Requiere monitoreo de actualización."),
        ("", ""),
        ("NOTAS IMPORTANTES", None),
        ("", "• Las celdas en AMARILLO son inputs editables — puedes modificarlas directamente."),
        ("", "• Las celdas en BLANCO/NEGRO son fórmulas calculadas — no editarlas manualmente."),
        ("", "• Las celdas en GRIS son 'PENDIENTE' — falta capturar el dato."),
        ("", "• Losponderadores en HOJA 2 son los únicos ajustes que necesitas hacer."),
        ("", "• Para datos de campo, usar la hoja PREGUNTAS_PROXY como guía de entrevista."),
    ]

    row = 4
    for item in instructions:
        tag, text = item
        if tag and not text:
            # sección en negrita
            c = ws.cell(row=row, column=1, value=tag)
            c.font  = Font(bold=True, size=11, color="1F497D", name="Calibri")
            c.fill  = SUBHDR_FILL
            ws.merge_cells(start_row=row, start_column=1,
                           end_row=row, end_column=8)
            ws.row_dimensions[row].height = 18
        elif tag:
            c_tag = ws.cell(row=row, column=1, value=tag)
            c_tag.font  = Font(bold=True, size=10, name="Calibri")
            c_tag.border = THIN_BORDER
            ws.merge_cells(start_row=row, start_column=2,
                           end_row=row, end_column=8)
            c_val = ws.cell(row=row, column=2, value=text)
            c_val.font  = Font(size=10, name="Calibri")
            c_val.border = THIN_BORDER
        elif text:
            c = ws.cell(row=row, column=1, value="")
            ws.merge_cells(start_row=row, start_column=1,
                           end_row=row, end_column=8)
        row += 1

    for col in range(1, 9):
        ws.column_dimensions[get_column_letter(col)].width = 22
    ws.column_dimensions["A"].width = 20

# ════════════════════════════════════════════════════════════════════════════
#  HOJA 2 — PONDERADORES
# ════════════════════════════════════════════════════════════════════════════

def build_ponderadores(wb):
    ws = wb.create_sheet("PONDERADORES")
    ws.sheet_view.showGridLines = False

    set_title(ws, 1, 1,
              "BLOQUE DE SUPUESTOS — PONDERACIONES DEL ÍNDICE PVE", 4)
    ws.row_dimensions[1].height = 28

    # Leyenda
    set_subhdr(ws, 2, 1, "LEYENDA DE COLORES", 4)
    legends = [
        (3, "🔵 Azul",   "Input hardcoded — valor primario, editable"),
        (4, "⚫ Negro",  "Fórmula calculada — no editar manualmente"),
        (5, "🟡 Amarillo", "Input editable — cambiar ponderación aquí"),
        (6, "🟢 Verde",  "Resultado positivo (cumple)"),
        (7, "🔴 Rojo",   "Resultado negativo (no cumple)"),
        (8, "⬜ Gris",    "Dato pendiente de capturar"),
    ]
    for r, emoji_label, desc in legends:
        c = ws.cell(row=r, column=1, value=emoji_label)
        c.font = Font(name="Calibri", size=10)
        c.border = THIN_BORDER
        c2 = ws.cell(row=r, column=2, value=desc)
        c2.font = Font(name="Calibri", size=10)
        c2.border = THIN_BORDER

    # Título sección ponderadores
    set_subhdr(ws, 10, 1, "PONDERACIONES — MODIFICAR SOLO LAS CELDAS AMARILLAS", 4)

    # Headers
    for col, hdr in enumerate(
        ["Componente", "Dimensión EUDR", "Variable", "Ponderación (%)"], 1):
        set_header(ws, 11, col, hdr)

    # Componentes con ponderaciones
    components = [
        ("EXP_UE",     "D7 / Exposición UE",
         "% FOB exportado a UE sobre FOB total", 25),
        ("TRAZA",      "D2 / Trazabilidad",
         "¿Existe vínculo lote → parcela con coords?", 20),
        ("DILIG",      "D5 / Debida diligencia",
         "¿Existe proceso de evaluación de riesgo?", 15),
        ("CAPAC",      "D6 / Capacidad digital",
         "¿Tiene personal dedicado a datos?", 10),
        ("PRESION",    "D7 / Presión comprador",
         "¿Comprador UE exige EUDR?", 15),
        ("CERTIF",     "D8 / Certificaciones",
         "Score de certificaciones vigentes (Org + Ftrade)", 10),
        ("PPWR",       "D14 / Envases",
         "¿Usa sacos reutilizables o certificados?", 5),
    ]
    for i, (comp_id, dim, var, pct) in enumerate(components, 12):
        ws.row_dimensions[i].height = 18
        data_cell(ws, i, 1, comp_id)
        data_cell(ws, i, 2, dim)
        data_cell(ws, i, 3, var)
        # Input editable en amarillo
        c = input_cell(ws, i, 4, pct)
        c.number_format = "0"
        c.alignment = CENTER_ALIGN

    # Total debe sumar 100%
    total_row = 12 + len(components)
    ws.row_dimensions[total_row].height = 20
    data_cell(ws, total_row, 1, "TOTAL", font=Font(bold=True, name="Calibri"))
    ws.merge_cells(start_row=total_row, start_column=2,
                   end_row=total_row, end_column=3)
    c_total = ws.cell(row=total_row, column=4,
                      value=f"=SUM(D{12}:D{total_row-1})")
    c_total.font = Font(bold=True, name="Calibri", color="000000")
    c_total.fill = SUBHDR_FILL
    c_total.border = THIN_BORDER
    c_total.alignment = CENTER_ALIGN
    c_total.number_format = "0"

    # Nota sobre ajuste
    note_row = total_row + 2
    ws.merge_cells(start_row=note_row, start_column=1,
                   end_row=note_row, end_column=4)
    c = ws.cell(row=note_row, column=1,
                value="⚠  El TOTAL debe sumar 100. Si lo ajustas, "
                      "el Índice PVE en SCORECARDS se recalcula automáticamente.")
    c.font = Font(italic=True, color="9C0006", name="Calibri", size=10)

    # Column widths
    ws.column_dimensions["A"].width = 12
    ws.column_dimensions["B"].width = 24
    ws.column_dimensions["C"].width = 48
    ws.column_dimensions["D"].width = 16

# ════════════════════════════════════════════════════════════════════════════
#  HOJA 3 — MATRIZ_174
# ════════════════════════════════════════════════════════════════════════════

def build_matriz(wb):
    ws = wb.create_sheet("MATRIZ_174")
    ws.sheet_view.showGridLines = False

    # ── Cargar datos existentes ──
    csv_path = os.path.join(DATA_DIR, "MATRIZ_ORGANIZACIONES_174_FINAL.csv")
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path, encoding="utf-8-sig")
    else:
        df = pd.DataFrame()

    set_title(ws, 1, 1,
              "MATRIZ 174 — Datos existentes de organizaciones", 19)
    ws.row_dimensions[1].height = 28

    # ── Headers ──
    headers = [
        ("RUC", 14),
        ("Razón Social (SUNAT)", 38),
        ("Depto", 14),
        ("Producto", 12),
        ("FOB Total USD", 14),
        ("N° DUAs", 8),
        ("Exporta", 9),
        ("Cert. Orgánica", 14),
        ("Cert. Fairtrade", 14),
        ("Estado SUNAT", 14),
        ("Avance EUDR", 14),
        ("FOB UE USD", 14),
        ("% UE/FOB", 10),
        ("HS Code principal", 14),
        ("Score Cert (0-1)", 14),
        ("Tipo org.", 12),
        ("N° aprox. socios", 14),
        ("Hectáreas aprox.", 14),
        ("PVE Score (0-100)", 14),
        ("Clasificación", 14),
    ]
    for col, (hdr, width) in enumerate(headers, 1):
        set_header(ws, 2, col, hdr)
        ws.column_dimensions[get_column_letter(col)].width = width
    ws.row_dimensions[2].height = 28

    # ── Data rows ──
    def safe_col(df, col_name):
        matches = [c for c in df.columns if col_name.lower() in c.lower()]
        if matches:
            return df[matches[0]]
        return pd.Series([None]*len(df))

    n_rows = len(df) if not df.empty else 0

    for i, (_, row_data) in enumerate(df.iterrows(), 3):
        ws.row_dimensions[i].height = 16
        ruc        = str(row_data.get("RUC", ""))[:15]
        razon      = str(row_data.get("Razón Social (SUNAT)",
                                       row_data.get("Razon Social", "")))[:60]
        depto      = str(row_data.get("Departamento", ""))
        producto   = str(row_data.get("Producto dominante",
                                       row_data.get("Producto", "")))[:20]
        fob_raw    = row_data.get("FOB total USD (interno)", None)
        try:
            fob = float(fob_raw) if fob_raw not in (None, "", "nan") else 0
        except:
            fob = 0
        duas       = row_data.get("N° DUAs", 0)
        exporta    = str(row_data.get("Exporta (interno)", "NO"))[:3]
        cert_org   = str(row_data.get("Cert. Orgánica (interno)", "NO"))[:3]
        cert_ft    = str(row_data.get("Cert. Comercio Justo (interno)", "NO"))[:3]
        estado     = str(row_data.get("Estado SUNAT", ""))
        avance_eudr = str(row_data.get("Avance EUDR", ""))
        socios_raw = row_data.get("Socios (interno)", None)
        try:
            socios = float(socios_raw) if socios_raw not in (None, "", "nan") else None
        except:
            socios = None
        has_raw    = row_data.get("Hectáreas (interno)", None)
        try:
            has = float(has_raw) if has_raw not in (None, "", "nan") else None
        except:
            has = None

        # Columnas
        col_map = {
            1: ruc, 2: razon, 3: depto, 4: producto,
            5: fob, 6: duas,
        }

        for col, val in col_map.items():
            c = data_cell(ws, i, col, val)
            if col == 5:
                c.number_format = '#,##0'
            elif col == 6:
                c.alignment = CENTER_ALIGN

        # Exporta (SI/NO con color)
        ce = data_cell(ws, i, 7, exporta)
        ce.alignment = CENTER_ALIGN
        if exporta == "SI":
            ce.fill = GREEN_FILL
            ce.font = GREEN_FONT
        else:
            ce.fill = RED_FILL
            ce.font = RED_FONT

        # Certs
        for col, val in [(8, cert_org), (9, cert_ft)]:
            cc = data_cell(ws, i, col, val)
            cc.alignment = CENTER_ALIGN
            if val == "SI":
                cc.fill = GREEN_FILL
                cc.font = GREEN_FONT

        data_cell(ws, i, 10, estado).alignment = CENTER_ALIGN

        # Avance EUDR
        ca = data_cell(ws, i, 11, avance_eudr)
        ca.alignment = CENTER_ALIGN

        # FOB UE (pendiente — celda amarilla editable)
        input_cell(ws, i, 12, 0).number_format = '#,##0'
        ws.cell(row=i, column=12).alignment = RIGHT_ALIGN

        # % UE/FOB — fórmula: FOB UE (col L=12) / FOB total (col E=5)
        c_pct = ws.cell(row=i, column=13,
                         value=f"=IF(E{i}>0,ROUND(L{i}/E{i}*100,1),0)")
        c_pct.number_format = '0.0"%"'
        c_pct.border = THIN_BORDER
        c_pct.font = FORMULA_FONT
        c_pct.alignment = CENTER_ALIGN

        # HS Code (pendiente)
        pending_cell(ws, i, 14)

        # Score certificaciones (0-1) — fórmula
        c_sc = ws.cell(row=i, column=15,
                       value=f"=IF(H{i}=\"SI\",1,0)*0.6+IF(I{i}=\"SI\",1,0)*0.4")
        c_sc.number_format = '0.00'
        c_sc.border = THIN_BORDER
        c_sc.font = FORMULA_FONT
        c_sc.alignment = CENTER_ALIGN

        # Tipo org. (pendiente — clasificación regulatoria)
        pending_cell(ws, i, 16)

        # Socios aprox.
        if socios is not None:
            c_soc = data_cell(ws, i, 17, socios)
            c_soc.number_format = '#,##0'
        else:
            pending_cell(ws, i, 17)

        # Hectáreas aprox.
        if has is not None:
            c_has = data_cell(ws, i, 18, has)
            c_has.number_format = '#,##0.0'
        else:
            pending_cell(ws, i, 18)

        # PVE Score — referencia a SCORECARDS (se completará en hoja 5)
        c_pve = ws.cell(row=i, column=19,
                        value=f"=IFERROR(SCORECARDS!C{i-2},\"—\")")
        c_pve.border = THIN_BORDER
        c_pve.alignment = CENTER_ALIGN
        c_pve.number_format = '0.0'

        # Clasificación semáforo
        c_clas = ws.cell(row=i, column=20,
                         value=f'=IF(ISTEXT(S{i}),S{i},'
                                f'IF(S{i}<34,"🔴 Crítico",'
                                f'IF(S{i}<67,"🟡 Vulnerable","🟢 Preparado")))')
        c_clas.border = THIN_BORDER
        c_clas.alignment = CENTER_ALIGN

    # ── Conditional formatting para % UE ──
    from openpyxl.formatting.rule import ColorScaleRule
    ws.conditional_formatting.add(
        f"M3:M{2+n_rows}",
        ColorScaleRule(
            start_type="num", start_value=0, start_color="F8696B",
            mid_type="num",   mid_value=50,   mid_color="FFEB84",
            end_type="num",   end_value=100,   end_color="63BE7B"
        )
    )

    # Freeze panes
    ws.freeze_panes = "C3"

# ════════════════════════════════════════════════════════════════════════════
#  HOJA 4 — PREGUNTAS_PROXY
# ════════════════════════════════════════════════════════════════════════════

def build_preguntas(wb):
    ws = wb.create_sheet("PREGUNTAS_PROXY")
    ws.sheet_view.showGridLines = False

    set_title(ws, 1, 1,
              "PREGUNTAS PROXY — Verificación rápida por dimensión EUDR", 9)
    ws.row_dimensions[1].height = 28

    # Headers
    headers = [
        ("Dim.", 6), ("#", 5), ("Pregunta", 52),
        ("Respuesta", 16), ("Score (0-1)", 11),
        ("Variable", 14), ("Fuente", 16), ("Obs.", 22),
    ]
    for col, (hdr, width) in enumerate(headers, 1):
        set_header(ws, 2, col, hdr)
        ws.column_dimensions[get_column_letter(col)].width = width
    ws.row_dimensions[2].height = 22

    # ── Preguntas por dimensión ──
    # (dim_id, num, pregunta, tipo, opciones, var_score, fuente, obs)
    preguntas = [
        # D1 — Clasificación regulatoria
        ("D1", "D1.1",
         "¿Cuál es el rol principal de la organización?",
         "choice", "Operador directo (exporta bajo su RUC) / Comerciante (compra a socios) / Micro-operador (vende a exportador)", "",
         "Entrevista directiva / SUNAT"),
        ("D1", "D1.2",
         "¿La organización está inscrita en el RNCA (Registro Nacional de Cooperativas Agrarias)?",
         "yesno", "Sí / No / No sabe", "",
         "SUNAT / MIDAGRI RNCA"),
        ("D1", "D1.3",
         "¿Exporta directamente bajo su propio RUC (no a través de un agente)?",
         "yesno", "Sí / No / Parcialmente", "",
         "ADUANET / DUAs"),

        # D2 — Trazabilidad
        ("D2", "D2.1",
         "¿Existe al menos un registro donde cada lote exportado esté vinculado a la parcela de origen?",
         "yesno", "Sí / Parcialmente / No", "",
         "Entrevista + revisión documentos"),
        ("D2", "D2.2",
         "¿Se registran las coordenadas geográficas de las parcelas de los socios?",
         "yesno", "Sí, todas / Sí, algunas / No", "",
         "Entrevista + evidencia"),
        ("D2", "D2.3",
         "¿Con qué frecuencia se actualizan las coordenadas de parcelas?",
         "choice", "Cada campaña / Cada año / Cuando hay reclamo / Nunca", "",
         "Entrevista"),
        ("D2", "D2.4",
         "¿Se usa balance de masas (mezcla de lotes sin segregación física)?",
         "yesno", "Sí / No", "",
         "Entrevista — ROJO si dice Sí",
         "⚠ Bal. de masas prohibido bajo EUDR"),
        ("D2", "D2.5",
         "¿Los proveedores externos (no socios) representan volumen significativo?",
         "pct", "0-100%", "",
         "Entrevista"),
        ("D2", "D2.6",
         "¿Se registra la trazabilidad de proveedores externos (nombre, cantidad, origen)?",
         "yesno", "Sí / Parcialmente / No", "",
         "Entrevista"),

        # D3 — Legalidad
        ("D3", "D3.1",
         "¿Qué porcentaje aproximado de los socios tiene título de propiedad o constancia de posesión inscrita en SUNARP?",
         "pct", "0-100%", "",
         "Entrevista / MIDAGRI"),
        ("D3", "D3.2",
         "¿La zona de producción está en un área natural protegida o zona de amortiguamiento?",
         "yesno", "Sí / No / No sabe", "",
         "GEOSERFOR / SINIA"),
        ("D3", "D3.3",
         "¿La organización cuenta con autorizaciones ambientales vigentes (EIA, DIA, certificación forestal)?",
         "yesno", "Sí / No / En proceso", "",
         "Entrevista / OEFA"),
        ("D3", "D3.4",
         "¿Hay algún proceso sancionador vigente de OEFA o SINEFA contra la organización?",
         "yesno", "Sí / No / No sabe", "",
         "OEFA / SINEFA"),

        # D4 — Deforestación
        ("D4", "D4.1",
         "¿La organización ha realizado cruces de sus parcelas contra mapas de deforestación (GEOSERFOR / PNCB)?",
         "yesno", "Sí / No / No sabe", "",
         "Entrevista / verificación web"),
        ("D4", "D4.2",
         "¿Se han detectado alertas de deforestación en parcelas de la organización?",
         "yesno", "Sí / No / No sabe", "",
         "GEOSERFOR / GFW"),

        # D5 — Debida diligencia
        ("D5", "D5.1",
         "¿Existe un proceso documentado para evaluar riesgo de deforestación antes de exportar?",
         "yesno", "Sí / Parcialmente / No", "",
         "Entrevista + revisión docs"),
        ("D5", "D5.2",
         "¿Se registran las alertas o rechazos de compradores europeos en los últimos 2 años?",
         "yesno", "Sí / No / No aplica", "",
         "Entrevista"),
        ("D5", "D5.3",
         "¿La organización elabora un reporte periódico de debida diligencia?",
         "choice", "Sí, con indicadores / Sí, básico / No", "",
         "Entrevista"),

        # D6 — Capacidad organizacional
        ("D6", "D6.1",
         "¿Hay personal dedicado (tiempo completo o parcial) a tareas de gestión de datos o sistemas?",
         "yesno", "Sí, FT / Sí, PT / No", "",
         "Entrevista"),
        ("D6", "D6.2",
         "¿La organización tiene acceso a internet estable en su sede?",
         "yesno", "Sí / Parcial / No", "",
         "Entrevista"),
        ("D6", "D6.3",
         "¿Usa algún software o herramienta digital para gestionar trazabilidad?",
         "choice", "App propia / App de comprador o proyecto / Excel / Ninguno", "",
         "Entrevista"),
        ("D6", "D6.4",
         "¿El presupuesto anual incluye una partida para tecnología o datos?",
         "yesno", "Sí / No / No sabe", "",
         "Entrevista directiva"),

        # D7 — Presión del comprador
        ("D7", "D7.1",
         "¿Cuál es el destino principal de las exportaciones?",
         "choice", "Europa / EE.UU. / Asia / Mercado interno / No exporta", "",
         "DUAs / Entrevista"),
        ("D7", "D7.2",
         "¿El comprador principal (primera mano) es una empresa europea o está sujeta a CS3D?",
         "yesno", "Sí / No / No sabe", "",
         "Entrevista / web"),
        ("D7", "D7.3",
         "¿El comprador ha solicitado evidencia de trazabilidad o geolocalización?",
         "yesno", "Sí, formalmente / Sí, informalmente / No", "",
         "Entrevista"),
        ("D7", "D7.4",
         "¿Hay contrato escrito con cláusula EUDR o debida diligencia?",
         "yesno", "Sí / No / No sabe", "",
         "Entrevista / docs legales"),

        # D8 — Gobernanza
        ("D8", "D8.1",
         "¿Los socios conocen los requisitos EUDR y sus implicancias?",
         "yesno", "Sí / Parcialmente / No", "",
         "Entrevista + observación"),
        ("D8", "D8.2",
         "¿Existe un mecanismo formal para que los socios entreguen datos de parcelas?",
         "yesno", "Sí / Parcialmente / No", "",
         "Entrevista"),

        # D9 — Sostenibilidad económica
        ("D9", "D9.1",
         "¿La organización ha estimado el costo de adecuación al EUDR?",
         "yesno", "Sí / No / No sabe", "",
         "Entrevista directiva"),
        ("D9", "D9.2",
         "¿Existe una fuente de financiamiento identificada para la adecuación?",
         "yesno", "Sí / No / En gestión", "",
         "Entrevista"),

        # D10 — Confusión certificación / EUDR
        ("D10", "D10.1",
         "¿La organización cree que sus certificaciones (Orgánica, Fairtrade, Rainforest) cubren los requisitos EUDR?",
         "yesno", "Sí / No / No sabe", "",
         "Entrevista — ROJO si dice Sí sin entender EUDR"),
        ("D10", "D10.2",
         "¿Ha recibido asesoría específica sobre EUDR (no solo genérica de sostenibilidad)?",
         "yesno", "Sí / No", "",
         "Entrevista"),

        # D11 — Ecosistema de apoyo
        ("D11", "D11.1",
         "¿Conoce programas de MIDAGRI, GIZ, EFI, PROMPERÚ o cooperación para apoyo EUDR?",
         "yesno", "Sí, los usa / Sí, los conoce / No", "",
         "Entrevista"),
        ("D11", "D11.2",
         "¿Está inscrita en la plataforma de trazabilidad de APPCACAO o JNC?",
         "yesno", "Sí / En proceso / No", "",
         "Verificación web + entrevista"),

        # PPWR — Envases
        ("PPWR", "P1",
         "¿Qué tipo de sacos de exportación usa principalmente?",
         "choice", "Yute reutilizable / Yute nuevo / Big bags reciclables / Bolsas papel / Otro", "",
         "Entrevista"),
        ("PPWR", "P2",
         "¿Los sacos tienen certificación FSC o equivalente?",
         "yesno", "Sí / No / No sabe", "",
         "Entrevista / proveedor"),
    ]

    # Grupo de preguntas por dimensión
    current_dim = None
    row = 3

    # Scores por respuesta
    yesno_scores = {"Sí": 1.0, "Parcialmente": 0.5, "No": 0.0,
                    "Sí, todas": 1.0, "Sí, algunas": 0.5,
                    "Sí, FT": 1.0, "Sí, PT": 0.6,
                    "Sí, formalmente": 1.0, "Sí, informalmente": 0.5,
                    "Sí, con indicadores": 1.0, "Sí, básico": 0.5,
                    "Sí, los usa": 1.0, "Sí, los conoce": 0.5,
                    "En proceso": 0.5, "En gestión": 0.5,
                    "Sí, lo sabe": 0.5,
                    "Europa": 1.0, "EE.UU.": 0.3, "Asia": 0.1,
                    "Mercado interno": 0.0, "No exporta": 0.0,
                    "App propia": 1.0, "App de comprador o proyecto": 0.7,
                    "Excel": 0.4, "Ninguno": 0.0,
                    "Yute reutilizable": 1.0, "Big bags reciclables": 0.8,
                    "Yute nuevo": 0.3, "Bolsas papel": 0.2, "Otro": 0.1}

    dim_colors = {
        "D1":  "4472C4", "D2":  "ED7D31", "D3":  "A9D18E",
        "D4":  "FF0000", "D5":  "9DC3E6", "D6":  "FFC000",
        "D7":  "7030A0", "D8":  "00B0F0", "D9":  "92D050",
        "D10": "FF6600", "D11": "C9A227", "PPWR": "808080",
    }

    dim_row_start = {}
    dim_row_end   = {}

    for item in preguntas:
        dim_id = item[0]
        num    = item[1]
        preg   = item[2]
        opts   = item[4]
        fuente = item[6]
        obs    = item[7] if len(item) > 7 else ""

        # Nueva dimensión → header de grupo
        if dim_id != current_dim:
            current_dim = dim_id
            dim_row_start[dim_id] = row
            fill_color = dim_colors.get(dim_id, "4472C4")
            hdr_fill = PatternFill("solid", fgColor=fill_color)
            hdr_font = Font(bold=True, color="FFFFFF", name="Calibri", size=11)
            ws.merge_cells(start_row=row, start_column=1,
                           end_row=row, end_column=8)
            c = ws.cell(row=row, column=1,
                        value=f"DIMENSIÓN {dim_id}  —  "
                              f"{get_dim_label(dim_id)}")
            c.font = hdr_font
            c.fill = hdr_fill
            c.alignment = LEFT_ALIGN
            ws.row_dimensions[row].height = 20
            row += 1

        ws.row_dimensions[row].height = 22
        # Dimensión y número
        data_cell(ws, row, 1, dim_id).alignment = CENTER_ALIGN
        data_cell(ws, row, 2, num.split(".")[-1]).alignment = CENTER_ALIGN
        # Pregunta
        cp = data_cell(ws, row, 3, preg)
        cp.alignment = LEFT_ALIGN
        # Respuesta — dropdown editable
        input_cell(ws, row, 4, "")
        ws.cell(row=row, column=4).alignment = CENTER_ALIGN
        # Opciones dropdown
        if opts:
            opts_list = ";".join(opts.split(" / "))
            dv_dropdown(ws, f'"{opts_list}"',
                        f"D{row}")
        # Score — serie de IF anidados que evitan {arrays} de Excel
        # Scores para respuestas "Sí" de alto valor
        score_val = (
            '=IF(D{r}="Sí",1,'
            'IF(D{r}="Sí, todas",1,'
            'IF(D{r}="Sí, FT",1,'
            'IF(D{r}="Sí, PT",0.6,'
            'IF(D{r}="Sí, formalmente",1,'
            'IF(D{r}="Sí, informalmente",0.5,'
            'IF(D{r}="Sí, con indicadores",1,'
            'IF(D{r}="Sí, básico",0.5,'
            'IF(D{r}="Sí, los usa",1,'
            'IF(D{r}="Sí, los conoce",0.5,'
            'IF(D{r}="Parcialmente",0.5,'
            'IF(D{r}="Sí, algunas",0.5,'
            'IF(D{r}="Europa",1,'
            'IF(D{r}="EE.UU.",0.3,'
            'IF(D{r}="Asia",0.1,'
            'IF(D{r}="Mercado interno",0,'
            'IF(D{r}="No exporta",0,'
            'IF(D{r}="App propia",1,'
            'IF(D{r}="App de comprador o proyecto",0.7,'
            'IF(D{r}="Excel",0.4,'
            'IF(D{r}="Ninguno",0,'
            'IF(D{r}="Yute reutilizable",1,'
            'IF(D{r}="Big bags reciclables",0.8,'
            'IF(D{r}="Yute nuevo",0.3,'
            'IF(D{r}="Bolsas papel",0.2,'
            'IF(D{r}="Otro",0.1,'
            'IF(D{r}="En proceso",0.5,'
            'IF(D{r}="En gestión",0.5,'
            'IF(D{r}="No sabe",0.3,'
            'IF(D{r}="No aplica",0.5,'
            'IF(D{r}="No",0,'
            'IF(D{r}="",0,'
            'IF(ISTEXT(D{r}),0.5,0)'
            ')))))))))))))))))))))))))'
        ).format(r=row)
        c_score = ws.cell(row=row, column=5, value=score_val)
        c_score.number_format = '0.00'
        c_score.border = THIN_BORDER
        c_score.font = FORMULA_FONT
        c_score.alignment = CENTER_ALIGN
        # Variable
        data_cell(ws, row, 6, get_var_name(dim_id, num)).alignment = CENTER_ALIGN
        # Fuente
        data_cell(ws, row, 7, fuente).alignment = CENTER_ALIGN
        # Obs
        if obs:
            co = data_cell(ws, row, 8, obs)
            co.font = Font(italic=True, color="9C0006", name="Calibri", size=9)
        else:
            ws.cell(row=row, column=8).border = THIN_BORDER

        dim_row_end[dim_id] = row
        row += 1

    # ── Resumen por dimensión ──
    row += 1
    set_title(ws, row, 1, "RESUMEN DE SCORES POR DIMENSIÓN", 8)
    ws.row_dimensions[row].height = 22
    row += 1

    for col, hdr in enumerate(["Dimensión", "Score promedio", "N° preguntas", "Nivel"], 1):
        set_header(ws, row, col, hdr)
    row += 1

    for dim_id in ["D1","D2","D3","D4","D5","D6","D7","D8","D9","D10","D11","PPWR"]:
        if dim_id not in dim_row_start:
            continue
        rs = dim_row_start[dim_id]
        re = dim_row_end[dim_id]
        label = get_dim_label(dim_id)
        c1 = data_cell(ws, row, 1, f"{dim_id} — {label}")
        c2 = ws.cell(row=row, column=2,
                     value=f"=IFERROR(AVERAGEIF(E{rs}:E{re},\">0\"),0)")
        c2.number_format = '0.00'
        c2.alignment = CENTER_ALIGN
        c3 = ws.cell(row=row, column=3,
                     value=f'=COUNTIF(E{rs}:E{re},">0")')
        c3.alignment = CENTER_ALIGN
        c4 = ws.cell(row=row, column=4,
                     value=f'=IF(B{row}>=0.67,"🟢 Verde",IF(B{row}>=0.34,"🟡 Amarillo","🔴 Rojo"))')
        c4.alignment = CENTER_ALIGN
        row += 1

    ws.freeze_panes = "A3"


def get_dim_label(dim_id):
    labels = {
        "D1": "Clasificación regulatoria",
        "D2": "Trazabilidad y geolocalización",
        "D3": "Legalidad de la producción",
        "D4": "Riesgo de deforestación",
        "D5": "Sistema de debida diligencia",
        "D6": "Capacidad organizacional y digital",
        "D7": "Posición en la cadena de valor",
        "D8": "Gobernanza y participación de socios",
        "D9": "Sostenibilidad económica del cumplimiento",
        "D10": "Confusión certificación / EUDR",
        "D11": "Ecosistema de apoyo externo",
        "PPWR": "Envases y Packaging (PPWR)",
    }
    return labels.get(dim_id, dim_id)


def get_var_name(dim_id, num):
    var_map = {
        "D1.1": "tipo_rol", "D1.2": "rnca", "D1.3": "exporta_directo",
        "D2.1": "lote_parcela", "D2.2": "coords", "D2.3": "frec_coords",
        "D2.4": "bal_masas", "D2.5": "pct_ext", "D2.6": "traza_ext",
        "D3.1": "pct_titulo", "D3.2": "anp", "D3.3": "aut_ambiental",
        "D3.4": "sancion_oea",
        "D4.1": "cruce_deforest", "D4.2": "alerta_deforest",
        "D5.1": "proc_dd", "D5.2": "reg_rechazos", "D5.3": "reporte_dd",
        "D6.1": "personal_datos", "D6.2": "internet", "D6.3": "sw_trazabilidad",
        "D6.4": "presupuesto_tech",
        "D7.1": "destino_principal", "D7.2": "comprador_ue", "D7.3": "exige_evidencia",
        "D7.4": "contrato_eudr",
        "D8.1": "socios_conocen", "D8.2": "mec_entrega",
        "D9.1": "costo_estimado", "D9.2": "financiamiento",
        "D10.1": "cree_cubierta", "D10.2": "asesoria_eudr",
        "D11.1": "prog_apoyo", "D11.2": "plataforma_traz",
        "P1": "tipo_saco", "P2": "fsc",
    }
    return var_map.get(num, f"{dim_id}_{num}")


# ════════════════════════════════════════════════════════════════════════════
#  HOJA 5 — SCORECARDS
# ════════════════════════════════════════════════════════════════════════════

def build_scorecards(wb):
    ws = wb.create_sheet("SCORECARDS")
    ws.sheet_view.showGridLines = False

    set_title(ws, 1, 1,
              "SCORECARDS — Índice PVE por organización (0-100)", 15)
    ws.row_dimensions[1].height = 28

    headers = [
        ("RUC", 14), ("Razón Social", 38), ("PVE Score", 11),
        ("Semáforo", 14), ("Ranking", 8), ("FOB UE USD", 14),
        ("% UE/FOB", 10), ("Trazab. (D2)", 11), ("Dilig. (D5)", 12),
        ("Capacidad (D6)", 13), ("Presión (D7)", 12), ("Cert (0-1)", 10),
        ("PPWR", 8), ("Depto", 14), ("Segmento", 16),
    ]
    for col, (hdr, width) in enumerate(headers, 1):
        set_header(ws, 2, col, hdr)
        ws.column_dimensions[get_column_letter(col)].width = width
    ws.row_dimensions[2].height = 22

    # ── Scores por dimensión — pesos ──
    # Se referencian a PONDERADORES!D12:D18
    # scores: 0-1 en cada dimensión
    # PVE = Σ(score_dim × peso_dim / 100)

    dv_seg = DataValidation(type="list",
                            formula1='"🔴 Crítico,🟡 Vulnerable,🟢 Preparado"',
                            allow_blank=True, showDropDown=False)
    dv_seg.sqref = "D3:D180"
    ws.add_data_validation(dv_seg)

    # Cargar RUCS de MATRIZ_174
    csv_path = os.path.join(DATA_DIR, "MATRIZ_ORGANIZACIONES_174_FINAL.csv")
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path, encoding="utf-8-sig")
    else:
        df = pd.DataFrame()

    for i, (_, row_data) in enumerate(df.iterrows(), 3):
        ws.row_dimensions[i].height = 16
        ruc   = str(row_data.get("RUC", ""))[:15]
        razon = str(row_data.get("Razón Social (SUNAT)",
                                  row_data.get("Razon Social", "")))[:60]
        depto = str(row_data.get("Departamento", ""))
        fob_raw = row_data.get("FOB total USD (interno)", 0)
        try:
            fob = float(fob_raw) if fob_raw not in (None, "", "nan") else 0
        except:
            fob = 0

        # RUC y Razón
        data_cell(ws, i, 1, ruc)
        data_cell(ws, i, 2, razon)
        data_cell(ws, i, 15, depto).alignment = CENTER_ALIGN

        # FOB UE (referencia a MATRIZ_174)
        c_fob_ue = ws.cell(row=i, column=6,
                           value=f"=IFERROR(MATRIZ_174!L{i},0)")
        c_fob_ue.number_format = '#,##0'
        c_fob_ue.border = THIN_BORDER
        c_fob_ue.alignment = RIGHT_ALIGN

        # % UE (referencia)
        c_pct = ws.cell(row=i, column=7,
                        value=f"=IFERROR(MATRIZ_174!M{i},0)")
        c_pct.number_format = '0.0"%"'
        c_pct.border = THIN_BORDER
        c_pct.alignment = CENTER_ALIGN

        # Trazabilidad D2 — score proxy editable
        # Por ahora 0 (pendiente de campo)
        input_cell(ws, i, 8, 0)
        ws.cell(row=i, column=8).number_format = '0.00'
        ws.cell(row=i, column=8).alignment = CENTER_ALIGN

        # Debida diligencia D5 — score proxy editable
        input_cell(ws, i, 9, 0)
        ws.cell(row=i, column=9).number_format = '0.00'
        ws.cell(row=i, column=9).alignment = CENTER_ALIGN

        # Capacidad D6 — score proxy editable
        input_cell(ws, i, 10, 0)
        ws.cell(row=i, column=10).number_format = '0.00'
        ws.cell(row=i, column=10).alignment = CENTER_ALIGN

        # Presión comprador D7 — score proxy editable
        input_cell(ws, i, 11, 0)
        ws.cell(row=i, column=11).number_format = '0.00'
        ws.cell(row=i, column=11).alignment = CENTER_ALIGN

        # Cert score (referencia MATRIZ_174 col 15 = score cert)
        c_cert = ws.cell(row=i, column=12,
                         value=f"=IFERROR(MATRIZ_174!O{i},0)")
        c_cert.number_format = '0.00'
        c_cert.border = THIN_BORDER
        c_cert.alignment = CENTER_ALIGN

        # PPWR — score proxy editable
        input_cell(ws, i, 13, 0)
        ws.cell(row=i, column=13).number_format = '0.00'
        ws.cell(row=i, column=13).alignment = CENTER_ALIGN

        # ── PVE Score ──
        # PVE = EXP_UE × %(col G=7) + TRAZA × D2(col H=8) + DILIG × D5(col I=9)
        #     + CAPAC × D6(col J=10) + PRESION × D7(col K=11)
        #     + CERTIF × cert(col L=12) + PPWR × PPWR(col M=13)
        # Cada ponderador es % directo; scores son 0-1
        pve_formula = (
            f"=ROUND("
            f"PONDERADORES!$D$12*G{i}"
            f"+PONDERADORES!$D$13*H{i}"
            f"+PONDERADORES!$D$14*I{i}"
            f"+PONDERADORES!$D$15*J{i}"
            f"+PONDERADORES!$D$16*K{i}"
            f"+PONDERADORES!$D$17*L{i}"
            f"+PONDERADORES!$D$18*M{i}"
            f",1)"
        )
        ws.cell(row=i, column=3, value=pve_formula)
        c_pve = ws.cell(row=i, column=3)
        c_pve.number_format = '0.0'
        c_pve.border = THIN_BORDER
        c_pve.alignment = CENTER_ALIGN
        c_pve.font = Font(bold=True, name="Calibri", size=10, color="000000")

        # Semáforo
        semaforo_formula = (
            "=IF(C" + str(i) + "<34,"
            + '"🔴 Critico",'
            + "IF(C" + str(i) + "<67,"
            + '"🟡 Vulnerable",'
            + '"🟢 Preparado"))'
        )
        c_sem = ws.cell(row=i, column=4, value=semaforo_formula)
        c_sem.border = THIN_BORDER
        c_sem.alignment = CENTER_ALIGN

        # Ranking
        rank_formula = '=IFERROR(RANK(C' + str(i) + ',C:C,-1),"")'
        c_rank = ws.cell(row=i, column=5, value=rank_formula)
        c_rank.border = THIN_BORDER
        c_rank.alignment = CENTER_ALIGN

        # Segmento
        seg_formula = (
            '=IF(AND(F' + str(i) + '>0,C' + str(i) + '<34),'
            + '"🔴 UE + Critico",'
            + 'IF(AND(F' + str(i) + '>0,C' + str(i) + '<67),'
            + '"🟡 UE + Vulnerable",'
            + 'IF(AND(F' + str(i) + '>0,C' + str(i) + '>=67),'
            + '"🟢 UE + Preparado",'
            + 'IF(C' + str(i) + '=0,"— Sin dato","Sin exposición UE"))))'
        )
        c_seg = ws.cell(row=i, column=14, value=seg_formula)
        c_seg.border = THIN_BORDER
        c_seg.alignment = CENTER_ALIGN

    # ── Conditional formatting semáforo ──
    n_rows = len(df) if not df.empty else 174
    ws.conditional_formatting.add(
        f"C3:C{2+n_rows}",
        CellIsRule(operator="lessThan", formula=["34"],
                   fill=RED_FILL, font=RED_FONT)
    )
    ws.conditional_formatting.add(
        f"C3:C{2+n_rows}",
        CellIsRule(operator="between", formula=["34", "66"],
                   fill=YELLOW_FILL, font=YELLOW_FONT)
    )
    ws.conditional_formatting.add(
        f"C3:C{2+n_rows}",
        CellIsRule(operator="greaterThanOrEqual", formula=["67"],
                   fill=GREEN_FILL, font=GREEN_FONT)
    )

    # ── Resumen ejecutivo ──
    sum_row = 3 + n_rows + 2
    set_title(ws, sum_row, 1, "RESUMEN EJECUTIVO", 7)
    ws.row_dimensions[sum_row].height = 22

    summary_items = [
        (sum_row+1, "Total organizaciones", f"=COUNTA(A3:A{2+n_rows})"),
        (sum_row+2, "Con exposición UE (FOB UE > 0)", f'=COUNTIF(F3:F{2+n_rows},">0")'),
        (sum_row+3, "🔴 Críticos (0-33)", f'=COUNTIF(C3:C{2+n_rows},"<34")-COUNTIF(C3:C{2+n_rows},0)'),
        (sum_row+4, "🟡 Vulnerables (34-66)", f'=COUNTIFS(C3:C{2+n_rows},">=34",C3:C{2+n_rows},"<67")'),
        (sum_row+5, "🟢 Preparados (67-100)", f'=COUNTIF(C3:C{2+n_rows},">=67")'),
        (sum_row+6, "Sin dato (score = 0)", f'=COUNTIF(C3:C{2+n_rows},0)'),
        (sum_row+7, "PVE promedio (con dato)", f'=IFERROR(AVERAGEIF(C3:C{2+n_rows},">0"),"N/A")'),
        (sum_row+8, "FOB total expuesto a UE (USD)", f'=SUMIF(F3:F{2+n_rows},">0",F3:F{2+n_rows})'),
    ]
    for r, label, formula in summary_items:
        ws.row_dimensions[r].height = 18
        c1 = data_cell(ws, r, 1, label)
        c1.font = Font(bold=True, name="Calibri", size=10)
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=4)
        c2 = ws.cell(row=r, column=2, value=formula)
        c2.border = THIN_BORDER
        c2.font = Font(name="Calibri", size=10)
        if "USD" in label:
            c2.number_format = '$#,##0'
        elif "%" in label:
            c2.number_format = '0.0'
        elif "promedio" in label.lower():
            c2.number_format = '0.0'

    ws.freeze_panes = "C3"


# ════════════════════════════════════════════════════════════════════════════
#  HOJA 6 — RADAR_BRECHAS
# ════════════════════════════════════════════════════════════════════════════

def build_radar(wb):
    ws = wb.create_sheet("RADAR_BRECHAS")
    ws.sheet_view.showGridLines = False

    set_title(ws, 1, 1,
              "RADAR DE BRECHAS — Score promedio por departamento y dimensión", 10)
    ws.row_dimensions[1].height = 28

    # Headers
    deptos = ["SAN MARTIN","JUNIN","AMAZONAS","CAJAMARCA","CUSCO",
              "UCAYALI","PASCO","PIURA","AYACUCHO","PUNO",
              "APURIMAC","MADRE DE DIOS","LORETO","LAMBAYEQUE","OTROS"]
    dim_ids  = ["D1","D2","D3","D4","D5","D6","D7","D8","D9","D10","D11"]

    col = 1
    set_header(ws, 2, col, "Departamento / Dimensión")
    ws.column_dimensions["A"].width = 28
    for d in dim_ids:
        col += 1
        c = set_header(ws, 2, col, d)
        ws.column_dimensions[get_column_letter(col)].width = 10
    col += 1
    set_header(ws, 2, col, "PVE Promedio")
    ws.column_dimensions[get_column_letter(col)].width = 12

    # Data rows — scores por depto (promedio de SCORECARDS)
    # Fórmula: promediar los scores de cada dimensión para las orgs de cada depto
    for r_dep, depto in enumerate(deptos, 3):
        ws.row_dimensions[r_dep].height = 18
        c1 = data_cell(ws, r_dep, 1, depto)
        c1.font = Font(bold=True, name="Calibri", size=10)
        scores = []
        for r_dim, dim_id in enumerate(dim_ids, 2):
            # Score promedio para este depto en esta dimensión
            # Promedio simple de SCORECARDS!col según deptos
            # Como SCORECARDS no tiene deptos, usamos MATRIZ_174 como join
            # Ref: promediar la col de scorecards que corresponde
            # Para D2=Col8, D5=Col9, D6=Col10, D7=Col11
            dim_col_map = {
                "D1": "PONDERADORES!$D$12",
                "D2": "H", "D3": "H", "D4": "H", "D5": "I",
                "D6": "J", "D7": "K", "D8": "H", "D9": "H",
                "D10": "H", "D11": "H",
            }
            # Para las dims sin score directo en SCORECARDS,
            # usamos 0 como placeholder (se completan al填 campos)
            # El radar muestra el estado actual de captura
            if dim_id in ("D2","D5","D6","D7","PPWR"):
                col_letter = {"D2":"H","D5":"I","D6":"J","D7":"K","PPWR":"M"}[dim_id]
                formula = (f"=IFERROR(AVERAGEIF(MATRIZ_174!C:C,A{r_dep},"
                           f"SCORECARDS!{col_letter}:{col_letter}),0)")
            else:
                formula = "=0"
            c = ws.cell(row=r_dep, column=r_dim, value=formula)
            c.number_format = '0.00'
            c.border = THIN_BORDER
            c.alignment = CENTER_ALIGN
            scores.append(f"{dim_id}={r_dim}")

        # PVE promedio por depto
        dim_start = 2
        dim_end   = 2 + len(dim_ids) - 1
        c_pve = ws.cell(row=r_dep, column=col,
                        value=f"=IFERROR(AVERAGE(B{r_dep}:{get_column_letter(dim_end)}{r_dep}),0)")
        c_pve.number_format = '0.00'
        c_pve.border = THIN_BORDER
        c_pve.font = Font(bold=True, name="Calibri", size=10)
        c_pve.alignment = CENTER_ALIGN

    # ── Leyenda de colores ──
    leg_row = 3 + len(deptos) + 2
    set_title(ws, leg_row, 1, "LEYENDA — NIVELES DE CUMPLIMIENTO", 7)
    ws.row_dimensions[leg_row].height = 20
    for r, (label, fill, font_c) in enumerate([
        ("🟢 Verde (0.67–1.00) — Cumplimiento adecuado", GREEN_FILL, GREEN_FONT),
        ("🟡 Amarillo (0.34–0.66) — Brecha moderada", YELLOW_FILL, YELLOW_FONT),
        ("🔴 Rojo (0.00–0.33) — Brecha crítica", RED_FILL, RED_FONT),
        ("⬜ Gris (0.00) — Sin dato capturado", PENDING_FILL, PENDING_FONT),
    ], leg_row+1):
        ws.row_dimensions[r].height = 18
        c = ws.cell(row=r, column=1, value=label)
        c.fill = fill
        c.font = font_c
        c.border = THIN_BORDER
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=7)

    # ── Nota ──
    note_row = leg_row + 6
    ws.merge_cells(start_row=note_row, start_column=1,
                   end_row=note_row, end_column=7)
    c = ws.cell(row=note_row, column=1,
                value="NOTA: Los scores en D2, D5, D6, D7 corresponden a los valores "
                      "ingresados manualmente en SCORECARDS. Completar la hoja PREGUNTAS_PROXY "
                      "y transferir los scores a SCORECARDS para actualizar este radar.")
    c.font = Font(italic=True, name="Calibri", size=9, color="595959")


# ════════════════════════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════════════════════════

def main():
    wb = openpyxl.Workbook()
    # remove default sheet first
    default_sheet = wb.active
    wb.remove(default_sheet)

    print("Construyendo INSTRUCCIONES...")
    build_instrucciones(wb)

    print("Construyendo PONDERADORES...")
    build_ponderadores(wb)

    print("Construyendo MATRIZ_174...")
    build_matriz(wb)

    print("Construyendo PREGUNTAS_PROXY...")
    build_preguntas(wb)

    print("Construyendo SCORECARDS...")
    build_scorecards(wb)

    print("Construyendo RADAR_BRECHAS...")
    build_radar(wb)

    print(f"Guardando: {OUT_FILE}")
    wb.save(OUT_FILE)
    print("✅ Plantilla PVE creada exitosamente.")
    print(f"   Archivo: {OUT_FILE}")
    import os
    size_kb = os.path.getsize(OUT_FILE) // 1024
    print(f"   Tamaño: {size_kb} KB")


if __name__ == "__main__":
    main()
