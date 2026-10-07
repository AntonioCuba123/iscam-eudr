"""
Limpieza y clasificacion del campo 7.35 (descripcion de mercancia)
=================================================================

El campo 7.35 de los PDF "Serie" de la DUA trae la descripcion libre del
item, pero el PDF la entrega en un formato que hay que reconstruir:

  1) MOJIBAKE. El PDF esta en latin-1 y PyMuPDF lo entrega como si fuera
     UTF-8: "DescripciÃ³n", "MercancÃ­as". Sin corregir, el 37.5% de los
     items arrastra el error y las palabras acentuadas quedan inservibles
     para buscar por nombre ("ORGANICO" vs "ORGÃNICO").

  2) REPETICION. El formulario imprime la misma descripcion numerada
     ("1. ...", "2. ...", "3. ..." ...) una vez por cada linea fisica que
     ocupa. Trocear por el numero de linea y deduplicar es correcto solo
     si el corte cae en el mismo punto que el corte del PDF; cuando no, los
     fragmentos quedan pegados a mitad de frase y el resultado es ilegible.

3) CLASIFICACION. El texto contiene atributos de trazabilidad que no se
     separan en ninguna columna: si el producto es organico, que variedad
     es, que proceso tuvo, que certificacion, y los codigos de identificacion
     que el exportador escribe a mano dentro de la mercancia. Estos ultimos
     son los que mas importan para EUDR y hay que separarlos bien:

       - SERIE ICO: numero de serie del certificado de origen que la Camara
         Peruana del Cafe y Cacao emite ante la Organizacion Internacional
         del Cafe. Se solicita POR OPERACION O LOTE. NO identifica a un
         productor ni permite llegar a la parcela.
       - NUMERO DE MARCA: rotulo impreso en el saco. Lleva la clave de pais,
         un bloque central que se mantiene estable dentro de un mismo
         exportador, y el numero de serie de la partida.

     Ambos tienen el mismo formato NN-AAA-NNN, asi que se distinguen por la
     etiqueta que los precede en el documento ("ICO:" frente a "MARCA:"),
     nunca por la forma del codigo.

Que hace este modulo
-------------------
  limpiar_descripcion(txt)  -> texto reconstruido, sin mojibake ni cortes
  clasificar(txt_limpio)    -> dict de atributos
  resumen                   -> diccionario para buscar de forma inclusiva
                               ("organico" encuentra "ORGÃNICO")
"""

import re
import unicodedata

# --------------------------------------------------------------------------- #
# 1. Mojibake
# --------------------------------------------------------------------------- #

MOJI_TAGS = ("Ã¡", "Ã©", "Ã­", "Ã³", "Ãº", "Ã±", "Ã¼",
             "Ã", "Ã‰", "Ã", "Ã", "Ã", "Ã", "Ãœ")


def _repara_mojibake(txt):
    """latin-1 leido como utf-8 y viceversa. Idempotente."""
    if not txt:
        return ""
    t = txt
    for _ in range(2):
        antes = t
        # caso habitual: los bytes utf-8 quedaron marcados como latin-1
        if any(tag in t for tag in MOJI_TAGS):
            try:
                t = t.encode("latin-1", "strict").decode("utf-8", "strict")
            except (UnicodeEncodeError, UnicodeDecodeError):
                t = t.encode("cp1252", "ignore").decode("utf-8", "ignore")
        if t == antes:
            break
    return t


def _sin_acentos(txt):
    """Para comparar y buscar: 'organico' y 'orgánico' deben ser la misma."""
    t = unicodedata.normalize("NFKD", txt)
    return "".join(c for c in t if not unicodedata.combining(c))


# --------------------------------------------------------------------------- #
# 2. Reconstruccion de la repeticion
# --------------------------------------------------------------------------- #

# las lineas del PDF se parten en puntos fijos de 69 caracteres; cuando el
# troceo por numero de linea no coincide, sobra un prefijo o un sufijo del
# fragmento anterior. Se detecta el solapamiento explicito.
_SPLIT_LINEA = re.compile(r"(?<!\d)(\d{1,2})\.\s*")
# El PDF escribe la etiqueta partida en dos lineas fisicas y el pipeline
# previo ya le quitó "Mercancías", dejando "Descripción" sola. Se contemplan
# las dos formas: pareja y huérfana.
_CABECERA = re.compile(
    r"(Descripci[oó]n\s+Mercanc[ií]as"
    r"|Mercanc[ií]as\s+Descripci[oó]n"
    r"|Descripci[oó]n(?:\s+Mercanc[ií]as)?"
    r"|Mercanc[ií]as)", re.I)


def _trocea_numerado(region):
    """Divide la region 7.35 por sus marcadores '1.', '2.', ... .
    Devuelve la lista de lineas fisicas en orden.

    La region suele empezar con la etiqueta 'Descripcion Mercancias', que NO
    lleva numero de linea y por tanto queda pegada al primer fragmento. Se
    separa antes de trocear para que la cabecera no sobreviva en el texto.
    """
    if not region:
        return []
    region = _CABECERA.sub(" ", region)
    partes = _SPLIT_LINEA.split(region)
    # split con grupo devuelve [pre, num, texto, num, texto, ...]
    lineas = []
    sobrante = partes[0].strip(" .-") if partes else ""
    for i in range(1, len(partes) - 1, 2):
        num = partes[i]
        txt = partes[i + 1]
        if not num or not txt or not txt.strip():
            continue
        if i == 1 and sobrante:
            # la etiqueta sin numerar precedia al item 1
            txt = sobrante + " " + txt
        lineas.append((int(num), txt))
    if not lineas:
        limpia = _CABECERA.sub(" ", region)
        return [limpia] if limpia.strip() else []
    return [t for _n, t in lineas]


def _quita_repeticiones(txt):
    """Elimina la repeticion en bloque cuando el PDF entrega la descripcion
    dos veces seguidas y el pipeline previo ya perdio los marcadores '1.', '2.'

    Se detecta por periodicidad: si la primera mitad del texto vuelve a
    aparecer mas adelante, se corta en el segundo comienzo. Es la operacion
    inversa de la deduplicacion por linea, y hace falta porque el recorte del
    campo en el pipeline previo (7.35 -> 7.36) arrastra la repeticion entera.
    """
    t = re.sub(r"\s+", " ", txt).strip()
    if len(t) < 40:
        return t

    n = len(t)
    # la repeticion puede empezar en la mitad exacta o algo antes/despues
    for corte in range(n // 2, min(n // 2 + 25, n)):
        primero = t[:corte].rstrip(" .-")
        if len(primero) < 20:
            continue
        resto = t[corte:].lstrip(" .-")
        if resto.startswith(primero[:max(20, len(primero) - 15)]):
            return primero
    return t


def _pega_lineas(lineas):
    """Une las lineas fisicas en una sola descripcion, evitando repetir.

    El PDF reimpone la MISMA descripcion en cada linea numerada cuando el
    texto es largo, y reparte el texto en varias lineas cuando es corto. Los
    dos casos se distinguen por el patron:

      caso A (texto largo, reimpuesto):  'CAFE VERDE ... 69' / 'KG CONSUMO'
                                          -> la 2a linea CONTINUA la 1a.
      caso B (texto corto, una sola vez): cada linea es la descripcion
                                          COMPLETA, y la 2a onwards repiten.

    En el caso B la deduplicacion exacta es suficiente. En el caso A hay que
    descartar el prefijo que se solapa con el final de la linea anterior.
    """
    if not lineas:
        return ""

    limpias = [re.sub(r"\s+", " ", ln).strip(" .-") for ln in lineas]
    limpias = [ln for ln in limpias if ln]

    # deduplicacion exacta conservando orden
    vistas, unicas = set(), []
    for ln in limpias:
        if ln not in vistas:
            vistas.add(ln)
            unicas.append(ln)

    # si quedan 2+ lineas y son identicas o una contiene a la otra, el PDF
    # estaba reimprimiendo la MISMA descripcion: gana la version mas larga.
    if len(unicas) >= 2:
        a = unicas[0]
        for b in unicas[1:]:
            if a in b:
                a = b
            elif b in a:
                pass
            else:
                a = None
                break
        if a:
            return a

    # caso distinto: las lineas son trozos que se CORTO la descripcion.
    # se concatenan detectando el solapamiento con la anterior.
    if len(unicas) >= 2:
        a, b = unicas[0], unicas[1]
        for k in range(min(len(a), len(b)), 3, -1):
            if a[-k:] == b[:k]:
                return a + b[k:]

    return " ".join(unicas)


def limpiar_descripcion(txt, maxlen=600):
    """Devuelve la descripcion reconstruida, sin mojibake ni repeticiones."""
    if not txt:
        return None
    t = _repara_mojibake(txt)
    t = _CABECERA.sub(" ", t)
    t = re.sub(r"[\u00a0\u2007\u202f]", " ", t)
    lineas = _trocea_numerado(t)
    limpio = _pega_lineas(lineas)
    limpio = _quita_repeticiones(limpio)
    limpio = re.sub(r"\s+", " ", limpio).strip(" .-")
    if not limpio:
        return None
    return limpio[:maxlen]


# --------------------------------------------------------------------------- #
# 3. Clasificacion
# --------------------------------------------------------------------------- #

# (atributo, regex sobre el texto SIN acentos y en mayusculas)
REGLAS = (
    # --- certificacion organica ---
    ("organico",
     r"\bORGANIC(?:O|A|OS|AS)?\b|\bECO\s?ORGANIC\b|\bBIOL[OÓ]GIC\w*\b"),
    ("fairtrade",
     r"\bFAIR\s?-?\s?TRADE\b|\bFAIRTRADE\b|\bFT\s?100\b"),
    ("rainforest",
     r"\bRAINFOREST\b|\bRFA\b|\bRAINFOREST\s+ALLIANCE\b"),
    ("utz_jbs",
     r"\bUTZ\b|\bJBS\b"),
    ("sustentable_cert",
     r"\bSUSTAINABLE\b|\bREGENERATIV\w*\b|\bAGROFOREST\w*\b"),
    # --- variedad ---
    ("arabica", r"\bARABICA\b|\bARABIC\w*\b"),
    ("robusta", r"\bROBUSTA\b"),
    ("criollo", r"\bCRIOLLO\b|\bCRILLO\b"),
    ("trinitario", r"\bTRINITARIO\b"),
    ("forastero", r"\bFORASTERO\b"),
    ("amazonico", r"\bAMAZ[OÓ]NICO\b|\bAMAZONICO\b"),
    # --- proceso / presentacion ---
    ("washed", r"\bWASHED\b|\bLAVADO\b|\bPERGAMINO\b"),
    ("honey", r"\bHONEY\b|\bMIEL\b"),
    ("natural", r"\bNATURAL\b"),
    ("sun_dried", r"\bSUN\s?-?\s?DRY\w*\b|\bSECADO\s+AL\s+SOL\b"),
    ("en_grano", r"\bEN\s+GRANO\b|\bGREEN\s+COFFEE\b|\bBEANS?\b"),
    ("en_bolsa", r"\bBAGS?\s+OF\b|\bEN\s+BOLSAS?\b|\bSACOS?\b"),
    ("a_granel", r"\bA\s+GRANEL\b|\bGRANEL\b|\bBULK\b"),
    # --- uso ---
    ("consumo_humano",
     r"\bCONSUMO\s+HUMANO\b|\bALIMENTO\b|\bHUMAN\s+CONSUMPTION\b"),
    # --- identificadores ---
    ("marca", r"\bMARCA\b|\bBRAND\b"),
    ("lote", r"\bLOTE\b|\bLOT\b"),
    ("contrato", r"\bCONTRATO\b|\bCONTRACT\b"),
)

# El PDF pega el ICO al token anterior sin espacio: "... SACOS X 69 KGICO: ..."
# Por eso NO se exige limite de palabra antes de "ICO"; se exige que siga
# el separador y los digitos, que es lo que lo distingue de una palabra
# cualquiera terminada en "ico".
#
# Los tres separadores son reales en el corpus: COCLA escribe "30/11/4039",
# Valle Grande escribe "30-826-5005" y un tercer exportador "30-1234-4759".
# Una version anterior solo aceptaba "/" y perdia 4 de las 24 series ICO.
RE_ICO = re.compile(
    r"ICO\s*[:.]?\s*(\d{1,2})\s*[/\\-]\s*(\d{2,4})\s*[/\\-]\s*(\d{3,5})", re.I)
RE_FDA = re.compile(r"\bFDA\s*[:.]?\s*(\d{5,})", re.I)

# Codigo con la forma NN-AAA-NNN, usada tanto por la serie ICO como por el
# numero de marca. El separador se captura para exigir que ambos pasos usen
# el mismo (\ y / estan prohibidos en una clase de caracteres).
CODIGO_MARCA = re.compile(r"(\d{2})\s*([/\\-])\s*(\d{2,4})\s*\2\s*(\d{3,4})")
RE_PESO = re.compile(r"\b(\d{1,5})\s?(?:KG|GR)\b", re.I)
RE_PESO_CERO = re.compile(r"\b00\s?(?:KG|GR)\b", re.I)
RE_LOTE = re.compile(r"\bLOTE\s*(?:N?\.?\s*(?:N?°?\s*)?)?#?\s*([A-Z0-9\-]{3,})", re.I)
RE_MARCA = re.compile(r"\bMARCA\s*:?\s*([A-Z0-9\.\- ]{2,40})", re.I)

# Etiqueta que precede al codigo NN-AAA-NNN. Decide si lo que se esta
# leyendo es una SERIE ICO (certificado de origen por operacion) o un NUMERO
# DE MARCA (rotulo del saco). Son cosas distintas con el mismo formato.
RE_ETIQUETA_COD = re.compile(
    r"(ICO|MARCA|MARK|LOT|LOTE|CONTRATO|CONTRACT)\s*[:=\-]*\s*$", re.I)


def _codigos_marcados(txt_limpio):
    """Devuelve [(etiqueta, codigo, partes)] para cada codigo NN-AAA-NNN.

    El bloque central es la clave de origen: se repite de forma consistente
    dentro de un mismo exportador, que es lo que la hace util como
    identificador de procedencia. El primer bloque es el pais y el tercero es
    el numero de serie de la partida.
    """
    if not txt_limpio:
        return []
    out = []
    for m in CODIGO_MARCA.finditer(txt_limpio):
        # una fecha como "28/02/2024" tiene la misma forma: se descarta
        if m.group(1) == "28" and m.group(3) == "02" and m.group(4) == "2024":
            continue
        previo = txt_limpio[max(0, m.start() - 40):m.start()]
        eti = RE_ETIQUETA_COD.findall(previo)
        etiqueta = eti[-1].upper() if eti else None
        codigo = m.group(0).replace(" ", "")
        out.append((etiqueta, codigo, (m.group(1), m.group(3), m.group(4))))
    return out


def clasificar(txt_limpio):
    """Devuelve los atributos declarados en la descripcion del item.

    Cada atributo es SI/NO. Nunca se infiere: si la palabra no esta escrita
    en el documento, el atributo es None (desconocido), no False. Confundir
    "no dice organico" con "dice que no es organico" seria un error grave en
    un atributo que se usa para trazar la certificacion de un producto EUDR.
    """
    if not txt_limpio:
        return {}

    plano = _sin_acentos(txt_limpio).upper()
    out = {}

    for nombre, rx in REGLAS:
        # True si la palabra esta escrita, None si NO aparece. Nunca False:
        # que la descripcion no mencione "organico" no significa que el
        # producto no sea organico, significa que la DUA no lo declara. Un
        # False se leeria como una certificacion negativa que nadie emitio.
        out[nombre] = True if re.search(rx, plano) else None

    # peso declarado en el propio texto de la mercancia
    pesos = [int(m) for m in RE_PESO.findall(txt_limpio)
             if not RE_PESO_CERO.match(m)]
    out["peso_declarado_kg"] = pesos[0] if pesos else None
    # el PDF a veces imprime "00 KG" donde deberia ir el peso: se marca para
    # que el lector no lo tome como peso cero.
    out["peso_texto_incompleto"] = bool(RE_PESO_CERO.search(txt_limpio))

    # identificadores de trazabilidad
    ico = RE_ICO.search(txt_limpio)
    out["ico"] = ("%s/%s/%s" % (ico.group(1), ico.group(2), ico.group(3))
                  if ico else None)
    fda = RE_FDA.search(txt_limpio)
    out["fda"] = fda.group(1) if fda else None
    lote = RE_LOTE.search(plano)
    out["lote"] = lote.group(1).strip() if lote else None
    marca = RE_MARCA.search(plano)
    out["marca_txt"] = marca.group(1).strip(" .-") if marca else None

    # La serie ICO y el numero de marca comparten formato, asi que se
    # clasifican por la etiqueta que las precede en el documento y no por la
    # forma del codigo. La serie ICO es el numero de serie del certificado de
    # origen que emite la Camara Peruana del Cafe y Cacao ante la OIC: se
    # solicita por operacion o lote y NO identifica a un productor. El numero
    # de marca rotula el saco; su bloque central si es estable por exportador.
    codigos = _codigos_marcados(txt_limpio)
    series = [c for eti, c, _ in codigos if eti == "ICO"]
    marcas = [(c, p) for eti, c, p in codigos if eti in ("MARCA", "MARK")]

    out["serie_ico"] = series[0] if series else None
    out["numero_marca"] = marcas[0][0] if marcas else None
    out["clave_origen"] = marcas[0][1][1] if marcas else None
    # el bloque central de la serie ICO tambien es clave de exportador
    if out["clave_origen"] is None and series:
        partes = [p for e, c, p in codigos if e == "ICO"][0]
        out["clave_origen"] = partes[1]
    out["pais_codigo"] = codigos[0][2][0] if codigos else None

    # Codigo con la forma correcta cuya etiqueta quedo cortada por el limite
    # de 100 caracteres de la descripcion ("HUMANO / 30-916-5421 / L ..." con
    # la palabra MARCA fuera del recorte, o "30/11/4773 - LOT ... KGICO:" con
    # el numero de serie despues del corte). Se registra por separado en vez
    # de asignarlo por contexto: sin la etiqueta no se puede distinguir si
    # era serie ICO o numero de marca, y adivinarlo contaminaria el conteo.
    sueltos = [c for eti, c, _p in codigos if eti is None]
    out["codigo_sin_etiqueta"] = sueltos[0] if sueltos else None
    if out["clave_origen"] is None and sueltos:
        partes = [p for e, c, p in codigos if e is None][0]
        out["clave_origen"] = partes[1]

    return out


# --------------------------------------------------------------------------- #
# 4. Indice de busqueda inclusivo
# --------------------------------------------------------------------------- #

def resumen(atributos):
    """Cadena compacta de los atributos SI declarados, para filtrar rapido.

    "organico+arabica+washed" o "" si no hay ninguno.
    """
    if not atributos:
        return ""
    etiquetas = {
        "organico": "organico", "fairtrade": "fairtrade",
        "rainforest": "rainforest", "utz_jbs": "utz", "sustentable_cert": "sustentable",
        "arabica": "arabica", "robusta": "robusta", "criollo": "criollo",
        "trinitario": "trinitario", "forastero": "forastero", "amazonico": "amazonico",
        "washed": "washed", "honey": "honey", "natural": "natural",
        "sun_dried": "sundried", "en_grano": "en_grano", "en_bolsa": "bolsa",
        "a_granel": "granel", "consumo_humano": "consumo_humano",
        "marca": "marca", "lote": "lote", "contrato": "contrato",
    }
    out = [etiquetas[k] for k in etiquetas if atributos.get(k)]
    return "+".join(out)
