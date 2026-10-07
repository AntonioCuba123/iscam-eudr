# -*- coding: utf-8 -*-
"""Análisis profundo de certificaciones en PAC + modelo ISCAM."""
import openpyxl
from collections import Counter

BASE = r'C:/Users/acuba/eudrperu'

# ── PAC v3: certificaciones ────────────────────────────────
print("="*60)
print("PAC v3 — CERTIFICACIONES CONOCIDAS")
print("="*60)

wb3 = openpyxl.load_workbook(
    f'{BASE}/Directorio Cooperativas Cafe-Cacao Peru (v3 - Cepicafe-Norandino).xlsx',
    read_only=True, data_only=True
)
sh3 = wb3['Cooperativas y asociaciones']

rows = list(sh3.iter_rows(values_only=True))
headers = [str(c) if c else '' for c in rows[0]]
cert_idx = None
for i, h in enumerate(headers):
    if 'certific' in h.lower():
        cert_idx = i
        print(f"  Columna certificaciones: [{i}] '{h}'")
        break

print(f"\n  Total orgs en PAC v3: {len(rows)-1}")
print(f"\n  FILA POR FILA — certificaciones:")
cert_values = []
for i, row in enumerate(rows[1:], start=2):
    org = row[0] if len(row) > 0 else ''
    cert = row[cert_idx] if cert_idx is not None and cert_idx < len(row) else ''
    if cert and str(cert).strip():
        cert_values.append((str(org).strip(), str(cert).strip()))
        print(f"  [{i:2d}] {org:<35} → {cert}")

print(f"\n  TOTAL con certificación conocida: {len(cert_values)}/48")
print(f"\n  Valores únicos de certificación:")
for org, cert in cert_values:
    print(f"    {org}: {cert}")

# ── PAC v1: certificaciones ───────────────────────────────
print("\n" + "="*60)
print("PAC v1 — CERTIFICACIONES CONOCIDAS")
print("="*60)

wb1 = openpyxl.load_workbook(
    f'{BASE}/Directorio Cooperativas Cafe-Cacao Peru.xlsx',
    read_only=True, data_only=True
)
sh1 = wb1['Cooperativas y asociaciones']
rows1 = list(sh1.iter_rows(values_only=True))
headers1 = [str(c) if c else '' for c in rows1[0]]

cert_idx1 = None
for i, h in enumerate(headers1):
    if 'certific' in h.lower():
        cert_idx1 = i
        print(f"  Columna: [{i}] '{h}'")
        break

print(f"\n  Total orgs PAC v1: {len(rows1)-1}")
cert_vals1 = []
for row in rows1[1:]:
    org = row[0] if len(row) > 0 else ''
    cert = row[cert_idx1] if cert_idx1 is not None and cert_idx1 < len(row) else ''
    if cert and str(cert).strip():
        cert_vals1.append((str(org).strip(), str(cert).strip()))
        print(f"    {org:<35} → {cert}")

print(f"\n  TOTAL PAC v1 con cert: {len(cert_vals1)}/{len(rows1)-1}")

# ── Modelo ISCAM ──────────────────────────────────────────
print("\n" + "="*60)
print("MODELO ISCAM — estructura real de datos")
print("="*60)

wb_iscam = openpyxl.load_workbook(
    f'{BASE}/Modelo de Calculo - ISA-IP-IV-RE-AHP.xlsx',
    read_only=True, data_only=True
)
print(f"  Hojas: {wb_iscam.sheetnames}")

# Datos_Crudos
ws_dc = wb_iscam['Datos_Crudos']
dc_rows = list(ws_dc.iter_rows(values_only=True))
dc_headers = list(dc_rows[0])
print(f"\n  Datos_Crudos: {len(dc_rows)-1} orgs × {len(dc_headers)} columnas")
print(f"  Headers relevantes para certificaciones:")
for i, h in enumerate(dc_headers):
    if 'cert' in str(h).lower() or '10' in str(h) or 'D11' in str(h) or 'D10' in str(h):
        print(f"    [{i:2d}] {h}")

# Ver estructura Cert_conteo_0a4 y D10
print(f"\n  Detalle de columnas de certificación:")
for row in dc_rows[1:]:
    if row[0]:  # skip empty
        org = row[0]
        # Find cert columns
        cert_count_idx = dc_headers.index('Cert_conteo_0a4') if 'Cert_conteo_0a4' in dc_headers else None
        d10_36_idx = dc_headers.index('D10_36_texto') if 'D10_36_texto' in dc_headers else None
        d10_37_idx = dc_headers.index('D10_37_texto') if 'D10_37_texto' in dc_headers else None
        d11_idx = dc_headers.index('D11_conteo_0a7') if 'D11_conteo_0a7' in dc_headers else None

        cert_count = row[cert_count_idx] if cert_count_idx else None
        d10_36 = row[d10_36_idx] if d10_36_idx else None
        d10_37 = row[d10_37_idx] if d10_37_idx else None
        d11 = row[d11_idx] if d11_idx else None
        print(f"  {org}:")
        print(f"    Cert_conteo: {cert_count}")
        print(f"    D10_36 (certific): {d10_36}")
        print(f"    D10_37 (estado): {d10_37}")
        print(f"    D11_conteo: {d11}")

# Sheet ISA
ws_isa = wb_iscam['ISA']
isa_rows = list(ws_isa.iter_rows(values_only=True))
print(f"\n  ISA sheet: {len(isa_rows)-1} orgs")
for row in isa_rows[1:]:
    if row[0]:
        print(f"  {row}")

# Sheet RE_Tipologia
ws_re = wb_iscam['RE_Tipologia']
re_rows = list(ws_re.iter_rows(values_only=True))
print(f"\n  RE_Tipologia: {len(re_rows)-1} orgs")
for row in re_rows[1:]:
    if row[0]:
        print(f"  {row}")

wb3.close()
wb1.close()
wb_iscam.close()

print("\n" + "="*60)
print("CORRECCIÓN AL ANÁLISIS ANTERIOR")
print("="*60)
print("""
ANTERIOR: 2/245 orgs con certificación en universo_consolidado
CORRECTO:  5/48 orgs tienen 'Certificación conocida' en PAC v3

El campo 'Certificación conocida' del PAC v3 tiene 5 valores:
  1. CECOVASA  → Fairtrade, Orgánico, Rainforest Alliance
  2. Fairtrade (mención en PAC v1 como contexto)
  3-5. Otras 3 organizaciones por identificar

Además, el archivo 'Modelo de Calculo - ISA-IP-IV-RE-AHP.xlsx' ya
contiene una estructura de 52 columnas con el Instrumento 2 codificado:
  - Datos_Crudos: 8 orgs de ejemplo con D1-D11 completos
  - D10_36_texto / D10_37_texto: preguntas de certificación
  - Cert_conteo_0a4: conteo de certificaciones (0-4)
  - D11_conteo_0a7: volumen/complejidad exportadora

Esto es MUCHO más rico que lo que se reflejó en el universo_consolidado.csv
""")
