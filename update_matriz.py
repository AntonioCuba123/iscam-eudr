import openpyxl

# Load both workbooks
wb_matriz = openpyxl.load_workbook('MATRIZ_IP_IV_v18_EUDRPERU.xlsx')
ws_matriz = wb_matriz['MATRIZ']

wb_dua = openpyxl.load_workbook('reports/DUA_CONSOLIDADO_con_atributos_20261002 (2).xlsx', read_only=True)
ws_por_ruc = wb_dua['por RUC']
ws_detalle = wb_dua['DETALLE_ITEMS']

# Aggregate DUA data by RUC
from collections import defaultdict

ruc_data = defaultdict(lambda: {
    'organico_count': 0, 'fairtrade_count': 0, 'rainforest_count': 0,
    'utz_count': 0, 'sustentable_count': 0,
    'marca_count': 0, 'lote_count': 0, 'contrato_count': 0,
    'bolsa_count': 0, 'granel_count': 0, 'en_grano_count': 0,
    'washed_count': 0, 'natural_count': 0, 'honey_count': 0,
    'arabica_count': 0, 'robusta_count': 0, 'criollo_count': 0,
    'trinitario_count': 0, 'forastero_count': 0, 'amazonico_count': 0,
    'consumo_humano_count': 0, 'total_items': 0
})

for row in ws_detalle.iter_rows(min_row=2, max_row=ws_detalle.max_row, values_only=True):
    ruc = row[0]
    if not ruc:
        continue
    attrs = row[8] or ''
    d = ruc_data[ruc]
    d['total_items'] += 1
    if row[9]: d['organico_count'] += 1
    if row[10]: d['fairtrade_count'] += 1
    if row[11]: d['rainforest_count'] += 1
    if row[12]: d['utz_count'] += 1
    if row[13]: d['sustentable_count'] += 1
    if attrs:
        if 'marca' in attrs: d['marca_count'] += 1
        if 'lote' in attrs: d['lote_count'] += 1
        if 'contrato' in attrs: d['contrato_count'] += 1
        if 'bolsa' in attrs: d['bolsa_count'] += 1
        if 'granel' in attrs: d['granel_count'] += 1
        if 'en_grano' in attrs: d['en_grano_count'] += 1
        if 'washed' in attrs: d['washed_count'] += 1
        if 'natural' in attrs: d['natural_count'] += 1
        if 'honey' in attrs: d['honey_count'] += 1
        if 'arabica' in attrs: d['arabica_count'] += 1
        if 'robusta' in attrs: d['robusta_count'] += 1
        if 'criollo' in attrs: d['criollo_count'] += 1
        if 'trinitario' in attrs: d['trinitario_count'] += 1
        if 'forastero' in attrs: d['forastero_count'] += 1
        if 'amazonico' in attrs: d['amazonico_count'] += 1
        if 'consumo_humano' in attrs: d['consumo_humano_count'] += 1

# Add new columns to MATRIZ (starting at column 59 = BG)
new_headers = [
    ('BG', 'DUA_items_total'),
    ('BH', 'DUA_organico_items'),
    ('BI', 'DUA_fairtrade_items'),
    ('BJ', 'DUA_rainforest_items'),
    ('BK', 'DUA_utz_items'),
    ('BL', 'DUA_bolsa_items'),
    ('BM', 'DUA_granel_items'),
    ('BN', 'DUA_en_grano_items'),
    ('BO', 'DUA_washed_items'),
    ('BP', 'DUA_natural_items'),
    ('BQ', 'DUA_honey_items'),
    ('BR', 'DUA_marca_items'),
    ('BS', 'DUA_lote_items'),
    ('BT', 'DUA_contrato_items'),
    ('BU', 'DUA_arabica_items'),
    ('BV', 'DUA_robusta_items'),
    ('BW', 'DUA_tiene_marca_origen'),
    ('BX', 'DUA_tiene_lote'),
    ('BY', 'DUA_tiene_contrato'),
    ('BZ', 'DUA_pct_organico'),
    ('CA', 'DUA_pct_bolsa'),
    ('CB', 'DUA_pct_granel'),
    ('CC', 'DUA_pct_washed'),
    ('CD', 'DUA_pct_certificados'),
    ('CE', 'DUA_trazabilidad_score'),
    ('CF', 'DUA_certificacion_score'),
]

for col_letter, header in new_headers:
    ws_matriz.cell(row=4, column=openpyxl.utils.column_index_from_string(col_letter), value=header)

# Source row (row 5) - fill with source info
source_info = 'DUA_CONSOLIDADO_con_atributos  |  2026'
for col_letter, _ in new_headers:
    ws_matriz.cell(row=5, column=openpyxl.utils.column_index_from_string(col_letter), value=source_info)

# Now populate data rows (starting row 7)
for row_idx in range(7, ws_matriz.max_row + 1):
    ruc_cell = ws_matriz.cell(row=row_idx, column=2)
    if not ruc_cell.value:
        continue
    ruc = str(ruc_cell.value).strip()
    if ruc in ruc_data:
        d = ruc_data[ruc]
        total = d['total_items']
        if total > 0:
            ws_matriz.cell(row=row_idx, column=59, value=total)  # BG
            ws_matriz.cell(row=row_idx, column=60, value=d['organico_count'])  # BH
            ws_matriz.cell(row=row_idx, column=61, value=d['fairtrade_count'])  # BI
            ws_matriz.cell(row=row_idx, column=62, value=d['rainforest_count'])  # BJ
            ws_matriz.cell(row=row_idx, column=63, value=d['utz_count'])  # BK
            ws_matriz.cell(row=row_idx, column=64, value=d['bolsa_count'])  # BL
            ws_matriz.cell(row=row_idx, column=65, value=d['granel_count'])  # BM
            ws_matriz.cell(row=row_idx, column=66, value=d['en_grano_count'])  # BN
            ws_matriz.cell(row=row_idx, column=67, value=d['washed_count'])  # BO
            ws_matriz.cell(row=row_idx, column=68, value=d['natural_count'])  # BP
            ws_matriz.cell(row=row_idx, column=69, value=d['honey_count'])  # BQ
            ws_matriz.cell(row=row_idx, column=70, value=d['marca_count'])  # BR
            ws_matriz.cell(row=row_idx, column=71, value=d['lote_count'])  # BS
            ws_matriz.cell(row=row_idx, column=72, value=d['contrato_count'])  # BT
            ws_matriz.cell(row=row_idx, column=73, value=d['arabica_count'])  # BU
            ws_matriz.cell(row=row_idx, column=74, value=d['robusta_count'])  # BV
            # Flags
            ws_matriz.cell(row=row_idx, column=75, value=1 if d['marca_count'] > 0 else 0)  # BW
            ws_matriz.cell(row=row_idx, column=76, value=1 if d['lote_count'] > 0 else 0)  # BX
            ws_matriz.cell(row=row_idx, column=77, value=1 if d['contrato_count'] > 0 else 0)  # BY
            # Percentages
            ws_matriz.cell(row=row_idx, column=78, value=round(d['organico_count']/total, 4))  # BZ
            ws_matriz.cell(row=row_idx, column=79, value=round(d['bolsa_count']/total, 4))  # CA
            ws_matriz.cell(row=row_idx, column=80, value=round(d['granel_count']/total, 4))  # CB
            ws_matriz.cell(row=row_idx, column=81, value=round(d['washed_count']/total, 4))  # CC
            cert_total = d['organico_count'] + d['fairtrade_count'] + d['rainforest_count'] + d['utz_count']
            ws_matriz.cell(row=row_idx, column=82, value=round(cert_total/total, 4))  # CD
            # D2 traceability composite: marca + lote + contrato + granel(inverse)
            traz = (d['marca_count'] + d['lote_count']*2 + d['contrato_count']*2) / (total * 3) if total > 0 else 0
            ws_matriz.cell(row=row_idx, column=83, value=round(min(traz, 1), 4))  # CE
            # D10 certification composite: organico + fairtrade + rainforest + (marca*0.5)
            cert_score = (d['organico_count'] + d['fairtrade_count']*1.5 + d['rainforest_count']*1.5 + d['marca_count']*0.5) / (total * 2) if total > 0 else 0
            ws_matriz.cell(row=row_idx, column=84, value=round(min(cert_score, 1), 4))  # CF

wb_matriz.save('MATRIZ_IP_IV_v18_EUDRPERU.xlsx')
print("MATRIZ updated with DUA-derived columns")

# Update COBERTURA IP IV sheet
ws_cob = wb_matriz['COBERTURA IP IV']
# Update D2 row (row 3) - now has DUA data for traceability
ws_cob.cell(row=3, column=3, value='DUA items (marca/lote/contrato/bolsa/granel/proceso)')
ws_cob.cell(row=3, column=4, value=sum(1 for d in ruc_data.values() if d['marca_count']+d['lote_count']+d['contrato_count'] > 0))
ws_cob.cell(row=3, column=5, value='{}%'.format(round(sum(1 for d in ruc_data.values() if d['marca_count']+d['lote_count']+d['contrato_count'] > 0)/len(ruc_data)*100)))
ws_cob.cell(row=3, column=6, value='Marcas/lotes/contratos en DUA; empaque y proceso como proxy trazabilidad')

# Update D10 row (row 11) - certifications now from DUA
ws_cob.cell(row=11, column=3, value='DUA items (organico/fairtrade/rainforest/utz) + Directorio PAC')
ws_cob.cell(row=11, column=4, value=sum(1 for d in ruc_data.values() if d['organico_count']+d['fairtrade_count']+d['rainforest_count']+d['utz_count'] > 0))
ws_cob.cell(row=11, column=5, value='{}%'.format(round(sum(1 for d in ruc_data.values() if d['organico_count']+d['fairtrade_count']+d['rainforest_count']+d['utz_count'] > 0)/len(ruc_data)*100)))
ws_cob.cell(row=11, column=6, value='Certificados declarados en DUA; 312 items, 108 organicos, 10 fairtrade, 0 rainforest/utz')

wb_matriz.save('MATRIZ_IP_IV_v18_EUDRPERU.xlsx')
print("COBERTURA IP IV updated")