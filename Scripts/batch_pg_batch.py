"""
Busca RUCs en PostgreSQL identidad-fiscal con una sola query.
Usa posicion inicial del termino en razon_social (usando strpos).
"""
import psycopg2
import pandas as pd

conn = psycopg2.connect(
    host='localhost', port=5438,
    user='fiscal', password='fiscal',
    dbname='identidad_fiscal', connect_timeout=10
)

# Terminos de busqueda para cada organizacion
# Se busca con strpos (posicion) para evitar LIKE %patron% lento
terminos = [
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
    ("SAN GABAN", "San Gabán"),
    ("SAN ALEJANDRO", "San Alejandro"),
    ("CAMPOS VERDES", "Campos Verdes"),
    ("ALTO PALOMAR", "Alto El Palomar"),
    ("TAHUANTINSUYO", "Tahuantinsuyo"),
    ("CACAO TUMBES", "Cacao Tumbes"),
    ("CACAO FRONTERAS", "Cacao Fronteras"),
    ("CACAO HUALLAGA", "Cacao Alto Huallaga"),
    ("CAFE MONTAÑA", "Café Montaña"),
    ("CEOACNOR", "CEOACNOR"),
    ("VRAQUS", "VRAQUS"),
    ("RODRIGUEZ MENDOZA", "Rodríguez de Mendoza"),
    ("SAN JORGE AMOTAPE", "San Jorge"),
    ("VALLE RIO APURIMAC", "Valle del Río Apurímac"),
    ("BAGUA GRANDE", "Bagua Grande"),
    ("CAFE PERU", "CAFÉ PERÚ"),
    ("CAFE CACAO PERU", "Café y Cacao Perú"),
]

# Construir query SQL con strpos para cada termino
# strpos es O(n) pero en la practica es mas rapido que LIKE
conditions = " OR ".join([f"strpos(UPPER(razon_social), '{t.upper()}') > 0" for t, _ in terminos])
sql = f"""
    SELECT ruc, razon_social, estado_contribuyente, condicion_domicilio, ubigeo
    FROM contribuyentes
    WHERE ({conditions})
      AND estado_contribuyente != 'BAJA DEFINITIVA'
    ORDER BY razon_social
    LIMIT 100
"""

print("Ejecutando query en 2.3M registros...")
cur = conn.cursor()
cur.execute(sql)
rows = cur.fetchall()
print(f"Resultados: {len(rows)} filas")
print()

# Para cada organizacion, encontrar el mejor match
resultados = []
for termino, display in terminos:
    # Filtrar los resultados que contienen este termino
    matches = [r for r in rows if termino.upper() in r[1].upper()]
    if matches:
        # Filtrar los que sonBAJA y tomar el mejor
        activos = [m for m in matches if m[2] not in ('BAJA DEFINITIVA',)]
        if activos:
            mejor = activos[0]
            print(f"OK [{display}]: {mejor[0]} | {mejor[1][:55]} | {mejor[2]} | {mejor[3]}")
            resultados.append({
                "nombre": display, "termino": termino,
                "encontrado": True, "ruc": mejor[0],
                "razon_social": mejor[1],
                "estado": mejor[2], "condicion": mejor[3],
                "ubigeo": mejor[4]
            })
        else:
            print(f"Solo BAJA [{display}]: {matches[0][0]}")
            resultados.append({"nombre": display, "termino": termino, "encontrado": False, "nota": "Solo BAJA DEFINITIVA"})
    else:
        print(f"NO [{display}]")
        resultados.append({"nombre": display, "termino": termino, "encontrado": False})

cur.close()
conn.close()

# Guardar
df = pd.DataFrame(resultados)
df.to_csv("data/RUC_busqueda_pg_batch.csv", sep="|", index=False)
print()
print(f"Guardado: data/RUC_busqueda_pg_batch.csv")
encontrados = df[df["encontrado"]==True]
print(f"Total encontrados: {len(encontrados)}/{len(df)}")
