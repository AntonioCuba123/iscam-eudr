# -*- coding: utf-8 -*-
"""
Tabla de codificación del Instrumento 2 — opción de respuesta → puntaje 0-100.
Artefacto metodológico: es la «tabla de codificación» que §5 del documento declaraba pendiente.
Regla: puntaje = alineamiento con el EUDR/Pacto Verde (100 = mejor). None = «sin dato»
(no se promedia; la ausencia de respuesta no se convierte en 0).

Ratificación de los 15 ítems [R] (2026-10-15) contra las fuentes originales del
Instrumento 2 — `Instrumentos/Instrumento 2 - Encuesta Cuantitativa.md` (Nota de
puntaje), `Instrumentos/DOC_TRABAJO_Instrumento2_ISCAM_v2.md` (Tabla 5: qué
promedia y qué no por dimensión) y `Instrumentos/Estructura Google Sheet -
Respuestas Instrumento 2.md` (reglas de integridad 3–7):

  · 8 de los 15 ítems [R] no entran a NINGÚN promedio, porque el propio instrumento
    los clasifica como bandera, mapeo, Bloque 0 o Bloque P → ver `NO_PROMEDIA`.
    No se elimina su captura ni su codificación: se reportan por separado.
  · Los 7 restantes sí promedian en su dimensión; su dirección queda ratificada
    (ver `RULING`). Las opciones que expresan desconocimiento siguen siendo «sin dato».

Por la misma regla se retiran del promedio, además, los ítems que no estaban en la
lista [R] pero que el instrumento marca igual: P8/P13/P14 (Bloque P), D5.19a y
D7.28c (mapeo), D3.14g (verificación) y las banderas D2.10, D2.5b, D3.14i y D4.15a.
"""

# ── Reglas directas (sin tabla de opciones) ─────────────────────────────────
REGLAS = {
    "Escala 0-4": "×25 → 0-100",
    "0-100": "valor nativo (validar 0-100)",
    "0/1/2": "÷2 → 0-1 (componente AMBIENTAL de ISA-PV)",
    "check": "puntaje = (n.º de opciones marcadas ÷ n.º total) × 100",
    "check_eu": "puntaje = (% de destinos UE sobre el total marcado) × 100",
    "no_puntua": "no puntúa el índice (identificación, validación o derivada)",
}

# ── Tabla opción → puntaje ──────────────────────────────────────────────────
# qid: (tipo, [(opción, puntaje|None), ...]  |  None + regla)
TABLA = {
 # ── D1 · Clasificación regulatoria ──────────────────────────────────────
 "D1.1":  ("O", [("Sí", 100), ("No", 50)]),                                   # ratificado 2026-10-15
 "D1.2":  ("R", "no_puntua"),                                                  # contexto de rol
 "D1.3":  ("O", [("Sí con certeza", 100), ("Idea aproximada", 50), ("No sabe", None)]),
 "D1.4":  ("O", [("Sí", 100), ("No", 50), ("No sabe", None)]),                 # ratificado 2026-10-15
 "D1.3a": ("O", [("Operador", 100), ("Operador posterior", 100), ("Comerciante", 100),
                 ("Micro o pequeño operador primario", 100), ("No sabe", None)]),
 # ── D2 · Trazabilidad y geolocalización ─────────────────────────────────
 "D2.5":  ("E", None), "D2.7": ("E", None),
 "D2.6":  ("N", None),
 "D2.8":  ("O", [("Técnico propio", 100), ("Consultor", 75), ("Proyecto de cooperación", 50),
                 ("Socio por su cuenta", 25), ("No se ha levantado", None)]),
 "D2.9":  ("O", [("Nunca", 0), ("Al ingreso del socio", 33), ("Anual", 67), ("Por cosecha", 100)]),
 "D2.10": ("O", [("Sí, se mezclan sin control", 0), ("Se mezclan pero con registro de origen", 50),
                 ("No, se mantiene segregación física completa", 100)]),
 "D2.5a": ("O", [("0%, todo proviene de socios", 100), ("Menos del 10%", 75),
                 ("Entre 10% y 30%", 50), ("Más del 30%", 25), ("No se ha cuantificado", None)]),
 "D2.5b": ("O", [("Sí, verificado con georreferencia", 100), ("Sí, pero sin georreferencia", 67),
                 ("Solo nombre y cantidad", 33), ("No se registra", 0), ("No aplica", None)]),
 # ── D3 · Legalidad de la producción ─────────────────────────────────────
 "D3.11": ("N", None), "D3.13": ("E", None),
 "D3.12": ("O", [("Sí, extensa", 0), ("Sí, puntual", 50),
                 ("Sí, en área natural protegida o zona de amortiguamiento", 0),
                 ("No verificado", None), ("No, ninguna", 100)]),              # ratificado 2026-10-15 (severidad)
 "D3.14": ("O", [("Sí", 0), ("No", 100), ("No verificado", None)]),
 "D3.14a":("O", [("Sí, todas las fuentes verificadas", 100), ("Parcialmente", 50),
                 ("No", 0), ("No aplica", None)]),
 "D3.14b":("O", [("Siempre", 100), ("A veces", 50), ("No", 0), ("No aplica", None)]),
 "D3.14c":("O", [("Sí", 0), ("No", 100), ("No sabe", None)]),
 "D3.14d":("O", [("No existe ningún derecho de terceros", 100),
                 ("Existe, pero está registrado y no restringe el uso", 80),
                 ("Existe un acuerdo documentado con el titular o con la autoridad que legitima el uso, aunque la cooperativa o el socio no tenga título formal", 60),
                 ("Existe usufructo, arrendamiento o carga sin acuerdo que lo resuelva", 20),
                 ("Se han invocado derechos de uso tradicional o consuetudinarios por una comunidad o pueblo indígena sin proceso de acuerdo", 0),
                 ("No verificado", None)]),
 "D3.14e":("O", [("Sí, verificado", 100), ("Parcialmente", 50),
                 ("No verificado", None), ("No sabe", None)]),
 "D3.14f":("O", [("Sí, formalizado", 100), ("Informal", 50), ("No existe", 0)]),
 "D3.14g":("O", [("Sí, proceso documentado", 100), ("Aplica pero no se ha realizado", 0),
                 ("No aplica, no hay territorios de este tipo", None), ("No sabe", None)]),
 "D3.14h":("O", [("Sí, vigentes y verificadas", 100), ("Parcial, alguna falta o está vencida", 50),
                 ("No", 0), ("No aplica (sin actividad que la requiera)", None)]),
 "D3.14i":("O", [("Sí, vigente y sin resolver", 0), ("Sí, en proceso de resolución", 50),
                 ("No", 100), ("No sabe", None)]),
 # ── D4 · Riesgo de deforestación ────────────────────────────────────────
 "D4.15": ("O", [("No verificado", None), ("Verificación parcial", 50),
                 ("Verificado sin hallazgos", 75), ("Casos detectados sin resolver", 0),
                 ("Verificado sistemáticamente y documentado", 100)]),         # ratificado 2026-10-15 (verificación)
 "D4.16": ("E", None),
 "D4.17": ("O", [("Sí documentado", 100), ("Idea aproximada", 50), ("No sabe", None)]),
 "D4.15a":("O", [("Sí, detectadas y sin resolver", 0), ("Sí, detectadas y mitigadas o aclaradas", 75),
                 ("No se han detectado", 100), ("No se monitorea", 0)]),
 # ── D5 · Diligencia debida ──────────────────────────────────────────────
 "P8":    ("O", [("Sí", 0), ("No", 100), ("No sabe", None)]),
 "D5.18": ("E", None), "D5.18a": ("E", None),
 "D5.18b":("O", [("No se prioriza, se atiende lo que surge", 0),
                 ("Priorización informal, sin criterio escrito", 50),
                 ("Priorización estructurada con matriz probabilidad×impacto o similar", 100)]),
 "D5.19": ("O", [("No sabe qué es", None), ("No pero lo entiende", 0),
                 ("En proceso", 50), ("Presentada y aceptada", 100)]),
 "D5.19a":("C", 7),
 "D5.20": ("O", [("No", 0), ("Función adicional", 50), ("Dedicado", 100)]),
 "D5.21": ("O", [("No", 0), ("Hace más de 12 meses", 50), ("Sí, reciente", 100)]),
 "D5.21a":("O", [("No hay revisión definida", 0), ("Revisión reactiva, sin frecuencia fija", 50),
                 ("Revisión periódica definida", 100)]),
 "D5.21b":("O", [("No", 0), ("Sí, uso interno solamente", 50),
                 ("Sí, interno y compartido con compradores u otras partes interesadas", 100)]),
 # ── D6 · Capacidad organizacional y digital ─────────────────────────────
 "D6.22": ("O", [("No", 0), ("Parcial, solo actividades de cumplimiento", 33),
                 ("Parcial, incluye tecnología y datos", 67),
                 ("Sí, con partida explícita para tecnología y datos", 100)]),
 "D6.22a":("O", [("No existe", 0), ("Existe en papel desorganizado", 33),
                 ("Existe digital pero sin vínculos entre tablas", 67),
                 ("Existe digital con vínculos actualizados entre socio-parcela-lote", 100)]),
 "D6.22b":("O", [("Excel o Access básico", 25),
                 ("Software especializado de trazabilidad (ChainPoint, Teia, BQuant, otro)", 50),
                 ("Sistema web propio o de tercero", 75),
                 ("Base de datos personalizada con soporte técnico regular", 100)]),
 "D6.23": ("O", [("Papel", 0), ("Mixto", 50), ("Digital", 100)]),
 "D6.24": ("O", [("No hay", 0), ("Limitada", 50), ("Confiable", 100)]),
 "D6.25": ("O", [("No y lo necesita", 0), ("No lo cree necesario", 25),
                 ("Sí en el pasado", 50), ("Sí activo", 100)]),
 "D6.25a":("O", [("No existe política de respaldo", 0), ("Parcial, solo los más críticos", 33),
                 ("Sí, con respaldo definido pero no probado", 67),
                 ("Sí, con protocolo probado periódicamente", 100)]),
 "D6.25b":("O", [("Diseñado internamente", 50), ("Con apoyo de ONG o programa", 50),
                 ("Con apoyo de consultoría o proveedor IT", 50), ("Nunca se ha probado", 0),
                 ("Probado hace más de 12 meses", 50),
                 ("Probado en los últimos 12 meses", 100)]),                   # ratificado 2026-10-15 (última prueba)
 "D6.22c":("O", [("Sí, personal dedicado", 100), ("Parcial, como función adicional", 50),
                 ("No", 0), ("No sabe", None)]),
 # ── D7 · Cadena de valor / presión comprador ────────────────────────────
 "B0.8":  ("X", 12),                                                           # no promedia (Bloque 0)
 "P10":   ("O", [("Sí", 0), ("No", 100), ("No sabe", None)]),                   # no promedia (Bloque P)
 "P13":   ("O", [("No", 0), ("Sí, de forma verbal o informal", 33),
                 ("Sí, como cuestionario de proveedor o documentación formal", 67),
                 ("Sí, como cláusula contractual o condición de pago", 100)]),
 "D7.26": ("O", [("Aún no", 0), ("Informalmente", 50), ("Formalmente por escrito", 100)]),
 "D7.27": ("O", [("Sí", 100), ("No", 0)]),
 "D7.28": ("O", [("No sabe", None), ("Bajo", 33), ("Medio", 67), ("Alto", 100)]),  # no promedia (bandera de urgencia)
 "D7.28b":("O", [("No ha mencionado nada", 0), ("Lo ha mencionado verbalmente sin requisito formal", 33),
                 ("Sí, ha enviado documentación o cuestionario de proveedores", 67),
                 ("Sí, lo ha formalizado como cláusula contractual", 100)]),
 "D7.28c":("C", 8),                                                         # no promedia (mapeo tipo+alcance)
 "D7.26a":("O", [("Sí, empresa de la UE", 100), ("No es de la UE pero está sujeto a CSDDD", 50),
                 ("No", 0), ("No sabe", None)]),
 "D7.26b":("O", [("Sí, con cláusula explícita EUDR o equivalente", 100),
                 ("Sí, pero sin cláusula específica", 50), ("No hay contrato escrito", 0),
                 ("No sabe", None)]),
 # ── D8 · Gobernanza y participación ─────────────────────────────────────
 "D8.29": ("E", None), "D8.30": ("N", None),
 "D8.31": ("O", [("No existe", 0), ("Se pide informalmente", 50),
                 ("Es requisito formal para vender a la cooperativa", 100)]),
 "D8.32": ("O", [("Alta", 0), ("Moderada", 50), ("Baja/estable", 100)]),
 # ── D9 · Sostenibilidad económica ───────────────────────────────────────
 "P14":   ("O", [("No ha intentado", 0), ("Lo intentó pero no cumplió los criterios", 25),
                 ("Sí, recibió financiamiento verde", 100), ("No sabe si aplica a su caso", None)]),
 "D9.33": ("O", [("Costo mayor al 10% del presupuesto anual", 0), ("Entre 3-10%", 50),
                 ("Menor al 3%", 100), ("No se ha estimado", None)]),
 "D9.34": ("O", [("Con crédito o endeudamiento", 33), ("Con recursos propios", 100),
                 ("Existe fuente de financiamiento identificada (verde, cooperación o programa público), aún no ejecutada", 67),
                 ("No ha sido necesario", 100), ("No sabe", None)]),           # ratificado 2026-10-15 (carga financiera)
 "D9.35": ("O", [("Sí, ya ha ocurrido", 0), ("Es un riesgo latente", 50),
                 ("No aplica", None), ("No se ha evaluado", None)]),
 # ── D10 · Confusión certificación/EUDR (bandera informativa, no promedia) ─
 "D10.36": ("O", [("Sí, totalmente", 0), ("Sí, en parte", 33),
                 ("No, sabe que son cosas distintas", 100), ("No tiene certificación", None)]),  # no promedia (bandera)
 "D10.37": ("O", [("Sí", 0), ("No", 100)]),                                      # no promedia (bandera)
 "D10.36a":("O", [("Sí, asesoría especializada en EUDR", 100),
                 ("Solo asesoría genérica de sostenibilidad", 50),
                 ("No ha recibido asesoría", 0), ("No sabe", None)]),           # no promedia (D10 = bandera)
 # ── D11 · Ecosistema de apoyo externo (mapeo, no promedia) ──────────────
 "D11.38": ("Cn", 7),                                                            # no promedia (mapeo/inventario)
 "D11.39": ("R", "no_puntua"),
 "D11.39a":("O", [("Sí", 100), ("En proceso de inscripción", 50),
                 ("No", 0), ("No conoce la plataforma", None)]),                # no promedia (D11 = inventario)
 # ── Pacto Verde D12-D15 (0/1/2 → componente AMBIENTAL de ISA-PV) ────────
 "D12.42": ("O", [("No mide (0)", 0),
                 ("Registra insumos o mide parcialmente, en curso (1)", 1),
                 ("Calculada y verificada por tercero (2)", 2)]),
 "D13.45": ("O", [("No (0)", 0), ("En preparación (1)", 1), ("Publicado (2)", 2)]),
 "D14.51": ("O", [("No (0)", 0), ("En transición, prácticas aisladas (1)", 1),
                 ("Avanzado, procesos establecidos (2)", 2)]),
 "D15.58": ("O", [("No verificado (0)", 0), ("En monitoreo interno (1)", 1),
                 ("Cumple límites UE verificado (2)", 2)]),
 # ── PPWR (peso 0 en ISA-PV hoy) ─────────────────────────────────────────
 "PP1":   ("O", [("Yute reutilizable", 100), ("Yute nuevo de un solo uso", 75),
                 ("Big-bag o saco plástico", 25), ("Saco de papel", 50),
                 ("Otro (especificar)", 50)]),                                 # ratificado 2026-10-15 (reutilización)
 "PP2":   ("O", [("Sí", 100), ("No", 0), ("No sabe", None)]),
}

# Preguntas que no puntúan (identificación, validación, derivadas, desempeño)
NO_PUNTUA = ["M1","M2","M3","B0.1","B0.2","B0.3","B0.4","B0.5","B0.6","B0.7","B0.9","B0.10","B0.11",
             "B0.12","B0.13","B0.14","B0.15","B0.16","B0.17",
             "P1","P1b","P2","P3","P4","P5","P6","P7","P9","P11","P12",
             "R1","R2","R3","R4","R5","R6","R7","R8","R9","R10"]

# ── Ítems que se capturan y codifican pero NO entran a ningún promedio ──────
# Fuente: Instrumento 2 (Nota de puntaje), DOC_TRABAJO v2 (Tabla 5) y
# Estructura Google Sheet (reglas de integridad 3–7). Se reportan por separado.
NO_PROMEDIA = {
    "B0.8":    "Bloque 0 (identificación) — no puntúa; variable de verificación de destinos",
    "P8":      "Bloque P (desempeño) — no puntúa; variable de resultado",
    "P10":     "Bloque P (desempeño) — no puntúa; variable de resultado",
    "P13":     "Bloque P (desempeño) — no puntúa; variable de resultado",
    "P14":     "Bloque P (desempeño) — no puntúa; variable de resultado",
    "D2.10":   "Bandera de mezcla de lotes — se reporta aparte; no promedia en D2",
    "D2.5b":   "Bandera de trazabilidad de proveedores externos — no promedia en D2",
    "D3.14g":  "Verificación CLPI — no promedia en D3",
    "D3.14i":  "Bandera de saneamiento OEFA/SINEFA — no promedia en D3",
    "D4.15a":  "Bandera de alertas de deforestación — no promedia en D4",
    "D5.19a":  "Mapeo de componentes del plan — insumo del Instrumento 4; no promedia en D5",
    "D7.28":   "Indicador de urgencia (riesgo percibido) — se reporta aparte; no promedia en D7",
    "D7.28c":  "Mapeo tipo/alcance de la documentación del comprador — no promedia en D7",
    "D10.36":  "Bandera de falsa seguridad (certificación ≠ EUDR) — se reporta aparte",
    "D10.37":  "Bandera (oferta de «certificación EUDR») — se reporta aparte",
    "D10.36a": "Asesoría EUDR — D10 es bandera pura (no promedia): se reporta aparte",
    "D11.38":  "Mapeo/inventario de actores — insumo del Instrumento 4; no promedia",
    "D11.39a": "D11 es inventario — se reporta por pregunta; no promedia",
}

# ── Dirección ratificada de los ítems [R] que sí promedian (2026-10-15) ─────
RULING = {
    "D1.1":  "Ratificado: 100 = introduce bajo su propio nombre (operador directo); 50 = vende a través de un tercero",
    "D1.4":  "Ratificado: 100 = cumple el umbral micro/pequeña empresa (Directiva 2013/34/UE), que define su régimen simplificado",
    "D3.12": "Ratificado: severidad de la superposición — ninguna 100 · puntual 50 · extensa 0 · ANP/zona de amortiguamiento 0",
    "D4.15":  "Ratificado: eje de verificación del cambio de uso post-31-dic-2020 — «casos detectados sin resolver» = 0",
    "D6.25b": "Ratificado: manda la última prueba (nunca 0 · >12 meses 50 · últimos 12 meses 100); el origen del protocolo es contexto (50)",
    "D9.34":  "Ratificado: carga financiera — recursos propios 100 · fuente identificada 67 · crédito 33 · no ha sido necesario 100",
    "PP1":    "Ratificado: escala de reutilización (yute reutilizable > yute nuevo > papel > plástico); alimenta PPWR, no el ISA-EUDR",
}

# Preguntas que promedian por dimensión (fuente: DOC_TRABAJO v2, Tabla 5;
# ajustado con las banderas/mapeos de la Estructura Google Sheet v0.4).
DIMS = [
    ("D1",  ["D1.1", "D1.3", "D1.4", "D1.3a"]),
    # D2.10a promedia (0/50/100). D2.10 y D2.5b son banderas y quedan fuera.
    ("D2",  ["D2.5", "D2.6", "D2.7", "D2.8", "D2.9", "D2.10a", "D2.5a"]),
    ("D3",  ["D3.11", "D3.12", "D3.13", "D3.14", "D3.14a", "D3.14b", "D3.14c", "D3.14d",
             "D3.14e", "D3.14f", "D3.14h"]),
    ("D4",  ["D4.15", "D4.16", "D4.17"]),
    ("D5",  ["D5.18", "D5.18a", "D5.18b", "D5.19", "D5.20", "D5.21", "D5.21a", "D5.21b"]),
    ("D6",  ["D6.22", "D6.22a", "D6.22b", "D6.22c", "D6.23", "D6.24", "D6.25", "D6.25a", "D6.25b"]),
    ("D7",  ["D7.26", "D7.26a", "D7.26b", "D7.27", "D7.28b"]),
    ("D8",  ["D8.29", "D8.30", "D8.31", "D8.32"]),
    ("D9",  ["D9.33", "D9.34", "D9.35"]),
    ("D10", []),        # bandera pura: D10.36, D10.37 y D10.36a se reportan aparte, no promedian
    ("D11", []),
]
