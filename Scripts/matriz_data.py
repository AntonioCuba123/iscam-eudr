# -*- coding: utf-8 -*-
# Fuente única de datos para la Matriz de Cobertura Técnica — nivel de pregunta.
# Cada tupla: (bloque, id, pregunta_corta, eudr, pasos_dd, otras_fuentes, ruta_ip, ruta_iv)
# "=" en cualquier columna significa "hereda el valor de la dimensión padre" (ver DIM_DEFAULTS)
# 2026-09-17: columna única "ISCAM (IP/IV/RE)" partida en "Ruta a IP" y "Ruta a IV" a pedido del usuario,
# para poder leer por separado cómo decanta cada pregunta en cada índice antes de RE = IV·(1−IP/100).
# 2026-10-08: agregados D12 (Huella carbono), D13 (Reporte sostenibilidad), D14 (Economía circular) — módulos Pacto Verde i, iv, v.

DIM_DEFAULTS = {
    "Bloque 0": (
        "Art. 9(1) — datos identificatorios del operador/producto/cantidad",
        "Paso 2.1 — mapeo de cadena de suministro (Tabla 3)",
        "—",
        "No entra a IP (Bloque 0 es identificación, no madurez)",
        "No entra directo; alimenta IV1/IV3/IV5 vía preguntas específicas de esta sección",
    ),
    "D1": (
        "Art. 2 (definiciones de operador) · Art. 3 (obligación general)",
        "No corresponde a un paso específico",
        "—",
        "Fuera de IP (estatus jurídico, no capacidad)",
        "IV2 completo — directo, recodificado 0–100",
    ),
    "D2": (
        "Art. 9(1)(d)–(f) (geolocalización) · Art. 10 (prohibición de mezcla)",
        "Paso 2.1 — mapeo de cadena de suministro (Tabla 3)",
        "—",
        "IP1 — directa (Trazabilidad y origen)",
        "No entra a IV",
    ),
    "D3": (
        "Art. 3(b) y Art. 2(40) — 8 letras (a)–(h) de legislación pertinente; la Tabla 6 del manual PROMPERÚ/BID las agrupa en 7 filas",
        "Paso 2.2.2.1.2 — riesgo de legalidad (Tabla 6)",
        "Doc. orientador ADEX/MIDAGRI/EFI",
        "IP2 — geométrica con D4: √(D3×D4)",
        "No entra a IV",
    ),
    "D4": (
        "Art. 2(13)–(14) (deforestación, corte 31-dic-2020) · Art. 9",
        "Paso 2.2.2.1.1 — riesgo de deforestación (Fig. 4)",
        "Doc. orientador ADEX/MIDAGRI/EFI (línea base 45%/25%)",
        "IP2 — geométrica con D3: √(D3×D4)",
        "No entra a IV",
    ),
    "D5": (
        "Art. 8 (sistema de DD) · Art. 9–11 · Art. 12 (declaración)",
        "Los 5 pasos completos",
        "Manual OCDE-FAO (2024)",
        "IP3 — aritmética junto con D8 y D6 parcial: (D8+D5+D6_sistemas)/3",
        "No entra a IV",
    ),
    "D6": (
        "No hay artículo específico — prerrequisito operativo",
        "Paso 3.1 — recursos del plan (componente 2)",
        "—",
        "IP3 parcial (D6.22/D6.25) + IP4 directa (D6.23)",
        "IV4 — D6.24 invertida: (100−D6.24)",
    ),
    "D7": (
        "No hay artículo específico — presión comercial del comprador",
        "No corresponde a un paso específico",
        "—",
        "IP5 — aritmética (relación con compradores)",
        "IV5 — invertida: (100−D7)",
    ),
    "D8": (
        "No hay artículo específico",
        "Paso 1 (sensibilización) · Paso 3.1 (consulta)",
        "—",
        "IP3 — aritmética (match directo \"Gobernanza\")",
        "IV5 parcial — solo fracción de fricción/resistencia, no toda la dimensión",
    ),
    "D9": (
        "No hay artículo específico",
        "Paso 3.1 — recursos financieros (componente 2)",
        "—",
        "IP5 — aritmética (\"Financiamiento\")",
        "IV4 — invertida, junto con D6.24",
    ),
    "D10": (
        "Art. 30 — certificación no sustituye la diligencia debida",
        "No corresponde a ningún paso",
        "—",
        "Fuera de IP — bandera de alerta aparte, nunca absorbida",
        "No entra a IV",
    ),
    "D11": (
        "No hay artículo específico",
        "Alineado con Fig. 4 (herramientas/actores estatales)",
        "Doc. orientador ADEX/MIDAGRI/EFI",
        "IP5 recalculado — % actores activos de D11.38, regla propia solo para IP",
        "No entra a IV",
    ),
    "D12": (
        "Pacto Verde módulo (i) — Taxonomía UE, CSRD, CBAM; CalCafé v2.1 (PromPerú/PUCP-PELCAN, ISO 14040/44, PEFCR) para café; cacao sin equivalente identificado",
        "No corresponde a un paso del manual EUDR — módulo transversal de preparación Pacto Verde",
        "CalCafé v2.1 (manual de uso 2021); IPCC Guidelines; GHG Protocol",
        "Fuera de ISA-EUDR — entra a ISA-PactoVerde (media aritmética D12–D14)",
        "No entra a IV",
    ),
    "D13": (
        "Pacto Verde módulo (iv) — CSRD/ESRS, Taxonomía verde UE, SFDR, NFRD legado",
        "No corresponde a un paso del manual EUDR — módulo transversal de preparación Pacto Verde",
        "GRI Standards, ESRS simplificado (EFRAG), Directiva CSRD (UE) 2022/2464",
        "Fuera de ISA-EUDR — entra a ISA-PactoVerde (media aritmética D12–D14)",
        "No entra a IV",
    ),
    "D14": (
        "Pacto Verde módulo (v) — Plan Acción Economía Circular UE, PPWR (Reglamento envases), Estrategia 'De la granja a la mesa'",
        "No corresponde a un paso del manual EUDR — módulo transversal de preparación Pacto Verde",
        "Directiva 94/62/CE (envases), PPWR propuesta, Plataforma Europea de Economía Circular",
        "Fuera de ISA-EUDR — entra a ISA-PactoVerde (media aritmética D12–D14)",
        "No entra a IV",
    ),
    "Bloque P": (
        "No hay artículo específico — variable de resultado",
        "No corresponde a ningún paso",
        "Objetivo (f) proyecto madre ISCAM",
        "No entra a IP",
        "IV1 — P1/P1b (numerador/denominador), P4 (concentración = 100/P4)",
    ),
}

# columnas: bloque, id, pregunta, eudr, pasos, otras, ruta_ip, ruta_iv  ("=" hereda default del bloque)
ROWS = [
# ---------------- BLOQUE 0 ----------------
("Bloque 0","0.1","Nombre de la cooperativa / razón social","Art. 9(1)(a) — identificación del operador","=","=","=","="),
("Bloque 0","0.2","RUC (clave de deduplicación del marco muestral)","Art. 9(1)(a)","=","=","=","="),
("Bloque 0","0.3","Producto(s) exportado(s) / código SA","Anexo I — lista de materias primas cubiertas (café, cacao, madera)","=","=","=","="),
("Bloque 0","0.4","N.º de socios / hectáreas totales asociadas","—","Tabla 3 — \"tamaño de finca\"","—","No entra a IP","Alimenta IV3 (tamaño de parcela = hectáreas/socios, derivado)"),
("Bloque 0","0.5","¿Exporta directo a la UE o a través de un tercero?","Art. 2 — determina el rol (operador / operador posterior)","=","—","No entra a IP directo (informa D1)","Alimenta IV2 (vía D1)"),
("Bloque 0","0.6","Si es indirecto: ¿quién es el comprador que exporta a la UE?","Art. 2","—","—","No entra a IP","Alimenta IV1 (vía D7)"),
("Bloque 0","0.7","Volumen anual aproximado destinado a la UE (%)","Art. 9(1) — cantidad","=","—","No entra a IP","IV1 (estimación rápida, reemplazada por P1/P1b)"),
("Bloque 0","0.8","País(es) de destino dentro de la UE","Art. 9(1)(c) — país de destino","=","—","=","="),
("Bloque 0","0.9","Certificaciones voluntarias vigentes","Art. 30 — no sustituyen la diligencia debida","Fig. 4 / Tabla 5 — certificaciones como criterio de riesgo","—","IP5 recalculado (Certificaciones, conteo 0/33/66/100)","No entra a IV directo (insumo D10)"),
("Bloque 0","0.10","Dispersión geográfica de los socios (insumo IV3)","—","Paso 2.2.2.1.3 — ubicación de acopios (tangencial)","—","No entra a IP","IV3 directo"),
("Bloque 0","0.11","Distancia a centro de acopio (insumo IV3)","—","Paso 2.2.2.1.3","—","No entra a IP","IV3 directo"),
("Bloque 0","0.12","% de mujeres en la directiva (insumo IV5)","—","Fig. 10, componente 7 — atención a productoras mujeres (tangencial)","Estudio Vietnam, Team Europe Initiative (2025)","No entra a IP","IV5 directo — (100−%mujeres_directiva)"),

# ---------------- BLOQUE P ----------------
("Bloque P","P1","Volumen exportado a la UE en el último año","Art. 9(1) — cantidad","=","=","No entra a IP","IV1 — numerador"),
("Bloque P","P1b","Volumen TOTAL exportado a todos los destinos","—","=","=","No entra a IP","IV1 — denominador (cierra brecha, 2026-09-16)"),
("Bloque P","P2","Volumen exportado a la UE hace 3 años (retrospectivo)","—","=","=","No entra a IP","No entra a IV (variable de resultado, no de IP/IV)"),
("Bloque P","P3","Ingreso total por ventas de exportación a la UE","—","=","=","=","="),
("Bloque P","P4","N.º de compradores europeos activos actualmente","—","=","=","No entra a IP","IV1 — concentración = 100/P4"),
("Bloque P","P5","N.º de compradores europeos hace 3 años (retrospectivo)","—","=","=","=","No entra a IV (retrospectivo, variable de resultado)"),
("Bloque P","P6","Precio promedio pagado al socio, último año","—","=","=","No entra a IP","No entra a IV directo — variable de resultado, conecta D9.35"),
("Bloque P","P7","Precio promedio pagado al socio, hace 3 años (retrospectivo)","—","=","=","=","="),
("Bloque P","P8","¿Lote rechazado/observado por comprador europeo?","Art. 3 — consecuencia de no declarar conforme (tangencial)","=","=","=","="),
("Bloque P","P9","N.º aproximado de lotes rechazados u observados","—","=","=","=","="),
("Bloque P","P10","¿Ha perdido contrato/comprador europeo por incumplimiento?","—","=","=","=","No entra a IV directo — variable de resultado, conecta D7.28"),
("Bloque P","P11","% del volumen exportado con trazabilidad verificada hasta parcela","—","=","Comparativa ISA-vs-ISCAM §3.3 — criterio de validación externa ISCAM","No entra a IP directo — se correlaciona contra IP una vez calculado, no es insumo de su fórmula","No entra a IV directo — mismo tratamiento, criterio de validación externa"),
("Bloque P","P12","N.º de años consecutivos exportando a la UE","—","=","Comparativa ISA-vs-ISCAM §3.3 — criterio de validación externa ISCAM (continuidad exportadora)","No entra a IP directo — criterio de validación externa","No entra a IV directo — criterio de validación externa"),

# ---------------- D1 ----------------
("D1","1","¿Introduce el producto directo en el mercado UE bajo su propio nombre?","Art. 2(15) — definición de \"operador\"","=","=","=","="),
("D1","2","¿Transforma el producto (trilla, tostado, fermentado, aserrío)?","Art. 2 — determina \"operador posterior\"","=","=","=","="),
("D1","3","¿Sabe con certeza qué rol le corresponde?","Art. 2 — las 4 categorías de operador/comerciante","=","=","=","="),
("D1","4","¿Cumple los umbrales de micro/pequeña empresa?","Remite a Directiva 2013/34/UE (vía Art. 2 EUDR)","=","=","=","="),

# ---------------- D2 ----------------
("D2","5","¿Existe registro de geolocalización (GPS/polígono) por parcela?","Art. 9(1)(d) — polígono/punto por parcela","=","=","=","="),
("D2","6","% de socios con parcela geolocalizada","Art. 9(1)(d)","Tabla 3 — \"parcela georreferenciada\"","—","=","="),
("D2","7","¿El sistema vincula lote exportado con parcela(s)?","Art. 9(1)(f) — trazabilidad lote-origen","Tabla 3 — trazabilidad","—","=","="),
("D2","8","¿Quién levantó la información de geolocalización?","—","Tabla 2 — importancia del mapeo","—","No entra a IP directo (informa D8, dependencia de terceros)","No entra a IV"),
("D2","9","Frecuencia de actualización del registro","—","Tabla 3 — \"evolución de superficie\" implica actualización","—","IP4 (proxy de monitoreo, junto con D6.23)","No entra a IV"),
("D2","10","¿Se mezclan lotes de distinto origen sin registro? (bandera)","Art. 10 — prohibición de balance de masas","Paso 2.2.2.1.3 — riesgo de mezcla (Fig. 6/7, Tabla 8/9)","—","IP1 (\"Segregación de producto\" — D2.10 es ese componente exacto)","No entra a IV"),

# ---------------- D3 ----------------
("D3","11","% de socios con título de propiedad reconocida","Tabla 6 fila 1 — \"tenencia de la tierra y uso de suelo\" (Art. 2(40)(a))","Paso 2.2.2.1.2 — riesgo de legalidad (Tabla 6)","Doc. ADEX/MIDAGRI/EFI (línea base Cavassa 2022, no verificada)","=","="),
("D3","12","¿Parcelas superpuestas a áreas protegidas/territorios indígenas?","Tabla 6 fila 1 — \"tenencia de la tierra y uso de suelo\" (Art. 2(40)(a))","=","=","=","="),
("D3","13","¿Se verifica cumplimiento laboral a nivel de finca?","Tabla 6 fila 3 — \"normas laborales\" (Art. 2(40)(e); (f) parcialmente)","=","=","=","="),
("D3","14","¿Parcela en zona de desarrollo alternativo/conflicto?","No es criterio del reglamento — contexto","—","—","No entra a IP","IV3 — D3.14 recodificada"),
("D3","14a","¿Socios con autorización de uso de agua?","Art. 2(40)(b) — protección ambiental","Tabla 6 fila 2 — \"permisos ambientales y cumplimiento forestal\"","Doc. orientador ADEX/MIDAGRI/EFI","=","="),
("D3","14b","¿Tratamiento de aguas residuales cumple norma ambiental?","Art. 2(40)(b)","Tabla 6 fila 2","Doc. ADEX/MIDAGRI/EFI (Castro y Julca 2020, 10%)","=","="),
("D3","14c","¿Parcela dentro de faja marginal de río/quebrada/laguna?","Art. 2(40)(b)","Tabla 6 fila 2 (extensión)","Doc. ADEX/MIDAGRI/EFI (mapa de fajas marginales, datosabiertos.gob.pe)","=","="),
("D3","14d","¿Derechos de terceros sobre la parcela o el inmueble (cargas, usufructo, acuerdos constructivos)?","Art. 2(40)(d) — derechos de terceros; DISEÑADA contra esta definición, no por analogía con la Tabla 6 (2026-10-02). La letra (c) — reglas forestales — se declara NO APLICABLE: solo es legislación pertinente cuando se relaciona directamente con la cosecha de madera","Paso 2.2.2.1.2 — riesgo de legalidad; la Tabla 6 (7 filas) no tiene fila para (d)","Comisión Europea C(2024) 7027 §6 \"Legality\" — cargas, usufructo, acuerdos constructivos","IP2 — hereda D3 (√(D3×D4)); promedia en D3, escala 4→0","No entra a IV"),
("D3","14e","¿Al día en obligaciones tributarias/aduaneras/comerciales?","Tabla 6 filas 5 y 6 — \"normativa tributaria y aduanera\" + \"normativa comercial\" (Art. 2(40)(h))","=","Manual PROMPERÚ/BID (origen de la pregunta)","=","="),
("D3","14f","¿Existen mecanismos internos contra la corrupción?","Tabla 6 fila 7 — \"medidas anticorrupción\" (Art. 2(40)(h))","=","Manual PROMPERÚ/BID","=","="),
("D3","14g","¿Proceso de CLPI cuando corresponde? (verificación, no promedia)","Tabla 6 fila 4 — \"CLPI\" (Art. 2(40)(g), no (f))","Tabla 6, fila 4","Doc. ADEX/MIDAGRI/EFI (concluyó: no requisito pertinente a nivel nacional) · Manual PROMPERÚ (origen de la pregunta)","Fuera de IP — verificación aislada, no promedia","Fuera de IV — verificación aislada, no promedia"),

# ---------------- D4 ----------------
("D4","15","¿Se verificó cambio de uso de suelo posterior a dic. 2020?","Art. 2(13)–(14) — definición y corte de deforestación","Tabla 5 — \"fecha de instalación del cultivo\"","—","=","="),
("D4","16","¿Usa herramientas de monitoreo satelital?","Art. 9 — evaluación de riesgo","Fig. 4 — GFW, GeoBosques, Satelligence","—","=","="),
("D4","17","¿Conoce la clasificación de riesgo de su zona?","Art. 9/10 — benchmarking país-riesgo","Tabla 5 — \"aumento de deforestación en el distrito\"","—","=","="),

# ---------------- D5 ----------------
("D5","18","¿Existe procedimiento escrito de diligencia debida?","Art. 8 — sistema de diligencia debida","Transversal a los 5 pasos","=","=","="),
("D5","18a","¿Política de deforestación formal con metas medibles?","Art. 8 (recomendación operativa del manual, no artículo textual propio)","Paso 1 — política de deforestación (Tabla 1)","Manual PROMPERÚ/BID, Paso 1 (origen de la pregunta)","=","="),
("D5","18b","¿Prioriza riesgos con criterio de probabilidad×impacto?","Art. 9 — evaluación de riesgo","Paso 2.3 — priorización de riesgos (Tabla 10)","Manual PROMPERÚ/BID, Paso 2.3","=","="),
("D5","19","¿Ha elaborado/participado en declaración de diligencia debida?","Art. 12 — declaración de diligencia debida","Paso 5 — comunicar (parcial)","=","=","="),
("D5","19a","Componentes del plan de gestión de riesgos (mapeo)","Art. 9–11","Paso 3 — plan de gestión (Fig. 10, 7 componentes)","Manual PROMPERÚ/BID, Paso 3","No entra a IP — mapeo, insumo Instrumento 4","No entra a IV"),
("D5","20","¿Existe responsable designado para el cumplimiento EUDR?","Art. 8 — sistema de diligencia debida","Fig. 10, componente 3 — responsables","—","=","="),
("D5","21","¿Capacitación formal en los últimos 12 meses?","—","Tabla 1 / Fig. 10, componente 6 — capacitación","—","=","="),
("D5","21a","¿El plan se revisa con frecuencia definida?","—","Paso 4 — monitoreo (Fig. 11)","Manual PROMPERÚ/BID, Paso 4","=","="),
("D5","21b","¿Elabora y comunica reporte de diligencia debida con KPIs?","Art. 12 — contenido de la declaración (parcial)","Paso 5 — comunicar (Fig. 12, Tabla 12)","Manual PROMPERÚ/BID, Paso 5","=","="),

# ---------------- D6 ----------------
("D6","22","Presupuesto asignado para cumplimiento EUDR","—","Fig. 10, componente 2 — recursos","—","IP3 parcial (sistemas de gestión)","No entra a IV"),
("D6","23","Digitalización de registros","—","—","—","IP4 directo (junto con D2.9)","No entra a IV"),
("D6","24","Conectividad a internet","—","—","—","No entra a IP (identificado como huérfano de IP, ver Remapeo §3.3)","IV4 — invertida: (100−D6.24) — mejor caso de reúso identificado"),
("D6","25","¿Ha gestionado apoyo externo para adecuarse?","—","Fig. 10, componente 4 — consulta (tangencial)","—","IP3 parcial (apoyo externo)","No entra a IV"),

# ---------------- D7 ----------------
("D7","26","¿El comprador ha exigido geolocalización/DD formalmente?","—","=","—","=","No entra a IV directo"),
("D7","27","¿El comprador ofrece financiamiento/asistencia condicionada?","—","=","—","=","No entra a IV directo"),
("D7","28","Riesgo percibido de perder el contrato si no cumple","—","=","—","No entra a IP (indicador de urgencia, no de madurez)","IV5 — (100−D7) — match directo con \"riesgo de perder el mercado\""),

# ---------------- D8 ----------------
("D8","29","¿Asambleas/reuniones informativas sobre EUDR a los socios?","—","Paso 1 — sensibilización (Tabla 1, match directo)","—","=","No entra a IV (mide esfuerzo institucional, no resistencia del socio — cerrado 2026-09-17, Diseño IV §6)"),
("D8","30","% de socios que entienden por qué se pide geolocalización","—","\"Importancia de la sensibilización\" (§ tras Paso 3.2.1)","—","=","IV5 — fricción_D8 = 100 − D8.30 (único ítem de D8 que entra a IV5; cerrado 2026-09-17, Diseño IV §6)"),
("D8","31","¿Mecanismo interno para que socios entreguen su información?","—","Fig. 10, componente 4 — consulta","—","=","No entra a IV (mide esfuerzo institucional, no resistencia del socio — cerrado 2026-09-17, Diseño IV §6)"),
("D8","32","Rotación de la directiva en los últimos 2 años","—","—","—","=","No entra a IV (mide continuidad, no fricción — cerrado 2026-09-17, Diseño IV §6)"),

# ---------------- D9 ----------------
("D9","33","Costo de adecuación vs. presupuesto anual","—","Fig. 10, componente 2 — recursos","—","=","="),
("D9","34","¿La adecuación se financió con deuda?","—","—","—","No entra a IP directo","="),
("D9","35","¿Riesgo de trasladar el costo al precio pagado al socio?","—","—","—","No entra a IP directo","IV4 — invertida; también variable de resultado vía P6/P7"),

# ---------------- D10 ----------------
("D10","36","¿Cree que su certificación ya cubre las obligaciones EUDR?","Art. 30 — match exacto","=","—","=","="),
("D10","37","¿Le han ofrecido una \"certificación EUDR\" como producto?","No existe tal certificación (sin base legal)","=","—","=","="),

# ---------------- D11 ----------------
("D11","38","Actores con los que ya tiene contacto o apoyo activo","—","Fig. 4 — actores y fuentes estatales","Doc. ADEX/MIDAGRI/EFI (GEOSERFOR, SINIA, OEFA, SENASA, BDPI, SUNAT/VUCE)","=","="),
("D11","39","Actores conocidos pero no contactados, y por qué","—","—","—","No entra a IP directo (insumo Instrumento 4)","No entra a IV"),

# ---------------- D12 — Huella de carbono (Pacto Verde i) ----------------
("D12","40","¿Conoce CalCafé v2.1 o equivalente para cacao?","Pacto Verde módulo (i) — Taxonomía, CSRD, CBAM","—","CalCafé v2.1 (manual 2021), IPCC Guidelines, GHG Protocol","Fuera de ISA-EUDR — entra a ISA-PactoVerde","No entra a IV"),
("D12","41","¿Registra insumos para huella (fertilizantes, combustible, energía, distancia)?","Pacto Verde módulo (i)","—","CalCafé v2.1 (requisitos de datos)","Fuera de ISA-EUDR — entra a ISA-PactoVerde","No entra a IV"),
("D12","42","¿Calculó huella de carbono en los últimos 2 años?","Pacto Verde módulo (i)","—","CalCafé v2.1, ISO 14040/44, PEFCR","Fuera de ISA-EUDR — entra a ISA-PactoVerde","No entra a IV"),
("D12","43","¿Tiene objetivo cuantificado de reducción de emisiones?","Pacto Verde módulo (i) — Taxonomía, CSRD","—","GHG Protocol, Science Based Targets initiative","Fuera de ISA-EUDR — entra a ISA-PactoVerde","No entra a IV"),
("D12","44","¿Reporta huella a compradores o plataformas (CDP, etc.)?","Pacto Verde módulo (i) — CSRD, SFDR","—","CDP, plataformas compradores UE","Fuera de ISA-EUDR — entra a ISA-PactoVerde","No entra a IV"),

# ---------------- D13 — Reporte de sostenibilidad (Pacto Verde iv) ----------------
("D13","45","¿Elabora reporte anual de sostenibilidad / memoria RSE?","Pacto Verde módulo (iv) — CSRD/ESRS, Taxonomía","—","GRI Standards, ESRS simplificado (EFRAG)","Fuera de ISA-EUDR — entra a ISA-PactoVerde","No entra a IV"),
("D13","46","¿Reporte incluye indicadores ambientales (deforestación, carbono, agua, biodiversidad, residuos)?","Pacto Verde módulo (iv)","—","GRI 300, ESRS E1–E5","Fuera de ISA-EUDR — entra a ISA-PactoVerde","No entra a IV"),
("D13","47","¿Reporte incluye indicadores sociales (trabajo infantil, forzoso, igualdad, mujeres, salud)?","Pacto Verde módulo (iv)","—","GRI 400, ESRS S1–S4","Fuera de ISA-EUDR — entra a ISA-PactoVerde","No entra a IV"),
("D13","48","¿Reporte incluye indicadores de gobernanza (directiva, anticorrupción, riesgos, canal denuncias)?","Pacto Verde módulo (iv)","—","GRI 200, ESRS G1–G2","Fuera de ISA-EUDR — entra a ISA-PactoVerde","No entra a IV"),
("D13","49","¿Información verificada/auditada por tercero independiente?","Pacto Verde módulo (iv) — CSRD (auditoría obligatoria)","—","ESRS (verificación limitada → razonable)","Fuera de ISA-EUDR — entra a ISA-PactoVerde","No entra a IV"),
("D13","50","¿Reporte se comparte proactivamente con compradores UE y partes interesadas?","Pacto Verde módulo (iv) — CSRD, taxonomía, expectativas compradores","—","Plataformas compradores UE, CDP","Fuera de ISA-EUDR — entra a ISA-PactoVerde","No entra a IV"),

# ---------------- D14 — Economía circular/envases (Pacto Verde v) ----------------
("D14","51","Gestión residuos beneficio/acopio (cáscara, mucílago, agua miel, trilla)","Pacto Verde módulo (v) — Plan Circular UE, PPWR, 'Granja a mesa'","—","Directiva 94/62/CE, PPWR, Plataforma Economía Circular UE","Fuera de ISA-EUDR — entra a ISA-PactoVerde","No entra a IV"),
("D14","52","Envases exportación (sacos, big-bags, contenedores): reutilizables/reciclables/compostables?","Pacto Verde módulo (v) — PPWR (envases)","—","PPWR propuesta, Directiva 94/62/CE","Fuera de ISA-EUDR — entra a ISA-PactoVerde","No entra a IV"),
("D14","53","Plan de reducción/eliminación plásticos un solo uso (bolsas, film, flejes, etiquetas)","Pacto Verde módulo (v) — PPWR, Directiva plásticos un solo uso","—","Directiva (UE) 2019/904, PPWR","Fuera de ISA-EUDR — entra a ISA-PactoVerde","No entra a IV"),
("D14","54","Subproductos valorizados (cáscara→biocombustible, mucílago→bioinsumos, agua→riego)","Pacto Verde módulo (v) — Economía circular, bioeconomía","—","Plan Acción Bioeconomía UE, Plataforma Economía Circular","Fuera de ISA-EUDR — entra a ISA-PactoVerde","No entra a IV"),
("D14","55","Trazabilidad de envases y residuos por lote exportado","Pacto Verde módulo (v) — PPWR (trazabilidad envases)","—","PPWR Art. 12 (trazabilidad), Digital Product Passport","Fuera de ISA-EUDR — entra a ISA-PactoVerde","No entra a IV"),
]

HEADERS = ["Dimensión", "Pregunta", "EUDR", "5 pasos de debida diligencia", "Otras fuentes citadas", "Ruta a IP", "Ruta a IV"]

def resolve_row(r):
    bloque, qid, texto, eudr, pasos, otras, ip, iv = r
    d_eudr, d_pasos, d_otras, d_ip, d_iv = DIM_DEFAULTS[bloque]
    eudr = d_eudr if eudr == "=" else eudr
    pasos = d_pasos if pasos == "=" else pasos
    otras = d_otras if otras == "=" else otras
    ip = d_ip if ip == "=" else ip
    iv = d_iv if iv == "=" else iv
    return (bloque, qid, texto, eudr, pasos, otras, ip, iv)

RESOLVED = [resolve_row(r) for r in ROWS]

if __name__ == "__main__":
    print(f"Total filas: {len(RESOLVED)}")
