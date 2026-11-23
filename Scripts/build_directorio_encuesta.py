"""Agenda-directorio de las organizaciones café-cacao a encuestar.

Cruza por RUC todas las fuentes locales de contacto y arma un Excel con:
  - DIRECTORIO : una fila por organización (contactos, teléfonos, correos,
                 web, calidad del contacto y columnas de seguimiento de campo)
  - PERSONAS   : todas las personas registradas por organización (formato largo)
  - RESUMEN    : cobertura de contacto por región y producto
  - FUENTES    : de dónde sale cada dato

Universo = base MIDAGRI café-cacao limpia (178) ∪ «base 174 detallada» (177).
Uso:  python Scripts/build_directorio_encuesta.py
"""
import json
import re
import unicodedata
from pathlib import Path

import pandas as pd
from openpyxl import Workbook
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "DIRECTORIO_ENCUESTA_ORGANIZACIONES.xlsx"

F_MIDAGRI = ROOT / "data/midagri_cafe_cacao_limpio.csv"
F_PVE = ROOT / "PLANTILLA_INDICE_PVE_ISCAM.xlsx"
F_DIR3 = ROOT / "3 directorio - trabajo en base global cafe cacao 12.10.26.xlsx"
F_RUCFUS = ROOT / "BASE CAFE CACAO 174/CONSULTA MASIVA RUC 10.10.26/CONSULTA_RUC_FUSIONADO.xlsx"
F_MATRIZ = ROOT / "BASE CAFE CACAO 174/MATRIZ_ORGANIZACIONES_174_FINAL.csv"
F_UNIV = ROOT / "data/backup/EUDRPERU_universo_final.csv"
F_CENA = ROOT / "data/backup/CENACOOP_fusion_EUDR.csv"
F_CEN17 = ROOT / "data/backup/soparse_cencoop2017.csv"
F_DIRV3 = ROOT / "Directorio Cooperativas Cafe-Cacao Peru (v3 - Cepicafe-Norandino).xlsx"

NULOS = {"", "nan", "none", "-", "--", "0", "no tiene", "no", "s/n", "sin dato", "nat", "n/a", "na"}


# ----------------------------------------------------------------- helpers
def ruc(v):
    s = re.sub(r"\D", "", str(v).split(".")[0])
    return s if len(s) == 11 else None


def txt(v):
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return ""
    s = re.sub(r"\s+", " ", str(v)).strip()
    return "" if s.lower() in NULOS else s


def nombre(v):
    s = txt(v)
    return s.title() if s and (s.isupper() or s.islower()) else s


def telefonos(v):
    """Devuelve números peruanos normalizados (celular 9 dígitos o fijo con código)."""
    s = txt(v)
    if not s:
        return []
    s = re.sub(r"(?<=\d)\.0\b", "", s)            # 976065194.0
    out = []
    for p in re.split(r"[/,;|]| y | - |\s{2,}", s):
        d = re.sub(r"\D", "", p)
        if d.startswith("51") and len(d) in (11, 10, 9 + 2):
            d = d[2:]
        if len(d) == 9 and d.startswith("9"):
            out.append(f"{d[:3]} {d[3:6]} {d[6:]}")
        elif 6 <= len(d) <= 9 and not d.startswith("9"):
            if len(d) == 8 and not d.startswith("0"):
                d = "0" + d
            if d.startswith("01"):
                out.append(f"(01) {d[2:]}")
            elif d.startswith("0") and len(d) == 9:
                out.append(f"({d[:3]}) {d[3:]}")
            else:
                out.append(d)
    return out


def correos(v):
    return [m.lower() for m in re.findall(r"[\w.+-]+@[\w-]+\.[\w.-]+", txt(v))]


def webs(v):
    s = txt(v)
    if not s:
        return []
    out = []
    for p in re.split(r"[\s,;|]+", s):
        if "." in p and "@" not in p and len(p) > 4:
            out.append(p.rstrip("/"))
    return out


CARGO_NORM = {"Representante (OECE)": "Representante legal", "Presidente (OECE)": "Presidente",
              "Representante (PAC)": "Representante legal", "Representante Legal": "Representante legal",
              "Gerente General": "Gerente general"}


class Org:
    def __init__(self, r):
        self.ruc = r
        self.campos = {}
        self.personas = []           # (nombre, cargo, tel, correo, fuente)
        self.tels = {}               # numero -> set(fuentes)
        self.mails = {}
        self.webs = {}
        self.listas = set()

    def set(self, k, v):
        v = txt(v)
        if v and not self.campos.get(k):
            self.campos[k] = v

    def add_tel(self, v, fuente):
        for t in telefonos(v):
            self.tels.setdefault(t, set()).add(fuente)

    def add_mail(self, v, fuente):
        for m in correos(v):
            self.mails.setdefault(m, set()).add(fuente)

    def add_web(self, v, fuente):
        for w in webs(v):
            self.webs.setdefault(w, set()).add(fuente)

    def add_persona(self, nom, cargo, fuente, tel="", mail=""):
        nom = nombre(nom)
        cargo = CARGO_NORM.get(cargo, cargo)
        if not nom:
            return
        key = re.sub(r"[^a-z]", "", nom.lower())
        for p in self.personas:
            pk = re.sub(r"[^a-z]", "", p["nombre"].lower())
            if pk == key or (set(nom.lower().split()) == set(p["nombre"].lower().split())):
                if cargo and cargo not in p["cargo"]:
                    p["cargo"] = f"{p['cargo']} / {cargo}" if p["cargo"] else cargo
                p["tel"] = p["tel"] or tel
                p["mail"] = p["mail"] or mail
                if fuente not in p["fuente"]:
                    p["fuente"] += f"; {fuente}"
                return
        self.personas.append(dict(nombre=nom, cargo=cargo, tel=tel, mail=mail, fuente=fuente))


ORGS: dict[str, Org] = {}


def org(r, crear=False):
    if r is None:
        return None
    if r not in ORGS:
        if not crear:
            return None
        ORGS[r] = Org(r)
    return ORGS[r]


def leer_csv(path, **kw):
    for enc in ("utf-8-sig", "latin1"):
        try:
            return pd.read_csv(path, encoding=enc, low_memory=False, **kw)
        except UnicodeDecodeError:
            continue


# ------------------------------------------------------------ 1. universo
mid = leer_csv(F_MIDAGRI)
col = lambda df, pref: next(c for c in df.columns if c.startswith(pref))
for _, x in mid.iterrows():
    o = org(ruc(x["RUC_limpio"]), crear=True)
    o.listas.add("MIDAGRI 178")
    o.set("org", x[col(mid, "Organiza")])
    o.set("sunat", x["NOMBRE SUNAT"])
    o.set("producto", x["producto_normalizado"])
    o.set("tipo", x["tipo_org_normalizado"])
    o.set("region", x[col(mid, "Regi")])
    o.set("provincia", x["Provincia"])
    o.set("distrito", x["Distrito"])
    o.set("direccion", x[col(mid, "Direcci")])
    o.set("estado", f"{txt(x['estado_sunat_norm'])} / {txt(x['condicion_sunat_norm'])}".strip(" /"))
    o.set("exporta", x["exporta_flag"])
    sv, sm = pd.to_numeric(x[col(mid, "Número de socios")], errors="coerce"), pd.to_numeric(x["Numero de socias (Mujeres)"], errors="coerce")
    if pd.notna(sv) or pd.notna(sm):
        o.set("socios", int((0 if pd.isna(sv) else sv) + (0 if pd.isna(sm) else sm)))
    f = "MIDAGRI (ficha org.)"
    o.add_persona(x["nombre representante legal"], "Representante legal", f, " · ".join(telefonos(x["celular.2"])))
    o.add_persona(x["nombre Gerente General"], "Gerente general", f, " · ".join(telefonos(x["celular"])), " · ".join(correos(x["Correo"])))
    o.add_persona(x["Representante OECE"], "Representante (OECE)", "MIDAGRI (OECE)")
    o.add_persona(x["Presidente OECE"], "Presidente (OECE)", "MIDAGRI (OECE)")
    o.add_tel(x["celular.2"], f); o.add_tel(x["celular"], f)
    o.add_mail(x["Correo"], f)
    o.add_web(x[col(mid, "Página Web")], f); o.add_web(x["Redes sociales"], f)

det = pd.read_excel(F_PVE, sheet_name="base 174 detallada")
det = det[det["N°"].astype(str).str.isdigit()]
for _, x in det.iterrows():
    o = org(ruc(x["RUC"]), crear=True)
    o.listas.add("Base detallada 177")
    o.set("org", x["Organización"]); o.set("sunat", x["NOMBRE SUNAT"])
    o.set("producto", x["Producto Dom"]); o.set("region", x["Región"])
    o.set("provincia", x["Provincia"]); o.set("distrito", x["Distrito"]); o.set("direccion", x["Dirección"])
    f = "Base detallada"
    o.add_persona(x["nombre representante legal"], "Representante legal", f, " · ".join(telefonos(x["celular.2"])))
    o.add_persona(x["nombre Gerente General"], "Gerente general", f, " · ".join(telefonos(x["celular"])), " · ".join(correos(x["Correo"])))
    o.add_tel(x["celular.2"], f); o.add_tel(x["celular"], f); o.add_mail(x["Correo"], f)
    o.add_web(x["Página Web"], f); o.add_web(x["Redes sociales"], f)

mat = leer_csv(F_MATRIZ)
for _, x in mat.iterrows():
    o = org(ruc(x["RUC"]))
    if not o:
        continue
    o.listas.add("Matriz 174")
    o.set("comercial", x["Nombre público / comercial (web)"])
    o.set("exporta", x["Exporta (interno)"])
    o.add_persona(x["Presidente vigente"], "Presidente", "Matriz 174 (SUNARP/OECE)")
    o.add_persona(x["Gerente general"], "Gerente general", "Matriz 174 (SUNARP/OECE)")
    o.add_web(x["Web / referencia principal"], "Matriz 174 (web)")
    o.set("hallazgo", x["HALLAZGO DETALLADO (fuentes públicas)"])

# ------------------------------------------------------- 2. enriquecimiento
oece = pd.read_excel(F_DIR3, sheet_name="ruc oece personas")
ORDEN_CARGO = {"Presidente": 0, "Gerente": 1, "Representante": 1, "Vice Presidente": 2, "Secretario": 3, "Tesorero": 4, "Fiscal": 5, "Vocal": 6}
for _, x in oece.iterrows():
    o = org(ruc(x["ruc"]))
    if o and txt(x["nombre_persona"]):
        cargo = txt(x["cargo"]) or ("Representante legal" if txt(x["rol"]) == "REPRESENTANTE" else txt(x["rol"]).title())
        if txt(x["rol"]) == "REPRESENTANTE":
            cargo = "Representante legal"
        if cargo != "Otros":
            o.add_persona(x["nombre_persona"], cargo, "OECE (registro de proveedores)")

for path, sh in [(F_RUCFUS, 0), (F_DIR3, "ficha ruc cafe"), (F_DIR3, "ficha ruc cacao")]:
    s = pd.read_excel(path, sheet_name=sh)
    for _, x in s.iterrows():
        o = org(ruc(x["NumeroRuc"]))
        if o:
            o.add_tel(x["Telefono"], "Ficha RUC SUNAT")
            o.set("direccion", x["Direccion"])
            o.set("sunat", x["Nombre ó RazonSocial"])
            o.set("estado", f"{txt(x['Estado del Contribuyente'])} / {txt(x['Condicion del Contribuyente'])}".strip(" /"))

uni = leer_csv(F_UNIV, sep="|")
for _, x in uni.iterrows():
    o = org(ruc(x["ruc"]))
    if not o:
        continue
    o.add_persona(x["rep_pac"], "Representante (PAC)", "Universo EUDR (PAC)", " · ".join(telefonos(x["tel_pac"])), " · ".join(correos(x["correo_pac"])))
    o.add_tel(x["tel_pac"], "Universo EUDR (PAC)"); o.add_mail(x["correo_pac"], "Universo EUDR (PAC)")
    o.add_tel(x["cen_tel_movil"], "CENCOOP 2017"); o.add_tel(x["cen_tel_fijo"], "CENCOOP 2017")
    o.add_mail(x["cen_email"], "CENCOOP 2017"); o.add_web(x["cen_web"], "CENCOOP 2017")
    if pd.notna(pd.to_numeric(x["socios_total"], errors="coerce")):
        o.set("socios", int(float(x["socios_total"])))

cena = leer_csv(F_CENA, sep="|")
for _, x in cena.iterrows():
    o = org(ruc(x["ruc_llave"])) or org(ruc(x["ruc_midagri"]))
    if not o:
        continue
    o.add_persona(x["representante_legal_midagri"], txt(x["cargo_representante_midagri"]).title() or "Representante legal", "Registro coop. MIDAGRI")
    o.add_tel(x["cen2017_TELEFONO_MOVIL"], "CENCOOP 2017"); o.add_tel(x["cen2017_TELEFONO_FIJO"], "CENCOOP 2017")
    o.add_mail(x["cen2017_CORREO"], "CENCOOP 2017"); o.add_web(x["cen2017_PAG_WEB"], "CENCOOP 2017")

c17 = leer_csv(F_CEN17, sep="|")
for _, x in c17.iterrows():
    o = org(ruc(x["NUM_RUC"]))
    if o:
        o.add_tel(x["TELEFONO_MOVIL"], "CENCOOP 2017"); o.add_tel(x["TELEFONO_FIJO"], "CENCOOP 2017")
        o.add_mail(x["CORREO"], "CENCOOP 2017"); o.add_web(x["PAG_WEB"], "CENCOOP 2017")

v3 = pd.read_excel(F_DIRV3, sheet_name="Cooperativas y asociaciones")
for _, x in v3.iterrows():
    o = org(ruc(x["RUC"]))
    if o:
        f = "Directorio v3 (Cepicafe-Norandino)"
        o.add_persona(x["Representante conocido"], txt(x["Cargo / nota"]), f, " · ".join(telefonos(x["Teléfono"])), " · ".join(correos(x["Correo"])))
        o.add_tel(x["Teléfono"], f); o.add_mail(x["Correo"], f)


F_WEB = ROOT / "data/contactos_publicos_web.csv"   # búsqueda en fuentes públicas (no versionado)
if F_WEB.exists():
    web = pd.read_csv(F_WEB, dtype=str, encoding="utf-8").fillna("")
    for _, x in web.iterrows():
        o = org(ruc(x["RUC"]))
        if not o:
            continue
        f = "Web pública"
        o.add_tel(x["telefonos"], f); o.add_tel(x["whatsapp"], f)
        o.add_mail(x["correos"], f)
        o.add_web(x["redes"], f); o.add_web(x["url_fuente"] if "http" in x["url_fuente"] and x["nota"].startswith("Web propia") else "", f)
        for p in [s.strip() for s in x["personas"].split("·") if s.strip()]:
            nom, _, cargo = p.partition(" - ")
            cargo = re.sub(r"\s*\(.*?\)\s*$", "", cargo).strip()
            o.add_persona(nom, cargo, f)
        o.set("web_fuente", f"{x['url_fuente']} ({x['fecha_consulta']})")
        o.set("web_nota", x["nota"])

# ------------------------------------------------------------ 3. ensamblar
def rango_persona(p):
    c = p["cargo"].lower()
    contacto = (2 if p["tel"] else 0) + (1 if p["mail"] else 0)
    if "gerente" in c:
        r = 0
    elif "representante" in c:
        r = 1
    elif "presidente" in c and "vice" not in c:
        r = 2
    elif "vice" in c:
        r = 4
    else:
        r = 5 + min(ORDEN_CARGO.get(p["cargo"], 9), 9)
    return (-contacto, r)


def fuente_peso(fs):  # contactos más recientes primero
    orden = ["Directorio v3", "MIDAGRI", "Base detallada", "Universo EUDR", "Ficha RUC SUNAT", "CENCOOP 2017"]
    return min((i for i, k in enumerate(orden) for f in fs if f.startswith(k)), default=99)


filas, personas = [], []
for o in ORGS.values():
    c = o.campos
    ps = sorted(o.personas, key=rango_persona)
    tels = sorted(o.tels, key=lambda t: (fuente_peso(o.tels[t]), not t.startswith("9")))
    mails = sorted(o.mails, key=lambda m: fuente_peso(o.mails[m]))
    wl = sorted(o.webs, key=lambda w: ("facebook" in w, fuente_peso(o.webs[w])))
    web = [w for w in wl if "facebook" not in w and "instagram" not in w]
    redes = [w for w in wl if w not in web]
    cel = [t for t in tels if t.startswith("9")]
    fijo = [t for t in tels if not t.startswith("9")]
    if tels and mails:
        cal = "A · Teléfono y correo"
    elif cel:
        cal = "B · Solo celular"
    elif mails:
        cal = "C · Solo correo"
    elif fijo:
        cal = "D · Solo teléfono fijo"
    else:
        cal = "E · Sin contacto directo"
    fuentes = sorted({f for d in (o.tels, o.mails) for fs in d.values() for f in fs})
    p1 = ps[0] if ps else {}
    p2 = ps[1] if len(ps) > 1 else {}
    filas.append({
        "RUC": o.ruc,
        "Organización": c.get("org") or c.get("sunat", ""),
        "Razón social (SUNAT)": c.get("sunat", ""),
        "Producto": (c.get("producto", "") or "").upper().replace("CAFE", "CAFÉ"),
        "Tipo": (c.get("tipo", "") or "").title(),
        "Región": "".join(ch for ch in unicodedata.normalize("NFD", (c.get("region", "") or "").upper())
                          if unicodedata.category(ch) != "Mn"),
        "Provincia": (c.get("provincia", "") or "").title(),
        "Distrito": (c.get("distrito", "") or "").title(),
        "Dirección (domicilio fiscal)": c.get("direccion", ""),
        "Contacto principal": p1.get("nombre", ""),
        "Cargo": p1.get("cargo", ""),
        "Contacto alterno": p2.get("nombre", ""),
        "Cargo alterno": p2.get("cargo", ""),
        "Celular(es)": " · ".join(cel),
        "Teléfono fijo": " · ".join(fijo),
        "Correo(s)": " · ".join(mails),
        "WhatsApp (enlace)": f"https://wa.me/51{cel[0].replace(' ', '')}" if cel else "",
        "Página web": " · ".join(web[:2]),
        "Redes sociales": " · ".join(redes[:2]),
        "Calidad del contacto": cal,
        "Estado SUNAT": c.get("estado", ""),
        "Exporta": (c.get("exporta", "") or "").upper().replace("SÍ", "SI"),
        "N.º socios": c.get("socios", ""),
        "Listas de origen": " + ".join(sorted(o.listas)),
        "Fuentes del contacto": "; ".join(fuentes),
        "Fuente web pública (URL, fecha)": c.get("web_fuente", ""),
        "Nota fuente web": c.get("web_nota", ""),
    })
    for p in ps:
        personas.append({"RUC": o.ruc, "Organización": c.get("org") or c.get("sunat", ""), "Nombre": p["nombre"],
                         "Cargo": p["cargo"], "Teléfono": p["tel"], "Correo": p["mail"], "Fuente": p["fuente"]})

df_all = pd.DataFrame(filas)
en176 = (df_all["Listas de origen"].str.contains("MIDAGRI 178")
         & df_all["Listas de origen"].str.contains("Base detallada 177"))
otras = df_all[~en176].copy()
df = df_all[en176].copy()
df["En Matriz 174"] = df["Listas de origen"].str.contains("Matriz 174").map({True: "Sí", False: "No"})
df = df.drop(columns=["Listas de origen"])

# ------------------------------------------------- intermediarios sugeridos
# Contactos institucionales verificados en fuentes públicas el 2026-11-23.
INTERMEDIARIOS = {
    "DEVIDA": ("DEVIDA – Desarrollo Alternativo", "Entidad pública",
               "Mesa de partes virtual: https://sistemas.devida.gob.pe/mesadepartesvirtual/ · Presencial: Av. José Ramírez "
               "Gastón de los Reyes 151, Miraflores (gob.pe también cita Av. Benavides 2199-B; confirmar) · Pedir derivación "
               "a la oficina zonal que corresponda", "https://www.gob.pe/institucion/devida"),
    "AGROIDEAS": ("Agroideas (MIDAGRI)", "Entidad pública",
                  "Aló Midagri – Agroideas: 997 822 487 · Central Midagri (01) 209-8600 opc. 1 · consultas@midagri.gob.pe · "
                  "https://www.gob.pe/agroideas", "https://www.gob.pe/institucion/midagri/pages/9241-acceder-a-los-canales-de-atencion-al-ciudadano-del-midagri"),
    "AGROMERCADO": ("Agromercado (MIDAGRI)", "Entidad pública",
                    "Canales de atención en https://www.gob.pe/institucion/agromercado · Central Midagri (01) 209-8600 opc. 1 · "
                    "consultas@midagri.gob.pe", "https://www.gob.pe/institucion/agromercado"),
    "APPCACAO": ("APPCACAO – Asociación Peruana de Productores de Cacao", "Gremio",
                 "gerencia@appcacao.org · imagen@appcacao.org · +51 1 566 6067 · Jr. Sáenz Peña 525 int. 605, Magdalena del Mar",
                 "Documento de proyecto IICA/APPCACAO (sección de contacto)"),
    "JNC": ("Junta Nacional del Café (JNC)", "Gremio",
            "www.juntadelcafe.org.pe · jnc@juntadelcafe.org.pe · (01) 433 1477 (dato de fecha incierta; confirmar) · "
            "Presidente: Delky Gutiérrez Guerrero (2024-2027)", "https://connectamericas.com/es/node/3671"),
    "NORANDINO": ("Cooperativa Agraria Norandino", "Cooperativa de segundo nivel",
                  "(073) 344983 · coopnorandino@coopnorandino.com.pe · Zona Industrial II Etapa Mz X lotes 3-4, Piura · "
                  "GG Omar Guerrero Alberca (2025) · datos de 2014/2024: confirmar",
                  "https://es.panjiva.com/Cooperativa-Agraria-Norandino-Ltda/25364786"),
    "HELVETAS": ("Helvetas Perú", "Cooperación internacional", "peru@helvetas.org",
                 "https://www.helvetas.org/Publications-PDFs/Latin-America/Peru/cacao%20imaza/brochure%20CACAO%20IMAZA.pdf"),
    "SERNANP": ("SERNANP – Jefatura SN Megantoni", "Entidad pública",
                "Canales de atención de SERNANP en gob.pe; pedir a la jefatura del Santuario Nacional Megantoni", "gob.pe"),
    "SSE": ("Sierra y Selva Exportadora", "Entidad pública",
            "Sede en Lince, Lima; canales en gob.pe (no se verificó teléfono)", "gob.pe"),
    "FIAD_UDEP": ("FIAD / Universidad de Piura – Proyectos sociales", "ONG / Universidad",
                  "https://www.udep.edu.pe/proyectos-sociales/ (proyecto de café en Lalaquiz)",
                  "https://www.udep.edu.pe/hoy/2023/04/mas-de-100-familias-de-lalaquiz-mejoran-la-calidad-de-sus-cultivos-de-cafe/"),
}
# Vínculo documentado en fuentes públicas (ver data/contactos_publicos_web.csv y notas de búsqueda)
VINCULO_DOC = {
    "20146696041": ("NORANDINO", "Es base de Norandino y exporta por ella"),
    "20610739491": ("AGROIDEAS", "Plan de negocio Agroideas aprobado (jul-2026)"),
    "20542251990": ("DEVIDA", "Planta chocolatera Devida 2019"),
    "20393882868": ("DEVIDA", "Planta chocolatera Devida / GORE Ucayali"),
    "20600029887": ("DEVIDA", "Proyecto BID PE-T1532 y Devida (Ramón Castilla)"),
    "20564032485": ("SERNANP", "Acuerdo de conservación con SERNANP (SN Megantoni)"),
    "20568560133": ("SSE", "Asistencia de Sierra Exportadora para certificación orgánica"),
    "20607382604": ("FIAD_UDEP", "Proyecto de café FIAD-UDEP en Lalaquiz"),
    "20608478311": ("HELVETAS", "Proyecto cacao Imaza-Nieva de Helvetas"),
    "20568428375": ("DEVIDA", "Rueda de negocios con asistencia de Devida"),
    "20602047025": ("DEVIDA", "Planta procesadora (convenio Agroideas-Devida)"),
    "20542289024": ("AGROMERCADO", "Asistencia técnica de Agromercado desde 2024"),
    "20611935243": ("AGROMERCADO", "Exportación con apoyo de Agromercado (2025)"),
    "20600010086": ("AGROIDEAS", "Plan de negocio Agroideas (Bolsón Cuchara)"),
    "20393786044": ("DEVIDA", "Capacitación de caficultores por Devida"),
}
# Distritos en zonas de desarrollo alternativo atendidas por DEVIDA
DEVIDA_DIST = {"pichari", "kimbiri", "llochegua", "pangoa", "rio tambo", "mazamari", "satipo", "rupa-rupa",
               "jose crespo y castillo", "marias", "nuevo progreso", "tocache", "juanjui", "picota", "padre abad",
               "irazola", "curimana", "neshuya", "alexander von humboldt", "boqueron", "puerto bermudez", "palcazu",
               "echarate", "quellouno", "teniente cesar lopez rojas", "yurimaguas"}


def _sin_tilde(s):
    return "".join(ch for ch in unicodedata.normalize("NFD", str(s).lower()) if unicodedata.category(ch) != "Mn").strip()


def intermediarios(r):
    dist = _sin_tilde(r["Distrito"])
    muni = f"Municipalidad de {r['Distrito']}" if r["Distrito"] else ""
    if r["RUC"] in VINCULO_DOC:
        k, motivo = VINCULO_DOC[r["RUC"]]
        alt = "DEVIDA" if dist in DEVIDA_DIST and k != "DEVIDA" else muni
        base = f"Vínculo documentado: {motivo}"
    elif dist in DEVIDA_DIST:
        k, alt, base = "DEVIDA", muni, "Por ámbito: zona de desarrollo alternativo"
    elif r["Producto"] == "CACAO":
        k, alt, base = "APPCACAO", muni, "Por producto: gremio nacional de cacao"
    elif r["Región"] in ("PIURA", "LAMBAYEQUE"):
        k, alt, base = "NORANDINO", muni, "Por ámbito: Norandino opera en la zona (verificar si es base)"
    else:
        k, alt, base = "JNC", muni, "Por producto: federación nacional del café"
    if not r["Estado SUNAT"].startswith("ACTIVO"):
        base += " · RUC no activo en SUNAT: confirmar si sigue operando"
    nom = lambda x: INTERMEDIARIOS[x][0] if x in INTERMEDIARIOS else x
    return pd.Series({"Intermediario sugerido": nom(k), "Intermediario alterno": nom(alt), "Base del vínculo": base,
                      "_k": k})


df = pd.concat([df, df.apply(intermediarios, axis=1)], axis=1)
df = df.sort_values(["Región", "Provincia", "Organización"]).reset_index(drop=True)
df.insert(0, "N.º", range(1, len(df) + 1))
k_inter = df.pop("_k")
pp = pd.DataFrame(personas)
pp = pp[pp["RUC"].isin(df["RUC"])].sort_values(["Organización", "RUC"])
SEGUIMIENTO = ["Estado de la gestión", "N.º intentos", "Fecha último contacto", "Fecha encuesta agendada",
               "Modalidad", "Encuestador", "Persona que responde", "Observaciones"]
for s in SEGUIMIENTO:
    df[s] = ""

# ------------------------------------------------------------ 4. Excel
VERDE, AZUL_OSC = "1F5130", "17375E"
thin = Side(style="thin", color="D0D7DE")
borde = Border(left=thin, right=thin, top=thin, bottom=thin)
hdr_font = Font(bold=True, color="FFFFFF", name="Calibri", size=10)
cuerpo = Font(name="Calibri", size=10)

wb = Workbook()
ws = wb.active
ws.title = "DIRECTORIO"
ws["A1"] = "Agenda-directorio de organizaciones café-cacao a encuestar"
ws["A1"].font = Font(bold=True, size=14, color=VERDE)
ws["A2"] = (f"{len(df)} organizaciones · presentes a la vez en la base MIDAGRI café-cacao (178) y en la base detallada (177) · "
            "contactos cruzados por RUC desde 7 fuentes locales (ver hoja FUENTES) · generado 23/11/2026")
ws["A2"].font = Font(italic=True, size=9, color="555555")
cols = list(df.columns)
n_datos = len(cols) - len(SEGUIMIENTO)
HR = 4
for j, h in enumerate(cols, 1):
    cell = ws.cell(row=HR, column=j, value=h)
    cell.font = hdr_font
    cell.fill = PatternFill("solid", fgColor=VERDE if j <= n_datos else AZUL_OSC)
    cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    cell.border = borde
ws.cell(row=HR - 1, column=n_datos + 1, value="SEGUIMIENTO DE CAMPO (llenar)").font = Font(bold=True, color=AZUL_OSC)
for i, row in enumerate(df.itertuples(index=False), HR + 1):
    for j, v in enumerate(row, 1):
        cell = ws.cell(row=i, column=j, value=v if v != "" else None)
        cell.font = cuerpo
        cell.border = borde
        cell.alignment = Alignment(vertical="top", wrap_text=cols[j - 1] in (
            "Organización", "Dirección (domicilio fiscal)", "Correo(s)", "Observaciones", "Cargo", "Cargo alterno",
            "Fuentes del contacto", "Razón social (SUNAT)", "Página web", "Redes sociales", "Celular(es)"))
        if cols[j - 1] == "WhatsApp (enlace)" and v:
            cell.hyperlink = v
            cell.value = "Abrir chat"
            cell.font = Font(name="Calibri", size=10, color="0563C1", underline="single")
        if cols[j - 1] == "RUC":
            cell.number_format = "@"

anchos = {"N.º": 5, "RUC": 13, "Organización": 38, "Razón social (SUNAT)": 34, "Producto": 8, "Tipo": 12,
          "Región": 13, "Provincia": 14, "Distrito": 15, "Dirección (domicilio fiscal)": 34,
          "Contacto principal": 26, "Cargo": 18, "Contacto alterno": 24, "Cargo alterno": 16,
          "Celular(es)": 15, "Teléfono fijo": 13, "Correo(s)": 30, "WhatsApp (enlace)": 11,
          "Página web": 24, "Redes sociales": 24, "Calidad del contacto": 22, "Estado SUNAT": 16,
          "Exporta": 8, "N.º socios": 8, "En Matriz 174": 9, "Fuentes del contacto": 30,
          "Fuente web pública (URL, fecha)": 34, "Nota fuente web": 34,
          "Intermediario sugerido": 28, "Intermediario alterno": 28, "Base del vínculo": 40,
          "Estado de la gestión": 18, "N.º intentos": 8, "Fecha último contacto": 12,
          "Fecha encuesta agendada": 12, "Modalidad": 13, "Encuestador": 16,
          "Persona que responde": 22, "Observaciones": 36}
for j, h in enumerate(cols, 1):
    ws.column_dimensions[get_column_letter(j)].width = anchos.get(h, 14)
ws.row_dimensions[HR].height = 42
ws.freeze_panes = ws.cell(row=HR + 1, column=4)
last = HR + len(df)
ws.auto_filter.ref = f"A{HR}:{get_column_letter(len(cols))}{last}"

L = {h: get_column_letter(j) for j, h in enumerate(cols, 1)}
dv_estado = DataValidation(type="list", formula1='"Pendiente,Contactado - sin respuesta,Número errado,Agendado,Encuestado,Rechazó,Reprogramar,No ubicable"', allow_blank=True)
dv_mod = DataValidation(type="list", formula1='"Presencial,Telefónica,Videollamada,Formulario en línea,WhatsApp"', allow_blank=True)
dv_fecha = DataValidation(type="date", operator="greaterThan", formula1="46000", allow_blank=True)
dv_int = DataValidation(type="whole", operator="between", formula1="0", formula2="20", allow_blank=True)
for dv, c in [(dv_estado, "Estado de la gestión"), (dv_mod, "Modalidad"), (dv_int, "N.º intentos")]:
    ws.add_data_validation(dv); dv.add(f"{L[c]}{HR+1}:{L[c]}{last}")
ws.add_data_validation(dv_fecha)
for c in ("Fecha último contacto", "Fecha encuesta agendada"):
    dv_fecha.add(f"{L[c]}{HR+1}:{L[c]}{last}")
    for r in range(HR + 1, last + 1):
        ws[f"{L[c]}{r}"].number_format = "dd/mm/yyyy"

# semáforos
rng_cal = f"{L['Calidad del contacto']}{HR+1}:{L['Calidad del contacto']}{last}"
for letra, color in [("A", "C6EFCE"), ("B", "E2F0D9"), ("C", "FFF2CC"), ("D", "FCE4D6"), ("E", "F8CBAD")]:
    ws.conditional_formatting.add(rng_cal, FormulaRule(formula=[f'LEFT({L["Calidad del contacto"]}{HR+1},1)="{letra}"'], fill=PatternFill("solid", fgColor=color)))
rng_est = f"A{HR+1}:{get_column_letter(len(cols))}{last}"
E = L["Estado de la gestión"]
for val, color in [("Encuestado", "D9EAD3"), ("Agendado", "DDEBF7"), ("Rechazó", "EDEDED"), ("No ubicable", "EDEDED")]:
    ws.conditional_formatting.add(rng_est, FormulaRule(formula=[f'${E}{HR+1}="{val}"'], fill=PatternFill("solid", fgColor=color)))

# PERSONAS
wp = wb.create_sheet("PERSONAS")
wp.append(list(pp.columns))
for r in pp.itertuples(index=False):
    wp.append(list(r))
for j, w in enumerate([13, 40, 30, 28, 16, 30, 40], 1):
    wp.column_dimensions[get_column_letter(j)].width = w
for cell in wp[1]:
    cell.font = hdr_font; cell.fill = PatternFill("solid", fgColor=VERDE); cell.alignment = Alignment(wrap_text=True)
wp.freeze_panes = "C2"
wp.auto_filter.ref = wp.dimensions

# INTERMEDIARIOS: a quién pedir los contactos de las organizaciones sin contacto (calidad E)
wi = wb.create_sheet("INTERMEDIARIOS", 1)
wi["A1"] = "Intermediarios para ubicar a las organizaciones sin teléfono ni correo"
wi["A1"].font = Font(bold=True, size=13, color=VERDE)
wi["A2"] = ("Un pedido por institución: enviar la lista de la columna F y solicitar contacto de gerente/presidente. "
            "Contactos institucionales verificados en fuentes públicas el 23/11/2026. Las municipalidades se ubican en gob.pe › "
            "«Municipalidad (distrital o provincial) de …» › Canales de atención.")
wi["A2"].font = Font(italic=True, size=9, color="555555")
hdr_i = ["Intermediario", "Tipo", "Contacto institucional", "Fuente del contacto", "N.º orgs sin contacto",
         "Organizaciones a solicitar (RUC – nombre – distrito)", "Estado del pedido", "Fecha de envío", "Respuesta / observaciones"]
for j, h in enumerate(hdr_i, 1):
    c = wi.cell(row=4, column=j, value=h)
    c.font = hdr_font; c.border = borde
    c.fill = PatternFill("solid", fgColor=VERDE if j <= 6 else AZUL_OSC)
    c.alignment = Alignment(wrap_text=True, vertical="center")
sinc = df["Calidad del contacto"].str.startswith("E")
grupos = df[sinc].assign(_k=k_inter[sinc]).groupby("_k")
fila = 5
for k, g in sorted(grupos, key=lambda kv: -len(kv[1])):
    nombre_i, tipo, contacto, fuente = INTERMEDIARIOS[k]
    lista = "\n".join(f"{r.RUC} – {r.Organización} – {r.Distrito}" for r in g.itertuples(index=False))
    for j, v in enumerate([nombre_i, tipo, contacto, fuente, len(g), lista], 1):
        c = wi.cell(row=fila, column=j, value=v)
        c.font = cuerpo; c.border = borde; c.alignment = Alignment(wrap_text=True, vertical="top")
    for j in range(7, 10):
        wi.cell(row=fila, column=j).border = borde
    fila += 1
# municipalidades como alterno general
munis = df[sinc]["Intermediario alterno"].loc[lambda s: s.str.startswith("Municipalidad")].value_counts()
wi.cell(row=fila + 1, column=1, value="Municipalidades (intermediario alterno)").font = Font(bold=True)
for i, (m, n) in enumerate(munis.items(), fila + 2):
    wi.cell(row=i, column=1, value=m).font = cuerpo
    wi.cell(row=i, column=5, value=int(n)).font = cuerpo
dv_ped = DataValidation(type="list", formula1='"Pendiente,Enviado,Respondió,Sin respuesta"', allow_blank=True)
wi.add_data_validation(dv_ped); dv_ped.add(f"G5:G{fila - 1}")
for c, w in zip("ABCDEFGHI", (30, 18, 48, 30, 10, 62, 14, 12, 34)):
    wi.column_dimensions[c].width = w
wi.freeze_panes = "B5"

# CORREOS: textos listos por intermediario (completar los [corchetes] antes de enviar)
FIRMA = ("Atentamente,\n[Nombre completo]\n[Cargo] – [Institución / proyecto]\n[Teléfono / WhatsApp] · [Correo]")
CONDICIONES = (
    "Algunos detalles del estudio:\n"
    "• La participación es voluntaria y la encuesta toma unos [XX] minutos (por teléfono, videollamada o formulario en línea).\n"
    "• Los datos de contacto se usarán solo para coordinar la encuesta, conforme a la Ley N.° 29733 de Protección de Datos "
    "Personales. Los resultados se presentarán de forma agregada, sin identificar a personas.\n"
    "• Con gusto compartiremos los resultados generales del estudio.\n\n"
    "Si alguna de estas organizaciones ya no está activa o cambió de nombre, también nos sería muy útil saberlo.")
INTRO = ("Le saluda [nombre], [cargo] de [institución / proyecto]. Estamos realizando un estudio sobre la preparación de las "
         "organizaciones de productores de café y cacao del Perú frente al Reglamento de la Unión Europea sobre productos libres "
         "de deforestación (EUDR). Como parte del estudio, aplicaremos una encuesta a organizaciones de la base de MIDAGRI.")


def lista_orgs(g, por_region=False):
    fmt = lambda r: f"• {r.Organización} (RUC {r.RUC}) – {r.Distrito}, {r.Región.title()}"
    if not por_region:
        return "\n".join(fmt(r) for r in g.itertuples(index=False))
    bloques = []
    for reg, gg in g.groupby("Región"):
        bloques.append(f"{reg.title()}:\n" + "\n".join(fmt(r) for r in gg.itertuples(index=False)))
    return "\n\n".join(bloques)


def correo(k, g):
    nombre_i, tipo, contacto, _ = INTERMEDIARIOS[k]
    n = len(g)
    orgs_txt = "organización" if n == 1 else "organizaciones"
    para = " · ".join(sorted(set(re.findall(r"[\w.+-]+@[\w-]+\.[\w.-]+", contacto)))) or contacto
    if tipo == "Entidad pública":
        if k == "DEVIDA":
            para = "Mesa de partes virtual: https://sistemas.devida.gob.pe/mesadepartesvirtual/"
        asunto = "Solicitud de información de contacto de organizaciones de productores de café y cacao, con fines de investigación"
        cuerpo = (f"Señores\n{nombre_i}\nPresente.-\n\n"
                  "Por medio del presente, en mi calidad de [cargo] de [institución / proyecto], me dirijo a ustedes para "
                  "saludarles. " + INTRO[INTRO.index("Estamos"):] + "\n\n"
                  f"No contamos con datos de contacto actualizados de {n} {orgs_txt} que, según información pública, "
                  f"{'es' if n == 1 else 'son'} o {'ha' if n == 1 else 'han'} sido {'atendida' if n == 1 else 'atendidas'} por su institución. Solicitamos su apoyo, a través de la oficina zonal o dirección "
                  "que corresponda, para obtener un teléfono o correo de su gerente o presidente, o para hacerles llegar esta "
                  "comunicación y que puedan escribirnos directamente.\n\n"
                  f"Organizaciones:\n{lista_orgs(g, por_region=(k == 'DEVIDA'))}\n\n{CONDICIONES}\n\n"
                  "Agradecemos de antemano su atención y quedamos atentos a su respuesta.\n\n" + FIRMA)
    else:
        asunto = f"Solicitud de apoyo para contactar a {n} {orgs_txt} de café y cacao (estudio EUDR)"
        extra = ""
        if k == "NORANDINO":
            extra = ("\n\nSegún información pública, algunas de estas organizaciones serían bases de Norandino o se ubican en su "
                     "zona de acopio. Si alguna no lo es, le agradeceremos indicárnoslo.")
        uno = n == 1
        cuerpo = (f"Estimado equipo de {nombre_i}:\n\n{INTRO}\n\n"
                  f"No contamos con datos de contacto actualizados de {'una organización que' if uno else 'un grupo de organizaciones que'}, "
                  f"según información pública, {'trabaja' if uno else 'trabajan'} con ustedes o se {'ubica' if uno else 'ubican'} "
                  "en su ámbito. Le agradeceríamos mucho que nos facilite un teléfono o correo de su gerente o presidente, o bien "
                  f"que le{'' if uno else 's'} reenvíe este mensaje para que nos escriba{'' if uno else 'n'} directamente."
                  f"{extra}\n\n{'Organización' if uno else 'Organizaciones'}:\n{lista_orgs(g)}\n\n{CONDICIONES}\n\n"
                  "Muchas gracias de antemano por su apoyo.\n\n" + FIRMA)
    return nombre_i, para, asunto, cuerpo, n


def correo_muni(muni, g):
    asunto = "Solicitud de contacto de organizaciones de productores de café y cacao del distrito (estudio EUDR)"
    cuerpo = (f"Estimados señores de la {muni}:\n\n{INTRO}\n\n"
              "Nos dirigimos a ustedes para solicitar, de ser posible, el contacto de las siguientes asociaciones y cooperativas "
              f"de productores de su jurisdicción:\n\n{lista_orgs(g)}\n\n"
              "Agradeceremos que nos indiquen la oficina o persona encargada del padrón de organizaciones agrarias "
              "(Gerencia de Desarrollo Económico o Agencia Agraria), o que les hagan llegar este mensaje.\n\n"
              f"{CONDICIONES}\n\nMuchas gracias por su apoyo.\n\n" + FIRMA)
    return muni, "Canales de atención en gob.pe («Municipalidad de …»)", asunto, cuerpo, len(g)


wc = wb.create_sheet("CORREOS", 2)
wc["A1"] = "Correos y oficios listos por intermediario"
wc["A1"].font = Font(bold=True, size=13, color=VERDE)
wc["A2"] = ("Completar los [corchetes] (nombre, cargo, institución, duración de la encuesta) antes de enviar. A entidades públicas: "
            "enviar como oficio por mesa de partes. Municipalidades: usar si el intermediario sugerido no responde en 7-10 días.")
wc["A2"].font = Font(italic=True, size=9, color="555555")
hdr_c = ["#", "Intermediario", "Para / canal de envío", "Asunto", "Cuerpo del mensaje", "N.º orgs", "Estado", "Fecha de envío"]
for j, h in enumerate(hdr_c, 1):
    c = wc.cell(row=4, column=j, value=h)
    c.font = hdr_font; c.border = borde
    c.fill = PatternFill("solid", fgColor=VERDE if j <= 6 else AZUL_OSC)
    c.alignment = Alignment(wrap_text=True, vertical="center")
filas_c = [correo(k, g) for k, g in sorted(grupos, key=lambda kv: -len(kv[1]))]
e_df = df[sinc]
filas_c += [correo_muni(m, e_df[e_df["Intermediario alterno"] == m])
            for m in munis.index]
# Datos del remitente (archivo local, no versionado): rellena los [corchetes]
F_REM = ROOT / "data/remitente_encuesta.json"
if F_REM.exists():
    rem = json.loads(F_REM.read_text(encoding="utf-8"))
    sust = {
        "de [institución / proyecto]": "de " + rem.get("institucion_con_articulo", rem["institucion"]),
        "[nombre]": rem["nombre"], "[Nombre completo]": rem["nombre"],
        "[cargo]": rem["cargo"], "[Cargo]": rem["cargo"][:1].upper() + rem["cargo"][1:],
        "[institución / proyecto]": rem["institucion"], "[Institución / proyecto]": rem["institucion"],
        "[Teléfono / WhatsApp]": rem["telefono"], "[Correo]": rem["correo"],
        "unos [XX] minutos": f"aproximadamente {rem['duracion']} minutos",
    }

    def rellenar(t):
        for a, b in sust.items():
            t = t.replace(a, b)
        return t

    filas_c = [(a, b, c, rellenar(d), n) for a, b, c, d, n in filas_c]
    wc["A2"] = ("Textos con los datos del remitente (data/remitente_encuesta.json). A entidades públicas: enviar como oficio "
                "por mesa de partes. Municipalidades: usar si el intermediario sugerido no responde en 7-10 días.")
for i, (nom_i, para, asunto, cuerpo_txt, n) in enumerate(filas_c, 1):
    r = 4 + i
    for j, v in enumerate([i, nom_i, para, asunto, cuerpo_txt, n], 1):
        c = wc.cell(row=r, column=j, value=v)
        c.font = cuerpo; c.border = borde; c.alignment = Alignment(wrap_text=True, vertical="top")
    for j in (7, 8):
        wc.cell(row=r, column=j).border = borde
    wc.row_dimensions[r].height = min(409, 15 * (cuerpo_txt.count("\n") + 2 + len(cuerpo_txt) // 110))
dv_c = DataValidation(type="list", formula1='"Pendiente,Enviado,Respondió,Sin respuesta"', allow_blank=True)
wc.add_data_validation(dv_c); dv_c.add(f"G5:G{4 + len(filas_c)}")
for c, w in zip("ABCDEFGH", (4, 26, 30, 34, 110, 8, 13, 12)):
    wc.column_dimensions[c].width = w
wc.freeze_panes = "C5"

# GUION: speech para la llamada / WhatsApp a cada organización
_r = json.loads(F_REM.read_text(encoding="utf-8")) if F_REM.exists() else {}
NOM = _r.get("nombre", "[nombre]")
CARGO = _r.get("cargo", "[cargo]")
INST = _r.get("institucion", "[institución]")
INST_ART = _r.get("institucion_con_articulo", INST)
DUR = _r.get("duracion", "[XX]")
GUION = [
    ("h", "1. Apertura (primeros 20 segundos)"),
    ("p", f"«Buenos días/tardes, ¿hablo con la [Cooperativa/Asociación ___]?\nMi nombre es {NOM}, soy {CARGO} de {INST_ART}.\n"
          "Le llamo por un estudio sobre cómo se están preparando las organizaciones de café y cacao para la nueva norma europea "
          "de deforestación, la EUDR.\n¿Podría comunicarme con el gerente o el presidente?»"),
    ("n", "Si llegaste por un intermediario, agrega tras presentarte: «Su contacto nos lo facilitó [DEVIDA / APPCACAO / la "
          "Municipalidad de ___ / Norandino]»."),
    ("n", "Si el gerente no está: «¿En qué horario lo puedo encontrar? ¿O me podría dar un número o WhatsApp donde escribirle?» "
          "Anota el nombre de quien atendió."),
    ("h", "2. Con el gerente o presidente (1-2 minutos)"),
    ("p", "«Gracias por atenderme, señor/a ___. Le explico rápido: estamos haciendo un diagnóstico de qué tan preparadas están "
          "las cooperativas y asociaciones de café y cacao para cumplir la EUDR, que exigirá a quienes vendan a Europa demostrar "
          "que su producto no viene de zonas deforestadas: georreferenciación de parcelas, trazabilidad, documentación.\n"
          "Su organización está en la base de MIDAGRI y nos interesa mucho conocer su experiencia: qué tienen avanzado y dónde "
          f"ven dificultades.\nLa encuesta toma aproximadamente {DUR} minutos y la podemos hacer cuando a usted le acomode: por "
          "teléfono, por videollamada o con un formulario en línea.»"),
    ("p", "«La participación es voluntaria y la información es confidencial; los resultados se presentan agregados, sin mencionar "
          "a ninguna organización en particular. Al terminar el estudio les compartiremos los resultados generales, que les pueden "
          "servir para compararse con otras organizaciones del sector.»"),
    ("p", "Cierre (pide fecha, no un «sí» abstracto): «¿Qué día de esta semana o la próxima le quedaría mejor? ¿Mañana o tarde?»"),
    ("h", "3. Si pone reparos"),
    ("t", [("Si te dice…", "Responde"),
           ("«No tengo tiempo, es mucho.»", "«Lo entiendo. Podemos dividirla en dos partes de media hora, o le envío el formulario "
            "para que lo llene a su ritmo. ¿Qué le resulta más cómodo?»"),
           ("«¿Para qué es? ¿Quién lo financia?»", f"«Es un estudio académico de {INST_ART}. No vendemos nada ni tiene costo. "
            "Si gusta, le envío por correo una carta de presentación.»"),
           ("«No exportamos a Europa / no nos afecta.»", "«Nos interesa incluir a organizaciones en todas las situaciones, también "
            "a las que venden en el mercado nacional o a intermediarios, porque la norma afecta a toda la cadena.»"),
           ("«No sabemos nada de la EUDR.»", "«No se preocupe, no es un examen. Esa información también es valiosa para el "
            "estudio; las preguntas son sobre cómo trabajan hoy.»"),
           ("«¿Qué harán con mis datos?»", "«Se usan solo para el estudio, conforme a la Ley de Protección de Datos Personales. "
            "No compartimos información individual de su organización con nadie.»"),
           ("«Hable con el presidente / el técnico.»", "«Perfecto, ¿me da su nombre y un número para contactarlo? ¿Puedo decirle "
            "que usted me recomendó?»"),
           ("«Mándeme información por escrito.»", "«Claro, ¿a qué correo o WhatsApp se la envío? Le escribo hoy y lo vuelvo a "
            "llamar el [día] para coordinar.»")]),
    ("h", "4. Confirmación (antes de colgar)"),
    ("p", "«Entonces quedamos el [día] a las [hora], por [teléfono / videollamada / formulario]. ¿Este es el mejor número para "
          "comunicarme con usted? ¿Tiene un correo donde le envíe la confirmación? Un día antes le escribo por WhatsApp para "
          "recordárselo. ¡Muchas gracias, señor/a ___!»"),
    ("h", "5. Mensajes de WhatsApp"),
    ("p", f"Primer contacto:\n«Buenos días, señor/a ___. Le saluda {NOM}, {CARGO} de {INST_ART}. Estamos haciendo un estudio "
          "sobre la preparación de las organizaciones de café y cacao frente a la norma europea de deforestación (EUDR) y nos "
          f"gustaría contar con la participación de [organización]. La encuesta toma aprox. {DUR} minutos y puede ser por teléfono, "
          "videollamada o formulario, en el horario que usted prefiera. ¿Podríamos coordinar una fecha? Muchas gracias.»"),
    ("p", f"Recordatorio (un día antes):\n«Buenos días, señor/a ___. Le recuerdo nuestra cita de mañana [día] a las [hora] para "
          f"la encuesta de {INST_ART} sobre la EUDR. Si necesita cambiar el horario, me avisa por aquí sin problema. ¡Gracias!»"),
    ("n", "Si no contesta en 3 intentos: pasar al intermediario alterno (hojas DIRECTORIO e INTERMEDIARIOS)."),
    ("h", "6. Qué anotar en DIRECTORIO tras cada intento"),
    ("p", "• Estado de la gestión (Contactado – sin respuesta / Agendado / Rechazó / Número errado…)\n"
          "• N.º intentos y Fecha último contacto\n• Fecha encuesta agendada y Modalidad\n"
          "• Persona que responde (nombre y cargo)\n"
          "• Observaciones: mejor horario, quién atendió, si pidió carta de presentación, si la org. está inactiva o cambió de nombre"),
    ("h", "Tips"),
    ("p", "• Llamar entre 8:00 y 11:00 a. m.: por la tarde muchos gerentes están en campo o en acopio.\n"
          "• En cosecha (café ~abril-agosto según zona) cuesta más: proponer fechas posteriores en vez de insistir.\n"
          "• Tener a la mano la ficha de la organización (región, producto, si exporta): un dato concreto genera confianza."),
]
wg = wb.create_sheet("GUION", 3)
wg["A1"] = "Guion de contacto con las organizaciones"
wg["A1"].font = Font(bold=True, size=14, color=VERDE)
wg["A2"] = f"{NOM} · {CARGO} · {INST} · encuesta ≈ {DUR} min. Los [corchetes] se ajustan en cada llamada."
wg["A2"].font = Font(italic=True, size=9, color="555555")
wg.column_dimensions["A"].width = 34
wg.column_dimensions["B"].width = 96
fila_g = 4
for tipo, contenido in GUION:
    if tipo == "h":
        fila_g += 1
        c = wg.cell(row=fila_g, column=1, value=contenido)
        c.font = hdr_font; c.fill = PatternFill("solid", fgColor=VERDE)
        wg.merge_cells(start_row=fila_g, start_column=1, end_row=fila_g, end_column=2)
        fila_g += 1
    elif tipo == "t":
        for i, (a, b) in enumerate(contenido):
            for j, v in enumerate((a, b), 1):
                c = wg.cell(row=fila_g, column=j, value=v)
                c.border = borde; c.alignment = Alignment(wrap_text=True, vertical="top")
                c.font = hdr_font if i == 0 else cuerpo
                if i == 0:
                    c.fill = PatternFill("solid", fgColor=AZUL_OSC)
            wg.row_dimensions[fila_g].height = 15 if i == 0 else 15 * (1 + len(b) // 95)
            fila_g += 1
    else:
        c = wg.cell(row=fila_g, column=1, value=contenido)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        c.font = Font(name="Calibri", size=10, italic=(tipo == "n"), color="555555" if tipo == "n" else "000000")
        wg.merge_cells(start_row=fila_g, start_column=1, end_row=fila_g, end_column=2)
        wg.row_dimensions[fila_g].height = 15 * (contenido.count("\n") + 1 + len(contenido) // 125)
        fila_g += 1
wg.sheet_view.showGridLines = False

# RESUMEN (con fórmulas vivas sobre DIRECTORIO)
wr = wb.create_sheet("RESUMEN")
wr["A1"] = "Cobertura de contacto"; wr["A1"].font = Font(bold=True, size=13, color=VERDE)
D = "DIRECTORIO!"
rng = lambda c: f"{D}${L[c]}${HR+1}:${L[c]}${last}"
wr.append([])
wr.append(["Indicador", "N.º", "%"])
ind = [
    ("Organizaciones", f"=COUNTA({rng('RUC')})"),
    ("Con celular", f'=COUNTIF({rng("Celular(es)")},"?*")'),
    ("Con correo", f'=COUNTIF({rng("Correo(s)")},"?*")'),
    ("Con nombre de contacto", f'=COUNTIF({rng("Contacto principal")},"?*")'),
    ("Sin contacto directo (E)", f'=COUNTIF({rng("Calidad del contacto")},"E*")'),
    ("Encuestadas", f'=COUNTIF({rng("Estado de la gestión")},"Encuestado")'),
    ("Agendadas", f'=COUNTIF({rng("Estado de la gestión")},"Agendado")'),
    ("Rechazos", f'=COUNTIF({rng("Estado de la gestión")},"Rechazó")'),
]
for i, (k, f) in enumerate(ind, 4):
    wr.append([k, f, None if i == 4 else f"=IFERROR(B{i}/$B$4,0)"])
    wr[f"C{i}"].number_format = "0%"
r0 = 4 + len(ind) + 2
wr.cell(row=r0, column=1, value="Calidad del contacto").font = Font(bold=True)
for i, cat in enumerate(["A · Teléfono y correo", "B · Solo celular", "C · Solo correo", "D · Solo teléfono fijo", "E · Sin contacto directo"], r0 + 1):
    wr.cell(row=i, column=1, value=cat)
    wr.cell(row=i, column=2, value=f'=COUNTIF({rng("Calidad del contacto")},A{i})')
    wr.cell(row=i, column=3, value=f"=IFERROR(B{i}/$B$4,0)").number_format = "0%"
r1 = r0 + 8
wr.cell(row=r1, column=1, value="Por región").font = Font(bold=True)
for j, h in enumerate(["Región", "Orgs", "Con celular", "Con correo", "Sin contacto", "Encuestadas"], 1):
    c = wr.cell(row=r1 + 1, column=j, value=h); c.font = hdr_font; c.fill = PatternFill("solid", fgColor=VERDE)
for i, reg in enumerate(sorted(df["Región"].replace("", "(sin región)").unique()), r1 + 2):
    wr.cell(row=i, column=1, value=reg)
    crit = f"A{i}"
    wr.cell(row=i, column=2, value=f"=COUNTIF({rng('Región')},{crit})")
    wr.cell(row=i, column=3, value=f'=COUNTIFS({rng("Región")},{crit},{rng("Celular(es)")},"?*")')
    wr.cell(row=i, column=4, value=f'=COUNTIFS({rng("Región")},{crit},{rng("Correo(s)")},"?*")')
    wr.cell(row=i, column=5, value=f'=COUNTIFS({rng("Región")},{crit},{rng("Calidad del contacto")},"E*")')
    wr.cell(row=i, column=6, value=f'=COUNTIFS({rng("Región")},{crit},{rng("Estado de la gestión")},"Encuestado")')
for c in "ABCDEF":
    wr.column_dimensions[c].width = 26 if c == "A" else 13
for cell in wr[3]:
    cell.font = hdr_font; cell.fill = PatternFill("solid", fgColor=VERDE)

# FUERA DE LAS 176
wo = wb.create_sheet("FUERA_DE_LAS_176")
wo.append(["Organizaciones que están en solo una de las dos bases (no forman parte de las 176). Solo como referencia."])
wo["A1"].font = Font(bold=True, color=VERDE)
cols_o = ["RUC", "Organización", "Región", "Contacto principal", "Cargo", "Celular(es)", "Correo(s)", "Estado SUNAT", "Listas de origen"]
wo.append(cols_o)
for r in otras[cols_o].itertuples(index=False):
    wo.append(list(r))
for cell in wo[2]:
    cell.font = hdr_font; cell.fill = PatternFill("solid", fgColor=VERDE)
for j, w in enumerate([13, 44, 14, 26, 20, 15, 28, 18, 36], 1):
    wo.column_dimensions[get_column_letter(j)].width = w

# FUENTES
wf = wb.create_sheet("FUENTES")
fuentes_txt = [
    ("Fuente", "Archivo local", "Qué aporta"),
    ("MIDAGRI (ficha org.)", "data/midagri_cafe_cacao_limpio.csv", "Universo de 178; representante legal, gerente, celular, correo, web, redes (≈25 orgs con ficha llena)"),
    ("Base detallada", "PLANTILLA_INDICE_PVE_ISCAM.xlsx › base 174 detallada", "Universo de 177; mismos campos de contacto"),
    ("Matriz 174", "BASE CAFE CACAO 174/MATRIZ_ORGANIZACIONES_174_FINAL.csv", "Presidente vigente, gerente general, web principal"),
    ("OECE", "3 directorio … 12.10.26.xlsx › ruc oece personas", "Consejo de administración y representantes inscritos en el registro de proveedores"),
    ("Ficha RUC SUNAT", "CONSULTA_RUC_FUSIONADO.xlsx y fichas ruc café/cacao", "Teléfono declarado a SUNAT, domicilio fiscal, estado/condición"),
    ("Universo EUDR (PAC)", "data/backup/EUDRPERU_universo_final.csv", "Representante, teléfono y correo del PAC; contactos CENCOOP"),
    ("CENCOOP 2017", "data/backup/soparse_cencoop2017.csv y CENACOOP_fusion_EUDR.csv", "Censo de cooperativas 2017: teléfonos, correo, web (pueden estar desactualizados)"),
    ("Directorio v3", "Directorio Cooperativas Cafe-Cacao Peru (v3 - Cepicafe-Norandino).xlsx", "Representante conocido, correo y teléfono verificados manualmente"),
    ("", "", ""),
    ("Notas", "", ""),
    ("Prioridad de datos", "", "Al ordenar teléfonos/correos se priorizan las fuentes más recientes: Directorio v3 > MIDAGRI > base detallada > PAC > SUNAT > CENCOOP 2017."),
    ("Contacto principal", "", "Se elige a la persona con teléfono/correo; a igualdad, gerente > representante legal > presidente."),
    ("Calidad del contacto", "", "A: teléfono+correo · B: solo celular · C: solo correo · D: solo fijo · E: sin contacto (buscar por redes, federación o visita)."),
    ("Datos personales", "", "Contiene teléfonos y correos de personas naturales: uso exclusivo para la gestión de la encuesta (Ley 29733)."),
]
for r in fuentes_txt:
    wf.append(list(r))
for cell in wf[1]:
    cell.font = hdr_font; cell.fill = PatternFill("solid", fgColor=VERDE)
wf["A11"].font = Font(bold=True)
for c, w in zip("ABC", (22, 62, 100)):
    wf.column_dimensions[c].width = w
for row in wf.iter_rows():
    for cell in row:
        cell.alignment = Alignment(wrap_text=True, vertical="top")

wb.save(OUT)
print(f"OK {OUT.name}: {len(df)} orgs, {len(pp)} personas")
print(df["Calidad del contacto"].value_counts().sort_index().to_string())
print("con celular", (df["Celular(es)"] != "").sum(), "| con correo", (df["Correo(s)"] != "").sum(),
      "| con nombre", (df["Contacto principal"] != "").sum())
print(otras[["RUC", "Organización", "Listas de origen", "Estado SUNAT"]].to_string())
