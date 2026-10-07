import pandas as pd
import re

# Leer el archivo markdown
with open(r'C:\Users\acuba\eudrperu\docs\cooperativas_fuentes_publicas.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Extraer la tabla de cooperativas
# La tabla está entre la línea 3 y la línea 29
lines = content.split('\n')

# Encontrar el inicio de la tabla (línea con headers)
table_start = None
table_end = None
for i, line in enumerate(lines):
    if line.startswith('| Item |') or line.startswith('| 1 |'):
        if table_start is None:
            table_start = i
    if line.startswith('---'):
        continue
    if table_start is not None and (line.strip() == '' or line.startswith('##')):
        table_end = i
        break

# Extraer las líneas de la tabla
table_lines = lines[table_start:table_end]

# Parsear la tabla
data = []
for line in table_lines:
    if line.strip() == '' or line.startswith('|------') or line.startswith('|---') or line.startswith('| Item |'):
        continue
    # Dividir por | y eliminar espacios
    parts = [part.strip() for part in line.split('|')]
    # Filtrar partes vacías (al inicio y final)
    parts = [p for p in parts if p]
    if len(parts) >= 5:
        data.append(parts)

# Crear DataFrame
df = pd.DataFrame(data, columns=['Item', 'Nombre de la Cooperativa', 'Lo que dicen las fuentes públicas', 'Fuentes públicas consultadas (con URL)', 'Fecha de acceso'])

# Guardar como Excel
output_path = r'C:\Users\acuba\eudrperu\docs\cooperativas_fuentes_publicas.xlsx'
df.to_excel(output_path, index=False, engine='openpyxl')

print(f'Archivo Excel creado exitosamente: {output_path}')
print(f'Total de filas: {len(df)}')
