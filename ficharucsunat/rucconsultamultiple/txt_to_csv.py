import csv
import os
import sys

DIR = r"C:\Users\acuba\eudrperu\ficharucsunat\rucconsultamultiple"


def to_csv(src_name, dst_name, header):
    sp = os.path.join(DIR, src_name)
    if not os.path.exists(sp):
        sp = os.path.join(DIR, os.path.splitext(src_name)[0] + ".txt")
    if not os.path.exists(sp):
        print("MISSING", src_name)
        return 0
    dst = os.path.join(DIR, dst_name)
    rows = [ln.strip().rstrip("|").strip() for ln in open(sp, encoding="utf-8") if ln.strip()]
    with open(dst, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows((r,) for r in rows)
    print(f"{src_name} -> {dst_name} | rows={len(rows)}")
    return len(rows)


def main():
    to_csv("rucs_lote_01.txt", "rucs_lote_01.csv", ["numero_ruc"])
    to_csv("rucs_lote_02.txt", "rucs_lote_02.csv", ["numero_ruc"])
    to_csv("rucs_consulta_5.txt", "rucs_consulta_5.csv", ["numero_ruc"])


if __name__ == "__main__":
    sys.exit(main())
