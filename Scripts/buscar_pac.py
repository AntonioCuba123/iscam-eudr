# -*- coding: utf-8 -*-
import openpyxl, re

nuevos_nombres = [
    ('20132509876','COOP AGRARIA CAFETALERA MARANURA LTDA'),
    ('20357021058','COOPERATIVA AGRARIA DE PRODUCTORES ORGANICOS APROMALPI LTDA.'),
    ('20484328162','COOPERATIVA AGRARIA DE PRODUCTORES ORGANICOS AMPBAO'),
    ('20486973219','COOPERATIVA AGRARIA SONOMORO DEL VRAEM LTDA'),
    ('20525955843','COOPERATIVA AGRARIA ECOLOGICA Y SOLIDARIA PIURA'),
    ('20526179367','COOPERATIVA AGRARIA ASPRAOSRA LTDA'),
    ('20601710456','COOPERATIVA AGRARIA DE PRODUCTORES PERUANOS ORGANICOS'),
    ('20603557825','COOPERATIVA AGRARIA KAFFEE SATIPO'),
    ('20603734255','COOPERATIVA AGROINDUSTRIAL MISHAGRO'),
    ('20604409811','COOPERATIVA AGRARIA DE USUARIOS RIO Y VALLE'),
    ('20607105929','COOPERATIVA AGRARIA DE SERVICIOS MULTIPLES APAGA'),
    ('20608057529','COOPERATIVA AGRARIA EXPORTADORA DE PRODUCTOS ORGANICOS DON A'),
]

pac_files = [
    r'C:\Users\acuba\eudrperu\Directorio Cooperativas Cafe-Cacao Peru (v3 - Cepicafe-Norandino).xlsx',
    r'C:\Users\acuba\eudrperu\Directorio Cooperativas Cafe-Cacao Peru.xlsx',
]

all_pac = []  # list of (name, ruc, region, producto)

for pac_path in pac_files:
    try:
        wb = openpyxl.load_workbook(pac_path, data_only=True, read_only=True)
        ws = wb.active
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row[0]:  # nombre usual
                all_pac.append({
                    'nombre': str(row[0]).strip(),
                    'ruc': str(row[2]).strip() if row[2] else '',
                    'region': str(row[3]).strip() if row[3] else '',
                    'producto': str(row[4]).strip() if row[4] else '',
                    'fuente': pac_path.split(chr(92))[-1][:30]
                })
        wb.close()
    except Exception as e:
        print(f'Error {pac_path}: {e}')

print(f'Nombres PAC cargados: {len(all_pac)}')

# Search for each new exporter
print('\n--- COINCIDENCIAS EN PAC ---')
for ruc, name in nuevos_nombres:
    name_l = name.lower()
    words_n = set(re.findall(r'\w{4,}', name_l))
    best_match = None
    best_score = 0
    for pac in all_pac:
        pac_l = pac['nombre'].lower()
        words_p = set(re.findall(r'\w{4,}', pac_l))
        shared = words_n & words_p
        # Also check RUC
        if pac['ruc'] == ruc:
            best_match = pac
            best_score = 999
            break
        if len(shared) >= 3 and len(shared) > best_score:
            best_score = len(shared)
            best_match = pac

    if best_match and best_score < 999:
        print(f'  MATCH {ruc}: SUNAT={name[:45]} | PAC={best_match["nombre"]} | RUC PAC={best_match["ruc"]} | score={best_score}')
    elif best_score == 999:
        print(f'  RUC MATCH {ruc}: {best_match["nombre"]} | RUC PAC={best_match["ruc"]}')
    else:
        print(f'  SIN MATCH: {ruc}: {name[:50]}')

# Also check if any nuevos RUC already exist in PAC by RUC
print('\n--- RUC YA EN PAC ---')
pac_rucs = set(p['ruc'] for p in all_pac if p['ruc'])
for ruc, name in nuevos_nombres:
    if ruc in pac_rucs:
        pac_match = next(p for p in all_pac if p['ruc'] == ruc)
        print(f'  {ruc}: {name} -> PAC: {pac_match["nombre"]}')
