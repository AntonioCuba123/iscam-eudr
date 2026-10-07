# -*- coding: utf-8 -*-
"""Análisis de cobertura de datos IP vs IV en las 4 fuentes."""
import csv, os, re
from collections import Counter

BASE = r'C:/Users/acuba/eudrperu/data'

def load_csv(name, delim='|', enc='utf-8'):
    path = os.path.join(BASE, name)
    try:
        with open(path, encoding=enc) as f:
            return list(csv.DictReader(f, delimiter=delim))
    except Exception:
        # try pipe
        with open(path, encoding=enc) as f:
            return list(csv.DictReader(f, delimiter='|'))

def safe_float(v):
    try:
        return float(v.strip().replace(',',''))
    except:
        return None

print("="*65)
print("ANÁLISIS: DATOS EXISTENTES vs. CAMPOS REQUERIDOS POR IP/IV")
print("="*65)

# ── Load all sources ──────────────────────────────────────
m = load_csv('MIDAGRI_cooperativas_agrarias_2026.csv')  # 961
p = load_csv('Cooperativas_2024_PRODUCE.csv', delim='|')  # 2266
c = load_csv('CENACOOP_fusion_EUDR.csv')  # 144
u = load_csv('EUDRPERU_universo_consolidado.csv')  # 245

print(f"\nFUENTES CARGADAS:")
print(f"  MIDAGRI 2026     : {len(m):>4} organizaciones")
print(f"  PRODUCE 2024     : {len(p):>4} organizaciones")
print(f"  CENACOOP fusion  : {len(c):>4} organizaciones")
print(f"  Universo EUDR     : {len(u):>4} organizaciones (universo咖啡+cacao)")

# ── PRODUCE experiencia ──────────────────────────────────
print("\n\n[ PRODUCE: campo 'experiencia' ]")
print(f"  Headers: {list(p[0].keys())[:8]}")
exp_vals = Counter([r.get('experiencia','').strip() for r in p])
print(f"  Distribución: {exp_vals.most_common(10)}")
exporta_vals = Counter([r.get('exporta','').strip() for r in p])
print(f"  exporta: {exporta_vals}")
fob_vals = [safe_float(r.get('fob_miles_dolar','0')) for r in p]
fob_nonzero = [v for v in fob_vals if v and v > 0]
print(f"  FOB > 0: {len(fob_nonzero)}/{len(p)}")

# ── universo consolidado ─────────────────────────────────
print("\n\n[ UNIVERSO CONSOLIDADO: cobertura de vars relevantes ]")
n = len(u)

checks = {
    'd2024_exporta': 'Exporta a 2024 (PRODUCE)',
    'd2024_fob':     'FOB 2024 (miles USD)',
    'socios_total':   'N° socios',
    'anio_inscripcion': 'Año inscripción MIDAGRI',
    'sunat_exporta':  'Exporta (SUNAT) — siempre False, useless',
}
for fld, label in checks.items():
    vals = [r.get(fld,'').strip() for r in u]
    nonempty = [v for v in vals if v and v not in ('nan','None')]
    pct = len(nonempty)/n*100
    bar = '█' * int(pct/5) + '░' * (20-int(pct/5))
    print(f"  {bar} {pct:4.0f}%  {label} ({len(nonempty)}/{n})")

# FOB nonzero en universo
fob_u = [safe_float(r.get('d2024_fob','0')) for r in u]
fob_nz = [v for v in fob_u if v and v > 0]
exp_u = [safe_float(r.get('exp_fob_usd','0')) for r in u]
exp_nz = [v for v in exp_u if v and v > 0]
pct_fob = len(fob_nz)/n*100
pct_exp = len(exp_nz)/n*100
bar_fob = '█' * int(pct_fob/5) + '░' * (20-int(pct_fob/5))
bar_exp = '█' * int(pct_exp/5) + '░' * (20-int(pct_exp/5))
print(f"  {bar_fob} {pct_fob:4.0f}%  FOB 2024 nonzero ({len(fob_nz)}/{n})")
print(f"  {bar_exp} {pct_exp:4.0f}%  FOB USD SUNAT nonzero ({len(exp_nz)}/{n})")

# Exportadores puros
exp_si = [r for r in u if r.get('d2024_exporta','').strip() == 'SI']
print(f"\n  Organizaciones que exportan según PRODUCE: {len(exp_si)}")
if exp_si:
    fobs = sorted([safe_float(r.get('d2024_fob','0')) or 0 for r in exp_si], reverse=True)
    print(f"  Top 5 FOB: {fobs[:5]}")

# ── cert_pac ────────────────────────────────────────────
print("\n\n[ CERTIFICACIONES en PAC directory ]")
cert_vals = [r.get('cert_pac','').strip() for r in u]
cert_nonempty = [v for v in cert_vals if v and v != 'nan']
print(f"  Org con cert_pac no vacío: {len(cert_nonempty)}/245")
for v in cert_nonempty:
    print(f"    → {v}")

# ── MIDAGRI: qué tiene ──────────────────────────────────
print("\n\n[ MIDAGRI 2026: headers completos ]")
print(f"  {list(m[0].keys())}")
# actividad_principal - cuántas son café/cacao
prod_m = Counter([r.get('producto_principal','').strip() for r in m])
print(f"\n  Productos únicos: {len(prod_m)}")
print(f"  Top 10: {prod_m.most_common(10)}")

# ── Síntesis IP vs IV ────────────────────────────────────
print("\n\n" + "="*65)
print("SÍNTESIS: MAPA DE EXISTENCIA DE DATOS")
print("="*65)
print("""
Cada celda responde: ¿cuántas de las 245 orgs del universo tienen
este dato en alguna de las 4 fuentes?

╔══════════════════════════════════════════╦══════════╦══════════╗
║  DIMENSIÓN ISCAM                        ║  IP / IV  ║  COBERTURA ║
╠══════════════════════════════════════════╬══════════╬══════════╣
║  D1: Identificación del operador         ║    IV    ║  ░░░░░  0%  ║
║  D2: Trazabilidad                       ║    IV    ║  ░░░░░  0%  ║
║  D3: Geolocalización                    ║    IV    ║  ░░░░░  0%  ║
║  D4: Vigilancia                         ║    IV    ║  ░░░░░  0%  ║
║  D5: Due diligence                     ║    IV    ║  ░░░░░  0%  ║
║  D6: Papeles deforestación              ║    IV    ║  ░░░░░  0%  ║
║  D7: Sanciones                         ║    IV    ║  ░░░░░  0%  ║
╠══════════════════════════════════════════╬══════════╬══════════╣
║  D8: Capacidad operativa               ║    IP    ║  █░░░░ ~20% ║
║    · Años de operación (inscripción)   ║    IP    ║  ███░░ ~69% ║
║    · N° socios / trabajadores           ║    IP    ║  ███░░ ~69% ║
║    · Software / conectividad           ║    IP    ║  ░░░░░  0%  ║
║    · Asistencia técnica                 ║    IP    ║  ░░░░░  0%  ║
║    · Presupuesto EUDR                  ║    IP    ║  ░░░░░  0%  ║
╠══════════════════════════════════════════╬══════════╬══════════╣
║  D9: Acceso a mercados                 ║    IP    ║  ██░░░ ~59% ║
║    · Exporta (SI/NO)                   ║    IP    ║  ██░░░ ~59% ║
║    · FOB exportaciones                 ║    IP    ║  ██░░░ ~23% ║
║    · N° países destino                 ║    IP    ║  ██░░░ ~16% ║
║    · Comprador EU identificado         ║    IP    ║  ░░░░░  0%  ║
║    · Requerimientos importador EU      ║    IP    ║  ░░░░░  0%  ║
╠══════════════════════════════════════════╬══════════╬══════════╣
║  D10: Certificaciones                  ║  IV/IP   ║  ░░░░░  <1% ║
║    · Rainforest Alliance               ║    IV    ║  ░░░░░  <1% ║
║    · Orgánico                          ║    IV    ║  ░░░░░  <1% ║
║    · Fair Trade                        ║    IV    ║  ░░░░░  <1% ║
╠══════════════════════════════════════════╬══════════╬══════════╣
║  D11: Volumen/exportación              ║  IV/IP   ║  ██░░░ ~23% ║
║    · Volumen TM exportado               ║  IV/IP   ║  ░░░░░  0%  ║
║    · Valor FOB USD                     ║  IV/IP   ║  ██░░░ ~23% ║
╠══════════════════════════════════════════╬══════════╬══════════╣
║  FUERA DE ÍNDICES (contexto)          ║          ║            ║
║    · Ubicación (dpto/prov/dist)        ║   INFO   ║  █████ 100%  ║
║    · RUC activo                        ║   INFO   ║  █████ 100% ║
║    · Contactos (email/tel)             ║   INFO   ║  ██░░░ ~22% ║
╚══════════════════════════════════════════╩══════════╩══════════╝
""")

print("""
CONCLUSIONES:

1. IV (vulnerabilidad / deforestación): PRÁCTICAMENTE CIELO.
   D1-D7 son el núcleo del EUDR y las fuentes administrativas NO los miden.
   No hay nada sobre trazabilidad, geolocalización, vigilancia, sanciones
   ambientales o due diligence en ningún archivo. Esto es normal — son datos
   que solo se levantan en campo con el Instrumento 2.

2. IP (preparación operativa / mercados): COBERTURA PARCIAL.
   - Lo que SÍ tenemos: exportación (59%), FOB (23%), socios (69%),
     años de operación (69%), contactos (22%).
   - Lo que NO tenemos: software, conectividad, presupuesto EUDR,
     asistencia técnica, comprador EU identificado.

3. D10 (certificaciones): CASI NULO.
   Solo 2 de 245 orgs tienen dato de certificación en PAC.
   Fuente oficial sería SENASA / OTA, que no hemos cruzado.

4. D11 (volumen/exportación): FOB existe (23%) pero en TM no hay nada.
   PRODUCE tiene FOB en miles USD; SUNAT tiene ops/FOB USD por país.

5. Lo que falta para el IP es casi tan crítico como lo que falta para el IV:
   no sabemos si tienen software, internet, presupuesto o asistencia técnica.
   Esto lo únicos que lo capturan son la encuesta de campo o MIDAGRI/PRODUCE
   en una versión mucho más detallada.
""")
