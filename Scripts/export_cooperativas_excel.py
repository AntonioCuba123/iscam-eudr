import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

data = [
    {
        'Item': 1,
        'Cooperativa': 'Cooperativa Agraria Cafetalera Chancamayo Ltda N 008-B-VII',
        'Lo que dicen las fuentes publicas': 'Registrada en MIDAGRI 2022 como Cooperativa Agraria Frutivalc Chancamayo en Cusco; sin RUC publico; actividad principal cafe y cacao; 80 socios totales (51 hombres, 29 mujeres)',
        'Fuentes publicas consultadas': 'MIDAGRI Cooperativas Agrarias 2026 (registro 0264-2022)'
    },
    {
        'Item': 2,
        'Cooperativa': 'Cooperativa Agraria Cafetalera Aguilayoc Ltda. 084',
        'Lo que dicen las fuentes publicas': 'Fundada 6 abril 1980 por 37 agricultores; Cusco; 25 socios (2024); certificacion organica y comercio justo; marca Aguilayoc; Buen Contribuyente SUNAT desde 2018; exporta a EE. UU. y Europa',
        'Fuentes publicas consultadas': 'Junta Nacional del Cafe (socios) · Festival Yo Tomo Cafe Peruano 2024 (gob.pe) · Lista Buenos Contribuyentes SUNAT 2018 · REUNAT 2025'
    },
    {
        'Item': 3,
        'Cooperativa': 'Cooperativa Agraria Cafetalera Mateo Pumacahua Ltda. 185',
        'Lo que dicen las fuentes publicas': 'Beneficiaria AGROIDEAS 2020 (plan de negocio cafe, Junin/Satipo); 75 socios, 365 ha; sin RUC publico; sin web propia',
        'Fuentes publicas consultadas': 'AGROIDEAS Relacion de Organizaciones Incentivo Tecnologia 2020 (p. 3)'
    },
    {
        'Item': 4,
        'Cooperativa': 'Central de Cooperativas Agrarias Cafetaleras Cocla Ltda. Nro 281',
        'Lo que dicen las fuentes publicas': 'Cooperativa de 2 grado; 21 cooperativas base; 3,500 familias; Cusco/La Convencion; cafe, cacao, te; Fairtrade/CLAC; gerente Vladimir Vivanco (rep. Red Cafe CLAC Peru); exporta a Belgica, Dinamarca, Paises Bajos, Suecia; US$ 322M FOB 2025',
        'Fuentes publicas consultadas': 'Web oficial cocla.pe · Comercio Justo perfil COCLA · Fairtrade Coffee Forum 2026 (Vivanco bio) · RUC.pe · JNC socios · SUNAT agentes retencion IGV 2018'
    },
    {
        'Item': 5,
        'Cooperativa': 'Cooperativa Agraria Cafetalera La Florida',
        'Lo que dicen las fuentes publicas': 'Fundada 1966 (59 anos); 450 socios; Junin/Pasco (Selva Central); organica + Fairtrade; 2 centrales beneficio humedo, 2 centros acopio; fincas 2-4 ha en 18 caserios; exporta via Algrano; marca propia',
        'Fuentes publicas consultadas': 'Web oficial lafloridacac.com · Central Cafe y Cacao socios · Algrano seller profile · AGROIDEAS 2020 · Festival Yo Tomo Cafe 2024'
    },
    {
        'Item': 6,
        'Cooperativa': 'Cooperativa Agraria Cafetalera Ccochapampa Ltda.',
        'Lo que dicen las fuentes publicas': 'Inscrita en padrones SUNAT Cusco 2004 (Res. REFT Acogimiento 017204); Cusco; sin web propia; aparece en lista AGROIDEAS 2020 (92 socios, 246 ha, Cajamarca? - posible homonima)',
        'Fuentes publicas consultadas': 'SUNAT Padrones Notificaciones Cusco 2004 (p061004111.htm) · AGROIDEAS 2020'
    },
    {
        'Item': 7,
        'Cooperativa': 'Cooperativa Agraria Cafetalera Tirijuay Pavayoc Ltda 13-B-VII',
        'Lo que dicen las fuentes publicas': 'Beneficiaria AGROIDEAS 2020 (plan de negocio cafe, Cusco/La Convencion/Ocobamba); 92 socios, 246 ha; inversion S/ 775,598; 94% ejecucion; sin RUC publico',
        'Fuentes publicas consultadas': 'AGROIDEAS Relacion de Organizaciones Incentivo Tecnologia 2020 (p. 4)'
    },
    {
        'Item': 8,
        'Cooperativa': 'Cooperativa Agraria Cafetalera Jorge Chavez Ltda.',
        'Lo que dicen las fuentes publicas': 'Aparece en universo consolidado EUDRPERU (RUC 20200880448); sin web publica; sin mencion en JNC, AGROIDEAS, MIDAGRI, SUNAT padrones recientes',
        'Fuentes publicas consultadas': 'EUDRPERU_universo_consolidado.csv (corpus local)'
    },
    {
        'Item': 9,
        'Cooperativa': 'Cooperativa Agraria Cafetalera CASIL LTDA',
        'Lo que dicen las fuentes publicas': 'Fundada 6 enero 1966; San Ignacio, Cajamarca; una de las primeras y mas grandes del Nororiente; oro en Federacion Alemana de Tostadores 2023 (cafe Rosa Elvita, Santos Acha Rivera); compradores directos Alemania/Hamburgo; exporta a Sustainable Harvest (US) Fairtrade + Organico IMOCERT; Ruta Productiva Exportadora 2023 admitida',
        'Fuentes publicas consultadas': 'Web oficial coopcasil.pe · Checkin Networks (premio Alemania) · ImportKey (exportaciones US) · Ruta Productiva Exportadora 2023-I (admitida) · JNC socios · SUNAT Buenos Contribuyentes 2018'
    },
    {
        'Item': 10,
        'Cooperativa': 'Cooperativa Agraria Valle Grande',
        'Lo que dicen las fuentes publicas': 'Exportadora registrada en JNC Ene-Jun 2024 (US$ 939,006 FOB, 2,204 kg?); aparece en EXPO 2024 SGrains; San Martin; sin web propia',
        'Fuentes publicas consultadas': 'JNC Exportaciones Ene-Jun 2024 · SGrains EXPO 2024 · EUDRPERU_universo_consolidado.csv'
    },
    {
        'Item': 11,
        'Cooperativa': 'Cooperativa Agraria Valle del Biavo Ltda',
        'Lo que dicen las fuentes publicas': 'Marca Cafe Biavo en Festival Yo Tomo Cafe Peruano 2024 (San Martin); sin RUC publico; sin web; no aparece en JNC socios ni AGROIDEAS',
        'Fuentes publicas consultadas': 'Festival Yo Tomo Cafe Peruano 2024 (gob.pe/devida)'
    },
    {
        'Item': 12,
        'Cooperativa': 'Cooperativa Agraria Ecológica Cafetalera de Lonya Grande',
        'Lo que dicen las fuentes publicas': 'Emprendimiento cooperativo de productores de cafe amazonicos; 851 socios (2022); Amazonas/Utcubamba/Lonya Grande; certificada organica; Ruta Productiva Exportadora 2023 admitida; sede Festival Cafes Especiales Amazonas 2026; registro MIDAGRI 2022',
        'Fuentes publicas consultadas': 'JNC socios · Ruta Productiva Exportadora 2023-I (admitida) · GORE Amazonas Festival 2026 · MIDAGRI Registro Nacional Cooperativas 281223.xls'
    },
    {
        'Item': 13,
        'Cooperativa': 'Asociacion de Productores Selva Nororiental - APROSELVANOR',
        'Lo que dicen las fuentes publicas': 'Constituida 2015; 49 socios -> 76 familias beneficiadas; Moyobamba, San Martin; certificacion organica + Fairtrade; 12 contenedores internacionales + 15 nacionales/ano; centro acopio financiado AGROIDEAS/MIDAGRI/Banco Mundial; preparada para EUDR (MIDAGRI 2025); Helvetas/SECO Suiza',
        'Fuentes publicas consultadas': 'MIDAGRI noticia 747793 (inauguracion centro acopio 2024) · AGROIDEAS Facebook · PeruMarketplace · MIDAGRI noticia 1304423 (preparacion EUDR 2025) · FoodNewsLatam (Alianza Cafe Sostenible 2019-2022)'
    },
    {
        'Item': 14,
        'Cooperativa': 'Cooperativa Agraria de Familias Campesinas Emprendedoras y Resilientes del Peru - CAFCER',
        'Lo que dicen las fuentes publicas': 'Sin hallazgo en fuentes publicas consultadas (JNC, MIDAGRI, AGROIDEAS, SUNAT, web, PeruMarketplace, gob.pe)',
        'Fuentes publicas consultadas': 'Ninguna fuente publica localizada'
    },
    {
        'Item': 15,
        'Cooperativa': 'Cooperativa Agraria Yuraq Yacu',
        'Lo que dicen las fuentes publicas': 'MIDAGRI 2025: inscripcion 0788-2025; Pasco/Oxapampa/Villa Rica; agricola; cafe + cacao; 25 socios (13H/12M); sin RUC publico',
        'Fuentes publicas consultadas': 'MIDAGRI Cooperativas Agrarias 2026 (registro 0788-2025)'
    },
    {
        'Item': 16,
        'Cooperativa': 'Cooperativa Agraria Cafetalera OCUMAL',
        'Lo que dicen las fuentes publicas': 'Fundada 2016; Luya, Amazonas; 343 ha (1200-2200 msnm); variedades Tipica, Catuaí, Borbon, Caturra, Villa Sarchí, Catimor; proyeccion 297 TM 2023; cafe organico especialidad; exportacion directa; Ruta Productiva 2023 admitida; UN Global Compact; donacion Municipalidad Luya 2025 (R.D. 112-2025)',
        'Fuentes publicas consultadas': 'Web oficial coopocumal.com · PeruMarketplace perfil · Ruta Productiva Exportadora 2023-I · UN Global Compact · Municipalidad Luya R.D. 112-2025 · EmpresasRUC'
    },
    {
        'Item': 17,
        'Cooperativa': 'Cooperativa Agraria Ecológica De Mujeres Cafetaleras Villa Rica (CEMCVIR)',
        'Lo que dicen las fuentes publicas': 'Primera cooperativa de mujeres en Pasco; 83 socias (79 mujeres); 100% organico; fincas trazables (9 items, 6 fincas, contratos 13-49339 a 13-49407, US$ 205,604 FOB 2025); socio comercial edles aus peru (Alemania) que incentivo y ayudo la formacion; Proyecto Semilla (sello Libre de Trabajo Infantil, OIT/USDOL); Lab Moali; exporta DE/BE',
        'Fuentes publicas consultadas': 'Web oficial cemcavir.com · Pagina Partners (edles aus peru, Semilla, Moali) · Pagina Quienes Somos · DUAs SUNAT 2025 (corpus local) · MIDAGRI 2025 (inscripcion 0899-2025)'
    },
    {
        'Item': 18,
        'Cooperativa': 'Cooperativa Agraria Ecologico Rosas Pampa Ltda - Caeco Rosas Pampa Ltda',
        'Lo que dicen las fuentes publicas': 'MIDAGRI 2026: inscripcion 0959-2026; Junin/Chanchamayo; cafe; 58 socios (35H/23M); sin RUC publico',
        'Fuentes publicas consultadas': 'MIDAGRI Cooperativas Agrarias 2026 (registro 0959-2026)'
    },
    {
        'Item': 19,
        'Cooperativa': 'Asociacion Agroexportadora de la Region San Martin',
        'Lo que dicen las fuentes publicas': 'RUC 20530336281 (exportadora banano organico Piura/Sullana, no cafe); 25 socios; GlobalGAP + Fairtrade + Organico; Valle del Chira; web agronortecooperative.com; tesis PUCP 2021 gestion relacion socios-proveedores',
        'Fuentes publicas consultadas': 'Web oficial agronortecooperative.com · Tesis PUCP repositorio · SEAIR exportaciones · Wix site · UniversidadPeru.com'
    },
    {
        'Item': 20,
        'Cooperativa': 'Cooperativa Agraria de Servicios Multiples Cordillera Azul',
        'Lo que dicen las fuentes publicas': 'RUC 20572145388; Ucayali/San Martin; cafe + cacao; marca Cafe Oro de Montana (Festival Yo Tomo Cafe 2024); exportadora JNC 2024 (Alemania, Reino Unido, EE. UU., US$ 1.34M FOB); admitida Ruta Productiva 2023?',
        'Fuentes publicas consultadas': 'Festival Yo Tomo Cafe 2024 · EUDRPERU_universo_consolidado.csv (exp 2026) · JNC Exportaciones 2024'
    },
    {
        'Item': 21,
        'Cooperativa': 'Cooperativa Agraria Tropical Products',
        'Lo que dicen las fuentes publicas': 'Probable error tipografico (Agraria vs Agria); sin hallazgo en JNC, MIDAGRI, AGROIDEAS, SUNAT, PeruMarketplace, gob.pe, web',
        'Fuentes publicas consultadas': 'Ninguna fuente publica localizada'
    },
    {
        'Item': 22,
        'Cooperativa': 'Asociacion de Productores Agroecologicos San Juan - APROCASJ',
        'Lo que dicen las fuentes publicas': 'MIDAGRI 2024: inscripcion 0598-2024; Amazonas/Utcubamba; cafe; 25 socios (13H/12M); sin RUC publico',
        'Fuentes publicas consultadas': 'MIDAGRI Cooperativas Agrarias 2026 (registro 0598-2024)'
    },
    {
        'Item': 23,
        'Cooperativa': 'Cooperativa Agraria de Productores Ecologicos los Chankas Valle del Rio Perene',
        'Lo que dicen las fuentes publicas': 'Beneficiaria AGROIDEAS 2020 (plan cafe, Junin/Chanchamayo/Pichanaki); 35 socios, 354 ha; inversion S/ 553,806; 99% ejecucion; MIDAGRI 2024 inscripcion 0787-2024 (Caeco Rosas Pampa?); sin RUC publico',
        'Fuentes publicas consultadas': 'AGROIDEAS 2020 (p. 5) · MIDAGRI 2026 (registro 0787-2024)'
    },
    {
        'Item': 24,
        'Cooperativa': 'Asociacion de Productores Cerro Blanco',
        'Lo que dicen las fuentes publicas': 'Sin hallazgo en fuentes publicas consultadas; aparece como clave origen 1005 en corpus local DUAs (exportador asociado)',
        'Fuentes publicas consultadas': 'EUDRPERU corpus local (clave_origen 1005 en DETALLE_ITEMS)'
    },
    {
        'Item': 25,
        'Cooperativa': 'Cooperativa Agraria Line Coffee Marañon',
        'Lo que dicen las fuentes publicas': 'Marca Line Coffee en Festival Yo Tomo Cafe 2024 (Amazonas); exportadora JNC Ene-Jun 2024 (US$ 69,944 FOB, 412.5 kg); MIDAGRI 2025 inscripcion 0741-2025 (Ceja de Selva V.R., Amazonas/Bagua?); sin RUC publico',
        'Fuentes publicas consultadas': 'Festival Yo Tomo Cafe 2024 · JNC Exportaciones Ene-Jun 2024 · MIDAGRI 2026 (registro 0741-2025)'
    }
]

df = pd.DataFrame(data)

wb = Workbook()
ws = wb.active
ws.title = 'Cooperativas_Fuentes_Publicas'

header_font = Font(bold=True, color='FFFFFF', size=11)
header_fill = PatternFill(start_color='2F5496', end_color='2F5496', fill_type='solid')
header_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
cell_alignment = Alignment(vertical='top', wrap_text=True)
thin_border = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)

headers = ['Item', 'Cooperativa', 'Lo que dicen las fuentes publicas', 'Fuentes publicas consultadas']
for col, header in enumerate(headers, 1):
    cell = ws.cell(row=1, column=col, value=header)
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = header_alignment
    cell.border = thin_border

for row_idx, row_data in enumerate(data, 2):
    for col_idx, key in enumerate(headers, 1):
        cell = ws.cell(row=row_idx, column=col_idx, value=row_data[key])
        cell.alignment = cell_alignment
        cell.border = thin_border

ws.column_dimensions['A'].width = 8
ws.column_dimensions['B'].width = 55
ws.column_dimensions['C'].width = 80
ws.column_dimensions['D'].width = 70

ws.freeze_panes = 'A2'

ws2 = wb.create_sheet('Resumen_Cobertura')
resumen_data = [
    ['Categoria', 'Cantidad'],
    ['Total cooperativas analizadas', 25],
    ['Con al menos 1 fuente publica verificable', 23],
    ['Con RUC confirmado en fuentes publicas', 13],
    ['En Junta Nacional del Cafe (socios/exportaciones)', 10],
    ['Beneficiarias AGROIDEAS 2020', 6],
    ['En registro MIDAGRI 2025-2026 vigente', 10],
    ['Admitidas en Ruta Productiva Exportadora 2023 (PROMPERU)', 4],
    ['Con cooperacion internacional documentada', 7],
    ['Sin ninguna fuente publica localizada', 2],
    ['Solo en corpus local (DUAs/SUNAT)', 3],
]

for row_idx, row_data in enumerate(resumen_data, 1):
    for col_idx, val in enumerate(row_data, 1):
        cell = ws2.cell(row=row_idx, column=col_idx, value=val)
        cell.border = thin_border
        cell.alignment = Alignment(vertical='top', wrap_text=True)
        if row_idx == 1:
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = header_alignment

ws2.column_dimensions['A'].width = 55
ws2.column_dimensions['B'].width = 15

output_path = r'C:\Users\acuba\eudrperu\docs\cooperativas_fuentes_publicas.xlsx'
wb.save(output_path)
print(f'Guardado en: {output_path}')