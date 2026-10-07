"""
EDA EUDR — Cooperativas Café Perú
3 archivos:
  1. Directorio PAC Café 2018-2025  (673 orgs)
  2. Directorio PAC Mango/Banano    (6 orgs)
  3. Perfil Cooperativas Café San Martín — Instrumento EUDR (25 orgs)
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import warnings, os, re
from datetime import datetime

warnings.filterwarnings('ignore')
OUT = r'C:\Users\acuba\eudrperu\eda_output'
os.makedirs(OUT, exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def clean_col(c, i):
    """Convierte valor de celda header a string limpio."""
    if c is None or (isinstance(c, float) and np.isnan(c)):
        return f'_EMPTY_{i}'
    s = str(c).strip()
    s = re.sub(r'\s+', ' ', s)
    if s in ('', 'nan', 'None'):
        return f'_EMPTY_{i}'
    return s

def safe_col_search(df, *keywords):
    """Busca columna por palabra clave (case-insensitive). Retorna None si no existe."""
    for kw in keywords:
        kw_lower = kw.lower()
        for c in df.columns:
            if kw_lower in str(c).lower():
                return c
    return None

def num(v, fallback=0.0):
    try:
        return float(v)
    except:
        return fallback

def to_numeric_series(series):
    return pd.to_numeric(
        series.replace(['#REF!', '#DIV/0!', '#N/A', ''], np.nan)
              .replace('nan', np.nan), errors='coerce')

# ─────────────────────────────────────────────────────────────────────────────
# 1. CARGA DE ARCHIVOS
# ─────────────────────────────────────────────────────────────────────────────

BASE = r'C:\Users\acuba\.minimax\v2\assets\2026\09\17'
files = sorted([f for f in os.listdir(BASE)
                if f.endswith('.xlsx') and 'asset.json' not in f])
f1, f2, f3 = [os.path.join(BASE, f) for f in files]
print("Archivos:", [os.path.basename(f) for f in [f1, f2, f3]])

# ── Archivo 1: Directorio PAC Café ─────────────────────────────────────────
df1_raw = pd.read_excel(f1, sheet_name='Hoja1', header=None)
hdr1 = [clean_col(c, i) for i, c in enumerate(df1_raw.iloc[3])]
df1 = df1_raw.iloc[4:].copy()
df1.columns = hdr1
df1 = df1.reset_index(drop=True)
# Eliminar filas donde la primera columna es NaN o es el propio header
first = df1.columns[0]
df1 = df1[df1[first].notna() & (df1[first] != 'Nombre de la Organización')]
df1 = df1.reset_index(drop=True)
print(f"Archivo 1 limpio: {df1.shape}")

# ── Archivo 2: Mango/Banano ────────────────────────────────────────────────
df2_raw = pd.read_excel(f2, sheet_name='Hoja2', header=None)
hdr2 = [clean_col(c, i) for i, c in enumerate(df2_raw.iloc[1])]
df2 = df2_raw.iloc[2:].copy()
df2.columns = hdr2
df2 = df2.reset_index(drop=True)
first2 = df2.columns[0]
df2 = df2[df2[first2].notna() & (df2[first2] != 'Nombre de la Organización')]
df2 = df2.reset_index(drop=True)
print(f"Archivo 2 limpio: {df2.shape}")

# ── Archivo 3: Perfil Cooperativas San Martín ───────────────────────────────
df3_raw = pd.read_excel(f3, sheet_name='Hoja 1', header=None)
hdr3 = [clean_col(c, i) for i, c in enumerate(df3_raw.iloc[0])]
df3 = df3_raw.iloc[1:].copy()
df3.columns = hdr3
df3 = df3.reset_index(drop=True)
df3 = df3[df3.iloc[:, 0].notna()]
df3 = df3.reset_index(drop=True)
print(f"Archivo 3 limpio: {df3.shape}")

# ─────────────────────────────────────────────────────────────────────────────
# 2. CALIDAD DE DATOS
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*60)
print("CALIDAD DE DATOS")
print("="*60)
for name, df in [("Directorio PAC Café", df1),
                  ("Directorio Mango/Banano", df2),
                  ("Perfil San Martín", df3)]:
    tot = df.shape[0]*df.shape[1]
    nulls = df.isnull().sum().sum()
    fill = 1 - nulls/tot
    empties = sum(1 for c in df.columns if c.startswith('_EMPTY'))
    print(f"\n{name}")
    print(f"  {df.shape[0]} orgs × {df.shape[1]} cols | Llenado: {fill:.1%} | Vacías: {empties}")

# ─────────────────────────────────────────────────────────────────────────────
# 3. ANÁLISIS — ARCHIVO 1 (Directorio PAC Café)
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*60)
print("ANÁLISIS: Archivo 1 — Directorio PAC Café")
print("="*60)

# ── 3a. Variables clave
col_org   = safe_col_search(df1, 'Nombre de la Organización')
col_dep   = safe_col_search(df1, 'DEPARTAMENTO')
col_prod  = safe_col_search(df1, 'PRODUCTO 1')
col_tipo  = safe_col_search(df1, 'Tipo de Organización')
col_serv  = safe_col_search(df1, 'SERVICIO')
col_ruc   = safe_col_search(df1, 'RUC')
col_sunat = safe_col_search(df1, 'NOMBRE SUNAT')
print(f"  columnas: org={col_org}, dep={col_dep}, prod={col_prod}, tipo={col_tipo}")

# ── 3b. Departamentos
dep_dist = df1[col_dep].value_counts()
print(f"\n  Departamentos ({len(dep_dist)}):")
for d, n in dep_dist.head(8).items():
    print(f"    {d}: {n}")

# ── 3c. Productos
prod_dist = df1[col_prod].value_counts()
print(f"\n  Productos ({len(prod_dist)}):")
for p, n in prod_dist.head(8).items():
    print(f"    {p}: {n}")

# ── 3d. Tipo de organización
tipo_dist = df1[col_tipo].value_counts()
print(f"\n  Tipos de organización:")
for t, n in tipo_dist.items():
    print(f"    {t}: {n}")

# ── 3e. Ventas por año
sale_year_cols = {}
for yr in [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]:
    for c in df1.columns:
        s = str(c)
        if str(yr) in s and ('TOTAL' in s.upper() or 'VENTAS TOTALES' in s.upper()) and 'INCREMENTO' not in s.upper():
            sale_year_cols[yr] = c
            break

print(f"\n  Ventas por año detectadas:")
sale_totals = {}
for yr, col in sale_year_cols.items():
    vals = to_numeric_series(df1[col])
    total = vals.sum()
    sale_totals[yr] = total
    print(f"    {yr}: S/ {total:>18,.0f}  ({vals.notna().sum()} orgs con dato)")

# ── 3f. Beneficiarios por año
ben_year_cols = {}
for yr in [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]:
    for c in df1.columns:
        s = str(c)
        if str(yr) in s and 'TOTAL' in s.upper() and 'BENF' in s.upper():
            ben_year_cols[yr] = c
            break

print(f"\n  Beneficiarios por año:")
ben_totals = {}
for yr, col in ben_year_cols.items():
    vals = to_numeric_series(df1[col])
    ben_totals[yr] = vals.sum()
    print(f"    {yr}: {vals.sum():>8,.0f}  ({vals.notna().sum()} orgs con dato)")

# ─────────────────────────────────────────────────────────────────────────────
# 4. ANÁLISIS — ARCHIVO 3 (Perfil Cooperativas San Martín)
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*60)
print("ANÁLISIS: Archivo 3 — Perfil Cooperativas Café San Martín")
print("="*60)

# ── 4a. Columnas clave
col_n       = safe_col_search(df3, 'N°')
col_org3    = safe_col_search(df3, 'Organización', 'organizacion', 'Organizacion')
col_region3 = safe_col_search(df3, 'Región', 'Region')
col_prov3   = safe_col_search(df3, 'Provincia', 'provincia')
col_dist3   = safe_col_search(df3, 'Distrito', 'distrito')
col_prod3   = safe_col_search(df3, 'volumen', 'producción', 'quintales')
col_sociom  = safe_col_search(df3, 'socios', 'varones', 'varon')
col_sociof  = safe_col_search(df3, 'mujeres', 'socias')
col_hect    = safe_col_search(df3, 'hectareas', 'hectárea', 'HAS')
col_cert_or = safe_col_search(df3, 'orgánica', 'organica')
col_cert_ft = safe_col_search(df3, 'comercio justo', 'fair trade', 'fairtrade')
col_cert_ra = safe_col_search(df3, 'rainforest', 'rain forest')
col_eudr    = safe_col_search(df3, 'eudr')
col_exporta  = safe_col_search(df3, 'exporta')
col_fob     = safe_col_search(df3, 'fob')
col_etapa   = safe_col_search(df3, 'etapa')
col_sacos   = safe_col_search(df3, 'sacos', 'contenedores')
col_dest    = safe_col_search(df3, 'destinos', 'destino')
col_alt     = safe_col_search(df3, 'altitud', 'm.s.n.m', 'msnm')
col_calidad = safe_col_search(df3, 'grado', 'defectos', 'calidad')
col_ruc3    = safe_col_search(df3, 'RUC', 'ruc')
col_gerente = safe_col_search(df3, 'gerente', 'gerente general')
col_email   = safe_col_search(df3, 'correo', 'email')
col_ruc3    = col_ruc3 or safe_col_search(df3, 'RUC')
col_sunat3  = safe_col_search(df3, 'SUNAT', 'status', 'activo')
col_marca   = safe_col_search(df3, 'marca', 'Marca')
col_regsan  = safe_col_search(df3, 'registro sanitario')

print(f"\n  Vars: org={col_org3}, prod={col_prod3}, socios_m={col_sociom}, "
      f"socios_f={col_sociof}, hect={col_hect}")
print(f"         eudr={col_eudr}, exporta={col_exporta}, fob={col_fob}, etapa={col_etapa}")
print(f"         cert_org={col_cert_or}, cert_ft={col_cert_ft}, cert_ra={col_cert_ra}")

# ── 4b. Estadísticas numéricas
stats = {}
for name, col in [('Socios varones', col_sociom),
                   ('Socias mujeres', col_sociof),
                   ('Hectáreas', col_hect),
                   ('Volumen (qq)', col_prod3),
                   ('FOB USD', col_fob),
                   ('Sacos 69kg', col_sacos)]:
    if col:
        vals = pd.to_numeric(df3[col].astype(str).str.replace(',','').str.strip(),
                             errors='coerce').dropna()
        if len(vals):
            stats[name] = vals
            print(f"\n  {name}:")
            print(f"    N={len(vals)} | Media={vals.mean():,.1f} | Med={vals.median():,.1f} "
                  f"| Mín={vals.min():,.1f} | Máx={vals.max():,.1f} | Suma={vals.sum():,.0f}")

# ── 4c. Certificaciones
print(f"\n  Certificaciones vigentes (de {len(df3)} orgs):")
for name, col in [('Orgánica', col_cert_or),
                   ('Fair Trade', col_cert_ft),
                   ('Rainforest Alliance', col_cert_ra)]:
    if col:
        cnt = df3[col].astype(str).str.strip().str.lower().isin(
            ['si', 'sí', 'x', '1', 'true', 'check']).sum()
        cnt = df3[col].notna().sum()
        print(f"    {name}: {cnt} ({cnt/len(df3):.0%})")

# ── 4d. EUDR
print(f"\n  Avance EUDR:")
if col_eudr:
    eudr_vals = pd.to_numeric(df3[col_eudr].astype(str).str.strip(), errors='coerce')
    valid = eudr_vals.notna()
    print(f"    N con dato: {valid.sum()}/{len(df3)}")
    print(f"    Distribución: {eudr_vals.value_counts().to_dict()}")
    print(f"    Promedio: {eudr_vals.mean():.2f}")
else:
    print("    (no encontrada)")

# ── 4e. Exportaciones
print(f"\n  Exportaciones:")
if col_exporta:
    exp_si = df3[col_exporta].astype(str).str.upper().str.contains('SI').sum()
    print(f"    Exporta: {exp_si}/{len(df3)} ({exp_si/len(df3):.0%})")
if col_dest:
    all_dest = []
    for d in df3[col_dest].dropna():
        for p in str(d).split(','):
            p = p.strip()
            if p:
                all_dest.append(p)
    dest_cnt = pd.Series(all_dest).value_counts()
    print(f"\n  Mercados de destino ({len(dest_cnt)}):")
    for d, n in dest_cnt.head(10).items():
        print(f"    {d}: {n}")

# ── 4f. Provincias y organizaciones
print(f"\n  Provincias:")
if col_prov3:
    print(f"    {df3[col_prov3].value_counts().to_dict()}")
if col_org3:
    print(f"\n  Organizaciones ({len(df3)}):")
    for i, row in df3.head(10).iterrows():
        org = str(row[col_org3])[:50] if col_org3 else '(sin nombre)'
        prod_v = ''
        if col_prod3:
            prod_v = f"| vol={row[col_prod3]}"
        print(f"    {i+1}. {org}{prod_v}")

# ── 4g. RUCs y estado SUNAT
print(f"\n  Estado SUNAT:")
if col_sunat3:
    sunat_dist = df3[col_sunat3].value_counts()
    print(f"    {sunat_dist.to_dict()}")
if col_ruc3:
    ruc_vals = df3[col_ruc3].astype(str).str.strip()
    ruc_valid = ruc_vals.str.match(r'^\d{11}$')
    print(f"    RUCs válidos (11 dígitos): {ruc_valid.sum()}/{len(df3)}")

# ── 4h. Marcas y registro sanitario
if col_marca:
    marcas = df3[col_marca].dropna().astype(str).str.strip()
    marcas = marcas[marcas != 'nan']
    print(f"\n  Marcas: {marcas.tolist()}")
if col_regsan:
    rs = df3[col_regsan].dropna().astype(str).str.strip()
    rs = rs[rs != 'nan']
    print(f"  Registro Sanitario: {rs.tolist()}")

# ─────────────────────────────────────────────────────────────────────────────
# 5. VISUALIZACIONES
# ─────────────────────────────────────────────────────────────────────────────

plt.rcParams.update({
    'figure.facecolor': '#F8F9FA', 'axes.facecolor': '#FFFFFF',
    'axes.grid': True, 'grid.alpha': 0.3,
    'font.family': 'DejaVu Sans', 'font.size': 10,
})
PAL = ['#2D6A4F','#40916C','#74C69D','#B7E4C7','#D8F3DC','#D4A373','#CCD5AE']

def sfig(fig, name):
    path = os.path.join(OUT, f'{name}.png')
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='#F8F9FA')
    plt.close(fig)
    print(f"  ✓ {name}")

# ── V1: Deptos (A1)
if col_dep:
    fig, ax = plt.subplots(figsize=(11, 6))
    dep_dist.head(15).plot(kind='barh', ax=ax, color='#2D6A4F', edgecolor='white')
    ax.set_title('Archivo 1 — Organizaciones PAC por Departamento\nDirectorio Café 2018–2025',
                 fontsize=13, fontweight='bold')
    ax.set_xlabel('N° de organizaciones')
    ax.invert_yaxis()
    for i, v in enumerate(dep_dist.head(15)):
        ax.text(v + 0.3, i, str(v), va='center', fontsize=9)
    sfig(fig, 'v01_deptos_pac')

# ── V2: Tipos org (A1)
if col_tipo:
    fig, ax = plt.subplots(figsize=(8, 4))
    tipo_dist.head(6).plot(kind='bar', ax=ax, color='#40916C', edgecolor='white')
    ax.set_title('Archivo 1 — Tipo de Organización', fontsize=12, fontweight='bold')
    ax.set_ylabel('Conteo')
    plt.xticks(rotation=25, ha='right')
    for i, v in enumerate(tipo_dist.head(6)):
        ax.text(i, v + 1, str(v), ha='center', fontsize=9)
    sfig(fig, 'v02_tipos_org')

# ── V3: Ventas anuales (A1)
if sale_totals:
    fig, ax = plt.subplots(figsize=(11, 4))
    years_s = sorted(sale_totals.keys())
    vals_s  = [sale_totals[y] for y in years_s]
    bars = ax.bar([str(y) for y in years_s], vals_s, color='#2D6A4F', edgecolor='white')
    ax.set_title('Archivo 1 — Ventas Totales por Año (S/)\nDirectorio PAC Café',
                 fontsize=12, fontweight='bold')
    ax.set_ylabel('Soles (suma)')
    ax.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: f'{x/1e6:.1f}M' if x >= 1e6 else f'{x/1e3:.0f}K'))
    for bar, val in zip(bars, vals_s):
        label = f'{val/1e6:.1f}M' if val >= 1e6 else f'{val/1e3:.0f}K'
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+max(vals_s)*0.01,
                label, ha='center', fontsize=8)
    sfig(fig, 'v03_ventas_anuales')

# ── V4: Beneficiarios anuales (A1)
if ben_totals:
    fig, ax = plt.subplots(figsize=(11, 4))
    years_b = sorted(ben_totals.keys())
    vals_b  = [ben_totals[y] for y in years_b]
    ax.bar([str(y) for y in years_b], vals_b, color='#74C69D', edgecolor='white')
    ax.set_title('Archivo 1 — Beneficiarios Totales por Año\nDirectorio PAC Café',
                 fontsize=12, fontweight='bold')
    ax.set_ylabel('N° beneficiarios')
    ax.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: f'{x/1e3:.0f}K' if x >= 1e3 else f'{x:.0f}'))
    sfig(fig, 'v04_beneficiarios')

# ── V5: Productos (A1)
if col_prod:
    fig, ax = plt.subplots(figsize=(8, 4))
    prod_dist.head(8).plot(kind='bar', ax=ax, color='#40916C', edgecolor='white')
    ax.set_title('Archivo 1 — Productos Principales\nDirectorio PAC Café', fontsize=12, fontweight='bold')
    ax.set_ylabel('N° organizaciones')
    plt.xticks(rotation=25, ha='right')
    sfig(fig, 'v05_productos')

# ── V6: Heatmap deptos × productos (A1)
if col_dep and col_prod:
    ct = pd.crosstab(df1[col_dep], df1[col_prod])
    ct_top = ct.loc[ct.sum(axis=1).nlargest(12).index, ct.sum(axis=0).nlargest(6).index]
    fig, ax = plt.subplots(figsize=(9, 7))
    sns.heatmap(ct_top, annot=True, fmt='d', cmap='Greens', ax=ax,
                linewidths=0.5, cbar_kws={'label': 'N° orgs'})
    ax.set_title('Archivo 1 — Productos por Departamento\n(Deptos y productos principales)',
                 fontsize=11, fontweight='bold')
    sfig(fig, 'v06_heatmap_prod_dept')

# ── V7: Socios varones vs mujeres (A3)
if col_sociom and col_sociof:
    sm = pd.to_numeric(df3[col_sociom].astype(str).str.replace(',','').str.strip(),
                        errors='coerce').dropna()
    sf = pd.to_numeric(df3[col_sociof].astype(str).str.replace(',','').str.strip(),
                        errors='coerce').dropna()
    fig, axes = plt.subplots(1, 2, figsize=(13, 4))
    axes[0].hist(sm, bins=12, color='#2D6A4F', edgecolor='white', alpha=0.85)
    axes[0].set_title('Socios Varones')
    axes[0].set_xlabel('N° socios'); axes[0].set_ylabel('Frecuencia')
    axes[1].hist(sf, bins=12, color='#D4A373', edgecolor='white', alpha=0.85)
    axes[1].set_title('Socias Mujeres')
    axes[1].set_xlabel('N° socias')
    fig.suptitle('Archivo 3 — Distribución de Socios (San Martín, 25 cooperativas)',
                 fontsize=12, fontweight='bold')
    sfig(fig, 'v07_socios_dist')

# ── V8: Hectáreas vs Volumen (A3)
if col_hect and col_prod3:
    h = pd.to_numeric(df3[col_hect].astype(str).str.replace(',','').str.strip(),
                       errors='coerce')
    p = pd.to_numeric(df3[col_prod3].astype(str).str.replace(',','').str.strip(),
                       errors='coerce')
    v = ~(h.isna() | p.isna() | (h == 0) | (p == 0))
    if v.sum() > 2:
        fig, ax = plt.subplots(figsize=(9, 6))
        ax.scatter(h[v], p[v], c='#2D6A4F', alpha=0.75, s=90, edgecolors='white')
        z = np.polyfit(h[v].values, p[v].values, 1)
        p1 = np.poly1d(z)
        x_l = np.linspace(h[v].min(), h[v].max(), 100)
        ax.plot(x_l, p1(x_l), '--', color='#D4A373', label=f'Tendencia (r={np.corrcoef(h[v],p[v])[0,1]:.2f})')
        ax.set_xlabel('Hectáreas totales')
        ax.set_ylabel('Volumen producción 2026 (qq)')
        ax.set_title('Archivo 3 — Hectáreas vs Volumen de Producción\nCooperativas San Martín',
                      fontsize=11, fontweight='bold')
        ax.legend()
        sfig(fig, 'v08_hect_vs_volumen')

# ── V9: Certificaciones (A3)
if col_cert_or or col_cert_ft or col_cert_ra:
    certs = {}
    for name, col in [('Orgánica', col_cert_or),
                       ('Fair Trade', col_cert_ft),
                       ('Rainforest Alliance', col_cert_ra)]:
        if col:
            certs[name] = df3[col].notna().sum()
    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(certs.keys(), certs.values(), color=['#2D6A4F','#40916C','#74C69D'],
                  edgecolor='white')
    ax.set_title('Archivo 3 — Certificaciones Vigentes\n(25 Cooperativas San Martín)',
                 fontsize=12, fontweight='bold')
    ax.set_ylabel('N° cooperativas')
    for bar, (name, val) in zip(bars, certs.items()):
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.1,
                f'{val}\n({val/len(df3):.0%})', ha='center', fontsize=10)
    ax.set_ylim(0, max(certs.values())*1.35)
    sfig(fig, 'v09_certificaciones')

# ── V10: FOB Exportaciones (A3)
if col_fob:
    fob = pd.to_numeric(df3[col_fob].astype(str).str.replace(',','').str.strip(),
                         errors='coerce').dropna()
    if len(fob):
        fig, ax = plt.subplots(figsize=(10, 5))
        idx = fob.sort_values().index
        org_names = [str(df3.loc[i, col_org3])[:35] if col_org3 else f'Org {i}'
                     for i in idx]
        ax.barh(range(len(fob)), fob.sort_values().values, color='#2D6A4F',
                edgecolor='white', height=0.7)
        ax.set_yticks(range(len(org_names)))
        ax.set_yticklabels(org_names, fontsize=8)
        ax.xaxis.set_major_formatter(
            plt.FuncFormatter(lambda x, _: f'${x/1e6:.2f}M' if x >= 1e6 else f'${x/1e3:.0f}K'))
        ax.set_title('Archivo 3 — Exportaciones FOB 2025 por Cooperativa\n(USD, San Martín)',
                     fontsize=11, fontweight='bold')
        ax.set_xlabel('FOB USD')
        sfig(fig, 'v10_fob_exportaciones')

# ── V11: Mercados destino (A3)
if col_dest:
    all_dest = []
    for d in df3[col_dest].dropna():
        for p in str(d).split(','):
            p = p.strip()
            if p:
                all_dest.append(p)
    dest_cnt = pd.Series(all_dest).value_counts().head(12)
    fig, ax = plt.subplots(figsize=(9, 5))
    dest_cnt.plot(kind='barh', ax=ax, color='#2D6A4F')
    ax.set_title('Archivo 3 — Mercados de Destino\n(Cooperativas San Martín)',
                 fontsize=11, fontweight='bold')
    ax.set_xlabel('Frecuencia')
    ax.invert_yaxis()
    sfig(fig, 'v11_destinos')

# ── V12: Avance EUDR (A3)
if col_eudr:
    eudr_num = pd.to_numeric(df3[col_eudr].astype(str).str.strip(), errors='coerce')
    bins = ['0 (Ninguno)', '0.1–0.4 (Inicial)', '0.5–0.7 (En progreso)', '0.8–1.0 (Avanzado)']
    cuts = pd.cut(eudr_num, bins=[-0.01, 0, 0.4, 0.7, 1.01], labels=bins)
    fig, ax = plt.subplots(figsize=(8, 4))
    cuts.value_counts().reindex(bins).plot(kind='barh', ax=ax,
       color=['#C1121F','#E85D04','#F9C74F','#2D6A4F'])
    ax.set_title('Archivo 3 — Nivel de Avance EUDR\n(0=Ninguno, 1=Completo, San Martín)',
                 fontsize=11, fontweight='bold')
    ax.set_xlabel('N° cooperativas')
    sfig(fig, 'v12_eudr_avance')

# ─────────────────────────────────────────────────────────────────────────────
# 6. INFORME MARKDOWN
# ─────────────────────────────────────────────────────────────────────────────

n1_v = len([y for y in sale_totals.values() if y > 0])
n1_b = len([y for y in ben_totals.values() if y > 0])
total_fob = 0
if col_fob:
    total_fob = pd.to_numeric(df3[col_fob].astype(str).str.replace(',','').str.strip(),
                                errors='coerce').sum()

report = f"""# EDA EUDR — Cooperativas Café Perú
*Generado: {datetime.now().strftime('%Y-%m-%d %H:%M')} · Proyecto eudrperu*

---

## 1. Resumen de Datos

| Archivo | Descripción | Registros | Columnas | Tasa Llenado |
|---------|-------------|-----------|----------|-------------|
| 1 | Directorio PAC Café 2018–2025 | {df1.shape[0]} | {df1.shape[1]} | ~84% |
| 2 | Directorio PAC Mango/Banano | {df2.shape[0]} | {df2.shape[1]} | ~86% |
| 3 | Perfil Cooperativas San Martín (EUDR) | {df3.shape[0]} | {df3.shape[1]} | ~87% |

---

## 2. Hallazgos Clave

### Archivo 1 — Directorio PAC Café ({df1.shape[0]} organizaciones)

**Cobertura geográfica:** {len(dep_dist)} departamentos. Los 5 principales son:
{chr(10).join(f'- **{d}**: {n} orgs' for d, n in dep_dist.head(5).items())}

**Productos:** {len(prod_dist)} categorías detectadas. Principales:
{chr(10).join(f'- **{p}**: {n} orgs' for p, n in prod_dist.head(4).items())}

**Tipos de organización:**
{chr(10).join(f'- **{t}**: {n}' for t, n in tipo_dist.items())}

**Ventas acumuladas 2018–2025:** S/ {sum(sale_totals.values()):,.0f} en {n1_v} años con dato.
- El año con mayor venta agregada: {max(sale_totals, key=sale_totals.get)} (S/ {max(sale_totals.values()):,.0f})
- NOTA: varias celdas contienen `#REF!` (fórmulas Excel rotas al exportar) — estos valores están excluidos.

**Beneficiarios acumulados:** ~{sum(ben_totals.values()):,.0f} en {n1_b} años con dato.

---

### Archivo 3 — Perfil Cooperativas San Martín ({df3.shape[0]} organizaciones)

**Escala:** ~{int(pd.to_numeric(df3[col_sociom].astype(str).str.replace(',','').str.strip(), errors='coerce').sum()):,} socios varones + ~{int(pd.to_numeric(df3[col_sociof].astype(str).str.replace(',','').str.strip(), errors='coerce').sum()):,} socias = ~{int(pd.to_numeric(df3[col_sociom].astype(str).str.replace(',','').str.strip(), errors='coerce').sum())+int(pd.to_numeric(df3[col_sociof].astype(str).str.replace(',','').str.strip(), errors='coerce').sum()):,} productores en {len(df3)} cooperativas.

**Superficie:** ~{pd.to_numeric(df3[col_hect].astype(str).str.replace(',','').str.strip(), errors='coerce').sum():,.0f} hectáreas total.

**Volumen cosecha 2026:** ~{pd.to_numeric(df3[col_prod3].astype(str).str.replace(',','').str.strip(), errors='coerce').sum():,.0f} qq de café verde estimado.

**Exportaciones FOB 2025:** ${total_fob:,.0f} USD
- Tasa de exportación: {exp_si}/{len(df3)} ({exp_si/len(df3):.0%})

**Certificaciones vigentes (de {len(df3)} orgs):**
{chr(10).join(f'- **{name}**: {df3[col].notna().sum()} ({df3[col].notna().sum()/len(df3):.0%})' for name, col in [('Orgánica', col_cert_or), ('Fair Trade', col_cert_ft), ('Rainforest Alliance', col_cert_ra)] if col)}

**Mercados de destino:** {', '.join(dest_cnt.head(5).index.tolist())}

**EUDR:** {valid.sum()} de {len(df3)} cooperativas registran avance EUDR. Promedio: {eudr_vals.mean():.2f}/1.0

---

## 3. Problemas de Calidad de Datos

1. **Archivo 1 — Celdas `#REF!`:** Fórmulas Excel que referencian celdas movidas/eliminadas. Afectan columnas de ventas incrementales. Se recomienda recalcular o reimportar desde la fuente.
2. **Archivo 1 — Headers multilínea:** Las columnas de beneficiarios están en filas de encabezado intermedias (merge vertical de celdas), lo que requiere lógica de limpieza especial.
3. **Archivo 2 — Solo 6 registros:** El directorio mango/banano está casi vacío. Útil como muestra piloto pero no representativo.
4. **Archivo 3 — Texto libre mezclado:** Las columnas de certificaciones, calidad y EUDR contienen texto narrativo, no valores estructurados. Se requiere procesamiento de texto (NLP) para extraer datos estructurados.
5. **Archivo 3 — Formatos numéricos inconsistentes:** Algunos campos numéricos usan comas como separadores de miles (estilo peruano). Se limpian correctamente en el análisis pero indican inconsistencia en la fuente.

---

## 4. Visualizaciones Generadas

| # | Gráfico | Archivo fuente |
|---|---------|---------------|
| v01 | Deptos PAC | A1 |
| v02 | Tipos organización | A1 |
| v03 | Ventas anuales | A1 |
| v04 | Beneficiarios anuales | A1 |
| v05 | Productos principales | A1 |
| v06 | Heatmap productos × deptos | A1 |
| v07 | Distribución socios | A3 |
| v08 | Hectáreas vs volumen | A3 |
| v09 | Certificaciones | A3 |
| v10 | FOB exportaciones | A3 |
| v11 | Mercados destino | A3 |
| v12 | Avance EUDR | A3 |
"""

with open(os.path.join(OUT, 'EDA_EUDR_hallazgos.md'), 'w', encoding='utf-8') as f:
    f.write(report)

print(f"\n✓ Informe: {os.path.join(OUT,'EDA_EUDR_hallazgos.md')}")
print(f"✓ Gráficos: {OUT}/")
