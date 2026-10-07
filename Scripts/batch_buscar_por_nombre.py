"""
Busca RUCs por nombre en identidad-fiscal (SUNAT local).
Usa writes directas a archivo para evitar buffering.
Query inteligente: COOPERATIVA AGRARIA + nombre propio.
"""
import urllib.request
import urllib.parse
import json
import time
import pandas as pd

BASE_URL = "http://localhost:4006/api/contribuyentes"
OUT_FILE = "data/RUC_busqueda_por_nombre.csv"

def log(msg):
    print(msg, flush=True)

def buscar(nombre: str, limit: int = 3) -> dict:
    params = urllib.parse.urlencode({"razonSocial": nombre, "limit": limit})
    url = f"{BASE_URL}?{params}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read())
    except Exception as e:
        return {"total": 0, "resultados": [], "error": str(e)}

def main():
    # 29 organizaciones sin RUC del PAC
    orgs = [
        ("CAFE PERU", "CAFÉ PERÚ"),
        ("VRAQUS", "VRAQUS"),
        ("CEOACNOR", "CEOACNOR"),
        ("BAGUA GRANDE", "Bagua Grande"),
        ("VALLE RIO APURIMAC", "Valle del Río Apurímac"),
        ("SAN JORGE", "San Jorge"),
        ("CAFE MONTAÑA", "Café Montaña"),
        ("RODRIGUEZ MENDOZA", "Rodríguez de Mendoza"),
        ("CACAO TUMBES", "Cacao Tumbes"),
        ("APROCAP", "APROCAP"),
        ("CEPROAA", "CEPROAA"),
        ("APROCAM", "APROCAM"),
        ("CACAO FRONTERAS", "Cacao Fronteras"),
        ("CHOBA CHOBA", "Choba Choba"),
        ("ORO VERDE", "Oro Verde"),
        ("ASPROC", "ASPROC"),
        ("DIVISORIA", "Divisoria"),
        ("CACAO ALTO HUALLAGA", "Cacao Alto Huallaga"),
        ("PALCAZU", "Palcazú"),
        ("SAN ALEJANDRO", "San Alejandro"),
        ("CAMPOS VERDES", "Campos Verdes"),
        ("PANGOA", "Pangoa"),
        ("CAFE CACAO PERU", "Café y Cacao Perú"),
        ("CACVRA", "CACVRA"),
        ("SAN GABAN", "San Gabán"),
        ("PERENE", "Perené"),
        ("TAHUANTINSUYO", "Tahuantinsuyo"),
        ("ALTO PALOMAR", "Alto El Palomar"),
        ("INCAHUASI", "Incahuasi"),
    ]

    resultados = []
    encontrados = 0
    t = len(orgs)

    log(f"Buscando RUCs para {t} organizaciones...")
    log("")

    for i, (query, display) in enumerate(orgs, 1):
        # Estrategia: buscar con "COOPERATIVA AGRARIA" primero, luego nombre solo
        query_full = f"COOPERATIVA AGRARIA {query}"
        resp = buscar(query_full, limit=3)
        total = resp.get("total", 0)
        error = resp.get("error")
        resultados_list = resp.get("resultados", [])

        if error:
            log(f"[{i}/{t}] ERROR {display}: {error}")
            resultados.append({"nombre": display, "query": query_full, "encontrado": False, "error": error})
            time.sleep(0.3)
            continue

        if total > 0 and total <= 10:
            # Buen match
            r = resultados_list[0]
            encontrados += 1
            log(f"[{i}/{t}] ENCONTRADO {display}: {r['ruc']} | {r['razonSocial']} | {r['estadoContribuyente']}")
            resultados.append({
                "nombre": display,
                "query": query_full,
                "encontrado": True,
                "ruc": r["ruc"],
                "razon_social": r["razonSocial"],
                "estado": r["estadoContribuyente"],
                "condicion": r["condicionDomicilio"],
                "ubigeo": r.get("ubigeo", ""),
                "direccion": r.get("direccion", ""),
            })
        elif total > 10:
            # Demasiados resultados - probar con query mas especifica
            resp2 = buscar(query, limit=3)
            total2 = resp2.get("total", 0)
            resultados2 = resp2.get("resultados", [])
            if 0 < total2 <= 10:
                r = resultados2[0]
                encontrados += 1
                log(f"[{i}/{t}] ENCONTRADO (2da) {display}: {r['ruc']} | {r['razonSocial']} | {r['estadoContribuyente']}")
                resultados.append({
                    "nombre": display,
                    "query": query,
                    "encontrado": True,
                    "ruc": r["ruc"],
                    "razon_social": r["razonSocial"],
                    "estado": r["estadoContribuyente"],
                    "condicion": r["condicionDomicilio"],
                    "ubigeo": r.get("ubigeo", ""),
                    "direccion": r.get("direccion", ""),
                })
            elif total2 > 10:
                log(f"[{i}/{t}] MUCHA AMBIGUEDAD {display}: {total2} resultados - probar manualmente")
                resultados.append({
                    "nombre": display,
                    "query": query,
                    "encontrado": False,
                    "nota": f"{total2} resultados, ambiguedad",
                })
            else:
                log(f"[{i}/{t}] NO ENCONTRADO {display}")
                resultados.append({"nombre": display, "query": query, "encontrado": False})
        else:
            # 0 resultados con query completa - intentar solo nombre
            resp2 = buscar(query, limit=3)
            total2 = resp2.get("total", 0)
            resultados2 = resp2.get("resultados", [])
            if 0 < total2 <= 10:
                r = resultados2[0]
                encontrados += 1
                log(f"[{i}/{t}] ENCONTRADO (nombre) {display}: {r['ruc']} | {r['razonSocial']} | {r['estadoContribuyente']}")
                resultados.append({
                    "nombre": display,
                    "query": query,
                    "encontrado": True,
                    "ruc": r["ruc"],
                    "razon_social": r["razonSocial"],
                    "estado": r["estadoContribuyente"],
                    "condicion": r["condicionDomicilio"],
                    "ubigeo": r.get("ubigeo", ""),
                    "direccion": r.get("direccion", ""),
                })
            elif total2 > 10:
                log(f"[{i}/{t}] MUCHA AMBIGUEDAD {display}: {total2} resultados - investigar")
                resultados.append({
                    "nombre": display,
                    "query": query,
                    "encontrado": False,
                    "nota": f"{total2} resultados, ambiguedad",
                })
            else:
                log(f"[{i}/{t}] NO ENCONTRADO {display}")
                resultados.append({"nombre": display, "query": query, "encontrado": False})

        time.sleep(0.25)

    # Guardar
    df = pd.DataFrame(resultados)
    df.to_csv(OUT_FILE, sep="|", index=False)

    log("")
    log(f"=== RESULTADO: {encontrados}/{t} RUCs encontrados ===")
    log(f"Guardado: {OUT_FILE}")

    found = df[df["encontrado"] == True]
    if len(found) > 0:
        log("")
        log("RUCs encontrados:")
        for _, r in found.iterrows():
            log(f"  {r['ruc']} | {r['razon_social'][:55]} | {r['estado']} | {r['condicion']}")

if __name__ == "__main__":
    main()
