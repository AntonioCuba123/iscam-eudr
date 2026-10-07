"""
Retry de 46 RUCs que recibieron 429 - delay 1s entre consultas.
"""
import pandas as pd
import urllib.request
import urllib.error
import json
import time

BASE_URL = "http://localhost:4006/api/contribuyentes"

def consultar_ruc(ruc: str) -> dict:
    url = f"{BASE_URL}/{ruc}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            if resp.status == 200:
                return {"ruc": ruc, "encontrado": True, "data": json.loads(resp.read())}
            return {"ruc": ruc, "encontrado": False, "status": resp.status, "data": None}
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"ruc": ruc, "encontrado": False, "status": 404, "data": None, "not_found": True}
        return {"ruc": ruc, "encontrado": False, "status": e.code, "data": None, "error": str(e)}
    except Exception as e:
        return {"ruc": ruc, "encontrado": False, "status": None, "data": None, "error": str(e)}

def main():
    err = pd.read_csv("data/SUNAT_batch_errores.csv", sep="|", dtype=str)
    rucs = err["ruc"].dropna().tolist()
    print(f"Reintentando {len(rucs)} RUCs con delay 1s...")

    encontrados = []
    no_encontrados = []
    errores = []

    for i, ruc in enumerate(rucs, 1):
        resultado = consultar_ruc(ruc)
        time.sleep(1.0)  # delay mayor para evitar 429
        if resultado["encontrado"]:
            data = resultado["data"]
            encontrados.append({
                "ruc": ruc,
                "razon_social": data.get("razonSocial", ""),
                "estado_contribuyente": data.get("estadoContribuyente", ""),
                "condicion_domicilio": data.get("condicionDomicilio", ""),
                "ubigeo": data.get("ubigeo", ""),
                "direccion": data.get("direccion", ""),
            })
        elif resultado.get("not_found"):
            no_encontrados.append({"ruc": ruc})
        else:
            errores.append({"ruc": ruc, "error": resultado.get("error", f"status {resultado.get('status')}")})

        print(f"  [{i}/{len(rucs)}] OK: {len(encontrados)} | No hallados: {len(no_encontrados)} | Errores: {len(errores)}")

    print()
    print("=== RESULTADO RETRY ===")
    print(f"Encontrados: {len(encontrados)}, No hallados: {len(no_encontrados)}, Errores: {len(errores)}")

    if errores:
        df_err = pd.DataFrame(errores)
        df_err.to_csv("data/SUNAT_batch_errores_final.csv", sep="|", index=False)
        print(f"Errores finales: data/SUNAT_batch_errores_final.csv")
        print(errores)

    # Cruzar al universo consolidado
    if encontrados:
        df_encontrados = pd.DataFrame(encontrados)
        df_encontrados.to_csv("data/SUNAT_batch_encontrados_retry.csv", sep="|", index=False)
        print(f"Encontrados retry: data/SUNAT_batch_encontrados_retry.csv")

        df = pd.read_csv("data/EUDRPERU_universo_consolidado.csv", sep="|", dtype=str)
        for _, row in df_encontrados.iterrows():
            mask = df["ruc"] == row["ruc"]
            if mask.any():
                df.loc[mask, "sunat_estado"] = row["estado_contribuyente"]
                df.loc[mask, "sunat_domicilio"] = row["condicion_domicilio"]
        df.to_csv("data/EUDRPERU_universo_consolidado.csv", sep="|", index=False)

        total = len(df)
        sin_estado = df["sunat_estado"].isna().sum()
        print(f"\nCobertura final: {total - sin_estado}/{total} ({100*(total-sin_estado)/total:.0f}%)")

if __name__ == "__main__":
    main()
