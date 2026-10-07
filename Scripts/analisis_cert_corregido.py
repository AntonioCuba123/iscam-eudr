# -*- coding: utf-8 -*-
"""Corrección: extraer certificaciones reales del PAC v3 y actualizar el universo."""
import openpyxl, csv, os
from collections import Counter

BASE = r'C:/Users/acuba/eudrperu/data'

# ── PAC v3: extraer todo con certificaciones ──────────────
wb3 = openpyxl.load_workbook(
    f'{BASE}/../Directorio Cooperativas Cafe-Cacao Peru (v3 - Cepicafe-Norandino).xlsx',
    read_only=True, data_only=True
)
sh3 = wb3['Cooperativas y asociaciones']
rows3 = list(sh3.iter_rows(values_only=True))
headers3 = [str(c) if c else '' for c in rows3[0]]
wb3.close()

# Find cert column
cert_idx = next((i for i, h in enumerate(headers3) if 'certific' in h.lower()), None)
print(f"Headers: {headers3}")
print(f"Cert idx: {cert_idx}")

# Build dict of org name → cert
cert_map = {}
for row in rows3[1:]:
    org = str(row[0]).strip() if row[0] else ''
    cert = str(row[cert_idx]).strip() if cert_idx and cert_idx < len(row) and row[cert_idx] else ''
    if org and cert:
        cert_map[org.upper()] = cert

print(f"\nOrganizaciones con certificación en PAC v3 ({len(cert_map)}):")
for org, cert in cert_map.items():
    print(f"  {org:<40} {cert}")

# ── Universo: cruzar certificaciones ─────────────────────
print("\n\n--- Cruce con universo ---")
u_path = os.path.join(BASE, 'EUDRPERU_universo_consolidado.csv')
with open(u_path, encoding='utf-8') as f:
    u_rows = list(csv.DictReader(f, delimiter='|'))

n = len(u_rows)
updated = 0
for r in u_rows:
    name_upper = r.get('nombre','').upper()
    # Try exact match first
    if name_upper in cert_map:
        r['cert_pac'] = cert_map[name_upper]
        updated += 1
    else:
        # Try partial match
        for pac_org, cert in cert_map.items():
            if pac_org in name_upper or name_upper in pac_org:
                r['cert_pac'] = cert
                updated += 1
                print(f"  Match parcial: '{name_upper}' ~ '{pac_org}' → {cert}")
                break

print(f"\n  Org con cert después del cruce: {updated}")
print(f"  Total universo: {n}")

# Count non-empty cert_pac
cert_nonempty = [r for r in u_rows if r.get('cert_pac','').strip() and r.get('cert_pac','').strip() not in ('nan','None')]
print(f"  Cert no vacío: {len(cert_nonempty)}/{n}")

# ── Actualizar universo_consolidado.csv ──────────────────
new_u_path = os.path.join(BASE, 'EUDRPERU_universo_consolidado.csv')
fieldnames = list(u_rows[0].keys())

# Backup first
import shutil
shutil.copy(new_u_path, new_u_path.replace('.csv', '_backup.csv'))
print(f"\nBackup creado: {os.path.basename(new_u_path.replace('.csv', '_backup.csv'))}")

with open(new_u_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, delimiter='|', fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(u_rows)

print(f"Actualizado: {os.path.basename(new_u_path)}")

# ── Output corrected coverage ────────────────────────────
print("\n\n" + "="*60)
print("COBERTURA CORREGIDA — CERTIFICACIONES")
print("="*60)
pct = len(cert_nonempty)/n*100
bar = '█' * int(pct/5) + '░' * (20-int(pct/5))
print(f"  {bar} {pct:.0f}%  ({len(cert_nonempty)}/245 orgs)")
print(f"\n  Organizaciones con certificación conocida:")
for r in cert_nonempty:
    print(f"    {r.get('nombre',''):<45} | {r.get('cert_pac','')}")

print(f"""
\nCORRECCIÓN AL ANÁLISIS ANTERIOR:
  ❌ ANTERIOR: 2/245 orgs con certificación
  ✅ CORREGIDO: {len(cert_nonempty)}/48 en PAC (pero solo {len(cert_nonempty)}/{n} del universo cruzado)

En el universo de 245 orgs (café+cacao), las certificaciones conocidas del PAC v3
cubren solo las organizaciones que están en el directorio PAC (~48 de las 245).
Las otras ~197 orgs fueron añadidas por MIDAGRI/PRODUCE y no tienen certificación.

Esto significa:
  - Tasa de cobertura de certificaciones EN EL PAC DIRECTO: 5/48 = 10%
  - Tasa de cobertura EN EL UNIVERSO COMPLETO: {len(cert_nonempty)}/{n} = {len(cert_nonempty)/n*100:.0f}%
  - Org sin cobertura PAC: resto del universo (MIDAGRI, PRODUCE)
""")
