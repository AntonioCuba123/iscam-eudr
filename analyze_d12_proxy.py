# -*- coding: utf-8 -*-
import openpyxl
wb = openpyxl.load_workbook(r'C:\Users\acuba\eudrperu\PLANTILLA_INDICE_PVE.xlsx', data_only=True)
ws = wb['MATRIZ_174']

print('=== D12=1 actual — certificaciones ===')
for r in range(3, ws.max_row+1):
    d12  = ws.cell(r, 23).value
    cert = str(ws.cell(r, 8).value or '').strip()
    fair = str(ws.cell(r, 9).value or '').strip()
    fob  = ws.cell(r, 12).value or 0
    prod = ws.cell(r, 4).value or ''
    org  = ws.cell(r, 2).value or ''
    if d12 == 1:
        print(f'  {str(org)[:35]:35} cert={cert:8} fair={fair:8} FOB UE={fob:12.0f} {prod}')

print()
print('=== D12=0 CON certificacion ( Organic | Fairtrade | UE ) ===')
for r in range(3, ws.max_row+1):
    d12  = ws.cell(r, 23).value
    cert = str(ws.cell(r, 8).value or '').lower().strip()
    fair = str(ws.cell(r, 9).value or '').lower().strip()
    fob  = ws.cell(r, 12).value or 0
    org  = ws.cell(r, 2).value or ''
    prod = ws.cell(r, 4).value or ''
    tiene_cert = any(x in cert for x in ['si', 'ue', 'org', 'cer']) or any(x in fair for x in ['si', 'fair', 'flo', 'fai'])
    if d12 == 0 and tiene_cert:
        print(f'  {str(org)[:35]:35} cert={ws.cell(r,8).value or "":8} fair={ws.cell(r,9).value or "":8} FOB UE={fob:12.0f} {prod}')

print()
print('=== D12=0 CON FOB UE > 500k USD (sin certificacion) ===')
count = 0
for r in range(3, ws.max_row+1):
    d12  = ws.cell(r, 23).value
    fob  = ws.cell(r, 12).value or 0
    org  = ws.cell(r, 2).value or ''
    prod = ws.cell(r, 4).value or ''
    if d12 == 0 and fob > 500000:
        print(f'  {str(org)[:35]:35} FOB UE={fob:12.0f} {prod}')
        count += 1
print(f'  --> {count} orgs')
