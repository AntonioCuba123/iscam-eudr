import os
import pandas as pd

DIR = r"C:\Users\acuba\eudrperu\ficharucsunat\ppaconsultamultiple"
SRC = [
    os.path.join(DIR, "resultado_consulta_padron.csv"),
    os.path.join(DIR, "resultado_consulta_padron (1).csv"),
]
DST = os.path.join(DIR, "resultado_padron_consolidado.xlsx")


def main():
    parts = []
    for s in SRC:
        if not os.path.exists(s):
            print("MISSING", s)
            continue
        parts.append(pd.read_csv(s, dtype={"tipo_doc": str, "nro_doc": str, "en_padron": str}))

    df = pd.concat(parts, ignore_index=True)
    df["nro_doc"] = df["nro_doc"].str.strip()
    total = len(df)
    dup = df.duplicated(subset=["tipo_doc", "nro_doc"], keep=False)
    n_dup = int(dup.sum())

    df = df.drop_duplicates(subset=["tipo_doc", "nro_doc"], keep="first").reset_index(drop=True)

    df.to_excel(DST, index=False, sheet_name="Resultado", engine="openpyxl")

    print(
        f"orig rows={total} | dup_rows={n_dup} | final rows={len(df)} | "
        f"en_padron SI={int((df['en_padron']=='SI').sum())} NO={int((df['en_padron']=='NO').sum())} | out={DST}"
    )


if __name__ == "__main__":
    main()
