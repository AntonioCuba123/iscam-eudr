# -*- coding: utf-8 -*-
"""Corrige elementos mezclados español/inglés en build_iscam_v3.py"""
with open(r'C:\Users\acuba\eudrperu\build_iscam_v3.py', encoding='utf-8') as f:
    content = f.read()

# Fix 1: IV3 label
content = content.replace(
    "    (23, 'IV3\\nha>0? 65:35'),\n    (24, 'IV4\\nCert=0? 70:30'),\n    (25, 'IV5\\nAsoc? 65:40'),",
    "    (23, 'IV3\\nha>0? → 65:35'),\n    (24, 'IV4\\nCert=0? → 70:30'),\n    (25, 'IV5\\nTipo Asoc → 65:40'),"
)

# Fix 2: nota row 'orgs' → 'organizaciones'
content = content.replace(
    "ws_i.cell(last_r, 29).value = f'n = {n_orgs} orgs'",
    "ws_i.cell(last_r, 29).value = f'n = {n_orgs} organizaciones'"
)

# Fix 3: nota metodológica - limpia inglés mezclado
content = content.replace(
    "IV3=ha>0?65:35, IV4=cert=0?70:30, IV5=tipo Asoc?65:40",
    "IV3=ha>0?→65:35, IV4=cert=0?→70:30, IV5=tipo Asoc?→65:40"
)

# Fix 4: fila 2 nota - 'col H/I/J' → 'cols H/I/J'
content = content.replace(
    "D2/D5/D6 → SCORECARDS col H/I/J  |  D3 → MATRIZ_174!U (Neon)",
    "D2/D5/D6 → SCORECARDS cols H/I/J  |  D3 → MATRIZ_174!U (Neon)"
)

with open(r'C:\Users\acuba\eudrperu\build_iscam_v3.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixes applied')
