import openpyxl
import re

# ─── Cargar matriz v7 ─────────────────────────────────────────────────────────
v7 = openpyxl.load_workbook('C:/Users/acuba/eudrperu/MATRIZ_IP_IV_v7_EUDRPERU.xlsx')
ws_v7 = v7['MATRIZ']
v7_rows = list(ws_v7.iter_rows(min_row=2, values_only=True))

def clean_ruc(v):
    if v is None: return None
    # Manejar floats de Excel (20603820691.0)
    try:
        if isinstance(v, float): v = int(v)
    except (ValueError, TypeError):
        pass
    s = str(v).strip().replace(' ', '')
    s = re.sub(r'[.\-]', '', s)
    return s if re.match(r'^\d{11}$', s) else None

v7_rucs = {}
for row in v7_rows:
    ruc = clean_ruc(row[0])
    nombre = str(row[1]).strip() if row[1] else ''
    if ruc:
        v7_rucs[ruc] = nombre

# ─── Cargar Archivo 3 (226 orgs SUNAT feb 2026) ────────────────────────────
path_a3 = ('C:/Users/acuba/.minimax/v2/assets/2026/09/18/'
           '11-41-19-638-asset_20260918-114119-638_339fdeb73f4f_'
           '62383744-ef961a72-59d3-44d9-adb4-2c9c4c728676_'
           '06260002713403 (1).xlsx')
wb3 = openpyxl.load_workbook(path_a3)
ws3 = wb3['Hoja 1']
a3_rows = list(ws3.iter_rows(values_only=True))

header = [str(c).strip() if c else '' for c in a3_rows[0]]

# Buscar columnas por nombre parcial
ruc_idx = next((i for i, h in enumerate(header) if 'RUC' in h.upper()), None)
status_idx = next((i for i, h in enumerate(header) if 'SUNAT' in h.upper() or 'HABIDO' in h.upper() or 'ACTIVO' in h.upper()), None)
nom_idx = next((i for i, h in enumerate(header) if 'NOMBRE' in h.upper()), 2)

print("Header A3:", header[:8])
print(f"RUC idx: {ruc_idx}, Status idx: {status_idx}, Nom idx: {nom_idx}")

a3_rucs = {}
for row in a3_rows[1:]:
    ruc = clean_ruc(row[ruc_idx]) if ruc_idx is not None else None
    status = str(row[status_idx]).strip() if status_idx is not None and row[status_idx] else ''
    nombre = str(row[nom_idx]).strip() if row[nom_idx] else ''
    if ruc:
        a3_rucs[ruc] = {'nombre': nombre, 'status': status}

# ─── Cruce ───────────────────────────────────────────────────────────────────
v7_set = set(v7_rucs.keys())
a3_set = set(a3_rucs.keys())

en_v7_no_a3 = v7_set - a3_set
en_a3_no_v7 = a3_set - v7_set
en_ambos = v7_set & a3_set

activos_ambos = {r: a3_rucs[r]['status'] for r in en_ambos}
habido = {r for r, s in activos_ambos.items() if 'SI' in s.upper() or 'HABIDO' in s.upper()}
no_habido = {r for r, s in activos_ambos.items() if 'NO' in s.upper() or 'BAJA' in s.upper() or 'INACTIVO' in s.upper()}

solo_a3_status = {r: a3_rucs[r]['status'] for r in en_a3_no_v7}
solo_a3_habido = sum(1 for s in solo_a3_status.values() if 'SI' in str(s).upper() or 'HABIDO' in str(s).upper())

print(f"\n=== RESULTADOS DEL CRUCE ===")
print(f"Orgs en v7 (con RUC limpio):        {len(v7_set)}")
print(f"Orgs en A3 (con RUC limpio):       {len(a3_set)}")
print(f"  -> En ambos:                     {len(en_ambos)}")
print(f"  -> Solo en v7 (sin RUC en A3):   {len(en_v7_no_a3)}")
print(f"  -> Solo en A3 (ausentes en v7):  {len(en_a3_no_v7)}")
print(f"     de estos, HABIDO:              {solo_a3_habido}")
print(f"     de estos, NO HABIDO/Baja:      {len(en_a3_no_v7) - solo_a3_habido}")

print(f"\nIntersccion — de {len(en_ambos)} orgs en ambos:")
print(f"  Status HABIDO (SI):               {len(habido)}")
print(f"  Status NO HABIDO/Baja:            {len(no_habido)}")

print(f"\n--- Muestra: orgs solo en v7 (primeros 20 RUC) ---")
for ruc in sorted(list(en_v7_no_a3))[:20]:
    print(f"  {ruc}  ->  {v7_rucs[ruc]}")

print(f"\n--- Muestra: orgs solo en A3, ausentes en v7 (primeros 20) ---")
for ruc in sorted(list(en_a3_no_v7))[:20]:
    d = a3_rucs[ruc]
    print(f"  {ruc}  [{d['status']:10s}]  ->  {d['nombre']}")
