"""
Batch validation de 146 RUCs faltantes contra identidad-fiscal (SUNAT local).
Endpoint: GET http://localhost:4006/api/contribuyentes/{ruc}
"""
import pandas as pd
import urllib.request
import urllib.error
import json
import time
import sys

BASE_URL = "http://localhost:4006/api/contribuyentes"

def consultar_ruc(ruc: str) -> dict:
    url = f"{BASE_URL}/{ruc}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            if resp.status == 200:
                return {"ruc": ruc, "encontrado": True, "data": json.loads(resp.read())}
            else:
                return {"ruc": ruc, "encontrado": False, "status": resp.status, "data": None}
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"ruc": ruc, "encontrado": False, "status": 404, "data": None, "not_found": True}
        return {"ruc": ruc, "encontrado": False, "status": e.code, "data": None, "error": str(e)}
    except Exception as e:
        return {"ruc": ruc, "encontrado": False, "status": None, "data": None, "error": str(e)}

def main():
    # Cargar universo consolidado
    df = pd.read_csv("data/EUDRPERU_universo_consolidado.csv", sep="|", dtype=str)

    # RUCs sin validacion SUNAT
    sin_sunat = df[df["sunat_estado"].isna()].copy()
    rucs = (
        sin_sunat["ruc"]
        .dropna()
        .str.strip()
        .replace("", pd.NA)
        .dropna()
        .tolist()
    )
    rucs = [r for r in rucs if len(r) == 11 and r.isdigit()]

    print(f"=== Batch SUNAT: {len(rucs)} RUCs por consultar ===")
    print(f"API: {BASE_URL}")
    print()

    encontrados = []
    no_encontrados = []
    errores = []

    for i, ruc in enumerate(rucs, 1):
        resultado = consultar_ruc(ruc)
        if resultado["encontrado"]:
            data = resultado["data"]
            encontrados.append({
                "ruc": ruc,
                "razon_social": data.get("razonSocial", ""),
                "estado_contribuyente": data.get("estadoContribuyente", ""),
                "condicion_domicilio": data.get("condicionDomicilio", ""),
                "ubigeo": data.get("ubigeo", ""),
                "direccion": data.get("direccion", ""),
                "fuentes": sin_sunat[sin_sunat["ruc"] == ruc]["fuentes"].values[0] if ruc in sin_sunat["ruc"].values else "",
                "nombre": sin_sunat[sin_sunat["ruc"] == ruc]["nombre"].values[0] if ruc in sin_sunat["ruc"].values else "",
            })
        elif resultado.get("not_found"):
            no_encontrados.append({
                "ruc": ruc,
                "fuentes": sin_sunat[sin_sunat["ruc"] == ruc]["fuentes"].values[0] if ruc in sin_sunat["ruc"].values else "",
                "nombre": sin_sunat[sin_sunat["ruc"] == ruc]["nombre"].values[0] if ruc in sin_sunat["ruc"].values else "",
            })
        else:
            errores.append({"ruc": ruc, "error": resultado.get("error", f"status {resultado.get('status')}")})

        # Progress cada 20 RUCs
        if i % 20 == 0 or i == len(rucs):
            print(f"  [{i}/{len(rucs)}] Encontrados: {len(encontrados)}, No hallados: {len(no_encontrados)}, Errores: {len(errores)}")

        # Rate limit suave
        time.sleep(0.1)

    print()
    print("=== RESULTADO ===")
    print(f"Encontrados en SUNAT:  {len(encontrados)}")
    print(f"No hallados en padrón: {len(no_encontrados)}")
    print(f"Errores de consulta:   {len(errores)}")
    print()

    # Guardar CSVs
    if encontrados:
        df_encontrados = pd.DataFrame(encontrados)
        df_encontrados.to_csv("data/SUNAT_batch_encontrados.csv", sep="|", index=False)
        print(f"Guardado: data/SUNAT_batch_encontrados.csv ({len(encontrados)} filas)")

        # Mostrar resumen estados
        print()
        print("Estados encontrados:")
        print(df_encontrados["estado_contribuyente"].value_counts().to_string())
        print()
        print("Condiciones de domicilio:")
        print(df_encontrados["condicion_domicilio"].value_counts().to_string())

    if no_encontrados:
        df_no = pd.DataFrame(no_encontrados)
        df_no.to_csv("data/SUNAT_batch_no_encontrados.csv", sep="|", index=False)
        print(f"\nGuardado: data/SUNAT_batch_no_encontrados.csv ({len(no_encontrados)} filas)")

    if errores:
        df_err = pd.DataFrame(errores)
        df_err.to_csv("data/SUNAT_batch_errores.csv", sep="|", index=False)
        print(f"\nGuardado: data/SUNAT_batch_errores.csv ({len(errores)} filas)")

if __name__ == "__main__":
    main()
