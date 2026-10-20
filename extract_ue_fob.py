# -*- coding: utf-8 -*-
"""
extract_ue_fob.py — Extrae FOB total y FOB UE por organización.

Fuentes:
  - RUC_FOB_DUA (BASE CONSOLIDADA): RUC + país de cada DUA (sin FOB)
  - CRUCE_DUAs_FOB_POR_ORGANIZACION.xlsx: FOB total por organización
  - DUA_Consolidado_Total (reportes): FOB por DUA individual + país
"""
import openpyxl
import pandas as pd

EU_SET = {
    'AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR',
    'DE', 'GR', 'HU', 'IE', 'IT', 'LV', 'LT', 'LU', 'MT', 'NL',
    'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE',
}

# ── 1. RUC_FOB_DUA: países por organización ──
print("Leyendo RUC_FOB_DUA (países)...")
wb_fob = openpyxl.load_workbook(
    r"C:\Users\acuba\eudrperu\ficharucsunat\BASE CONSOLIDADA.xlsx",
    read_only=True, data_only=True)
ws_fob = wb_fob['RUC_FOB_DUA']

fob_rows = []
for r in ws_fob.iter_rows(min_row=2, values_only=True):
    ruc  = str(r[0]).strip()[:15] if r[0] else ''
    pais = str(r[5]).strip().upper() if r[5] else ''
    dua  = str(r[6]).strip()[:10] if r[6] else ''
    if ruc and pais:
        fob_rows.append({'ruc': ruc, 'pais': pais, 'dua': dua})
wb_fob.close()

df_pais = pd.DataFrame(fob_rows)
print(f"  {len(df_pais)} DUAs con país")

# ¿Cuántos países UE por RUC?
df_ue = df_pais[df_pais['pais'].isin(EU_SET)]
rucs_con_ue = set(df_ue['ruc'].unique())
rucs_sin_ue = set(df_pais['ruc'].unique()) - rucs_con_ue
print(f"  RUCs con al menos 1 DUA a UE: {len(rucs_con_ue)}")
print(f"  RUCs solo a países NO-UE: {len(rucs_sin_ue)}")

# ── 2. CRUCE_DUAs_FOB: FOB total por organización ──
print("Leyendo CRUCE_DUAs_FOB_POR_ORGANIZACION...")
wb_cruce = openpyxl.load_workbook(
    r"C:\Users\acuba\eudrperu\BASE CAFE CACAO 174\CONSULTA MASIVA RUC 10.10.26"
    r"\CRUCE_DUAs_FOB_POR_ORGANIZACION.xlsx",
    read_only=True, data_only=True)
ws_cruce = wb_cruce['1. Cruce por organización']

cruce_rows = []
for r in ws_cruce.iter_rows(min_row=2, values_only=True):
    if r[0]:  # RUC
        cruce_rows.append({
            'ruc': str(r[0]).strip()[:15],
            'razon': str(r[1])[:80] if r[1] else '',
            'fob_total': float(r[7]) if r[7] else 0.0,
            'paises': str(r[18])[:200] if r[18] else '',
            'n_duas': int(r[15]) if r[15] else 0,
        })
wb_cruce.close()

df_cruce = pd.DataFrame(cruce_rows)
print(f"  {len(df_cruce)} organizaciones con DUAs+FOB")

# ── 3. Combinar: FOB total + países UE ──
# Para cada RUC del CRUCE, marcar si tiene DUA a UE
df_cruce['tiene_ue'] = df_cruce['ruc'].isin(rucs_con_ue)
df_cruce['pct_ue'] = df_cruce.apply(
    lambda r: (1.0 if r['tiene_ue'] else 0.0) * 100, axis=1)

# Estimar FOB UE usando el pct de DUAs UE
# Para los que tienen países detectados, estimar pct_ue por proporción de DUAs
# Pero no tenemos conteo de DUAs por país → usar aproximación: si tiene UE, marcar 50% mínimo
# Para una estimación más precisa, usamos los datos del DUA_Consolidado_Total
# ── 4. Refinar con DUA_Consolidado_Total (FOB por DUA individual) ──
print("Leyendo DUA_Consolidado_Total (FOB detallado)...")
wb_dua = openpyxl.load_workbook(
    r"C:\Users\acuba\eudrperu\reports"
    r"\DUA_CONSOLIDADO_con_atributos_20261002 (2).xlsx",
    read_only=True, data_only=True)
ws_dua = wb_dua['DUA_Consolidado_Total']

dua_detail = []
for r in ws_dua.iter_rows(min_row=2, values_only=True):
    ruc  = str(r[0]).strip()[:15] if r[0] else ''
    pais = str(r[6]).strip().upper() if r[6] else ''
    fob  = r[11]   # fob_pdf
    dua  = str(r[1]).strip()[:10] if r[1] else ''
    if not ruc or not pais or fob is None:
        continue
    try:
        fob = float(fob)
    except:
        fob = 0.0
    dua_detail.append({'ruc': ruc, 'pais': pais, 'fob': fob, 'dua': dua})
wb_dua.close()

df_dua_detail = pd.DataFrame(dua_detail)
print(f"  {len(df_dua_detail)} DUAs con FOB detallado")

# Agregar FOB por RUC+país (dividir FOB si DUA compartido entre países)
if df_dua_detail.empty:
    df_fob_ue = pd.DataFrame(columns=['ruc', 'fob_ue', 'fob_total'])
else:
    dua_count = df_dua_detail.groupby(['ruc', 'dua'])['pais'].transform('count')
    df_dua_detail['fob_adj'] = df_dua_detail['fob'] / dua_count
    df_country = df_dua_detail.groupby(['ruc', 'pais'])['fob_adj'].sum().reset_index()
    fob_total_dua = df_country.groupby('ruc')['fob_adj'].sum().rename('fob_total')
    fob_ue_dua = (df_country[df_country['pais'].isin(EU_SET)]
                   .groupby('ruc')['fob_adj'].sum()
                   .rename('fob_ue'))
    df_fob_ue = (pd.DataFrame({'ruc': fob_total_dua.index,
                                 'fob_total': fob_total_dua.values})
                   .merge(pd.DataFrame({'ruc': fob_ue_dua.index,
                                         'fob_ue': fob_ue_dua.values}),
                          on='ruc', how='left').fillna(0))
    df_fob_ue['pct_ue'] = df_fob_ue.apply(
        lambda r: round(r['fob_ue'] / r['fob_total'] * 100, 1)
        if r['fob_total'] > 0 else 0, axis=1)

# ── 5. Combinar todo ──
df_r = df_cruce.copy()
df_r = df_r.rename(columns={'ruc': 'RUC'})

# Cruce con FOB detallado
df_r = df_r.merge(
    df_fob_ue.rename(columns={'ruc': 'RUC'}),
    on='RUC', how='left')

# Para los que no tienen FOB del DUA detallado, usar el del CRUCE como FOB total
df_r['fob_total_calc'] = df_r['fob_total_x'].fillna(df_r['fob_total_y'])
df_r['fob_ue'] = df_r['fob_ue'].fillna(0)
df_r['fob_ue'] = df_r.apply(
    lambda r: r['fob_ue'] if r['fob_ue'] > 0
              else (r['fob_total_calc'] * 0.5 if r['tiene_ue'] else 0.0),
    axis=1)
df_r['pct_ue'] = df_r.apply(
    lambda r: round(r['fob_ue'] / r['fob_total_calc'] * 100, 1)
    if r['fob_total_calc'] > 0 else 0, axis=1)

# ── 6. Cruce con MATRIZ_174 ──
matriz_path = r"C:\Users\acuba\eudrperu\BASE CAFE CACAO 174\MATRIZ_ORGANIZACIONES_174_FINAL.csv"
df_matriz = pd.read_csv(matriz_path, encoding='utf-8-sig')
df_r = df_r.merge(
    df_matriz[['RUC', 'Razón Social (SUNAT)']].assign(
        RUC=df_matriz['RUC'].astype(str).str.strip()),
    on='RUC', how='left')

print(f"\n  Total orgs con FOB en CRUCE: {len(df_r)}")
print(f"  Org con exposición UE confirmada: {(df_r['fob_ue'] > 0).sum()}")
print(f"  FOB total (CRUCE): USD {df_r['fob_total_calc'].sum():,.0f}")
print(f"  FOB UE estimado: USD {df_r['fob_ue'].sum():,.0f}")

# ── 7. Top 15 ──
print("\n=== TOP 15 ORGANIZACIONES CON EXPOSICIÓN UE ===")
top = df_r[df_r['fob_ue'] > 0].nlargest(15, 'fob_ue')
for _, r in top.iterrows():
    nombre = str(r.get('Razón Social (SUNAT)', r['razon']))[:48]
    fobeu  = r['fob_ue']
    fobt   = r['fob_total_calc']
    pct    = r['pct_ue']
    paises = str(r.get('paises', ''))[:40]
    tipo   = '(detallado)' if r['fob_ue'] <= r['fob_total_calc'] * 0.9 else '(estimado)'
    print(f"  {nombre:<48} | UE: USD {fobeu:>11,.0f} {tipo} | Total: USD {fobt:>12,.0f} | {pct:.0f}%")

# ── 8. Escribir en PLANTILLA_INDICE_PVE ──
print("\nActualizando PLANTILLA_INDICE_PVE...")
pve_path = r"C:\Users\acuba\eudrperu\PLANTILLA_INDICE_PVE.xlsx"
wb_pve = openpyxl.load_workbook(pve_path)
ws_mat = wb_pve['MATRIZ_174']
ws_sco = wb_pve['SCORECARDS']

updated = 0
for row in range(3, ws_mat.max_row + 1):
    ruc_val = ws_mat.cell(row=row, column=1).value
    if not ruc_val:
        continue
    ruc_str = str(ruc_val).strip()
    match = df_r[df_r['RUC'].astype(str).str.strip() == ruc_str]
    if match.empty:
        continue

    r_data = match.iloc[0]
    fob_ue    = round(float(r_data['fob_ue']), 2)
    fob_total = round(float(r_data['fob_total_calc']), 2)

    # MATRIZ col 5 = FOB total
    current_fob = ws_mat.cell(row=row, column=5).value
    if not current_fob or float(current_fob or 0) == 0:
        ws_mat.cell(row=row, column=5).value = fob_total

    # MATRIZ col 12 = FOB UE
    ws_mat.cell(row=row, column=12).value = fob_ue

    # SCORECARDS col 6 = FOB UE
    ws_sco.cell(row=row, column=6).value = fob_ue

    updated += 1

wb_pve.save(pve_path)
print(f"  ✅ {updated} organizaciones actualizadas")
print(f"  📁 Guardado: {pve_path}")
