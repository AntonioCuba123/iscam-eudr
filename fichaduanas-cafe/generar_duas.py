"""
Extraccion de DUAs (SUNAT) desde PDF -> DUAS_POR_RUC.xlsx
=========================================================

Los PDF de `fichaduanas` son de dos tipos y ambos describen la MISMA DUA:

  Serie    (A1+A2)  un PDF por ITEM.  Trae el detalle de la mercancia:
                      subpartida, bultos, pesos, unidad comercial, FOB, descripcion.
  Consulta (A1)      un PDF por DUA.   Trae la cabecera y los totales:
                      transportista,Deposito, modalidad, valor clausula, y los
                      totales de "OTROS DATOS".

Tener el Serie equivale a tener la DUA. La cabecera es informacion adicional.

Como se lee el PDF
------------------
PyMuPDF devuelve cada palabra con su caja (x0, y0, x1, y1, texto). El formulario
es una tabla, asi que:
  1) FILAS: se agrupan las palabras por su coordenada Y.
  2) ETIQUETAS: una fila es etiqueta si contiene un codigo de campo ("3.1",
     "7.12"), si es un titulo de seccion ("3 TRANSPORTE") o si es texto de
     encabezado ("Codigo", "Fecha", "OTROS DATOS"...).
  3) VALORES: de cada etiqueta se baja a la fila de valores, que esta a un
     offset vertical fijo medido (SER_DY / SEC_DY). El offset se calibra por
     aduana porque el alto de la cabecera varia, nunca por coordenada absoluta.
  4) COLUMNAS: dentro de la fila de valores cada campo se recorta por su banda
     X (band/bnum). Las X si son estables entre archivos.

Evidencia de calibracion
------------------------
  3 aduanas: 046 Paita, 118 Callao, 235 Aerea. Dispersion maxima entre ellas
  ~1.6 px, asi que una tolerancia de 3 px cubre los tres formatos.
  Referencia verificada a mano en la DUA 039967: ruc 20606451122, 275 bultos,
  peso neto 18,975.00, bruto 19,200.00, unidad comercial 41,832.7,
  FOB 191,070.86, valor clausula 216,170.48, gastos deducibles 25,099.62.

Controles de calidad que produce
--------------------------------
  control_fob    suma del FOB de los items vs el 6.5 de la cabecera
  control_pesos  suma de peso_neto de items vs "OTROS DATOS"
  Ambos se leen, no se ajustan: un descuadre se reporta, no se corrige.

Uso:  python generar_duas.py
"""
import csv
import json
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict

import fitz

from desc_items import clasificar, limpiar_descripcion, resumen

# --------------------------------------------------------------------------- #
# Rutas
# --------------------------------------------------------------------------- #
RAIZ = r"C:\Users\acuba\eudrperu"
PDF_DIR = os.path.join(RAIZ, "fichaduanas")
URL_DIR = os.path.join(RAIZ, "ficharucsunat")
JSON_OUT = os.path.join(RAIZ, "duas_parsed.json")
URL_CSVS = ("dua_canal_final.csv", "dua_canal.csv", "dua_canal_2024_reintento.csv")

# Integracion hacia el directorio de MINAGRI: se copia la hoja 'por RUC' a
# partir de la columna de inicio, emparejando por RUC. Poner None para no
# tocar ese archivo.
MINAGRI_XLSX = (r"C:\Users\acuba\Downloads"
                r"\3 directorio- base de datos de los excels de minagri (1) - ACTUALIZADO v2.xlsx")
MINAGRI_HOJA = "base 25 detallada"
MINAGRI_COL_RUC = 2        # columna B del destino: RUC de la organizacion
MINAGRI_COL_INICIO = 79    # columna CA
MINAGRI_BACKUP_DIR = r"C:\Users\acuba\AppData\Local\Temp\kilo"

ROW_TOL = 2.0     # tolerancia vertical para agrupar palabras en una fila
SEC_TOL = 3.0     # tolerancia para el offset etiqueta -> valor


# --------------------------------------------------------------------------- #
# Texto: el PDF llega con mojibake
# --------------------------------------------------------------------------- #
# "Codigo" acentuado llega como U+00C3 U+00B3, que son los bytes latin-1 de 'o'
# acentuada mal interpretados como UTF-8. Comparar etiquetas por el texto crudo
# no es fiable, asi que se reparan esas parejas y se pliega sin tildes.
_MOJI = re.compile("[\u00c0-\u00ff][\u0080-\u00bf]")

NOISE = ("codigo", "fecha", "nº", "otros datos",
         "diligencia", "leyenda", "retornar", "imprimir")
NOISE_SUB = ("sujeto a",)          # puede aparecer antes o dentro de la fila

# Codigo de campo ("3.1", "7.12"). Exige que lo siga una letra: asi la fila de
# totales "1035.0 1061.0 1.0 1035.0 15.0" NO se confunde con una etiqueta, y las
# subpartidas ("09.01.11.90.00") tampoco.
FIELD_CODE = re.compile(r"(?<![0-9.,])[1-8]\.\d{1,2}(?=\s+[^\d\s])")
# Titulo de seccion: "3 TRANSPORTE", "6 VALOR ADUANA", "8 DECLARANTE"...
SECTION = re.compile(r"^\d+\s+[A-Z\u00c0-\u00de][A-Z\u00c0-\u00de0-9 ./]*$")


def unmojibake(s):
    return _MOJI.sub(
        lambda m: m.group(0).encode("latin-1").decode("utf-8", "replace"), s)


def fold(s):
    """minusculas sin tildes, para comparar etiquetas. La reparacion va ANTES de
    lower(): lower() convierte U+00C3 en U+00E3 y la pareja dejaria de ser valida."""
    s = unicodedata.normalize("NFKD", unmojibake(str(s)).lower())
    return "".join(c for c in s if not unicodedata.combining(c))


def pad_dua(n):
    """el numero de DUA sale de 5 o 6 digitos segun el PDF; se normaliza a 6
    para que Serie y Consulta emparejen por (aduana, anio, dua)"""
    return n.zfill(6) if n else None


def nz(v):
    """normaliza un campo vacio del formulario ('-', 'N') a None. Solo recorta
    por la izquierda: los nombres de empresa terminan en 'S.A.C.'"""
    if v is None:
        return None
    t = re.sub(r"\s+", " ", str(v)).strip()
    t = re.sub(r"^[-.\s]+", "", t)
    t = re.sub(r"[\s-]+$", "", t)
    if not t or not re.search(r"[0-9A-Za-z]", t):
        return None
    return None if t.upper() in ("N", "NO", "X", "ND", "NA", "NONE") else t


def _isnum(s):
    try:
        float(str(s).replace(",", ""))
        return True
    except ValueError:
        return False


# --------------------------------------------------------------------------- #
# Geometria de la pagina
# --------------------------------------------------------------------------- #
def words_of(page):
    return page.get_text("words")


def rows(words, tol=ROW_TOL):
    """agrupa las palabras en filas por su coordenada Y"""
    words = sorted(words, key=lambda w: w[1])
    out, cur = [], []
    for w in words:
        if cur and w[1] - cur[-1][1] > tol:
            out.append(cur)
            cur = []
        cur.append(w)
    if cur:
        out.append(cur)
    return out


def rtext(row):
    return " ".join(w[4] for w in row)


def is_label_row(row):
    t = rtext(row).strip()
    if FIELD_CODE.search(t.lower()) or SECTION.match(t):
        return True
    core = fold(t).strip()
    if any(m in core for m in NOISE_SUB):
        return True
    return any(core == n or core.startswith(n) for n in NOISE)


def band(row, x0, x1):
    """texto de la fila dentro de una banda de coordenadas X"""
    ws = [w for w in row if x0 <= w[0] <= x1]
    return " ".join(w[4] for w in sorted(ws, key=lambda w: w[0])) or None


def bnum(row, x0, x1):
    """primer numero de la fila dentro de una banda X"""
    s = band(row, x0, x1)
    if not s:
        return None
    for p in s.split():
        if _isnum(p):
            return float(p.replace(",", ""))
    return None


def find_row(W, pred):
    for r in rows(W):
        if pred(fold(rtext(r))):
            return r
    return None


def below_rows(W, label_row, max_dy=45.0):
    """filas de valor (no etiqueta) bajo una etiqueta, en orden"""
    y0 = label_row[0][1]
    out = []
    for r in rows(W):
        d = r[0][1] - y0
        if d > max_dy:
            break
        if 0 < d and not is_label_row(r):
            out.append(r)
    return out


def row_at(W, y_target, tol=SEC_TOL):
    """fila no-etiqueta mas cercana a una coordenada Y"""
    best, bestd = None, None
    for r in rows(W):
        if is_label_row(r):
            continue
        d = abs(r[0][1] - y_target)
        if d <= tol and (bestd is None or d < bestd):
            best, bestd = r, d
    return best


def top_text(doc, n=8):
    """texto de las primeras filas. Algunos PDF traen encabezado de impresion
    del navegador ('24/9/26, 8:55 a.m. Consulta DUA') que desplaza la fila real."""
    return " ".join(rtext(r) for r in rows(words_of(doc[0]))[:n])


def page_text(doc):
    return "\n".join(rtext(r) for r in rows(words_of(doc[0])))


def aduana_of(W):
    """codigo de aduana: sigue a 'REGISTRO DE ADUANA', en esa fila o la siguiente"""
    RS = rows(W)
    for i, r in enumerate(RS[:8]):
        if "REGISTRO DE ADUANA" not in rtext(r).upper():
            continue
        for r2 in RS[i:i + 3]:
            m = re.search(r"\b(\d{3})\b", rtext(r2))
            if m:
                return m.group(1)
    return None


def aduana_nombre_of(W):
    """nombre de la aduana: la fila que sigue a 'REGISTRO DE ADUANA', sin el
    codigo de 3 digitos. El PDF a veces lo imprime junto ('PAITA 046') y a
    veces no ('CALLAO')."""
    RS = rows(W)
    for i, r in enumerate(RS[:8]):
        if "REGISTRO DE ADUANA" not in rtext(r).upper():
            continue
        for r2 in RS[i + 1:i + 3]:
            t = " ".join(rtext(r2).split())
            t = re.sub(r"\b\d{3}\b", " ", t).strip(" .")
            if t and not re.match(r"^N", t):
                return t
    return None


def canal_of(W):
    """canal (VERDE/ROJO). El orden de las palabras varia: en Serie el token
    aparece ANTES de la etiqueta ('VERDE Sujeto a:')."""
    for r in rows(W):
        t = rtext(r)
        if "sujeto a" not in fold(t):
            continue
        m = re.search(r"\b(VERDE|ROJO)\b", t)
        if m:
            return m.group(1)
    return None


# Offsets verticales etiqueta -> valor, medidos. En Serie el bloque de etiqueta
# va seguido de una fila de ENCABEZADOS y luego la de valores, asi que el salto
# es mayor que en Consulta.
SER_DY = {"1.2": 17.6, "7.1": 35.6, "7.6": 26.6,
          "7.12": 26.6, "7.19": 26.6, "7.29": 26.6}
SEC_DY = {"3.1": 26.6, "4.1": 17.6, "5.1": 17.0, "5.2": 20.2,
          "6.1": 12.8, "8.1": 17.2, "tot": 17.6}


def sec_row(W, label, key, tol=SEC_TOL, dymap=None):
    """fila de valores de la seccion `label`, al offset medido `key`"""
    r = find_row(W, lambda t: label in t)
    if not r:
        return None
    return row_at(W, r[0][1] + (dymap or SEC_DY)[key], tol)


# --------------------------------------------------------------------------- #
# Serie: un PDF por item
# --------------------------------------------------------------------------- #
def parse_serie(path):
    doc = fitz.open(path)
    W = words_of(doc[0])
    full = page_text(doc)
    out = {"file": os.path.basename(path), "tipo": "SERIE", "paginas": doc.page_count}

    m = re.search(r"DECLARACION\s*:\s*(\d{3})-(\d{4})-40-(\d+)", top_text(doc))
    out["aduana"], out["anio"], _dua = m.groups() if m else (None, None, None)
    out["dua"] = pad_dua(_dua)
    m = re.search(r"\b(\d{2}/\d{2}/\d{4})\b", top_text(doc, 12))
    out["fecha_numeracion"] = m.group(1) if m else None
    out["canal"] = canal_of(W)

    # 1.1 exportador
    r11 = find_row(W, lambda t: "1.1 importador" in t)
    if r11:
        out["exportador"] = nz(" ".join(rtext(r) for r in below_rows(W, r11)))

    # 1.2 RUC + ubigeo + direccion (la direccion puede ocupar varias lineas)
    r12 = find_row(W, lambda t: "1.2 c" in t)
    if r12:
        vs = below_rows(W, r12, 40.0)
        if vs:
            t0 = rtext(vs[0])
            m = re.search(r"\b4\s*-\s*(\d{11})\b", t0)
            out["ruc"] = m.group(1) if m else None
            dig = re.findall(r"\b\d{6}\b", t0)
            out["ubigeo"] = dig[-1] if dig else None
            extra = " ".join(rtext(r) for r in vs[1:])
            out["direccion"] = nz((band(vs[0], 240, 560) or "") + " " + extra)

    # 7.1-7.5 numero de item
    v = sec_row(W, "7.1 n", "7.1", dymap=SER_DY)
    if v:
        n = bnum(v, 110, 200)
        out["item"] = str(int(n)) if n is not None else None

    # 7.6-7.11
    v = sec_row(W, "7.6 puerto de embarque", "7.6", dymap=SER_DY)
    if v:
        out["fecha_embarque"] = nz(band(v, 110, 175))
        out["doc_transporte"] = nz(band(v, 160, 280))
        out["cert_origen"] = nz(band(v, 280, 380))
        out["unidad_comercial"] = bnum(v, 380, 470)

    # 7.12-7.18
    v = sec_row(W, "7.12 cantidad", "7.12", dymap=SER_DY)
    if v:
        out["bultos"] = bnum(v, 0, 80)
        out["clase"] = nz(band(v, 80, 150))
        out["peso_neto"] = bnum(v, 150, 220)
        out["peso_bruto"] = bnum(v, 220, 300)
        out["u_fisica"] = bnum(v, 300, 333)
        out["unidad_fisica_txt"] = nz(band(v, 333, 560))

    # 7.19-7.28
    v = sec_row(W, "7.19 subpartida", "7.19", dymap=SER_DY)
    if v:
        out["subpartida"] = nz(band(v, 0, 130))
        out["sub_tipo"] = nz(band(v, 130, 230))
        out["tm"] = bnum(v, 230, 275)
        out["tpi"] = bnum(v, 275, 315)
        out["tpn"] = bnum(v, 315, 360)
        out["cod_lib"] = bnum(v, 360, 560)

    # 7.29-7.34
    v = sec_row(W, "7.29 fob moneda", "7.29", dymap=SER_DY)
    if v:
        out["cod_moneda"] = nz(band(v, 0, 100))
        out["fob"] = bnum(v, 100, 215)
        out["flete"] = bnum(v, 215, 285)
        out["seguro"] = bnum(v, 285, 450)
        out["valor_aduana"] = bnum(v, 450, 560)

    # 7.35 descripcion: se localiza por numeros de campo (sin depender de
    # acentos ni de mojibake). La region cruda se entrega a desc_items, que
    # repara el mojibake (el PDF es latin-1), quita la cabecera del campo,
    # reconstruye el texto que el formulario reimprime por linea y separa los
    # atributos declarados. Ver desc_items.py para el detalle de cada paso.
    i = full.find("7.35")
    if i != -1:
        j = min([p for p in (full.find(k, i + 4) for k in ("7.36", "7.37"))
                 if p != -1] or [len(full)])
        region = full[i + 4:j]
        limpia = limpiar_descripcion(region)
        out["descripcion"] = limpia
        if limpia:
            out.update(clasificar(limpia))
            out["atributos"] = resumen(out)
    return out


# --------------------------------------------------------------------------- #
# Consulta: un PDF por DUA
# --------------------------------------------------------------------------- #
def parse_consulta(path):
    doc = fitz.open(path)
    W = words_of(doc[0])
    out = {"file": os.path.basename(path), "tipo": "CONSULTA", "paginas": doc.page_count}

    # Cabecera: el PDF mezcla texto con y sin mojibake, asi que se usan anclas
    # ASCII puras sobre las primeras filas.
    RS = rows(W)
    head = " ".join(rtext(r) for r in RS[:12])
    m = re.search(r"\b(\d{4})-(\d{1,6})\b", head)
    out["anio"], out["dua"] = ((m.group(1), pad_dua(m.group(2))) if m
                              else (None, None))
    m = re.search(r"\b(\d{2}/\d{2}/\d{4})\b", head)
    out["fecha_numeracion"] = m.group(1) if m else None
    out["canal"] = canal_of(W)
    for r in RS[:6]:
        m = re.search(r"([A-Z\u00c0-\u00de][A-Z\u00c0-\u00de .\-]*?)\s+(\d{3})\s*$",
                      rtext(r))
        if m:
            out["aduana"] = m.group(2)
            break
    out.setdefault("aduana", aduana_of(W))
    out["aduana_nombre"] = aduana_nombre_of(W)

    r11 = find_row(W, lambda t: "1.1 importador" in t)
    if r11:
        out["exportador"] = nz(" ".join(rtext(r) for r in below_rows(W, r11)))

    r12 = find_row(W, lambda t: "1.2 c" in t)
    if r12:
        v = below_rows(W, r12)
        if v:
            m = re.search(r"\b4\s*-\s*(\d{11})\b", rtext(v[0]))
            out["ruc"] = m.group(1) if m else None

    # 3.1 transportista / 3.2 manifiesto / 3.3 via
    # Bandas X medidas: transportista <338, manifiesto 338-400, via >400.
    # El nombre puede ocupar 2 lineas, asi que si la fila del offset medido solo
    # trae el codigo se busca la fila con letras. Si tampoco hay letras, esa
    # banda es el codigo y no el nombre.
    lr = find_row(W, lambda t: "3.1 empresa transporte" in t)
    if lr:
        ly = lr[0][1]
        win = [r for r in rows(W) if 8.0 < r[0][1] - ly <= 44.0
               and not is_label_row(r)]
        has_txt = lambda r: bool(re.search(r"[A-Za-z]{3}", band(r, 110, 338) or ""))
        has_num = lambda r: bool(re.search(r"\d", band(r, 110, 200) or ""))
        v = row_at(W, ly + SEC_DY["3.1"])
        if v and not has_txt(v):
            v = next((r for r in win if has_txt(r)), v)
        v2 = next((r for r in win if has_num(r) and not has_txt(r)), None)
        if v:
            tname = nz(band(v, 110, 338))
            tcode = nz(band(v2, 110, 200)) if v2 else None
            if tname and not re.search(r"[A-Za-z]{3}", tname):
                tcode = tcode or tname
                tname = None
            out["transportista"] = tname
            out["manifiesto"] = nz(band(v, 338, 400))
            out["via"] = nz(band(v, 400, 560))
        if v2 and v2 is not v:
            out["transportista_codigo"] = nz(band(v2, 110, 200))
            out["via_codigo"] = nz(band(v2, 200, 560))

    # 4.1 deposito temporal / 4.2 deposito AA / 4.3 plazo
    # 4.1 y 4.2 no tienen ancho fijo (depende de si el valor es un codigo corto o
    # un nombre largo), asi que se separan por el hueco mayor y el ultimo token
    # queda siempre del lado de 4.2. El 4.3 si tiene X estable.
    v = sec_row(W, "4.1 dep", "4.1")
    if v:
        left = sorted([w for w in v if w[0] < 300], key=lambda w: w[0])
        gaps = [(left[i + 1][0] - left[i][2], i) for i in range(len(left) - 1)]
        best = max(gaps) if gaps else (0.0, 0)
        cut = best[1] + 1 if best[0] >= 4.0 else max(len(left) - 1, 1)
        out["deposito_temporal"] = nz(" ".join(w[4] for w in left[:cut]))
        out["deposito_aa"] = nz(" ".join(w[4] for w in left[cut:]))
        out["plazo_solicitado"] = nz(band(v, 440, 560))

    # 5.1 entidad financiera / 5.2 modalidad
    v = sec_row(W, "5.2 modalidad", "5.1", tol=1.8)
    if v:
        out["entidad_financiera"] = nz(band(v, 110, 250))
    v = sec_row(W, "5.2 modalidad", "5.2", tol=1.8)
    if v:
        out["modalidad"] = nz(band(v, 250, 560))

    # 6.1 valor clausula / 6.2 comision / 6.3 gastos deducibles / 6.4 ajustes /
    # 6.5 valor neto. El FOB a validar es 6.5, NO 6.1-6.2-6.3: en la DUA 039967
    # 6.4 Total Ajustes viene en 0 aunque 6.3 tiene 25,099.62.
    v = sec_row(W, "6 valor aduana", "6.1")
    if v:
        out["valor_clausula"] = bnum(v, 110, 181)
        out["comision"] = bnum(v, 181, 277)
        out["gastos_deducibles"] = bnum(v, 277, 366)
        out["total_ajustes"] = bnum(v, 366, 446)
        out["valor_neto_fob"] = bnum(v, 446, 560)

    # 8.1 declarante
    v = sec_row(W, "8.1 declarante", "8.1")
    if v:
        m = re.search(r"RUC\s+(\d{11})\s*-\s*(.+)", rtext(v))
        if m:
            out["declarante_ruc"], out["declarante"] = m.group(1), nz(m.group(2))

    # OTROS DATOS: totales de la DUA
    v = sec_row(W, "total peso neto", "tot")
    if v:
        out["total_peso_neto"] = bnum(v, 110, 179)
        out["total_peso_bruto"] = bnum(v, 179, 278)
        out["total_bultos"] = bnum(v, 278, 368)
        out["total_u_fisicas"] = bnum(v, 368, 449)
        out["total_u_comercial"] = bnum(v, 449, 560)
    return out


def parse_any(path):
    """clasifica por CONTENIDO, no por nombre de archivo. Hay PDFs mal
    nombrados: 'Consulta DUA 109415-S2.pdf' es en realidad una Serie."""
    doc = fitz.open(path)
    head = top_text(doc, 6)
    if "DECLARACION :" in head:
        return parse_serie(path)
    if "DUA PROV. DE EXPORTACION" in head:
        return parse_consulta(path)
    return {"file": os.path.basename(path), "tipo": "DESCONOCIDO",
            "paginas": doc.page_count, "head": head[:160]}


# --------------------------------------------------------------------------- #
# Links de consulta en aduanet.gob.pe
# --------------------------------------------------------------------------- #
_URLPAT = re.compile(r"codaduana=(\d+)&anoprese=(\d+)&numecorre=(\d+)")


def load_urls():
    """(aduana, anoprese, dua) -> url. Para este corpus anoprese == anio,
    verificado 201/201 sin excepciones."""
    urls = {}
    for name in URL_CSVS:
        path = os.path.join(URL_DIR, name)
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8-sig") as fh:
            for row in csv.DictReader(fh):
                m = _URLPAT.search(row.get("url_detalle") or "")
                if m:
                    urls.setdefault(m.groups(), row["url_detalle"])
    return urls


URLS = load_urls()


def link(k):
    return URLS.get(tuple(k)) if all(k) else None


# --------------------------------------------------------------------------- #
# Lectura del corpus
# --------------------------------------------------------------------------- #
def leer_corpus():
    serie, consulta, errores, desconocidos = [], [], [], []
    for name in sorted(os.listdir(PDF_DIR)):
        if not name.lower().endswith(".pdf"):
            continue
        try:
            r = parse_any(os.path.join(PDF_DIR, name))
        except Exception as e:                      # noqa: BLE001
            errores.append((name, "%s: %s" % (type(e).__name__, e)))
            continue
        if r.get("tipo") == "SERIE":
            serie.append(r)
        elif r.get("tipo") == "CONSULTA":
            consulta.append(r)
        else:
            desconocidos.append(name)
    return serie, consulta, errores, desconocidos


def deduplicar(serie):
    """Un mismo (aduana, anio, dua, item) puede estar en 2 archivos, porque hay
    descargas duplicadas y nombres mal puestos. Se conserva el archivo 'Serie'."""
    best, dups = {}, []
    for s in serie:
        k = (s.get("aduana"), s.get("anio"), s.get("dua"), s.get("item"))
        prev = best.get(k)
        if prev is None:
            best[k] = s
            continue
        dups.append((k, prev["file"], s["file"]))
        if not prev["file"].startswith("Serie") and s["file"].startswith("Serie"):
            best[k] = s
    return list(best.values()), dups


# --------------------------------------------------------------------------- #
# Armado de las hojas
# --------------------------------------------------------------------------- #
H_ITEMS = [
    "ruc", "razon_social", "direccion", "ubigeo", "anio", "dua", "item",
    "descripcion", "atributos",
    "organico", "fairtrade", "rainforest", "utz_jbs", "sustentable_cert",
    "arabica", "robusta", "criollo", "trinitario", "forastero", "amazonico",
    "washed", "honey", "natural", "sun_dried",
    "en_grano", "en_bolsa", "a_granel", "consumo_humano",
    "serie_ico", "numero_marca", "clave_origen", "pais_codigo",
    "codigo_sin_etiqueta", "fda", "lote", "marca_txt", "contrato",
    "peso_declarado_kg", "peso_texto_incompleto",
    "subpartida", "sub_tipo", "clase", "bultos",
    "peso_neto", "peso_bruto", "u_fisica", "unidad_fisica_txt",
    "unidad_comercial", "fob", "flete", "seguro", "valor_aduana",
    "aduana", "fecha_numeracion", "canal", "fecha_embarque", "doc_transporte",
    "cert_origen", "exportador", "transportista", "manifiesto", "via",
    "deposito_temporal", "deposito_aa", "plazo_solicitado",
    "entidad_financiera", "modalidad", "valor_clausula", "gastos_deducibles",
    "valor_neto_fob", "total_peso_neto", "total_peso_bruto", "total_bultos",
    "declarante_ruc", "declarante", "archivo", "tiene_consulta",
    "control_fob", "control_pesos", "link_aduanet",
]

# Atributos que se escriben como SI/NO leidos de la descripcion del item.
# Ver desc_items.py: si la palabra no esta en el documento el valor es None
# (no declarado), nunca False. Un False implicito seria afirmar que el
# producto NO es organico, que es una afirmacion que la DUA no hace.
H_SINO = [
    "organico", "fairtrade", "rainforest", "utz_jbs", "sustentable_cert",
    "arabica", "robusta", "criollo", "trinitario", "forastero", "amazonico",
    "washed", "honey", "natural", "sun_dried",
    "en_grano", "en_bolsa", "a_granel", "consumo_humano", "contrato",
    "peso_texto_incompleto",
]

# Todas las columnas que provienen de la descripcion del item. El bloque se
# lee una sola vez al escribir DETALLE_ITEMS, en el orden de H_ITEMS, para que
# agregar un atributo no pueda desplazar los campos vecinos.
H_ATRIBUTOS = [
    "atributos",
    "organico", "fairtrade", "rainforest", "utz_jbs", "sustentable_cert",
    "arabica", "robusta", "criollo", "trinitario", "forastero", "amazonico",
    "washed", "honey", "natural", "sun_dried",
    "en_grano", "en_bolsa", "a_granel", "consumo_humano",
    "serie_ico", "numero_marca", "clave_origen", "pais_codigo",
    "codigo_sin_etiqueta", "fda", "lote", "marca_txt", "contrato",
    "peso_declarado_kg", "peso_texto_incompleto",
]

# Hoja SERIES_ICO: una fila por SERIE ICO declarada.
#
# Correccion terminologica importante. El ICO NO es el codigo individual del
# productor. Segun la Camara Peruana del Cafe y Cacao, que es el organismo
# certificante acreditado ante la Organizacion Internacional del Cafe, la
# "serie ICO" es el numero de serie del CERTIFICADO DE ORIGEN que esa Camara
# emite, y se solicita POR CADA OPERACION O LOTE. Identifica una operacion
# comercial, no a un productor ni a una parcela. La version anterior de este
# modulo la describia como codigo de productor y la hoja se llamaba
# PRODUCTORES_ICO, lo que era incorrecto.
#
# Lo que si identifica origen es el numero de MARCA: lleva la clave de pais,
# un bloque central estable dentro de un mismo exportador, y el numero de
# serie de la partida. Esa clave se agrega en la hoja CLAVES_ORIGEN.
H_PROD = [
    "serie_ico", "ruc_exportador", "razon_social", "clave_origen", "n_items",
    "n_duas", "fob_total", "peso_neto_total", "peso_bruto_total", "bultos_total",
    "anios", "duas", "organico", "fairtrade", "arabica", "washed",
    "subpartidas", "atributos", "descripcion_ejemplo", "cobertura_serie_ico",
]

# Hoja CLAVES_ORIGEN: una fila por bloque central de marca, que se mantiene
# estable dentro de un mismo exportador. Es el identificador de procedencia mas
# cercano a la parcela que existe hoy en las DUAs, y esta escrito en el campo
# de marca comercial en lugar de un campo de trazabilidad.
H_CLAVE = [
    "clave_origen", "pais_codigo", "ruc_exportador", "razon_social",
    "n_items", "n_duas", "fob_total", "peso_neto_total", "bultos_total",
    "anios", "n_series_ico", "n_marcas", "organico", "fairtrade",
    "descripcion_ejemplo",
]

# Atributos agregados que se anexan a 'por RUC'. van al final del bloque para
# no desplazar las columnas que MINAGRI ya tiene escritas desde CA.
RUC_ATRIB_SINO = [
    "organico", "fairtrade", "rainforest", "utz_jbs", "sustentable_cert",
    "arabica", "washed", "en_bolsa", "a_granel", "consumo_humano",
]
H_RUC_ATRIB = (
    ["items_con_descripcion"] + ["n_items_%s" % c for c in RUC_ATRIB_SINO]
    + ["n_series_ico", "series_ico", "n_claves_origen", "claves_origen",
       "n_lotes", "n_marcas"]
)

H_DUAS = [
    "ruc", "razon_social", "anio", "dua", "aduana", "fecha_numeracion", "canal",
    "exportador", "transportista", "manifiesto", "via", "deposito_aa",
    "plazo_solicitado", "modalidad", "entidad_financiera", "valor_clausula",
    "gastos_deducibles", "valor_neto_fob", "total_peso_neto",
    "total_peso_bruto", "total_bultos", "total_u_fisicas", "total_u_comercial",
    "declarante_ruc", "declarante", "n_items", "fob_suma_items", "fuente",
    "link_aduanet",
]

H_SIN_CAB = [
    "aduana", "anio", "dua", "ruc", "razon_social", "n_items", "fob_suma_items",
    "peso_neto_suma", "archivos_serie", "estado", "link_reconsulta",
]


def construir_items(serie, consulta):
    """una fila por item, completada con la cabecera de su DUA"""
    hdr = {}
    for c in consulta:
        hdr.setdefault((c.get("aduana"), c.get("anio"), c.get("dua")), c)

    fob = defaultdict(float)
    peso = defaultdict(float)
    for s in serie:
        k = (s.get("aduana"), s.get("anio"), s.get("dua"))
        fob[k] += s.get("fob") or 0
        peso[k] += s.get("peso_neto") or 0

    def ctrl_fob(k, c):
        if c is None:
            return "SIN_CABECERA"
        ref = c.get("valor_neto_fob")
        if ref is None:
            return "SIN_REFERENCIA"
        d = round(fob[k] - ref, 2)
        if abs(d) <= 0.05:
            return "OK"
        # por debajo significa que al folder le faltan items de esa DUA
        return ("FALTAN_ITEMS %.2f" % -d) if d < 0 else ("EXCEDE %.2f" % d)

    def ctrl_pesos(k, c):
        if c is None or c.get("total_peso_neto") is None:
            return ""
        d = round(peso[k] - c["total_peso_neto"], 2)
        return "OK" if abs(d) <= 0.05 else "DIFIERE %.2f" % d

    filas, sin_cabecera = [], []
    for s in serie:
        k = (s.get("aduana"), s.get("anio"), s.get("dua"))
        c = hdr.get(k)
        if c is None:
            sin_cabecera.append(k + (s.get("file"),))
        g = lambda campo: (c or {}).get(campo)          # noqa: E731
        # la razon social puede venir de la cabecera o del propio item (cada PDF
        # la trunca segun el alto disponible); se conserva la version mas larga
        razon = max([x for x in (g("exportador"), s.get("exportador")) if x],
                    key=len, default=None)
        # la fila se arma como diccionario y se serializa siguiendo H_ITEMS.
        # Armarla como lista posicional obligaba a contar 70+ campos a mano:
        # agregar una columna despues desalineaba todas las siguientes sin
        # que nada lo denunciara. El orden de H_ITEMS es la unica fuente.
        fila = {
            "ruc": s.get("ruc"),
            "razon_social": razon,
            "direccion": g("direccion") or s.get("direccion"),
            "ubigeo": s.get("ubigeo"),
            "anio": s.get("anio"),
            "dua": s.get("dua"),
            "item": s.get("item"),
            "descripcion": s.get("descripcion"),
            "atributos": s.get("atributos"),
            "subpartida": s.get("subpartida"),
            "sub_tipo": s.get("sub_tipo"),
            "clase": s.get("clase"),
            "bultos": s.get("bultos"),
            "peso_neto": s.get("peso_neto"),
            "peso_bruto": s.get("peso_bruto"),
            "u_fisica": s.get("u_fisica"),
            "unidad_fisica_txt": s.get("unidad_fisica_txt"),
            "unidad_comercial": s.get("unidad_comercial"),
            "fob": s.get("fob"),
            "flete": s.get("flete"),
            "seguro": s.get("seguro"),
            "valor_aduana": s.get("valor_aduana"),
            "aduana": s.get("aduana"),
            "fecha_numeracion": s.get("fecha_numeracion")
            or g("fecha_numeracion"),
            "canal": s.get("canal") or g("canal"),
            "fecha_embarque": s.get("fecha_embarque"),
            "doc_transporte": s.get("doc_transporte"),
            "cert_origen": s.get("cert_origen"),
            "exportador": g("exportador") or s.get("exportador"),
            "transportista": g("transportista"),
            "manifiesto": g("manifiesto"),
            "via": g("via"),
            "deposito_temporal": g("deposito_temporal"),
            "deposito_aa": g("deposito_aa"),
            "plazo_solicitado": g("plazo_solicitado"),
            "entidad_financiera": g("entidad_financiera"),
            "modalidad": g("modalidad"),
            "valor_clausula": g("valor_clausula"),
            "gastos_deducibles": g("gastos_deducibles"),
            "valor_neto_fob": g("valor_neto_fob"),
            "total_peso_neto": g("total_peso_neto"),
            "total_peso_bruto": g("total_peso_bruto"),
            "total_bultos": g("total_bultos"),
            "declarante_ruc": g("declarante_ruc"),
            "declarante": g("declarante"),
            "archivo": s.get("file"),
            "tiene_consulta": "SI" if c else "NO",
            "control_fob": ctrl_fob(k, c),
            "control_pesos": ctrl_pesos(k, c),
            "link_aduanet": link(k),
        }
        # atributos declarados en la descripcion del item
        for col in H_ATRIBUTOS:
            v = s.get(col)
            if col in H_SINO:
                # SI / NO / "" (no declarado). Nunca False: la DUA no afirma
                # la ausencia del atributo, solo lo declara cuando aparece.
                fila[col] = "" if v is None else ("SI" if v else "NO")
            else:
                fila[col] = v
        filas.append([fila.get(col) for col in H_ITEMS])
    return filas, sin_cabecera


def hoja_productores(serie):
    """Una fila por SERIE ICO declarada en las descripciones de los items.

    Correccion de lectura: la serie ICO no es un codigo de productor. Es el
    numero de serie del certificado de origen que emite la Camara Peruana del
    Cafe y Cacao ante la Organizacion Internacional del Cafe, y se tramita por
    operacion o lote. Agrupar por ella responde "cuantas operaciones de
    origen se certificataron y con que volumen", no "cuantos productores hay".

    Solo se incluyen los items que traen la serie. La columna
    'cobertura_serie_ico' deja claro cuantos items quedan fuera, para que la
    hoja no se lea como si cubriera todo el corpus.
    """
    por_ico = defaultdict(list)
    sin_ico = 0
    for s in serie:
        ico = s.get("serie_ico")
        if ico:
            por_ico[ico].append(s)
        else:
            sin_ico += 1

    def todos(ics, campo):
        """SI si el atributo esta declarado en AL MENOS un item de la serie;
        '' si ninguno de los items lo declara. No se emite NO: la ausencia
        de la palabra no es una certificacion negativa."""
        v = [x.get(campo) for x in ics]
        return "SI" if any(v) else ""

    def union(ics, campo):
        return "; ".join(sorted({str(x.get(campo)) for x in ics
                                if x.get(campo) is not None}))

    n_con_serie = sum(len(g) for g in por_ico.values())
    cobertura = "items con serie ICO %d / %d del corpus (%d sin serie)" % (
        n_con_serie, len(serie), sin_ico)

    filas = []
    for ico in sorted(por_ico):
        ics = por_ico[ico]
        duas = sorted({str(x.get("dua")) for x in ics})
        rucs = sorted({str(x.get("ruc")) for x in ics if x.get("ruc")})
        razones = [x.get("exportador") for x in ics if x.get("exportador")]
        claves = sorted({str(x.get("clave_origen")) for x in ics
                         if x.get("clave_origen") is not None})
        filas.append([
            ico,
            "; ".join(rucs),
            max(razones, key=len, default=None),
            "; ".join(claves),
            len(ics),
            len(duas),
            round(sum(x.get("fob") or 0 for x in ics), 2),
            round(sum(x.get("peso_neto") or 0 for x in ics), 2),
            round(sum(x.get("peso_bruto") or 0 for x in ics), 2),
            sum(x.get("bultos") or 0 for x in ics),
            union(ics, "anio"),
            "; ".join(duas),
            todos(ics, "organico"),
            todos(ics, "fairtrade"),
            todos(ics, "arabica"),
            todos(ics, "washed"),
            union(ics, "subpartida"),
            union(ics, "atributos"),
            (ics[0].get("descripcion") or None),
            cobertura,
        ])
    return filas


def hoja_claves_origen(serie):
    """Una fila por bloque central de marca, que es estable por exportador.

    El numero de marca del saco tiene la forma NN-AAA-NNN: el primer bloque
    es el pais, el central se mantiene constante dentro de un mismo
    exportador y el ultimo es el numero de serie de la partida. Ese bloque
    central es lo mas cerca de un identificador de procedencia que existe hoy
    escrito en una DUA, y EUDR pide precisamente identificar el origen
    geografico de la parcela.

    No es un identificador de productor individual ni de parcela: identifica a
    la organizacion que exporta, que puede agregar coffee de socios de varios
    departamentos.
    """
    por_clave = defaultdict(list)
    for s in serie:
        c = s.get("clave_origen")
        if c is not None:
            por_clave[str(c)].append(s)

    def todos(ics, campo):
        v = [x.get(campo) for x in ics]
        return "SI" if any(v) else ""

    filas = []
    for clave in sorted(por_clave, key=lambda x: (len(x), x)):
        ics = por_clave[clave]
        rucs = sorted({str(x.get("ruc")) for x in ics if x.get("ruc")})
        razones = [x.get("exportador") for x in ics if x.get("exportador")]
        paises = sorted({str(x.get("pais_codigo")) for x in ics
                         if x.get("pais_codigo") is not None})
        series = {str(x.get("serie_ico")) for x in ics if x.get("serie_ico")}
        marcas = {str(x.get("numero_marca")) for x in ics if x.get("numero_marca")}
        filas.append([
            clave,
            "; ".join(paises),
            "; ".join(rucs),
            max(razones, key=len, default=None),
            len(ics),
            len({str(x.get("dua")) for x in ics}),
            round(sum(x.get("fob") or 0 for x in ics), 2),
            round(sum(x.get("peso_neto") or 0 for x in ics), 2),
            sum(x.get("bultos") or 0 for x in ics),
            "; ".join(sorted({str(x.get("anio")) for x in ics})),
            len(series),
            len(marcas),
            todos(ics, "organico"),
            todos(ics, "fairtrade"),
            (ics[0].get("descripcion") or None),
        ])
    return filas


# Identificadores que representan un rastro de origen declarado en el item.
# El conteo da la "riqueza de trazabilidad" de cada partida: 0 significa que
# la DUA no dice de donde viene el producto.
IDS_ORIGEN = ["serie_ico", "numero_marca", "clave_origen", "lote",
              "codigo_sin_etiqueta"]

H_COBERTURA = [
    "n_identificadores", "items", "pct_items", "fob_total", "pct_fob",
    "peso_neto_total", "con_clave_origen", "con_serie_ico", "con_numero_marca",
    "con_lote", "organico", "fairtrade",
]


def hoja_cobertura_identificadores(serie):
    """Una fila por cantidad de identificadores de origen declarados.

    El 0 es la fila que importa: son las partidas donde la DUA no dice nada
    sobre el origen. En el corpus son 224 de 312 items y US$ 28.4 millones,
    69,5% del FOB. La hoja existe para que esa cifra no se pierda de vista al
    mirar las demas, que muestran los casos que si traen dato.
    """
    filas = []
    total_fob = sum(s.get("fob") or 0 for s in serie)
    total_peso = sum(s.get("peso_neto") or 0 for s in serie)

    def cuenta(ics, campo):
        return sum(1 for x in ics if x.get(campo) is not None)

    def declara(ics, campo):
        return sum(1 for x in ics
                   if str(x.get(campo)).upper() == "SI")

    for n in range(len(IDS_ORIGEN) + 1):
        ics = [s for s in serie
               if sum(1 for c in IDS_ORIGEN if s.get(c) is not None) == n]
        if not ics:
            continue
        fob = sum(x.get("fob") or 0 for x in ics)
        filas.append([
            n, len(ics), round(len(ics) / len(serie) * 100, 1),
            round(fob, 2),
            round(fob / total_fob * 100, 1) if total_fob else None,
            round(sum(x.get("peso_neto") or 0 for x in ics), 2),
            cuenta(ics, "clave_origen"),
            cuenta(ics, "serie_ico"),
            cuenta(ics, "numero_marca"),
            cuenta(ics, "lote"),
            declara(ics, "organico"),
            declara(ics, "fairtrade"),
        ])
    return filas


H_FINCAS = [
    "dua", "anio", "ruc", "razon_social", "item", "finca", "variedad",
    "contrato", "contrato_truncado", "fob", "peso_neto", "bultos",
    "organico", "descripcion",
]

# La descripcion de la mercancia es el unico campo del formulario aduanero
# donde puede aparecer el nombre de una finca. La cooperativa escribe siempre
# el mismo bloque: "G1 <FINCA> [-<variedad>] CTR <numero>". Algunas veces
# omite la palabra FINCA ("G1 SANTA SOFIA - HONEY"), por eso es opcional.
RE_FINCA = re.compile(
    r"\bG1\s+(?:FINCA\s+)?"
    r"([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ]*(?:\s+[A-ZÁÉÍÓÚÑ]+)*?)"      # nombre
    r"(?:\s*-\s*([A-ZÁÉÍÓÚÑ]+))?"                            # variedad
    r"(?:\s+CTR\b|\s*$)", re.I)
RE_VARIEDAD = re.compile(
    r"\b(GEISHA|BOURBON|CASTILLO|CATUAZ|CATIMOR|GEOISHA|PACAMARA)\b", re.I)
RE_CONTRATO = re.compile(r"CTR\s*(\d{2}-\d{5})", re.I)
RE_CTR = re.compile(r"\bCTR\b", re.I)
# El PDF corta la descripcion a 100 caracteres y el contrato cae partido:
# "... CTR 13" al final y "49400, 60 BOLSAS ..." al principio.
RE_CONTRATO_PARTIDO = re.compile(r"CTR\s*(\d{2})\s*$")
RE_CONTRATO_TOPE = re.compile(r"^\s*(\d{4,6})\s*,")


def hoja_fincas(serie):
    """Una fila por item que nombra una finca dentro de la descripcion.

    Unica casilla del corpus donde el rastro baja del exportador a la finca:
    nueve items de una sola declaracion, escritos por la cooperativa en el
    campo de descripcion, no por un sistema. Se registra porque prueba que el
    dato es alcanzable sin instrumentar nada nuevo.
    """
    filas = []
    for s in serie:
        desc = s.get("descripcion") or ""
        m = RE_FINCA.search(desc)
        if not m:
            continue
        # "G1" tambien es un grado de exportacion ("G1 EN GRANO", "G1
        # ORGANICO"). Solo es una finca si la descripcion lo dice con la
        # palabra FINCA o si trae el bloque "CTR <contrato>".
        if not RE_CTR.search(desc):
            continue
        nombre = " ".join(m.group(1).split()).title()
        var = m.group(2)
        if not var:
            v = RE_VARIEDAD.search(m.group(1))
            var = v.group(1).upper() if v else None
        if var:
            # "LA REQUIA BOURBON" y "LA REQUIA - GEISHA" traen la variedad
            # pegada al nombre; no es parte de la finca.
            nombre = " ".join(
                w for w in m.group(1).split() if w.upper() != var
            ).title()

        contrato = truncado = None
        c = RE_CONTRATO.search(desc)
        if c:
            contrato = c.group(1)
        else:
            # el numero quedo partido por el corte del PDF: "... CTR 13" al
            # final de la linea y "49400, 60 BOLSAS ..." al principio.
            p = RE_CONTRATO_PARTIDO.search(desc)
            t = RE_CONTRATO_TOPE.match(desc)
            if p and t:
                contrato = "%s-%s" % (p.group(1), t.group(1))
                truncado = "SI"
            elif p or desc.upper().rstrip().endswith("CTR"):
                truncado = "SI"

        org = s.get("organico")
        filas.append([
            s.get("dua"), s.get("anio"), s.get("ruc"),
            s.get("exportador"), s.get("item"),
            nombre, var,
            contrato or "(truncado)", truncado or "",
            round(s.get("fob") or 0, 2),
            s.get("peso_neto"), s.get("bultos"),
            "SI" if org is True else ("" if org is None else org),
            desc,
        ])
    return sorted(filas, key=lambda r: (str(r[2]), str(r[0]), r[4] or 0))


def construir_duas(serie, consulta):
    """una fila por DUA. Prioriza la cabecera; si no hay, se arma con el item."""
    items_por_dua = defaultdict(list)
    for s in serie:
        items_por_dua[(s.get("aduana"), s.get("anio"), s.get("dua"))].append(s)

    duas, vistas = [], set()
    for c in consulta:
        k = (c.get("aduana"), c.get("anio"), c.get("dua"))
        if k in vistas:
            continue
        vistas.add(k)
        its = items_por_dua.get(k, [])
        duas.append([
            c.get("ruc"), c.get("exportador"), c.get("anio"), c.get("dua"),
            c.get("aduana"), c.get("fecha_numeracion"), c.get("canal"),
            c.get("exportador"), c.get("transportista"), c.get("manifiesto"),
            c.get("via"), c.get("deposito_aa"), c.get("plazo_solicitado"),
            c.get("modalidad"), c.get("entidad_financiera"),
            c.get("valor_clausula"), c.get("gastos_deducibles"),
            c.get("valor_neto_fob"), c.get("total_peso_neto"),
            c.get("total_peso_bruto"), c.get("total_bultos"),
            c.get("total_u_fisicas"), c.get("total_u_comercial"),
            c.get("declarante_ruc"), c.get("declarante"), len(its),
            round(sum(i.get("fob") or 0 for i in its), 2), "CONSULTA", link(k),
        ])
    for s in serie:
        k = (s.get("aduana"), s.get("anio"), s.get("dua"))
        if k in vistas:
            continue
        vistas.add(k)
        duas.append([
            s.get("ruc"), s.get("exportador"), s.get("anio"), s.get("dua"),
            s.get("aduana"), s.get("fecha_numeracion"), s.get("canal"),
            s.get("exportador"), None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None, None, None, 1,
            s.get("fob"), "SERIE (sin cabecera)", link(k),
        ])
    return duas


# --------------------------------------------------------------------------- #
# Escritura
# --------------------------------------------------------------------------- #
def escribir_excel(serie, consulta, filas, duas, sin_cabecera, dups,
                   errores, desconocidos):
    from openpyxl import load_workbook
    from openpyxl.styles import Font
    from openpyxl.utils import get_column_letter

    BOLD = Font(bold=True)
    LINK = Font(color="0563C1", underline="single")
    # se agregan al libro unico del proyecto, no a uno aparte
    wb = load_workbook(CONSOLIDADO)
    for t in ("DETALLE_ITEMS", "DUAS", "SIN_CABECERA", "CONTROL",
              "SERIES_ICO", "CLAVES_ORIGEN", "COBERTURA_IDENTIFICADORES",
              "FINCAS", "PRODUCTORES_ICO"):
        if t in wb.sheetnames:
            del wb[t]

    def tabla(title, hdrs, data, anchos=None):
        ws = wb.create_sheet(title)
        ws.append(hdrs)
        for c in ws[1]:
            c.font = BOLD
        for row in data:
            ws.append(row)
        ws.freeze_panes = "A2"
        for i, name in enumerate(hdrs, 1):
            if (anchos or {}).get(name):
                ancho = anchos[name]
            elif data:
                ancho = max(len(str(name)) + 2,
                            max(min(40, len(str(r[i - 1])) + 2) for r in data))
            else:
                ancho = 18
            ws.column_dimensions[get_column_letter(i)].width = ancho
        return ws

    tabla("DETALLE_ITEMS", H_ITEMS, filas)
    tabla("DUAS", H_DUAS, duas)
    tabla("SERIES_ICO", H_PROD, hoja_productores(serie))
    tabla("CLAVES_ORIGEN", H_CLAVE, hoja_claves_origen(serie))
    tabla("COBERTURA_IDENTIFICADORES", H_COBERTURA,
          hoja_cobertura_identificadores(serie))
    tabla("FINCAS", H_FINCAS, hoja_fincas(serie))

    # SIN_CABECERA: DUAs sin el PDF de Consulta. NO estan incompletas: el PDF
    # Serie ya esta y trae todos los items. Falta solo la vista de cabecera,
    # que es redundante, asi que no hay nada que descargar.
    items_por_dua = defaultdict(list)
    for s in serie:
        items_por_dua[(s.get("aduana"), s.get("anio"), s.get("dua"))].append(s)
    por_dua = defaultdict(list)
    for a, an, du, ar in sin_cabecera:
        por_dua[(a, an, du)].append(ar)
    filas_sc = []
    for k in sorted(por_dua, key=lambda x: (x[0], x[1], x[2])):
        its = items_por_dua.get(k, [])
        rs = [x for x in [its[0].get("exportador") if its else None] if x]
        filas_sc.append([
            k[0], k[1], k[2], its[0].get("ruc") if its else None,
            max(rs, key=len) if rs else None, len(its),
            round(sum(i.get("fob") or 0 for i in its), 2),
            round(sum(i.get("peso_neto") or 0 for i in its), 2),
            "; ".join(sorted(por_dua[k])),
            "DUA COMPLETA (items en PDF Serie). Falta solo la vista de "
            "cabecera, que es redundante. No hay nada que descargar.",
            link(k) or "SIN LINK en las fuentes",
        ])
    tabla("SIN_CABECERA", H_SIN_CAB, filas_sc,
          {"razon_social": 46, "archivos_serie": 52, "estado": 66,
           "link_reconsulta": 70})

    # hyperlinks reales
    for title, hdrs, col in (("DETALLE_ITEMS", H_ITEMS, "link_aduanet"),
                             ("DUAS", H_DUAS, "link_aduanet"),
                             ("SIN_CABECERA", H_SIN_CAB, "link_reconsulta")):
        ws = wb[title]
        ci = hdrs.index(col) + 1
        for row in ws.iter_rows(min_row=2, min_col=ci, max_col=ci):
            for c in row:
                if isinstance(c.value, str) and c.value.startswith("http"):
                    c.hyperlink, c.font = c.value, LINK

    # ---- CONTROL
    idx = lambda h: H_ITEMS.index(h)                  # noqa: E731
    faltan, exceden = [], []
    for f in filas:
        cf = str(f[idx("control_fob")])
        k = (f[idx("aduana")], f[idx("anio")], f[idx("dua")])
        if cf.startswith("FALTAN_ITEMS") and k not in faltan:
            faltan.append(k)
        elif cf.startswith("EXCEDE") and k not in exceden:
            exceden.append(k)

    ws = wb.create_sheet("CONTROL")
    ws.append(["metrica", "valor"])
    for c in ws[1]:
        c.font = BOLD
    for k, v in [
        ("pdfs leidos", len(serie) + len(dups) + len(consulta)
         + len(errores) + len(desconocidos)),
        ("items (Series) leidos", len(serie) + len(dups)),
        ("items duplicados descartados", len(dups)),
        ("items unicos en DETALLE_ITEMS", len(serie)),
        ("cabeceras (Consulta)", len(consulta)),
        ("filas DETALLE_ITEMS", len(filas)),
        ("filas DUAS", len(duas)),
        ("RUC distintos", len({s.get("ruc") for s in serie})),
        ("errores de parseo", len(errores)),
        ("pdfs no reconocidos", len(desconocidos)),
        ("items con serie ICO", sum(1 for s in serie if s.get("serie_ico"))),
        ("series ICO distintas",
         len({s["serie_ico"] for s in serie if s.get("serie_ico")})),
        ("items con numero de marca",
         sum(1 for s in serie if s.get("numero_marca"))),
        ("items con clave de origen",
         sum(1 for s in serie if s.get("clave_origen") is not None)),
        ("claves de origen distintas",
         len({str(s["clave_origen"]) for s in serie
              if s.get("clave_origen") is not None})),
        ("items con codigo sin etiqueta",
         sum(1 for s in serie if s.get("codigo_sin_etiqueta"))),
        ("items sin ningun identificador de origen",
         sum(1 for s in serie
             if not any(s.get(c) is not None for c in IDS_ORIGEN))),
        ("items que nombran una finca",
         sum(1 for s in serie
             if RE_FINCA.search(s.get("descripcion") or ""))),
    ]:
        ws.append([k, v])

    def seccion(titulo):
        ws.append([])
        ws.append([titulo])
        for c in ws[ws.max_row]:
            c.font = BOLD

    seccion("FALTAN ITEMS: la cabecera declara mas FOB del que hay en el folder")
    ws.append(["estos si son DUAs a las que habria que descargar PDF"])
    for a, an, du in faltan:
        its = [s for s in serie
               if (s.get("aduana"), s.get("anio"), s.get("dua")) == (a, an, du)]
        ref = next(x.get("valor_neto_fob") for x in consulta
                   if (x.get("aduana"), x.get("anio"), x.get("dua")) == (a, an, du))
        ws.append(["DUA %s" % du, "aduana %s %s" % (a, an),
                   "items en folder: %d" % len(its),
                   "FALTAN %.2f de FOB" % -round(
                       sum(s.get("fob") or 0 for s in its) - ref, 2),
                   link((a, an, du)) or "SIN LINK"])
    ws.append(["", "", "total: %d DUAs" % len(faltan)])

    seccion("EXCEDE: la suma de FOB de los items supera el 6.5 de la cabecera")
    ws.append(["no falta nada, hay de mas: revisar si esos items son legitimos",
               "total: %d DUAs" % len(exceden)])
    for a, an, du in exceden:
        ws.append(["DUA %s" % du, "aduana %s %s" % (a, an), link((a, an, du)) or ""])

    seccion("SIN CABECERA: NO son DUAs incompletas")
    ws.append(["tienen su PDF Serie con todos los items; falta solo la vista de "
               "cabecera, que es redundante. Ver hoja SIN_CABECERA.",
               "total: %d DUAs" % len(por_dua)])

    seccion("ITEMS DUPLICADOS (mismo dua+item en 2 archivos)")
    for k, a, b in dups:
        ws.append(["dua %s item %s" % (k[2], k[3]), a, b])

    seccion("CODIGOS DE MARCA CON PAIS INCONSISTENTE")
    ws.append(["la clave de pais deberia ser la misma para todas las marcas de un "
               "mismo exportador; un valor distinto rompe la agrupacion"])
    pais_por_ruc = defaultdict(set)
    marca_por_ruc = defaultdict(list)
    for s in serie:
        if s.get("clave_origen") is not None and s.get("pais_codigo"):
            pais_por_ruc[str(s.get("ruc"))].add(str(s["pais_codigo"]))
            marca_por_ruc[str(s.get("ruc"))].append(
                (str(s["pais_codigo"]), s.get("numero_marca"),
                 s.get("descripcion")))
    for ru, paises in sorted(pais_por_ruc.items()):
        if len(paises) > 1:
            razon = next((s.get("exportador") for s in serie
                          if str(s.get("ruc")) == ru), "")
            ws.append(["ruc %s (%s)" % (ru, razon),
                        "paises declarados: %s" % ", ".join(sorted(paises))])
            for pais, marca, desc in marca_por_ruc[ru]:
                if pais not in (min(paises),):
                    ws.append(["", "marca %s (pais %s)" % (marca, pais),
                               (desc or "")[:70]])

    seccion("ERRORES DE PARSEO")
    for f, e in errores:
        ws.append([f, e])

    seccion("PDFS NO RECONOCIDOS")
    for f in desconocidos:
        ws.append([f])
    for col, w in (("A", 34), ("B", 46), ("C", 26), ("D", 26), ("E", 74)):
        ws.column_dimensions[col].width = w
    wb.save(CONSOLIDADO)
    return faltan, exceden, por_dua


# --------------------------------------------------------------------------- #
# Enlace de los PDF descargados dentro de 'base 25 detallada'
# --------------------------------------------------------------------------- #
CONSOLIDADO = os.path.join(PDF_DIR, "DUA_CONSOLIDADO.xlsx")
HOJA_BASE25 = "base 25 detallada"
HOJA_RUC = "por RUC"
HOJA_PEND = "DESCARGAR_PENDIENTES"
HOJA_DISC = "REVISAR_DISCREPANCIA"
HOJA_EXCL = "ITEMS_EXCLUIDOS"
HOJA_CONS = "DUA_Consolidado_Total"
MAX_ITEMS = 10          # la DUA con mas items de este corpus tiene 10


def enlazar_base25(serie, consulta):
    """Agrega a 'base 25 detallada' una columna por item con el enlace al PDF
    local, mas la de la cabecera. Solo AGREGA columnas: no toca las existentes.

    El match es por (aduana, anio, dua_numero con 6 digitos). Ojo: la hoja
    guarda aduana/anio/dua como enteros, hay que normalizarlos a texto.
    """
    from openpyxl import load_workbook
    from openpyxl.styles import Font
    from openpyxl.utils import get_column_letter

    items = defaultdict(list)
    for s in serie:
        items[(str(s.get("aduana")), str(s.get("anio")), s.get("dua"))].append(s)
    cab = {}
    for c in consulta:
        cab.setdefault((str(c.get("aduana")), str(c.get("anio")), c.get("dua")), c)

    wb = load_workbook(CONSOLIDADO)
    ws = wb[HOJA_BASE25]
    H = [c.value for c in ws[1]]
    iA, iY, iD = H.index("aduana_codigo"), H.index("anio"), H.index("dua_numero")

    # idempotente: si las columnas ya existen se reutilizan en vez de duplicarlas
    nuevas = (["n_items_pdf", "estado_pdf"] + ["pdf_item_%d" % (i + 1)
                                              for i in range(MAX_ITEMS)]
              + ["pdf_cabecera"])
    existentes = [H.index(n) + 1 for n in nuevas if n in H]
    c0 = min(existentes) if existentes else len(H) + 1
    for j, nombre in enumerate(nuevas):
        col = c0 + j
        ws.cell(row=1, column=col, value=nombre).font = Font(bold=True)

    LINK = Font(color="0563C1", underline="single")
    con_pdf = con_cab = sin_pdf = 0
    for r in range(2, ws.max_row + 1):
        dua = ws.cell(row=r, column=iD + 1).value
        if dua in (None, ""):
            continue
        k = (str(ws.cell(row=r, column=iA + 1).value).zfill(3),
             str(ws.cell(row=r, column=iY + 1).value), str(dua).zfill(6))
        its = sorted(items.get(k, []), key=lambda s: int(s.get("item") or 0))
        c = cab.get(k)
        if its:
            con_pdf += 1
            estado = "RESUELTO" if c else "ITEMS SIN CABECERA"
        else:
            sin_pdf += 1
            estado = "SIN PDF EN CARPETA"
        if c:
            con_cab += 1

        ws.cell(row=r, column=c0, value=len(its))
        ws.cell(row=r, column=c0 + 1, value=estado)
        for j in range(MAX_ITEMS):
            cel = ws.cell(row=r, column=c0 + 2 + j)
            if j < len(its):
                ruta = os.path.join(PDF_DIR, its[j]["file"])
                cel.value = "file:///%s" % ruta.replace("\\", "/")
                cel.hyperlink = ruta          # enlace al archivo local
                cel.font = LINK
            else:
                # limpia enlaces de corridas anteriores: si la DUA perdio items o
                # el archivo se renombro/borro, el link viejo quedaria roto
                cel.value = None
                cel.hyperlink = None
        cel = ws.cell(row=r, column=c0 + 2 + MAX_ITEMS)
        if c:
            ruta = os.path.join(PDF_DIR, c["file"])
            cel.value = "file:///%s" % ruta.replace("\\", "/")
            cel.hyperlink = ruta
            cel.font = LINK
        else:
            cel.value = None
            cel.hyperlink = None

    for j in range(len(nuevas)):
        ws.column_dimensions[get_column_letter(c0 + j)].width = (
            30 if nuevas[j] == "estado_pdf" else 12)
    ws.freeze_panes = "A2"
    wb.save(CONSOLIDADO)
    return len(nuevas), con_pdf, con_cab, sin_pdf


def resumen_atributos_ruc(ru, atrib, n_desc):
    """Columnas de atributos agregados para una fila de 'por RUC'.

    Cada atributo se cuenta como cantidad de DUAs en las que el exportador lo
    declara, no como cantidad de items: un exportador que manda 6 items del
    mismo lote en una sola DUA cuenta 1. Cuando el valor es 0 significa que
    no se declara en ninguna DUA del exportador, no que el producto sea
    negativo; ver la nota de semantica en desc_items.py.
    """
    a = atrib.get(ru, {})
    out = [n_desc.get(ru, 0)]
    for col in RUC_ATRIB_SINO:
        out.append(len(a.get(col, ())))
    ics = a.get("series_ico", ())
    claves = a.get("claves_origen", ())
    out += [len(ics), ", ".join(sorted(ics)),
            len(claves), ", ".join(sorted(claves)),
            len(a.get("lotes", ())),
            len(a.get("marcas", ()))]
    return out


def agrupar_por_ruc(serie, consulta, excluir=None):
    """Una fila por RUC con el detalle desglosado por anio. Se agrega como hoja
    nueva: 'base 25 detallada' sigue intacta porque es el nivel de detalle por
    DUA y desde ahi se llega a los PDF.

    Las DUAs de `excluir` (discrepancia de FOB, ver hoja_discrepancias) no suman
    a los agregados: quedan aparte en su propia hoja.
    """
    from openpyxl import load_workbook
    from openpyxl.styles import Font
    from openpyxl.utils import get_column_letter

    excluye = {normaliza_k(k) for k in (excluir or ())}
    ws = load_workbook(CONSOLIDADO)[HOJA_BASE25]
    H = [c.value for c in ws[1]]
    i = {h: H.index(h) + 1 for h in H}
    g = lambda r, h: ws.cell(row=r, column=i[h]).value      # noqa: E731

    # razon social desde lo que se parseo de los PDF
    razon = {}
    for s in serie:
        r = s.get("ruc")
        if r and s.get("exportador") and len(s["exportador"]) > len(razon.get(r, "")):
            razon[r] = s["exportador"]

    ANIOS = (2024, 2025, 2026)
    acc = defaultdict(lambda: defaultdict(lambda: {
        "n": 0, "n_pdf": 0, "fob": 0.0, "peso": 0.0, "bultos": 0, "duas": []}))
    meta = {}
    for r in range(2, ws.max_row + 1):
        dua = g(r, "dua_numero")
        if dua in (None, ""):
            continue
        k = (str(g(r, "aduana_codigo")).zfill(3), str(g(r, "anio")),
             str(dua).zfill(6))
        if k in excluye:
            continue
        ru = str(g(r, "ruc")).zfill(11)
        an = g(r, "anio")
        a = acc[ru][an]
        a["n"] += 1
        a["duas"].append(str(dua).zfill(6))
        if g(r, "estado_pdf") != "SIN PDF EN CARPETA":
            a["n_pdf"] += 1
        for col, key in (("fob_pdf", "fob"), ("peso_neto_pdf", "peso"),
                         ("bultos_pdf", "bultos")):
            v = g(r, col)
            if v not in (None, ""):
                a[key] += float(v)
        m = meta.setdefault(ru, {"paises": set(), "aduanas": set(),
                                "agentes": set(), "anios": set()})
        for col, key in (("pais_codigo", "paises"), ("aduana_codigo", "aduanas"),
                         ("agente_codigo", "agentes")):
            if g(r, col) not in (None, ""):
                m[key].add(g(r, col))
        m["anios"].add(an)

    def head(a):
        return ["%s_n_duas" % a, "%s_n_duas_con_pdf" % a, "%s_fob" % a,
                "%s_peso_neto" % a, "%s_bultos" % a, "%s_duas" % a]

    H2 = (["ruc", "razon_social", "anios_con_datos"] + head("2024")
          + head("2025") + head("2026")
          + ["total_n_duas", "total_n_duas_con_pdf", "total_fob",
             "total_peso_neto", "total_bultos", "paises", "aduanas", "agentes",
             "aduanas_nombre", "agentes_nombre"]
          + H_RUC_ATRIB)

    cat = leer_catalogos()

    # Atributos agregados por RUC, tomados de los items del PDF Serie. Se
    # cuenta quantos items de cada exportador lo declaran, no quantos DUAs.
    atrib = defaultdict(lambda: defaultdict(set))
    n_desc = defaultdict(int)
    for s in serie:
        ru = s.get("ruc")
        if not ru:
            continue
        ru = str(ru)
        if s.get("descripcion"):
            n_desc[ru] += 1
        for col in RUC_ATRIB_SINO:
            if s.get(col):
                atrib[ru][col].add(s.get("dua"))
        if s.get("serie_ico"):
            atrib[ru]["series_ico"].add(s["serie_ico"])
        if s.get("clave_origen") is not None:
            atrib[ru]["claves_origen"].add(str(s["clave_origen"]))
        if s.get("lote"):
            atrib[ru]["lotes"].add(str(s["lote"]))
        if s.get("numero_marca"):
            atrib[ru]["marcas"].add(str(s["numero_marca"]))

    def nombres(codigos, hoja):
        return ", ".join(
            cat.get((hoja, str(x).zfill(3)), "?%s" % x)
            for x in sorted(codigos))

    filas = []
    for ru in sorted(acc, key=lambda x: (-sum(acc[x][y]["n"] for y in ANIOS), x)):
        tot = {"n": 0, "n_pdf": 0, "fob": 0.0, "peso": 0.0, "bultos": 0}
        fila = [ru, razon.get(ru),
                ",".join(str(y) for y in ANIOS
                         if acc[ru].get(y, {}).get("n"))]
        for y in ANIOS:
            a = acc[ru].get(y) or {"n": 0, "n_pdf": 0, "fob": 0.0,
                                   "peso": 0.0, "bultos": 0, "duas": []}
            for k in ("n", "n_pdf", "fob", "peso", "bultos"):
                tot[k] += a[k]
            fila += [a["n"], a["n_pdf"], round(a["fob"], 2), round(a["peso"], 2),
                     a["bultos"], ", ".join(sorted(a["duas"]))]
        m = meta[ru]
        fila += [tot["n"], tot["n_pdf"], round(tot["fob"], 2),
                 round(tot["peso"], 2), tot["bultos"],
                 ", ".join(str(x) for x in sorted(m["paises"])),
                 ", ".join(str(x) for x in sorted(m["aduanas"])),
                 ", ".join(str(x) for x in sorted(m["agentes"])),
                 nombres(m["aduanas"], "CAT_ADUANAS"),
                 nombres(m["agentes"], "CAT_AGENTES")]
        fila += resumen_atributos_ruc(ru, atrib, n_desc)
        filas.append(fila)

    wb = load_workbook(CONSOLIDADO)
    if "por RUC" in wb.sheetnames:
        del wb["por RUC"]
    out = wb.create_sheet("por RUC", 0)
    out.append(H2)
    for c in out[1]:
        c.font = Font(bold=True)
    for f in filas:
        out.append(f)
    out.freeze_panes = "B2"
    for j, nombre in enumerate(H2, 1):
        ancho = 46 if nombre == "razon_social" else (
            14 if nombre.endswith("_duas") and "total" not in nombre else 13)
        out.column_dimensions[get_column_letter(j)].width = ancho
    wb.save(CONSOLIDADO)
    return H2, filas


# --------------------------------------------------------------------------- #
def normalizar_anio_desde_url():
    """El 'anio' de 'base 25 detallada' es el parametro de consulta con el que se
    pidio el listado a SUNAT, no el anio que devolvio SUNAT: dua_canal_full.py parsea
ese valor (anio_dua) pero nunca lo escribe, asi que se perdio. La URL de detalle
    si la construye SUNAT y trae el anio de presentacion autoritativo (anoprese).
    Se alinea anio con anoprese. En este corpus solo difieren 4 filas.
    """
    from openpyxl import load_workbook

    wb = load_workbook(CONSOLIDADO)
    ws = wb[HOJA_BASE25]
    H = [c.value for c in ws[1]]
    iY, iU = H.index("anio") + 1, H.index("url_detalle") + 1
    cambios = []
    for r in range(2, ws.max_row + 1):
        m = _URLPAT.search(str(ws.cell(row=r, column=iU).value or ""))
        if not m:
            continue
        y = int(m.group(2))            # grupo 2 = anoprese
        if int(ws.cell(row=r, column=iY).value) != y:
            cambios.append((ws.cell(row=r, column=H.index("dua_numero") + 1).value,
                            int(ws.cell(row=r, column=iY).value), y))
            ws.cell(row=r, column=iY).value = y
            # el mes viene del mismo parametro de consulta que el anio; en estas
            # filas ya venia en 1 y se deja fijo para que anio/mes sean coherentes
            ws.cell(row=r, column=H.index("mes") + 1).value = 1
    if cambios:
        wb.save(CONSOLIDADO)
    return cambios


def hoja_pendientes():
    """Hoja con las DUAs que aun NO tienen PDF en la carpeta, con la URL de SUNAT
    como hipervinculo clicable. Se refresca en cada corrida: al descargar el PDF y
    volver a ejecutar el pipeline, la DUA sale de la lista sola.

    Notar que url_detalle siempre lleva anoprese=anio, ver normalizar_anio_desde_url.
    """
    from openpyxl import load_workbook
    from openpyxl.styles import Font
    from openpyxl.utils import get_column_letter

    wb = load_workbook(CONSOLIDADO)
    ws0 = wb[HOJA_BASE25]
    H = [c.value for c in ws0[1]]
    col = {h: H.index(h) + 1 for h in H}

    # conserva las notas que haya escrito el usuario, por DUA
    notas = {}
    if HOJA_PEND in wb.sheetnames:
        hp = wb[HOJA_PEND]
        Hp = [c.value for c in hp[1]]
        if "dua_numero" in Hp and "notas" in Hp:
            for r in range(2, hp.max_row + 1):
                d = hp.cell(row=r, column=Hp.index("dua_numero") + 1).value
                n = hp.cell(row=r, column=Hp.index("notas") + 1).value
                if d and n:
                    notas[str(d).zfill(6)] = n

    cab = ["ruc", "dua_numero", "anio", "mes", "aduana_codigo", "agente_codigo",
           "pais_codigo", "fecha_embarque", "url_detalle", "notas"]
    filas = []
    for r in range(2, ws0.max_row + 1):
        if ws0.cell(row=r, column=col["estado_pdf"]).value != "SIN PDF EN CARPETA":
            continue
        dua = str(ws0.cell(row=r, column=col["dua_numero"]).value).zfill(6)
        filas.append([ws0.cell(row=r, column=col[h]).value for h in cab[:-1]]
                     + [notas.get(dua, "")])
    filas.sort(key=lambda x: (x[2] or 0, x[3] or 0, x[1]))

    if HOJA_PEND in wb.sheetnames:
        del wb[HOJA_PEND]
    out = wb.create_sheet(HOJA_PEND)
    out.append(cab)
    for c in out[1]:
        c.font = Font(bold=True)
    LINK = Font(color="0563C1", underline="single")
    for f in filas:
        out.append(f)
        cel = out.cell(row=out.max_row, column=cab.index("url_detalle") + 1)
        cel.hyperlink = str(cel.value)
        cel.font = LINK
    out.freeze_panes = "A2"
    out.auto_filter.ref = "A1:%s%d" % (get_column_letter(len(cab)), out.max_row)
    for j, nombre in enumerate(cab, 1):
        out.column_dimensions[get_column_letter(j)].width = \
            62 if nombre == "url_detalle" else (24 if nombre == "notas" else 13)
    wb.save(CONSOLIDADO)
    return len(filas)


def recalcular_fob(serie, consulta):
    """Fija fob_pdf de forma autoritativa: el 6.5 de la cabecera si existe (es el
    total del propio documento), si no la suma del FOB de los items.

    Es necesario recalcular, no solo rellenar: el extractor legado
    (enriquecer_base_v2.py:31-40) deja valores corruptos en celdas YA ocupadas --
    valores pegados al piso de su ventana magica (50,000.00 / 100,000.00) y a
    veces un unico item en vez de la suma. Esos casos sin cabecera no los
    detectaba la correccion por cabecera, y quedaban subestimados.
    """
    from openpyxl import load_workbook

    suma = {}
    for s in serie:
        k = str(s.get("dua")).zfill(6)
        suma[k] = round(suma.get(k, 0.0) + float(s.get("fob") or 0), 3)

    fob_cab = {}
    for c in consulta:
        if c.get("valor_neto_fob"):
            fob_cab[str(c.get("dua")).zfill(6)] = float(c["valor_neto_fob"])

    wb = load_workbook(CONSOLIDADO)
    ws = wb[HOJA_BASE25]
    H = [c.value for c in ws[1]]
    iF, iD = H.index("fob_pdf") + 1, H.index("dua_numero") + 1

    cambios = []
    for r in range(2, ws.max_row + 1):
        dua = str(ws.cell(row=r, column=iD).value or "").zfill(6)
        if dua in fob_cab:
            v, origen = round(fob_cab[dua], 2), "cabecera"
        elif dua in suma:
            v, origen = round(suma[dua], 2), "items"
        else:
            continue
        antes = ws.cell(row=r, column=iF).value
        if antes not in (None, "") and abs(float(antes) - v) < 0.01:
            continue
        ws.cell(row=r, column=iF).value = v
        cambios.append((dua, antes, v, origen))

    if cambios:
        wb.save(CONSOLIDADO)
    return cambios


def normaliza_k(k):
    """(aduana, anio, dua) de las claves internas -> comparable con la hoja."""
    return (str(k[0]).zfill(3), str(k[1]), str(k[2]).zfill(6))


def excluir_items_fantasma(serie, consulta):
    """Retira los items sobrantes de las DUAs cuya suma de FOB supera el 6.5 de la
    cabecera. Mandan los datos del documento: en este corpus, para las 7 DUAs
    afectadas, el FOB, el peso neto y los bultos de la cabecera coinciden con el
    item 1, de modo que los S2/S3 sobrantes no son mercancia de esa DUA (una DUA
    no admite items nuevos despues de numerarse sin rectificatoria).

    Se quitan de mayor a menor FOB, nunca el de menor numero de item, y solo si
    al hacerlo la suma cuadra con el 6.5. Si no cuadra, se descarta el resto y
    queda el item 1, que es el que la cabecera respalda.
    """
    ref = {}
    for c in consulta:
        if c.get("valor_neto_fob"):
            ref[normaliza_k((c.get("aduana"), c.get("anio"), c.get("dua")))] = \
                float(c["valor_neto_fob"])

    por = defaultdict(list)
    for s in serie:
        por[normaliza_k((s.get("aduana"), s.get("anio"), s.get("dua")))].append(s)

    fuera, quitan = set(), []
    for k, its in por.items():
        if k not in ref:
            continue
        tot = sum(float(s.get("fob") or 0) for s in its)
        if tot - ref[k] <= 0.05:
            continue
        # el item de menor numero nunca se retira: es el que respalda la cabecera
        primero = min(its, key=lambda s: int(s.get("item") or 0))
        for s in sorted((x for x in its if x is not primero),
                        key=lambda x: -float(x.get("fob") or 0)):
            if tot - float(s.get("fob") or 0) >= ref[k] - 0.05:
                tot -= float(s.get("fob") or 0)
                fuera.add(id(s))
                quitan.append((k, primero, s, round(ref[k] - tot, 2)))
    limpia = [s for s in serie if id(s) not in fuera]
    return limpia, quitan


def hoja_items_excluidos(quitan):
    """Rastro de los items retirados, para que la exclusion sea auditable."""
    from openpyxl import load_workbook
    from openpyxl.styles import Font
    from openpyxl.utils import get_column_letter

    if not quitan:
        wb = load_workbook(CONSOLIDADO)
        if HOJA_DISC in wb.sheetnames:
            del wb[HOJA_DISC]
            wb.save(CONSOLIDADO)
        return 0

    # la hoja de cuarentena quedo obsoleta: las DUAs se corrigen, no se apartan
    wb = load_workbook(CONSOLIDADO)
    if HOJA_DISC in wb.sheetnames:
        del wb[HOJA_DISC]

    cab = ["aduana_codigo", "anio", "dua_numero", "ruc", "item_excluido",
           "fob_excluido", "bultos_excluido", "peso_neto_excluido", "archivo",
           "item_conservado", "fob_6_5_cabecera", "motivo"]
    filas = []
    for k, primero, s, resto in quitan:
        filas.append([k[0], k[1], k[2], primero.get("ruc"), s.get("item"),
                      s.get("fob"), s.get("bultos"), s.get("peso_neto"),
                      s.get("file"), primero.get("item"), round(resto, 2),
                      "suma de items > 6.5 de la cabecera; la cabecera coincide "
                      "con el item %s" % primero.get("item")])
    filas.sort(key=lambda x: (x[1], x[2], x[4]))

    if HOJA_EXCL in wb.sheetnames:
        del wb[HOJA_EXCL]
    out = wb.create_sheet(HOJA_EXCL)
    out.append(cab)
    for c in out[1]:
        c.font = Font(bold=True)
    for f in filas:
        out.append(f)
    out.freeze_panes = "A2"
    out.auto_filter.ref = "A1:%s%d" % (get_column_letter(len(cab)), out.max_row)
    for j, nombre in enumerate(cab, 1):
        out.column_dimensions[get_column_letter(j)].width = \
            52 if nombre == "motivo" else (44 if nombre == "archivo" else 14)
    wb.save(CONSOLIDADO)
    return len(filas)


def sincronizar_consolidado():
    """Reescribe 'DUA_Consolidado_Total' desde 'base 25 detallada'.

    Esa pestana la dejo enriching_final.py antes de las correcciones y se quedo
    contradiciendo a la buena: 84 fob_pdf distintos, 63 vacios y 3 anios erroneos.
    Ahora se deriva de la hoja master, asi que no puede divergir.
    """
    from openpyxl import load_workbook
    from openpyxl.styles import Font
    from openpyxl.utils import get_column_letter

    wb = load_workbook(CONSOLIDADO)
    src = wb[HOJA_BASE25]
    H = [c.value for c in src[1]]

    cols = ["ruc", "dua_numero", "anio", "mes", "aduana_codigo", "agente_codigo",
            "pais_codigo", "dua_numero_orig", "fecha_embarque", "canal",
            "url_detalle", "fob_pdf", "peso_neto_pdf", "bultos_pdf",
            "tipo_bulto", "subpartida"]
    origen = [c for c in cols if c != "dua_numero_orig" and c not in H]
    if origen:                      # no deberia pasar: la hoja master no cambia
        raise KeyError("columnas ausentes en '%s': %s" % (HOJA_BASE25, origen))
    filas = []
    for r in range(2, src.max_row + 1):
        if src.cell(row=r, column=H.index("dua_numero") + 1).value in (None, ""):
            continue
        vals = []
        for c in cols:
            # dua_numero_orig no vive en la hoja master: es el numero tal cual venia
            if c == "dua_numero_orig":
                vals.append(src.cell(row=r, column=H.index("dua_numero") + 1).value)
            else:
                vals.append(src.cell(row=r, column=H.index(c) + 1).value)
        filas.append(vals)

    if HOJA_CONS in wb.sheetnames:
        del wb[HOJA_CONS]
    out = wb.create_sheet(HOJA_CONS)
    out.append(cols)
    for c in out[1]:
        c.font = Font(bold=True)
    LINK = Font(color="0563C1", underline="single")
    for f in filas:
        out.append(f)
        cel = out.cell(row=out.max_row, column=cols.index("url_detalle") + 1)
        if cel.value:
            cel.hyperlink = str(cel.value)
            cel.font = LINK
    out.freeze_panes = "A2"
    out.auto_filter.ref = "A1:%s%d" % (get_column_letter(len(cols)), out.max_row)
    for j, nombre in enumerate(cols, 1):
        out.column_dimensions[get_column_letter(j)].width = \
            62 if nombre == "url_detalle" else 13
    wb.save(CONSOLIDADO)
    return len(filas)


def catalogo_codigos(consulta):
    """Resuelve el nombre de cada aduana y de cada agente de comercio.

    Los codigos (aduana_codigo, agente_codigo) vienen de SUNAT, pero SUNAT no
    publica el nombre junto al dato; la fuente autoritativa es el propio PDF,
    que ya quedó parseado: aduana_nombre viene de 'REGISTRO DE ADUANA' y el
    agente es el declarante ('8 DECLARANTE': RUC + razon social).

    Cuando un codigo trae mas de una variante gana la mas frecuente (las
    diferencias suelen ser solo de puntuacion). Deja hojas CAT_ADUANAS y
    CAT_AGENTES.
    """
    from openpyxl import load_workbook
    from openpyxl.styles import Font

    ws = load_workbook(CONSOLIDADO)[HOJA_BASE25]
    H = [c.value for c in ws[1]]
    i = {h: H.index(h) + 1 for h in H}

    decl = {}
    for c in consulta:
        k = (str(c.get("aduana")), str(c.get("anio")), str(c.get("dua")))
        nombre = c.get("declarante")
        if nombre and k not in decl:
            decl[k] = (str(nombre).strip(), str(c.get("declarante_ruc") or ""))

    # El PDF de la DUA imprime el acronimo, no el nombre. Esta equivalencia se
    # verifico contra las DUs oficiales de SUNAT, que la listan asi.
    ADUANA_OFICIAL = {"235": "AEREA Y POSTAL EX-IAAC"}

    ad_acc, ag_acc = defaultdict(Counter), defaultdict(Counter)
    for c in consulta:
        ad, nom = c.get("aduana"), c.get("aduana_nombre")
        if ad and nom:
            k = str(ad).zfill(3)
            ad_acc[k][ADUANA_OFICIAL.get(k, " ".join(str(nom).split()))] += 1

    for r in range(2, ws.max_row + 1):
        dua = ws.cell(row=r, column=i["dua_numero"]).value
        if dua in (None, ""):
            continue
        ag = ws.cell(row=r, column=i["agente_codigo"]).value
        if ag in (None, ""):
            continue
        k = (str(ws.cell(row=r, column=i["aduana_codigo"]).value).zfill(3),
             str(ws.cell(row=r, column=i["anio"]).value),
             str(dua).zfill(6))
        if k in decl:
            ag_acc[str(ag).strip()][decl[k]] += 1

    wb = load_workbook(CONSOLIDADO)
    hojas = [("CAT_ADUANAS", ["codigo", "nombre", "n_duas"],
              [(k, ad_acc[k].most_common(1)[0][0], sum(ad_acc[k].values()))
               for k in sorted(ad_acc)]),
             ("CAT_AGENTES", ["codigo", "nombre", "ruc", "n_duas"],
              [(k, ag_acc[k].most_common(1)[0][0][0],
                ag_acc[k].most_common(1)[0][0][1], sum(ag_acc[k].values()))
               for k in sorted(ag_acc)])]
    for titulo, cab, filas in hojas:
        if titulo in wb.sheetnames:
            del wb[titulo]
        sh = wb.create_sheet(titulo)
        sh.append(cab)
        for c in sh[1]:
            c.font = Font(bold=True)
        for f in filas:
            sh.append(list(f))
        sh.freeze_panes = "A2"
        for col, w in (("A", 12), ("B", 52), ("C", 18), ("D", 10)):
            sh.column_dimensions[col].width = w
    wb.save(CONSOLIDADO)
    return ad_acc, ag_acc


def leer_catalogos():
    """codigo -> nombre, leido de las hojas de catalogo del consolidado."""
    from openpyxl import load_workbook

    out = {}
    try:
        wb = load_workbook(CONSOLIDADO, read_only=True)
    except Exception:                                   # noqa: BLE001
        return out
    for titulo in ("CAT_ADUANAS", "CAT_AGENTES"):
        if titulo not in wb.sheetnames:
            continue
        for row in wb[titulo].iter_rows(min_row=2, values_only=True):
            if row[0] is None:
                continue
            clave = str(row[0]).strip()
            out[(titulo, clave.zfill(3))] = row[1]
            out[(titulo, clave)] = row[1]
    return out


def integrar_minagri():
    """Vuelca la hoja 'por RUC' del consolidado dentro del directorio de MINAGRI,
    emparejando por RUC y empezando en MINAGRI_COL_INICIO.

    Antes de escribir limpia el bloque previo que hubiera en esas columnas (si
    'por RUC' cambio de ancho, si no quedan restos del bloque viejo), deja el
    archivo anterior como respaldo y despues relee lo guardado para confirmar
    que cada fila escrita coincide con el consolidado. Devuelve un resumen o
    None si el destino no existe.
    """
    from copy import copy
    from datetime import datetime

    import shutil

    from openpyxl import load_workbook
    from openpyxl.utils import get_column_letter

    if not MINAGRI_XLSX or not os.path.exists(MINAGRI_XLSX):
        return None

    src = load_workbook(CONSOLIDADO)[HOJA_RUC]
    H2 = [c.value for c in src[1]]
    ncols = len(H2)
    datos = {}
    for r in range(2, src.max_row + 1):
        ruc = src.cell(row=r, column=1).value
        if ruc not in (None, ""):
            datos[str(ruc).zfill(11)] = [src.cell(row=r, column=c).value
                                        for c in range(1, ncols + 1)]

    wb = load_workbook(MINAGRI_XLSX)
    ws = wb[MINAGRI_HOJA]
    for r in range(1, ws.max_row + 1):
        for c in range(MINAGRI_COL_INICIO, ws.max_column + 1):
            ws.cell(row=r, column=c).value = None

    estilo = ws.cell(row=1, column=77)
    fmt = {}
    for i, h in enumerate(H2):
        col = MINAGRI_COL_INICIO + i
        c = ws.cell(row=1, column=col)
        c.value = h
        if estilo.has_style:
            c.font = copy(estilo.font)
            c.alignment = copy(estilo.alignment)
            c.fill = copy(estilo.fill)
            c.border = copy(estilo.border)
        if any(k in str(h) for k in ("fob", "peso_neto")):
            fmt[col] = "#,##0.00"
        elif "bultos" in str(h) or "n_duas" in str(h) or h == "ruc":
            fmt[col] = "#,##0"

    escritas, sin_match = 0, []
    for r in range(2, ws.max_row + 1):
        ruc = ws.cell(row=r, column=MINAGRI_COL_RUC).value
        if ruc in (None, ""):
            continue
        ruc = str(ruc).zfill(11)
        vals = datos.get(ruc)
        if vals is None:
            sin_match.append(ruc)
            continue
        for i, v in enumerate(vals):
            col = MINAGRI_COL_INICIO + i
            c = ws.cell(row=r, column=col)
            if i == 0:
                c.value = ruc
                c.number_format = "@"
            else:
                c.value = v
                if col in fmt and isinstance(v, (int, float)):
                    c.number_format = fmt[col]
        escritas += 1

    for col in range(MINAGRI_COL_INICIO, MINAGRI_COL_INICIO + ncols):
        ws.column_dimensions[get_column_letter(col)].width = (
            44 if H2[col - MINAGRI_COL_INICIO] in ("razon_social", "agentes_nombre",
                                                  "aduanas_nombre")
            else 16)

    bak = None
    if os.path.isdir(MINAGRI_BACKUP_DIR):
        bak = os.path.join(MINAGRI_BACKUP_DIR, "minagri_backup_%s.xlsx"
                           % datetime.now().strftime("%Y%m%d_%H%M%S"))
        shutil.copy2(MINAGRI_XLSX, bak)

    wb.save(MINAGRI_XLSX)

    # releer para verificar contra el consolidado
    chk = load_workbook(MINAGRI_XLSX)[MINAGRI_HOJA]
    ok = 0
    for r in range(2, chk.max_row + 1):
        ruc = chk.cell(row=r, column=MINAGRI_COL_RUC).value
        if ruc in (None, ""):
            continue
        ruc = str(ruc).zfill(11)
        if ruc not in datos:
            continue
        leido = [chk.cell(row=r, column=MINAGRI_COL_INICIO + i).value
                 for i in range(ncols)]
        ok += leido == [ruc] + datos[ruc][1:]

    return {"columnas": "%s:%s" % (get_column_letter(MINAGRI_COL_INICIO),
                                   get_column_letter(MINAGRI_COL_INICIO + ncols - 1)),
            "ncols": ncols, "escritas": escritas, "sin_match": sin_match,
            "verificadas": ok, "bak": bak}


def main():
    normalizar_anio_desde_url()
    serie, consulta, errores, desconocidos = leer_corpus()
    serie, dups = deduplicar(serie)
    serie, quitan = excluir_items_fantasma(serie, consulta)
    filas, sin_cabecera = construir_items(serie, consulta)
    duas = construir_duas(serie, consulta)
    cambios_fob = recalcular_fob(serie, consulta)

    with open(JSON_OUT, "w", encoding="utf-8") as fh:
        json.dump({"serie": serie, "consulta": consulta, "errores": errores,
                   "desconocidos": desconocidos, "duplicados": dups,
                   "items_excluidos": [
                       {"aduana": k[0], "anio": k[1], "dua": k[2],
                        "item": s.get("item"), "fob": s.get("fob"),
                        "bultos": s.get("bultos"), "archivo": s.get("file")}
                       for k, _p, s, _r in quitan]},
                  fh, ensure_ascii=False, indent=1)

    faltan, exceden, por_dua = escribir_excel(
        serie, consulta, filas, duas, sin_cabecera, dups, errores, desconocidos)

    ncols, con_pdf, con_cab, sin_pdf = enlazar_base25(serie, consulta)
    n_excl = hoja_items_excluidos(quitan)
    ad_acc, ag_acc = catalogo_codigos(consulta)
    H2, filas_ruc = agrupar_por_ruc(serie, consulta, exceden)
    n_cons = sincronizar_consolidado()
    n_pend = hoja_pendientes()
    mi = integrar_minagri()

    print("Excel: %s" % CONSOLIDADO)
    print("JSON : %s" % JSON_OUT)
    print("\nitems=%d  cabeceras=%d  errores=%d  no reconocidos=%d  duplicados=%d"
          % (len(serie), len(consulta), len(errores), len(desconocidos), len(dups)))
    print("filas DETALLE_ITEMS=%d  filas DUAS=%d" % (len(filas), len(duas)))
    print("\nfob_pdf actualizado (cabecera si existe, si no suma de items): %d DUAs"
          % len(cambios_fob))
    for dua, antes, ahora, origen in cambios_fob:
        prev = "%12.2f" % float(antes) if antes not in (None, "") else "      vacio"
        print("   dua %-7s %s -> %12.2f  (%s)" % (dua, prev, ahora, origen))
    print("\nDUAs con items realmente faltantes: %d %s" % (len(faltan), faltan))
    print("DUAs con items de mas:             %d %s" % (len(exceden), exceden))
    print("  items fantasma retirados: %d -> hoja '%s'" % (n_excl, HOJA_EXCL))
    print("  '%s' resincronizada desde '%s': %d filas"
          % (HOJA_CONS, HOJA_BASE25, n_cons))
    print("DUAs sin PDF de cabecera (dato redundante, NO incompletas): %d"
          % len(por_dua))
    print("\nbase 25 detallada: +%d columnas en %s" % (ncols, CONSOLIDADO))
    print("  con PDF de items: %d   ademas con cabecera: %d   sin PDF: %d"
          % (con_pdf, con_cab, sin_pdf))
    print("  hoja 'por RUC': %d filas x %d columnas (un RUC por fila)"
          % (len(filas_ruc), len(H2)))
    print("  catalogos: %d aduanas y %d agentes resueltos a nombre"
          % (len(ad_acc), len(ag_acc)))
    if mi:
        print("\nMINAGRI %s" % MINAGRI_XLSX)
        print("  bloque %s (%d columnas) escrito desde '%s'"
              % (mi["columnas"], mi["ncols"], HOJA_RUC))
        print("  filas escritas: %d   verificadas contra el consolidado: %d"
              % (mi["escritas"], mi["verificadas"]))
        if mi["sin_match"]:
            print("  RUCs del directorio sin DUAs en el consolidado (%d): %s"
                  % (len(mi["sin_match"]), ", ".join(mi["sin_match"])))
        print("  respaldo del archivo anterior: %s" % (mi["bak"] or "(sin respaldo)"))
    print("  hoja '%s': %d DUAs sin PDF (URL clicable; se refresca al re-ejecutar)"
          % (HOJA_PEND, n_pend))
    for f, e in errores:
        print("  ERROR %s %s" % (f, e))
    for f in desconocidos:
        print("  NO RECONOCIDO %s" % f)


if __name__ == "__main__":
    sys.exit(main())
