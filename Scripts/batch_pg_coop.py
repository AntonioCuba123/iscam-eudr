"""
Busca RUCs de cooperativas agrarias en identidad-fiscal via pg_trgm.
Busca: COOPERATIVA AGRARIA + termino clave.
"""
import psycopg2
import pandas as pd

conn = psycopg2.connect(
    host='localhost', port=5438,
    user='fiscal', password='fiscal',
    dbname='identidad_fiscal', connect_timeout=10
)

orgs = [
    # (termino_busqueda, nombre_display)
    ("CACVRA", "CACVRA"),
    ("PANGOA", "Pangoa"),
    ("INCAHUASI", "Incahuasi"),
    ("CHOBA", "Choba Choba"),
    ("APROCAP", "APROCAP"),
    ("APROCAM", "APROCAM"),
    ("CEPROAA", "CEPROAA"),
    ("OROVERDE", "Oro Verde"),
    ("ASPROC", "ASPROC"),
    ("DIVISORIA", "Divisoria"),
    ("PALCAZU", "Palcazú"),
    ("PERENE", "Perené"),
    ("SANGABAN", "San Gabán"),
    ("SANALEJANDRO", "San Alejandro"),
    ("CAMPOSVERDES", "Campos Verdes"),
    ("ALTOPALOMAR", "Alto El Palomar"),
    ("TAHUANTINSUYO", "Tahuantinsuyo"),
    ("CACAOTUMBES", "Cacao Tumbes"),
    ("CACAOFRONTERAS", "Cacao Fronteras"),
    ("CACAOHUALLAGA", "Cacao Alto Huallaga"),
    ("CAFEMONTAÑA", "Café Montaña"),
    ("CEOACNOR", "CEOACNOR"),
    ("VRAQUS", "VRAQUS"),
    ("RODRIGUEZMENDOZA", "Rodríguez de Mendoza"),
    ("SANJORGE", "San Jorge"),
    ("VALLEAPURIMAC", "Valle del Río Apurímac"),
    ("BAGUAGRANDE", "Bagua Grande"),
    ("CAFEPERU", "CAFÉ PERÚ"),
    ("CAFECACAOPERU", "Café y Cacao Perú"),
]

resultados = []
cur = conn.cursor()

print(f"Buscando {len(orgs)} organizaciones como COOPERATIVA AGRARIA...")

for termino, display in orgs:
    # Usar ILIKE con el indice trigram (rapido)
    # Buscar COOPERATIVA y el termino
    sql = """
        SELECT ruc, razon_social, estado_contribuyente, condicion_domicilio, ubigeo
        FROM contribuyentes
        WHERE razon_social ILIKE %s
          AND estado_contribuyente NOT IN ('BAJA DEFINITIVA', 'BAJA DE OFICIO')
        ORDER BY razon_social
        LIMIT 3
    """
    # Dos estrategias: con COOPERATIVA y solo el termino
    patron_coop = f"%COOPERATIVA%{termino}%"
    patron_solo = f"%{termino}%"

    cur.execute(sql, (patron_coop,))
    rows_coop = cur.fetchall()

    if rows_coop:
        r = rows_coop[0]
        print(f"OK [COOP] {display}: {r[0]} | {r[1][:55]} | {r[2]} | {r[3]}")
        resultados.append({
            "nombre": display, "termino": termino,
            "encontrado": True, "patron": "COOPERATIVA+termino",
            "ruc": r[0], "razon_social": r[1],
            "estado": r[2], "condicion": r[3], "ubigeo": r[4]
        })
    else:
        # Buscar solo el termino (asociaciones o nombres alternativos)
        sql2 = """
            SELECT ruc, razon_social, estado_contribuyente, condicion_domicilio, ubigeo
            FROM contribuyentes
            WHERE razon_social ILIKE %s
              AND estado_contribuyente NOT IN ('BAJA DEFINITIVA', 'BAJA DE OFICIO')
            ORDER BY razon_social
            LIMIT 1
        """
        cur.execute(sql2, (patron_solo,))
        rows_solo = cur.fetchall()
        if rows_solo:
            r = rows_solo[0]
            print(f"OK [SOLO] {display}: {r[0]} | {r[1][:55]} | {r[2]} | {r[3]}")
            resultados.append({
                "nombre": display, "termino": termino,
                "encontrado": True, "patron": "solo",
                "ruc": r[0], "razon_social": r[1],
                "estado": r[2], "condicion": r[3], "ubigeo": r[4]
            })
        else:
            print(f"NO {display}")
            resultados.append({
                "nombre": display, "termino": termino,
                "encontrado": False
            })

cur.close()
conn.close()

df = pd.DataFrame(resultados)
df.to_csv("data/RUC_busqueda_pg_coop.csv", sep="|", index=False)
print()
print(f"Guardado: data/RUC_busqueda_pg_coop.csv")
encontrados = df[df["encontrado"]==True]
print(f"Total encontrados: {len(encontrados)}/{len(df)}")
