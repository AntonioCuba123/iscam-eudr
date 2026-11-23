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
df = df.sort_values(["Región", "Provincia", "Organización"]).reset_index(drop=True)
df.insert(0, "N.º", range(1, len(df) + 1))
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
