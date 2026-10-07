import os
import csv
import pandas as pd

DIR = r"C:\Users\acuba\eudrperu\ficharucsunat"
SRC_DIR = r"C:\Users\acuba\eudrperu\ficharucsunat\rucconsultamultiple"
PPA_DIR = r"C:\Users\acuba\eudrperu\ficharucsunat\ppaconsultamultiple"
os.makedirs(PPA_DIR, exist_ok=True)

SOURCES = [
    os.path.join(SRC_DIR, "rucs_consulta.txt"),
    os.path.join(SRC_DIR, "rucs_consulta_2.txt"),
    os.path.join(SRC_DIR, "rucs_consulta_3.txt"),
    os.path.join(SRC_DIR, "rucs_consulta_4.txt"),
]
MASTER_TXT = os.path.join(PPA_DIR, "rucs_a_consultar.txt")
MASTER_XLSX = os.path.join(PPA_DIR, "rucs_a_consultar.xlsx")
HEADER = ["tipo_doc", "nro_doc"]
BATCH = 100


def collect():
    order = []
    seen = set()
    for s in SOURCES:
        if not os.path.exists(s):
            print("MISSING", s)
            continue
        with open(s, encoding="utf-8") as fh:
            for ln in fh:
                r = ln.strip().rstrip("|").strip()
                if len(r) == 11 and r.isdigit() and r not in seen:
                    seen.add(r)
                    order.append(r)
    return order


def main():
    rucs = collect()

    with open(MASTER_TXT, "w", encoding="utf-8", newline="") as fh:
        for r in rucs:
            fh.write(f"{r}|\n")

    with open(MASTER_TXT, "r", encoding="utf-8") as fh:
        rows = [(ln.strip().rstrip("|").strip(),) for ln in fh if ln.strip()]

    for i in range(0, len(rows), BATCH):
        chunk = rows[i : i + BATCH]
        n = i // BATCH + 1
        txt = os.path.join(PPA_DIR, f"rucs_lote_{n:02d}.txt")
        csvf = os.path.join(PPA_DIR, f"rucs_lote_{n:02d}.csv")
        with open(txt, "w", encoding="utf-8", newline="") as f:
            for (r,) in chunk:
                f.write(f"{r}|\n")
        with open(csvf, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow(HEADER)
            w.writerows(("RUC", r) for (r,) in chunk)

    out = pd.DataFrame({"tipo_doc": ["RUC"] * len(rows), "nro_doc": [r for (r,) in rows]})
    out.to_csv(os.path.join(PPA_DIR, "rucs_a_consultar.csv"), index=False, encoding="utf-8-sig")
    out.to_excel(MASTER_XLSX, index=False, sheet_name="RUC", engine="openpyxl")

    print(f"master rucs: {len(rows)}  (txt+csv+xlsx)")
    for i in range(0, len(rows), BATCH):
        n = i // BATCH + 1
        print(f"  lote_{n:02d}: {len(rows[i:i+BATCH])} rucs  (rucs_lote_{n:02d}.txt + .csv)")


if __name__ == "__main__":
    main()
