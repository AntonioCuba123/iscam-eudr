# -*- coding: utf-8 -*-
"""Filtrar las 83 orgs cafe/cacao nuevas de SOPARSE por exportacion via PRODUCE."""
import pandas as pd

# Cargar SOPARSE completo
sop = pd.read_csv(r'C:/Users/acuba/eudrperu/data/soparse_cencoop2017.csv', sep='|', dtype=str, low_memory=False)
sop['NUM_RUC_LIMPIO'] = sop['NUM_RUC'].str.strip()

# Cargar matriz actual (v4)
xls = pd.read_excel(r'C:/Users/acuba/eudrperu/MATRIZ_IP_IV_v4_EUDRPERU.xlsx', sheet_name='MATRIZ', header=0)
xls['RUC_LIMPIO'] = xls['RUC'].astype(str).str.strip().str.zfill(11)
xls_rucs = set(xls['RUC_LIMPIO'].dropna())

# Org cafe/cacao en SOPARSE fuera del Excel
sop_caf = sop[sop['RAZON_SOCIAL'].str.contains('CAFE|CAFÉ|CACAO|COCOA', case=False, na=False)]
nuevas = sop_caf[~sop_caf['NUM_RUC_LIMPIO'].isin(xls_rucs)].copy()
print(f'83 orgs cafe/cacao en SOPARSE fuera del Excel: {len(nuevas)}')

# Cargar PRODUCE (MIDAGRI match)
produce = pd.read_csv(r'C:/Users/acuba/eudrperu/data/PRODUCE_match_keywords.csv', sep='|', dtype=str, low_memory=False)
produce_rucs = set(produce['ruc'].astype(str).str.strip().str.zfill(11).dropna())

# Cargar PAC directo (Directorio Cooperativas Cafe-Cacao Peru v3)
pac_files = [
    r'C:/Users/acuba/eudrperu/Directorio Cooperativas Cafe-Cacao Peru (v3 - Cepicafe-Norandino).xlsx',
    r'C:/Users/acuba/eudrperu/Directorio Cooperativas Cafe-Cacao Peru.xlsx',
]
pac_dfs = []
for pf in pac_files:
    try:
        pac_raw = pd.read_excel(pf, sheet_name='Cooperativas y asociaciones', header=None)
        if pac_raw.iloc[0].tolist()[0] == 'Organización (nombre usual)':
            pac_raw = pac_raw.iloc[1:].reset_index(drop=True)
        pac_dfs.append(pac_raw)
    except Exception:
        pass
if pac_dfs:
    pac_all = pd.concat(pac_dfs, ignore_index=True)
    pac_all.columns = range(len(pac_all.columns))
    pac_rucs = set(pac_all[2].astype(str).str.strip().str.zfill(11).dropna())  # col 2 = RUC
else:
    pac_rucs = set()

# Cargar MIDAGRI (CSV)
try:
    midagri = pd.read_csv(r'C:/Users/acuba/eudrperu/data/MIDAGRI_cooperativas_agrarias_2026.csv', sep='|', dtype=str, nrows=5)
    midagri_col = [c for c in midagri.columns if 'ruc' in c.lower()][0] if any('ruc' in c.lower() for c in midagri.columns) else midagri.columns[0]
    midagri_all = pd.read_csv(r'C:/Users/acuba/eudrperu/data/MIDAGRI_cooperativas_agrarias_2026.csv', sep='|', dtype=str, low_memory=False)
    midagri_rucs = set(midagri_all[midagri_col].astype(str).str.strip().str.zfill(11).dropna())
except:
    midagri_rucs = set()

# Exportadores confirmados: union de PRODUCE + PAC + MIDAGRI
export_rucs = produce_rucs | pac_rucs | midagri_rucs

# Filtrar las 83 por exportacion
nuevas['EN_PRODUCE'] = nuevas['NUM_RUC_LIMPIO'].isin(produce_rucs)
nuevas['EN_PAC'] = nuevas['NUM_RUC_LIMPIO'].isin(pac_rucs)
nuevas['EN_MIDAGRI'] = nuevas['NUM_RUC_LIMPIO'].isin(midagri_rucs)
nuevas['ES_EXISTENTE_MATRIZ'] = False

exportadoras = nuevas[nuevas['EN_PRODUCE'] | nuevas['EN_PAC'] | nuevas['EN_MIDAGRI']]
no_exportadoras = nuevas[~(nuevas['EN_PRODUCE'] | nuevas['EN_PAC'] | nuevas['EN_MIDAGRI'])]

print(f'\n--- Resultados del filtro ---')
print(f'Con datos en PRODUCE (exportadores): {nuevas["EN_PRODUCE"].sum()}')
print(f'Con datos en PAC directo:           {nuevas["EN_PAC"].sum()}')
print(f'Con datos en MIDAGRI:               {nuevas["EN_MIDAGRI"].sum()}')
print(f'Total exportadoras (al menos 1 fuente): {len(exportadoras)}')
print(f'No exportadoras en fuentes actuales:   {len(no_exportadoras)}')

print(f'\n--- Organizaciones cafe/cacao nuevas que SÍ exportan (candidatas) ---')
if len(exportadoras) > 0:
    cols_show = ['NUM_RUC_LIMPIO','RAZON_SOCIAL','NOMBREDD','NOMBREPV','NOMBREDI','EN_PRODUCE','EN_PAC','EN_MIDAGRI']
    disponibles = [c for c in cols_show if c in exportadoras.columns]
    print(exportadoras[disponibles].to_string(index=False))
else:
    print('Ninguna de las 83 orgs cafe/cacao esta en PRODUCE, PAC o MIDAGRI.')

print(f'\n--- Organizaciones cafe/cacao nuevas que NO exportan (descartadas) ---')
cols_no = ['NUM_RUC_LIMPIO','RAZON_SOCIAL','NOMBREDD','NOMBREPV','NOMBREDI']
disponibles_no = [c for c in cols_no if c in no_exportadoras.columns]
print(no_exportadoras[disponibles_no].to_string(index=False))

# Guardar lista de exportadoras candidatas
if len(exportadoras) > 0:
    exp_out = exportadoras.rename(columns={
        'NUM_RUC_LIMPIO': 'RUC',
        'RAZON_SOCIAL': 'NOMBRE',
        'NOMBREDD': 'DPTO',
        'NOMBREPV': 'PROV',
        'NOMBREDI': 'DIST',
        'C1_P6': 'ANIO_CONST',
        'C1_P7': 'ANIO_INICIO_OP',
        'CIIU_REV4': 'CIIU',
        'C1_P15': 'ESTADO'
    })
    exp_out.to_csv(r'C:/Users/acuba/eudrperu/data/nuevas_exportadoras_soparse.csv', index=False, sep='|', encoding='utf-8-sig')
    print(f'\nCSV de exportadoras candidatas guardado: {len(exp_out)} orgs')
