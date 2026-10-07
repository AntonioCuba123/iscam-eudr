"""
Investigacion de 18 organizaciones sin RUC en SUNAT.
Estrategia: busquedas multiples con terminos expandidos + filtro regional.
"""
import psycopg2
import pandas as pd

conn = psycopg2.connect(
    host='localhost', port=5438,
    user='fiscal', password='fiscal',
    dbname='identidad_fiscal', connect_timeout=10
)

# Organizaciones faltantes con busquedas alternativas
# (termino_principal, sinonimos, region)
faltantes = [
    {
        "org": "CACVRA",
        "display": "CACVRA (Central Valle Río Apurímac)",
        "terminos": ["CACVRA", "CENTRAL VALLE APURIMAC", "COOP VALLE APURIMAC", "VALLE RIO APURIMAC", "CENTRAL CAFETALERA VALLE"],
        "region": "APURIMAC",
    },
    {
        "org": "CEOACNOR",
        "display": "CEOACNOR",
        "terminos": ["CEOACNOR", "CENTRAL ORGANICA NORTE", "CAFES NORTE", "CAFECERCA NORTE"],
        "region": "CAJAMARCA",
    },
    {
        "org": "VRAQUS",
        "display": "VRAQUS",
        "terminos": ["VRAQUS", "VALLE RIO APURIMAC QUIMABAMBA", "VRAEM CAFE"],
        "region": "CUSCO",
    },
    {
        "org": "Bagua Grande",
        "display": "Bagua Grande (Amazonas)",
        "terminos": ["BAGUA GRANDE", "LUYA", "CHACHAPOYAS", "BAGUA"],
        "region": "AMAZONAS",
    },
    {
        "org": "Valle del Río Apurímac",
        "display": "Valle del Río Apurímac (VRAE)",
        "terminos": ["VALLE RIO APURIMAC", "VRAE", "QUIMABAMBA", "SAN JORGE APURIMAC"],
        "region": "CUSCO",
    },
    {
        "org": "San Jorge",
        "display": "San Jorge",
        "terminos": ["SAN JORGE APURIMAC", "SAN JORGE VRAE", "COOP SAN JORGE"],
        "region": "CUSCO",
    },
    {
        "org": "Rodríguez de Mendoza",
        "display": "Rodríguez de Mendoza (Amazonas)",
        "terminos": ["RODRIGUEZ MENDOZA", "MENDOZA AMAZONAS", "ASPRM"],
        "region": "AMAZONAS",
    },
    {
        "org": "Café Montaña",
        "display": "Café Montaña",
        "terminos": ["CAFE MONTAÑA", "MONTAÑA VERDE", "CAFE SELVA"],
        "region": None,
    },
    {
        "org": "Cacao Tumbes",
        "display": "Cacao Tumbes",
        "terminos": ["CACAO TUMBES", "CACAOTERA TUMBES", "TUMBES CACAO"],
        "region": "TUMBES",
    },
    {
        "org": "APROCAP",
        "display": "APROCAP",
        "terminos": ["APROCAP", "ASOC PRODUCTORES CACAO", "PRODUCTORES CACAO PASCO"],
        "region": "PASCO",
    },
    {
        "org": "CEPROAA",
        "display": "CEPROAA",
        "terminos": ["CEPROAA", "CENTRAL PRODUCTORES", "CACAO AMAZONAS"],
        "region": "AMAZONAS",
    },
    {
        "org": "Cacao Fronteras",
        "display": "Cacao Fronteras",
        "terminos": ["CACAO FRONTERAS", "FRONTERA CACAO", "CACAO NORTE SAN MARTIN"],
        "region": "SAN MARTIN",
    },
    {
        "org": "Cacao Alto Huallaga",
        "display": "Cacao Alto Huallaga",
        "terminos": ["CACAO ALTO HUALLAGA", "ALTO HUALLAGA CACAO", "MARAÑON CACAO"],
        "region": "HUANUCO",
    },
    {
        "org": "San Gabán",
        "display": "San Gabán (Puno)",
        "terminos": ["SAN GABAN", "SANGABAN", "MACUSANI"],
        "region": "PUNO",
    },
    {
        "org": "San Alejandro",
        "display": "San Alejandro",
        "terminos": ["SAN ALEJANDRO HUANUCO", "ALEJANDRO PADRE"],
        "region": "HUANUCO",
    },
    {
        "org": "Campos Verdes",
        "display": "Campos Verdes",
        "terminos": ["CAMPOS VERDES", "CAMPOS VERDES VRAE"],
        "region": "CUSCO",
    },
    {
        "org": "Alto El Palomar",
        "display": "Alto El Palomar",
        "terminos": ["ALTO PALOMAR", "PALOMAR SELVA"],
        "region": None,
    },
    {
        "org": "Café y Cacao Perú",
        "display": "Café y Cacao Perú",
        "terminos": ["CAFE CACAO PERU", "CAFE Y CACAO PERU", "COMERCIO CAFE CACAO"],
        "region": None,
    },
]

cur = conn.cursor()
resultados = []

print(f"Investigando {len(faltantes)} organizaciones...\n")

for item in faltantes:
    org = item["org"]
    display = item["display"]
    region = item["region"]
    todos_matches = []

    for termino in item["terminos"]:
        patron = f"%{termino}%"
        if region:
            sql = """
                SELECT ruc, razon_social, estado_contribuyente, condicion_domicilio, ubigeo
                FROM contribuyentes
                WHERE razon_social ILIKE %s
                  AND estado_contribuyente NOT IN ('BAJA DEFINITIVA', 'BAJA DE OFICIO')
                  AND ubigeo LIKE %s
                ORDER BY razon_social
                LIMIT 5
            """
            ubigeo_pattern = region[:2] + "%"
            cur.execute(sql, (patron, ubigeo_pattern))
        else:
            sql = """
                SELECT ruc, razon_social, estado_contribuyente, condicion_domicilio, ubigeo
                FROM contribuyentes
                WHERE razon_social ILIKE %s
                  AND estado_contribuyente NOT IN ('BAJA DEFINITIVA', 'BAJA DE OFICIO')
                ORDER BY razon_social
                LIMIT 5
            """
            cur.execute(sql, (patron,))

        rows = cur.fetchall()
        for r in rows:
            todos_matches.append({
                "ruc": r[0],
                "razon_social": r[1],
                "estado": r[2],
                "condicion": r[3],
                "ubigeo": r[4],
                "termino": termino,
            })

    # Deduplicar por RUC
    seen = set()
    unicos = []
    for m in todos_matches:
        if m["ruc"] not in seen:
            seen.add(m["ruc"])
            unicos.append(m)

    if unicos:
        mejor = unicos[0]
        print(f"ENCONTRADO [{display}]:")
        print(f"    RUC: {mejor['ruc']}")
        print(f"    Nombre: {mejor['razon_social'][:70]}")
        print(f"    Estado: {mejor['estado']} | {mejor['condicion']}")
        print(f"    Ubigeo: {mejor['ubigeo']}")
        print(f"    Termino que matcheo: {mejor['termino']}")
        if len(unicos) > 1:
            print(f"    +{len(unicos)-1} alternativa(s):")
            for a in unicos[1:]:
                print(f"      - {a['ruc']} | {a['razon_social'][:55]}")
        print()
        resultados.append({
            "org": org, "display": display,
            "encontrado": True,
            "ruc": mejor["ruc"],
            "razon_social": mejor["razon_social"],
            "estado": mejor["estado"],
            "condicion": mejor["condicion"],
            "ubigeo": mejor["ubigeo"],
            "alternativas": len(unicos) - 1,
        })
    else:
        print(f"NO ENCONTRADO: {display}")
        print()
        resultados.append({"org": org, "display": display, "encontrado": False})

cur.close()
conn.close()

df = pd.DataFrame(resultados)
df.to_csv("data/RUC_investigacion_faltantes.csv", sep="|", index=False)
print("=" * 60)
encontrados = df[df["encontrado"]==True]
print(f"RESULTADO: {len(encontrados)}/{len(df)} organizaciones encontradas")
print(f"Guardado: data/RUC_investigacion_faltantes.csv")
