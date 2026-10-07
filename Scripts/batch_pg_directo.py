"""
Busca RUCs por nombre directamente en PostgreSQL de identidad-fiscal.
Evita el ILIKE lento de la API usando consultas directas con GIN/trigram index.
"""
import psycopg2
import pandas as pd

conn = psycopg2.connect(
    host='localhost', port=5438,
    user='fiscal', password='fiscal',
    dbname='identidad_fiscal', connect_timeout=10
)

orgs = [
    ("CAFE PERU", "CAFÉ PERÚ"),
    ("VRAQUS", "VRAQUS"),
    ("CEOACNOR", "CEOACNOR"),
    ("BAGUA GRANDE", "Bagua Grande"),
    ("VALLE RIO APURIMAC", "Valle del Río Apurímac (VRAE)"),
    ("SAN JORGE", "San Jorge"),
    ("CAFE MONTAÑA", "Café Montaña"),
    ("RODRIGUEZ MENDOZA", "Rodríguez de Mendoza"),
    ("CACAO TUMBES", "Cacao Tumbes"),
    ("APROCAP", "APROCAP"),
    ("CEPROAA", "CEPROAA"),
    ("APROCAM", "APROCAM"),
    ("CACAO FRONTERAS", "Cacao Fronteras"),
    ("CHOBA CHOBA", "Choba Choba"),
    ("ORO VERDE", "Oro Verde"),
    ("ASPROC", "ASPROC"),
    ("DIVISORIA", "Divisoria"),
    ("CACAO ALTO HUALLAGA", "Cacao Alto Huallaga"),
    ("PALCAZU", "Palcazú"),
    ("SAN ALEJANDRO", "San Alejandro"),
    ("CAMPOS VERDES", "Campos Verdes"),
    ("PANGOA", "Pangoa"),
    ("CAFE CACAO PERU", "Café y Cacao Perú"),
    ("CACVRA", "CACVRA"),
    ("SAN GABAN", "San Gabán"),
    ("PERENE", "Perené"),
    ("TAHUANTINSUYO", "Tahuantinsuyo"),
    ("ALTO PALOMAR", "Alto El Palomar"),
    ("INCAHUASI", "Incahuasi"),
]

resultados = []
cur = conn.cursor()

# Usar LIKE (mas rapido que ILIKE si hay indice) + Upper
for query, display in orgs:
    palabras = query.replace(" ", "%").replace("  ", "%")
    like_pattern = f"%{palabras}%"

    # Query directa a PostgreSQL
    sql = """
        SELECT ruc, razon_social, estado_contribuyente, condicion_domicilio, ubigeo,
               tipo_via, nombre_via, numero
        FROM contribuyentes
        WHERE UPPER(razon_social) LIKE UPPER(%s)
          AND estado_contribuyente != 'BAJA DEFINITIVA'
        ORDER BY razon_social
        LIMIT 5
    """
    try:
        cur.execute(sql, (like_pattern,))
        rows = cur.fetchall()
        total = len(rows)

        if total == 0:
            print(f"NO ENCONTRADO: {display}")
            resultados.append({"nombre": display, "query": query, "encontrado": False})
        else:
            r = rows[0]
            ruc, razon, estado, cond, ubigeo, tv, nv, num = r
            dir_full = " ".join(filter(None, [str(tv or ""), str(nv or ""), str(num or "")]))
            print(f"ENCONTRADO [{total}]: {display} -> RUC {ruc} | {razon[:50]} | {estado} | {cond}")
            resultados.append({
                "nombre": display, "query": query,
                "encontrado": True, "total": total,
                "ruc": ruc, "razon_social": razon,
                "estado": estado, "condicion": cond,
                "ubigeo": ubigeo, "direccion": dir_full
            })
    except Exception as e:
        print(f"ERROR {display}: {e}")
        resultados.append({"nombre": display, "query": query, "encontrado": False, "error": str(e)})

cur.close()
conn.close()

# Guardar
df = pd.DataFrame(resultados)
df.to_csv("data/RUC_busqueda_pg_directo.csv", sep="|", index=False)
print()
print(f"Guardado: data/RUC_busqueda_pg_directo.csv")
encontrados = df[df["encontrado"]==True]
print(f"Total encontrados: {len(encontrados)}/{len(df)}")
