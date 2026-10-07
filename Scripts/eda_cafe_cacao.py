"""
EDA Café y Cacao — Proyecto EUDRPERU
Universo: organizaciones PAC con productos CAFÉ o CACAO
+ perfil San Martín (Archivo 3, 100% café)
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
OUT = r'C:\Users\acuba\eudrperu\eda_output_cc'
os.makedirs(OUT, exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def clean_col(c, i):
    if c is None or (isinstance(c, float) and np.isnan(c)):
        return f'_E{i}'
    s = re.sub(r'\s+', ' ', str(c).strip())
    return s if s not in ('', 'nan', 'None') else f'_E{i}'

def to_num(series):
    return pd.to_numeric(
        series.astype(str)
              .str.replace('#REF!', '').str.replace(',', '').str.strip()
              .replace(['', 'nan', 'None', '#DIV/0!'], np.nan),
        errors='coerce')

def fmt(v, dec=1):
    if v >= 1e6:   return f'{v/1e6:.{dec}f}M'
    if v >= 1e3:    return f'{v/1e3:.{dec}f}K'
    return f'{v:.{dec}f}'

def pie_labels(ax, vals, total=None):
    for i, (patch, val) in enumerate(zip(ax.patches, vals)):
        pct = val / sum(vals) * 100
        ang = (patch.theta2 + patch.theta1) / 2
        x = 1.4 * np.cos(np.radians(ang))
        y = 1.4 * np.sin(np.radians(ang))
        ax.annotate(f'{val} ({pct:.0f}%)', xy=(x * 0.6, y * 0.6),
                    ha='center', va='center', fontsize=9, fontweight='bold',
                    color='white' if pct > 10 else '#374151')

def sfig(fig, name):
    fig.savefig(os.path.join(OUT, f'{name}.png'), dpi=150, bbox_inches='tight',
                facecolor='#F8F9FA')
    plt.close(fig)
    print(f"  ✓ {name}")

# ─────────────────────────────────────────────────────────────────────────────
# 1. CARGA
# ─────────────────────────────────────────────────────────────────────────────

BASE = r'C:\Users\acuba\.minimax\v2\assets\2026\09\17'
files = sorted([f for f in os.listdir(BASE) if f.endswith('.xlsx') and 'asset.json' not in f])
f1, f2, f3 = [os.path.join(BASE, f) for f in files]

# --- Archivo 1 (PAC Café 2018-2025) ---
raw1 = pd.read_excel(f1, sheet_name='Hoja1', header=None)
hdr1 = [clean_col(c, i) for i, c in enumerate(raw1.iloc[3])]
df1  = raw1.iloc[4:].copy()
df1.columns = hdr1
df1 = df1.reset_index(drop=True)
df1 = df1[df1.iloc[:, 0].notna()].reset_index(drop=True)

# --- Archivo 3 (Perfil San Martín) ---
raw3 = pd.read_excel(f3, sheet_name='Hoja 1', header=None)
hdr3 = [clean_col(c, i) for i, c in enumerate(raw3.iloc[0])]
df3  = raw3.iloc[1:].copy()
df3.columns = hdr3
df3 = df3.reset_index(drop=True)
df3 = df3[df3.iloc[:, 0].notna()].reset_index(drop=True)

print(f"A1 total orgs: {len(df1)} | A3: {len(df3)}")

# ─────────────────────────────────────────────────────────────────────────────
# 2. IDENTIFICAR CAFÉ / CACAO
# ─────────────────────────────────────────────────────────────────────────────

col_prod = [c for c in df1.columns if 'PRODUCTO' in str(c).upper() and 'DOM' not in str(c).upper()][0]
all_prods = df1[col_prod].astype(str).str.strip().str.lower()

CAFE_PATTERNS = ['cafe', 'café', 'cafe verde', 'cafe pergamino']
CACAO_PATTERNS = ['cacao', 'cacao en grano']

def is_cafe(row):   return any(p in str(row).lower() for p in CAFE_PATTERNS)
def is_cacao(row):  return any(p in str(row).lower() for p in CACAO_PATTERNS)

mask_cafe  = df1[col_prod].astype(str).apply(is_cafe)
mask_cacao = df1[col_prod].astype(str).apply(is_cacao)

df_cafe  = df1[mask_cafe].copy()
df_cacao = df1[mask_cacao].copy()
df_cc    = df1[mask_cafe | mask_cacao].copy()   # universo completo café+cacao

print(f"  Café:   {len(df_cafe)} orgs")
print(f"  Cacao:  {len(df_cacao)} orgs")
print(f"  Union:  {len(df_cc)} orgs  ( cafés: {mask_cafe.sum()}, cacaos: {mask_cacao.sum()})")

# ─────────────────────────────────────────────────────────────────────────────
# 3. CALIDAD DE DATOS
# ─────────────────────────────────────────────────────────────────────────────

print("\nCALIDAD DE DATOS")
for name, df in [("Café (A1)", df_cafe), ("Cacao (A1)", df_cacao),
                  ("San Martín (A3)", df3)]:
    tot   = df.shape[0]*df.shape[1]
    nulls = df.isnull().sum().sum()
    print(f"  {name}: {df.shape[0]} orgs | Llenado {1-nulls/tot:.1%}")

# ─────────────────────────────────────────────────────────────────────────────
# 4. ANÁLISIS — A1: CAFÉ
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*60)
print("ANÁLISIS A1 — CAFÉ")
print("="*60)

col_dep  = [c for c in df_cafe.columns if 'DEPARTAMENTO' in str(c).upper()][0]
col_prov = [c for c in df_cafe.columns if 'Provincia' in str(c)][0]
col_dist = [c for c in df_cafe.columns if 'Distrito' in str(c)][0]
col_tip  = [c for c in df_cafe.columns if 'Tipo de Organización' in str(c)][0]
col_serv = [c for c in df_cafe.columns if 'SERVICIO' in str(c).upper()][0]
col_ruc  = [c for c in df_cafe.columns if c == 'RUC'][0]

# Deptos
dept_cafe = df_cafe[col_dep].value_counts()
print(f"\nDepartamentos café: {len(dept_cafe)}")
for d, n in dept_cafe.head(10).items():
    print(f"  {d}: {n}")

# Provincias
prov_cafe = df_cafe[col_prov].value_counts().head(10)
print(f"\nProvincias top café: {prov_cafe.to_dict()}")

# Tipo org
tipo_cafe = df_cafe[col_tip].value_counts()
print(f"\nTipos: {tipo_cafe.to_dict()}")

# Servicio
serv_cafe = df_cafe[col_serv].value_counts()
print(f"\nServicios: {serv_cafe.to_dict()}")

# RUCs válidos
ruc_cafe = df_cafe[col_ruc].astype(str).str.strip()
ruc_ok_cafe = ruc_cafe.str.match(r'^\d{11}$')
print(f"\nRUCs café válidos (11 dígitos): {ruc_ok_cafe.sum()}/{len(df_cafe)}")

# ─────────────────────────────────────────────────────────────────────────────
# 5. ANÁLISIS — A1: CACAO
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*60)
print("ANÁLISIS A1 — CACAO")
print("="*60)

col_dep_d  = [c for c in df_cacao.columns if 'DEPARTAMENTO' in str(c).upper()][0]
col_prov_d = [c for c in df_cacao.columns if 'Provincia' in str(c)][0]
col_tip_d  = [c for c in df_cacao.columns if 'Tipo de Organización' in str(c)][0]
col_ruc_d  = [c for c in df_cacao.columns if c == 'RUC'][0]

dept_cacao = df_cacao[col_dep_d].value_counts()
print(f"\nDepartamentos cacao: {len(dept_cacao)}")
for d, n in dept_cacao.head(10).items():
    print(f"  {d}: {n}")

tipo_cacao = df_cacao[col_tip_d].value_counts()
print(f"\nTipos: {tipo_cacao.to_dict()}")

ruc_cacao = df_cacao[col_ruc_d].astype(str).str.strip()
ruc_ok_cacao = ruc_cacao.str.match(r'^\d{11}$')
print(f"\nRUCs cacao válidos: {ruc_ok_cacao.sum()}/{len(df_cacao)}")

# ─────────────────────────────────────────────────────────────────────────────
# 6. ANÁLISIS — A3: PERFIL SAN MARTÍN (café)
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*60)
print("ANÁLISIS A3 — PERFIL SAN MARTÍN (café)")
print("="*60)

def g3(*kws):
    for kw in kws:
        for c in df3.columns:
            if kw.lower() in c.lower():
                return c
    return None

col_n3     = g3('N°')
col_org3   = g3('Organización', 'organizacion')
col_prov3  = g3('Provincia', 'provincia')
col_sociom = g3('socios', 'varones', 'varon')
col_sociof = g3('mujeres', 'socias')
col_hect3  = g3('hectareas', 'hectárea', 'HAS')
col_vol3   = g3('volumen', 'producción', 'quintales')
col_cert_o = g3('orgánica', 'organica')
col_cert_f = g3('comercio justo', 'fair trade')
col_cert_r = g3('rainforest', 'rain forest')
col_eudr3  = g3('eudr')
col_exp3   = g3('exporta')
col_fob3   = g3('fob')
col_dest3  = g3('destinos', 'destino')
col_alt3   = g3('altitud', 'msnm', 'm.s.n.m')
col_cal3   = g3('grado', 'defectos', 'calidad')
col_etap3  = g3('etapa')
col_ruc3   = g3('RUC', 'ruc')
col_marca3 = g3('marca', 'Marca')
col_rsani3 = g3('registro sanitario')
col_email3 = g3('correo', 'email')

# Stats numéricas
for name, col in [
    ('Socios varones', col_sociom), ('Socias mujeres', col_sociof),
    ('Hectáreas', col_hect3), ('Volumen qq', col_vol3), ('FOB USD', col_fob3)]:
    if col:
        v = to_num(df3[col])
        v = v.dropna()
        if len(v):
            print(f"\n  {name}: N={len(v)} Med={v.median():,.0f} "
                  f"Media={v.mean():,.0f} Mín={v.min():,.0f} Máx={v.max():,.0f} Suma={v.sum():,.0f}")

# Certificaciones
print(f"\n  Certificaciones:")
for name, col in [('Orgánica', col_cert_o), ('Fair Trade', col_cert_f), ('Rainforest', col_cert_r)]:
    if col:
        cnt = df3[col].notna().sum()
        print(f"    {name}: {cnt}/{len(df3)} ({cnt/len(df3):.0%})")

# EUDR
if col_eudr3:
    eudr = to_num(df3[col_eudr3])
    valid_e = eudr.notna()
    print(f"\n  EUDR: {valid_e.sum()}/{len(df3)} con dato | Media={eudr.mean():.2f}")
    print(f"    Dist: {eudr.value_counts().to_dict()}")

# Exportaciones
if col_exp3:
    exp = df3[col_exp3].astype(str).str.upper().str.contains('SI').sum()
    print(f"\n  Exporta: {exp}/{len(df3)} ({exp/len(df3):.0%})")

# Mercados
if col_dest3:
    all_d = []
    for d in df3[col_dest3].dropna():
        for p in str(d).split(','):
            p = p.strip().rstrip('.')
            if p: all_d.append(p)
    dest = pd.Series(all_d).value_counts()
    print(f"\n  Mercados: {dest.to_dict()}")

# Provincias
if col_prov3:
    prov3 = df3[col_prov3].value_counts()
    print(f"\n  Provincias: {prov3.to_dict()}")

# Marcas
if col_marca3:
    marcas = df3[col_marca3].dropna().astype(str).str.strip()
    marcas = marcas[~marcas.isin(['nan', 'NaN', ''])]
    print(f"\n  Marcas ({len(marcas)}): {marcas.tolist()}")

# RUC
if col_ruc3:
    ruc3 = df3[col_ruc3].astype(str).str.strip()
    print(f"  RUC válidos (11d): {ruc3.str.match(r'^\\d{11}$').sum()}/{len(df3)}")

# Registro sanitario
if col_rsani3:
    rs = df3[col_rsani3].dropna().astype(str).str.strip()
    rs = rs[~rs.str.lower().str.contains('no cuenta')]
    print(f"  Registro sanitario: {rs.tolist()}")

# SUNAT status
sunat_col = g3('SUNAT', 'status', 'activo')
if sunat_col:
    print(f"\n  Status SUNAT: {df3[sunat_col].value_counts().to_dict()}")

# ─────────────────────────────────────────────────────────────────────────────
# 7. VISUALIZACIONES
# ─────────────────────────────────────────────────────────────────────────────

plt.rcParams.update({
    'figure.facecolor': '#F8F9FA', 'axes.facecolor': '#FFFFFF',
    'axes.grid': True, 'grid.alpha': 0.3,
    'font.family': 'DejaVu Sans', 'font.size': 10,
})
G  = '#1B4332'   # verde oscuro
GM = '#2D6A4F'   # verde medio
GL = '#40916C'   # verde claro
GS = '#74C69D'   # verde suave
AO = '#D4A373'   # ocre
AM = '#E9C46A'   # ámbar
RO = '#C1121F'   # rojo
BL = '#FFFFFF'

# ──────────────────────────────────────────────────────────────────────────────
# V1: Deptos — Café
fig, ax = plt.subplots(figsize=(10, 6))
dept_cafe.head(14).plot(kind='barh', ax=ax, color=GM, edgecolor=BL)
ax.set_title('CAFÉ — Organizaciones PAC por Departamento\n(Archivo 1: Directorio 2018–2025)',
             fontsize=13, fontweight='bold', color=G)
ax.set_xlabel('N° organizaciones'); ax.invert_yaxis()
for i, v in enumerate(dept_cafe.head(14)):
    ax.text(v + 0.2, i, str(v), va='center', fontsize=9)
ax.set_xlim(0, dept_cafe.head(14).max() * 1.12)
sfig(fig, 'v01_cafe_deptos')

# V2: Deptos — Cacao
fig, ax = plt.subplots(figsize=(10, 5))
dept_cacao.head(12).plot(kind='barh', ax=ax, color=AO, edgecolor=BL)
ax.set_title('CACAO — Organizaciones PAC por Departamento\n(Archivo 1: Directorio 2018–2025)',
             fontsize=13, fontweight='bold', color='#8B4513')
ax.set_xlabel('N° organizaciones'); ax.invert_yaxis()
for i, v in enumerate(dept_cacao.head(12)):
    ax.text(v + 0.2, i, str(v), va='center', fontsize=9)
sfig(fig, 'v02_cacao_deptos')

# V3: Tipos org — comparativa Café vs Cacao
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
colors_t = [G, GM, GL, GS]
for ax, df_sub, title, palette in [
    (axes[0], df_cafe, 'CAFÉ', [G, GM, GL]),
    (axes[1], df_cacao, 'CACAO', [AO, '#C4956A', '#E5C9A8'])]:
    vals = df_sub[col_tip if df_sub is df_cafe else col_tip_d].value_counts()
    vals.plot(kind='bar', ax=ax, color=palette[:len(vals)], edgecolor=BL)
    ax.set_title(f'{title} — Tipo de Organización', fontsize=12, fontweight='bold')
    ax.set_ylabel('Conteo'); ax.set_xlabel('')
    plt.sca(ax); plt.xticks(rotation=25, ha='right')
    for i, v in enumerate(vals):
        ax.text(i, v + 1, str(v), ha='center', fontsize=9)
fig.suptitle('CAFÉ vs CACAO — Estructura Organizacional', fontsize=13, fontweight='bold', y=1.02)
plt.tight_layout()
sfig(fig, 'v03_tipos_comparativa')

# V4: Comparativa deptos Café vs Cacao (stacked horizontal)
top_cafe   = set(dept_cafe.head(10).index)
top_cacao  = set(dept_cacao.head(10).index)
both       = top_cafe & top_cacao
cafe_only  = top_cafe - top_cacao
cacao_only = top_cacao - top_cafe
all_labels = list(both) + list(cafe_only) + list(cacao_only)
cafe_vals   = [dept_cafe.get(d, 0) for d in all_labels]
cacao_vals  = [dept_cacao.get(d, 0) for d in all_labels]
colors_map  = [G]*len(both) + [GM]*len(cafe_only) + [AO]*len(cacao_only)

fig, ax = plt.subplots(figsize=(11, 7))
y = np.arange(len(all_labels))
w = 0.38
b1 = ax.barh(y, cafe_vals, height=w, color=G, label='Café', edgecolor=BL)
b2 = ax.barh(y + w, cacao_vals, height=w, color=AO, label='Cacao', edgecolor=BL)
ax.set_yticks(y + w/2)
ax.set_yticklabels(all_labels, fontsize=9)
ax.set_xlabel('N° organizaciones')
ax.set_title('CAFÉ vs CACAO — Cobertura por Departamento\n(Solo deptos con presencia en al menos un producto)',
             fontsize=12, fontweight='bold')
ax.legend()
ax.set_xlim(0, max(max(cafe_vals), max(cacao_vals)) * 1.15)
for i, (cv, dv) in enumerate(zip(cafe_vals, cacao_vals)):
    if cv > 0: ax.text(cv + 0.2, i, str(cv), va='center', fontsize=8, color=G)
    if dv > 0: ax.text(dv + 0.2, i + w, str(dv), va='center', fontsize=8, color=AO)
sfig(fig, 'v04_comparativa_deptos')

# V5: Mapa de calor deptos x producto (A1 universo CC)
if col_dep:
    ct = pd.crosstab(df_cc[col_dep], df_cc[col_prod])
    ct_t = ct.loc[ct.sum(axis=1).nlargest(14).index, ct.sum(axis=0).nlargest(8).index]
    fig, ax = plt.subplots(figsize=(11, 8))
    sns.heatmap(ct_t, annot=True, fmt='d', cmap='Greens', ax=ax,
                linewidths=0.5, cbar_kws={'label': 'N° organizaciones'}, linecolor='#F0F0F0')
    ax.set_title('Mapa de calor — Departamentos × Producto Café/Cacao\n(Archivo 1: 199 organizaciones)',
                 fontsize=12, fontweight='bold')
    sfig(fig, 'v05_heatmap_deptos_producto')

# V6: RUCs válidos — Café vs Cacao
fig, axes = plt.subplots(1, 2, figsize=(9, 4))
for ax, df_sub, ruc_ok, title in [
    (axes[0], df_cafe, ruc_ok_cafe, 'CAFÉ'),
    (axes[1], df_cacao, ruc_ok_cacao, 'CACAO')]:
    vals = [ruc_ok.sum(), (~ruc_ok).sum()]
    labels = [f'Válidos\n{vals[0]}', f'Inválidos\n{vals[1]}']
    bars = ax.bar(labels, vals, color=[G, RO], edgecolor=BL, width=0.5)
    ax.set_title(f'{title} — Validación de RUC\n(Sunat 11 dígitos)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Conteo')
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
                str(v), ha='center', fontsize=12, fontweight='bold')
sfig(fig, 'v06_ruc_validacion')

# V7: Socios San Martín (A3)
if col_sociom and col_sociof:
    sm = to_num(df3[col_sociom]).dropna()
    sf = to_num(df3[col_sociof]).dropna()
    total_socios = int(sm.sum()) + int(sf.sum())
    pct_mujer = int(sf.sum()) / total_socios * 100

    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    # Hist varon
    axes[0].hist(sm, bins=12, color=G, edgecolor=BL, alpha=0.9)
    axes[0].axvline(sm.mean(), color=RO, linestyle='--', linewidth=2, label=f'Media={sm.mean():.0f}')
    axes[0].set_title('Socios Varones\n(Cooperativas San Martín)', fontsize=11, fontweight='bold')
    axes[0].set_xlabel('N°'); axes[0].set_ylabel('Frecuencia'); axes[0].legend(fontsize=9)
    # Hist mujer
    axes[1].hist(sf, bins=12, color=AO, edgecolor=BL, alpha=0.9)
    axes[1].axvline(sf.mean(), color=RO, linestyle='--', linewidth=2, label=f'Media={sf.mean():.0f}')
    axes[1].set_title('Socias Mujeres\n(Cooperativas San Martín)', fontsize=11, fontweight='bold')
    axes[1].set_xlabel('N°'); axes[1].legend(fontsize=9)
    # Pie
    axes[2].pie([sm.sum(), sf.sum()], labels=['Varones', 'Mujeres'],
                colors=[G, AO], autopct='%1.1f%%', startangle=90,
                wedgeprops=dict(edgecolor=BL, linewidth=2))
    axes[2].set_title(f'Composición de Género\nTotal: {total_socios:,} productores', fontsize=11, fontweight='bold')
    fig.suptitle('Archivo 3 — Perfil de Socios (25 Cooperativas San Martín)',
                 fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    sfig(fig, 'v07_socios_genero')

# V8: Hectáreas vs Volumen (A3)
if col_hect3 and col_vol3:
    h = to_num(df3[col_hect3])
    v = to_num(df3[col_vol3])
    valid = ~(h.isna() | v.isna() | (h == 0) | (v == 0))
    if valid.sum() > 2:
        fig, ax = plt.subplots(figsize=(9, 6))
        ax.scatter(h[valid], v[valid], c=G, alpha=0.75, s=100, edgecolors=BL, linewidth=1.5)
        z = np.polyfit(h[valid].values, v[valid].values, 1)
        p1 = np.poly1d(z)
        x_l = np.linspace(h[valid].min(), h[valid].max(), 100)
        r = np.corrcoef(h[valid].values, v[valid].values)[0, 1]
        ax.plot(x_l, p1(x_l), '--', color=AO, linewidth=2,
                label=f'Tendencia (r={r:.2f})')
        ax.set_xlabel('Hectáreas totales', fontsize=11)
        ax.set_ylabel('Volumen cosecha 2026 (qq café verde)', fontsize=11)
        ax.set_title('San Martín — Hectáreas vs Volumen de Producción\n(Cooperativas cafeteras)',
                     fontsize=12, fontweight='bold')
        ax.legend()
        sfig(fig, 'v08_hect_vs_volumen')

# V9: Certificaciones (A3)
if col_cert_o or col_cert_f:
    certs = {}
    for name, col in [('Orgánica', col_cert_o), ('Fair Trade', col_cert_f), ('Rainforest Alliance', col_cert_r)]:
        if col:
            certs[name] = df3[col].notna().sum()
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    names = list(certs.keys()); vals = list(certs.values())
    # Barras
    bars = axes[0].bar(names, vals, color=[G, GM, GL], edgecolor=BL)
    axes[0].set_title('Certificaciones Vigentes\n(25 Cooperativas San Martín)', fontsize=11, fontweight='bold')
    axes[0].set_ylabel('N° cooperativas')
    for bar, v in zip(bars, vals):
        axes[0].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.1,
                     f'{v}\n({v/len(df3):.0%})', ha='center', fontsize=10, fontweight='bold')
    axes[0].set_ylim(0, max(vals)*1.35)
    # Pie
    pie_data = [certs.get('Orgánica', 0), len(df3) - certs.get('Orgánica', 0)]
    axes[1].pie(pie_data, labels=['Con Orgánica', 'Sin Orgánica'],
                 colors=[G, '#E5E7EB'], autopct='%1.0f%%', startangle=90,
                 wedgeprops=dict(edgecolor=BL, linewidth=2))
    axes[1].set_title('Cobertura Certificación Orgánica', fontsize=11, fontweight='bold')
    plt.tight_layout()
    sfig(fig, 'v09_certificaciones')

# V10: EUDR (A3)
if col_eudr3:
    eudr = to_num(df3[col_eudr3])
    bins_lbl = ['0\nNinguno', '0.1–0.4\nInicial', '0.5–0.7\nEn progreso', '0.8–1.0\nAvanzado']
    cuts = pd.cut(eudr, bins=[-0.01, 0, 0.4, 0.7, 1.01], labels=bins_lbl)
    fig, axes = plt.subplots(1, 2, figsize=(13, 4))
    cut_vc = cuts.value_counts().reindex(bins_lbl)
    cut_vc.plot(kind='bar', ax=axes[0], color=[RO, AM, '#F4A261', G], edgecolor=BL)
    axes[0].set_title('Avance EUDR por Nivel\n(17 de 25 cooperativas con dato)', fontsize=11, fontweight='bold')
    axes[0].set_ylabel('N° cooperativas'); plt.sca(axes[0]); plt.xticks(rotation=0)
    for i, v in enumerate(cut_vc):
        axes[0].text(i, v + 0.05, str(v), ha='center', fontsize=11, fontweight='bold')
    # Histograma
    axes[1].hist(eudr.dropna(), bins=8, color=G, edgecolor=BL, alpha=0.85)
    axes[1].axvline(eudr.mean(), color=RO, linestyle='--', linewidth=2, label=f'Media={eudr.mean():.2f}')
    axes[1].set_title('Distribución del Score EUDR\n(0=None, 1=Completo)', fontsize=11, fontweight='bold')
    axes[1].set_xlabel('Score EUDR'); axes[1].set_ylabel('Frecuencia'); axes[1].legend()
    plt.tight_layout()
    sfig(fig, 'v10_eudr')

# V11: FOB Exportaciones (A3)
if col_fob3:
    fob = to_num(df3[col_fob3]).dropna().sort_values()
    if len(fob):
        fig, ax = plt.subplots(figsize=(11, 5))
        orgs = [str(df3.loc[i, col_org3])[:35] if col_org3 else f'Org {i}'
                for i in fob.index]
        bars = ax.barh(range(len(fob)), fob.values, color=G, edgecolor=BL, height=0.65)
        ax.set_yticks(range(len(orgs))); ax.set_yticklabels(orgs, fontsize=8)
        ax.xaxis.set_major_formatter(
            plt.FuncFormatter(lambda x, _: f'${fmt(x)}'))
        ax.set_title('Exportaciones FOB 2025 por Cooperativa (USD)\nSan Martín — Café',
                     fontsize=12, fontweight='bold')
        ax.set_xlabel('FOB USD')
        # Etiquetas
        for bar, val in zip(bars, fob.values):
            ax.text(val + fob.max()*0.01, bar.get_y()+bar.get_height()/2,
                    f'${fmt(val)}', va='center', fontsize=8, color=G)
        sfig(fig, 'v11_fob')

# V12: Mercados destino (A3)
if col_dest3:
    all_d = []
    for d in df3[col_dest3].dropna():
        for p in str(d).split(','):
            p = p.strip().rstrip('.').rstrip(',')
            if p: all_d.append(p)
    dest = pd.Series(all_d).value_counts()
    fig, ax = plt.subplots(figsize=(9, 5))
    dest.head(12).plot(kind='barh', ax=ax, color=G)
    ax.set_title('Mercados de Destino de Exportación\n(Cooperativas San Martín — Café)',
                 fontsize=12, fontweight='bold')
    ax.set_xlabel('Frecuencia'); ax.invert_yaxis()
    sfig(fig, 'v12_destinos')

# V13: Provincias San Martín (A3)
if col_prov3:
    prov3 = df3[col_prov3].value_counts()
    fig, ax = plt.subplots(figsize=(8, 5))
    prov3.plot(kind='barh', ax=ax, color=GM, edgecolor=BL)
    ax.set_title('Cooperativas por Provincia\n(San Martín — Archivo 3)',
                 fontsize=12, fontweight='bold')
    ax.set_xlabel('N° cooperativas'); ax.invert_yaxis()
    for i, v in enumerate(prov3):
        ax.text(v + 0.05, i, str(v), va='center', fontsize=10)
    sfig(fig, 'v13_provincias_sm')

# V14: Altitud (A3)
if col_alt3:
    alt = df3[col_alt3].dropna().astype(str).str.strip()
    alt = alt[~alt.isin(['nan', 'NaN', ''])]
    print(f"\n  Altitudes reportadas ({len(alt)}): {alt.tolist()}")

# V15: Calidad café (A3)
if col_cal3:
    cal = df3[col_cal3].dropna().astype(str).str.strip()
    cal = cal[~cal.isin(['nan', 'NaN', ''])]
    print(f"\n  Calidad ({len(cal)} registros):")
    for c in cal.tolist():
        print(f"    {c[:120]}")

print(f"\n\nTotal graficos generados en: {OUT}")
print(f"  v01 - v15")
