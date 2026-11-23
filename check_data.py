import pandas as pd
df = pd.read_csv('data/midagri_cafe_cacao_limpio.csv', encoding='latin1')
print(f'Total rows: {len(df)}')
print(f'avance_eudr_num notna: {df["avance_eudr_num"].notna().sum()}')
print(f'avance_eudr_num null: {df["avance_eudr_num"].isna().sum()}')
vals = df['avance_eudr_num'].dropna().unique()
print(f'Unique values (non-null): {vals[:20]}')
print(f'Total unique: {len(vals)}')