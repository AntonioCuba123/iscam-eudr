import pandas as pd
df = pd.read_csv(r'C:\Users\acuba\eudrperu\BASE CAFE CACAO 174\MATRIZ_ORGANIZACIONES_174_FINAL.csv', encoding='utf-8-sig')

print("=== PERFIL DE LA BASE ===")
print(f"Total organizaciones: {len(df)}")
print(f"Exportan: {(df['Exporta (interno)'] == 'SI').sum()}")

exportadores = df[df['Exporta (interno)'] == 'SI']
fob_numeric = pd.to_numeric(exportadores['FOB total USD (interno)'], errors='coerce')
con_fob = exportadores[fob_numeric > 0]
print(f"Exportadores con FOB > 0: {len(con_fob)}")
print(f"Total FOB exportadores con datos: USD {fob_numeric.sum():,.0f}")

print("\n=== TOP 15 POR FOB ===")
cols = ['RUC', 'Razón Social (SUNAT)', 'FOB total USD (interno)', 'N° DUAs', 'Avance EUDR']
top = con_fob.nlargest(15, 'FOB total USD (interno)')[cols]
for _, r in top.iterrows():
    rs = str(r['Razón Social (SUNAT)'])[:55]
    fob = r['FOB total USD (interno)']
    duas = r['N° DUAs']
    avance = str(r['Avance EUDR'])[:30] if pd.notna(r['Avance EUDR']) else 'N/A'
    print(f"  {rs} | FOB: {fob:>12,.0f} | DUAs: {duas} | {avance}")

print("\n=== AVANCE EUDR ===")
print(exportadores['Avance EUDR'].value_counts(dropna=False))

print("\n=== DEPARTAMENTOS DE EXPORTADORES ===")
print(exportadores['Departamento'].value_counts())
