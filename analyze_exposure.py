import pandas as pd
import json

df = pd.read_csv('data/midagri_cafe_cacao_limpio.csv', encoding='latin1')
with open('data/resumen_universo_midagri.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=" * 60)
print("ANÁLISIS TÉCNICO: NIVEL DE EXPOSICIÓN EUDR EN COOPERACIONES")
print("=" * 60)

# CONTEXTO
print("\n1. CONTEXTO GENERAL")
print(f"   • Total organizaciones: {data['total_organizaciones_originales']}")
print(f"   • Total café: {data['total_cafe']}, Total cacao: {data['total_cacao']}")
print(f"   • Total cooperativas: {data['total_cooperativas']} | Total asociaciones: {data['total_asociaciones']}")
print(f"   • Activas y habidas: {data['total_activas_y_habidas']} | Cooperativas activas: {data['cooperativas_activas_habidas']}")

# AVANCE EUDR - KEY METRIC
print("\n2. AVANCE EUDR: NIVEL DE EXPOSICIÓN REAL")
eudr_num_col = 'avance_eudr_num'
df['avance_num'] = pd.to_numeric(df[eudr_num_col], errors='coerce')
avg = df['avance_num'].mean()
median = df['avance_num'].median()

print(f"   • Promedio avance EUDR: {avg:.4f} ({avg*100:.1f}%) - escala 0-1")
print(f"   • Mediana: {median:.4f} ({median*100:.1f}%)")
print(f"   • Rangos: Min={df['avance_num'].min()}, Max={df['avance_num'].max()}")

# Categorías de exposición crítica
df['exposure_level'] = pd.cut(df['avance_num'], 
                              bins=[-0.01, 0.33, 0.66, 1.01], 
                              labels=['Baja (0-33)', 'Media (33-66)', 'Alta (66-100)'])
counts = df['exposure_level'].value_counts().sort_index()
print(f"   • Distribución de exposición:")
for cat, cnt in counts.items():
    print(f"     {cat}: {cnt} de {len(df)} ({cnt/len(df)*100:.1f}%)")

# Interpretation
alta = (df['avance_num'] > 0.66).sum()
media = ((df['avance_num'] > 0.33) & (df['avance_num'] <= 0.66)).sum()
baja = (df['avance_num'] <= 0.33).sum()
print(f"\n   • {alta} de {len(df)} ({alta/len(df)*100:.1f}%) organizaciones")
print(f"   tienen EXPOSICIÓN ALTA a EUDR (avance > 66%).")
print(f"   Solo {baja} ({baja/len(df)*100:.1f}%) están en exposición baja")
print(f"   y {media} ({media/len(df)*100:.1f}%) en exposición media.")

# PATRÓN POR TIPO ORGANIZACIÓN
print("\n3. EXPOSICIÓN EUDR POR TIPO DE ORGANIZACIÓN")
org_col = 'Tipo de Organización'
for org_type in ['Cooperativa', 'Asociación']:
    mask = df[org_col].str.contains(org_type, na=False)
    type_df = df[mask]
    if org_type == 'Cooperativa':
        n = data['cooperativas_activas_habidas']
    else:
        n_assoc = len(df[df[org_col].str.contains('Asociación', na=False)])
        n = n_assoc
    pct_alta = (type_df['avance_num'] > 0.66).mean()*100 if len(type_df) > 0 else 0
    print(f"   • {org_type}: {len(type_df)} de {n} organizados | {pct_alta:.1f}% en exposición ALTA a EUDR")

# PATRÓN POR PRODUCTO
print("\n4. EXPOSICIÓN EUDR POR PRODUCTO")
prod_col = 'Producto Dom'
for prod in ['CAFÉ', 'CACAO']:
    mask = df[prod_col].str.upper().str.contains(prod, na=False)
    prod_df = df[mask]
    alta_exp = (prod_df['avance_num'] > 0.66).sum()
    total = len(prod_df)
    pct = alta_exp/total*100 if total > 0 else 0
    print(f"   • {prod}: {alta_exp} de {total} ({pct:.1f}%) en exposición ALTA a EUDR")

# EXPORTACIÓN
print("\n5. PATRÓN DE EXPORTACIÓN")
exporta_cols = [c for c in df.columns if 'exporta' in c.lower()]
if exporta_cols:
    exp_col = exporta_cols[0]
    n_exportando = (df[exp_col]=='SI').sum()
    print(f"   • Que exportan (SI): {n_exportando} de {len(df)} ({100*(df[exp_col]=='SI').mean():.1f}%)")
    # Correlación entre exportar y exposición EUDR
    if n_exportando > 0:
        exp_alta = df[(df[exp_col]=='SI') & (df['avance_num'] > 0.66)].shape[0]
        print(f"   • De las que exportan, {exp_alta} también tienen exposición ALTA a EUDR")

# HECTÁREAS Y VOLUMEN
print("\n6. SUPERFICIE Y VOLUMEN PRODUCTIVO")
# Hectáreas
hectarea_cols = [c for c in df.columns if 'hectarea' in c.lower() and 'totales' in c.lower()]
if hectarea_cols:
    hcol = hectarea_cols[0]
    total_ha = df[hcol].sum(skipna=True)
    print(f"   • Hectáreas totales en muestra: {total_ha:.0f} ha")
# Volumen
volumen_cols = [c for c in df.columns if 'volumen' in c.lower() and 'cafe' in c.lower() and 'verde' in c.lower()]
if volumen_cols:
    vcol = volumen_cols[0]
    total_q = df[vcol].sum(skipna=True)
    print(f"   • Volumen café verde estimado 2026: {total_q:.0f} q")

# DISTRIBUCIÓN REGIONAL
print("\n7. DISTRIBUCIÓN REGIONAL - EXPOSICIÓN EUDR")
region_cols = [c for c in df.columns if 'region' in c.lower()]
if region_cols:
    region_col = region_cols[0]
    top_regions = df[region_col].value_counts().head(5)
    for region, count in top_regions.items():
        subset = df[df[region_col]==region]
        alta = (subset['avance_num'] > 0.66).sum()
        pct = alta/len(subset)*100 if len(subset) > 0 else 0
        print(f"   • {region}: {count} orgs | {pct:.1f}% exposición ALTA a EUDR")

print("\n" + "=" * 60)
print("CONCLUSIONES TÉCNICAS")
print("=" * 60)
print(f"""
1. EXPOSICIÓN MASIVA: {alta} de {len(df)} ({alta/len(df)*100:.1f}%) organizaciones 
   tienen ALTA exposición al reglamento EUDR (avance > 66% en escala 0-1). 
   No es una minoría afectada, es la norma nacional actual.

2. COOPERATIVAS son el núcleo: La mayoría de las {data['cooperativas_activas_habidas']} 
   cooperativas activas ya tienen avance significativo en cumplimiento EUDR, 
   pero el {baja} ({baja/len(df)*100:.1f}%) en exposición baja y 
   {media} ({media/len(df)*100:.1f}%) en exposición media requieren 
   apoyo prioritario.

3. VOLUMEN ECONÓMICO: Las organizaciones implican {total_ha:.0f} ha y 
   {total_q:.0f} q de producción que hoy requieren cumplir EUDR para 
   acceder al mercado UE.

4. BRECHAS RESIDUALES: El grupo de {baja} organizaciones en exposición 
   baja y {media} en exposición media son la prioritaria para intervención 
   técnica de cierre de brechas EUDR.

5. El diagnóstico no es opcional: Con {alta/len(df)*100:.1f}% de organizaciones 
   ya en exposición alta, el cumplimiento EUDR es una cuestión de supervivencia 
   comercial, no de optatividad.
""")