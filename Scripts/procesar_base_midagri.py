"""
Script para procesar, limpiar y estandarizar la base de datos de MIDAGRI / AGROMERCADO
y cruzarla con los datos tributarios (SUNAT) y órganos de administración (OECE).

Genera:
- data/midagri_cafe_cacao_limpio.xlsx
- data/midagri_cafe_cacao_limpio.csv
- data/resumen_universo_midagri.json
"""

import os
import re
import json
import pandas as pd
import numpy as np

FILE_EXCEL = "3 directorio - base de datos de los excels de midagri 06.10.26.xlsx"
OUTPUT_DIR = "data"

def clean_ruc(val):
    if pd.isna(val):
        return ""
    val_str = str(val).strip()
    # Extraer dígitos
    digits = re.sub(r"\D", "", val_str)
    return digits if len(digits) == 11 else val_str

def parse_eudr_progress(val):
    if pd.isna(val):
        return np.nan
    val_str = str(val).strip()
    # Si es porcentaje tipo '50 %' o '64.8%'
    match_pct = re.search(r"(\d+(\.\d+)?)\s*%", val_str)
    if match_pct:
        return round(float(match_pct.group(1)) / 100.0, 4)
    # Si es número decimal tipo '0.75' o '1'
    try:
        val_float = float(val_str)
        if 0.0 <= val_float <= 1.0:
            return round(val_float, 4)
        elif 1.0 < val_float <= 100.0:
            return round(val_float / 100.0, 4)
    except ValueError:
        pass
    return np.nan

def main():
    print(">>> Leyendo hoja 'base cafe cacao'...")
    df = pd.read_excel(FILE_EXCEL, sheet_name="base cafe cacao")
    
    # 1. Limpieza de RUC
    df["RUC_limpio"] = df["RUC"].apply(clean_ruc)
    
    # 2. Normalización de Producto
    df["producto_normalizado"] = df["Producto Dom"].astype(str).str.strip().str.upper()
    df["producto_normalizado"] = df["producto_normalizado"].replace({
        "CAFE": "CAFÉ",
        "CAFE VERDE": "CAFÉ",
        "CAFE PERGAMINO": "CAFÉ",
        "CACAO EN GRANO": "CACAO"
    })
    
    # Filtrar estrictamente café y cacao
    es_cafe_cacao = df["producto_normalizado"].isin(["CAFÉ", "CACAO"])
    df_filtrado = df[es_cafe_cacao].copy()
    
    # 3. Normalización de Tipo de Organización
    df_filtrado["tipo_org_normalizado"] = df_filtrado["Tipo de Organización"].astype(str).str.strip()
    df_filtrado["es_cooperativa"] = df_filtrado["tipo_org_normalizado"].str.contains("Cooperativa", case=False, na=False)
    
    # 4. Estado y Condición SUNAT
    df_filtrado["estado_sunat_norm"] = df_filtrado["Estado SUNAT"].astype(str).str.strip().str.upper()
    df_filtrado["condicion_sunat_norm"] = df_filtrado["Condición SUNAT"].astype(str).str.strip().str.upper()
    df_filtrado["activo_y_habido"] = (
        (df_filtrado["estado_sunat_norm"] == "ACTIVO") &
        (df_filtrado["condicion_sunat_norm"] == "HABIDO")
    )
    
    # 5. Estandarización de avance EUDR
    df_filtrado["avance_eudr_num"] = df_filtrado["Indicar el avance con el reglamento de la EUDR"].apply(parse_eudr_progress)
    
    # 6. Estandarización de Exporta SÍ/NO
    df_filtrado["exporta_flag"] = df_filtrado["Exporta SÍ/NO"].astype(str).str.strip().str.upper()
    df_filtrado["exporta_flag"] = df_filtrado["exporta_flag"].replace({"SI": "SÍ", "NAN": np.nan, "": np.nan})
    
    # 7. Resumen estadístico
    resumen = {
        "total_organizaciones_originales": len(df),
        "total_cafe_y_cacao": len(df_filtrado),
        "total_cafe": int((df_filtrado["producto_normalizado"] == "CAFÉ").sum()),
        "total_cacao": int((df_filtrado["producto_normalizado"] == "CACAO").sum()),
        "total_cooperativas": int(df_filtrado["es_cooperativa"].sum()),
        "total_asociaciones": int((~df_filtrado["es_cooperativa"]).sum()),
        "total_activas_y_habidas": int(df_filtrado["activo_y_habido"].sum()),
        "cooperativas_activas_habidas": int((df_filtrado["es_cooperativa"] & df_filtrado["activo_y_habido"]).sum()),
        "con_avance_eudr_declarado": int(df_filtrado["avance_eudr_num"].notna().sum()),
        "promedio_avance_eudr_declarado": float(df_filtrado["avance_eudr_num"].mean()) if df_filtrado["avance_eudr_num"].notna().sum() > 0 else 0.0
    }
    
    print("\n>>> RESUMEN DEL UNIVERSO MIDAGRI / PAC (CAFÉ Y CACAO):")
    for k, v in resumen.items():
        print(f"  - {k}: {v}")
        
    # Guardar salidas
    output_excel = os.path.join(OUTPUT_DIR, "midagri_cafe_cacao_limpio.xlsx")
    output_csv = os.path.join(OUTPUT_DIR, "midagri_cafe_cacao_limpio.csv")
    output_json = os.path.join(OUTPUT_DIR, "resumen_universo_midagri.json")
    
    df_filtrado.to_excel(output_excel, index=False)
    df_filtrado.to_csv(output_csv, index=False, encoding="utf-8-sig")
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(resumen, f, indent=2, ensure_ascii=False)
        
    print(f"\n>>> Archivos generados exitosamente:")
    print(f"  [+] {output_excel}")
    print(f"  [+] {output_csv}")
    print(f"  [+] {output_json}")

if __name__ == "__main__":
    main()
