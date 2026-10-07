# -*- coding: utf-8 -*-
import json

data = {
  "20132509876": {"status": 200, "razonSocial": "COOPERATIVA AGRARIA CAFETALERA MARANURA LTDA. 129", "estado": "ACTIVO", "condicion": "HABIDO", "ubigeo": "080904", "direccion": "SN"},
  "20357021058": {"status": 200, "razonSocial": "COOPERATIVA AGRARIA DE PRODUCTORES ORGANICOS APROMALPI LTDA.", "estado": "ACTIVO", "condicion": "HABIDO", "ubigeo": "200401", "direccion": "JR. ICA 100"},
  "20484328162": {"status": 200, "razonSocial": "COOPERATIVA AGRARIA DE PRODUCTORES ORGANICOS AMPBAO", "estado": "ACTIVO", "condicion": "HABIDO", "ubigeo": "200601", "direccion": "CAL. SAN JOSE S/N"},
  "20486973219": {"status": 200, "razonSocial": "COOPERATIVA AGRARIA SONOMORO DEL VRAEM LTDA", "estado": "ACTIVO", "condicion": "HABIDO", "ubigeo": "120606", "direccion": "JR. LAS PALMERAS SN"},
  "20487107949": {"status": 200, "razonSocial": "COOPERATIVA AGRARIA APROSAROCH MAZAMARI LTDA", "estado": "ACTIVO", "condicion": "HABIDO", "ubigeo": "120604", "direccion": "AV. DEL PANGOA"},
  "20525315607": {"status": 200, "razonSocial": "\"COOPERATIVA AGRARIA DE PRODUCTORES AGROPECUARIOS DE PEDREGAL\" - \"CAPAPE\"", "estado": "ACTIVO", "condicion": "HABIDO", "ubigeo": "200114", "direccion": "CAR. PANAMERICANA NORTE"},
  "20525612644": {"status": 200, "razonSocial": "COOPERATIVA AGRARIA DE PRODUCTORES DE MANGO ORGANICO AGRO VIDA", "estado": "ACTIVO", "condicion": "HABIDO", "ubigeo": "200114", "direccion": "CAR. SULLANA-TAMBOGRANDE"},
  "20525955843": {"status": 200, "razonSocial": "COOPERATIVA AGRARIA ECOLÓGICA Y SOLIDARIA PIURA - CAES PIURA", "estado": "ACTIVO", "condicion": "HABIDO", "ubigeo": "200101", "direccion": "CAL. AREQUIPA SUR 1120"},
  "20526179367": {"status": 200, "razonSocial": "COOPERATIVA AGRARIA DE USUARIOS ASPRAOSRA LTDA", "estado": "ACTIVO", "condicion": "HABIDO", "ubigeo": "200402", "direccion": "---- BQ PUEBLO NUEVO"},
  "20568190450": {"status": 200, "razonSocial": "COOPERATIVA AGRARIA KEMITO ENE LTDA. - KEMITO ENE", "estado": "ACTIVO", "condicion": "HABIDO", "ubigeo": "120601", "direccion": "JR. FRANCISCO IRAZOLA 1401"},
  "20601710456": {"status": 200, "razonSocial": "COOPERATIVA AGRARIA DE PRODUCTORES PERUANOS ORGÁNICOS", "estado": "SUSPENSION TEMPORAL", "condicion": "HABIDO", "ubigeo": "200608", "direccion": "CAL. CALLE BOLIVAR CDRA 10 S/N"},
  "20603557825": {"status": 200, "razonSocial": "COOPERATIVA AGRARIA KAFFEE SATIPO", "estado": "ACTIVO", "condicion": "HABIDO", "ubigeo": "120601", "direccion": "CAR. MARGINAL A MAZAMARI 557"},
  "20603734255": {"status": 200, "razonSocial": "COOPERATIVA AGRARIA AGROINDUSTRIAL MISHAGRO", "estado": "ACTIVO", "condicion": "HABIDO", "ubigeo": "120303", "direccion": "AV. MARGINAL 810"},
  "20603820691": {"status": 200, "razonSocial": "COOPERATIVA AGRARIA DE SERVICIOS MULTIPLES CORDILLERA AZUL - CORDILLERA AZUL COOP", "estado": "ACTIVO", "condicion": "HABIDO", "ubigeo": "220201", "direccion": "CAR. F. BELAUNDE TERRY S/N"},
  "20603862369": {"status": 200, "razonSocial": "COOPERATIVA AGRARIA TROPICALS PRODUCTS", "estado": "ACTIVO", "condicion": "HABIDO", "ubigeo": "120303", "direccion": "JR. ANDRES AVELINO CACERES 732"},
  "20604409811": {"status": 200, "razonSocial": "COOPERATIVA AGRARIA DE USUARIOS RIO Y VALLE", "estado": "ACTIVO", "condicion": "HABIDO", "ubigeo": "200601", "direccion": "AV. JOSE DE LAMA 1605"},
  "20604876126": {"status": 200, "razonSocial": "COOPERATIVA AGRARIA AGROINDUSTRIAL INTERCULTURAL ECOLÓGICA SAN JUAN VALLE CHENI LTDA-COOP CHENI LTDA", "estado": "ACTIVO", "condicion": "HABIDO", "ubigeo": "120607", "direccion": "S/N"},
  "20606281804": {"status": 200, "razonSocial": "COOPERATIVA AGRARIA MANASABA LTDA. - MANASABA", "estado": "ACTIVO", "condicion": "HABIDO", "ubigeo": "221001", "direccion": "OTR. SN"},
  "20607105929": {"status": 200, "razonSocial": "COOPERATIVA AGRARIA DE SERVICIOS MULTIPLES APAGA", "estado": "ACTIVO", "condicion": "HABIDO", "ubigeo": "130401", "direccion": "CAL. LIMA 515"},
  "20608057529": {"status": 200, "razonSocial": "COOPERATIVA AGRARIA EXPORTADORA DE PRODUCTOS ORGANICOS DON AUGUSTO", "estado": "ACTIVO", "condicion": "HABIDO", "ubigeo": "200603", "direccion": "CAL. GARCILAZO DE LA VEGA SN"},
  "20609098989": {"status": 200, "razonSocial": "COOPERATIVA AGRARIA CAFETALERA AROMAS FINOS DEL PERU", "estado": "ACTIVO", "condicion": "HABIDO", "ubigeo": "060801", "direccion": "CAL. VIRGEN DEL CISNE 203"},
  "20609224666": {"status": 200, "razonSocial": "COOPERATIVA AGRARIA AGROINDUSTRIAL YACCUMAMA", "estado": "ACTIVO", "condicion": "HABIDO", "ubigeo": "120303", "direccion": "JR. SANTO TORIBIO"}
}

with open(r'C:\Users\acuba\eudrperu\data\resultados_validacion_22.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print('Saved!')
