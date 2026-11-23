import pandas as pd
import json

# Leer CSV
df = pd.read_csv('data/midagri_cafe_cacao_limpio.csv')
print("=== CSV Shape ===")
print(f"Filas: {df.shape[0]}, Columnas: {df.shape[1]}")
print("\n=== Columnas ===")
print(list(df.columns))

# Leer JSON resumen
with open('data/resumen_universo_midagri.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("\n=== JSON Resumen ===")
print(f"Total organizaciones: {data.get('total_organizaciones_originales')}")
print(f"Total café+y cacao: {data.get('total_cafe_y_cacao')}")
print(f"Total café: {data.get('total_cafe')}")
print(f"Total cacao: {data.get('total_cacao')}")
print(f"Total cooperativas: {data.get('total_cooperativas')}")
print(f"Total asociaciones: {data.get('total_asociaciones')}")
print(f"Activas y habidas: {data.get('total_activas_y_habidas')}")
print(f"Cooperativas activas: {data.get('cooperativas_activas_habidas')}")
print(f"Con avance EUDR declarado: {data.get('con_avance_eudr_declarado')}")
print(f"Promedio avance EUDR: {data.get('promedio_avance_eudr_declarado')}")

# Ver primeras filas del CSV
print("\n=== Primeras filas CSV ===")
print(df.head(3).to_string())